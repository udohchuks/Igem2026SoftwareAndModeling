"""Explicit amounts prevent dilution or seed addition from creating feed gold."""
import numpy as np
import pytest

from src import params, recovery_audit, recovery_process


V = params.values(params.load("recovery_process")["volumes"])
T = params.values(params.load("recovery_audit")["verification"])


def assert_ledger(result):
    total = sum(result[key] for key in ("unbound_gold_amount_umol",
        "uneluted_gold_amount_umol", "unreduced_gold_amount_umol", "new_metal_amount_umol"))
    assert total == pytest.approx(result["feed_gold_amount_umol"])
    assert result["new_metal_amount_umol"] <= result["eluted_gold_amount_umol"] + T["dilute_feed"]


def test_equal_volumes_reproduce_the_existing_reference():
    previous = recovery_audit.stage_amounts()
    result = recovery_process.run()
    assert result["new_metal_amount_umol"] == pytest.approx(
        previous["metal_umol_per_initial_L"] * V["feed_volume_L"], rel=T["relative_tolerance"])
    assert result["bound_gold_amount_umol"] == pytest.approx(previous["bound_uM"] * V["feed_volume_L"])
    assert_ledger(result)


def test_volume_changes_and_seed_cannot_create_feed_gold_or_binding_sites():
    baseline = recovery_process.run()
    factor = T["short_fraction"]
    result = recovery_process.run(feed_volume_L=V["feed_volume_L"] / factor,
        feed_gold_concentration_uM=baseline["feed_gold_concentration_uM"] * factor,
        capture_volume_L=V["capture_volume_L"] / factor,
        elution_volume_L=V["elution_volume_L"] * factor,
        seed_fraction=factor)
    assert result["feed_gold_amount_umol"] == pytest.approx(baseline["feed_gold_amount_umol"])
    assert result["biomass_mass_g"] == baseline["biomass_mass_g"]
    assert result["binding_site_amount_umol"] == baseline["binding_site_amount_umol"]
    assert_ledger(result)


def test_lysate_dilution_conserves_gold_and_computes_the_actual_protein_dose():
    baseline = recovery_process.run()
    lysate_volume = V["elution_volume_L"] * T["short_fraction"]
    concentration = baseline["reduction_protein_concentration_uM"]
    result = recovery_process.run(lysate_volume_L=lysate_volume,
        lysate_protein_uM=concentration, protein_supply="lysate")
    total_volume = V["elution_volume_L"] + lysate_volume
    assert result["eluted_gold_amount_umol"] == baseline["eluted_gold_amount_umol"]
    assert result["reduction_gold_concentration_uM"] == pytest.approx(
        baseline["eluted_gold_amount_umol"] / total_volume)
    assert result["reduction_protein_concentration_uM"] == pytest.approx(concentration * lysate_volume / total_volume)
    assert_ledger(result)


def test_invalid_volumes_and_unknown_lysate_concentration_are_rejected():
    for volume in ("feed_volume_L", "capture_volume_L", "elution_volume_L"):
        for invalid in (V["lysate_volume_L"], -V[volume], np.nan):
            with pytest.raises(ValueError):
                recovery_process.run(**{volume: invalid})
    with pytest.raises(ValueError):
        recovery_process.run(lysate_volume_L=-V["elution_volume_L"])
    with pytest.raises(KeyError, match="lysate_protein_uM"):
        recovery_process.run(protein_supply="lysate")


def test_final_protein_override_is_explicit_and_cannot_conflict_with_lysate_mode():
    concentration = recovery_audit.operating_parameters()["E_tot"] * T["short_fraction"]
    result = recovery_process.run(final_protein_concentration_uM=concentration)
    assert result["reduction_protein_concentration_uM"] == concentration
    with pytest.raises(ValueError):
        recovery_process.run(protein_supply="lysate", lysate_protein_uM=concentration,
                             final_protein_concentration_uM=concentration)
