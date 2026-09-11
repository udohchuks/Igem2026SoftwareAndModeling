"""Joint checks: unit handling and the numbers the two joints produce."""

import io
import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import expression, interfaces, leach, params, recovery_chain  # noqa: E402

P_EXPR = params.values(params.load("expression"))


def test_joint1_accepts_both_names_for_the_same_unit():
    assert interfaces.au_feed_from_leach(12.0, "umol/L") == 12.0
    assert interfaces.au_feed_from_leach(12.0, "uM") == 12.0


def test_joint1_rejects_a_wrong_unit():
    with pytest.raises(interfaces.UnitError):
        interfaces.au_feed_from_leach(12.0, "mol/L")


def test_joint1_feed_warning_follows_the_revised_window():
    """The window moved on 2026-08-10 when Part II's q_max was adopted.

    Part III section 2.1 recommended 10-20 uM against a 22 uM capacity
    ceiling. At the adopted q_max the ceiling was 0.0539 uM, so the window was
    revised to 0.4-0.8 uM and the warnings now read from the YAML rather than
    from hard-coded thresholds. See ISSUES.md items 2, 26 and 33.

    2026-08-19: the ceiling moved to 0.4566 uM with Part II's copy number, and
    THE BOTTOM OF THE WINDOW IS NOW REACHABLE. A 0.4 uM feed is the first feed
    inside the recommended window that is not capacity-limited. The window
    itself does not move: it stays conditional on the engineering target.
    ISSUES.md items 61 and 62.
    """
    p3 = params.load("recovery_chain")["V1_capture"]
    lo, hi = p3["Au_feed"]["range"]
    ceiling = p3["q_max"]["value"] * p3["X_max"]["value"]
    assert (lo, hi) == (0.4, 0.8)
    assert p3["Au_feed"]["conditional_on"] == "q_max.engineering_target"

    assert ceiling == pytest.approx(0.4566, rel=1e-2)
    # The ceiling now lands INSIDE the window rather than below all of it.
    assert lo < ceiling < hi
    assert interfaces.feed_warning(lo) is None
    for feed in (0.5, 1.0, 1.5, 2.0, 10.0):
        assert "capacity ceiling" in interfaces.feed_warning(feed)
    # Above 30 uM the A_tox warning fires first; it is checked before the
    # capacity one because it is the older documented cliff.
    assert "above 30 uM" in interfaces.feed_warning(50.0)

    # The revised window becomes reachable only at the engineering target,
    # and it had to be halved on 2026-08-11 when the target itself fell.
    target = p3["q_max"]["engineering_target"]["value"]
    assert target * p3["X_max"]["value"] == pytest.approx(0.9805, rel=1e-2)
    # The whole window must sit UNDER the ceiling it is conditional on.
    # The superseded 1-2 uM window did not: its top exceeded 1.48 uM.
    assert target * p3["X_max"]["value"] > hi
    assert p3["Au_feed"]["superseded_range"] == [1, 2]


def test_joint2_conversion_is_dimensionally_correct():
    """1 mol of sites per gram must give 1e6 uM per (g/L)."""
    sites = interfaces.N_A / interfaces.CELLS_PER_G
    assert interfaces.qmax_from_expression(sites) == pytest.approx(1e6, rel=1e-9)


def test_joint2_is_linear_and_zero_at_zero():
    assert interfaces.qmax_from_expression(0.0) == 0.0
    a = interfaces.qmax_from_expression(1000.0)
    b = interfaces.qmax_from_expression(2000.0)
    assert b == pytest.approx(2 * a)


def test_joint2_historical_disagreement_stays_on_the_record():
    """The two q_max estimates are independent and they disagree by ~255x.

    Part II gives about 0.017 uM/(g/L). Part III uses 4.4 uM/(g/L) and
    flags it as possibly 5-13x optimistic. The gap is far larger than that:
    Part III is about 255x higher, and still about 19x higher than the low
    end of its own 0.33-4.4 sweep.

    Resolved on 2026-08-10 by adopting Part II across the chain, so
    params/recovery_chain.yaml now carries Part II's value with 4.4 kept
    beside it as `superseded`. This test measures Part II's cascade against
    the superseded constant, using the conversion in interfaces, so the size
    of the original gap stays checkable independently of the cells_per_g
    correction in item 33. See ISSUES.md items 2 and 33.
    """
    A = expression.steady_state(P_EXPR)["A"]
    q = interfaces.qmax_from_expression(A)
    report = interfaces.qmax_disagreement(
        q, interfaces.QMAX_PART_III_SUPERSEDED)
    # 2026-08-19: Part II's copy number moved 20 -> 300, so the gap narrowed
    # from about 255x to about 48x. It is still a gap, and still unresolved.
    assert report["ratio_II_over_III"] == pytest.approx(0.0208, rel=0.05)
    assert report["ratio_II_over_III"] < 0.05
    assert report["part_III_uM_per_gL"] / q == pytest.approx(48.2, rel=0.05)


