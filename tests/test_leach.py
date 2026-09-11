"""Part I checks: conservation, geometry, and limit behaviour.

The process is three vessels. Stage 1 is algebraic, Stage 2 is a closed
two-state system, Stage 3 is the leach. Everything here runs on Stage 3 or on
the pure helpers, because those are the only places the chemistry lives.

The first block uses a small artificial parameter set so that one effect can be
isolated at a time. The second block reads params/leach.yaml and reproduces the
numbers Part I reports.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import leach  # noqa: E402


M_AU = 197e-3      # kg/mol
M_CU = 63.55e-3    # kg/mol


def make_params(**over):
    """Test-only parameter set. Deliberately artificial, so effects separate.

    Solid inventories are carried in umol, not mol. The section 4 table gives
    n_Au as "mol (or umol)" while R_Au is in umol/min, so the two must be
    reconciled by the user of the model; umol is the consistent choice.
    See ISSUES.md item 4.

    No exhaustion smoothing, so the switch is hard and a limit test is exact.
    """
    p = dict(
        # tetrathionate, and the enzyme carried over if any
        K_S4O6=500.0, k_par=1e-5, Y=1.0, k_cat=125.0, E_stage3=0.0,
        carry_enzyme=False,
        # reactor
        V_R=1.0, O2=250.0, t_stage3=200.0,
        # gold
        m_Au=1e-4, rho_Au=19300.0, t_film=1e-6,
        k_Au_O2=11.0, k_Au_Cu=11.0e3, K_O2=50.0, K_S2O3=5.0e4, K_CuII=100.0,
        # copper
        m_Cu=1e-2, rho_Cu=8960.0, d=4e-3,
        k_Cu_O2=1.0, k_Cu_Cu=1.0, k_ox_Cu=1e-6,
        # proton balance off unless a check asks for it
        pH_on=False, pH0=7.0, beta=1e5,
        M_Au=M_AU, M_Cu=M_CU,
    )
    p.update(over)
    return leach.refresh(p)


def leach_state(p, S4O6=1e4, S2O3=1e5, Vmax=0.0, Cu_I=0.0, Cu_II=0.0):
    """A Stage 3 starting state, in STATES_STAGE3 order."""
    return [Vmax, S4O6, S2O3, p["n_Au0"], 0.0, p["n_Cu0"], Cu_I, Cu_II, 0.0]


def run(p, y0=None, t_end=200.0, **kw):
    return leach.simulate_stage3(p, 1e4, 1e5, t_end=t_end, y0=y0, **kw)


def test_gold_area_formula():
    """a_Au = m/(rho*t). A film of area A and thickness t has volume m/rho."""
    A = leach.exposed_gold_area(m_Au=1e-4, rho_Au=19300.0, t_film=1e-6)
    assert A == pytest.approx(1e-4 / (19300.0 * 1e-6))


def test_copper_area_two_thirds_power():
    """a_Cu(t) = a_Cu(0)*(n/n0)^(2/3): area goes as r^2, volume as r^3."""
    assert leach.exposed_copper_area(100.0, 1.0, 1.0) == pytest.approx(100.0)
    assert leach.exposed_copper_area(100.0, 0.125, 1.0) == pytest.approx(25.0)
    assert leach.exposed_copper_area(100.0, 0.0, 1.0) == 0.0


def test_gold_mass_balance():
    """Solid gold lost must equal dissolved complex gained.

    Both sides are in umol: n_Au is umol and Au_complex*V_R is umol/L times L.
    """
    p = make_params()
    _, traj = run(p, leach_state(p))
    lost = p["n_Au0"] - traj["n_Au"]
    gained = traj["Au_complex"] * p["V_R"]
    assert np.allclose(lost, gained, rtol=1e-6, atol=1e-9)
    assert lost[-1] > 0.0        # something actually happened


def test_no_thiosulfate_means_no_gold_leaching():
    """Every gold route multiplies through the thiosulfate saturation factor.

    Tetrathionate must also be absent, otherwise carried-over enzyme would
    regenerate thiosulfate within the run and gold would start to leach.
    """
    p = make_params()
    y0 = leach_state(p, S4O6=0.0, S2O3=0.0)
    for model in ("A", "B"):
        _, traj = run(p, y0, t_end=50.0, model=model)
        assert traj["n_Au"][-1] == pytest.approx(p["n_Au0"], rel=1e-12)


def test_model_B_leaches_faster_than_model_A_when_cu_II_is_present():
    """Cu(II) is a parallel oxidant pathway, so Model B adds a positive term.

    Cu(II) must be present at the start. From a copper-free start the Cu(II)
    pool has no production route and the two models coincide. See ISSUES.md
    item 5.
    """
    p = make_params()
    y0 = leach_state(p, Cu_II=500.0)
    _, a = run(p, y0, model="A")
    _, b = run(p, y0, model="B")
    assert b["n_Au"][-1] < a["n_Au"][-1]

    # The Cu(II) rate constant is about 1e3 times the O2 one, but the run
    # does not show a 1e3 speed-up: the Cu(II) pool is consumed as it works,
    # and it has no production route from a copper-free solution.
    assert (p["n_Au0"] - b["n_Au"][-1]) > 5.0 * (p["n_Au0"] - a["n_Au"][-1])


def test_stage1_enzyme_steady_state_is_algebraic():
    """[E] = k_syn*X/(k_deg + mu). Stage 1 is never integrated.

    The culture settles in about 1/(k_deg+mu) minutes, far faster than
    anything downstream, so only the level it reaches is used. This replaced
    the standalone enzyme ODE when the one-pot model was retired.
    """
    got = leach.stage1_enzyme_steady_state(k_syn=8.74e-17, X=1e12,
                                           k_deg=1.1e-3, mu=0.0173)
    assert got == pytest.approx(4.75e-3, rel=1e-2)
    assert leach.culture_volume_ratio(0.043, got) == pytest.approx(9.05, rel=1e-2)


def test_enzyme_capacity_is_constant_in_the_leach_vessel():
    """There are no cells in Stage 3, so Vmax cannot build or decay.

    Whatever is carried over stays. Nothing synthesises it and no growth
    dilutes it.
    """
    p = make_params(carry_enzyme=True, E_stage3=0.04)
    y0 = leach_state(p, Vmax=p["k_cat"] * p["E_stage3"])
    _, traj = run(p, y0, t_end=500.0)
    assert np.allclose(traj["Vmax"], traj["Vmax"][0], rtol=1e-12)


def test_cu_II_goes_negative_under_source_stoichiometry():
    """The write-up as printed drives Cu(II) below zero from a copper-free start.

    Section 5 states Cu(II) is "produced only by oxygen re-oxidation of
    Cu(I)". Starting from zero dissolved copper, v4 is zero. The printed form
    then subtracts the whole gold rate from Cu(II), including its oxygen
    pathway, which consumes no copper. So the pool has a sink and no source
    and goes negative.

    This pins the documented behaviour, ISSUES.md item 5. It is a structural
    problem in the write-up, not a coding error, and the sequential document
    still prints it. ISSUES.md item 37.
    """
    p = make_params()
    _, traj = run(p, leach_state(p), stoichiometry="source")
    assert traj["Cu_II"].min() < 0.0
    assert traj["S4O6"].min() > 0.0


def test_balanced_stoichiometry_keeps_cu_II_non_negative():
    """Charging each pathway its own coefficients removes the negative pool.

    Only the Cu(II)-driven gold pathway consumes Cu(II); the oxygen pathway
    does not. Once R_Au is split, the Cu(II) sink vanishes at Cu(II) = 0
    instead of staying finite, so the pool cannot go below zero.

    This is the fix described in ISSUES.md item 18, and it resolves item 5.
    """
    p = make_params()
    _, traj = run(p, leach_state(p), stoichiometry="balanced")
    assert traj["Cu_II"].min() >= 0.0
    assert traj["Cu_I"].min() >= 0.0
    assert traj["S4O6"].min() > 0.0


def test_balanced_stoichiometry_charges_thiosulfate_per_copper_route():
    """Copper must draw 2 thiosulfate on the O2 route, 4 on the Cu(II) route.

    Run with copper leaching only, no gold, and check the thiosulfate lost
    against the copper dissolved.
    """
    p = make_params(k_Au_O2=0.0, k_Au_Cu=0.0, k_par=0.0,
                    k_ox_Cu=0.0, k_Cu_Cu=0.0)          # O2 route only
    y0 = leach_state(p)
    y0[3] = 0.0                                        # no solid gold
    _, tr = run(p, y0, t_end=100.0, model="A", stoichiometry="balanced")
    cu_dissolved = p["n_Cu0"] - tr["n_Cu"][-1]
    s2o3_used = tr["S2O3"][0] - tr["S2O3"][-1]
    assert s2o3_used == pytest.approx(2.0 * cu_dissolved / p["V_R"], rel=1e-3)


def test_stoichiometric_yield_scales_thiosulfate_production():
    """Y is wired into the production term, so changing it must bite.

    Section 3's table gives Y = 1 and the equation beside it omits Y, so the
    two agreed only by accident. ISSUES.md item 6. This needs enzyme in the
    vessel, so it runs with carry_enzyme. Leaching and the parasitic route are
    switched off, leaving production as the only thiosulfate term.
    """
    p = make_params(k_Au_O2=0.0, k_Au_Cu=0.0, k_Cu_O2=0.0, k_Cu_Cu=0.0,
                    k_par=0.0, k_ox_Cu=0.0, carry_enzyme=True, E_stage3=0.04)
    y0 = leach_state(p, S2O3=0.0, Vmax=p["k_cat"] * p["E_stage3"])
    made = {}
    for Y in (1.0, 2.0):
        p["Y"] = Y
        _, traj = run(p, y0, t_end=50.0)
        made[Y] = traj["S2O3"][-1]
    assert made[1.0] > 0.0
    assert made[2.0] == pytest.approx(2.0 * made[1.0], rel=1e-6)


def test_no_enzyme_means_tetrathionate_is_a_dead_end():
    """With no enzyme carried over and no parasitic route, S4O6 cannot move.

    This is the structural fact that separates the leach vessel from the
    retired one-pot model: nothing in Stage 3 consumes tetrathionate.
    """
    p = make_params(k_par=0.0)
    _, traj = run(p, leach_state(p), t_end=100.0)
    assert traj["Vmax"][-1] == pytest.approx(0.0, abs=1e-12)
    assert traj["S4O6"][-1] == pytest.approx(traj["S4O6"][0], rel=1e-9)


def test_copper_redox_pair_is_closed_without_leaching():
    """With no metal left, Cu(I)+Cu(II) changes only through v3 and v4.

    v3 converts 2 Cu(II) -> 2 Cu(I) and v4 converts 4 Cu(I) -> 4 Cu(II), so
    the total copper in solution must be constant.
    """
    p = make_params()
    y0 = leach_state(p, Cu_I=100.0, Cu_II=100.0)
    y0[3] = 0.0          # no solid gold
    y0[5] = 0.0          # no solid copper
    _, traj = run(p, y0, t_end=500.0)
    total = traj["Cu_I"] + traj["Cu_II"]
    assert np.allclose(total, total[0], rtol=1e-8)


# ===========================================================================
# THE WHOLE PROCESS, against params/leach.yaml. ISSUES.md items 36 to 46.
#
# Unlike the checks above, these read the real parameter file. Part I ships
# numeric results, so there is something to reproduce.
# ===========================================================================

from src import params as _params        # noqa: E402


def sequential_params():
    return leach.parameters()


def test_every_part_I_rate_constant_now_has_a_value():
    """Part I's author supplied the five constants this file held at null.

    Before 2026-08-12 k_Au_Cu, k_Cu_O2, k_Cu_Cu, k_par and k_ox_Cu were all
    null, and Part I could not be run end to end at all. This closes ISSUES.md
    item 8 and, with the Model A against Model B test below, item 20.
    """
    p = sequential_params()
    for name in ("k_Au_Cu", "k_Cu_O2", "k_Cu_Cu", "k_par", "k_ox_Cu"):
        assert name in p, f"{name} went back to null"
        assert p[name] > 0.0


def test_K_S2O3_sourced_value_beat_the_repository_placeholder():
    """3900 replaced 5e4 because a source beats a placeholder.

    AGENTS.md section 6 step 3 ranks the grounds for choosing between two
    numbers. This repository's 5e4 carried `status: calibrate` and the note
    "calibrate (~5e4)", which is a placeholder by its own admission. Part I's
    3900 is 1/K_ads with K_ads measured at 172 to 510 M^-1, so the sourced
    band is 1960 to 5800 umol/L and 5e4 sat 8.6x above the top of it.

    The superseded value stays in the YAML so this cannot be quietly reversed,
    and the two are held apart here because the choice is a 1.7x lever on the
    headline result.
    """
    block = _params.load("leach")["gold_leaching"]["K_S2O3"]
    assert block["value"] == 3376        # geometric mean, from 2026-08-19
    assert block["superseded"]["value"] == 3900             # was the midpoint
    assert block["superseded"]["superseded"]["value"] == 5.0e4  # placeholder
    assert block["status"] == "sourced"

    p = sequential_params()
    high = dict(p, K_S2O3=5.0e4)
    got = leach.simulate_sequential(p, n=801)["stage3"]["gold_recovered"][-1]
    old = leach.simulate_sequential(high, n=801)["stage3"]["gold_recovered"][-1]
    assert got > 1.4 * old        # 28.5 % against 19.1 %


def test_stage2_is_closed_and_conserves_sulfur():
    """No copper, no metal, no losses. S4O6 + S2O3 cannot change.

    This is the structural claim the whole sequential design rests on: the
    conversion vessel banks the full broth charge because nothing in it can
    destroy thiosulfate.
    """
    p = sequential_params()
    _, s2 = leach.simulate_stage2(p, n=1001)
    total = s2["S4O6"] + s2["S2O3"]
    assert np.allclose(total, total[0], rtol=1e-10)
    assert s2["S2O3"][-1] > s2["S2O3"][0]      # thiosulfate only ever rises


def test_stage2_matches_the_integrated_michaelis_menten_solution():
    """A closed Michaelis-Menten step has an exact solution. Use it.

    K*ln(S0/S) + (S0 - S) = Vmax*t. If the solver and the closed form disagree
    then one of them is wrong, and the closed form has no solver settings.
    """
    p = sequential_params()
    t, s2 = leach.simulate_stage2(p, n=1001)
    analytic = leach.stage2_time_to_reach(p, s2["S4O6"][-1])
    assert analytic == pytest.approx(t[-1], rel=1e-6)


def test_stage3_has_no_thiosulfate_source_without_carryover():
    """The leach vessel holds a budget, not a flow.

    This is the second structural claim. With no enzyme carried over,
    thiosulfate can only fall, and tetrathionate made by the parasitic
    reaction is a dead end that nothing converts back.
    """
    p = sequential_params()
    assert p["carry_enzyme"] is False
    r = leach.simulate_sequential(p, n=1001)
    s3 = r["stage3"]
    assert np.all(np.diff(s3["S2O3"]) <= 1e-9)     # monotone down
    assert s3["S4O6"][-1] > s3["S4O6"][0]          # dead-end accumulation
    assert s3["Vmax"][-1] == pytest.approx(0.0, abs=1e-12)


def test_sequential_reproduces_the_numbers_part_I_reports():
    """Part I's sequential write-up prints results. Reproduce them.

    Every figure below is quoted from that document. This is the test that
    fails if a parameter is edited without the write-up being edited too.

    RUNS ON THE RETIRED CONSTANTS, deliberately. k_Au_Cu, k_par and K_S2O3
    all changed on 2026-08-19 when the team chose glycine over ammonia. The
    write-up is a source document and is never edited, so reproducing it
    requires the ammoniacal values it was computed with. They live in
    params/leach.yaml :: reproduction_2026_08_12 for exactly this purpose.
    The live defaults are pinned separately, by
    test_ammonia_free_constants_reproduce_the_v5_thiosulfate_ledger.
    """
    p = dict(sequential_params(), **leach.source_2026_08_12_overrides())
    r = leach.simulate_sequential(p, n=20001)
    s2, s3 = r["stage2"], r["stage3"]

    assert s2["S4O6"][-1] == pytest.approx(941, abs=1)
    assert s2["S2O3"][-1] == pytest.approx(94359, abs=2)
    assert 100 * (1 - s2["S4O6"][-1] / p["S4O6_initial"]) == pytest.approx(95.9, abs=0.1)

    i24 = int(np.argmin(abs(s3["t"] - 1440)))
    assert 100 * s3["gold_recovered"][i24] == pytest.approx(35.1, abs=0.2)
    assert s3["Cu_II"].max() == pytest.approx(829, abs=2)
    assert 100 * s3["copper_recovered"][-1] == pytest.approx(0.176, abs=0.005)

    ledger = leach.thiosulfate_ledger(p, s3["t"], s3)
    assert ledger["gold"] == pytest.approx(78, abs=1)
    assert ledger["copper"] == pytest.approx(1660, abs=10)
    assert ledger["parasitic"] == pytest.approx(92618, abs=20)
    assert ledger["total"] == pytest.approx(ledger["actually_lost"], rel=1e-7)


def test_ammonia_free_constants_reproduce_the_v5_thiosulfate_ledger():
    """The live constants are checked against a document they were not fitted to.

    v5 ("Bioleaching_Models_v5.docx", 2026-08-19) runs the same three vessels
    with the ammonia-free constants and prints its own thiosulfate ledger and
    its own Cu(II) peak. This repository reproduces all four numbers, none of
    which was used to set a parameter:

        sink                v5 reports      here
        gold                     57.9       57.9
        copper                 ~1 640     1639.7
        parasitic              92 661    92661.1
        Cu(II) peak               818      818.0

    That is the check that the ammonia-free switch was made correctly, and not
    merely made.

    ONE NUMBER DOES NOT AGREE, and it is v5's. v5 reports 19.69 % gold at 24 h
    against 28.93 % at 72 h, so 68 % of the run's gold in the first third.
    Here it is 27.75 % against 28.49 %, which is 97 %. v5's own text says f_S
    falls below 0.5 by 23.7 h and is effectively zero by 26 to 28 h, and that
    description implies the 97 %, not the 68 %. Every other number in the
    section reproduces exactly. Recorded in ISSUES.md; left standing in the
    document.
    """
    p = sequential_params()
    r = leach.simulate_sequential(p, n=20001)
    s3 = r["stage3"]
    ledger = leach.thiosulfate_ledger(p, s3["t"], s3)

    assert ledger["gold"] == pytest.approx(57.9, abs=0.5)
    assert ledger["copper"] == pytest.approx(1640, abs=10)
    assert ledger["parasitic"] == pytest.approx(92661, abs=20)
    assert s3["Cu_II"].max() == pytest.approx(818, abs=2)
    assert ledger["total"] == pytest.approx(ledger["actually_lost"], rel=1e-7)

    assert 100 * s3["gold_recovered"][-1] == pytest.approx(28.5, abs=0.3)
    i24 = int(np.argmin(abs(s3["t"] - 1440)))
    assert 100 * s3["gold_recovered"][i24] == pytest.approx(27.75, abs=0.3)


def test_the_cu_II_oxidant_route_dies_with_ammonia():
    """ISSUES.md item 20 does not survive the ammonia-free constant.

    Item 20 held that Model B beats Model A once k_ox_Cu builds a Cu(II) pool,
    and that this was worth 9.6 percentage points. It was worth that because
    k_Au_Cu was 1500, measured in ammoniacal solution where ammonia holds
    Cu(II) as the cupric-tetraammine oxidant.

    At the ammonia-free 21.0 the pool still builds to the same 818 umol/L and
    buys almost nothing: 0.1 points, not 9.6. The saturation factor is not the
    difference; Cu(II) peaks at 818 against K_CuII = 5e4 in both regimes. The
    rate constant is.

    This is the case against ammonia stated as a number. Copper still destroys
    98 % of the thiosulfate, and now it does not pay for it in gold. Both
    regimes are pinned so the collapse cannot be undone silently.
    """
    p = sequential_params()

    def gain(q):
        b = leach.simulate_sequential(q, n=801, model="B")
        a = leach.simulate_sequential(q, n=801, model="A")
        return (b["stage3"]["gold_recovered"][-1]
                - a["stage3"]["gold_recovered"][-1])

    ammoniacal = dict(p, **leach.source_2026_08_12_overrides())
    assert gain(ammoniacal) == pytest.approx(0.096, abs=0.01)   # 9.6 points
    assert gain(p) == pytest.approx(0.001, abs=0.005)           # 0.1 points


def test_cu_I_reoxidation_is_what_makes_copper_fatal():
    """Item 20 assumed the wrong sign. Killing k_ox_Cu HELPS, and by a lot.

    Item 20 reads as though a small k_ox_Cu would be bad, because Model B
    would lose its oxidant. The opposite happens. Oxygen re-oxidising Cu(I) to
    Cu(II) is the only route into the Cu(II) pool, and that same pool is what
    destroys 98 % of the thiosulfate. Switch the route off and copper is
    harmless: Cu(II) never forms, the leachant survives, and gold recovery
    goes from 38 % to 88 % on the oxygen route alone.

    So Cu(I) re-oxidation is not a supporting reaction. It is the reaction
    that decides the process. Recorded here because the conclusion reverses
    the one written in item 20, and AGENTS.md rule 6 says reversed conclusions
    are restated, not erased.

    k_ox_Cu = 0 is not physical at 500 umol/L of dissolved oxygen. The usable
    version of this lever is the oxygen level itself; see the test below.
    """
    p = sequential_params()
    live = leach.simulate_sequential(p, n=801, model="B")["stage3"]
    dead = leach.simulate_sequential(dict(p, k_ox_Cu=0.0), n=801,
                                     model="B")["stage3"]
    assert dead["Cu_II"].max() < 1.0                  # the pool never forms
    assert dead["S2O3"][-1] > 5e4                     # leachant survives
    assert dead["gold_recovered"][-1] > 2.0 * live["gold_recovered"][-1]


def test_dissolved_oxygen_has_an_interior_optimum_well_below_the_baseline():
    """More aeration is not better. The baseline sits on the wrong side.

    Oxygen does two opposite things. It drives the gold and copper leaching
    routes, and it re-oxidises Cu(I) into the Cu(II) that destroys the
    leachant. The two pull against each other, so recovery peaks at an
    interior oxygen level and falls away on both sides.

    At the baseline 500 umol/L, gold recovery is 28.5 %. Near 80 umol/L it is
    about 52 %. Turning the sparger down is worth more than any other single
    change in the model, and it costs nothing.

    The ammonia-free constants of 2026-08-19 made this effect LARGER, not
    smaller. The optimum was 61 % against 38.4 %, a 1.6x gain; it is now 52 %
    against 28.5 %, a 1.8x gain. Removing the Cu(II) gold route removes the
    only reason oxygen was worth having in quantity, so the penalty for over-
    aerating is now almost unopposed. v5 reaches the same finding from the
    other direction in its Intervention 1.

    The optimum moves with k_par, which is borrowed from ammoniacal
    literature, so the 80 umol/L figure is not a set point. The existence of
    the optimum is the robust part, and that is what this test pins.
    """
    p = sequential_params()

    def recovery(o2):
        return leach.simulate_sequential(dict(p, O2=float(o2)),
                                         n=801)["stage3"]["gold_recovered"][-1]

    low, peak, high = recovery(50), recovery(80), recovery(500)
    assert peak > low                       # starved of oxidant below it
    assert peak > 1.5 * high                # poisoned by Cu(II) above it
    assert peak == pytest.approx(0.515, abs=0.03)


def test_finer_crushing_lowers_gold_recovery():
    """Coarser is better here, which is not the usual rule.

    Finer crushing exposes more copper, which makes more Cu(II), which
    destroys more thiosulfate. Gold sits in a film whose area does not depend
    on crush size at all, so finer crushing buys gold nothing and costs it the
    leachant. Part I's author left this sweep commented out and it appears in
    neither write-up, so it is pinned here or it is lost.
    """
    fine = leach.simulate_sequential(dict(sequential_params(), d=2.0e-3), n=801)
    coarse = leach.simulate_sequential(dict(sequential_params(), d=6.0e-3), n=801)
    assert coarse["stage3"]["gold_recovered"][-1] > \
        1.4 * fine["stage3"]["gold_recovered"][-1]


def test_alkalinity_is_tracked_instead_of_free_protons():
    """Free [H+] cannot be a state here. The pools differ by a millionfold.

    The run makes on the order of 1e5 umol/L of net base while the free proton
    pool at pH 7 is 0.1 umol/L. A free-[H+] state is driven negative and pH
    diverges. The retired one-pot model had that form; the sequential model
    tracks alkalinity, which is correct, and that is the one implemented.
    ISSUES.md item 37.
    """
    p = dict(sequential_params(), pH_on=True)
    r = leach.simulate_sequential(p, n=1001)
    s3 = r["stage3"]
    assert s3["alkalinity"][-1] > 0.0            # the leach makes net base
    assert s3["pH"][-1] == pytest.approx(7.94, abs=0.05)

    free_proton_pool = 10 ** (-p["pH0"]) * 1e6   # umol/L at pH 7
    assert s3["alkalinity"][-1] > 1e5 * free_proton_pool


def test_pH_is_off_by_default_so_the_flat_trace_is_not_a_result():
    """Part I's figure shows a flat pH because pH_on is false, not because
    the leach is buffered. Recorded so nobody quotes the panel."""
    p = sequential_params()
    assert p["pH_on"] is False
    r = leach.simulate_sequential(p, n=401)
    assert np.all(r["stage3"]["alkalinity"] == 0.0)


def test_stage3_derivatives_only_appends_to_the_chemistry():
    """The extensions are bolted on, not woven in.

    stage3_derivatives calls `derivatives` for the eight chemical states and
    appends the rest. Check that directly, so a future edit cannot quietly
    change the chemistry inside the wrapper.

    Since 2026-08-19 it appends five states, not one, and it also modifies
    dS4O6 and dS2O3 when the alkaline route is open. That route is off here,
    which is the default, so the eight must still match exactly. The nine-
    element state vector below is the pre-2026-08-19 form and still runs.
    """
    p = sequential_params()
    y = [0.0, 941.0, 94359.0, p["n_Au0"], 0.0, p["n_Cu0"], 10.0, 200.0, 0.0]
    from_stage3 = leach.stage3_derivatives(0.0, y, p)
    from_shared = leach.derivatives(0.0, y[:8], p)
    assert from_stage3[:8] == pytest.approx(from_shared)


def test_carrying_the_enzyme_into_the_leach_is_a_large_process_gain():
    """One pipe, 28.5 % to 33.7 %. Recorded, not adopted.

    Carrying purified enzyme into Stage 3 recycles the dead-end tetrathionate
    the parasitic reaction makes. It also puts the enzyme back into the pH
    conflict of ISSUES.md item 37, which is why it is not the default.

    IT IS NO LONGER THE LARGEST GAIN. Under the ammoniacal constants it was
    worth 15.9 points, 38.4 % to 54.3 %, and beat everything else. Under the
    ammonia-free constants it is worth 5.2 points, while turning the sparger
    down is worth 23. The ranking of the process levers changed on 2026-08-19
    and the name of this test changed with it.
    """
    p = sequential_params()
    off = leach.simulate_sequential(p, n=1001)
    on = leach.simulate_sequential(dict(p, carry_enzyme=True), n=1001)
    assert on["stage3"]["gold_recovered"][-1] > \
        off["stage3"]["gold_recovered"][-1] + 0.04
    assert on["stage3"]["S2O3"][-1] > 100.0       # budget not fully spent
    assert off["stage3"]["S2O3"][-1] < 1.0        # spent to nothing


# ===========================================================================
# THE 2026-08-19 EXTENSIONS
#
# Three switches, all false by default: the alkaline decomposition of
# tetrathionate, dissolved oxygen fed by the air pump, and pH held by a dosing
# pump. Plus glycine, which needs all of the first and third.
#
# Every test below either checks that the switch is inert when off, or runs it
# on deliberately. Nothing here changes a default.
# ===========================================================================


def test_every_new_switch_is_off_and_inert_by_default():
    """The extensions cannot move a number nobody asked them to move.

    This is the test that lets the rest of the file keep its pinned values.
    If it fails, some switch has been defaulted on and every reported figure
    in the repository is suspect.
    """
    p = sequential_params()
    for switch in ("alkaline_decay_on", "O2_dynamic", "pH_control", "gly_on"):
        assert p[switch] is False, switch

    s3 = leach.simulate_sequential(p, n=801)["stage3"]
    assert np.all(s3["S3O6"] == 0.0)
    assert np.all(s3["O2_diss"] == 0.0)
    assert np.all(s3["titrant"] == 0.0)
    assert 100 * s3["gold_recovered"][-1] == pytest.approx(28.49, abs=0.05)


def test_the_unmeasured_extension_parameters_raise_instead_of_guessing():
    """AGENTS.md rule 4, at the three places it matters most.

    pH_set is an operating choice nobody has made. G_T is a dose nobody has
    chosen. eps_gly is a constant nobody has measured. Each is null in
    params/leach.yaml, so each is absent from the parameter dict and using it
    raises KeyError. None of them may quietly become a default.
    """
    p = sequential_params()
    for missing, over in (("pH_set", dict(alkaline_decay_on=True)),
                          ("G_T", dict(gly_on=True, pH_set=10.0)),
                          ("eps_gly", dict(gly_on=True, pH_set=10.0,
                                           G_T=2.7e5))):
        with pytest.raises(KeyError) as exc:
            leach.simulate_sequential(dict(p, **over), n=201)
        assert missing in str(exc.value)


def test_the_alkaline_decomposition_stoichiometry_is_not_fitted():
    """Every coefficient comes off a balanced equation, so check it balances.

        4 S4O6(2-) + 6 OH-  ->  5 S2O3(2-) + 2 S3O6(2-) + 3 H2O

    Per one tetrathionate: 1.5 hydroxide in, 1.25 thiosulfate and 0.5
    trithionate out. Sulfur, oxygen and charge each close independently.

    The sulfur line is the one that matters: 4 = 2 x 1.25 + 3 x 0.50.
    Trithionate carries THREE sulfur atoms, not six. Getting that wrong was a
    real error during this work and the audit caught it.
    """
    p = sequential_params()
    nS2, nS3, nOH = p["nu_S2_S4"], p["nu_S3_S4"], p["nu_OH_S4"]

    assert 2.0 * nS2 + 3.0 * nS3 == pytest.approx(4.0)              # sulfur
    assert 6.0 + nOH == pytest.approx(3.0 * nS2 + 6.0 * nS3 + nOH / 2.0)  # O
    assert -2.0 - nOH == pytest.approx(-2.0 * nS2 - 2.0 * nS3)      # charge


def test_sulfur_atoms_are_conserved_once_the_alkaline_route_is_open():
    """The audit is exact, and the audit v5 uses would not have closed at all.

    v5 checks [S4O6] + [S2O3] = constant and calls it sulfur conservation.
    That is a MOLECULE count. It happens to be constant in v5's Stage 2
    because the reaction there is one-in one-out, but it is not conservation
    and it cannot catch an error. Here it drifts by 42 %.

    The atom count closes to machine precision, but only because S_removed
    accumulates the thiosulfate drawn into the gold and copper complexes. That
    draw is 2 per copper on the oxygen route and 4 on the Cu(II) route, so it
    depends on the path and cannot be reconstructed from the end state.
    """
    p = dict(sequential_params(), alkaline_decay_on=True, pH_set=10.0)
    s3 = leach.simulate_sequential(p, n=2001)["stage3"]

    atoms = leach.sulfur_audit(s3)
    assert abs(atoms - atoms[0]).max() / atoms[0] < 1e-9

    molecules = s3["S4O6"] + s3["S2O3"] + s3["S3O6"]
    assert abs(molecules - molecules[0]).max() / molecules[0] > 0.1


def test_the_alkaline_return_leg_is_the_largest_term_and_is_not_free():
    """Tetrathionate stops being a dead end, and trithionate becomes the sink.

    Without the alkaline route, tetrathionate made by the parasitic reaction
    accumulates forever and gold stops at 28.5 %. With it, at pH 10, most of
    that tetrathionate comes back as thiosulfate and gold reaches 49.9 %.
    That is the largest single term in Part I.

    IT IS NOT FREE, and this is the half that is easy to miss. The balanced
    equation returns 5 thiosulfate and 2 trithionate per 4 tetrathionate, so
    only five of every eight sulfur atoms come back. Nothing consumes
    trithionate at 25 C, because k_tri is null and deliberately so. It ends up
    holding 83 % of all the sulfur in the vessel.

    That matters downstream, not just in the ledger. ISSUES.md item 44 blocks
    on tetrathionate reaching the GolB cysteines, and this route trades
    tetrathionate for a different polythionate rather than removing one.
    """
    p = sequential_params()
    off = leach.simulate_sequential(p, n=1601)["stage3"]
    on = leach.simulate_sequential(
        dict(p, alkaline_decay_on=True, pH_control=True, pH_set=10.0),
        n=1601)["stage3"]

    assert 100 * off["gold_recovered"][-1] == pytest.approx(28.5, abs=0.3)
    assert 100 * on["gold_recovered"][-1] == pytest.approx(49.9, abs=0.5)
    assert on["S4O6"][-1] < 0.2 * off["S4O6"][-1]      # tetrathionate cleared

    total = leach.sulfur_audit(on)[-1]
    assert 3.0 * on["S3O6"][-1] / total > 0.80         # and it went here


def test_pH_has_an_interior_optimum_and_the_ceiling_is_not_about_gold():
    """Too basic is worse, and gold is not the reason.

    Gold dissolution is reported flat over pH 9 to 11, so pH acts only on
    whether the leachant survives. Two effects pull against each other:

        higher pH  ->  faster tetrathionate recycling      helps
        higher pH  ->  faster permanent loss to S3O6       hurts

    The result is an interior optimum near 10.3, and 10.5 is already past it.
    Two further ceilings the model does not carry push the same way: the Gly-
    fraction flattens above 10.3, and Cu(OH)2 precipitates above about 10.5.

    Titrant demand is negative throughout, meaning ACID. The parasitic
    reaction is a net acid source and the alkaline route consumes hydroxide,
    so holding the set point costs acid, and less of it the higher you go.
    """
    p = dict(sequential_params(), alkaline_decay_on=True, pH_control=True)

    def run(pH):
        s3 = leach.simulate_sequential(dict(p, pH_set=pH), n=801)["stage3"]
        return 100 * s3["gold_recovered"][-1], leach.titrant_demand(s3), s3

    g93, d93, _ = run(9.3)
    g100, _, _ = run(10.0)
    g103, d103, s3 = run(10.3)
    g105, _, _ = run(10.5)

    assert g103 > g100 > g93              # rising to the optimum
    assert g103 > g105                    # and falling past it
    assert g93 == pytest.approx(40.2, abs=0.5)
    assert g103 == pytest.approx(50.2, abs=0.5)

    assert d93 < 0 and d103 < 0           # acid, not base
    assert abs(d93) > abs(d103)           # and less of it higher up
    assert np.all(s3["alkalinity"] == 0.0)     # the pump holds it


def test_pump_fed_oxygen_reproduces_v5_intervention_1():
    """Oxygen as a state, checked against a number it was not fitted to.

    v5's Intervention 1 replaces the imposed 500 umol/L with a kLa balance and
    reports gold rising from 28.93 % to 35.63 % without ammonia. Here the same
    switch gives 28.49 % to 35.94 %. Both legs agree to under half a point,
    and none of v5's figures set a parameter.

    Two separate things improve at once, and it is worth separating them.
    C_star is 259 umol/L, so the old imposed 500 was ABOVE what air can
    dissolve at all; only pure-oxygen sparging reaches it. And the pump is
    then finite rather than infinite. Turning kLa down keeps helping, which is
    the same finding as the constant-O2 optimum near 80 umol/L.
    """
    p = sequential_params()
    imposed = leach.simulate_sequential(p, n=801)["stage3"]
    pumped = leach.simulate_sequential(dict(p, O2_dynamic=True),
                                       n=801)["stage3"]

    assert 100 * imposed["gold_recovered"][-1] == pytest.approx(28.5, abs=0.3)
    assert 100 * pumped["gold_recovered"][-1] == pytest.approx(35.9, abs=0.5)
    # Saturation is a ceiling the pump cannot pass. 1e-6 is solver slack,
    # not physics: LSODA overshoots the equilibrium by about 1e-8 umol/L.
    assert pumped["O2_diss"].max() <= p["C_star"] + 1e-6
    assert pumped["O2_diss"].min() < p["C_star"]        # the pump is finite

    slow = leach.simulate_sequential(dict(p, O2_dynamic=True, kLa=0.05),
                                     n=801)["stage3"]
    assert slow["gold_recovered"][-1] > pumped["gold_recovered"][-1]


def test_glycine_with_eps_one_is_exactly_no_glycine():
    """The limit that proves the speciation is wired in the right place.

    eps_gly is the reactivity of copper glycinate toward thiosulfate relative
    to free Cu(2+). At eps_gly = 1 the complex is as reactive as free copper,
    so glycine must do nothing at all, at any dose and any pH. Exactly
    nothing, not approximately.

    If this ever drifts, glycine is affecting a rate it has no business
    affecting.
    """
    p = dict(sequential_params(), alkaline_decay_on=True, pH_control=True,
             pH_set=10.0)
    without = leach.simulate_sequential(p, n=801)["stage3"]
    with_gly = leach.simulate_sequential(
        dict(p, gly_on=True, G_T=2.7e5, eps_gly=1.0), n=801)["stage3"]

    assert (with_gly["gold_recovered"][-1]
            == pytest.approx(without["gold_recovered"][-1], abs=1e-12))


def test_glycine_helps_across_the_whole_calibrated_band_of_eps():
    """The recommendation survives the uncertainty; the number does not.

    eps_gly is unmeasured. Calibrating it against the published observable,
    thiosulfate consumption falling from 5.2 to 2.2 g/L, gives about 0.012.
    Re-calibrating under five different operating conditions gives 0.0024 to
    0.0421, a 17x spread.

    Gold was never used in that calibration, so what the model says about gold
    is a prediction. Across the entire 17x band it stays above 85 %, against
    49.9 % without glycine. The BAND is quotable. The point value is not.

    At pH 10 with 0.27 M glycine the free Cu(2+) fraction is about 8e-15, so
    alpha_free is not what decides the answer. eps_gly is. That is why it is
    held null and why the wet-lab experiment in ISSUES.md item 54 is the one
    that matters.
    """
    p = dict(sequential_params(), alkaline_decay_on=True, pH_control=True,
             pH_set=10.0)
    baseline = leach.simulate_sequential(p, n=801)["stage3"]

    alpha, gly_minus = leach.free_cu_fraction(10.0, dict(p, G_T=2.7e5))
    assert alpha < 1e-12
    assert gly_minus == pytest.approx(0.168, abs=0.005)     # mol/L of Gly-

    for eps in (0.0421, 0.0116, 0.0024):
        s3 = leach.simulate_sequential(
            dict(p, gly_on=True, G_T=2.7e5, eps_gly=eps), n=801)["stage3"]
        assert 100 * s3["gold_recovered"][-1] > 85.0
        assert s3["S2O3"][-1] > 10 * baseline["S2O3"][-1]   # leachant survives


def test_glycine_does_not_touch_the_gold_rate():
    """The asymmetry is the entire mechanism, so pin it directly.

    Copper glycinate still oxidises gold; free Cu(2+) is what attacks
    thiosulfate. So the parasitic term sees a reduced Cu(II) and the gold term
    does not. If glycine were applied to both, it would slow gold as much as
    it protects the leachant and there would be no reason to add it.

    Checked at the level of the rate law, with a fixed state, so no integration
    can hide it.
    """
    p = dict(sequential_params(), pH_set=10.0, G_T=2.7e5, eps_gly=0.01)
    y = [0.0, 1000.0, 90000.0, p["n_Au0"], 0.0, p["n_Cu0"], 10.0, 500.0]

    _, off = leach.derivatives(0.0, y, dict(p, gly_on=False),
                               return_rates=True)
    _, on = leach.derivatives(0.0, y, dict(p, gly_on=True),
                              return_rates=True)

    assert on["R_Au"] == pytest.approx(off["R_Au"], rel=1e-12)   # untouched
    assert on["R_Au_Cu"] == pytest.approx(off["R_Au_Cu"], rel=1e-12)
    assert on["v_par"] < 0.02 * off["v_par"]                     # suppressed


# ===========================================================================
# THE TWO LIGAND SCENARIOS
#
# v5 runs Stage 3 with ammonia and then with no ligand at all. "No ligand" is
# not a choice anybody proposed, so the second column here is glycine. Both
# run at one operating point, so every difference is the ligand.
# ===========================================================================


def test_scenario_overrides_are_numbers_and_not_strings():
    """A YAML float trap that would have propagated silently.

    PyYAML 1.1 needs a decimal point in scientific notation: `2.7e5` parses as
    the STRING "2.7e5" while `2.7e+5` parses as a float. A string glycine dose
    would have reached `free_cu_fraction` and raised somewhere unrelated, or
    worse, compared as truthy and quietly changed a rate.
    """
    from src import params as _params

    doc = _params.load("leach")["scenarios"]
    for name in leach.scenario_names():
        for key, value in doc[name]["overrides"].items():
            assert isinstance(value, (int, float, bool)), (name, key, value)
    for value in leach.eps_gly_band():
        assert isinstance(value, float)


def test_both_scenarios_differ_only_in_the_ligand():
    """The comparison is worth printing only if one thing changed.

    Same pH set point, same aeration, same crush, same batch time, same
    charge. If a future edit moves the operating point of one column, this
    fails rather than producing a comparison that reads fine and means
    nothing.
    """
    a = leach.scenario("ammonia")
    g = leach.scenario("glycine", eps_gly=0.0116)

    # Two constants and a switch have different values in the two columns.
    shared_keys = set(a) & set(g)
    differing = {k for k in shared_keys
                 if isinstance(a[k], (int, float, bool)) and a[k] != g[k]}
    assert differing == {"k_Au_Cu", "k_par", "gly_on"}

    # Two more exist only in the glycine column. They are null in the
    # parameter file, so they are absent from the ammonia dict entirely, which
    # is how an ammonia run that touched them would raise instead of drifting.
    assert set(g) - set(a) == {"G_T", "eps_gly"}

    for shared in ("pH_set", "pH_control", "alkaline_decay_on", "O2_dynamic",
                   "kLa", "C_star", "d", "t_stage3", "k_ox_Cu"):
        assert a[shared] == g[shared], shared


def test_the_glycine_scenario_refuses_to_pick_its_own_eps():
    """eps_gly is unmeasured and spans 17x, so there is no value to default to.

    The scenario carries a calibrated BAND, not a number. Running it without
    choosing from that band must raise.
    """
    with pytest.raises(KeyError) as exc:
        leach.run_scenario("glycine", n=201)
    assert "eps_gly" in str(exc.value)

    assert len(leach.eps_gly_band()) == 3
    lo, mid, hi = leach.eps_gly_band()
    assert hi / lo > 15.0             # the honest spread, not a tight range


def test_the_ledger_closes_once_the_alkaline_return_is_counted():
    """Two ways this ledger can be wrong, both caught by one closure check.

    First, the alkaline route is a thiosulfate SOURCE. Counting only the three
    sinks leaves the charge unaccounted for, because tetrathionate hands back
    1.25 thiosulfate per molecule decomposed.

    Second, and this one was a real defect: recomputing the rates along a
    finished trajectory has to use the oxygen the run actually had. Falling
    back to the imposed constant while the air pump was on left a 2.5 % gap.
    Nothing in the sink numbers themselves looks wrong when that happens; only
    the closure check shows it.
    """
    for name, eps in (("ammonia", None), ("glycine", 0.0116)):
        p, r = leach.run_scenario(name, eps_gly=eps, n=2001)
        L = r["ledger"]
        assert p["O2_dynamic"] is True and p["alkaline_decay_on"] is True
        assert L["returned"] > 0.0
        assert L["total"] == pytest.approx(L["actually_lost"], rel=1e-6)
        assert r["sulfur_drift"] < 1e-9


def test_ammonia_beats_glycine_on_gold_and_glycine_is_still_the_choice():
    """The result that goes against the recommendation. Pinned, not buried.

    At pH 10 with the alkaline return leg open, thiosulfate no longer runs
    out, so ammonia's fast Cu(II) route runs to completion and takes ALL the
    gold in 72 hours. Glycine reaches 81 to 85 %. Ammonia wins on gold, and
    the earlier framing in ISSUES.md item 54, that glycine roughly doubles
    recovery, was measured against NO ligand and does not transfer to this
    comparison.

    Three things keep the decision where it is.

    1. AT 24 HOURS THEY ARE THE SAME, 28.9 % against 27.2 to 27.5 %. Ammonia's
       advantage lives entirely in the 24-to-72-hour window, and v5's own
       recommendation is to run one day, not three.
    2. GLYCINE HANDS DOWNSTREAM FAR LESS POLYTHIONATE. ISSUES.md item 44 is a
       BLOCKING item: tetrathionate attacks the cysteine pair GolB binds gold
       with. Ammonia leaves 58 336 umol/L of polythionate; glycine leaves
       7 817 to 44 187.
    3. GLYCINE COSTS LESS REAGENT, and the ammonia column is an upper bound
       anyway, because it assumes the air pump does not strip the ammonia it
       certainly would.

    The comparison is generous to ammonia on purpose. It keeps its own
    measured constants, it is assumed not to be stripped, and k_ox_Cu is
    ammoniacal in both columns because no ammonia-free value exists.
    """
    runs = leach.compare_ligands(n=2001)
    _, amm = runs["ammonia"]
    mid = runs["glycine_mid"][1]

    # 1. ammonia genuinely wins at 72 h, and the whole band loses
    assert amm["gold_72h"] > 99.0
    for key in ("glycine_low", "glycine_mid", "glycine_high"):
        assert 80.0 < runs[key][1]["gold_72h"] < 90.0

    # 2. and at 24 h the difference is under two points
    for key in ("glycine_low", "glycine_mid", "glycine_high"):
        assert abs(amm["gold_24h"] - runs[key][1]["gold_24h"]) < 2.0

    # 3. glycine hands downstream less of what ISSUES 44 blocks on
    amm_poly = amm["S4O6_end"] + amm["S3O6_end"]
    for key in ("glycine_low", "glycine_mid", "glycine_high"):
        g = runs[key][1]
        assert g["S4O6_end"] + g["S3O6_end"] < amm_poly

    # 4. and costs less titrant. Both are acid demands, hence the abs.
    assert amm["titrant"] < 0 and mid["titrant"] < 0
    assert abs(mid["titrant"]) < abs(amm["titrant"])


def test_the_glycine_band_is_narrow_in_gold_though_wide_in_eps():
    """17x in the unmeasured constant, under 4 points in the answer.

    This is what makes the recommendation quotable while the constant is not.
    eps_gly spans 0.0024 to 0.0421 and gold at 72 h spans 85.0 % to 81.1 %.
    The thiosulfate left over does NOT collapse the same way, spanning 4x,
    which is the right place for the uncertainty to show: eps_gly is
    calibrated against thiosulfate consumption, so that is the quantity it
    controls directly.
    """
    runs = leach.compare_ligands(n=2001)
    golds = [runs[k][1]["gold_72h"]
             for k in ("glycine_low", "glycine_mid", "glycine_high")]
    left = [runs[k][1]["S2O3_end"]
            for k in ("glycine_low", "glycine_mid", "glycine_high")]

    assert max(golds) - min(golds) < 5.0        # gold barely moves
    assert max(left) / min(left) > 3.0          # thiosulfate does
    assert golds[0] > golds[1] > golds[2]       # monotone in eps_gly


def test_k_tri_is_wired_to_something_and_still_refuses_to_guess():
    """A null that raises is safe. A null that is IGNORED is not.

    Until 2026-08-19 `k_tri` was declared in params/leach.yaml and read by no
    code at all. Obtaining the 25 C value and setting it would have changed
    nothing, silently, which is the worst of the three possible behaviours.
    The model audit found it. It is now wired to the reaction it names:

        S3O6(2-) + H2O  ->  S2O3(2-) + SO4(2-) + 2 H+

    first order in trithionate and not hydroxide-dependent, so the unit is
    min^-1 and not the L.mol^-1.min^-1 the entry carried before.

    It is still null, because the reported measurements are at 70 to 85 C and
    there is no 25 C value, so switching the route on raises.
    """
    from src import params as _params

    block = _params.load("leach")["tetrathionate"]["k_tri"]
    assert block["value"] is None
    assert block["unit"] == "min^-1"

    p = dict(sequential_params(), alkaline_decay_on=True,
             pH_control=True, pH_set=10.3)
    assert "k_tri" not in p

    with pytest.raises(KeyError) as exc:
        leach.simulate_sequential(dict(p, trithionate_hydrolysis_on=True),
                                  n=201)
    assert "k_tri" in str(exc.value)

    # Wired means it must actually do something when given a value.
    off = leach.simulate_sequential(p, n=1601)["stage3"]
    on = leach.simulate_sequential(
        dict(p, trithionate_hydrolysis_on=True, k_tri=1e-4), n=1601)["stage3"]

    assert on["S3O6"][-1] < off["S3O6"][-1]          # the sink drains
    assert on["S2O3"][-1] > off["S2O3"][-1]          # back to leachant
    assert on["gold_recovered"][-1] > off["gold_recovered"][-1]

    # Two protons per trithionate. The leach is net base-producing, so the
    # pump is delivering acid; a proton source reduces that demand.
    assert leach.titrant_demand(on) > leach.titrant_demand(off)
    assert leach.titrant_demand(on) < 0.0            # still acid, just less

    # And sulfur still closes: 3 = 2 to thiosulfate + 1 to untracked sulfate.
    atoms = leach.sulfur_audit(on)
    assert abs(atoms - atoms[0]).max() / atoms[0] < 1e-9

    # k_tri = 0 must be exactly the switched-off case, or the term is
    # contributing something it should not.
    zero = leach.simulate_sequential(
        dict(p, trithionate_hydrolysis_on=True, k_tri=0.0), n=1601)["stage3"]
    assert zero["gold_recovered"][-1] == pytest.approx(
        off["gold_recovered"][-1], abs=1e-14)


def test_two_enzyme_routes_disagree_77x():
    """ISSUES.md item 68. The culture vessel has two answers, 77x apart.

    REVIEW.md 2.1 sizes the culture from the source document's k_syn x X.
    Everything else in the repository sizes the enzyme from enzyme_capacity,
    which replaced that pair on 2026-08-11 because no measurement separates
    k_syn from k_cat.

    The ratio is pinned, not either value. Neither has been measured for TetH:
    one is a cross-species specific activity, the other is GolB's display
    density standing in for a harvested cytoplasmic protein. Freezing either
    number would claim a measurement this repository does not have.

    The test fails if one route moves and the other does not, which is the
    only way the item can be closed by accident.
    """
    doc = _params.load("leach")
    cap = doc["enzyme_capacity"]

    # The live route. The same arithmetic the file records under Vmax.
    live_uM = (cap["teth_per_cell"]["value"]
               * cap["biomass"]["value"]
               * cap["cells_per_g"]["value"] / 6.022e23 * 1e6)

    # It must reproduce the Vmax the file publishes, or the route has drifted.
    assert live_uM * doc["tetrathionate"]["k_cat"]["value"] == pytest.approx(
        cap["Vmax"]["value"], rel=1e-3)

    # The source document's route. k_syn and X are null in the file, so the
    # source's own values are written here -- this is the one place the
    # retired pair is still evaluated, and mu is the source's 40 min doubling
    # rather than the 35 min one params/leach.yaml holds.
    source_uM = leach.stage1_enzyme_steady_state(
        8.74e-17, 1.0e12, doc["enzyme_production"]["k_deg"]["value"], 0.0173)
    assert source_uM == pytest.approx(4.75e-3, rel=1e-2)

    # 77x apart, and on opposite sides of the conversion vessel's charge: the
    # source route must concentrate the harvest, the live route must dilute it.
    E_stage2 = doc["sequential"]["E_stage2"]["value"]
    assert live_uM / source_uM == pytest.approx(77.0, rel=0.05)
    assert source_uM < E_stage2 < live_uM
    assert E_stage2 / source_uM == pytest.approx(9.1, rel=0.02)
    assert E_stage2 / live_uM == pytest.approx(0.12, rel=0.05)

    # And the null pair still cannot be reached through the loader.
    assert "k_syn" not in _params.values(doc["enzyme_production"])
    assert "X" not in _params.values(doc["enzyme_production"])
