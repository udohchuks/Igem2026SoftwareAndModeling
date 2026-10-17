"""Independent balance and limiting-case verification; no biological calibration."""
import numpy as np
import pytest

from src import params, reduction, recovery_chain, fit_fw

R = params.load("recovery_chain")
V = params.values(params.load("reduction_solver")["verification"])
S = params.values(params.load("reduction_solver")["solver"])


def operating():
    p = params.values(R["reduction"])
    p.update(params.values(params.load("recovery_audit")["operating"]))
    arm = params.values(R["reagent_arm"])
    p["E_tot"] = recovery_chain.protein_uM(arm["protein_target_g_per_L"],
                                          arm["M_r_reductase"])
    return p


@pytest.mark.parametrize("seeded", [False, True])
@pytest.mark.parametrize("recharge", [False, True])
@pytest.mark.parametrize("oxidation", [False, True])
def test_gold_and_electron_ledgers_close(seeded, recharge, oxidation):
    p = operating()
    p.update(seeding_on=seeded, seed_frac=R["reduction"]["seed_frac"]["modelled_band"][0])
    if not recharge:
        p["k_rech"] = 0
    if not oxidation:
        p["k_ox"] = 0
    out = reduction.simulate(p["Au_feed"], p)
    for key in ("gold_residual", "electron_residual"):
        np.testing.assert_allclose(out[key], 0, atol=V["comparison_tolerance"])
    assert out["eta_reduce"] <= out["donor_ceiling"]+V["comparison_tolerance"]


def test_starved_donor_caps_metal_without_recharge():
    p = operating()
    p.update(Rech_0=0, k_rech=0, k_ox=0,
             E_tot=p["nu"]*p["Au_feed"]*V["donor_limited_fraction"])
    out = reduction.simulate(p["Au_feed"], p)
    np.testing.assert_allclose(out["E_red"]+p["nu"]*out["metal_new"],
                               p["E_tot"], atol=V["comparison_tolerance"])
    assert out["eta_reduce"] == pytest.approx(V["donor_limited_fraction"],
                                               abs=V["comparison_tolerance"])


def test_donor_excess_matches_independent_finke_watzky_solution():
    p = operating()
    p.update(E_tot=p["Au_feed"]*V["donor_excess_multiplier"], k_ox=0, k_rech=0)
    out = reduction.simulate(p["Au_feed"], p)
    expected = fit_fw.finke_watzky_curve(out["t_h"], p["Au_feed"], p["k_nuc"], p["k_grow"])
    np.testing.assert_allclose(out["metal_new"], expected,
                               rtol=V["comparison_tolerance"], atol=V["comparison_tolerance"])


def test_seed_is_never_counted_as_new_product():
    p = operating()
    p.update(seeding_on=True, seed_frac=R["reduction"]["seed_frac"]["modelled_band"][0])
    out = reduction.simulate(p["Au_feed"], p, t_end=0)
    assert out["eta_reduce"] == 0
    assert out["Au_s"][0] == p["seed_frac"]*p["Au_feed"]
    assert out["metal_new"][0] == 0


def test_reference_dose_reproduces_effective_model_exactly():
    p = operating()
    fixed = reduction.simulate(p["Au_feed"], p)
    scaled = reduction.simulate(p["Au_feed"], p, protein_scaling="linear_reference", E_ref=p["E_tot"])
    np.testing.assert_array_equal(fixed["metal_new"], scaled["metal_new"])


def test_linear_reference_dose_response_is_a_distinct_structural_hypothesis():
    p = operating()
    ref = p["E_tot"]
    p["E_tot"] *= V["dose_fraction"]
    end = 1/p["k_nuc"]
    fixed = reduction.simulate(p["Au_feed"], p, t_end=end)
    scaled = reduction.simulate(p["Au_feed"], p, t_end=end,
                                 protein_scaling="linear_reference", E_ref=ref)
    assert scaled["eta_reduce"] < fixed["eta_reduce"]


@pytest.mark.parametrize("key", ["k_nuc", "k_grow", "k_rech", "k_ox", "Rech_0", "E_tot", "nu", "nu_rech", "K_inh"])
def test_negative_parameters_are_rejected(key):
    p = operating()
    p[key] = -1
    with pytest.raises(ValueError):
        reduction.simulate(p["Au_feed"], p)


def test_missing_stoichiometry_and_reference_are_not_guessed():
    p = operating()
    del p["nu_rech"]
    with pytest.raises(KeyError):
        reduction.simulate(p["Au_feed"], p)
    with pytest.raises(KeyError):
        reduction.simulate(operating()["Au_feed"], operating(), protein_scaling="linear_reference")


def test_zero_gold_protein_and_initial_reducing_power_are_supported():
    p = operating()
    assert reduction.simulate(0, p)["eta_reduce"] == 0
    assert reduction.simulate(p["Au_feed"], dict(p, E_tot=0))["eta_reduce"] == 0
    out = reduction.simulate(p["Au_feed"], dict(p, Rech_0=0), initial_reduced_fraction=0)
    assert out["eta_reduce"] == 0


@pytest.mark.parametrize("bad", [-1, np.nan, np.inf])
def test_invalid_charge_and_duration_are_rejected(bad):
    p = operating()
    with pytest.raises(ValueError):
        reduction.simulate(bad, p)
    with pytest.raises(ValueError):
        reduction.simulate(p["Au_feed"], p, t_end=bad)


def test_endpoint_only_sampling_matches_trajectory():
    p = operating()
    whole = reduction.simulate(p["Au_feed"], p)
    endpoint = reduction.simulate(p["Au_feed"], p, times=[p["t_reduce_h"]])
    assert endpoint["eta_reduce"] == pytest.approx(whole["eta_reduce"], abs=S["atol"])


def test_solver_failure_is_reported(monkeypatch):
    class Failed:
        success = False
        message = "synthetic solver failure"
    monkeypatch.setattr(reduction, "solve_ivp", lambda *args, **kwargs: Failed())
    p = operating()
    with pytest.raises(RuntimeError, match="synthetic solver failure"):
        reduction.simulate(p["Au_feed"], p)
