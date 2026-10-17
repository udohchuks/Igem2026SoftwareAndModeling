"""Arm B checks: growing the reductase, and when to lyse. ISSUES.md item 52.

src/reductase.py answers one operational question -- at what moment should the
culture be harvested -- and one strategic one: whether the culture can reach
the 0.2 g/L the whole reduction stage assumes. These tests pin both, and pin
the fact that the cascade constants for this construct are still null.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import params, reductase as rd  # noqa: E402

R = params.load("recovery_chain")
E = params.load("expression")
C = params.load("conversions")
V = params.values(params.load("recovery_audit")["verification"])


def arm(**over):
    """The part-proxy culture. burden is null in YAML, so it must be passed.

    `construct=a` makes this read the reductase's own N from the YAML, which
    stopped being null on 2026-08-20. Passing the block rather than the value
    means alpha, beta and delta_c arrive the same way when they are measured,
    instead of needing this harness edited. ISSUES.md item 65 is what happens
    when a test harness carries its own copy of a parameter.
    """
    a = R["reagent_arm"]
    p = dict(rd.golb_proxy_cascade(E, construct=a))
    p.update(mu=E["mu"]["value"],
             X_0=a["X_0"]["value"], X_cap=a["X_cap"]["value"],
             X_ind=a["OD_induce"]["value"] * a["g_dw_per_OD600"]["value"],
             burden=a["burden"]["value"],
             M_r=a["M_r_reductase"]["value"],
             cells_per_g=C["cells_per_g_dry_weight"]["value"],
             N_A=C["N_A"]["value"])
    p.update(over)
    return p


def test_the_construct_parameters_are_still_null_and_the_cascade_is_a_proxy():
    """AGENTS.md rule 3. Modelling the arm must not invent the construct.

    alpha, beta and delta_c belong to the reductase construct, which does not
    exist. golb_proxy_cascade reaches into params/expression.yaml for GolB's
    values instead, and any absolute yield below is an order of magnitude on
    that basis, not a prediction.

    alpha, N and beta all stay null, but for a different reason since
    2026-08-20: they are not separately identifiable, so a value in any one of
    them would be a choice of how to split a product. The construct's own
    expression is carried in alpha_N_beta instead. ISSUES.md item 67.
    """
    a = R["reagent_arm"]
    for name in ("alpha", "N", "beta", "concentration_factor"):
        assert a[name]["value"] is None, f"{name} acquired a value"
    for name in ("alpha", "N", "beta"):
        assert a[name]["status"] == "not_separately_identifiable"

    proxy = rd.golb_proxy_cascade(E)
    assert proxy["alpha"] == E["alpha"]["value"]
    assert proxy["beta"] == E["beta"]["value"]
    assert proxy["k_sec"] == 0.0, "the reductase is cytoplasmic, not displayed"
    assert proxy["N"] == E["N"]["value"], "no construct given, so N is GolB's"

    # With the construct, the lump supplies alpha, N and beta, and delta_c
    # was sourced on 2026-08-21, so nothing is borrowed from GolB any more.
    # The lump is still a proxy; it is this construct's proxy, not GolB's.
    assert rd.borrowed_keys(E, a) == ()


def test_lumping_the_expression_group_is_exact_and_not_an_approximation():
    """ISSUES.md item 67, and the reason the three parameters became one.

    alpha, N and beta enter the cascade only as their product, so replacing
    them by (product, 1, 1) must change nothing a measurement could see. This
    is the claim the restructure rests on, and it is checked rather than
    asserted in prose. Raue et al. 2009 is the identifiability reference.

    The mRNA series IS rescaled by the same factor and is deliberately not
    compared: nothing in this repository reads it, and reductase.py says so.
    """
    three = dict(arm())
    three.update(alpha=2.5, N=50.0, beta=4.0)
    assert rd.lumped_group(three) == pytest.approx(500.0)

    one = dict(arm())
    one.update(rd.cascade_from_lumped(rd.lumped_group(three), E))

    s3, s1 = rd.simulate(three), rd.simulate(one)
    for key in ("X", "P_c", "C_prot"):
        scale = max(float(np.max(np.abs(s3[key]))), 1e-30)
        assert float(np.max(np.abs(s3[key] - s1[key]))) / scale < 1e-6, key

    assert rd.harvest_time(three)["C_prot_g_per_L"] == pytest.approx(
        rd.harvest_time(one)["C_prot_g_per_L"], rel=1e-6)


def test_the_expression_group_is_the_constructs_own_and_it_reaches_the_model():
    """ISSUES.md item 67. pET-24(+) is not the pJUMP backbone GolB sits on.

    Two things are checked, and the second is the one that matters. First,
    that the YAML lump is used in preference to GolB's three constants.
    Second, that the culture the rest of this file simulates is actually
    running on it -- a value can be correct in params/ and never reach the
    model, which is exactly what item 62 was.
    """
    a = R["reagent_arm"]
    anb = a["alpha_N_beta"]["value"]
    assert anb is not None
    lo, hi = a["alpha_N_beta"]["range"]
    assert lo <= anb <= hi

    # THE TWO VECTOR DIFFERENCES VERY NEARLY CANCEL, and that is the finding
    # rather than an accident worth hiding. Copy number falls about 6x on a
    # rom-intact pBR322 replicon against GolB's pUC-type origin; promoter
    # strength rises about 5x on T7 against a generic E. coli promoter. The
    # group lands within a factor of two of GolB's, so the pET-24(+) arm ends
    # up close to where the proxy had it -- by cancellation, not by luck, and
    # not because the proxy was right. ISSUES.md item 67.
    golb = rd.lumped_group(rd.golb_proxy_cascade(E))
    assert 0.5 < anb / golb < 2.0, "the two vector differences nearly cancel"
    assert anb != golb, "nearly is not exactly; these are different constructs"

    mixed = rd.golb_proxy_cascade(E, construct=a)
    assert rd.lumped_group(mixed) == pytest.approx(anb)
    assert mixed["delta_c"] == E["delta_c"]["value"], "delta_c still borrowed"
    assert rd.lumped_group(arm()) == pytest.approx(anb),         "the harness must not carry its own copy"


def test_carrying_the_lump_and_its_parts_together_is_refused():
    """A value in alpha alongside alpha_N_beta is a silent double count.

    It cannot be resolved -- the two disagree about what the promoter is and
    the model has no way to prefer one -- so it must raise rather than pick.
    """
    a = dict(R["reagent_arm"])
    a["alpha"] = {"value": 2.5}
    with pytest.raises(ValueError):
        rd.golb_proxy_cascade(E, construct=a)


def test_growth_dilution_means_volumetric_yield_peaks_after_growth_stops():
    """Per-cell and per-litre yields are different questions.

    While the culture divides, mu appears as a loss term in dP_c/dt, so each
    cell holds less. The volumetric yield is P_c*X and keeps climbing after
    per-cell yield has levelled, because X is still rising.
    """
    s = rd.simulate(arm())
    i_cell = int(np.argmax(s["P_c"]))
    i_vol = int(np.argmax(s["C_prot"]))
    assert s["X"][i_vol] > 0.95 * arm()["X_cap"]
    assert i_vol >= i_cell - 1


def test_stationary_biomass_does_not_dilute_protein():
    """ISSUES 87: match the independent stationary-culture cascade solution."""
    p = arm()
    p["X_0"] = p["X_cap"]
    s = rd.simulate(p)
    t = s["t_min"]
    dm, dc = p["delta_m"], p["delta_c"]
    expected = rd.lumped_group(p) / dm * (
        (1 - np.exp(-dc*t))/dc
        - (np.exp(-dm*t)-np.exp(-dc*t))/(dc-dm))
    np.testing.assert_allclose(s["P_c"], expected,
        rtol=V["relative_tolerance"], atol=V["relative_tolerance"])


def test_expression_amplitude_does_not_change_the_normalised_trajectory():
    """Amplitude invariance does not establish decay or harvest robustness."""
    p = arm()
    q = dict(p, alpha=p["alpha"] * V["signal_per_uM"])
    a, b = rd.simulate(p), rd.simulate(q)
    np.testing.assert_allclose(a["C_prot"], b["C_prot"]/V["signal_per_uM"],
        rtol=V["relative_tolerance"], atol=V["relative_tolerance"])


def test_protein_decay_changes_the_time_course_after_growth_stops():
    """ISSUES 87: decay cannot be masked by fictitious stationary dilution."""
    p = arm()
    lo, hi = R["reagent_arm"]["delta_c"]["range"]
    a = rd.simulate(dict(p, delta_c=lo))
    b = rd.simulate(dict(p, delta_c=hi))
    assert a["C_prot"][-1] > b["C_prot"][-1]
    assert a["C_prot"][-1] > a["C_prot"][-2]


def test_source_harvest_schedule_remains_an_input_not_a_model_optimum():
    p = arm()
    s = rd.simulate(p)
    t = s["induced_at_min"] / C["minutes_per_hour"]["value"]
    source = R["reagent_arm"]["t_harvest_source_h"]["value"]
    at_source = rd.yield_at(p, t + source)
    assert 0 < at_source < s["C_prot"][-1]


def test_stationary_yield_matches_the_cascade_balance_and_band_needs_refitting():
    """ISSUES 87 supersedes the old 3x deficit; the band is not a physical cap."""
    p = arm()
    p["X_0"] = p["X_cap"]
    s = rd.simulate(p)
    steady = rd.lumped_group(p)/(p["delta_m"]*p["delta_c"])
    steady *= p["X_cap"]*p["cells_per_g"]/p["N_A"]*p["M_r"]
    assert s["C_prot"][-1] == pytest.approx(steady, rel=V["relative_tolerance"])
    # Lysis and mixing remain mass balances whatever expression model is used.
    ly = R["reagent_arm"]["lysis_yield"]["value"]
    assert rd.lysate_g_per_L(steady, ly, 1) == pytest.approx(steady*ly)
    from src import recovery_chain as rc
    target = R["reagent_arm"]["protein_target_g_per_L"]["value"]
    with pytest.raises(ValueError):
        rc.lysate_mixing_ratio(target, target)


def test_medium_capacity_scales_stationary_yield_without_guaranteeing_expression():
    x = R["reagent_arm"]["X_cap"]
    assert x["source"] is not None
    lo, hi = x["range"]
    a = rd.simulate(arm(X_cap=lo, X_0=lo))["C_prot"][-1]
    b = rd.simulate(arm(X_cap=hi, X_0=hi))["C_prot"][-1]
    assert b/a == pytest.approx(hi/lo, rel=V["relative_tolerance"])


def test_carrying_capacity_scales_the_shortfall_in_proportion():
    """The one lever with no unknown in it.

    X_cap multiplies the volumetric yield directly, so a denser culture buys
    its own factor. A fed-batch at 20 g/L would close the 37x to about 3.7x.
    """
    p10 = arm(X_cap=20.0)
    plateau10 = float(rd.simulate(p10)["C_prot"].max())
    plateau = float(rd.simulate(arm())["C_prot"].max())
    assert plateau10 / plateau == pytest.approx(10.0, rel=0.05)


def test_reduction_protein_sweeps_require_a_kinetic_transfer_assumption():
    """ISSUES 88: fixed effective FW constants cannot prove enzyme independence."""
    a = R["reagent_arm"]
    assert a["protein_target_g_per_L"]["value"] > 0
    assert R["reduction"]["k_nuc"]["status"] == "sourced_by_proxy"
    assert R["reduction"]["k_nuc"]["range"][0] < R["reduction"]["k_nuc"]["value"]


def test_protein_yield_rejects_unknown_times_instead_of_clamping_endpoints():
    """A late or invalid request must not silently report a simulated endpoint."""
    p = arm()
    end_h = R["reagent_arm"]["t_harvest_source_h"]["value"] * V["short_fraction"]
    end_min = end_h * C["minutes_per_hour"]["value"]
    end_h = end_min / C["minutes_per_hour"]["value"]
    s = rd.simulate(p, t_end_min=end_min, n=V["sample_count"])
    for t in (s["t_h"][0], end_h):
        expected = np.interp(t, s["t_h"], s["C_prot"])
        assert rd.yield_at(p, t, t_end_min=end_min,
                           n=V["sample_count"]) == pytest.approx(expected)
    for t in (-end_h, np.nextafter(end_h, np.inf), np.nan, np.inf):
        with pytest.raises(ValueError, match="simulated window"):
            rd.yield_at(p, t, t_end_min=end_min, n=V["sample_count"])


def test_mistiming_cannot_fabricate_yields_outside_the_simulation():
    p = arm()
    end_h = R["reagent_arm"]["t_harvest_source_h"]["value"]
    end_min = end_h * C["minutes_per_hour"]["value"]
    offsets = (end_h + V["short_fraction"], -end_h - V["short_fraction"])
    for offset in offsets:
        with pytest.raises(ValueError, match="simulated window"):
            rd.cost_of_mistiming(p, [offset], t_end_min=end_min,
                                n=V["sample_count"])

