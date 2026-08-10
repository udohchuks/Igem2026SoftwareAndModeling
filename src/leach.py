"""Part I — Bioleaching.

Implements the five coupled sections of "Bioleaching Models.docx":

  1. Enzyme production      d[E]/dt
  2. Tetrathionate          d[S4O6]/dt      Michaelis-Menten + Cu(II) regeneration
  3. Thiosulfate            d[S2O3]/dt      production - parasitic - Au - Cu draws
  4. Gold leaching          R_Au            Model A (O2 only) or Model B (O2 + Cu(II))
  5. Copper and Cu(I)/Cu(II) balance

Units: umol/L, minutes, mol for solid inventories, m and m^2 for geometry.

State vector, in order:
    [E, S4O6, S2O3, n_Au, Au_complex, n_Cu, Cu_I, Cu_II]

Two rate constants in the source table are given only as relative or
unmeasured values (k_cat, k_Au_Cu, k_Cu_O2, k_Cu_Cu, k1, k3, k4). They must be
supplied by the caller. Nothing is invented here.
"""

import numpy as np
from scipy.integrate import solve_ivp

STATES = ["E", "S4O6", "S2O3", "n_Au", "Au_complex", "n_Cu", "Cu_I", "Cu_II"]


def gold_area(m_Au, rho_Au, t_film):
    """Section 4 — A_Au = m_Au / (rho_Au * t_film).

    Gold on a PCB is a plated film. It thins at roughly constant face area
    until exhausted, so the area is a constant while gold remains.
    """
    return m_Au / (rho_Au * t_film)


def copper_area(A_Cu0, n_Cu, n_Cu0):
    """Section 5 — A_Cu(t) = A_Cu(0) * (n_Cu/n_Cu0)^(2/3).

    Copper is bulk metal and genuinely erodes inward, so area falls as the
    two-thirds power of the fraction remaining.
    """
    frac = max(n_Cu / n_Cu0, 0.0)
    return A_Cu0 * frac ** (2.0 / 3.0)


def copper_area_initial(m_Cu, rho_Cu, d):
    """Section 5 — A_Cu(0) = 6*m_Cu / (rho_Cu * d)."""
    return 6.0 * m_Cu / (rho_Cu * d)


def _mm(x, K):
    """Saturating Langmuir/Michaelis factor x/(K+x), clamped at zero."""
    x = max(x, 0.0)
    return x / (K + x)


def rhs(t, y, p, model="B"):
    """Right-hand side of the full leach system.

    model="A" uses the oxygen-only gold rate of section 4 Model A.
    model="B" adds the Cu(II) oxidant pathway of section 4 Model B, and uses
    the combined-oxidant copper rate v1B of section 5.
    """
    E, S4O6, S2O3, n_Au, Au_cplx, n_Cu, Cu_I, Cu_II = y
    V = p["V"]

    # --- 1. enzyme -------------------------------------------------------
    dE = p["k_syn"] * p["X"] - (p["k_deg"] + p["mu"]) * E

    # --- shared saturating factors ---------------------------------------
    f_S = _mm(S2O3, p["K_S"])
    f_O2 = _mm(p["O2"], p["K_O2"])
    f_Cu = _mm(Cu_II, p["K_Cu"])

    # --- 4. gold ---------------------------------------------------------
    A_Au = gold_area(p["m_Au"], p["rho_Au"], p["t_film"]) if n_Au > 0.0 else 0.0
    if model == "A":
        R_Au = p["k_Au_O2"] * A_Au * f_O2 * f_S
    else:
        R_Au = A_Au * f_S * (p["k_Au_O2"] * f_O2 + p["k_Au_Cu"] * f_Cu)

    # --- 5. copper -------------------------------------------------------
    A_Cu = copper_area(p["A_Cu0"], n_Cu, p["n_Cu0"]) if n_Cu > 0.0 else 0.0
    if model == "A":
        v1 = 2.0 * p["k_Cu_O2"] * A_Cu * f_O2 * f_S
    else:
        v1 = A_Cu * f_S * (2.0 * p["k_Cu_O2"] * f_O2 + 4.0 * p["k_Cu_Cu"] * f_Cu)
    v2 = R_Au
    v3 = p["k3"] * Cu_II * S2O3
    v4 = p["k4"] * p["O2"] * Cu_I

    # --- 2. tetrathionate ------------------------------------------------
    v_hyd = p["k_cat"] * E * _mm(S4O6, p["K_m"])
    dS4O6 = p["F_in"] - v_hyd + p["k1"] * Cu_II * S2O3

    # --- 3. thiosulfate --------------------------------------------------
    dS2O3 = v_hyd - 2.0 * p["k1"] * Cu_II * S2O3 - (2.0 / V) * R_Au - (1.0 / V) * v1

    # --- solid and dissolved inventories ---------------------------------
    dn_Au = -R_Au
    dAu_cplx = R_Au / V
    dn_Cu = -v1
    dCu_I = (1.0 / V) * 2.0 * v1 + (1.0 / V) * v2 + 2.0 * v3 - 4.0 * v4
    dCu_II = 4.0 * v4 - (1.0 / V) * v1 - (1.0 / V) * v2 - 2.0 * v3

    return [dE, dS4O6, dS2O3, dn_Au, dAu_cplx, dn_Cu, dCu_I, dCu_II]


def _gold_exhausted(t, y, p, model):
    """Event: solid gold reaches zero."""
    return y[3]


_gold_exhausted.terminal = True
_gold_exhausted.direction = -1


def _copper_exhausted(t, y, p, model):
    """Event: solid copper reaches zero."""
    return y[5]


_copper_exhausted.terminal = True
_copper_exhausted.direction = -1


def simulate(p, y0, t_end, n=2001, model="B", stop_at_exhaustion=True):
    """Integrate the leach. Returns (t, dict of state arrays).

    Section 4 makes the gold area a step function: constant while gold
    remains, zero once exhausted. That discontinuity is in the source model,
    not added here. Integrating straight through it makes the solver take
    vanishingly small steps, so by default the integration stops at the
    exhaustion point via a terminal event. The returned arrays are then
    shorter than `n`; check `t[-1]` against `t_end` to detect this.

    Pass stop_at_exhaustion=False to integrate through it anyway. Expect the
    call to be slow and the solid inventory to go slightly negative.
    """
    t_eval = np.linspace(0.0, t_end, n)
    events = [_gold_exhausted, _copper_exhausted] if stop_at_exhaustion else None
    sol = solve_ivp(rhs, (0.0, t_end), list(y0), args=(p, model),
                    t_eval=t_eval, rtol=1e-8, atol=1e-12, method="LSODA",
                    events=events)
    return sol.t, dict(zip(STATES, sol.y))


def gold_recovered_fraction(traj, n_Au0):
    """Fraction of the plated gold that has entered solution."""
    return 1.0 - traj["n_Au"] / n_Au0
