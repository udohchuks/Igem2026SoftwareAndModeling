"""Stage 3 design analysis: the numbers docs/CAPTURE_DESIGN.md quotes.

The write-up states results computed by docs/capture_design_analysis.py. These
tests recompute them and check the write-up still says the same thing, so a
changed parameter cannot leave the document quoting a stale number
(AGENTS.md section 11: a stale number is a defect).

The model uses GolB's own measured constants (S76) directly. They are so far
below every feed that binding is stoichiometric, so the tests also guard that
limit.
"""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "docs"))
import capture_design_analysis as cda  # noqa: E402

MD = (ROOT / "docs" / "CAPTURE_DESIGN.md").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def p():
    return cda.inputs()


def test_constants_are_the_S76_measurements(p):
    """Kd in uM: 3.02e-37 M and 1.61e-17 M, read straight from the params."""
    assert p["Kd_Au"] == pytest.approx(3.02e-31)
    assert p["Kd_Cu"] == pytest.approx(1.61e-11)
    assert p["Kd_Cu"] / p["Kd_Au"] == pytest.approx(5.3e19, rel=0.01)


def test_stoichiometric_limit_is_valid_for_every_feed(p):
    """(3.6) holds only while both constants are far below the gold feed."""
    for _, Au0, _ in cda.cases(p):
        cda.check_limit(p, Au0)          # raises if it ever stops being true
        assert max(p["Kd_Au"], p["Kd_Cu"]) < 1e-6 * Au0


def test_the_limit_guard_fires_when_binding_is_not_stoichiometric(p):
    weak = dict(p, Kd_Au=0.7, Kd_Cu=36.4)       # the old apparent constants
    with pytest.raises(ValueError):
        cda.check_limit(weak, p["Au_in_author"])


def test_floor_is_one_site_per_gold_atom(p):
    for _, Au0, Cu0 in cda.cases(p):
        X = cda.cells_for_sites(p, Au0)
        AuB, CuB = cda.bound(p, Au0, Cu0, cda.sites(p, X))
        assert AuB == pytest.approx(Au0)
        assert CuB == pytest.approx(0.0, abs=1e-9)
        assert X / Au0 == pytest.approx(0.216, abs=0.001)   # g per umol gold


def test_capture_is_linear_below_the_floor_and_flat_above(p):
    Au0, Cu0 = p["Au_in_author"], p["Cu_band"][-1]
    Xf = cda.cells_for_sites(p, Au0)
    f_half = cda.captured(p, 0.5 * Xf, Au0, Cu0)[0]
    assert f_half == pytest.approx(0.5)
    assert cda.captured(p, 2.0 * Xf, Au0, Cu0)[0] == pytest.approx(1.0)


def test_copper_never_reduces_gold_capture(p):
    """Gold takes its sites first, so no amount of copper changes it."""
    Au0 = p["Au_in_author"]
    for X in (2.0, 5.0, 9.0, 20.0):
        none = cda.captured(p, X, Au0, 0.0)[0]
        lots = cda.captured(p, X, Au0, 1.0e6)[0]
        assert lots == pytest.approx(none)


def test_every_gram_above_the_floor_captures_copper(p):
    Au0, Cu0 = p["Au_in_author"], p["Cu_band"][-1]
    Xf = cda.cells_for_sites(p, Au0)
    _, CuB = cda.bound(p, Au0, Cu0, cda.sites(p, Xf + 1.0))
    assert CuB == pytest.approx(p["q_Au"])               # 4.62 uM per g/L
    _, CuB12 = cda.bound(p, Au0, Cu0, cda.sites(p, 12.0))
    assert CuB12 == pytest.approx(11.44, abs=0.01)


def test_design_loading_serves_every_feed(p):
    Xd = cda.design_loading(p)
    assert Xd == pytest.approx(9.52, abs=0.01)
    for name, Au0, Cu0 in cda.cases(p):
        assert cda.captured(p, Xd, Au0, Cu0)[0] == pytest.approx(1.0), name