def test_time_unit_round_trip():
    assert interfaces.per_minute(interfaces.per_hour(0.1)) == pytest.approx(0.1)


def test_elution_uses_pseudo_second_order_and_the_ceiling_is_unchanged():
    """The default rate law is PSO from 2026-08-16. ISSUES.md item 47.

    Both laws stop at (1-phi), so phi and every ceiling argument in REVIEW.md
    6.2 are unaffected. Only the approach differs: 50% of the ceiling at 1/k
    and 95% at 19/k, against 0.69/k and 3/k for the superseded PFO.
    """
    phi, k = 0.13, 2.0
    ceiling = 1 - phi
    assert recovery_chain.eta_elute(0.0, phi, k) == 0.0
    assert recovery_chain.eta_elute(1e9, phi, k) == pytest.approx(ceiling)
    assert recovery_chain.eta_elute(1.0 / k, phi, k) == pytest.approx(0.5 * ceiling)
    assert recovery_chain.eta_elute(19.0 / k, phi, k) == pytest.approx(0.95 * ceiling)


def test_pfo_is_retained_and_is_the_optimistic_law():
    """PFO stays callable so the comparison figure and old numbers reproduce.

    It reaches the ceiling far sooner than PSO. Pinning the gap stops anyone
    quoting a PFO contact time while the eluent and the rate law are open.
    """
    phi, k, ceiling = 0.13, 2.0, 0.87
    assert recovery_chain.eta_elute_pfo(0.0, phi, k) == 0.0
    assert recovery_chain.eta_elute_pfo(1e6, phi, k) == pytest.approx(ceiling)
    assert recovery_chain.eta_elute_pfo(3.0 / k, phi, k) == pytest.approx(
        0.95 * ceiling, rel=0.01)

    # The switch cost, at the 6 h operating point sensitivity.py uses.
    assert recovery_chain.eta_elute_pfo(6.0, phi, k) == pytest.approx(0.8700, abs=5e-4)
    assert recovery_chain.eta_elute(6.0, phi, k) == pytest.approx(0.8031, abs=5e-4)


def test_elution_has_one_rate_constant_and_the_model_is_PSO():
    """One eluent, one rate constant. The eluent is still unchosen.

    k_elute follows the eluent (ISSUES.md item 28) and is a placeholder until
    that choice is made. A second symbol k_elute_pso existed briefly and was
    dropped; this pins that the step does not regrow one, and that the rate
    law does not silently revert.

    CHANGED 2026-08-24. k_elute was pinned here as source: None. It now carries
    published anchors and a band, so the assertion is that the VALUE has not
    moved and the band still contains it. The step is still unmeasured on this
    sorbent: only S60 yields a rate, 1.1 h^-1, and it is the band's floor.
    """
    elution = params.load("recovery_chain")["elution"]
    assert elution["kinetic_model"]["value"] == "PSO"
    assert elution["kinetic_model"]["superseded"]["value"] == "PFO"
    assert "k_elute_pso" not in elution
    assert elution["k_elute"]["value"] == 2.0
    assert elution["k_elute"]["source"] == ["S60", "S24", "S61", "S62"]
    lo, hi = elution["k_elute"]["range"]
    assert lo < elution["k_elute"]["value"] < hi
    assert elution["phi"]["source"] == "S59"


def test_capacity_ceiling_after_adopting_part_II():
    """The transition sits at q_max*X_max, which moved when Part II was adopted.

    Part III section 2.1 put it at 22 uM with q_max = 4.4. Adopting Part II
    moved it to 0.0539 uM, a factor of 408; Part II's copy-number correction on
    2026-08-19 brought it back to 0.4566 uM, a factor of 48. The superseded
    values are still in the YAML and still reproduce the documented 22 uM,
    which is asserted here so each change is visible rather than silent.
    See ISSUES.md items 2, 33, 61 and 62.
    """
    p3 = params.load("recovery_chain")["V1_capture"]
    X_max = p3["X_max"]["value"]
    assert p3["q_max"]["value"] * X_max == pytest.approx(0.4566, rel=1e-2)
    assert p3["q_max"]["superseded_2026_08_19"]["value"] * X_max == (
        pytest.approx(0.0539, rel=1e-2))
    assert p3["q_max"]["superseded"]["value"] * X_max == pytest.approx(22.0)
    assert p3["q_max"]["status"] == "adopted_from_part_II"


