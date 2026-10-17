"""Capture design calculations invert equilibrium and conserve gold."""
import numpy as np
import pytest

from src import capture_design, params, recovery_audit, recovery_chain

P = recovery_audit.operating_parameters()
V = params.values(params.load("recovery_process")["volumes"])
T = params.values(params.load("recovery_audit")["verification"])


def test_required_sites_and_biomass_recover_the_requested_equilibrium_fraction():
    feed = P["Au_feed"] * V["feed_volume_L"]
    volume = V["capture_volume_L"]
    for fraction in (T["short_fraction"], T["plateau_fraction"]):
        sites = capture_design.required_site_amount(feed, volume, P["K_Au"], fraction)
        bound = recovery_chain.capture_equilibrium(feed/volume, sites/volume, P["K_Au"])*volume
        assert bound/feed == pytest.approx(fraction)
        biomass = capture_design.required_biomass(feed, volume, P["K_Au"], fraction, P["q_max"])
        assert biomass*P["q_max"] == pytest.approx(sites)


def test_dilution_with_fixed_gold_and_biomass_cannot_increase_bound_amount():
    feed = P["Au_feed"] * V["feed_volume_L"]
    sites = P["q_max"]*P["X_max"]*V["feed_volume_L"]
    original_volume = V["capture_volume_L"]
    diluted_volume = original_volume/T["short_fraction"]
    bound = [recovery_chain.capture_equilibrium(feed/volume, sites/volume, P["K_Au"])*volume
             for volume in (original_volume, diluted_volume)]
    assert bound[-1] <= bound[0]


def test_fresh_contacts_conserve_gold_and_charge_biomass_for_every_contact():
    feed = P["Au_feed"]*V["feed_volume_L"]
    biomass = P["X_max"]*V["feed_volume_L"]
    contacts = T["sample_count"]
    result = capture_design.fresh_contact_series(feed, V["capture_volume_L"], P["K_Au"],
                                                P["q_max"], biomass, contacts)
    np.testing.assert_allclose(result["residual_gold_amount_umol"]
        + result["cumulative_captured_gold_amount_umol"], feed)
    np.testing.assert_allclose(-np.diff(result["residual_gold_amount_umol"]),
                               result["captured_per_contact_umol"])
    assert np.all(result["residual_gold_amount_umol"] >= 0)
    assert np.all(result["captured_per_contact_umol"] <= biomass*P["q_max"])
    assert result["total_fresh_biomass_g"] == contacts*biomass


def test_capture_design_refuses_invalid_inputs_and_zero_feed_needs_no_sites():
    zero = V["lysate_volume_L"]
    fraction = T["short_fraction"]
    assert capture_design.required_site_amount(zero, V["capture_volume_L"], P["K_Au"], fraction) == zero
    for invalid in (np.nan, -fraction, V["feed_volume_L"]):
        with pytest.raises(ValueError):
            capture_design.required_site_amount(P["Au_feed"], V["capture_volume_L"], P["K_Au"], invalid)
    with pytest.raises(ValueError):
        capture_design.required_biomass(P["Au_feed"], V["capture_volume_L"], P["K_Au"], fraction, zero)
    with pytest.raises(ValueError):
        capture_design.fresh_contact_series(P["Au_feed"], V["capture_volume_L"], P["K_Au"], P["q_max"], P["X_max"], fraction)


def test_capacity_scenario_inverts_required_site_amount():
    feed = P["Au_feed"] * V["feed_volume_L"]
    volume = V["capture_volume_L"]
    for fraction in (T["short_fraction"], T["plateau_fraction"]):
        sites = capture_design.required_site_amount(feed, volume, P["K_Au"], fraction)
        scenario = capture_design.capacity_scenario(feed, volume, P["K_Au"],
                                                    sites/P["X_max"], P["X_max"])
        assert scenario["site_amount_umol"] == pytest.approx(sites)
        assert scenario["captured_fraction"] == pytest.approx(fraction)


def test_capacity_scenario_rises_with_capacity_and_stays_inside_feed_and_sites():
    feed = P["Au_feed"] * V["feed_volume_L"]
    volume = V["capture_volume_L"]
    literature = params.values(params.load("capture_design")["literature"])
    capacities = sorted([P["q_max"]] + list(literature.values()))
    bound = []
    for capacity in capacities:
        scenario = capture_design.capacity_scenario(feed, volume, P["K_Au"],
                                                    capacity, P["X_max"])
        assert 0 <= scenario["bound_gold_amount_umol"] <= feed
        assert scenario["bound_gold_amount_umol"] <= scenario["site_amount_umol"]
        assert scenario["bound_gold_amount_umol"] + scenario["unbound_gold_amount_umol"] \
            == pytest.approx(feed)
        bound.append(scenario["bound_gold_amount_umol"])
    assert bound == sorted(bound)


def test_literature_capacities_are_other_system_and_not_adopted_as_the_project_capacity():
    """ISSUES 91 and 92. Published loadings are scenario inputs, never the parameter.

    The project capacity stays null until it is measured in the project matrix,
    so `params.values` must keep omitting it and raise KeyError at the point of use.
    """
    capture = params.load("recovery_chain")["V1_capture"]
    assert capture["whole_cell_capacity"]["value"] is None
    assert "whole_cell_capacity" not in params.values(capture)
    literature = params.load("capture_design")["literature"]
    assert literature, "the literature block must not be emptied"
    for name, spec in literature.items():
        assert "other_system" in spec["status"], name
        assert spec["conditions"].strip(), name
        assert spec["value"] != P["q_max"], name
