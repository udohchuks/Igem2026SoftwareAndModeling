"""Part II — GolB surface site density.

Implements the cascade of "GolB_model_writeup.docx" sections 3, 5 and 6:

    m -> P_c -> P_s -> A = f * P_s

    dm/dt   = alpha*N - (delta_m + mu)*m
    dPc/dt  = beta*m  - (k_sec + delta_c + mu)*Pc
    dPs/dt  = k_sec*Pc*(1 - Ps/Ps_max) - (delta_s + mu)*Ps
    A       = f*Ps

Units: molecules per cell, minutes.
"""

import numpy as np
from scipy.integrate import solve_ivp


def rhs(t, y, p):
    """Right-hand side of the three-pool cascade. y = [m, P_c, P_s]."""
    m, Pc, Ps = y
    dm = p["alpha"] * p["N"] - (p["delta_m"] + p["mu"]) * m
    dPc = p["beta"] * m - (p["k_sec"] + p["delta_c"] + p["mu"]) * Pc
    dPs = p["k_sec"] * Pc * (1.0 - Ps / p["P_s_max"]) - (p["delta_s"] + p["mu"]) * Ps
    return [dm, dPc, dPs]


def simulate(p, t_end=400.0, n=801, y0=(0.0, 0.0, 0.0)):
    """Integrate the cascade. Returns (t, m, Pc, Ps, A)."""
    t_eval = np.linspace(0.0, t_end, n)
    sol = solve_ivp(rhs, (0.0, t_end), list(y0), args=(p,),
                    t_eval=t_eval, rtol=1e-9, atol=1e-12, method="LSODA")
    m, Pc, Ps = sol.y
    return sol.t, m, Pc, Ps, p["f"] * Ps


def steady_state(p):
    """Closed form WITH the anchor-capacity bracket. Use this one.

        m*  = alpha*N / (delta_m + mu)
        Pc* = beta*m* / (k_sec + delta_c + mu)
        J   = k_sec*Pc*                        the export flux
        Ps* = J / (J/P_s_max + delta_s + mu)
        A*  = f*Ps*

    It stays closed-form because Pc is decoupled from Ps: nothing downstream
    of the membrane feeds back on the cytoplasm. Crowding simply adds one more
    first-order escape route, the J/P_s_max term in the denominator.

    THIS REPRODUCES THE ODE EXACTLY, to 1e-14. `steady_state_linear` does not,
    and the gap between them is ISSUES.md item 3: Part II reported P_s from
    the ODE and A from the linear closed form, so its own numbers disagreed by
    5.5 %. They were never inconsistent, they were two different calculations.
    Supplying this form closes that item.

    The bracket is not a correction any more. At N = 300 the linear form
    overpredicts surface protein by 87 %, and beyond N = 350 it predicts more
    protein on the membrane than the membrane physically holds.
    """
    m = p["alpha"] * p["N"] / (p["delta_m"] + p["mu"])
    Pc = p["beta"] * m / (p["k_sec"] + p["delta_c"] + p["mu"])
    J = p["k_sec"] * Pc
    Ps = J / (J / p["P_s_max"] + p["delta_s"] + p["mu"])
    return {"m": m, "P_c": Pc, "P_s": Ps, "A": p["f"] * Ps, "J": J}


def steady_state_linear(p):
    """The non-saturating limit. RETAINED FOR COMPARISON, NOT FOR PREDICTION.

        A* = f*alpha*N*beta*k_sec
             / [(delta_m + mu)(k_sec + delta_c + mu)(delta_s + mu)]

    This was the repository's only closed form until 2026-08-19. It is elegant
    and it makes the design logic visible -- site density scales directly with
    promoter strength, copy number, translation strength and folding fraction
    -- but it is valid only while occupancy stays low.

        N      linear P_s    true P_s    error
        20          5,818       5,498      5.8 %
        100        29,091      22,535       29 %
        300        87,273      46,602       87 %
        350       101,818      50,450    exceeds P_s_max: impossible

    Below about N = 50 the two agree and the old reasoning is sound. The
    project moved to a pUC-type backbone, so it no longer applies.
    """
    m = p["alpha"] * p["N"] / (p["delta_m"] + p["mu"])
    Pc = p["beta"] * m / (p["k_sec"] + p["delta_c"] + p["mu"])
    Ps = p["k_sec"] * Pc / (p["delta_s"] + p["mu"])
    return {"m": m, "P_c": Pc, "P_s": Ps, "A": p["f"] * Ps}