def test_engineering_target_is_the_physical_anchor_ceiling():
    """q_max.engineering_target must equal f * P_s_max converted, not a wish."""
    p2 = params.load("expression")
    ceiling_sites = p2["f"]["value"] * p2["P_s_max"]["value"]
    target = params.load("recovery_chain")["V1_capture"]["q_max"]["engineering_target"]
    assert interfaces.qmax_from_expression(ceiling_sites) == pytest.approx(
        target["value"], rel=1e-3)
    # 2026-08-19: the headroom above the value in use fell from 18.2x to
    # 2.15x, because the surface is now 46.6% occupied rather than 5.5%.
    # Filling every remaining anchor is worth a factor of two and no more.
    assert target["value"] / params.load(
        "recovery_chain")["V1_capture"]["q_max"]["value"] == pytest.approx(2.15, rel=0.05)


def test_qmax_is_part_II_pushed_through_joint_2():
    """q_max is NOT independent. It must equal Part II's A* through Joint 2.

    This test exists because of a real failure. On 2026-08-19 Part II's copy
    number moved from 20 to 300 and every downstream file was updated except
    this one, so params/recovery_chain.yaml went on carrying 0.0108 while the
    report quoted 0.0913 in its body and 0.0108 in its appendix. Nothing
    caught it, because nothing recomputed the joint.

    Recomputing it here means the two files cannot drift again: if Part II
    moves and recovery_chain.yaml does not, this fails. ISSUES.md item 62.
    """
    p2 = params.load("expression")
    p = {k: v["value"] for k, v in p2.items()
         if isinstance(v, dict) and "value" in v}
    A = expression.steady_state(p)["A"]
    stored = params.load("recovery_chain")["V1_capture"]["q_max"]["value"]
    assert interfaces.qmax_from_expression(A) == pytest.approx(stored, rel=1e-3)

    # And the retired value must still be Part II's retired A*, so the size of
    # the correction stays checkable from the files alone.
    retired = params.load(
        "recovery_chain")["V1_capture"]["q_max"]["superseded_2026_08_19"]
    assert interfaces.qmax_from_expression(2749.1) == pytest.approx(
        retired["value"], rel=1e-2)
    assert stored / retired["value"] == pytest.approx(8.5, rel=0.05)


def test_part_II_and_part_III_now_agree_on_growth_rate():
    """Adopted 2026-08-10. Part II is the authority. See ISSUES.md item 24."""
    mu_II_per_min = params.load("expression")["mu"]["value"]
    mu_III_per_h = params.load("recovery_chain")["V1_capture"]["mu"]["value"]
    assert interfaces.per_hour(mu_II_per_min) == pytest.approx(mu_III_per_h, rel=0.01)


def test_K_Au_was_deliberately_not_adopted_from_part_II():
    """The one exception to the adopt-Part-II decision. See ISSUES.md item 1.

    Both documents now use the name K_Au for the GolB-gold dissociation
    constant, which makes the 10 uM vs 0.1 uM conflict impossible to miss.
    """
    p3 = params.load("recovery_chain")["V1_capture"]["K_Au"]
    assert p3["value"] == 0.1
    assert "decision_2026_08_10" in p3
    assert params.load("expression")["K_Au"]["value"] == 10.0   # the placeholder
    assert params.load("expression")["K_Au"]["status"] == "placeholder"


def test_electron_budget_reproduces_section_4_1():
    """Section 4.1: 0.2 g/L protein supplies 98.9% of electrons at 5.78 uM Au(I)."""
    E_tot = 0.2 / 70000.0 * 1e6      # g/L over 70 kDa, expressed in uM
    ceiling = recovery_chain.electron_budget_ceiling(
        E_tot=E_tot, Rech_0=0.0, Au_aq0=5.78, n_e_Au=1.0)
    assert ceiling == pytest.approx(0.989, abs=0.01)


# ---------------------------------------------------------------------------
# Joint 3, added 2026-08-11: Part II's cascade now also supplies Part I's Vmax
# ---------------------------------------------------------------------------

P_LEACH = params.load("leach")


def test_vmax_now_comes_from_the_expression_cascade():
    """Vmax = k_cat * [TetH], with [TetH] from Part II. ISSUES.md item 30.

    The team confirmed E. coli makes the thiosulfate. E. coli has no native
    tetrathionate metabolism, so the retired growth-yield route does not
    apply to it. This walks the whole chain and checks the stored number.
    """
    cap = P_LEACH["enzyme_capacity"]
    teth = cap["teth_per_cell"]["value"]
    B = cap["biomass"]["value"]
    cells_per_L = B * cap["cells_per_g"]["value"]
    k_cat = P_LEACH["tetrathionate"]["k_cat"]["value"]

    vmax = leach.vmax_from_expression(teth, cells_per_L, k_cat)
    assert vmax == pytest.approx(cap["Vmax"]["value"], rel=0.01)


def test_teth_per_cell_matches_part_II_cascade():
    """teth_per_cell must be f * P_s from Part II's own cascade, not a guess.

    It moved from 2,749 to 23,301 on 2026-08-19 with Part II's copy number.
    This test is what forces the two files to move together; without it the
    stored value would silently describe a backbone the model no longer uses.
    """
    _, _, _, Ps, _ = expression.simulate(P_EXPR, t_end=2000.0)
    expected = P_EXPR["f"] * Ps[-1]
    stored = P_LEACH["enzyme_capacity"]["teth_per_cell"]["value"]
    assert stored == pytest.approx(expected, rel=0.01)


