"""Arm B: a provisional expression cascade coupled to logistic biomass.

Biomass grows at g = mu_eff*(1-X/X_cap), and g is the dilution term in
both per-cell equations. The old maximum-rate dilution at stationary biomass
violated the total-molecule balance (ISSUES 87). Minutes are used internally.

Expression after growth stops is not calibrated. Constant synthesis can give
unphysical late yields at the upper proxy and has no finite plateau for zero
protein decay. Simulated maxima are not validated harvest optima. The
alpha_N_beta proxy requires refitting after the dilution correction.
"""

import numpy as np
from scipy.integrate import solve_ivp
from . import params


CASCADE_KEYS = ("alpha", "N", "beta", "delta_c")
LUMP_KEY = "alpha_N_beta"


def lumped_group(cascade):
    """alpha * N * beta, the only combination of the three the model can see.

    The cascade's steady state is

        P_c* = alpha*N*beta / ((delta_m + mu) * (delta_c + mu))

    so the three appear as one product and no protein measurement separates
    them. Raue et al. 2009 calls this structural non-identifiability; the
    prescribed treatment is to lump the group and estimate the lump, which is
    what params/recovery_chain.yaml now carries. ISSUES.md item 67.
    """
    return cascade["alpha"] * cascade["N"] * cascade["beta"]


def cascade_from_lumped(anb, expression_params, delta_c=None):
    """Cascade constants carrying `anb` as one number rather than three.

    alpha takes the whole group and N and beta are set to 1. This is EXACT,
    not an approximation: only the product enters, so protein per cell is
    reproduced to about 3e-8, which is integrator noise. The module's tests
    pin that.

    The one thing it does not reproduce is the mRNA series, which is rescaled
    by the same factor. `m` from such a run is bookkeeping, not a prediction,
    and nothing in this repository reads it.
    """
    e = expression_params
    return {"alpha": float(anb), "N": 1.0, "beta": 1.0,
            "delta_m": e["delta_m"]["value"],
            "delta_c": e["delta_c"]["value"] if delta_c is None else delta_c,
            "k_sec": 0.0}


def golb_proxy_cascade(expression_params, construct=None):
    """Part II's GolB cascade constants, with secretion switched off.

    A PROXY where the construct's own value is missing. The reductase is a
    different protein under a different promoter; only its topology is known
    to match, in that it stays cytoplasmic. Returns the constants the cascade
    needs, with k_sec set to zero because nothing is displayed.

    Pass `construct` -- the reagent_arm block of params/recovery_chain.yaml --
    and any of alpha, N, beta or delta_c that carries a real value there
    replaces GolB's. As of 2026-08-20 that is N alone: the team reported a
    pET-24(+) backbone, so the copy number is the construct's own and the rest
    are still borrowed. ISSUES.md item 67.

    Without `construct` this returns the pure proxy, which is what it always
    returned. ISSUES.md item 48 keeps the remaining constants null for the
    real construct. This function exists so the timing question can be
    answered before they are measured, not so the nulls can be filled in.
    """
    e = expression_params
    out = {"alpha": e["alpha"]["value"], "N": e["N"]["value"],
           "beta": e["beta"]["value"], "delta_m": e["delta_m"]["value"],
           "delta_c": e["delta_c"]["value"], "k_sec": 0.0}
    if construct is not None:
        anb = construct.get(LUMP_KEY, {}).get("value")
        if anb is not None:
            # The lump wins over the three separately, and over GolB's. It is
            # the only form the construct's own expression is carried in.
            out.update(cascade_from_lumped(anb, expression_params,
                                           delta_c=out["delta_c"]))
        for k in CASCADE_KEYS:
            own = construct.get(k, {}).get("value")
            if own is not None:
                if anb is not None and k in ("alpha", "N", "beta"):
                    raise ValueError(
                        "%s carries a value alongside %s. They are not "
                        "separately identifiable; keep the lump only."
                        % (k, LUMP_KEY))
                out[k] = own
    return out


