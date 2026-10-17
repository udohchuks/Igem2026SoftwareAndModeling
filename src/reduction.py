"""Conditional reduction trajectories with explicit gold and electron ledgers.

The linear-reference protein option is an unvalidated dose-scaling hypothesis.
The default retains the effective Finke-Watzky coefficients at each dose.
Neither option supplies a measured activity, active fraction, or mechanism.
"""
import numpy as np
from scipy.integrate import solve_ivp

from . import params


def _physical(name, value, positive=False):
    if not np.isfinite(value) or value < 0 or (positive and value == 0):
        raise ValueError(f"{name} must be finite and {'positive' if positive else 'non-negative'}")
    return value


def simulate(Au_aq0, p, t_end=None, *, times=None,
             protein_scaling="fixed_effective", E_ref=None,
             initial_reduced_fraction=1.0):
    """Return trajectories (uM, h), new-metal efficiency and balance residuals.

    ``p`` contains the existing reduction parameters plus explicit nu_rech.
    Initial protein is fully reduced unless a different fraction is supplied.
    The seed is additional metal and is never counted as newly reduced gold.
    ``times`` may be [t_end] for endpoint-only evaluation; its final time must
    equal t_end. No returned concentration or efficiency is clipped.
    """
    Au_aq0 = _physical("Au_aq0", Au_aq0)
    end = _physical("t_end", p["t_reduce_h"] if t_end is None else t_end)
    required = ("k_nuc", "k_grow", "k_ox", "k_rech", "Rech_0", "E_tot")
    q = {key: _physical(key, p[key]) for key in required}
    q.update({key: _physical(key, p[key], positive=True)
              for key in ("K_inh", "nu", "nu_rech")})
    fraction = _physical("initial_reduced_fraction", initial_reduced_fraction)
    if fraction > 1:
        raise ValueError("initial_reduced_fraction must not exceed one")
    if protein_scaling not in ("fixed_effective", "linear_reference"):
        raise ValueError("unknown protein_scaling")
    if protein_scaling == "linear_reference":
        if E_ref is None:
            raise KeyError("E_ref")
        denominator = _physical("E_ref", E_ref, positive=True)
    else:
        denominator = q["E_tot"]
    seed = (_physical("seed_frac", p["seed_frac"]) * Au_aq0
            if p.get("seeding_on", False) else 0.0)
    settings = params.values(params.load("reduction_solver")["solver"])
    if times is None:
        t = np.linspace(0, end, settings["points"]) if end else np.array([0.0])
    else:
        t = np.asarray(times, dtype=float)
        if (t.ndim != 1 or not t.size or not np.all(np.isfinite(t))
                or np.any(t < 0) or np.any(np.diff(t) <= 0) or t[-1] != end):
            raise ValueError("times must be finite, ordered, non-negative and end at t_end")
    initial_red = q["E_tot"] * fraction
    initial = np.array([Au_aq0, seed, initial_red, q["Rech_0"], 0.0])

    def rhs(time, y):
        # Evaluate rates in the physical domain at solver trial states only.
        # Raw integrated states are returned and checked below.
        a, b, e, r, loss = y
        a, b, r = max(a, 0), max(b, 0), max(r, 0)
        e = min(max(e, 0), q["E_tot"])
        v = ((q["k_nuc"] + q["k_grow"]*b)*a*e/denominator
             if denominator else 0.0)
        recharge = q["k_rech"]*(q["E_tot"]-e)*r/(1+a/q["K_inh"])
        oxidation = q["k_ox"]*e
        return [-v, v, -q["nu"]*v+recharge-oxidation,
                -q["nu_rech"]*recharge, oxidation]

    if end == 0:
        y = initial[:, None]
    else:
        solution = solve_ivp(rhs, (0, end), initial, t_eval=t, method="LSODA",
                             rtol=settings["rtol"], atol=settings["atol"])
        if not solution.success:
            raise RuntimeError("reduction integration failed: " + solution.message)
        y = solution.y
    a, b, e, r, loss = y
    new = b-seed
    gold_residual = a+b-Au_aq0-seed
    budget = initial_red+q["Rech_0"]/q["nu_rech"]
    electron_residual = e+r/q["nu_rech"]+q["nu"]*new+loss-budget
    gold_tolerance = settings["check_factor"]*(settings["atol"]+settings["rtol"]*(Au_aq0+seed))
    electron_tolerance = settings["check_factor"]*(settings["atol"]+settings["rtol"]*budget)
    protein_tolerance = settings["check_factor"]*(settings["atol"]+settings["rtol"]*q["E_tot"])
    if (not np.all(np.isfinite(y)) or min(np.min(a), np.min(b)) < -gold_tolerance
            or min(np.min(e), np.min(q["E_tot"]-e)) < -protein_tolerance
            or min(np.min(r/q["nu_rech"]), np.min(loss)) < -electron_tolerance
            or np.min(new) < -gold_tolerance or np.max(new-Au_aq0) > gold_tolerance
            or np.max(np.abs(gold_residual)) > gold_tolerance
            or np.max(np.abs(electron_residual)) > electron_tolerance):
        raise RuntimeError("reduction trajectory violates physical bounds or conservation")
    return dict(t_h=t, Au_aq=a, Au_s=b, metal_new=new, E_red=e,
                E_ox=q["E_tot"]-e, Rech=r, oxidation_loss=loss,
                gold_residual=gold_residual, electron_residual=electron_residual,
                eta_reduce=float(new[-1]/Au_aq0) if Au_aq0 else 0.0,
                donor_ceiling=min(1.0, budget/(q["nu"]*Au_aq0)) if Au_aq0 else 0.0)