def test_dimer_ambiguity_cancels_in_vmax():
    """Monomers x 110/min equals dimers x 220/min. ISSUES.md item 15.

    teth_per_cell counts monomers, so the factor of 2 in k_cat is matched by
    a factor of 2 in the molecule count and never reaches Vmax.
    """
    cells_per_L = 1.0e13
    monomers = leach.vmax_from_expression(2749.0, cells_per_L, 110.0)
    dimers = leach.vmax_from_expression(2749.0 / 2.0, cells_per_L, 220.0)
    assert monomers == pytest.approx(dimers, rel=1e-12)


def test_ecoli_route_is_far_weaker_per_gram_than_the_retired_route():
    """The headline consequence: about 40x less capacity per gram of cells.

    The retired A. ferrooxidans route claimed Vmax = 14.3 at 0.1 g/L. The
    E. coli route gives 9.49 at 4 g/L, so it is about 60x weaker per gram.
    Biomass is the lever that closes the gap; 6.0 g/L would reach 14.2.
    The ratio moved from 40x to 60x when cells_per_g was corrected in
    ISSUES.md item 33.
    """
    cap = P_LEACH["enzyme_capacity"]
    retired = cap["retired_A_ferrooxidans_route"]
    at_0_1 = leach.vmax_from_expression(
        cap["teth_per_cell"]["value"], 0.1 * cap["cells_per_g"]["value"],
        P_LEACH["tetrathionate"]["k_cat"]["value"])
    # 2026-08-19: the E. coli route gained 8.5x when Part II's copy number was
    # corrected, so the gap to the retired A. ferrooxidans route fell from
    # about 60x to about 7x. The direction of the finding is unchanged --
    # E. coli is still the weaker host per gram -- but it is no longer an
    # order-of-magnitude weaker, and that changes how much biomass Part I needs.
    ratio = retired["Vmax_at_0.1_g_per_L"]["value"] / at_0_1
    assert 6.0 < ratio < 9.0
    assert cap["biomass"]["value"] == pytest.approx(4.0)
    assert cap["Vmax"]["value"] == pytest.approx(80.36, rel=1e-2)


def test_part_I_growth_rate_now_matches_the_other_two_parts():
    """One organism, one growth rate. ISSUES.md item 29's headline reversed."""
    mu_leach = P_LEACH["enzyme_production"]["mu"]["value"]
    assert mu_leach == pytest.approx(P_EXPR["mu"])
    assert P_LEACH["enzyme_production"]["mu"]["superseded"]["value"] == 0.0


# ---------------------------------------------------------------------------
# Capture equilibrium, added 2026-08-11 by the audit.
#
# Every capture number in MASTER.md step 8 and in ISSUES.md items 1, 2, 22 and
# 26 was computed by solving the Langmuir mass balance. Until this date no
# function in the repository did that, and the one that looked as if it did
# applied the isotherm to total gold. These tests pin the published tables so
# the two cannot drift apart again.
# ---------------------------------------------------------------------------

K_AU_III = 0.1        # params/recovery_chain.yaml :: V1_capture.K_Au
X_MAX = 5.0           # params/recovery_chain.yaml :: V1_capture.X_max


def test_isotherm_applied_to_total_gold_is_unphysical():
    """Why capture_equilibrium exists. The isotherm alone can exceed the feed.

    S0 = 22 uM of sites, 10 uM of gold in: the isotherm reports 21.8 uM bound,
    which is 218% of what was added. This is not a bug in the isotherm; it is
    what happens when total gold is passed where free gold belongs.
    """
    bound = recovery_chain.capture_langmuir_isotherm(10.0, 22.0, K_AU_III)
    assert bound > 10.0
    assert recovery_chain.capture_equilibrium(10.0, 22.0, K_AU_III) < 10.0


def test_capture_never_exceeds_the_feed_or_the_sites():
    """C <= A_tot and C <= S0, at every combination worth checking."""
    for A in (0.001, 0.05, 1.0, 10.0, 50.0, 500.0):
        for S0 in (0.0815, 1.482, 22.0):
            C = recovery_chain.capture_equilibrium(A, S0, K_AU_III)
            assert 0.0 <= C <= A + 1e-12
            assert C <= S0 + 1e-12


