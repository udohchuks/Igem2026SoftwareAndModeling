"""The two joints between the three models.

This is the only place where one part's output becomes another part's input.
Each part still runs standalone; nothing here is imported by the model
modules themselves.

JOINT 1  Part I  -> Part III   Au(S2O3)2 3- concentration  ->  Au_feed
JOINT 2  Part II -> Part III   active sites per cell       ->  q_max

WHAT ELSE CROSSES JOINT 1, added 2026-08-12
-------------------------------------------
A joint is not only the quantity the two documents agreed to talk about. The
leach liquor carries everything else too, and the audit of Part I's sequential
model found that the gold is the smallest part of it:

    gold complex Au(S2O3)2 3-        39 umol/L
    copper, Cu(I) + Cu(II)          829 umol/L      21x the gold
    tetrathionate S4O6 2-        47,251 umol/L   1,212x the gold

Part III consumes none of the last two and has no term for either. Copper was
already flagged as a selectivity unknown. Tetrathionate is worse than unknown:
it is a thiol-blocking reagent arriving at a protein that binds gold with a
pair of cysteines. See `sulfur_feed_from_leach` and ISSUES.md item 44.

TRITHIONATE JOINED THEM, 2026-08-19
-----------------------------------
The alkaline decomposition route added to Part I on 2026-08-19 recycles
tetrathionate into thiosulfate, and makes trithionate S3O6 2- doing it. Two of
every four tetrathionate become trithionate, nothing consumes it at 25 C, and
it becomes the LARGEST sulfur pool in the vessel:

    ammonia scenario     S4O6  9,097   S3O6  49,239   umol/L at 72 h
    glycine scenario     S4O6  8,220   S3O6  16,578   umol/L at 72 h

Between the change that created trithionate and the audit that caught the
omission, both on 2026-08-19, this joint carried tetrathionate alone and
reported a polythionate load 3.0x to 6.4x lower than the model's own answer.
That is the same silent drop at the joint that item 44 was raised to stop, in
the same file, seven days after item 44's fix landed. So it is now carried
explicitly and `sulfur_feed_from_leach` requires it rather than defaulting it
to zero.

Both adapters carry the unit conversion and assert the units of their input,
because the three parts do not share a unit system:

    Part I    umol/L, minutes
    Part II   molecules/cell, minutes
    Part III  uM, hours, g/L
"""

from . import params as _params

_CONV = _params.load("conversions")
_CAPTURE = _params.load("recovery_chain")["V1_capture"]
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


#: GolB binds Au(I) through one Cys-X-X-Cys motif, so two thiols per site.
THIOLS_PER_GOLB_SITE = 2


def sulfur_feed_from_leach(s4o6, s2o3, s3o6, unit="umol/L"):
    """JOINT 1, the part nobody was carrying. ISSUES.md item 44.

    Until 2026-08-12 this joint carried gold, and later copper. It never
    carried the sulfur species, because nothing suggested they mattered. They
    are the largest thing in the stream by three orders of magnitude, and one
    of them attacks the capture protein.

    TETRATHIONATE IS A THIOL-BLOCKING REAGENT. It attacks a free cysteine to
    form a sulfenylthiosulfate, and where two cysteines sit close together, as
    they do in GolB's Cys-X-X-Cys motif, it closes an intramolecular disulfide.
    Either outcome removes the gold binding site. In the sequential design
    tetrathionate is a dead-end product that nothing converts back, so it
    accumulates to about 47,000 umol/L and travels to capture with the gold.

    Free thiosulfate is carried too, and it matters for the opposite reason.
    Capture is a ligand exchange that releases thiosulfate:

        Au(S2O3)2 3-  +  GolB(SH)2  <->  GolB-Au  +  2 S2O3 2-

    so how much is already present sets where that equilibrium sits, and
    K_Au is only valid at the thiosulfate level it was measured at. See
    ISSUES.md item 22, whose premise of a thiosulfate-rich leachate the
    sequential model has now reversed.

    TRITHIONATE IS REQUIRED, NOT OPTIONAL. It has no default, so a caller
    that has not decided what to do with it fails loudly. Defaulting it to
    zero would reproduce the exact bug this argument was added to fix: a
    sulfur species dropped at the joint while the numbers still looked
    plausible.

    Returns a dict. Nothing is consumed by Part III; this makes the stream
    visible rather than silently dropping it at the joint.
    """
    if unit not in ("umol/L", "uM"):
        raise UnitError(f"sulfur_feed_from_leach expects umol/L or uM, got {unit!r}.")
    return {"S4O6_uM": float(s4o6), "S2O3_uM": float(s2o3),
            "S3O6_uM": float(s3o6),
            "polythionate_uM": float(s4o6) + float(s3o6),
            "consumed_by_part_III": False}


