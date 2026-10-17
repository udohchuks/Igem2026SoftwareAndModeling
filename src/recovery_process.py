"""Amount-conserving capture, elution and reduction with explicit liquid volumes.

Volume settings are illustrative. Transfers conserve gold; capture equilibrium
and empirical elution are unchanged. Physical collection is outside the model.
"""
import numpy as np

from . import params, recovery_audit, recovery_chain, reduction


def _validate(name, value, *, positive=False):
    if not np.isfinite(value) or value < 0 or (positive and value == 0):
        raise ValueError(f"{name} must be finite and {'positive' if positive else 'non-negative'}")
    return value


def run(*, feed_volume_L=None, capture_volume_L=None, elution_volume_L=None,
        lysate_volume_L=None, biomass_mass_g=None, feed_gold_concentration_uM=None,
        lysate_protein_uM=None, protein_supply="target", nucleation_rate_per_h=None,
        growth_rate_per_uM_h=None, reduction_duration_h=None, seed_fraction=None,
        final_protein_concentration_uM=None):
    """Return gold amounts in umol, concentrations in uM, and stage efficiencies.

    Biomass defaults to the original reference biomass inventory, even when
    volumes change. The target protein mode supplies the reference final dose
    independently. The lysate mode requires its measured protein concentration
    and computes final dose from the added volume; missing data raise KeyError.

    Internal parameter mapping: feed_gold_concentration_uM -> Au_feed,
    nucleation_rate_per_h -> k_nuc, growth_rate_per_uM_h -> k_grow,
    reduction_duration_h -> t_reduce_h, seed_fraction -> seed_frac,
    final_protein_concentration_uM -> E_tot. Biomass mass replaces the implicit
    X_max concentration; binding capacity still comes from the expression joint.
    """
    reference = params.values(params.load("recovery_process")["volumes"])
    supplied = dict(feed_volume_L=feed_volume_L, capture_volume_L=capture_volume_L,
                    elution_volume_L=elution_volume_L, lysate_volume_L=lysate_volume_L)
    volumes = {key: _validate(key, reference[key] if value is None else value,
                             positive=key != "lysate_volume_L")
               for key, value in supplied.items()}
    p = recovery_audit.operating_parameters()
    biomass = _validate("biomass_mass_g", p["X_max"] * reference["feed_volume_L"]
                        if biomass_mass_g is None else biomass_mass_g)
    feed_concentration = _validate("feed_gold_concentration_uM", p["Au_feed"]
        if feed_gold_concentration_uM is None else feed_gold_concentration_uM)
    feed_amount = feed_concentration * volumes["feed_volume_L"]
    capture_concentration = feed_amount / volumes["capture_volume_L"]
    site_amount = p["q_max"] * biomass
    bound = float(recovery_chain.capture_equilibrium(capture_concentration,
        site_amount / volumes["capture_volume_L"], p["K_Au"])) * volumes["capture_volume_L"]
    elution_efficiency = float(recovery_chain.eta_elute(p["t_elute_h"], p["phi"], p["k_elute"]))
    eluted = bound * elution_efficiency
    reduction_volume = volumes["elution_volume_L"] + volumes["lysate_volume_L"]
    if protein_supply == "lysate":
        if final_protein_concentration_uM is not None:
            raise ValueError("final_protein_concentration_uM requires protein_supply='target'")
        if lysate_protein_uM is None:
            raise KeyError("lysate_protein_uM")
        p["E_tot"] = (_validate("lysate_protein_uM", lysate_protein_uM)
                      * volumes["lysate_volume_L"] / reduction_volume)
    elif protein_supply != "target":
        raise ValueError("protein_supply must be target or lysate")
    elif lysate_protein_uM is not None:
        raise ValueError("lysate_protein_uM requires protein_supply='lysate'")
    elif final_protein_concentration_uM is not None:
        p["E_tot"] = _validate("final_protein_concentration_uM", final_protein_concentration_uM)
    for key, value in (("k_nuc", nucleation_rate_per_h),
                       ("k_grow", growth_rate_per_uM_h),
                       ("t_reduce_h", reduction_duration_h)):
        if value is not None:
            p[key] = value
    if seed_fraction is not None:
        p.update(seeding_on=True, seed_frac=seed_fraction)
    trajectory = reduction.simulate(eluted / reduction_volume, p)
    metal = float(trajectory["metal_new"][-1]) * reduction_volume
    unreduced = float(trajectory["Au_aq"][-1]) * reduction_volume
    unbound, uneluted = feed_amount - bound, bound - eluted
    residual = feed_amount - unbound - uneluted - unreduced - metal
    settings = params.values(params.load("reduction_solver")["solver"])
    tolerance = settings["check_factor"] * (settings["atol"] * reduction_volume
                                            + settings["rtol"] * feed_amount)
    if abs(residual) > tolerance:
        raise RuntimeError("recovery process violates gold conservation")
    return dict(**volumes, reduction_volume_L=reduction_volume,
        biomass_mass_g=biomass, binding_site_amount_umol=site_amount,
        feed_gold_concentration_uM=feed_concentration,
        capture_gold_concentration_uM=capture_concentration,
        eluate_gold_concentration_uM=eluted / volumes["elution_volume_L"],
        reduction_gold_concentration_uM=eluted / reduction_volume,
        reduction_protein_concentration_uM=p["E_tot"], feed_gold_amount_umol=feed_amount,
        bound_gold_amount_umol=bound, eluted_gold_amount_umol=eluted,
        unbound_gold_amount_umol=unbound, uneluted_gold_amount_umol=uneluted,
        unreduced_gold_amount_umol=unreduced, new_metal_amount_umol=metal,
        capture_efficiency=bound / feed_amount if feed_amount else 0.0,
        elution_efficiency=elution_efficiency, reduction_efficiency=trajectory["eta_reduce"],
        metal_fraction_of_feed=metal / feed_amount if feed_amount else 0.0,
        gold_balance_residual_umol=residual, reduction_trajectory=trajectory)