def test_capture_reproduces_master_step_8_table():
    """MASTER.md step 8, all fifteen cells, to one decimal place."""
    published = {
        0.0163: {0.05: 38.4, 0.5: 13.2, 1.0: 7.4, 10.0: 0.8, 50.0: 0.2},
        0.2964: {0.05: 93.5, 0.5: 91.1, 1.0: 86.1, 10.0: 14.6, 50.0: 3.0},
        4.4:    {0.05: 99.5, 0.5: 99.5, 1.0: 99.5, 10.0: 99.2, 50.0: 43.8},
    }
    for q_max, row in published.items():
        for feed, percent in row.items():
            got = 100.0 * recovery_chain.eta_capture(feed, q_max * X_MAX, K_AU_III)
            assert got == pytest.approx(percent, abs=0.05), (q_max, feed)


def test_K_Au_swing_reproduces_issue_1_table():
    """ISSUES.md item 1: K_Au moved from insensitive to a 2.6x lever."""
    S0 = 0.0163 * X_MAX
    published = {0.02: 2.36, 0.05: 2.60, 0.10: 2.47, 0.50: 1.23, 10.0: 1.01}
    for feed, swing in published.items():
        lo = recovery_chain.eta_capture(feed, S0, 1e-4)
        hi = recovery_chain.eta_capture(feed, S0, 0.1)
        assert lo / hi == pytest.approx(swing, abs=0.01), feed


def test_capture_reaches_its_two_limits():
    """Capacity-limited C -> S0. Affinity-limited C -> S0*A_tot/K_Au."""
    S0 = 0.0815
    assert recovery_chain.capture_equilibrium(1e6, S0, K_AU_III) == pytest.approx(S0, rel=1e-4)
    A, K = 1e-6, 1e3
    assert (recovery_chain.capture_equilibrium(A, S0, K)
            == pytest.approx(S0 * A / K, rel=1e-4))


def test_capacity_ceiling_bounds_the_equilibrium_solve():
    """The rate-free ceiling in model.md section 2 must bound the full solve."""
    for q_max in (0.0163, 0.2964, 4.4):
        for feed in (0.05, 1.0, 10.0, 50.0):
            ceiling = recovery_chain.capacity_ceiling(q_max, X_MAX, feed)
            got = recovery_chain.eta_capture(feed, q_max * X_MAX, K_AU_III)
            assert got <= min(ceiling, 1.0) + 1e-9


# ===========================================================================
# THE SECOND AUDIT, 2026-08-12. ISSUES.md items 43 and 44.
#
# The first audit checked that Part I reproduces its own numbers. These pin
# what the joint was NOT carrying.
# ===========================================================================


def test_the_joint_carries_the_sulfur_species_now():
    """ISSUES.md item 44. Every polythionate crosses Joint 1 and must be visible.

    Until 2026-08-12 the joint carried gold and copper. The sulfur species were
    dropped silently, and tetrathionate is 1,212x the gold by concentration.

    TRITHIONATE WAS DROPPED THE SAME WAY on 2026-08-19, when Part I gained the
    alkaline decomposition route that makes it and this function was not
    updated to match. It is the larger of the two species. ISSUES.md item 60.
    """
    got = interfaces.sulfur_feed_from_leach(s4o6=47251.0, s2o3=0.0, s3o6=0.0)
    assert got["S4O6_uM"] == 47251.0
    assert got["S3O6_uM"] == 0.0
    assert got["polythionate_uM"] == 47251.0
    assert got["consumed_by_part_III"] is False

    with pytest.raises(interfaces.UnitError):
        interfaces.sulfur_feed_from_leach(1.0, 1.0, 1.0, unit="mM")


def test_tetrathionate_swamps_the_golb_cysteines():
    """ISSUES.md item 44, the number that makes it blocking.

    GolB binds Au(I) through one Cys-X-X-Cys motif, so two thiols per site.
    The sequential leach delivers 47,251 uM of tetrathionate against 0.913 uM
    of cysteine. At that excess the reaction need not be fast to finish.

    2026-08-19: the cysteine pool rose 8.5x with Part II's copy number, so the
    excess fell from 437,506 to 51,753. IT IS STILL BLOCKING. Item 44 does not
    turn on the size of the ratio once it is this far past one.
    """
    q_max, X_max = 0.0913, 5.0
    thiols = interfaces.THIOLS_PER_GOLB_SITE * q_max * X_max
    assert thiols == pytest.approx(0.913)

    s4o6 = 47250.61                               # model value at 72 h
    assert s4o6 / thiols == pytest.approx(51753, rel=1e-4)

    note = interfaces.thiol_blocking_warning(s4o6, q_max, X_max)
    assert note is not None
    assert "51,753 to 1" in note
    assert "item 44" in note
    assert interfaces.thiol_blocking_warning(0.0) is None
    assert interfaces.thiol_blocking_warning(0.0, s3o6_uM=0.0) is None


