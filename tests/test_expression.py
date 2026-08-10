"""Part II checks. Every target here is a number printed in the source document."""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import expression, params  # noqa: E402

P = params.values(params.load("expression"))
REPORTED = params.load("expression")["reported_steady_state"]


def test_closed_form_matches_reported_steady_state():
    """Section 5: roughly 45 mRNA, 1,460 cytoplasmic, 5,500 surface, 2,900 active.

    The mRNA and cytoplasmic pools match to better than 1%. The surface pool
    does not: the closed form gives 5,818 against a reported 5,500, because
    the closed form drops the saturation factor. See ISSUES.md item 3.
    """
    ss = expression.steady_state(P)
    assert ss["m"] == pytest.approx(REPORTED["m"], rel=0.02)
    assert ss["P_c"] == pytest.approx(REPORTED["P_c"], rel=0.02)
    assert ss["P_s"] == pytest.approx(REPORTED["P_s"], rel=0.06)
    assert ss["A"] == pytest.approx(REPORTED["A"], rel=0.02)


def test_reported_numbers_are_internally_inconsistent():
    """The document's own two surface numbers do not satisfy A = f*P_s.

    Section 5 reports P_s = 5,500 and A = 2,900, and section 7 panel (b)
    describes the active sites as "being half the surface pool". Half of
    5,500 is 2,750, not 2,900. The reported P_s matches the ODE (5,498) and
    the reported A matches the closed form (2,909), so the two numbers were
    taken from different calculations. Pinned here so it is not lost.
    See ISSUES.md item 3.
    """
    implied = P["f"] * REPORTED["P_s"]
    assert implied == 2750.0
    assert REPORTED["A"] != implied


def test_ode_converges_to_closed_form():
    """The non-saturating closed form must agree with the saturating ODE here.

    Section 8 argues this holds because site density stays far below the 1e5
    capacity. It holds to about 6%, not exactly: the saturation factor
    (1 - P_s/P_s_max) costs 5.5% of the surface pool at steady state.
    """
    _, m, Pc, Ps, A = expression.simulate(P, t_end=3000.0, n=3001)
    ss = expression.steady_state(P)
    assert m[-1] == pytest.approx(ss["m"], rel=1e-4)
    assert Pc[-1] == pytest.approx(ss["P_c"], rel=1e-4)
    assert Ps[-1] == pytest.approx(ss["P_s"], rel=0.06)
    assert A[-1] == pytest.approx(ss["A"], rel=0.06)
    assert Ps[-1] < ss["P_s"]   # saturation can only reduce it


def test_surface_pool_stays_below_capacity():
    """Section 8: thousands of sites against a ceiling of 1e5."""
    ss = expression.steady_state(P)
    assert ss["P_s"] < 0.2 * P["P_s_max"]


def test_surface_pool_exceeds_cytoplasmic_pool():
    """Panel (b): export drains the cytoplasm, so displayed protein accumulates."""
    ss = expression.steady_state(P)
    assert ss["P_s"] > ss["P_c"]


def test_mrna_equilibrates_faster_than_protein():
    """Panel (a) 20-30 min for mRNA; panel (b) 150-200 min for protein."""
    t, m, _, _, A = expression.simulate(P, t_end=600.0, n=6001)

    def t90(y):
        return t[np.argmax(y >= 0.9 * y[-1])]

    assert t90(m) < 30.0
    assert 100.0 < t90(A) < 250.0


def test_sensitivities_match_panel_d():
    """Panel (d): alpha, N, beta, f near +1; k_sec near +0.2; mu most negative."""
    for symbol in ("alpha", "N", "beta", "f"):
        assert expression.normalised_sensitivity(P, symbol) == pytest.approx(1.0, abs=0.01)
    assert expression.normalised_sensitivity(P, "k_sec") == pytest.approx(0.2, abs=0.1)

    negatives = {s: expression.normalised_sensitivity(P, s)
                 for s in ("mu", "delta_m", "delta_c", "delta_s")}
    assert all(v < 0 for v in negatives.values())
    assert min(negatives, key=negatives.get) == "mu"


def test_langmuir_plateau_equals_site_count():
    """Section 6: each site binds one ion, so the plateau is the site count."""
    A = expression.steady_state(P)["A"]
    K_d = params.load("expression")["K_d"]["value"]
    assert expression.langmuir_uptake(0.0, A, K_d) == 0.0
    assert expression.langmuir_uptake(K_d, A, K_d) == pytest.approx(A / 2.0)
    assert expression.langmuir_uptake(1e6, A, K_d) == pytest.approx(A, rel=1e-4)
