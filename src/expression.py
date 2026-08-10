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
    """Closed form of section 5, the non-saturating limit.

        A* = f*alpha*N*beta*k_sec
             / [(delta_m + mu)(k_sec + delta_c + mu)(delta_s + mu)]

    Valid while site density stays well below P_s_max. Section 8 states this
    holds here: thousands of sites against a ceiling of 1e5.
    """
    m = p["alpha"] * p["N"] / (p["delta_m"] + p["mu"])
    Pc = p["beta"] * m / (p["k_sec"] + p["delta_c"] + p["mu"])
    Ps = p["k_sec"] * Pc / (p["delta_s"] + p["mu"])
    return {"m": m, "P_c": Pc, "P_s": Ps, "A": p["f"] * Ps}


def langmuir_uptake(C, A, K_d):
    """Section 6 — gold ions bound per cell at leachate concentration C.

        q(C) = A*C / (K_d + C)

    C and K_d in uM. One site binds one Au(I) ion, so the plateau is A.
    """
    C = np.asarray(C, dtype=float)
    return A * C / (K_d + C)


def normalised_sensitivity(p, symbol, eps=1e-4):
    """Fractional change in A* per fractional change in one parameter.

    This reproduces panel (d) of Figure 1. alpha, N, beta and f should return
    approximately +1; k_sec approximately +0.2; mu the strongest negative.
    """
    base = steady_state(p)["A"]
    q = dict(p)
    q[symbol] = p[symbol] * (1.0 + eps)
    return ((steady_state(q)["A"] - base) / base) / eps