def test_areal_density_is_one_measurable_number(p):
    """(3.8) rho_A is weighed, not calculated from a layer count. The layer
    model was retired 2026-10-17; its record stays in a superseded block."""
    from src import params
    assert cda.areal_density(p) == pytest.approx(6.36, abs=0.01)
    design = params.load("capture_design")["stage3_design"]
    assert design["design_layers"]["value"] is None
    assert design["design_layers"]["superseded"]["value"] == 30
    assert design["layer_cases"]["value"] is None


def test_area_needed_is_a_straight_proportion(p):
    """(3.9) Q1's cells divided by what a square metre carries."""
    one = cda.area_needed(p, 1)
    assert one == pytest.approx(1.50, abs=0.01)
    for V in (2, 5, 10, 100):
        assert cda.area_needed(p, V) == pytest.approx(V * one)


def test_dips_divide_the_area(p):
    """(3.10) Reusing the comb divides the area it must carry."""
    one = cda.area_needed(p, 1, 1)
    assert cda.area_needed(p, 1, 4) == pytest.approx(one / 4)
    assert cda.area_needed(p, 1, 4) == pytest.approx(0.374, abs=0.002)


def test_the_1L_comb_delivers_the_area(p):
    """The worked example must cover the three-dip area for the design feed."""
    need = cda.area_needed(p, 1, p["dips"], p["Au_in"])
    branch = cda.branch_area(p)
    assert branch > need, "30 combs must cover the design feed in 3 dips"
    assert branch == pytest.approx(0.60, abs=0.001)


def test_comb_capacity_is_area_times_density_times_loading(p):
    """(3.8) C = A x rho_A x q_Au."""
    C = cda.comb_capacity(p, 0.5)
    assert C == pytest.approx(0.5 * 30 * 0.2119 * 4.62, rel=2e-3)
    assert C == pytest.approx(14.69, abs=0.02)


def test_elution_releases_71_percent_in_6_hours(p):
    """(3.9) from the S60 transferred parameters in recovery_chain.yaml."""
    assert p["t_elute"] == 6.0
    assert cda.release_fraction(p) == pytest.approx(0.711, abs=0.001)
    assert cda.cycles_per_day(p) == pytest.approx(24.0 / 6.5)


def test_dips_halve_when_the_area_doubles(p):
    base = cda.dips_needed(p, 0.5, p["Au_in_author"])
    assert base == pytest.approx(3.0, abs=0.05)
    assert cda.dips_needed(p, 1.0, p["Au_in_author"]) == pytest.approx(base / 2)


def test_each_dip_takes_the_whole_comb(p):
    """A dip starts with a fresh comb, so the elution share does not reduce
    it. gold_per_dip is the capacity, not 71.1 % of it."""
    assert cda.gold_per_dip(p, 0.5) == pytest.approx(cda.comb_capacity(p, 0.5))
    assert cda.release_fraction(p) == pytest.approx(0.711, abs=0.001)


def test_gap_is_fixed_by_area_and_volume(p):
    """(3.12) The gap is not a free choice: liquid = one-face area x gap."""
    g = cda.leaf_gap(p, 0.5)
    assert g * cda.MM_PER_M == pytest.approx(4.0)
    # the liquid it holds is the batch
    assert (0.5 / 2) * g * cda.L_PER_M3 == pytest.approx(p["V_leach"])
    # double the area, halve the gap
    assert cda.leaf_gap(p, 1.0) == pytest.approx(g / 2)
    # halve the leachate, halve the gap
    assert cda.leaf_gap(p, 0.5, 0.5) == pytest.approx(g / 2)


def test_vessel_volume_holds_liquid_and_leaves(p):
    """(3.13) The vessel is the liquid plus the leaves themselves."""
    V = cda.stack_volume(p, 0.5)
    assert V == pytest.approx(1.25, abs=0.005)
    assert V > p["V_leach"]


