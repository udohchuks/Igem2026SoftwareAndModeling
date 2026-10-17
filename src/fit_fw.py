"""Fit donor-excess Finke-Watzky kinetics to calibrated concentrations.

Absolute metal data or dissolved gold after excluding non-reduction losses
may be used. Optical input needs a measured blank and signal-per-uM
calibration valid across the time course. A plateau does not establish total
conversion: extinction changes with particle properties. ISSUES 85, S75.
Synthetic fits verify the implementation; they do not validate the chemistry.
"""

import numpy as np
from scipy.optimize import curve_fit

__all__ = ["finke_watzky_curve", "fit_finke_watzky", "t_to_conversion"]


def finke_watzky_curve(t, Au_aq0, k_nuc, k_grow):
    """Solid gold at time t, from the closed form. Units: uM, h.

    Bentea, Watzky & Finke 2017; SOURCES.md S67. Vectorised over t.
    """
    t = np.asarray(t, dtype=float)
    if Au_aq0 < 0.0 or k_nuc < 0.0 or k_grow < 0.0 or np.any(t < 0.0):
        raise ValueError("concentrations, rate constants and times must be non-negative")
    lam = k_nuc + k_grow * Au_aq0
    # Equivalent closed form using a decaying exponential. It handles pure
    # nucleation and zero feed without dividing by k_grow or by the feed.
    decay = np.exp(-lam * t)
    denom = k_nuc + k_grow * Au_aq0 * decay
    return np.divide(Au_aq0 * k_nuc * -np.expm1(-lam * t), denom,
                     out=np.zeros_like(t), where=denom > 0.0)


def fit_finke_watzky(t_h, signal, Au_aq0, dissolved=False, p0=None,
                    *, signal_per_uM=None, baseline=None):
    """Return (k_nuc, k_grow, one_sigma_k_nuc, one_sigma_k_grow).

    t_h       hours from the start of the reaction
    signal    calibrated metal concentration in uM, or calibrated optical
              signal with signal_per_uM and a measured blank baseline
    Au_aq0    gold charged, uM
    dissolved set True when `signal` tracks gold REMAINING in solution
              (ICP-MS on the filtrate) rather than metal made

    Never normalise against the observed maximum: an incomplete experiment
    is not evidence of full conversion. Dissolved inputs are absolute uM;
    their disappearance is only a metal proxy after adsorption and other
    losses have been excluded experimentally. Errors are conditional fit
    covariance estimates, not uncertainty in the reaction mechanism.
    """
    t_h = np.asarray(t_h, dtype=float)
    y = np.asarray(signal, dtype=float)
    if t_h.shape != y.shape:
        raise ValueError("t_h and signal must have the same length")
    if t_h.size < 5:
        raise ValueError("at least 5 points are needed to fit two constants")
    if t_h.ndim != 1 or not np.all(np.isfinite(t_h)) or not np.all(np.isfinite(y)):
        raise ValueError("time and signal must be finite one-dimensional arrays")
    if Au_aq0 <= 0.0 or not np.isfinite(Au_aq0):
        raise ValueError("Au_aq0 must be finite and positive")
    if np.any(np.diff(t_h) <= 0.0) or np.any(t_h < 0.0):
        raise ValueError("times must be non-negative and strictly increasing")
    if dissolved:
        if signal_per_uM is not None or baseline is not None:
            raise ValueError("dissolved gold must be supplied as absolute uM")
        Au_s = Au_aq0 - y
    elif signal_per_uM is not None:
        if signal_per_uM <= 0.0 or not np.isfinite(signal_per_uM) or baseline is None:
            raise ValueError("optical input needs positive signal_per_uM and a baseline")
        if not np.isfinite(baseline):
            raise ValueError("baseline must be finite")
        Au_s = (y - baseline) / signal_per_uM
    else:
        if baseline is not None:
            raise ValueError("baseline requires an optical calibration")
        Au_s = y
    if float(np.max(Au_s)) <= 0.0:
        raise ValueError("the signal never rises; there is nothing to fit")

    if p0 is None:
        # A first guess costs nothing and keeps the optimiser off the flat part
        # of the surface. t_ind = 1/(k_grow*Au_aq0) inverts the observed time to
        # 5 % conversion; k_nuc then follows from the initial slope.
        hits = np.flatnonzero(Au_s >= 0.05 * Au_aq0)
        i = int(hits[0]) if hits.size else t_h.size - 1
        i = min(max(i, 1), t_h.size - 1)
        k_grow0 = 1.0 / max(t_h[i], 1e-6) / Au_aq0
        k_nuc0 = max(Au_s[i] / max(t_h[i], 1e-6) / Au_aq0, 1e-8)
        p0 = (k_nuc0, k_grow0)

    popt, pcov = curve_fit(
        lambda t, kn, kg: finke_watzky_curve(t, Au_aq0, kn, kg),
        t_h, Au_s, p0=p0, bounds=((1e-12, 1e-8), (1e3, 1e6)), maxfev=20000)
    err = np.sqrt(np.diag(pcov))
    return float(popt[0]), float(popt[1]), float(err[0]), float(err[1])


def t_to_conversion(Au_aq0, k_nuc, k_grow, f=0.95):
    """Hours to convert a fraction f of the gold. docs/RECOVERY.md 4.3.

    This is the number a fitted pair is FOR: it sizes the vessel.
    """
    if not 0.0 < f < 1.0:
        raise ValueError("f must lie strictly between 0 and 1")
    if Au_aq0 <= 0.0 or k_nuc < 0.0 or k_grow < 0.0:
        raise ValueError("positive feed and non-negative rate constants are required")
    if k_nuc == 0.0:
        return float("inf")
    ratio = k_grow * Au_aq0 / k_nuc
    return float(np.log((1.0 + f * ratio) / (1.0 - f)) / (k_nuc + k_grow * Au_aq0))
