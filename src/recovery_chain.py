"""Recovery closed forms and compatibility entry points.

The volume-aware process is in recovery_process; reduction trajectories and
conservation checks are in reduction; sampling and PRCC are in sensitivity.
Source-document implementations remain historical records.
"""
import numpy as np


def chain(**kwargs):
    """Run the amount/volume recovery process using descriptive inputs."""
    from .recovery_process import run
    return run(**kwargs)


def eta_reduce_ode(Au_aq0, p, t_end=None):
    """Return the reduction endpoint; use reduction.simulate for trajectories."""
    from .sensitivity import reduce_finke_watzky
    return reduce_finke_watzky(Au_aq0, p, t_end=t_end)


def sample(*args, **kwargs):
    """Draw a Latin hypercube using sensitivity.latin_hypercube's interface."""
    from .sensitivity import latin_hypercube
    return latin_hypercube(*args, **kwargs)


# --- closed forms stated directly in model.md -----------------------------

def eta_elute(t_k, phi, k_elute):
    """Elution. First-order release, the model in use.

        eta_elute(t_k) = (1 - phi) * (1 - exp(-k_elute*t_k))

    The residual fraction phi fixes the ceiling. The working k_elute is the
    conservative first-order lower bound derived from S60. Neither the law nor
    the constant is validated on the project GolB comb. ISSUES.md item 47.
    """
    return (1.0 - phi) * (1.0 - np.exp(-k_elute * np.asarray(t_k, dtype=float)))

def eta_elute_pfo(t_k, phi, k_elute):
    """Compatibility name for the first-order model now used by eta_elute."""
    return eta_elute(t_k, phi, k_elute)


def eta_elute_pso(t_k, phi, k_elute):
    """Retired pseudo-second-order candidate, retained for comparison."""
    kt = np.asarray(k_elute, dtype=float) * np.asarray(t_k, dtype=float)
    return (1.0 - phi) * kt / (1.0 + kt)


def capture_langmuir_isotherm(A_free, S0, K_Au):
    """model.md section 2 — the Langmuir isotherm, as written.

        C_eq = S0 * A_free / (A_free + K_Au)

    A_free is the gold still IN SOLUTION at equilibrium, not the gold you put
    in. Pass total gold and this returns more gold bound than exists: at
    S0 = 22 uM, K_Au = 0.7 and 10 uM of total gold it returns 20.6 uM, which is
    206% of the feed.

    Use capture_equilibrium below unless you already know the free
    concentration. This function is kept because it is the isotherm model.md
    prints, and because the capacity check in section 2 reads off its plateau.
    """
    return S0 * A_free / (A_free + K_Au)


def capture_equilibrium(A_tot, S0, K_Au):
    """Gold bound at equilibrium from the gold you actually added.

    The isotherm above plus the mass balance A_tot = A_free + C. Substituting
    A_free = A_tot - C into C = S0*A_free/(K_Au + A_free) and clearing the
    denominator gives one quadratic:

        C^2  -  (S0 + K_Au + A_tot) * C  +  S0 * A_tot  =  0

    The physical root is the smaller one, because C can exceed neither A_tot
    nor S0. Returns the same unit as A_tot and S0, normally uM.

    This is the function behind every capture number quoted in MASTER.md
    step 8 and in ISSUES.md items 1, 2, 22 and 26. It replaces an earlier
    version of this module that applied the isotherm to total gold and could
    report capture above 100%.

    Two limits worth knowing, both pinned by tests:

      capacity-limited   S0 << A_tot   ->  C -> S0
      affinity-limited   K_Au >> A_tot ->  C -> S0*A_tot/K_Au
    """
    A_tot, S0, K_Au = np.broadcast_arrays(
        np.asarray(A_tot, dtype=float), np.asarray(S0, dtype=float),
        np.asarray(K_Au, dtype=float))
    if any(np.any(~np.isfinite(x) | (x < 0.0)) for x in (A_tot, S0, K_Au)):
        raise ValueError("gold, sites and K_Au must be finite and non-negative")
    b = S0 + K_Au + A_tot
    # Rationalise the smaller root: subtracting almost equal numbers loses
    # the bound inventory at low feed. This discriminant is a sum of squares.
    disc = (A_tot - S0) ** 2 + K_Au * (K_Au + 2.0 * (A_tot + S0))
    denom = b + np.sqrt(disc)
    return np.divide(2.0 * S0 * A_tot, denom,
                     out=np.zeros_like(denom), where=denom > 0.0)


def eta_capture(A_tot, S0, K_Au):
    """Fraction of the gold fed that ends up bound. Between 0 and 1."""
    A_tot = np.asarray(A_tot, dtype=float)
    bound = capture_equilibrium(A_tot, S0, K_Au)
    return np.divide(bound, A_tot, out=np.zeros_like(bound), where=A_tot > 0.0)


def capacity_ceiling(q_max, X_max, Au_tot):
    """model.md section 2 — eta <= q_max * X_max / Au_tot.

    A capture efficiency above this value is impossible regardless of rates,
    so it is the first thing to check when a capture number looks good.
    """
    return q_max * X_max / Au_tot