def test_capture_capacity_is_a_scale_mismatch_not_a_concentration():
    """ISSUES.md item 43, and it supersedes the advice given with item 39.

    The capture step is over capacity at any leach recovery above 0.45%, so
    no stopping rule makes it fit. Stated as the mass ratio that follows,
    because that is the number the process is actually sized by.

    2026-08-19: the ratio fell 8.5x with Part II's copy number, from 94 g of
    dry cells per gram of board to 11 g. THE SHAPE OF THE PROBLEM IS UNCHANGED.
    Eleven grams of engineered cells per gram of board is still a scale
    mismatch and still not something a stopping rule tunes. ISSUES.md item 43.
    """
    q_max, X_max = 0.0913, 5.0
    ceiling = q_max * X_max                       # umol Au per litre
    au_on_board = 101.54                          # umol per litre of liquor
    pcb_g_per_L = 100.0

    assert 100.0 * ceiling / au_on_board == pytest.approx(0.450, abs=0.005)

    au_per_g_board = au_on_board / pcb_g_per_L
    cells_per_board = au_per_g_board / q_max
    assert cells_per_board == pytest.approx(11.1, abs=0.2)

    # Both Part III stretch targets together now DO close it, at the delivered
    # 28.9 uM rather than the 39 uM item 43 was written against.
    assert 28.9 / (0.1961 * 130.0) == pytest.approx(1.13, abs=0.05)


def test_reagent_arm_mixing_only_dilutes_and_is_priced():
    """Arm B: the lysate volume is a multiplier on the binding constraint.

    ISSUES.md item 48. Mixing conserves reductase and adds volumes, so a
    lysate at or below the target can never reach the target. How far above
    it sits decides the volume ratio, and the ratio dilutes the gold that
    reduction is already short of. Item 35.
    """
    target = recovery_chain.protein_uM(0.2, 70000.0)
    assert target == pytest.approx(2.857, abs=1e-3)

    # A lysate barely above target needs a huge volume and costs 21x on gold.
    r_weak = float(recovery_chain.lysate_mixing_ratio(1.05 * target, target))
    assert r_weak == pytest.approx(20.0, rel=0.01)
    assert recovery_chain.gold_after_mixing(0.4566, r_weak) == pytest.approx(
        0.0217, abs=1e-4)

    # Ten times above target costs 11%.
    r_strong = float(recovery_chain.lysate_mixing_ratio(10.0 * target, target))
    assert r_strong == pytest.approx(1.0 / 9.0, rel=0.01)
    assert recovery_chain.gold_after_mixing(0.4566, r_strong) == pytest.approx(
        0.4109, abs=1e-4)

    # Equal to or below the target is impossible, not merely inefficient.
    for E in (target, 0.5 * target):
        with pytest.raises(ValueError):
            recovery_chain.lysate_mixing_ratio(E, target)


def test_reagent_arm_construct_parameters_are_all_null():
    """The reductase construct does not exist, so nothing may pretend it does.

    AGENTS.md rule 4. Only the design choices and the reported backbone carry
    values; every quantity the construct or the bench decides stays null until
    ISSUES.md item 48 is answered.

    ONE value left this list on 2026-08-20, and it is not any of alpha, N or
    beta. Those three are not separately identifiable -- they enter the model
    only as their product -- so each stays null and their product,
    alpha_N_beta, carries the construct's expression. It is not a measurement
    of this strain, so it must carry a band and a source. A value without a
    band here would be a guess wearing a number, which is the failure mode
    this test exists to catch. ISSUES.md item 67.
    """
    arm = params.load("recovery_chain")["reagent_arm"]
    assert arm["protein_target_g_per_L"]["value"] == 0.2
    assert arm["M_r_reductase"]["value"] == 70000
    for name in ("alpha", "N", "beta", "concentration_factor"):
        assert arm[name]["value"] is None, f"{name} acquired a value"

    # delta_c, lysis_yield and burden left the null list on 2026-08-21, each
    # with a literature band rather than a measurement of this system. The
    # band is what makes that honest, so every one of them must carry it.
    for name in ("delta_c", "lysis_yield", "burden"):
        spec = arm[name]
        assert spec["value"] is not None, f"{name} lost its value"
        assert spec["source"] is not None, f"{name} has a value and no source"
        lo, hi = spec["range"]
        assert lo <= spec["value"] <= hi, name

    # concentration_factor stays null because no paper decides it: it is a
    # process choice, not a property of anything. AGENTS.md rule 4.
    assert arm["concentration_factor"]["source"] is None

    # Retired into the lump, not merely unknown. The status must say which,
    # because "nobody has measured it" and "nothing can measure it" are
    # different problems and want different experiments.
    for name in ("alpha", "N", "beta"):
        assert arm[name]["status"] == "not_separately_identifiable"

    spec = arm["alpha_N_beta"]
    assert spec["value"] == 500.0
    assert spec["status"] == "sourced_by_proxy"
    lo, hi = spec["range"]
    assert lo <= spec["value"] <= hi
    assert spec["source"] is not None, "a value with no source is item 66"

    # The band must admit the possibility that the construct is no better than
    # a generic promoter on a low-copy plasmid. A floor, not a belief.
    assert lo <= 0.5 * 15 * 4.0


