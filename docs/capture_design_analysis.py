"""Stage 3 design analyses: GolB capture of dissolved gold.

The write-up is docs/CAPTURE_DESIGN.md; the equation numbers below match it.
Each design question moves one lever the team controls and reports how the
captured gold responds.

    Conversions  (3.1)-(3.3)  gold, sites, cells and comb area per litre
    Q1           (3.4)-(3.7)  how many dry cells per litre, with copper
                              competing for the same sites
    Q2           (3.8)-(3.10) the panel area the Q1 cells need
    Q2 worked    (3.11)-(3.13) the 1 L comb that delivers it
    Q3           (3.14)-(3.16) how long one dip must last

The binding constants are GolB's own, as measured by Wei et al. (S76) and read
straight from params/capture_design.yaml. They are so far below any feed
concentration that binding is stoichiometric: gold takes every site it needs
and copper takes what is left. `check_limit` fails loudly if that ever stops
being true.

Basis: the bioleaching model's batch, 1 L of leachate from 100 g of crushed
board (docs/source/bioleaching_2026-10-17/). Every result is per litre, so it
holds at any scale; the stage ledger projects it to the plant.

No model number lives in this file. Every value is read from params/*.yaml, as
AGENTS.md rule 2 requires. The only literals below are unit conversions.

    python docs/capture_design_analysis.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src import params  # noqa: E402

MM_PER_M = 1000.0        # unit conversion
L_PER_M3 = 1000.0        # unit conversion
UMOL_PER_MOL = 1.0e6     # unit conversion
HOURS_PER_DAY = 24.0       # unit conversion
SECONDS_PER_HOUR = 3600.0  # unit conversion
MIN_PER_HOUR = 60.0        # unit conversion
G_PER_KG = 1000.0        # unit conversion
M_TO_UM = 1.0e6          # molar to micromolar
LIMIT_RATIO = 1.0e-6     # a constant this far below the feed is "stoichiometric"
TIE = 1.0e-9             # numerical tolerance, not a parameter


def inputs():
    """Collect every number this module uses, from the params files."""
    cap = params.load("capture_design")
    leach = params.load("leach")
    design = cap["stage3_design"]
    feed = leach["feed_basis"]
    prox = cap["binding_proxies"]
    recovery = params.load("recovery_chain")
    elution = recovery["elution"]
    return {
        # capture biology: GolB's own measured constants, uM
        "q_Au": cap["literature"]["wei2012_loading"]["value"],
        "Kd_Au": prox["wei2012_golb_Kd_Au"]["value"] * M_TO_UM,
        "Kd_Cu": prox["wei2012_golb_Kd_Cu"]["value"] * M_TO_UM,
        # the comb
        "rho_A": design["areal_density_g_m2"]["value"],
        "panel_L": design["panel_length_m"]["value"],
        "panel_W": design["panel_width_m"]["value"],
        "panels_per_comb": design["panels_per_comb"]["value"],
        "combs": design["combs_per_branch"]["value"],
        "dips": design["design_dips"]["value"],
        "k_on": recovery["V1_capture"]["k_on"]["value"],
        "f_cap": design["capture_fractions"]["value"],
        "f_dip": design["dip_target_fraction"]["value"],
        "t_dip": design["dip_time_h"]["value"],
        "dip_cells": design["dip_cell_loadings"]["value"],
        "D_w": design["diffusivity_water"]["value"],
        "D_ratio": design["diffusivity_biofilm_ratio"]["value"],
        "t_film": design["film_thickness_m"]["value"],
        "t_elute": design["elution_time_h"]["value"],
        "V_leach": design["leachate_volume_L"]["value"],
        "leaf_t": design["leaf_thickness_m"]["value"],
        "k_elute": elution["k_elute"]["value"],
        "phi_res": elution["phi"]["value"],
        # handoff from bioleaching
        "Au_in": design["gold_feed"]["value"],
        "Au_in_noNH3": design["gold_feed_no_ammonia"]["value"],
        "Au_in_author": design["gold_feed_author_case"]["value"],
        "Cu_band": design["copper_band"]["value"],
        "Cu_peak": design["copper_peak_ammonia"]["value"],
        # design choice and presentation settings
        "X_report": design["report_cell_loadings"]["value"],
        # plant basis and the boards
        "board_kg_day": design["plant_board_per_day"]["value"],
        "pulp_g_L": feed["pcb_loading"]["value"],
        "m_Au": feed["m_Au"]["value"],
        "M_Au": feed["M_Au"]["value"],
        "M_Cu": feed["M_Cu"]["value"],
        "M_Au_g": feed["M_Au"]["value"] * G_PER_KG,   # g/mol
        "M_Cu_g": feed["M_Cu"]["value"] * G_PER_KG,   # g/mol
    }


# --------------------------------------------------------------------
#  Conversions (3.1)-(3.3). Not an analysis.
# --------------------------------------------------------------------
def sites(p, X):
    """(3.2) Binding sites a cell loading supplies, uM."""
    return p["q_Au"] * X


def comb_area(p, X):
    """(3.3) Wetted comb area per litre that carries X, m^2/L."""
    return X / p["rho_A"]


def cells_for_sites(p, B):
    """(3.2) rearranged: dry cells per litre for B sites, g/L."""
    return B / p["q_Au"]


# --------------------------------------------------------------------
#  Q1. Gold and copper on one shared class of sites.
# --------------------------------------------------------------------
def check_limit(p, Au0):
    """(3.6) is only valid if both constants are far below the gold feed."""
    worst = max(p["Kd_Au"], p["Kd_Cu"])
    if worst >= LIMIT_RATIO * Au0:
        raise ValueError(
            "Kd = %.3g uM is not far below the %.3g uM feed: binding is not "
            "stoichiometric and (3.5) must be solved numerically instead."
            % (worst, Au0))


def bound(p, Au0, Cu0, B):
    """(3.6) Bound gold and bound copper, uM.

    The limit of the competitive equilibrium (3.5) when both dissociation
    constants are far below the feed, and gold is held far more tightly than
    copper. Gold takes every site it needs; copper takes whatever is left.
    """
    check_limit(p, Au0)
    AuB = min(Au0, B)
    CuB = min(Cu0, max(0.0, B - AuB))
    return AuB, CuB


def captured(p, X, Au0, Cu0):
    """Fraction of the dissolved gold captured, and copper's share of sites."""
    B = sites(p, X)
    AuB, CuB = bound(p, Au0, Cu0, B)
    return AuB / Au0, (CuB / B if B > 0 else 0.0)


