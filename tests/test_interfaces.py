"""Joint checks: unit handling and the numbers the two joints produce."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import expression, interfaces, params, recovery_chain  # noqa: E402

P_EXPR = params.values(params.load("expression"))


def test_joint1_accepts_both_names_for_the_same_unit():
    assert interfaces.au_feed_from_leach(12.0, "umol/L") == 12.0
    assert interfaces.au_feed_from_leach(12.0, "uM") == 12.0


def test_joint1_rejects_a_wrong_unit():
    with pytest.raises(interfaces.UnitError):
        interfaces.au_feed_from_leach(12.0, "mol/L")


def test_joint1_feed_warning_thresholds_match_the_document():
    """Part III section 2.1: 22 uM capacity ceiling, 30 uM A_tox cliff."""
    assert interfaces.feed_warning(15.0) is None
    assert "capacity ceiling" in interfaces.feed_warning(25.0)
    assert "above 30 uM" in interfaces.feed_warning(50.0)
    assert "below the recommended" in interfaces.feed_warning(3.0)


def test_joint2_conversion_is_dimensionally_correct():
    """1 mol of sites per gram must give 1e6 uM per (g/L)."""
    sites = interfaces.N_A / interfaces.CELLS_PER_G
    assert interfaces.qmax_from_expression(sites) == pytest.approx(1e6, rel=1e-9)


def test_joint2_is_linear_and_zero_at_zero():
    assert interfaces.qmax_from_expression(0.0) == 0.0
    a = interfaces.qmax_from_expression(1000.0)
    b = interfaces.qmax_from_expression(2000.0)
    assert b == pytest.approx(2 * a)


def test_joint2_disagrees_with_part_III_and_says_so():
    """The two q_max estimates are independent and they disagree by ~255x.

    Part II gives about 0.017 uM/(g/L). Part III uses 4.4 uM/(g/L) and
    flags it as possibly 5-13x optimistic. The gap is far larger than that:
    Part III is about 255x higher, and still about 19x higher than the low
    end of its own 0.33-4.4 sweep.

    This is not a bug to fix in code. It is ISSUES.md item 2, pinned here so
    that a later parameter change cannot quietly hide it. If this test starts
    failing, the disagreement has been resolved and the issue must be closed.
    """
    A = expression.steady_state(P_EXPR)["A"]
    q = interfaces.qmax_from_expression(A)
    report = interfaces.qmax_disagreement(q)
    assert report["ratio_II_over_III"] < 0.01
    assert report["part_III_uM_per_gL"] / q == pytest.approx(255.0, rel=0.05)


def test_time_unit_round_trip():
    assert interfaces.per_minute(interfaces.per_hour(0.1)) == pytest.approx(0.1)


def test_elution_closed_form_ceiling_and_approach():
    """Part III section 3: ceiling (1-phi), 95% of it at 3/k_max."""
    phi, k_max = 0.13, 2.0
    assert recovery_chain.eta_elute(0.0, phi, k_max) == 0.0
    assert recovery_chain.eta_elute(1e6, phi, k_max) == pytest.approx(1 - phi)
    at_3tau = recovery_chain.eta_elute(3.0 / k_max, phi, k_max)
    assert at_3tau == pytest.approx(0.95 * (1 - phi), rel=0.01)


def test_capacity_ceiling_reproduces_the_22uM_transition():
    """Part III section 2.1: the transition is exactly q_max*Xmax = 22 uM."""
    p3 = params.load("recovery_chain")["V1_capture"]
    q_max = p3["q_max"]["value"]
    X_max = p3["Xmax"]["value"]
    assert q_max * X_max == pytest.approx(22.0)
    assert recovery_chain.capacity_ceiling(q_max, X_max, 22.0) == pytest.approx(1.0)


def test_electron_budget_reproduces_section_4_1():
    """Section 4.1: 0.2 g/L protein supplies 98.9% of electrons at 5.78 uM Au(I)."""
    E_tot = 0.2 / 70000.0 * 1e6      # g/L over 70 kDa, expressed in uM
    ceiling = recovery_chain.electron_budget_ceiling(
        E_tot=E_tot, R0=0.0, A0=5.78, n_e_Au=1.0)
    assert ceiling == pytest.approx(0.989, abs=0.01)
