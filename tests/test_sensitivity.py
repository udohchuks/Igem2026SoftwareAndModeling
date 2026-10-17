"""Item 27 checks: the recomputed PRCC, and the reduction threshold.

src/sensitivity.py is an independent implementation of Part III's chain, built
because ensemble.py is not in this repository. These tests validate it against
Part III's own published ensemble before any of its rankings are quoted.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import params, recovery_chain, sensitivity as sn  # noqa: E402

R = params.load("recovery_chain")


def _v(block, key):
    return R[block][key]["value"]


def reduction_params(**over):
    p = dict(k_nuc=_v("reduction", "k_nuc"), k_grow=_v("reduction", "k_grow"),
             k_ox=_v("reduction", "k_ox"),
             k_rech=_v("reduction", "k_rech"), K_inh=_v("reduction", "K_inh"),
             nu=_v("reduction", "nu"),
             # Both of these read the YAML. Rech_0 was hard-coded at 100.0
             # here until 2026-08-20, while params/recovery_chain.yaml carried
             # 4.6 uM from S35's own recipe -- corrected in the YAML on
             # 2026-08-17 by ISSUES.md item 51 and never corrected here. Every
             # eta_reduce this file published came from the wrong pool.
             # ISSUES.md item 65.
             E_tot=recovery_chain.protein_uM(
                 _v("reagent_arm", "protein_target_g_per_L"),
                 _v("reagent_arm", "M_r_reductase")),
             Rech_0=_v("reduction", "Rech_0"),
             t_reduce_h=24.0)
    p.update(over)
    return p


def test_reduction_has_no_concentration_cliff_below_the_electron_ceiling():
    """SUPERSEDES the cliff test of ISSUES.md item 35. Rewritten 2026-08-24.

    Until 2026-08-24 this test asserted the opposite: that reduction failed
    below about 1 uM and only cleared 3 uM. That behaviour was a consequence of
    k_nuc = 5.0e-5 /h, a CHEMICAL nucleation rate borrowed from ascorbate and
    plant-extract fits. In this vessel the reductase performs the nucleation,
    so k_nuc is now scaled from the first measured enzyme constants for gold,
    (k_cat/K_M)*E_tot = 0.96 /h. SOURCES.md S74, ISSUES.md item 82.

    With that value there is no induction period to escape and no cliff. The
    only limit left is the electron budget, and it is a limit on the TOTAL, so
    it bites from above, not from below.
    """
    p = reduction_params()
    for charge in (0.05, 1.0, 3.0, 10.0):
        assert sn.reduce_finke_watzky(charge, p) > 0.99, charge

    # Above the ceiling, 2*E_tot + 2*Rech_0 = 105.7 uM, conversion falls along
    # it because the electrons run out. That is the ONLY failure mode now.
    assert sn.reduce_finke_watzky(120.0, p) == pytest.approx(0.879, abs=1e-2)
    assert sn.reduce_finke_watzky(200.0, p) == pytest.approx(0.527, abs=1e-2)


def test_reduction_rises_to_the_electron_ceiling_and_then_falls_along_it():
    """Conversion is NOT monotonic in starting gold, and it was never meant
    to be.

    This test asserted monotonicity until 2026-08-20 and passed, because the
    harness was feeding Rech_0 = 100 uM against the YAML's 4.6. At 100 uM the
    electron budget covers 206 uM of Au(I) and nothing in the tested range
    runs out. At the sourced 4.6 uM it covers 14.9 uM, so conversion peaks and
    then falls. ISSUES.md item 65.

    RECOMPUTED 2026-08-21. Rech_0 was raised from S35's 4.6 uM to 50 uM as a
    design choice, so the budget is 105.7 uM and the turn now happens near
    100 uM of gold rather than near 15. The SHAPE is unchanged, and so is the
    cross-check against the closed form; only where it bites has moved.

    The falling limb is not a defect. It is the closed-form electron ceiling
    of src/recovery_chain.py :: electron_budget_ceiling, which the ODE has no
    knowledge of, arrived at independently:

        eta_reduce <= (2*E_tot + 2*Rech_0) / (n_e_Au * Au_aq0)

    The two agreeing to within 3 % across the whole starved region is a
    genuine cross-check of the reduction model, and it only became visible
    once the recharging pool was read from the file that sources it.
    """
    p = reduction_params()
    budget = 2.0 * p["E_tot"] + 2.0 * p["Rech_0"]
    # RAISED 2026-08-21 from 14.914 uM: Rech_0 moved 4.6 -> 50 uM once the
    # team confirmed the reagent, so the DONOR now supplies 95 % of the
    # electrons and the protein only 5 %. The ceiling bites much later.
    assert budget == pytest.approx(105.714, rel=1e-3)

    # Rising limb: strictly increasing while electrons are plentiful. The
    # limb is LONGER since 2026-08-21 because the donor pool grew sevenfold.
    rising = [sn.reduce_finke_watzky(a, p) for a in (0.05, 0.5, 3.0, 10.0)]
    assert all(b >= a - 1e-9 for a, b in zip(rising, rising[1:]))
    assert rising[-1] == pytest.approx(1.0, abs=1e-3)

    # Falling limb: strictly decreasing, and pinned to the closed form. These
    # gold levels moved out with the ceiling: 20-50 uM used to be starved and
    # is now comfortably supplied.
    for au in (150.0, 200.0, 300.0):
        eta = sn.reduce_finke_watzky(au, p)
        ceiling = recovery_chain.electron_budget_ceiling(
            p["E_tot"], p["Rech_0"], au, 1.0)
        assert eta < 1.0
        assert eta <= ceiling + 1e-9
        assert eta == pytest.approx(ceiling, rel=0.03)

    falling = [sn.reduce_finke_watzky(a, p) for a in (150.0, 200.0, 300.0)]
    assert all(b <= a + 1e-9 for a, b in zip(falling, falling[1:]))

    # The turn happens near the budget, not somewhere arbitrary.
    assert sn.reduce_finke_watzky(0.9 * budget, p) > 0.95
    assert sn.reduce_finke_watzky(2.0 * budget, p) < 0.60

    # The ceiling is where it is because of the DONOR, not the enzyme. At the
    # 50 uM adopted on 2026-08-21 the dithionite carries over 94 % of the
    # budget, so the protein target has stopped setting this limit -- which is
    # the point of raising it, and why the reagent-arm shortfall matters less
    # than it did. ISSUES.md item 67.
    assert 2.0 * p["Rech_0"] / budget > 0.94


def test_concentrating_the_gold_is_no_longer_needed_for_the_rate():
    """SUPERSEDES item 35's proposed fix. Rewritten 2026-08-24.

    A 10x concentration step was the standing recommendation because the
    delivered 0.34 uM sat below the cliff. With an enzyme-scaled k_nuc the
    delivered gold converts on its own, so the concentration step is no longer
    a kinetic requirement. It remains useful for volume and for reagent cost,
    which is a different argument and belongs to whoever makes it.
    ISSUES.md item 82.
    """
    p = reduction_params()
    assert sn.reduce_finke_watzky(0.34, p) > 0.99
    assert sn.reduce_finke_watzky(3.4, p) > 0.99


def test_prcc_recovers_a_known_monotonic_relationship():
    """Sanity check on the PRCC implementation itself, not on the model.

    y = a - b + 0*c. PRCC must return about +1 for a, -1 for b, 0 for c.
    """
    rng = np.random.default_rng(0)
    n = 400
    s = {k: rng.random(n) for k in ("a", "b", "c")}
    y = s["a"] - s["b"]
    out = sn.prcc(s, y)
    assert out["a"] > 0.95
    assert out["b"] < -0.95
    assert abs(out["c"]) < 0.20


def test_first_order_elution_rate_is_propagated_through_the_chain():
    """The S60-derived PFO decision reaches the chain. ISSUES.md item 47."""
    old_k_au = params.load("recovery_chain")["V1_capture"]["K_Au"] \
        ["superseded_2026_09_18"]["value"]
    p = dict(reduction_params(), q_max=4.4, X_max=5.0, Au_feed=10.0,
             K_Au=old_k_au, phi=_v("elution", "phi"),
             k_elute=_v("elution", "k_elute"), t_elute_h=6.0)
    out = sn.chain_eta_total(p)
    assert "eta_phys" not in out, "the chain ends at reduction"
    expected_elution = recovery_chain.eta_elute(
        p["t_elute_h"], p["phi"], p["k_elute"])
    assert out["eta_elute"] == pytest.approx(expected_elution)
    assert out["eta_total"] == pytest.approx(
        out["eta_capture"] * out["eta_elute"] * out["eta_reduce"])


def test_the_reduction_constants_stay_inside_their_literature_bands():
    """ISSUES.md items 67, 79 and 82. The bands are the deliverable here.

    Neither constant is measured on this system. Each carries a band, and this
    test pins that the adopted values sit inside their own bands, that both
    declare a source, and that both are still labelled as proxies rather than
    measurements.

    RECENTRED 2026-08-24. k_grow moved from 0.2 to the log-centre of its band,
    0.082, closing the declared 2.4x fast-side bias. k_nuc moved from 5.0e-5 to
    0.96 and its band with it, from chemical nucleation to enzymatic:
    floor = the retired chemical value, ceiling = the engineered MerA variant
    of SOURCES.md S74.
    """
    v = params.load("recovery_chain")["reduction"]
    for name in ("k_nuc", "k_grow"):
        spec = v[name]
        lo, hi = spec["range"]
        assert lo <= spec["value"] <= hi, name
        assert spec["source"] is not None, name
        assert spec["status"] == "sourced_by_proxy", name

    # k_grow now sits AT its log-centre. The bias this test used to pin is
    # closed, so what it pins now is that it stays closed.
    lo, hi = v["k_grow"]["range"]
    assert v["k_grow"]["value"] / (lo * hi) ** 0.5 == pytest.approx(1.0,
                                                                   abs=0.05)

    # k_nuc's band is not a symmetric uncertainty and its log-centre means
    # nothing: the floor is the RETIRED chemical estimate, kept as a
    # pessimistic bound, and the ceiling is the ENGINEERED enzyme. What is
    # pinned is that the value in use is the wild type, more than tenfold
    # below what protein engineering has already achieved.
    lo, hi = v["k_nuc"]["range"]
    assert v["k_nuc"]["value"] < 0.1 * hi

    # And the band no longer spans the stage. THAT is the finding: with
    # nucleation set by the enzyme, the whole 656-fold k_grow band changes
    # conversion at the delivered gold by less than a point.
    p = dict(reduction_params())
    lo_kg, hi_kg = v["k_grow"]["range"]
    slow = sn.reduce_finke_watzky(0.3667, dict(p, k_grow=lo_kg), t_end=24.0)
    fast = sn.reduce_finke_watzky(0.3667, dict(p, k_grow=hi_kg), t_end=24.0)
    assert slow > 0.99 and fast > 0.99


def test_the_vessel_can_be_designed_so_the_unmeasurable_constants_stop_mattering():
    """ISSUES.md item 67. The answer to a constant nobody can measure.

    k_nuc and k_grow are the joint #1 driver and there is no route to either:
    the wet lab cannot measure them and no published fit exists for
    protein-mediated gold reduction. Waiting is not a plan.

    So the model is asked a different question. Not "what is k_grow" but "is
    there a vessel that clears the target whatever k_grow turns out to be". If
    the design clears the SLOWEST corner of both bands, the true value cannot
    change the outcome and the constants leave the critical path.

    This test pins the recommended design against both bands, and pins that it
    is genuinely needed -- that the delivered eluate in a 24 h batch does NOT
    clear it, which is what makes the recommendation more than decoration.
    """
    v = params.load("recovery_chain")["reduction"]
    design = params.load("recovery_chain")["reagent_arm"]["robust_design"]
    bands = {"k_nuc": tuple(v["k_nuc"]["range"]),
             "k_grow": tuple(v["k_grow"]["range"])}

    delivered = 0.3666
    p = dict(reduction_params())

    # The recommendation, read from params/ and not restated here. Rech_0 is
    # part of it: at 30x concentration the vessel runs out of ELECTRONS before
    # it runs out of time, and S35's own 4.6 uM caps it at 82 %.
    conc = design["concentration_factor"]["value"]
    p.update(t_reduce_h=design["t_reduce_h"]["value"],
             Rech_0=design["Rech_0"]["value"],
             seeding_on=True, seed_frac=design["seed_frac"]["value"])
    worst, corner = sn.reduce_worst_case(delivered * conc, p, bands)

    assert worst > 0.95, "the design must clear the target at the worst corner"
    assert worst == pytest.approx(
        design["worst_case_eta_reduce"]["value"], abs=0.01)
    assert corner == {"k_nuc": bands["k_nuc"][0], "k_grow": bands["k_grow"][0]}

    # Slower on both constants is worse, which is why corners suffice.
    mid, _ = sn.reduce_worst_case(delivered * conc, p,
                                  {"k_grow": (0.2, 0.2), "k_nuc": (5e-5, 5e-5)})
    assert mid >= worst

    # And the design is not decoration: without it, the worst corner fails.
    bare = dict(reduction_params(), t_reduce_h=24.0)
    bare_worst, _ = sn.reduce_worst_case(delivered, bare, bands)
    assert bare_worst < 0.01, "as delivered in 24 h, the slow corner fails"

    # Every term earns its place. Dropping the dithionite back to the recipe
    # value leaves the vessel ELECTRON-limited, not slow, so more time cannot
    # rescue it -- which is why Rech_0 is in the design at all.
    # S35's own 4.6 uM, now in `superseded`, is what "starved" means here.
    starved = dict(p, Rech_0=params.load("recovery_chain")
                   ["reduction"]["Rech_0"]["superseded"]["value"])
    starved_worst, _ = sn.reduce_worst_case(delivered * conc, starved, bands)
    assert starved_worst < 0.90, "without the dithionite the design fails"
    longer, _ = sn.reduce_worst_case(delivered * conc,
                                     dict(starved, t_reduce_h=336.0), bands)
    assert longer - starved_worst < 0.05, "starved of electrons, time is no cure"

    # NOR IS MORE ENZYME A CURE, and it is worth pinning because it is the
    # obvious thing to reach for. The rate carries E_red/E_tot, the FRACTION
    # of enzyme that is reduced, so adding enzyme against a fixed donor pool
    # dilutes the reducing power per molecule. Twentyfold more protein makes
    # the starved vessel measurably WORSE. ISSUES.md items 64 and 67.
    from src import recovery_chain as _rc
    richer = dict(starved, E_tot=_rc.protein_uM(4.0, 70000))
    richer_worst, _ = sn.reduce_worst_case(delivered * conc, richer, bands)
    assert richer_worst < starved_worst, "more enzyme cannot buy electrons"


def test_latin_hypercube_covers_each_range_once():
    rng = np.random.default_rng(3)
    s = sn.latin_hypercube({"x": (1.0, 2.0, "lin"), "y": (1e-3, 1e1, "log")},
                           200, rng)
    assert s["x"].min() >= 1.0 and s["x"].max() <= 2.0
    assert s["y"].min() >= 1e-3 and s["y"].max() <= 1e1
    # one draw per stratum: sorted gaps must be near-uniform for the linear one
    assert np.ptp(np.diff(np.sort(s["x"]))) < 0.02


def test_reduction_follows_standard_finke_watzky_with_the_donor_in_mass_action():
    """ISSUES.md item 50. No min() branch, and the protein pool is conserved.

    Finke-Watzky holds the reductant in excess and folds it into k_nuc and
    k_grow. Taking min() of two mechanisms is not a standard kinetic form. The
    donor is now carried by an (E_red/E_tot) factor, which equals 1 in the
    excess limit and so reproduces textbook F-W there, and closes the reaction
    down smoothly rather than switching branches when the donor runs out.

    The excess limit is not safe to assume across the operating range, which
    is why the factor is explicit: gold consumes 8.0% of the donor at the
    0.457 uM this chain delivers, but 52% at 3 uM. Before 2026-08-19 the
    delivered figure was 0.054 uM and 0.95%.
    """
    p = reduction_params()

    # k_donor is retired. The model must not depend on it in any way.
    assert "k_donor" not in p
    assert sn.reduce_finke_watzky(3.0, p) > 0.90

    # The excess condition, stated as arithmetic rather than assumed.
    E_tot, nu = p["E_tot"], p["nu"]
    assert nu * 0.4566 / E_tot == pytest.approx(0.080, abs=0.005)
    assert nu * 0.4566 / E_tot < 0.10         # as delivered: donor has slack
    assert nu * 3.0 / E_tot > 0.50            # after a 6.6x concentration: not


def test_the_reduction_landmarks_are_pinned_at_the_current_constants():
    """The same five landmarks, re-derived 2026-08-24 when k_nuc and k_grow
    moved. ISSUES.md item 82.

    They used to read 0.0039, 0.0013, 0.0287, 0.9925 and 1.000. Every one of
    them was a consequence of a chemical nucleation rate, and every one of them
    is now complete conversion. The landmarks are kept rather than deleted so
    that the size of the change stays visible in the test history.
    """
    p = reduction_params()
    for charge in (0.4566, 0.054, 1.0, 3.0, 5.78):
        assert sn.reduce_finke_watzky(charge, p) == pytest.approx(1.0,
                                                                 abs=5e-3)


# --------------------------------------------------------------------------

DELIVERED = 0.3667


def test_seeding_is_off_by_default_and_changes_nothing_when_off():
    """The switch-and-default-off rule, applied to the reduction stage."""
    p = reduction_params()
    assert "seeding_on" not in p
    assert sn.reduce_finke_watzky(DELIVERED, p) == pytest.approx(1.0, abs=5e-3)

    off = reduction_params(seeding_on=False, seed_frac=0.10)
    assert sn.reduce_finke_watzky(DELIVERED, off) == pytest.approx(
        sn.reduce_finke_watzky(DELIVERED, p), rel=1e-9)


def test_seeding_refuses_to_guess_a_seed_fraction():
    """seed_frac is null in the YAML and must raise, not substitute a number.

    No seeding experiment has been run. A default here would set the answer,
    because the whole finding is that a 1 % seed is worth more than a 4x
    concentration. AGENTS.md rule 4.
    """
    p = params.load("recovery_chain")["reduction"]
    assert p["seeding_on"]["value"] is False
    assert p["seed_frac"]["value"] is None

    with pytest.raises(KeyError):
        sn.reduce_finke_watzky(DELIVERED, reduction_params(seeding_on=True))

    with pytest.raises(ValueError):
        sn.reduce_finke_watzky(
            DELIVERED, reduction_params(seeding_on=True, seed_frac=-0.1))


def test_the_seed_is_not_counted_as_product():
    """Conversion must be metal this vessel MADE, not metal it was handed.

    At a 100 % seed the difference is a factor of two in the headline number,
    which is exactly the size of error that would make seeding look like a
    free win. The check is that a seed with no reaction time returns zero.
    """
    p = reduction_params(seeding_on=True, seed_frac=1.0)
    assert sn.reduce_finke_watzky(DELIVERED, p, t_end=0.0) == pytest.approx(
        0.0, abs=1e-9)

    # And the unseeded vessel at t = 0 also returns zero, so the two agree
    # where they must.
    assert sn.reduce_finke_watzky(
        DELIVERED, reduction_params(), t_end=0.0) == pytest.approx(0.0,
                                                                   abs=1e-9)


def test_seeding_is_inert_now_that_nucleation_is_enzymatic():
    """SUPERSEDES the seeding finding of ISSUES.md item 64. Rewritten
    2026-08-24.

    Seeding was the cheapest lever in this model because the vessel spent its
    first hours building the catalyst it needed: at k_nuc = 5.0e-5 /h a 1 %
    seed took the delivered gold from 0.3 % to 4.5 %, and a 4x concentration
    with a 1 % seed reached 92 % where 4x alone reached 16 %.

    A seed removes an induction period. With k_nuc set by the enzyme there is
    no induction period, so the seed has nothing to remove and every one of
    those numbers is now 100 %. ISSUES.md item 82.

    The branch is kept because it is correct and costs nothing, and because it
    becomes the lever again if a fitted k_nuc comes back small.
    """
    def eta(factor, seed):
        p = (reduction_params(seeding_on=True, seed_frac=seed) if seed
             else reduction_params())
        return sn.reduce_finke_watzky(DELIVERED * factor, p, t_end=24.0)

    for factor in (1.0, 4.0, 10.0):
        bare = eta(factor, 0.0)
        assert bare > 0.99, factor
        for seed in (0.01, 0.10):
            assert eta(factor, seed) == pytest.approx(bare, abs=5e-3)


def test_the_answer_no_longer_depends_on_the_unmeasured_constants():
    """SUPERSEDES the seeding-substitutes test. Rewritten 2026-08-24.

    The old test showed that a 1 % seed removed the model's dependence on
    k_nuc, which mattered because k_nuc is unmeasured. Setting k_nuc from the
    enzyme does the same thing more directly: at the delivered gold, a 100x
    rise in k_nuc and the full 656-fold width of the k_grow band all leave
    conversion at 100 %.

    This is the strongest statement this repository can currently make about
    the reduction stage: the two constants it cannot source no longer decide
    the answer. What decides it is the electron budget, which is a design
    input. ISSUES.md items 74 and 82.
    """
    p = reduction_params()
    base = sn.reduce_finke_watzky(DELIVERED, p, t_end=24.0)
    assert base > 0.99

    for over in (dict(k_nuc=100.0 * p["k_nuc"]),
                 dict(k_grow=3.2e-3),
                 dict(k_grow=2.1)):
        assert sn.reduce_finke_watzky(
            DELIVERED, reduction_params(**over), t_end=24.0) == \
            pytest.approx(base, abs=1e-2), over

    # k_nuc is the one that still matters, and only downwards. A tenfold drop
    # costs 6 points; the model is not indifferent to it, it is merely no
    # longer decided by it.
    assert sn.reduce_finke_watzky(
        DELIVERED, reduction_params(k_nuc=p["k_nuc"] / 10.0),
        t_end=24.0) == pytest.approx(0.936, abs=1e-2)


def test_electrons_are_not_what_limits_the_delivered_conversion():
    """The negative result, and it redirects the wet lab.

    Ten times the reductase and ten times the dithionite change the delivered
    conversion by less than a tenth of a point. The reagent-arm shortfall of
    items 48 and 52 therefore does not touch this problem, and effort spent
    growing more reductase buys nothing here.
    """
    base = reduction_params()
    plain = sn.reduce_finke_watzky(DELIVERED, base, t_end=24.0)

    for mult in (2.0, 5.0, 10.0):
        more_e = reduction_params(E_tot=base["E_tot"] * mult)
        more_r = reduction_params(Rech_0=base["Rech_0"] * mult)
        assert sn.reduce_finke_watzky(DELIVERED, more_e,
                                      t_end=24.0) == pytest.approx(plain,
                                                                   abs=1e-3)
        assert sn.reduce_finke_watzky(DELIVERED, more_r,
                                      t_end=24.0) == pytest.approx(plain,
                                                                   abs=1e-3)

    # The reason: gold consumes only 8 % of the donor pool at this gold.
    assert base["nu"] * DELIVERED / base["E_tot"] < 0.10


def test_the_inhibition_term_in_v_rech_never_fires():
    """K_inh = 500 uM is 45x above the highest concentration ever designed for.

    v_rech carries a competitive-inhibition factor, 1/(1 + Au_aq/K_inh), for
    dissolved gold taking spent reductase out of play. At every concentration
    this project uses the factor is within 3 % of 1, so the term is inert:
    removing it moves conversion by less than 0.01 of a point anywhere between
    the 0.367 uM elution delivers and 120 uM, which is past the electron
    ceiling. ISSUES.md item 74.
    """
    base = reduction_params()
    off = reduction_params(K_inh=1e12)          # effectively no inhibition

    for charge, t_end in ((DELIVERED, 24.0), (1.5, 24.0), (3.0, 24.0),
                          (11.0, 96.0), (120.0, 96.0)):
        assert sn.reduce_finke_watzky(charge, off, t_end=t_end) == \
            pytest.approx(sn.reduce_finke_watzky(charge, base, t_end=t_end),
                          abs=1e-4)


def test_the_donor_system_reduces_to_an_electron_cap():
    """Five states behave like two states plus one inequality.

    The donor equations exist because the reductant is not in excess. But
    recharging is fast -- v_rech reaches 14 uM/h against a demand of 5.5 uM
    over a whole 96 h batch -- so E_red/E_tot sits at 1 until the dithionite
    is spent, and then the reaction stops for lack of electrons rather than
    slowing down.

    That is exactly the structure docs/RECOVERY.md 4.3 and 4.4 describe: check
    the budget, then check the kinetics. This test pins that the shortcut is
    not just a narrative device. Plain Finke-Watzky on two states, capped at
    2*E_tot + 2*Rech_0 of gold, reproduces the full five-state integration to
    within half a point across three orders of magnitude of charge, with and
    without a seed. ISSUES.md item 74.
    """
    from scipy.integrate import solve_ivp

    def two_state(Au_aq0, p, t_end, seed=0.0):
        total = Au_aq0 + seed
        k1, k2 = p["k_nuc"], p["k_grow"]
        sol = solve_ivp(lambda _t, y: [(k1 + k2 * y[0]) * (total - y[0])],
                        (0.0, t_end), [seed], t_eval=[t_end],
                        rtol=1e-9, atol=1e-12, method="LSODA")
        made = float(sol.y[0][-1]) - seed
        cap = 2.0 * p["E_tot"] + 2.0 * p["Rech_0"]
        return min(made, cap) / Au_aq0

    cases = ((DELIVERED, 24.0, 0.0), (3.0, 24.0, 0.0), (11.0, 96.0, 0.5),
             (60.0, 96.0, 0.0), (120.0, 96.0, 0.0), (200.0, 96.0, 0.0))
    for charge, t_end, seed in cases:
        p = reduction_params()
        full_p = dict(p)
        if seed:
            full_p.update(seeding_on=True, seed_frac=seed)
        full = sn.reduce_finke_watzky(charge, full_p, t_end=t_end)
        assert two_state(charge, p, t_end, seed * charge) == \
            pytest.approx(full, abs=5e-3)


def test_the_time_to_a_given_conversion_matches_the_ode():
    """t_f is the closed form inverted, and it agrees with the integration.

    docs/RECOVERY.md 4.3 quotes t_ind = 1/(k_grow*Au_aq) as the induction time
    and t_f = ln((1 + f*R)/(1 - f))/(k_nuc + k_grow*Au_aq0) as the time to a
    conversion f, with R = k_grow*Au_aq0/k_nuc. This checks both the algebra
    and the claim that the prefactor may be replaced by t_ind, against a direct
    integration of dAu_s/dt = (k_nuc + k_grow*Au_s)*(Au_aq0 - Au_s) stopped at
    the Au_s = f*Au_aq0 event. ISSUES.md item 77.
    """
    from scipy.integrate import solve_ivp

    p = reduction_params()
    k1, k2 = p["k_nuc"], p["k_grow"]

    def t_f(Au_aq0, f):
        ratio = k2 * Au_aq0 / k1
        return np.log((1.0 + f * ratio) / (1.0 - f)) / (k1 + k2 * Au_aq0)

    def t_f_numeric(Au_aq0, f):
        event = lambda _t, y: y[0] - f * Au_aq0      # noqa: E731
        event.terminal = True
        sol = solve_ivp(lambda _t, y: [(k1 + k2 * y[0]) * (Au_aq0 - y[0])],
                        (0.0, 1e6), [0.0], events=event,
                        rtol=1e-11, atol=1e-15, method="LSODA")
        return float(sol.t_events[0][0])

    for Au_aq0 in (DELIVERED, 1.5, 3.0, 11.0):
        t_ind = 1.0 / (k2 * Au_aq0)
        for f in (0.5, 0.95):
            exact = t_f(Au_aq0, f)
            assert t_f_numeric(Au_aq0, f) == pytest.approx(exact, abs=0.1)
            # The t_ind shortcut is NOT used any more. It needs
            # k_grow*Au >> k_nuc, which held at k_nuc = 5.0e-5 and fails at
            # 0.96: R runs 0.03 to 0.94 across this range, so the prefactor
            # keeps both terms. ISSUES.md item 82.
            assert 0.01 < k2 * Au_aq0 / k1 < 1.0
            assert t_ind > 0.0

    # the three rows of the table in docs/RECOVERY.md 4.3
    for Au_aq0, t_95 in ((DELIVERED, 3.06), (1.5, 2.87), (3.0, 2.67)):
        assert t_f(Au_aq0, 0.95) == pytest.approx(t_95, abs=0.05)
