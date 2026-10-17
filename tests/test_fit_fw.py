"""The fitter must recover constants it was not told, from data shaped like the
plate reader's. ISSUES.md item 81.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import fit_fw  # noqa: E402


def _course(Au_aq0, k_nuc, k_grow, t_end, n=80, noise=0.0, seed=0):
    t = np.linspace(0.0, t_end, n)
    y = fit_fw.finke_watzky_curve(t, Au_aq0, k_nuc, k_grow)
    if noise:
        y = y + np.random.default_rng(seed).normal(0.0, noise * Au_aq0, y.shape)
    return t, y


def test_it_recovers_the_constants_it_was_given():
    for Au_aq0, k_nuc, k_grow in ((3.0, 5.0e-5, 0.2),
                                  (0.367, 1.0e-4, 0.082),
                                  (11.0, 8.6e-4, 3.2e-3)):
        t_end = 3.0 * fit_fw.t_to_conversion(Au_aq0, k_nuc, k_grow, 0.95)
        t, y = _course(Au_aq0, k_nuc, k_grow, t_end)
        kn, kg, _, _ = fit_fw.fit_finke_watzky(t, y, Au_aq0)
        assert kn == pytest.approx(k_nuc, rel=0.05)
        assert kg == pytest.approx(k_grow, rel=0.05)


def test_optical_calibration_preserves_the_concentration_scale():
    """A plate reader returns arbitrary units, so the fit must not depend on
    them. The same curve at 1x and at 137x must give the same constants."""
    t, y = _course(3.0, 5.0e-5, 0.2, 40.0)
    a = fit_fw.fit_finke_watzky(t, y, 3.0)
    b = fit_fw.fit_finke_watzky(t, 137.0 * y, 3.0, signal_per_uM=137.0, baseline=0.0)
    assert a[0] == pytest.approx(b[0], rel=1e-6)
    assert a[1] == pytest.approx(b[1], rel=1e-6)


def test_it_accepts_dissolved_gold_as_well_as_metal_made():
    t, y = _course(3.0, 5.0e-5, 0.2, 40.0)
    kn, kg, _, _ = fit_fw.fit_finke_watzky(t, 3.0 - y, 3.0, dissolved=True)
    assert kn == pytest.approx(5.0e-5, rel=0.05)
    assert kg == pytest.approx(0.2, rel=0.05)


def test_it_survives_two_percent_noise():
    t, y = _course(3.0, 5.0e-5, 0.2, 40.0, noise=0.02, seed=7)
    kn, kg, _, _ = fit_fw.fit_finke_watzky(t, y, 3.0)
    assert kn == pytest.approx(5.0e-5, rel=0.5)
    assert kg == pytest.approx(0.2, rel=0.2)


def test_t_to_conversion_matches_the_curve_it_came_from():
    for f in (0.5, 0.95):
        t95 = fit_fw.t_to_conversion(3.0, 5.0e-5, 0.2, f)
        assert fit_fw.finke_watzky_curve(t95, 3.0, 5.0e-5, 0.2) == \
            pytest.approx(f * 3.0, rel=1e-6)


def test_it_refuses_data_it_cannot_fit():
    t = np.linspace(0.0, 10.0, 40)
    with pytest.raises(ValueError):
        fit_fw.fit_finke_watzky(t, np.zeros_like(t), 3.0)
    with pytest.raises(ValueError):
        fit_fw.fit_finke_watzky(t[:3], t[:3], 3.0)
