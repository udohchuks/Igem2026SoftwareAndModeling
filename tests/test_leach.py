"""Part I checks: conservation, geometry, and limit behaviour.

Part I ships no numeric results, so there is nothing to reproduce. What can
be checked is that the equations conserve what they must and reduce to the
right limits. Rate constants marked 'calibrate' are given placeholder values
here that exist only inside this test file.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import leach  # noqa: E402


M_AU = 197e-3      # kg/mol
M_CU = 63.55e-3    # kg/mol


def make_params(**over):
    """Test-only parameter set. Calibration targets get arbitrary values.

    Solid inventories are carried in umol, not mol. The section 4 table gives
    n_Au as "mol (or umol)" while R_Au is in umol/min, so the two must be
    reconciled by the user of the model; umol is the consistent choice.
    See ISSUES.md item 4.
    """
    p = dict(
        # enzyme
        k_syn=1e-12, X=1e12, k_deg=1.1e-3, mu=0.0,
        # tetrathionate
        F_in=0.0, k_cat=10.0, K_m=500.0, k1=1e-5,
        # reactor
        V=1.0, O2=250.0,
        # gold
        m_Au=1e-4, rho_Au=19300.0, t_film=1e-6,
        k_Au_O2=11.0, k_Au_Cu=11.0e3, K_O2=50.0, K_S=5.0e4, K_Cu=100.0,
        # copper
        m_Cu=1e-2, rho_Cu=8960.0, d=4e-3,
        k_Cu_O2=1.0, k_Cu_Cu=1.0, k3=1e-5, k4=1e-6,
    )
    p.update(over)
    p["A_Cu0"] = leach.copper_area_initial(p["m_Cu"], p["rho_Cu"], p["d"])
    p["n_Cu0"] = p["m_Cu"] / M_CU * 1e6      # umol
    return p


def initial_state(p, S2O3=1e5, S4O6=1e4):
    """Returns (y0, n_Au0) with all solid inventories in umol."""
    n_Au0 = p["m_Au"] / M_AU * 1e6           # umol
    return [0.0, S4O6, S2O3, n_Au0, 0.0, p["n_Cu0"], 0.0, 0.0], n_Au0


def test_gold_area_formula():
    """A_Au = m/(rho*t). A film of area A and thickness t has volume m/rho."""
    A = leach.gold_area(m_Au=1e-4, rho_Au=19300.0, t_film=1e-6)
    assert A == pytest.approx(1e-4 / (19300.0 * 1e-6))


def test_copper_area_two_thirds_power():
    """A_Cu(t) = A_Cu(0)*(n/n0)^(2/3): area goes as r^2, volume as r^3."""
    assert leach.copper_area(100.0, 1.0, 1.0) == pytest.approx(100.0)
    assert leach.copper_area(100.0, 0.125, 1.0) == pytest.approx(25.0)
    assert leach.copper_area(100.0, 0.0, 1.0) == 0.0


def test_gold_mass_balance():
    """Solid gold lost must equal dissolved complex gained.

    Both sides are in umol: n_Au is umol and Au_complex*V is umol/L times L.
    """
    p = make_params()
    y0, n_Au0 = initial_state(p)
    _, traj = leach.simulate(p, y0, t_end=200.0, model="B")
    lost = n_Au0 - traj["n_Au"]
    gained = traj["Au_complex"] * p["V"]
    assert np.allclose(lost, gained, rtol=1e-6, atol=1e-9)
    assert lost[-1] > 0.0        # something actually happened


def test_no_thiosulfate_means_no_gold_leaching():
    """Both models multiply through by the thiosulfate saturation factor.

    Tetrathionate must also be absent, otherwise hydrolysis regenerates
    thiosulfate within the run and gold starts to leach.
    """
    p = make_params(F_in=0.0)
    y0, n_Au0 = initial_state(p, S2O3=0.0, S4O6=0.0)
    for model in ("A", "B"):
        _, traj = leach.simulate(p, y0, t_end=50.0, model=model)
        assert traj["n_Au"][-1] == pytest.approx(n_Au0, rel=1e-12)


def test_model_B_leaches_faster_than_model_A_when_cu_II_is_present():
    """Cu(II) is a parallel oxidant pathway, so Model B adds a positive term.

    Cu(II) must be present at the start. From a copper-free start the Cu(II)
    pool has no production route and the two models coincide. See ISSUES.md
    item 5.
    """
    p = make_params()
    y0, n_Au0 = initial_state(p)
    y0[7] = 500.0                       # Cu(II), umol/L
    _, a = leach.simulate(p, y0, t_end=200.0, model="A")
    _, b = leach.simulate(p, y0, t_end=200.0, model="B")
    assert b["n_Au"][-1] < a["n_Au"][-1]

    # The Cu(II) rate constant is about 1e3 times the O2 one, but the run
    # does not show a 1e3 speed-up: the Cu(II) pool is consumed as it works,
    # and it has no production route from a copper-free solution.
    assert (n_Au0 - b["n_Au"][-1]) > 5.0 * (n_Au0 - a["n_Au"][-1])


def test_enzyme_reaches_analytic_steady_state():
    """[E]_ss = k_syn*X/(k_deg + mu), from section 1.

    Leaching is switched off so this isolates the enzyme pool. With leaching
    active the long horizon runs into gold exhaustion, which section 4 makes
    a step discontinuity.
    """
    p = make_params(k_Au_O2=0.0, k_Au_Cu=0.0, k_Cu_O2=0.0, k_Cu_Cu=0.0)
    y0, _ = initial_state(p)
    _, traj = leach.simulate(p, y0, t_end=9000.0, n=2001)
    expected = p["k_syn"] * p["X"] / (p["k_deg"] + p["mu"])
    assert traj["E"][-1] == pytest.approx(expected, rel=1e-3)


def test_cu_II_goes_negative_from_a_copper_free_start():
    """Cu(II) has no production term other than O2 re-oxidation of Cu(I).

    Section 5 states Cu(II) is "produced only by oxygen re-oxidation of
    Cu(I)". Starting from zero dissolved copper, v4 is zero, so the only
    non-zero terms are losses and the pool goes negative. That in turn drives
    tetrathionate negative through the k1 regeneration term.

    This test asserts the behaviour of the equations as written. It is a
    structural issue in Part I, recorded as ISSUES.md item 5, not a coding
    error. If Part I is later amended, this test should fail and be removed.
    """
    p = make_params()
    y0, _ = initial_state(p)
    _, traj = leach.simulate(p, y0, t_end=200.0, model="B")
    assert traj["Cu_II"].min() < 0.0
    assert traj["S4O6"].min() < 0.0


def test_zero_enzyme_means_no_tetrathionate_hydrolysis():
    """With k_cat = 0 and no feed, tetrathionate can only grow via Cu(II)."""
    p = make_params(k_cat=0.0, F_in=0.0, k1=0.0)
    y0, _ = initial_state(p)
    _, traj = leach.simulate(p, y0, t_end=100.0)
    assert traj["S4O6"][-1] == pytest.approx(traj["S4O6"][0], rel=1e-9)


def test_copper_redox_pair_is_closed_without_leaching():
    """With no metal left, Cu(I)+Cu(II) changes only through v3 and v4.

    v3 converts 2 Cu(II) -> 2 Cu(I) and v4 converts 4 Cu(I) -> 4 Cu(II), so
    the total copper in solution must be constant.
    """
    p = make_params(m_Au=0.0)
    y0, _ = initial_state(p)
    y0[3] = 0.0          # no solid gold
    y0[5] = 0.0          # no solid copper
    y0[6] = 100.0        # Cu(I)
    y0[7] = 100.0        # Cu(II)
    _, traj = leach.simulate(p, y0, t_end=500.0)
    total = traj["Cu_I"] + traj["Cu_II"]
    assert np.allclose(total, total[0], rtol=1e-8)