def test_a_bigger_comb_in_the_same_litre_closes_the_gap(p):
    """A bigger comb in the same litre closes the gap in direct proportion.
    The biofilm is not what fails there: two facing 30 um films fill 6 % of a
    1 mm gap and only touch near 0.06 mm. Flow fails first; that is Q3."""
    assert cda.leaf_gap(p, 2.0) * cda.MM_PER_M == pytest.approx(1.0)
    film_um = cda.film_thickness(p) * 1e6
    gap_um = cda.leaf_gap(p, 2.0) * 1e6
    assert 2 * film_um / gap_um == pytest.approx(0.06, abs=0.001)


def test_dip_time_reduces_to_first_order_when_one_pool_dominates(p):
    """(3.14a) With gold far in excess the sites fill first order at k_on*a0,
    and with sites far in excess the gold falls first order at k_on*s0."""
    import math
    f = 0.9
    first_order = math.log(1.0 / (1.0 - f))
    t = cda.dip_time(p, 1.0e-4, 1.0e4, f)        # gold swamps the sites
    assert t == pytest.approx(first_order / (p["k_on"] * 1.0e4), rel=1e-3)
    t = cda.dip_time(p, 1.0e4, 1.0e-4, f)        # sites swamp the gold
    assert t == pytest.approx(first_order / (p["k_on"] * 1.0e4), rel=1e-3)


def test_dip_time_is_symmetric_in_the_two_pools(p):
    """Gold and sites are consumed one for one, so swapping them cannot
    change the time."""
    assert cda.dip_time(p, 14.1, 44.0, 0.99) == pytest.approx(
        cda.dip_time(p, 44.0, 14.1, 0.99))


def test_dip_time_peaks_where_the_pools_match(p):
    """The design result of Q3: a comb sized to the gold exactly is the
    slowest comb there is."""
    tie = cda.dip_time(p, 44.0, 44.0, 0.99)
    assert tie * cda.MIN_PER_HOUR == pytest.approx(135.0, abs=1.0)
    assert tie > cda.dip_time(p, 14.1, 44.0, 0.99)
    assert tie > cda.dip_time(p, 88.0, 44.0, 0.99)


def test_dip_time_for_the_1L_comb(p):
    cells = cda.branch_area(p) * cda.areal_density(p)
    assert cells == pytest.approx(3.82, abs=0.01)
    mins = cda.binding_time(p, cells, 0.99, p["Au_in_author"]) * cda.MIN_PER_HOUR
    assert mins == pytest.approx(9.3, abs=0.1)
    assert cda.binding_time(p, cells, 0.999, p["Au_in_author"]) \
        * cda.MIN_PER_HOUR == pytest.approx(14.6, abs=0.1)


def test_a_leaner_batch_binds_more_slowly(p):
    """(3.17) Why the later dips are the slow ones."""
    cells = cda.branch_area(p) * cda.areal_density(p)
    rich = cda.binding_time(p, cells, 0.99, p["Au_in_author"])
    lean = cda.binding_time(p, cells, 0.99, p["Au_in_noNH3"])
    assert lean > rich


def test_dip_schedule_clears_the_batch(p):
    """(3.17) Three dips at the design feed, and the last is the slowest."""
    area = cda.branch_area(p)
    sched = cda.dip_schedule(p, area, p["Au_in_author"])
    assert len(sched) == 3
    assert sched[0][0] == pytest.approx(p["Au_in_author"])
    assert [round(t * cda.MIN_PER_HOUR, 1) for _l, t in sched] == [
        9.3, 23.8, 27.3]
    assert max(t for _l, t in sched) * cda.MIN_PER_HOUR < p["t_dip"] \
        * cda.MIN_PER_HOUR, "the chosen dip time must cover the slowest dip"


def test_dip_time_does_not_change_with_batch_volume(p):
    """Intensive: twice the litres with twice the comb is the same clock."""
    cells = cda.branch_area(p) * cda.areal_density(p)
    assert cda.binding_time(p, 2 * cells, 0.99, p["Au_in_author"], litres=2.0) \
        == pytest.approx(cda.binding_time(p, cells, 0.99, p["Au_in_author"]))