def volumetric_capture(p, t_hours, mu=None):
    """Total sites per litre, which is what a process actually recovers.

    Returns (sites_per_cell, relative_biomass, product). Biomass is exp(mu*t)
    from a common starting point, so only ratios between calls mean anything.

    THIS EXISTS TO STOP ONE SPECIFIC MISREADING. `normalised_sensitivity`
    makes mu the largest negative term, which invites the conclusion that mild
    stress -- cooler, leaner, off-pH -- raises capture. It does the opposite:

        mu      doubling   sites/cell   biomass at 8 h   total capture
        0.005      139 min      36,342             x11         x0.001
        0.010       69 min      31,177            x122         x0.011
        0.020       35 min      23,301         x14,765      x1 (reference)
        0.030       23 min      17,786      x1,794,075            x93

    Slowing growth four-fold raises per-cell density 1.6x and cuts capture per
    litre about a thousand-fold. Growth wins, overwhelmingly and always.

    The design resolution is to separate the two stages in time: grow and
    express in rich medium where mu and expression are both high, then harvest
    and resuspend the cells in the leachate, where mu is about zero and the
    site count is whatever was built beforehand. That reframes the steady
    state above as a PRE-LOAD TARGET reached in a separate vessel, not a
    condition held in the leach liquor -- where it could not be held anyway.
    """
    import math

    q = dict(p) if mu is None else dict(p, mu=mu)
    A = steady_state(q)["A"]
    biomass = math.exp(q["mu"] * t_hours * 60.0)
    return A, biomass, A * biomass


def langmuir_uptake(C, A, K_Au):
    """Section 6 — gold ions bound per cell at leachate concentration C.

        q(C) = A*C / (K_Au + C)

    C and K_Au in uM. One site binds one Au(I) ion, so the plateau is A.
    """
    C = np.asarray(C, dtype=float)
    return A * C / (K_Au + C)


def normalised_sensitivity(p, symbol, eps=1e-4):
    """Fractional change in A* per fractional change in one parameter.

        S_p = (dA*/dp)(p/A*) = d ln A* / d ln p

    Increase p by 1 % and the site count changes by S_p percent. Raw
    derivatives cannot be compared -- dA/dN is sites per plasmid copy while
    dA/dmu is sites times minutes -- so normalising is what makes a ranking
    possible at all. These are LOCAL derivatives: a parameter with S = 0.53
    needs a 3.7-fold increase to double the site count, not a doubling.

    Computed on the SATURATING steady state since 2026-08-19, which changes
    the ranking rather than just the values:

        parameter   linear, N=20    saturating, N=300
        f                  +1.00                +1.00   unchanged, still first
        alpha, N, beta     +1.00                +0.53   halved by crowding
        P_s_max            +0.00                +0.47   NEWLY CO-LIMITING
        k_sec              +0.20                +0.11
        delta_m            -0.91                -0.49
        mu                 -1.05                -0.56

    P_s_max going from irrelevant to co-limiting is the whole design message:
    the limiting resource moved from the gene to the membrane, so the useful
    handles are now the folding fraction and the display scaffold.

    WARNING ON mu. It is the largest negative here and reading that as process
    guidance is a serious error -- see `volumetric_capture`. Site density is
    weakly hyperbolic in mu; biomass is exponential in it.
    """
    base = steady_state(p)["A"]
    q = dict(p)
    q[symbol] = p[symbol] * (1.0 + eps)
    return ((steady_state(q)["A"] - base) / base) / eps