def thiol_blocking_warning(s4o6_uM, q_max=None, X_max=None, s3o6_uM=0.0):
    """Test the polythionate load against the cysteines it can block.

    Returns a short string, or None if there is no polythionate at all.
    Defaults to the capture parameters in params/recovery_chain.yaml.

    There is no rate here and no claim of one. The point is the ratio: at a
    large enough excess the reaction does not need to be fast or efficient to
    finish, and one experiment settles it. ISSUES.md item 44.

    TWO RATIOS ARE REPORTED, AND THE SECOND IS A BOUND, NOT A RESULT
    ---------------------------------------------------------------
    Tetrathionate's mechanism is established: the cysteine thiolate attacks
    the outer sulfur of S4O6 2- to give a cysteine-S-sulfonate, and where two
    cysteines sit close together, as they do in GolB's Cys-X-X-Cys motif, the
    sulfenylthiosulfate intermediate closes an intramolecular disulfide.
    Either outcome removes the binding site.

    TRITHIONATE'S RELATIVE REACTIVITY IS NOT PUBLISHED. It is a polythionate
    and it does react with thiols, but no measurement comparing it with
    tetrathionate was found in the accessible literature, and the structures
    differ in a way that should matter: tetrathionate carries two sulfane
    sulfurs joined by an S-S bond, trithionate carries one, flanked by two
    sulfonates.

    So no relative rate constant is invented here. The tetrathionate ratio is
    reported as the established figure, and the combined polythionate ratio as
    an UPPER BOUND that assumes trithionate is as reactive as tetrathionate.
    The truth is between them, and one binding assay would say where.

    `s3o6_uM` keeps a default of zero, unlike `sulfur_feed_from_leach`, because
    the trithionate term only exists when Part I's alkaline route is switched
    on. A run without it genuinely has none.
    """
    total = s4o6_uM + s3o6_uM
    if total <= 0.0:
        return None
    q = _CAPTURE["q_max"]["value"] if q_max is None else q_max
    X = _CAPTURE["X_max"]["value"] if X_max is None else X_max
    thiols = THIOLS_PER_GOLB_SITE * q * X
    note = (f"S4O6 = {s4o6_uM:.0f} uM against {thiols:.4g} uM of GolB "
            f"cysteines, an excess of {s4o6_uM / thiols:,.0f} to 1. "
            "Tetrathionate S-sulfonates free thiols and closes disulfides "
            "across Cys-X-X-Cys motifs. Reduce the liquor or the cells before "
            "capture. ISSUES.md item 44.")
    if s3o6_uM > 0.0:
        note += (f" Plus S3O6 = {s3o6_uM:.0f} uM of trithionate, taking the "
                 f"polythionate total to {total:.0f} uM, "
                 f"{total / thiols:,.0f} to 1. That second ratio is an UPPER "
                 "BOUND: trithionate's reactivity toward thiols relative to "
                 "tetrathionate is not published, so it is counted here as if "
                 "equal. ISSUES.md item 60.")
    return note


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
    ceiling = _CAPTURE["q_max"]["value"] * _CAPTURE["X_max"]["value"]
    lo, hi = _CAPTURE["Au_feed"]["range"]
    if au_feed_uM > ceiling:
        return (f"Au_feed = {au_feed_uM:.3g} uM is above the {ceiling:.3g} uM "
                f"capacity ceiling q_max*X_max. Capture is capacity-limited "
                f"here. Note the ceiling moved from 22 uM to {ceiling:.3g} uM "
                "when Part II's q_max was adopted; see ISSUES.md item 2.")
    if au_feed_uM > hi:
        return (f"Au_feed = {au_feed_uM:.3g} uM is above the revised "
                f"{lo}-{hi} uM window.")
    if au_feed_uM < lo:
        return (f"Au_feed = {au_feed_uM:.3g} uM is below the revised "
                f"{lo}-{hi} uM window. Fraction captured is high but absolute "
                "gold recovered is low (Part III section 6).")
    return None


#: The value Part III used before 2026-08-10. Kept as a named constant so the
#: historical 255x disagreement stays checkable after the adoption decision.
QMAX_PART_III_SUPERSEDED = 4.4


def qmax_disagreement(q_max_from_part_II,
                      q_max_in_part_III=QMAX_PART_III_SUPERSEDED):
    """Report the ratio between the two q_max estimates.

    On 2026-08-10 the team adopted Part II as the authority for every
    protein-model quantity, so params/recovery_chain.yaml now carries
    q_max = 0.0163 and keeps 4.4 beside it as `superseded`. The default here
    is the superseded value, so this function still measures the original
    disagreement. See ISSUES.md item 2.
    """
    return {
        "part_II_uM_per_gL": q_max_from_part_II,
        "part_III_uM_per_gL": q_max_in_part_III,
        "ratio_II_over_III": q_max_from_part_II / q_max_in_part_III,
    }
