"""Audit regressions: independent balances and previously uncovered failures."""
import numpy as np
import pytest
from src import params, recovery_audit as audit, recovery_chain as rc
from src import sensitivity as sn, fit_fw

V = params.values(params.load("recovery_audit")["verification"])


def test_incomplete_calibrated_data_are_not_rescaled_to_full_conversion():
    p = audit.operating_parameters()
    a = audit.stage_amounts(p)["eluate_uM"]
    # Use the slow scenario so both kinetic terms are observable.
    kn = params.load("recovery_chain")["reduction"]["k_nuc"]["range"][0]
    kg = p["k_grow"]
    end = fit_fw.t_to_conversion(a, kn, kg, V["short_fraction"])
    t = np.linspace(0, end, V["sample_count"])
    metal = fit_fw.finke_watzky_curve(t, a, kn, kg)
    for signal, kw in ((metal, {}), (a-metal, {"dissolved": True}),
                       (V["baseline"] + metal*V["signal_per_uM"],
                        {"signal_per_uM": V["signal_per_uM"], "baseline": V["baseline"]})):
        got = fit_fw.fit_finke_watzky(t, signal, a, **kw)
        assert got[0] == pytest.approx(kn, rel=V["relative_tolerance"])
        assert got[1] == pytest.approx(kg, rel=V["relative_tolerance"])


def test_low_feed_capture_preserves_the_mass_balance():
    p = audit.operating_parameters()
    a, s, k = V["dilute_feed"], p["q_max"]*p["X_max"], p["K_Au"]
    bound = rc.capture_equilibrium(a, s, k)
    assert bound/a == pytest.approx(s/(s+k), rel=V["relative_tolerance"])
    assert bound == pytest.approx(s*(a-bound)/(k+a-bound), rel=V["relative_tolerance"], abs=0)
    with np.errstate(divide="raise", invalid="raise"):
        assert rc.eta_capture(0, s, k) == 0


def test_ensemble_runs_with_only_the_three_in_scope_stages():
    p = audit.operating_parameters()
    spec = params.load("recovery_chain")["reduction"]["k_nuc"]
    samples, out, ranks = sn.run(p, {"k_nuc": (*spec["range"], "log")},
                                n=V["sample_count"], seed=V["seed"])
    assert "eta_phys" not in out
    np.testing.assert_allclose(out["eta_total"], out["eta_capture"]*out["eta_elute"]*out["eta_reduce"])
    assert np.isfinite(ranks["k_nuc"])


def test_ties_cannot_manufacture_a_sensitivity_result():
    x = np.arange(V["sample_count"])
    constant = np.ones_like(x)
    assert np.all(sn._rank(constant) == np.mean(sn._rank(constant)))
    assert np.isnan(sn.prcc({"x": x}, constant)["x"])


def test_reduction_uncertainty_includes_the_declared_slow_scenario():
    band = audit.reduction_scenario_range()
    assert band["slow_corner"] < V["relative_tolerance"] < band["fast_corner"]


def test_zero_protein_has_no_protein_mediated_reduction():
    p = audit.operating_parameters()
    assert sn.reduce_finke_watzky(p["Au_feed"], dict(p, E_tot=0)) == 0


def test_unknown_damage_coefficient_is_not_replaced_by_a_guess():
    block = params.load("recovery_chain")["V1_capture"]
    assert block["lambda_D"]["value"] is None
    with pytest.raises(KeyError):
        params.values(block)["lambda_D"]


def test_no_autocatalysis_reduces_to_first_order_and_no_nucleation_stays_zero():
    p = audit.operating_parameters()
    t = np.linspace(0, p["t_reduce_h"], V["sample_count"])
    expected = p["Au_feed"] * -np.expm1(-p["k_nuc"]*t)
    np.testing.assert_allclose(
        fit_fw.finke_watzky_curve(t, p["Au_feed"], p["k_nuc"], 0), expected)
    assert np.all(fit_fw.finke_watzky_curve(t, p["Au_feed"], 0, p["k_grow"]) == 0)