def borrowed_keys(expression_params, construct):
    """Which cascade constants are still GolB's rather than the construct's.

    The point of a labelled proxy is that the label travels with it. Anything
    listed here is a borrowed number and any absolute yield resting on it is
    an order of magnitude, not a prediction.

    When the construct carries the lump, alpha, N and beta are supplied by it
    and are not reported as borrowed -- the lump itself is still a proxy, and
    says so in its own note, but it is the construct's proxy and not GolB's.
    """
    supplied = set()
    if construct.get(LUMP_KEY, {}).get("value") is not None:
        supplied = {"alpha", "N", "beta"}
    return tuple(k for k in CASCADE_KEYS
                 if k not in supplied
                 and construct.get(k, {}).get("value") is None)


def simulate(p, t_end_min=1440.0, n=2881):
    """Grow, induce, express. Returns a dict of time series.

    p needs, in minutes and g/L:
        mu, X_cap, X_0, X_ind, burden
        alpha, N, beta, delta_m, delta_c
        M_r, cells_per_g, N_A

    Keys returned: t_min, t_h, X, m, P_c, C_prot, induced_at_min.
    """
    mu, X_cap, burden = p["mu"], p["X_cap"], p["burden"]
    X_ind = p["X_ind"]

    def mu_eff(X, induced):
        return mu * (1.0 - burden) if induced else mu

    def rhs(t, y):
        X, m, P_c = y
        X = min(max(X, 0.0), X_cap)
        induced = X >= X_ind
        me = mu_eff(X, induced)
        dX = me * X * (1.0 - X / X_cap)
        induction = 1.0 if induced else 0.0
        # Per-cell dilution is the ACTUAL specific growth rate dX/(X dt),
        # not its maximum. Otherwise molecules disappear even at constant
        # biomass. ISSUES 87. This does not supply stationary-phase synthesis
        # regulation; absolute late yields still need calibration.
        dilution = me * (1.0 - X / X_cap)
        dm = p["alpha"] * p["N"] * induction - (p["delta_m"] + dilution) * m
        dP_c = p["beta"] * m - (p["delta_c"] + dilution) * P_c
        return [dX, dm, dP_c]

    # atol MUST be scaled to each state or the integrator stalls. X is order 1,
    # but m and P_c are molecules per cell and run to 1e4 and 1e7. A flat
    # atol = 1e-12 asks LSODA for nineteen significant figures on P_c, the step
    # size collapses, and the call never returns. It never bit while the
    # expression constants were narrow; it bit the moment the alpha_N_beta band
    # reached its Studier ceiling. Found and fixed 2026-08-20, ISSUES.md 67.
    #
    # The scales are the analytic steady states, so this is the size the states
    # actually reach and not a fudge factor.
    m_scale = max(p["alpha"] * p["N"] / (p["delta_m"] + mu), 1.0)
    P_scale = max(p["beta"] * m_scale / (p["delta_c"] + mu), 1.0)
    atol = [1e-12, 1e-9 * m_scale, 1e-9 * P_scale]

    t_eval = np.linspace(0.0, t_end_min, n)
    sol = solve_ivp(rhs, (0.0, t_end_min), [p["X_0"], 0.0, 0.0],
                    t_eval=t_eval, rtol=1e-8, atol=atol, method="LSODA")
    if not sol.success:
        raise RuntimeError("reductase integration failed: " + sol.message)
    t, X, m, P_c = sol.t, sol.y[0], sol.y[1], sol.y[2]

    # molecules/cell -> g/L. cells_per_g is dry weight, X is dry weight per L.
    C_prot = P_c * X * p["cells_per_g"] / p["N_A"] * p["M_r"]

    induced = np.flatnonzero(X >= X_ind)
    t_ind = float(t[induced[0]]) if induced.size else float("nan")

    return {"t_min": t, "t_h": t / 60.0, "X": X, "m": m, "P_c": P_c,
            "C_prot": C_prot, "induced_at_min": t_ind}