def electron_budget_ceiling(E_tot, Rech_0, Au_aq0, n_e_Au):
    """model.md section 4.1 — the rate-free reduction ceiling.

        eta_reduce <= (2*E_tot + 2*Rech_0) / (n_e_Au * Au_aq0)

    E_tot is the reductase, Rech_0 the small-molecule reductant that recharges
    it, and Au_aq0 the dissolved gold present. Each of the first two carries a
    disulfide worth 2 electrons; each Au(I) demands 1 and each Au(III) 3.

    Needs no rate constant. Section 4.1 uses it twice: to show that 0.2 g/L
    protein already supplies 98.9% of the electrons at 5.78 uM Au(I), and to
    show that the source papers' regime covers only 0.048%.
    """
    return (2.0 * E_tot + 2.0 * Rech_0) / (n_e_Au * Au_aq0)


# --- Arm B, the reagent arm. ISSUES.md item 48 --------------------------------
#
# The source document draws two arms converging at reduction. Arm A, the gold,
# is modelled end to end. Arm B grows the reductase, lyses it, concentrates the
# lysate and mixes it into the eluate, and was drawn but never built.
#
# The construct's expression parameters are null in params/recovery_chain.yaml,
# so lysate_reductase_uM cannot run until they exist. The two functions after
# it need no new parameter: the mixing arithmetic is exact.


def protein_uM(protein_g_per_L, M_r):
    """Convert a protein concentration in g/L to uM.

    Replaces a literal that lived in model.ipynb and tests/test_sensitivity.py
    until 2026-08-16. E_tot in the reduction ODE is this quantity.
    """
    return protein_g_per_L / M_r * 1e6


def lysate_reductase_uM(P_c_per_cell, cells_per_L, lysis_yield,
                        concentration_factor, N_A):
    """Reductase concentration in the lysate, uM, before it meets the eluate.

    P_c_per_cell comes from Part II's cascade run with k_sec = 0, because the
    reductase stays cytoplasmic:

        expression.steady_state({... "k_sec": 0.0 ...})["P_c"]

    lysis_yield is the soluble fraction recovered after sonication and the
    100,000 g spin. concentration_factor is whatever step follows it.

    Every input except N_A is null in the parameter file, so this raises rather
    than returning a guess. That is the point: ISSUES.md item 48 exists to fill
    them.
    """
    molecules_per_L = (P_c_per_cell * cells_per_L
                      * lysis_yield * concentration_factor)
    return molecules_per_L / N_A * 1e6


def lysate_mixing_ratio(E_lysate, E_target):
    """Volumes of lysate per volume of eluate, to hit E_target after mixing.

    Mixing conserves the reductase and adds the volumes, so

        E_target = E_lysate * r / (1 + r),      r = V_lysate / V_eluate

    which inverts to r = f/(1 - f) with f = E_target/E_lysate.

    MIXING CAN ONLY DILUTE. A lysate at exactly E_target never reaches E_target
    at any finite ratio, and one below it never reaches it at all, so the
    lysate must exceed the target. How far above decides the volume, and the
    volume decides how much the gold is diluted. See gold_after_mixing.
    """
    E_lysate = np.asarray(E_lysate, dtype=float)
    if np.any(E_lysate <= E_target):
        raise ValueError(
            "lysate must be more concentrated than the target: mixing only "
            f"dilutes. Got E_lysate={E_lysate} uM against E_target={E_target} uM."
        )
    f = E_target / E_lysate
    return f / (1.0 - f)


def gold_after_mixing(Au_eluate, ratio):
    """Gold left after the lysate is added, uM. The cost of Arm B.

    Adding r volumes of lysate to 1 volume of eluate dilutes the gold by
    (1 + r). Reduction has a threshold near 3 uM (REVIEW.md 6.3) and capture
    delivers 0.457 uM, so this multiplier lands on the quantity that is
    already the binding constraint. ISSUES.md items 35, 48 and 61.
    """
    return np.asarray(Au_eluate, dtype=float) / (1.0 + np.asarray(ratio,
                                                                 dtype=float))


def eta_phys(eta_spin, eta_wash, eta_ash):
    """RETIRED 2026-08-21. Physical recovery is out of scope.

    model.md section 5 defined eta_phys = eta_spin * eta_wash * eta_ash. The
    team decided on 2026-08-16, and confirmed permanently on 2026-08-21, that
    whatever gold reaches metal is the gold we have. The kept definition is
    the record of what the equation was, not a step in the chain.

    It raises rather than computes, because a caller reaching for it is
    working from a stale idea of what this model covers, and the three terms
    it needs are null and out of scope in params/recovery_chain.yaml.
    """
    raise NotImplementedError(
        "physical recovery is out of scope; eta_total ends at reduction. "
        "See params/recovery_chain.yaml, the recovery block.")


def eta_total(eta_capture, eta_elute_, eta_reduce, eta_phys_=1.0):
    """model.md section 1 — the product of the four stage efficiencies."""
    return eta_capture * eta_elute_ * eta_reduce * eta_phys_
