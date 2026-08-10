"""The two joints between the three models.

This is the only place where one part's output becomes another part's input.
Each part still runs standalone; nothing here is imported by the model
modules themselves.

JOINT 1  Part I  -> Part III   Au(S2O3)2 3- concentration  ->  Au_feed
JOINT 2  Part II -> Part III   active sites per cell       ->  q_max

Both adapters carry the unit conversion and assert the units of their input,
because the three parts do not share a unit system:

    Part I    umol/L, minutes
    Part II   molecules/cell, minutes
    Part III  uM, hours, g/L
"""

from . import params as _params

_CONV = _params.load("conversions")
N_A = _CONV["N_A"]["value"]
CELLS_PER_G = _CONV["cells_per_g_dry_weight"]["value"]
MIN_PER_H = _CONV["minutes_per_hour"]["value"]


class UnitError(ValueError):
    """Raised when an adapter is handed a quantity in the wrong unit."""


def au_feed_from_leach(au_complex, unit="umol/L"):
    """JOINT 1 — leachate dissolved gold becomes the V1 capture feed.

    Part III section 10: "Au_feed has no upstream model though it dominates
    V1." Part I section 4 computes [Au(S2O3)2 3-] and that is this quantity.

    Parameters
    ----------
    au_complex : float
        Dissolved gold complex concentration from Part I.
    unit : str
        Must be 'umol/L' or 'uM'. These are the same unit; both are accepted
        because the two documents use different names for it.

    Returns
    -------
    float
        Au_feed in uM, as Part III expects.

    Notes
    -----
    Part III section 2.1 recommends operating at 10-20 uM feed and shows that
    capture collapses above about 30 uM. This adapter does not clip the value.
    Use `feed_warning` to test the returned number against that guidance.

    This adapter carries gold only. Part I also produces Cu(I) and Cu(II),
    and Part III section 0 states that selectivity against Cu/Ag/Ni is
    unknown. See `cu_feed_from_leach`.
    """
    if unit not in ("umol/L", "uM"):
        raise UnitError(
            f"au_feed_from_leach expects umol/L or uM, got {unit!r}. "
            "Part I works in umol/L; Part III works in uM; they are equal."
        )
    return float(au_complex)


def cu_feed_from_leach(cu_I, cu_II, unit="umol/L"):
    """Copper carried forward from Part I. Tracked, not yet consumed.

    Part III has no copper term anywhere. Section 0 records that selectivity
    against Cu/Ag/Ni is unknown and section 10 lists it as a wet-lab fact the
    model cannot supply. This function exists so that the copper stream is
    visible in the coupled run instead of being silently dropped at the joint.
    """
    if unit not in ("umol/L", "uM"):
        raise UnitError(f"cu_feed_from_leach expects umol/L or uM, got {unit!r}.")
    return {"Cu_I_uM": float(cu_I), "Cu_II_uM": float(cu_II),
            "consumed_by_part_III": False}


def qmax_from_expression(active_sites_per_cell, cells_per_g=CELLS_PER_G):
    """JOINT 2 — active-site count becomes the capture capacity q_max.

    Part III section 9 ranks q_max measurement priority 2 and notes it is
    "being addressed by the secretion model". Part II section 5 computes the
    active-site count A* per cell. This converts one to the other.

        q_max [uM per (g/L)] = A [sites/cell] * cells_per_g [cell/g]
                               / N_A [1/mol] * 1e6 [umol/mol]

    Parameters
    ----------
    active_sites_per_cell : float
        A* from Part II, in molecules per cell.
    cells_per_g : float
        Cells per gram dry weight, from params/conversions.yaml.

    Returns
    -------
    float
        q_max in uM/(g/L), the unit Part III uses.
    """
    if active_sites_per_cell < 0:
        raise ValueError("active_sites_per_cell must be non-negative")
    mol_per_g = active_sites_per_cell * cells_per_g / N_A
    return mol_per_g * 1e6


def per_hour(rate_per_minute):
    """Convert a Part I or Part II rate constant to Part III time units."""
    return rate_per_minute * MIN_PER_H


def per_minute(rate_per_hour):
    """Convert a Part III rate constant to Part I or Part II time units."""
    return rate_per_hour / MIN_PER_H


def feed_warning(au_feed_uM):
    """Test an Au_feed value against the guidance in Part III section 2.1.

    Returns a short string, or None if the feed is inside the recommended
    10-20 uM window. The thresholds are quoted from the document; they are
    not new claims.
    """
    if au_feed_uM > 30:
        return (f"Au_feed = {au_feed_uM:.3g} uM is above 30 uM. Part III "
                "section 2.1: the A_tox disagreement costs 63-96% of capture "
                "above 30 uM.")
    if au_feed_uM > 22:
        return (f"Au_feed = {au_feed_uM:.3g} uM is above the 22 uM capacity "
                "ceiling q_max*Xmax. Part III section 2.1: capture becomes "
                "capacity-limited here.")
    if au_feed_uM < 10:
        return (f"Au_feed = {au_feed_uM:.3g} uM is below the recommended "
                "10-20 uM window. Fraction captured is high but absolute gold "
                "recovered is low (Part III section 6).")
    return None


def qmax_disagreement(q_max_from_part_II, q_max_in_part_III=4.4):
    """Report the ratio between the two independent q_max estimates.

    Part III uses 4.4 uM/(g/L) and flags it as possibly 5-13x optimistic.
    Part II implies its own value through the site count. They should be
    compared explicitly before the joint is trusted. See ISSUES.md item 2.
    """
    return {
        "part_II_uM_per_gL": q_max_from_part_II,
        "part_III_uM_per_gL": q_max_in_part_III,
        "ratio_II_over_III": q_max_from_part_II / q_max_in_part_III,
    }