def design_loading(p):
    """(3.7) Dry cells per litre: one site per gold atom at the richest feed,
    g/L. Sized for the richest feed so it holds for every other."""
    richest = max(p["Au_in"], p["Au_in_noNH3"], p["Au_in_author"])
    return cells_for_sites(p, richest)


def cases(p):
    """The feeds the design loading must serve. (name, Au uM, Cu uM)."""
    return [
        ("no ammonia", p["Au_in_noNH3"], p["Cu_band"][0]),
        ("ammonia, copper peak", p["Au_in"], p["Cu_peak"]),
        ("author's high-grade case", p["Au_in_author"], p["Cu_band"][-1]),
    ]


# --------------------------------------------------------------------
#  Q2. A comb of a given area, dipped again and again.
# --------------------------------------------------------------------
def comb_capacity(p, area_m2):
    """(3.8) Gold a comb can hold, umol.

    The comb carries area x rho_A grams of cells; each gram holds q_Au umol
    of gold. The area counts both faces of every panel.
    """
    return area_m2 * p["rho_A"] * p["q_Au"]


def release_fraction(p):
    """(3.9) Share of the held gold that one elution releases.

    First-order release with a residual that stays bound, from the elution
    parameters in params/recovery_chain.yaml. This governs how much of the
    captured gold reaches the next stage. It does NOT reduce the next dip:
    every dip starts with a fresh comb.
    """
    return (1.0 - p["phi_res"]) * (1.0 - math.exp(-p["k_elute"] * p["t_elute"]))


def gold_per_dip(p, area_m2):
    """(3.10) Gold one dip captures, umol. Each dip starts with a fresh comb,
    so a dip takes the comb's whole capacity."""
    return comb_capacity(p, area_m2)


def dips_needed(p, area_m2, Au0, litres=1.0):
    """Dips to capture all the gold in `litres` of leachate at `Au0` uM."""
    return Au0 * litres / gold_per_dip(p, area_m2)


def cycles_per_day(p):
    """At most this many dip-and-release cycles fit in a day. One cycle is the
    dip Q3 sets plus the elution; handling between them is not counted."""
    return HOURS_PER_DAY / (p["t_dip"] + p["t_elute"])


