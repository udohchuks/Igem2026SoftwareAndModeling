"""Two-metal competition for one GolB site inventory.

Extended-Langmuir capture of gold against copper, solved with the liquid mass
balance instead of the feed concentration. `src.recovery_chain.capture_equilibrium`
is the one-metal version of the same calculation; this module is what it becomes
when a second metal shares the sites.

Nothing here adopts a copper constant. `K_Cu` has never been measured in the
project liquor, so the entry point for reporting is `selectivity_sweep`, which
sweeps the dimensionless ratio `alpha = K_Cu / K_Au` and locates the point where
copper starts to take the sites. ISSUES.md items 22 and 92.

Units follow the rest of the repository: concentrations and site inventories in
uM, amounts in umol, capacities in umol per g dry cells.
"""

import numpy as np
from scipy.optimize import brentq


def occupancy(C_Au, C_Cu, K_Au, K_Cu):
    """Fractions of the site inventory held by gold and by copper.

    The extended Langmuir. Both metals divide one denominator, which is what
    makes them competitors rather than two independent isotherms:

        theta_Au = (C_Au/K_Au) / (1 + C_Au/K_Au + C_Cu/K_Cu)

    `C_Au` and `C_Cu` are FREE concentrations at equilibrium, never the feed.
    Passing a feed concentration here is the standard error and it overstates
    gold occupancy whenever binding depletes the liquid.
    """
    for name, value in (("C_Au", C_Au), ("C_Cu", C_Cu)):
        if value < 0.0:
            raise ValueError(name + " must be non-negative")
    for name, value in (("K_Au", K_Au), ("K_Cu", K_Cu)):
        if value <= 0.0:
            raise ValueError(name + " must be positive")
    a, b = C_Au/K_Au, C_Cu/K_Cu
    denom = 1.0 + a + b
    return a/denom, b/denom


def capture_equilibrium(Au_tot, Cu_tot, S0, K_Au, K_Cu):
    """Gold and copper bound at equilibrium, in the same unit as the inputs.

    Two mass balances share one site inventory `S0`:

        Au_tot = C_Au + S0*theta_Au(C_Au, C_Cu)
        Cu_tot = C_Cu + S0*theta_Cu(C_Au, C_Cu)

    Eliminating the copper balance leaves one monotone equation in the free
    gold, which `brentq` brackets on [0, Au_tot]. Reducing to a polynomial was
    avoided on purpose: the cubic loses the bound inventory at low feed for the
    same reason the one-metal quadratic did, and ISSUES.md item 26 records that
    failure.

    Returns a dict, not a tuple, because four of the five outputs are needed to
    tell a sizing result from an affinity result.
    """
    if S0 < 0.0 or Au_tot < 0.0 or Cu_tot < 0.0:
        raise ValueError("feeds and site inventory must be non-negative")

    def free_copper(C_Au):
        # Copper's own balance at a given free gold. Monotone in C_Cu, so the
        # same bracketing argument applies one level down.
        if Cu_tot == 0.0:
            return 0.0

        def residual(C_Cu):
            return C_Cu + S0*occupancy(C_Au, C_Cu, K_Au, K_Cu)[1] - Cu_tot

        return brentq(residual, 0.0, Cu_tot, xtol=1e-15, rtol=1e-14)

    def gold_residual(C_Au):
        C_Cu = free_copper(C_Au)
        return C_Au + S0*occupancy(C_Au, C_Cu, K_Au, K_Cu)[0] - Au_tot

    if Au_tot == 0.0:
        C_Au = 0.0
    else:
        C_Au = brentq(gold_residual, 0.0, Au_tot, xtol=1e-15, rtol=1e-14)
    C_Cu = free_copper(C_Au)
    th_Au, th_Cu = occupancy(C_Au, C_Cu, K_Au, K_Cu)
    return dict(free_Au=C_Au, free_Cu=C_Cu,
                bound_Au=S0*th_Au, bound_Cu=S0*th_Cu,
                theta_Au=th_Au, theta_Cu=th_Cu,
                captured_Au_fraction=(S0*th_Au/Au_tot) if Au_tot else 0.0,
                captured_Cu_fraction=(S0*th_Cu/Cu_tot) if Cu_tot else 0.0)


def separation_factor(result):
    """Ratio of distribution coefficients, the field's selectivity measure.

        S = (q_Au/C_Au) / (q_Cu/C_Cu)

    S > 1 means the sorbent enriches gold over copper. This is not the eluate
    enrichment factor, which also carries the wash and elution steps.
    """
    num = result["bound_Au"]/result["free_Au"] if result["free_Au"] else np.inf
    den = result["bound_Cu"]/result["free_Cu"] if result["free_Cu"] else 0.0
    if den == 0.0:
        return np.inf
    return num/den


def critical_selectivity(Au_tot, Cu_tot):
    """The selectivity `alpha = K_Cu/K_Au` at which the two metals tie.

    Gold and copper claim equal shares of the denominator when
    C_Au/K_Au = C_Cu/K_Cu, so the tie sits at alpha = C_Cu/C_Au. Evaluated on
    the feed it is an upper bound on the requirement, because binding depletes
    gold faster than copper.
    """
    if Au_tot <= 0.0:
        raise ValueError("Au_tot must be positive")
    return Cu_tot/Au_tot


def selectivity_sweep(Au_tot, Cu_tot, S0, K_Au, alphas):
    """Capture across a sweep of alpha = K_Cu/K_Au, with K_Cu never adopted.

    This is the reporting entry point while the copper constant is unmeasured:
    one dimensionless unknown, swept, with the breakpoint read off the table.
    """
    rows = []
    for alpha in np.atleast_1d(np.asarray(alphas, dtype=float)):
        if alpha <= 0.0:
            raise ValueError("alpha must be positive")
        r = capture_equilibrium(Au_tot, Cu_tot, S0, K_Au, alpha*K_Au)
        r["alpha"] = float(alpha)
        r["separation_factor"] = separation_factor(r)
        rows.append(r)
    return rows