def test_s35_recipe_is_recorded_and_its_electron_ledger_does_not_close():
    """ISSUES.md item 51. Read from S35's methods on 2026-08-17.

    Two things are pinned. First, Rech is sodium dithionite at 4.6 uM, an
    added reagent, and the mediator is methyl viologen at 0.1 uM; the previous
    record called Rech a lysis carryover, which S35 refutes by purifying the
    protein before adding the dithionite. Second, S35 supplied a small
    fraction of the electrons its own gold demanded, which is why it reports
    colour and TEM and never a conversion. No eta_reduce in this repository is
    corroborated by that source.
    """
    red = params.load("recovery_chain")["reduction"]

    # S35's own recipe: 100 uL of 46 uM into 1000 uL, and 100 uL of 1 uM into
    # 1000 uL. Rech_0 STOPPED being the operating value on 2026-08-21, when
    # the team adopted 50 uM as a design choice; S35's figure lives in
    # `superseded` and this test reads it there, because what is pinned here
    # is what the SOURCE did, not what this project chose. ISSUES.md item 67.
    s35_rech = red["Rech_0"]["superseded"]["value"]
    assert s35_rech == pytest.approx(46.0 * 100.0 / 1000.0)
    assert red["mediator_0"]["value"] == pytest.approx(1.0 * 100.0 / 1000.0)
    assert red["mediator_0"]["source"] == "S35"
    assert "S35" in red["Rech_0"]["source"]

    # The operating value is above the source's, and declares itself a choice.
    assert red["Rech_0"]["value"] > s35_rech
    assert red["Rech_0"]["status"] == "design_choice"

    # The superseded lysate reading is kept too, under its own date-stamped
    # key so that neither retirement overwrites the other. AGENTS.md rule 5.
    assert "lysis" in red["Rech_0"]["superseded_2026_08_17"]["status"]
    assert red["Rech_0"]["superseded_2026_08_17"]["range"][0] > s35_rech

    # The ledger. Dithionite carries 2 electrons; S35's Au(III) needs 3 each.
    electrons_supplied = 2.0 * s35_rech
    assert electrons_supplied == pytest.approx(9.2)
    for au_mM, ratio in ((0.5, 0.0061), (10.0, 0.00031)):
        demand = 3.0 * au_mM * 1000.0
        assert electrons_supplied / demand == pytest.approx(ratio, rel=0.02)


def test_trithionate_is_required_at_the_joint_and_never_defaulted():
    """The argument has no default, on purpose. ISSUES.md item 60.

    Defaulting trithionate to zero would reproduce the bug it was added to
    fix: a sulfur species silently dropped at the joint while every number
    still looked plausible. A caller that has not decided what to do with it
    must fail, not guess.
    """
    with pytest.raises(TypeError):
        interfaces.sulfur_feed_from_leach(1000.0, 0.0)


def test_the_warning_reports_the_bound_separately_from_the_measured_ratio():
    """Two ratios, and the second is labelled a bound rather than a result.

    Tetrathionate's mechanism is established: the thiolate attacks its outer
    sulfur to give a cysteine-S-sulfonate, and across a Cys-X-X-Cys motif the
    intermediate closes an intramolecular disulfide.

    Trithionate's reactivity RELATIVE to tetrathionate is not published. No
    relative rate constant is invented here. The combined ratio assumes they
    are equally reactive, which is the worst case, and says so.

    Numbers below are the glycine scenario at 72 h: the tetrathionate-only
    ratio understates the polythionate load by 3.0x. The ratio itself fell 8.5x
    on 2026-08-19 with Part II's copy number; the 3.0x understatement did not
    move, because it is a ratio of two ratios.
    """
    q_max, X_max = 0.0913, 5.0
    s4o6, s3o6 = 8220.0, 16578.0

    alone = interfaces.thiol_blocking_warning(s4o6, q_max, X_max)
    both = interfaces.thiol_blocking_warning(s4o6, q_max, X_max, s3o6_uM=s3o6)

    assert "trithionate" not in alone
    assert "UPPER BOUND" not in alone

    assert "trithionate" in both
    assert "UPPER BOUND" in both
    assert "item 60" in both
    assert alone.split(" Plus")[0] in both      # the measured half is intact

    thiols = interfaces.THIOLS_PER_GOLB_SITE * q_max * X_max
    assert f"{(s4o6 + s3o6) / thiols:,.0f} to 1" in both


