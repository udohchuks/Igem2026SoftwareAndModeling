"""Equilibrium sorbent requirements and independent fresh-biomass contacts.

These calculations use the existing apparent affinity and capacity. They do
not predict contact time, transport or successful biomass regeneration.
"""
import numpy as np

from . import recovery_chain


def _validate(name, value, *, positive=False):
    if not np.isfinite(value) or value < 0 or (positive and value == 0):
        raise ValueError(f"{name} must be finite and {'positive' if positive else 'non-negative'}")
    return value


def required_site_amount(feed_gold_amount_umol, capture_volume_L,
                         dissociation_constant_uM, target_fraction):
    """Binding sites in umol needed for an equilibrium captured fraction.

    Inverting the gold balance and Langmuir law gives
    sites = fraction*feed + Kd*volume*fraction/(1-fraction).
    A target of exactly complete capture is excluded; zero feed needs no sites.
    """
    feed = _validate("feed_gold_amount_umol", feed_gold_amount_umol)
    volume = _validate("capture_volume_L", capture_volume_L, positive=True)
    affinity = _validate("dissociation_constant_uM", dissociation_constant_uM)
    fraction = _validate("target_fraction", target_fraction)
    if fraction >= 1:
        raise ValueError("target_fraction must be less than one")
    return (fraction*feed + affinity*volume*fraction/(1-fraction)) if feed else 0.0


def required_biomass(feed_gold_amount_umol, capture_volume_L,
                     dissociation_constant_uM, target_fraction, capacity_umol_per_g):
    """Dry biomass in g required by the inverse equilibrium calculation."""
    capacity = _validate("capacity_umol_per_g", capacity_umol_per_g, positive=True)
    return required_site_amount(feed_gold_amount_umol, capture_volume_L,
                                dissociation_constant_uM, target_fraction) / capacity


def fresh_contact_series(feed_gold_amount_umol, capture_volume_L,
                         dissociation_constant_uM, capacity_umol_per_g,
                         biomass_per_contact_g, contacts):
    """Independent equilibrium contacts, each with fresh biomass, at fixed volume.

    Captured gold and its biomass are removed after each contact. The returned
    residual and cumulative amounts include the pre-contact state. No original
    cells are reused, and no elution/regeneration performance is assumed.
    """
    feed = _validate("feed_gold_amount_umol", feed_gold_amount_umol)
    volume = _validate("capture_volume_L", capture_volume_L, positive=True)
    affinity = _validate("dissociation_constant_uM", dissociation_constant_uM)
    capacity = _validate("capacity_umol_per_g", capacity_umol_per_g, positive=True)
    biomass = _validate("biomass_per_contact_g", biomass_per_contact_g)
    if isinstance(contacts, (bool, np.bool_)) or not isinstance(contacts, (int, np.integer)) or contacts < 0:
        raise ValueError("contacts must be a non-negative integer")
    residual, captured_each = [feed], []
    for _ in range(contacts):
        captured = float(recovery_chain.capture_equilibrium(
            residual[-1]/volume, capacity*biomass/volume, affinity)) * volume
        captured_each.append(captured)
        residual.append(residual[-1]-captured)
    residual = np.asarray(residual)
    return dict(contact_number=np.arange(len(residual)),
                residual_gold_amount_umol=residual,
                cumulative_captured_gold_amount_umol=feed-residual,
                captured_per_contact_umol=np.asarray(captured_each),
                total_fresh_biomass_g=contacts*biomass)


def capacity_scenario(feed_gold_amount_umol, capture_volume_L,
                      dissociation_constant_uM, capacity_umol_per_g, biomass_mass_g):
    """Forward equilibrium capture at a stated capacity, for scenario comparison.

    The inverse of `required_site_amount`: that one asks what capacity a target
    needs, this one asks what a capacity delivers. Site occupancy is reported
    beside the captured fraction because a low fraction at high occupancy is a
    sizing result, while a low fraction at low occupancy is an affinity result.

    The capacity argument carries whatever meaning its source gave it. A
    single-occupancy site inventory and a measured whole-cell loading are not
    the same observable, and this function cannot tell them apart.
    """
    feed = _validate("feed_gold_amount_umol", feed_gold_amount_umol)
    volume = _validate("capture_volume_L", capture_volume_L, positive=True)
    affinity = _validate("dissociation_constant_uM", dissociation_constant_uM)
    capacity = _validate("capacity_umol_per_g", capacity_umol_per_g, positive=True)
    biomass = _validate("biomass_mass_g", biomass_mass_g)
    sites = capacity * biomass
    bound = float(recovery_chain.capture_equilibrium(
        feed/volume, sites/volume, affinity)) * volume
    return dict(capacity_umol_per_g=capacity, biomass_mass_g=biomass,
                site_amount_umol=sites, bound_gold_amount_umol=bound,
                unbound_gold_amount_umol=feed-bound,
                captured_fraction=bound/feed if feed else 0.0,
                site_occupancy=bound/sites if sites else 0.0)
