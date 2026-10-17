"""Part II checks. Every target here is a number printed in the source document."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import expression, params  # noqa: E402

P = params.values(params.load("expression"))
REPORTED = params.load("expression")["reported_steady_state"]

#: The source document was written at N = 20, a pBR322-like backbone. The wet
#: lab later confirmed a pUC-type high-copy plasmid and N moved to 300 on
#: 2026-08-19. Reproducing the document therefore needs its copy number back.
#: Every test whose target is a number PRINTED in that document uses this.
P_SOURCE = dict(P, N=params.load("expression")["N"]["superseded"]["value"])


def test_closed_form_matches_reported_steady_state():
    """Draft 4 Table 3: 682 mRNA, 21,818 cytoplasmic, 46,602 surface, 23,301
    active, at the confirmed N = 300.

    All four are quoted from the saturating closed form, so all four must match
    to a rounding place rather than to a few per cent. The earlier draft's
    numbers disagreed with each other by 5.5 %; draft 4's do not disagree with
    anything. ISSUES.md items 3 and 61.
    """
    ss = expression.steady_state(P)
    for key in ("m", "P_c", "P_s", "A"):
        assert ss[key] == pytest.approx(REPORTED[key], rel=1e-3), key


def test_the_earlier_drafts_reported_numbers_were_internally_inconsistent():
    """The EARLIER draft's two surface numbers did not satisfy A = f*P_s.

    It reported P_s = 5,500 and A = 2,900, while describing the active sites as
    half the surface pool. Half of 5,500 is 2,750, not 2,900. The reported P_s
    matched the ODE (5,498) and the reported A matched the non-saturating
    closed form (2,909), so the two numbers came from different calculations.
    That is ISSUES.md item 3, closed by draft 4 on 2026-08-19.

    The retired numbers are kept in the YAML and checked here, so the reason
    item 3 was raised stays checkable after the item was closed. Draft 4's own
    numbers, asserted below, are consistent.
    """
    old = params.load("expression")["reported_steady_state"][
        "superseded_2026_08_19"]
    assert P["f"] * old["P_s"] == 2750.0
    assert old["A"] != P["f"] * old["P_s"]

    # Draft 4 does satisfy it, which is the whole point of the correction.
    assert P["f"] * REPORTED["P_s"] == pytest.approx(REPORTED["A"], rel=1e-3)

    # And the retired closed form is what produced the retired A.
    lin = expression.steady_state_linear(P_SOURCE)
    assert lin["A"] == pytest.approx(old["A"], rel=0.01)
    assert lin["P_s"] == pytest.approx(5818.2, rel=1e-3)
    assert expression.steady_state(P_SOURCE)["P_s"] == pytest.approx(
        old["P_s"], rel=0.01)


def test_ode_converges_to_the_saturating_closed_form_exactly():
    """This is what closes ISSUES.md item 3.

    The repository carried only the non-saturating closed form until
    2026-08-19, so it disagreed with its own ODE by 5.5 % at N = 20 and by
    87 % at N = 300. There was never an inconsistency in the model -- the two
    were different calculations, and the document quoted one number from each.

    The saturating form is exact, at both copy numbers, to 1e-12.
    """
    for q, label in ((P_SOURCE, "N=20, the document"), (P, "N=300, current")):
        _, m, Pc, Ps, A = expression.simulate(q, t_end=6000.0, n=6001)
        ss = expression.steady_state(q)
        assert m[-1] == pytest.approx(ss["m"], rel=1e-6), label
        assert Pc[-1] == pytest.approx(ss["P_c"], rel=1e-6), label
        assert Ps[-1] == pytest.approx(ss["P_s"], rel=1e-6), label
        assert A[-1] == pytest.approx(ss["A"], rel=1e-6), label

        # and the linear form is the one that misses
        lin = expression.steady_state_linear(q)
        assert lin["P_s"] > ss["P_s"]

    assert (expression.steady_state_linear(P)["P_s"]
            / expression.steady_state(P)["P_s"]) == pytest.approx(1.87, rel=0.01)


def test_the_membrane_is_now_co_limiting_not_comfortably_empty():
    """Section 8's premise no longer holds, and that is the design result.

    The document argued the capacity bracket was negligible because site
    density stayed far below 1e5. At N = 20 that was true, 5.5 % occupancy.
    At the confirmed pUC-type backbone the surface is 46.6 % full, and the
    limiting resource has moved from the gene to the membrane.
    """
    assert expression.steady_state(P_SOURCE)["P_s"] < 0.10 * P["P_s_max"]

    ss = expression.steady_state(P)
    occupancy = ss["P_s"] / P["P_s_max"]
    assert 0.40 < occupancy < 0.55
    assert ss["P_s"] == pytest.approx(46602, rel=1e-3)
    assert ss["A"] == pytest.approx(23301, rel=1e-3)

    # No copy number can pass f*P_s_max, so the ceiling is a real one.
    assert expression.steady_state(dict(P, N=1e9))["A"] < P["f"] * P["P_s_max"]
    assert expression.steady_state(dict(P, N=1e9))["A"] == pytest.approx(
        P["f"] * P["P_s_max"], rel=1e-3)


def test_surface_pool_exceeds_cytoplasmic_pool():
    """Panel (b): export drains the cytoplasm, so displayed protein accumulates."""
    ss = expression.steady_state(P)
    assert ss["P_s"] > ss["P_c"]


def test_mrna_equilibrates_faster_than_protein():
    """Panel (a): mRNA in minutes, protein in an hour or two.

    Crowding SPEEDS the approach while lowering the destination -- it adds an
    extra first-order escape route -- so the surface fills faster at N = 300
    than at N = 20 even though it fills to a lower fraction of capacity.
    """
    t, m, _, _, A = expression.simulate(P, t_end=600.0, n=6001)

    def t95(y):
        return t[np.argmax(y >= 0.95 * y[-1])]

    assert t95(m) < 30.0
    assert 60.0 < t95(A) < 120.0

    _, _, _, _, A20 = expression.simulate(P_SOURCE, t_end=600.0, n=6001)
    assert t95(A20) > t95(A)          # slower at low copy number

    # An eight-hour batch is at steady state with hours to spare, so batch
    # length is set by binding and handling, not by expression.
    assert t95(A) < 8 * 60


def test_the_sensitivity_ranking_changed_when_the_membrane_filled():
    """Panel (d), and the ranking is the design message.

    At N = 20 on the linear form, alpha, N, beta and f were all +1.00 and the
    anchor capacity did not appear at all. At the confirmed N = 300 on the
    saturating form, the expression handles halve to +0.53 and P_s,max arrives
    at +0.47. Only f keeps its full +1.00, because it multiplies P_s AFTER all
    the saturation has happened.

    So the productive directions are now the folding fraction and the display
    scaffold, not the promoter, the copy number or the RBS.
    """
    EXPECTED = {"f": 1.00, "alpha": 0.53, "N": 0.53, "beta": 0.53,
                "P_s_max": 0.47, "k_sec": 0.11,
                "delta_c": -0.02, "delta_s": -0.11,
                "delta_m": -0.49, "mu": -0.56}
    for symbol, want in EXPECTED.items():
        got = expression.normalised_sensitivity(P, symbol)
        assert got == pytest.approx(want, abs=0.02), symbol

    # f alone survives the move, and it is still first.
    assert max(EXPECTED, key=EXPECTED.get) == "f"
    assert expression.normalised_sensitivity(P, "f") == pytest.approx(1.0, abs=0.01)

    # At the document's copy number the old ranking is recovered exactly,
    # so neither version is wrong -- they describe different backbones.
    for symbol in ("alpha", "N", "beta", "f"):
        got = ((expression.steady_state_linear(dict(P_SOURCE, **{symbol: P_SOURCE[symbol] * 1.000001}))["A"]
                / expression.steady_state_linear(P_SOURCE)["A"]) - 1) / 1e-6
        assert got == pytest.approx(1.0, abs=0.01), symbol


def test_langmuir_plateau_equals_site_count():
    """Section 6: each site binds one ion, so the plateau is the site count."""
    A = expression.steady_state(P)["A"]
    K_Au = params.load("expression")["K_Au"]["value"]
    assert expression.langmuir_uptake(0.0, A, K_Au) == 0.0
    assert expression.langmuir_uptake(K_Au, A, K_Au) == pytest.approx(A / 2.0)
    assert expression.langmuir_uptake(1e6, A, K_Au) == pytest.approx(A, rel=1e-4)




def test_the_growth_rate_trap():
    """mu is the largest negative per cell and slowing growth is still wrong.

    The sensitivity table invites the conclusion that mild stress -- cooler,
    leaner, off-pH -- raises capture, because mu appears only as a loss. Per
    litre it does the opposite. Site density is weakly hyperbolic in mu;
    biomass is exponential in it.

    Slowing growth four-fold raises per-cell density 1.6x and cuts capture per
    litre about a thousand-fold. This caveat must travel with panel (d)
    wherever it is reproduced.
    """
    slow = expression.volumetric_capture(P, 8.0, mu=0.005)
    base = expression.volumetric_capture(P, 8.0, mu=0.020)
    fast = expression.volumetric_capture(P, 8.0, mu=0.030)

    # per cell, slow wins -- and only by 1.6x
    assert slow[0] > base[0] > fast[0]
    assert slow[0] / base[0] == pytest.approx(1.56, rel=0.02)

    # per litre, it loses by three orders of magnitude
    assert slow[2] / base[2] == pytest.approx(0.0012, rel=0.05)
    assert fast[2] / base[2] == pytest.approx(93.0, rel=0.05)

    # mu is still the largest negative per-cell sensitivity, which is the
    # whole reason this test exists next to it.
    negatives = {s: expression.normalised_sensitivity(P, s)
                 for s in ("mu", "delta_m", "delta_c", "delta_s")}
    assert min(negatives, key=negatives.get) == "mu"


def test_saturation_compresses_the_copy_number_uncertainty():
    """N is quoted anywhere from 75 to 700, and it matters less than that.

    NEB's pUC19 datasheet gives about 75; 300-700 and 500-700 are both widely
    quoted elsewhere. A 9.3x spread in the input becomes 3.7x in the answer,
    because the membrane absorbs the difference. That is the one comfort the
    high-copy regime offers.
    """
    A = {N: expression.steady_state(dict(P, N=N))["A"] for N in (75, 300, 700)}
    assert A[75] == pytest.approx(8955, rel=1e-3)
    assert A[300] == pytest.approx(23301, rel=1e-3)
    assert A[700] == pytest.approx(33533, rel=1e-3)
    assert A[700] / A[75] == pytest.approx(3.74, rel=0.02)
    assert (700 / 75) / (A[700] / A[75]) > 2.4      # the compression factor