def test_biofilm_diffusion_is_not_the_limit(p):
    """Gold crosses a 30 um film in seconds; the still liquid takes an hour."""
    cells = cda.branch_area(p) * cda.areal_density(p)
    t_bind = cda.binding_time(p, cells, 0.99, p["Au_in_author"])
    t_film = cda.diffusion_time(p, cda.film_thickness(p), True)
    half_gap = cda.leaf_gap(p, cda.branch_area(p)) / 2
    t_liquid = cda.diffusion_time(p, half_gap)
    assert cda.film_thickness(p) == pytest.approx(30e-6)
    assert t_film * cda.SECONDS_PER_HOUR < 5, "biofilm is never the limit"
    assert t_liquid > t_bind, "a still vessel is slower than binding: stir it"


def test_dip_is_short_against_the_strip(p):
    assert p["t_dip"] < p["t_elute"]


def test_dip_time_is_a_design_choice_set_by_Q3():
    """It was null until 2026-10-17. Q3 sets it, so it is a design choice and
    says so: it is still not a measurement."""
    from src import params
    entry = params.load("capture_design")["stage3_design"]["dip_time_h"]
    assert entry["value"] == 0.5
    assert entry["status"] == "design_choice_set_by_Q3"


def test_ledger_projection(p):
    litres = p["board_kg_day"] * cda.G_PER_KG / p["pulp_g_L"]
    assert litres == pytest.approx(10000.0)
    Xd = cda.design_loading(p)
    gold_in = p["Au_in"] * litres * p["M_Au_g"] / cda.UMOL_PER_MOL
    assert gold_in == pytest.approx(73.2, abs=0.05)
    assert Xd * litres / cda.G_PER_KG == pytest.approx(95.2, abs=0.05)
    _, CuB = cda.bound(p, p["Au_in"], p["Cu_peak"], cda.sites(p, Xd))
    assert CuB * litres * p["M_Cu_g"] / cda.UMOL_PER_MOL == pytest.approx(
        4.3, abs=0.05)
    # the panel area the plant needs at the design dip count
    assert cda.area_needed(p, litres, p["dips"], p["Au_in"]) == pytest.approx(
        4216.0, abs=1.0)


def test_retired_selectivity_entries_are_superseded_not_deleted():
    """ISSUES 93: the thiosulfate-corrected band was retired 2026-10-17, and
    its record stays in a superseded block."""
    from src import params
    cap = params.load("capture_design")
    for entry in (cap["stage3_design"]["selectivity_band"],
                  cap["stage3_design"]["selectivity_design"],
                  cap["binding_proxies"]["conditional_selectivity_band"]):
        assert entry["value"] is None
        assert "ISSUES 93" in entry["superseded"]["reason"]
    assert cap["stage3_design"]["selectivity_band"]["superseded"]["value"] \
        == [5300.0, 5.3e8]
    assert cap["binding_proxies"]["checa2007_gols_selectivity_alpha"][
        "superseded"]["value"] == 52.0


@pytest.mark.parametrize("quote", [
    "9.52", "0.216", "4.33", "8.04", "11.4", "6.8 µM", "71.1 %", "6.36",
    "1.50 m²", "14.97 m²", "0.50 m²", "0.0200 m²", "0.600 m²", "3.82 g",
    "17.6 µmol", "3.33 mm", "26.0 cm", "1.30 L", "73.2 g/day", "95.2 kg/day",
    "4.3 g/day", "4 216 m²", "9.3", "14.6", "39 min", "1.5 s",
    "17.6 µM", "27.3 min", "132.4", "60 min", "30 minutes", "0.588 µmol",
])
def test_writeup_quotes_the_computed_numbers(quote):
    assert quote in MD, f"CAPTURE_DESIGN.md no longer quotes {quote!r}"


def test_writeup_has_no_stale_references():
    """t_leaf is NOT stale: it is the leaf thickness in (3.13). It was removed
    with the old leaf-spacing model and reintroduced with the comb geometry."""
    for stale in ("matlab/capture_design.m", "working selectivity",
                  "Do we remove copper first", "alpha", "5.3 × 10³",
                  "5.3 × 10⁸", "K_Cu", "a_comb"):
        assert stale not in MD, f"stale text in CAPTURE_DESIGN.md: {stale!r}"