def harvest_time(p, t_end_min=1440.0, n=2881):
    """Maximum simulated protein within the requested finite time window.

    This is a descriptive endpoint, not a validated harvest optimum. In a
    monotone trajectory its maximum can simply be the end of the simulation.
    Use measurements of active protein and stationary synthesis for scheduling.
    """
    s = simulate(p, t_end_min=t_end_min, n=n)
    i = int(np.argmax(s["C_prot"]))
    return {"t_harvest_h": float(s["t_h"][i]),
            "t_after_induction_h": float((s["t_min"][i] - s["induced_at_min"])
                                         / 60.0),
            "C_prot_g_per_L": float(s["C_prot"][i]),
            "P_c": float(s["P_c"][i]), "X": float(s["X"][i]),
            "induced_at_h": float(s["induced_at_min"] / 60.0)}


def yield_at(p, t_h, t_end_min=1440.0, n=2881):
    """Volumetric protein, g/L, within the simulated wall-clock window.

    Times outside the window are unknown, not the nearest endpoint yield.
    Compare in hours so converting a valid floating-point endpoint back to
    minutes cannot spuriously put it beyond the simulation.
    """
    minutes_per_hour = params.values(params.load("conversions"))["minutes_per_hour"]
    end_h = t_end_min / minutes_per_hour
    if (not np.isfinite(t_h) or not np.isfinite(end_h)
            or t_h < 0.0 or t_h > end_h):
        raise ValueError("yield time must be finite and within the simulated window in hours")
    s = simulate(p, t_end_min=t_end_min, n=n)
    return float(np.interp(t_h, s["t_min"] / minutes_per_hour, s["C_prot"]))


def cost_of_mistiming(p, hours, t_end_min=1440.0, n=2881):
    """Fraction of the peak yield retained if lysis happens `hours` early/late.

    `hours` may be negative, but every resulting absolute harvest time must
    lie within the simulated window; otherwise ValueError is raised. Returns
    {hours: fraction of peak}. This describes the finite simulation, not a
    validated harvest schedule.
    """
    best = harvest_time(p, t_end_min=t_end_min, n=n)
    out = {}
    for h in hours:
        out[h] = yield_at(p, best["t_harvest_h"] + h,
                          t_end_min=t_end_min, n=n) / best["C_prot_g_per_L"]
    return out


def harvest_time_is_robust(p, factors=(0.1, 0.5, 2.0, 10.0), tol_h=1.0):
    """Does the time to a fraction of the analytic plateau move?

    Unreached or nonexistent plateaus make the result non-robust. A shared
    simulation endpoint is not evidence of timing robustness.

    alpha, N and beta are unmeasured for this construct and enter dP_c/dt
    linearly, so scaling them scales P_c and C_prot by the same factor without
    changing the shape in time. delta_c does change the shape. This scales each
    in turn and reports the spread of harvest times.

    Returns {"t_h": [...], "spread_h": float, "robust": bool}.
    """
    times = []
    fraction = params.values(params.load("recovery_audit")["verification"])["plateau_fraction"]
    for name in ("alpha", "N", "beta", "delta_c"):
        for f in factors:
            q = dict(p)
            q[name] = p[name] * f
            s = simulate(q)
            if q["delta_c"] <= 0.0:
                times.append(float("inf"))
                continue
            plateau = (lumped_group(q) / (q["delta_m"] * q["delta_c"])
                       * q["X_cap"] * q["cells_per_g"] / q["N_A"] * q["M_r"])
            reached = np.flatnonzero(s["C_prot"] >= fraction * plateau)
            times.append(float(s["t_h"][reached[0]]) if reached.size else float("inf"))
    if not np.all(np.isfinite(times)):
        return {"t_h": times, "spread_h": float("inf"), "robust": False}
    spread = float(max(times) - min(times))
    return {"t_h": times, "spread_h": spread, "robust": spread <= tol_h}


def lysate_g_per_L(C_prot, lysis_yield, concentration_factor):
    """What reaches the mixing vessel: lysis loses some, concentration recovers.

    C_lysate = C_prot * lysis_yield * concentration_factor
    """
    return C_prot * lysis_yield * concentration_factor


def uM_from_g_per_L(c_g_per_L, M_r):
    """g/L to uM for a protein of relative molecular mass M_r."""
    return c_g_per_L / M_r * 1e6