def areal_density(p):
    """(3.8) Dry cells one m^2 of panel carries, g/m^2. One measured number,
    not a layer count."""
    return p["rho_A"]


def area_needed(p, litres=1.0, dips=1, Au0=None):
    """(3.9)/(3.10) Panel area the Q1 cells need, m^2.

    Used once, the comb must carry every gram at once. Dipping it again reuses
    the same panels, so the area divides by the dips.
    """
    Au0 = p["Au_in_author"] if Au0 is None else Au0
    cells = cells_for_sites(p, Au0) * litres        # g, from Q1
    return cells / (areal_density(p) * dips)


def comb_area_each(p):
    """(3.11a) Area of one comb, both faces of each panel, m^2."""
    return p["panels_per_comb"] * 2.0 * p["panel_L"] * p["panel_W"]


def branch_area(p, combs=None):
    """(3.11b) Area of a branch of combs, both faces, m^2."""
    combs = p["combs"] if combs is None else combs
    return combs * comb_area_each(p)


def panel_count(p, combs=None):
    """Panels on the branch."""
    combs = p["combs"] if combs is None else combs
    return combs * p["panels_per_comb"]


def leaf_gap(p, area_m2, litres=None):
    """(3.12) Gap between adjacent leaf faces, m.

    NOT a free choice. The liquid between the leaves is the one-face area
    times the gap, so holding the batch fixes the gap once the area is set.
    """
    litres = p["V_leach"] if litres is None else litres
    return (litres / L_PER_M3) / (area_m2 / 2.0)


def stack_volume(p, area_m2, litres=None):
    """(3.13) Volume the comb and its liquid occupy, L. Sets the vessel."""
    g = leaf_gap(p, area_m2, litres)
    return (area_m2 / 2.0) * (g + p["leaf_t"]) * L_PER_M3


def stack_height(p, combs=None, litres=None):
    """Height of the panels stacked in one column, m."""
    area = branch_area(p, combs)
    return panel_count(p, combs) * (leaf_gap(p, area, litres) + p["leaf_t"])


# --------------------------------------------------------------------
#  Q3. How long one dip must last.
# --------------------------------------------------------------------
def dip_time(p, s0, a0, fraction):
    """(3.14) Time for one dip to consume `fraction` of the scarcer pool, h.

    Gold and sites are consumed one for one and binding is effectively
    irreversible (Q1), so the bound amount x obeys

        dx/dt = k_on (a0 - x) (s0 - x)

    with a0 the gold in the batch and s0 the free sites on the comb, both uM.
    Neither pool is in large excess over the other here -- that is the whole
    point of Q1 -- so the dip time depends on both. `fraction` is measured
    against whichever pool runs out first, since the other cannot be emptied.
    """
    x = fraction * min(a0, s0)
    if abs(a0 - s0) < TIE:                 # equal pools: the general form 0/0
        return x / (p["k_on"] * a0 * (a0 - x))
    return math.log(s0 * (a0 - x) / (a0 * (s0 - x))) / (p["k_on"] * (a0 - s0))


def binding_time(p, cells_g, fraction, Au0, litres=1.0):
    """(3.14) The same time, written against the cells on the comb, h."""
    return dip_time(p, sites(p, cells_g / litres), Au0, fraction)


def dip_schedule(p, area_m2, Au0, litres=1.0):
    """(3.17) Gold left in the batch before each dip, and that dip's time, h.

    Every dip starts with a fresh comb, so every dip offers the comb's whole
    capacity. The batch gets poorer dip by dip, and a poorer batch binds more
    slowly.
    """
    free = gold_per_dip(p, area_m2) / litres
    left, schedule = Au0, []
    while True:
        gold_runs_out = left <= free
        schedule.append((left, dip_time(p, free, left, p["f_dip"])))
        left -= p["f_dip"] * min(free, left)
        if gold_runs_out:
            return schedule


def film_thickness(p):
    """(3.15) Biofilm thickness, m. An assumption, never measured here."""
    return p["t_film"]


def diffusion_time(p, length_m, in_biofilm=False):
    """(3.16) Time for gold to diffuse a distance, h.

    Order of magnitude only: both diffusivities are unsourced estimates. Used
    to see which step controls the dip, never to set the dip time.
    """
    D = p["D_w"] * (p["D_ratio"] if in_biofilm else 1.0)
    return length_m ** 2 / (2.0 * D) / SECONDS_PER_HOUR


