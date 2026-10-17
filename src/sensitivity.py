"""Conditional three-stage recovery scenarios, Latin hypercube sampling and PRCC.

Capture and elution use recovery_chain closed forms; reduction integrates
an effective donor-coupled Finke-Watzky law. Parameter transfer remains a
hypothesis. Verification against balances and synthetic cases is not
experimental validation. ISSUES 84-88.

PRCC measures partial monotonic association in a specified sampling design.
Average ranks handle ties; constant outputs have undefined correlation.
Historical PRCC files are not current results or calibrated uncertainties.
"""

import itertools

import numpy as np
from scipy.stats import rankdata

from . import recovery_chain as rc


def reduce_worst_case(Au_aq0, p, bands, t_end=None):
    """Lowest conversion among the supplied parameter-range corners.

    This is a corner scenario check, not a proof of a global minimum over
    arbitrary bands. Interior extrema, uncertain mechanisms and unmodelled
    failures are not covered. The full recovery kinetic grid is generated
    separately; none of these scenarios is a confidence interval.
    """
    names = sorted(bands)
    worst, where = None, None
    for combo in itertools.product(*(bands[k] for k in names)):
        corner = dict(zip(names, combo))
        eta = reduce_finke_watzky(Au_aq0, dict(p, **corner), t_end=t_end)
        if worst is None or eta < worst:
            worst, where = eta, corner
    return worst, where


def reduce_finke_watzky(Au_aq0, p, t_end=None, n=None):
    """Compatibility endpoint interface to the checked reduction trajectory.

    ``n`` is retained for callers; only the requested endpoint is evaluated.
    Legacy dictionaries obtain recharge stoichiometry from the parameter file.
    """
    from . import reduction, params
    q = dict(p)
    if "nu_rech" not in q:
        q["nu_rech"] = params.values(params.load("recovery_chain")["reduction"])["nu_rech"]
    end = q["t_reduce_h"] if t_end is None else t_end
    return reduction.simulate(Au_aq0, q, t_end=end, times=[end])["eta_reduce"]


def chain_eta_total(p):
    """The four stages multiplied, from one parameter dictionary."""
    S0 = p["q_max"] * p["X_max"]
    eta_cap = float(rc.eta_capture(p["Au_feed"], S0, p["K_Au"]))
    eta_el = float(rc.eta_elute(p["t_elute_h"], p["phi"], p["k_elute"]))
    gold_to_reduce = p["Au_feed"] * eta_cap * eta_el
    eta_red = reduce_finke_watzky(gold_to_reduce, p)
    # Physical collection is OUT OF SCOPE, permanently, decided 2026-08-21.
    # Whatever gold reaches metal is the gold we have, so the chain is three
    # stages and not four. A caller that still supplies eta_spin, eta_wash or
    # eta_ash is working from a stale idea of what this model covers, and is
    # told so rather than silently given a different answer.
    for stale in ("eta_phys", "eta_spin", "eta_wash", "eta_ash"):
        if stale in p:
            raise ValueError(
                "%s was supplied, but physical recovery is out of scope. "
                "eta_total ends at reduction. params/recovery_chain.yaml, "
                "the recovery block." % stale)
    return {"eta_capture": eta_cap, "eta_elute": eta_el,
            "eta_reduce": eta_red,
            "eta_total": eta_cap * eta_el * eta_red}


def latin_hypercube(ranges, n, rng):
    """One stratified sample per parameter, shuffled independently.

    `ranges` maps a name to (low, high, scale) with scale "lin" or "log".
    Returns {name: array of n draws}. Latin hypercube rather than plain Monte
    Carlo because it covers each parameter's range evenly at small n, which
    matters when one ODE solve costs milliseconds.
    """
    out = {}
    for name, (lo, hi, scale) in ranges.items():
        strata = (rng.permutation(n) + rng.random(n)) / n
        if scale == "log":
            out[name] = np.exp(np.log(lo) + strata * (np.log(hi) - np.log(lo)))
        else:
            out[name] = lo + strata * (hi - lo)
    return out


def _rank(x):
    # Equal observations must have equal ranks. Arbitrary ordering of ties
    # fabricates correlations, especially for saturated conversion outputs.
    return rankdata(np.asarray(x, dtype=float), method="average")


def prcc(samples, output):
    """Partial rank correlation of each input with the output.

    Returns {name: rho}. Values near zero mean the parameter does not move the
    result monotonically once the others are accounted for; it does NOT mean
    the parameter is unimportant in absolute terms.
    """
    names = list(samples)
    if np.ptp(output) == 0.0:
        return {name: float("nan") for name in names}
    R = np.column_stack([_rank(samples[k]) for k in names])
    y = _rank(np.asarray(output, dtype=float))
    n, k = R.shape
    ones = np.ones((n, 1))
    out = {}
    for i, name in enumerate(names):
        if np.ptp(R[:, i]) == 0.0:
            out[name] = float("nan")
            continue
        others = np.delete(R, i, axis=1)
        X = np.hstack([ones, others])
        beta_i, *_ = np.linalg.lstsq(X, R[:, i], rcond=None)
        beta_y, *_ = np.linalg.lstsq(X, y, rcond=None)
        ri = R[:, i] - X @ beta_i
        ry = y - X @ beta_y
        denom = np.sqrt(np.sum(ri * ri) * np.sum(ry * ry))
        out[name] = 0.0 if denom == 0.0 else float(np.sum(ri * ry) / denom)
    return out


def run(fixed, ranges, n=2000, seed=0):
    """Sample, evaluate the chain, and return (samples, outputs, prcc table)."""
    rng = np.random.default_rng(seed)
    samples = latin_hypercube(ranges, n, rng)
    totals = np.empty(n)
    parts = {k: np.empty(n) for k in
             ("eta_capture", "eta_elute", "eta_reduce")}
    for j in range(n):
        p = dict(fixed)
        p.update({name: samples[name][j] for name in samples})
        r = chain_eta_total(p)
        totals[j] = r["eta_total"]
        for k in parts:
            parts[k][j] = r[k]
    return samples, {"eta_total": totals, **parts}, prcc(samples, totals)