def test_the_joint_sees_what_the_leach_scenarios_actually_produce():
    """End to end: run Part I, hand the stream over, and check nothing is lost.

    This is the check that would have caught the four-day gap. It reads the
    sulfur states straight off a finished leach rather than from a literal, so
    a new species added to Part I and not to the joint fails here.
    """
    from src import leach

    runs = leach.compare_ligands(n=801)
    for name in ("ammonia", "glycine_mid"):
        s3 = runs[name][1]["traj"]
        feed = interfaces.sulfur_feed_from_leach(
            s4o6=float(s3["S4O6"][-1]), s2o3=float(s3["S2O3"][-1]),
            s3o6=float(s3["S3O6"][-1]))

        assert feed["S3O6_uM"] > 0.0                  # the route really runs
        assert feed["polythionate_uM"] > feed["S4O6_uM"]
        note = interfaces.thiol_blocking_warning(
            feed["S4O6_uM"], s3o6_uM=feed["S3O6_uM"])
        assert "UPPER BOUND" in note

    # And trithionate is the larger species in both, which is why dropping it
    # understated the load rather than rounding it.
    for name in ("ammonia", "glycine_mid"):
        s3 = runs[name][1]["traj"]
        assert s3["S3O6"][-1] > s3["S4O6"][-1]

# --------------------------------------------------------------------------
# The parameter files themselves. ISSUES.md item 66.
# --------------------------------------------------------------------------

PARAM_FILES = ("leach", "expression", "recovery_chain", "conversions")


def test_no_yaml_file_has_a_duplicate_key():
    """yaml.safe_load keeps the LAST duplicate key and reports nothing.

    params/leach.yaml carried two `derivation`, two `note` and two `source`
    keys on tetrathionate.k_cat_per_subunit, so the derivation the file
    actually served described a different parameter's value. Nothing failed,
    because nothing looked. ISSUES.md item 66.
    """
    import yaml

    dups = []

    class Loader(yaml.SafeLoader):
        pass

    def mapping(loader, node, deep=False):
        seen = set()
        for key_node, _ in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in seen:
                dups.append((loader.name, key,
                             key_node.start_mark.line + 1))
            seen.add(key)
        return yaml.SafeLoader.construct_mapping(loader, node, deep)

    Loader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, mapping)

    for f in PARAM_FILES:
        path = params.PARAMS_DIR / (f + ".yaml")
        loader = Loader(io.open(path, encoding="utf-8").read())
        loader.name = f
        try:
            loader.get_single_data()
        finally:
            loader.dispose()

    assert dups == [], dups


def test_every_derived_value_still_equals_its_own_derivation():
    """A derivation that no longer reproduces its value is a lie in the file.

    Vmax carried `2749 molecules/cell ... = 9.49 umol/L/min` while its value
    read 80.36, for a day after ISSUES.md item 61 moved the copy number. The
    parameter file is the authority for every number in the model, so a
    contradiction inside it is worse than one in a document.
    """
    p2 = {k: v["value"] for k, v in params.load("expression").items()
          if isinstance(v, dict) and "value" in v}
    ss = expression.steady_state(p2)
    cap = params.load("leach")["enzyme_capacity"]
    L = params.load("leach")

    # teth_per_cell = f * P_s, from Part II's cascade
    assert cap["teth_per_cell"]["value"] == pytest.approx(
        p2["f"] * ss["P_s"], rel=1e-4)

    # Vmax = k_cat * [TetH], and the scales_with_biomass table agrees with it
    def vmax_at(X):
        teth = (cap["teth_per_cell"]["value"] * X
                * cap["cells_per_g"]["value"] / 6.022e23) * 1e6
        return L["tetrathionate"]["k_cat"]["value"] * teth

    assert cap["Vmax"]["value"] == pytest.approx(
        vmax_at(cap["biomass"]["value"]), rel=5e-3)
    for X, quoted in cap["Vmax"]["scales_with_biomass"].items():
        assert vmax_at(float(X)) == pytest.approx(quoted, rel=5e-3), X

    # q_max = A through joint 2, and its target = f * P_s_max through the same
    q = params.load("recovery_chain")["V1_capture"]["q_max"]
    assert interfaces.qmax_from_expression(ss["A"]) == pytest.approx(
        q["value"], rel=2e-3)
    assert interfaces.qmax_from_expression(
        p2["f"] * p2["P_s_max"]) == pytest.approx(
            q["engineering_target"]["value"], rel=2e-3)

    # k_cat and k_cat_per_subunit each follow from their own specific activity
    assert L["tetrathionate"]["k_cat"]["value"] == pytest.approx(
        2.2 / 0.01, rel=1e-9)
    assert L["tetrathionate"]["k_cat_per_subunit"]["value"] == pytest.approx(
        2.5 / 0.02, rel=1e-9)

    # K_S2O3 is 1 / the geometric mean of the measured K_ads band
    assert L["gold_leaching"]["K_S2O3"]["value"] == pytest.approx(
        1e6 / math.sqrt(172 * 510), rel=1e-3)

    # the two files that both carry cells_per_g must agree exactly
    assert cap["cells_per_g"]["value"] == params.load(
        "conversions")["cells_per_g_dry_weight"]["value"]