# --------------------------------------------------------------------
#  Report. ASCII only: the console here is cp1252.
# --------------------------------------------------------------------
def report(p):
    board = p["m_Au"] / p["M_Au"] * UMOL_PER_MOL
    Xd = design_loading(p)
    Au_rich = p["Au_in_author"]

    print("CONVERSIONS (per litre of leachate)")
    print("  gold on the boards            %8.2f umol/L" % board)
    print("  (3.1) [Au]_in, ammonia        %8.2f uM" % p["Au_in"])
    print("  q_Au (S76)                    %8.2f umol/g" % p["q_Au"])
    one_site = cells_for_sites(p, p["Au_in"])
    print("  (3.2) X for one site per gold %8.2f g/L" % one_site)
    print("  (3.3) comb area at %.2f g/m2 %8.2f m2/L"
          % (p["rho_A"], comb_area(p, one_site)))

    print("\nQ1  Constants (S76, GolB): Kd_Au = %.2e uM, Kd_Cu = %.2e uM"
          % (p["Kd_Au"], p["Kd_Cu"]))
    check_limit(p, min(c[1] for c in cases(p)))
    print("  both are below %.0e of the smallest feed: binding is stoichiometric"
          % LIMIT_RATIO)

    print("\n  Gold captured (%) and copper held on the comb (uM), by cell loading")
    head = "".join("%22s" % ("%s %.1f uM" % (n.split(',')[0][:9], a))
                   for n, a, _ in cases(p))
    print("  %7s%s" % ("X g/L", head))
    for X in p["X_report"]:
        row = ""
        for _, Au0, Cu0 in cases(p):
            f, _s = captured(p, X, Au0, Cu0)
            _, CuB = bound(p, Au0, Cu0, sites(p, X))
            row += "%12.1f %% %6.1f uM" % (100 * f, CuB)
        print("  %7.0f%s" % (X, row))

    print("\n  FLOOR: cells for one site per gold atom, X = [Au]_in / q_Au")
    for name, Au0, _ in cases(p):
        X = cells_for_sites(p, Au0)
        print("  %-26s %6.1f uM -> X = %5.2f g/L, %.3f g cells per umol Au, "
              "comb %5.1f m2/L"
              % (name, Au0, X, X / Au0, comb_area(p, X)))

    print("\n  DESIGN LOADING (3.7): one site per gold atom at the richest feed")
    print("  X_design = %.2f g/L (%.0f uM)" % (Xd, Au_rich))
    print("  %-26s %12s %16s" % ("feed", "captured %", "copper held uM"))
    for name, Au0, Cu0 in cases(p):
        f, _s = captured(p, Xd, Au0, Cu0)
        _, CuB = bound(p, Au0, Cu0, sites(p, Xd))
        print("  %-26s %12.1f %16.2f" % (name, 100 * f, CuB))

    f_rel = release_fraction(p)
    rho_A = areal_density(p)
    X = cells_for_sites(p, Au_rich)

    print("\nQ2  The panel area the Q1 cells need")
    print("  Q1 cells %.2f g/L; one m2 of panel carries %.2f g (to be measured)"
          % (X, rho_A))
    print("  (3.9) area used once = %.2f / %.2f = %.2f m2 per litre"
          % (X, rho_A, area_needed(p)))
    print("  %10s %12s %12s" % ("litres", "cells g", "area m2"))
    for V in (1, 2, 5, 10, 20, 50, 100):
        print("  %10d %12.1f %12.2f" % (V, X * V, area_needed(p, V)))
    print("  (3.10) dipping the same comb divides it:")
    for D in (1, 2, 4, 5):
        print("    %d dip%s -> %5.2f m2 per litre" % (D, " " if D == 1 else "s",
                                                      area_needed(p, 1, D)))

    print("\nQ2 worked: the 1 L comb")
    print("  one comb: %d panels of %.0f x %.0f cm, both faces = %.4f m2"
          % (p["panels_per_comb"], p["panel_L"] * 100, p["panel_W"] * 100,
             comb_area_each(p)))
    print("  %d combs -> %.4f m2, %.2f g cells, %.2f umol per dip (fresh comb)"
          % (p["combs"], branch_area(p), branch_area(p) * rho_A,
             gold_per_dip(p, branch_area(p))))
    print("  one strip of %.0f h releases %.1f %% of it; %.1f cycles fit in a day"
          % (p["t_elute"], 100 * f_rel, cycles_per_day(p)))
    area = branch_area(p)
    for name, Au0, _cu in cases(p):
        print("    %-28s %d dips" % (name, math.ceil(dips_needed(p, area, Au0))))
    print("  gap (3.12) %.2f mm, stack %.1f cm, vessel (3.13) %.2f L"
          % (leaf_gap(p, area) * MM_PER_M, stack_height(p) * 100,
             stack_volume(p, area)))

    print("\nQ3  How long one dip must last")
    cells = branch_area(p) * rho_A
    f_t = p["f_dip"]
    print("  the 1 L comb carries %.2f g of cells = %.1f uM of sites; k_on = %.2f uM-1 h-1"
          % (cells, sites(p, cells), p["k_on"]))
    print("  at the design feed of %.0f uM, how full the dip runs:" % Au_rich)
    print("  %10s %12s" % ("consumed", "minutes"))
    for f in p["f_cap"]:
        print("  %9.1f %% %12.1f"
              % (100 * f, binding_time(p, cells, f, Au_rich) * MIN_PER_HOUR))
    print("  minutes to %.0f %%, by cells on the comb and gold in the batch:" % (100 * f_t))
    print("  %9s %10s%s" % ("cells g", "sites uM",
                            "".join("%16s" % ("%.0f uM" % a) for _n, a, _c in cases(p))))
    for c in p["dip_cells"]:
        row = "".join("%16.1f" % (binding_time(p, c, f_t, a) * MIN_PER_HOUR)
                      for _n, a, _c in cases(p))
        print("  %9.2f %10.1f%s" % (c, sites(p, c), row))
    print("  the scarcer pool is the one that empties: sites below %.2f g of cells"
          % cells_for_sites(p, min(a for _n, a, _c in cases(p))))
    print("  (3.17) the 1 L comb, dip by dip, at the design feed:")
    print("  %6s %12s %12s" % ("dip", "gold left uM", "minutes"))
    sched = dip_schedule(p, area, Au_rich)
    for i, (left, t) in enumerate(sched, 1):
        print("  %6d %12.1f %12.1f" % (i, left, t * MIN_PER_HOUR))
    print("  %6s %12s %12.0f" % ("total", "", sum(t for _l, t in sched) * MIN_PER_HOUR))
    print("  what else takes time (order of magnitude, UNSOURCED diffusivities):")
    print("    into the %.0f um biofilm      %8.1f s"
          % (film_thickness(p) * 1e6,
             diffusion_time(p, film_thickness(p), True) * SECONDS_PER_HOUR))
    half = leaf_gap(p, branch_area(p)) / 2.0
    print("    across half the %.2f mm gap  %8.0f min  (still liquid)"
          % (leaf_gap(p, branch_area(p)) * MM_PER_M,
             diffusion_time(p, half) * MIN_PER_HOUR))

    litres = p["board_kg_day"] * G_PER_KG / p["pulp_g_L"]
    f, _s = captured(p, Xd, p["Au_in"], p["Cu_peak"])
    _, CuB = bound(p, p["Au_in"], p["Cu_peak"], sites(p, Xd))
    gold_in = p["Au_in"] * litres * p["M_Au_g"] / UMOL_PER_MOL
    print("\nSTAGE LEDGER, projected from the 1 L result, %.0f kg board/day"
          % p["board_kg_day"])
    print("  leachate treated       %10.0f L/day" % litres)
    print("  gold in                %10.1f g/day" % gold_in)
    print("  gold captured          %10.1f g/day  (%.1f %%, X = %.2f g/L)"
          % (gold_in * f, 100 * f, Xd))
    print("  gold lost, spent liquor%10.1f g/day" % (gold_in * (1 - f)))
    print("  dry cells to grow      %10.1f kg/day" % (Xd * litres / G_PER_KG))
    print("  copper held with gold  %10.2f uM  (%.1f g/day)"
          % (CuB, CuB * litres * p["M_Cu_g"] / UMOL_PER_MOL))
    print("  panel area at %d dips  %10.0f m2  (%.2f m2 per litre)"
          % (p["dips"], area_needed(p, litres, p["dips"], p["Au_in"]),
             area_needed(p, 1, p["dips"], p["Au_in"])))


if __name__ == "__main__":
    report(inputs())
