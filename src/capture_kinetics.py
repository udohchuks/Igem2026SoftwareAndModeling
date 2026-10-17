"""Time-dependent capture of gold, and of competing copper, on one GolB site pool.

`src.competition` answers where the two metals finish; this module answers how
the liquid gets there. Both metals draw on the same inventory `S_total`, so the
free-site balance is what couples them:

    r_Au    = k_on_Au*[Au]*[S_free] - k_off_Au*[Au-GolB]
    r_Cu    = k_on_Cu*[Cu]*[S_free] - k_off_Cu*[Cu-GolB]
    [S_free] = S_total - [Au-GolB] - [Cu-GolB]

The dissociation constants enter as `k_off = K*k_on`, which is the identity the
long-time limit of this system shares with the equilibrium module. `tests/
test_capture_kinetics.py` checks that limit against `src.competition` rather
than against a stored number.

No copper time constant has been measured for GolB. A copper feed is therefore
accepted only when copper rate constants are supplied with it, and the gold-only
call is the one the figures use. ISSUES.md items 22 and 92.

Units follow the rest of the repository: concentrations in uM, time in hours,
rate constants in uM^-1 h^-1 and h^-1.
"""

import numpy as np
from scipy.integrate import solve_ivp


def _physical(name, value, *, positive=False):
    value = float(value)
    if not np.isfinite(value) or value < 0.0 or (positive and value == 0.0):
        raise ValueError("%s must be finite and %s"
                         % (name, "positive" if positive else "non-negative"))
    return value


def k_off(K, k_on):
    """The dissociation rate constant implied by an affinity and an on-rate.

        k_off = K*k_on

    Written out because it is the only place the draft's `K_Au k_on,Au` becomes
    a number, and a sign or inversion error here is invisible in the trajectory.
    """
    return _physical("K", K, positive=True)*_physical("k_on", k_on, positive=True)


def simulate(Au_0, S_total, k_on_Au, K_Au, t_end, points, *,
             Cu_0=0.0, k_on_Cu=None, K_Cu=None):
    """Trajectories for one capture contact, as arrays in uM against hours.

    Returns `t_h`, `Au`, `Cu`, `Au_GolB`, `Cu_GolB`, the captured gold fraction
    `eta_capture_t`, and `gold_balance_residual_uM`, the largest departure of
    `[Au] + [Au-GolB]` from its starting value. The residual is returned rather
    than asserted, so a caller can report it instead of discovering a silent
    integration failure in a figure.

    The comb starts clean: `[Au-GolB]_0 = [Cu-GolB]_0 = 0`, which is the draft's
    initial condition and not a settable input.
    """
    Au_0 = _physical("Au_0", Au_0)
    Cu_0 = _physical("Cu_0", Cu_0)
    S_total = _physical("S_total", S_total)
    k_on_Au = _physical("k_on_Au", k_on_Au, positive=True)
    off_Au = k_off(K_Au, k_on_Au)
    t_end = _physical("t_end", t_end, positive=True)
    points = int(points)
    if points < 2:
        raise ValueError("points must be at least two")

    if Cu_0 > 0.0:
        if k_on_Cu is None or K_Cu is None:
            raise ValueError(
                "a copper feed needs k_on_Cu and K_Cu; no Cu-GolB time "
                "constant has been measured, so copper competition is "
                "reported at equilibrium by src.competition instead")
        on_Cu = _physical("k_on_Cu", k_on_Cu, positive=True)
        off_Cu = k_off(K_Cu, on_Cu)
    else:
        on_Cu = off_Cu = 0.0

    def rhs(_t, y):
        # Trial states are clipped into the physical domain for rate evaluation
        # only. The integrated states are returned unclipped, so the balance
        # residual below still reports a solver that has gone wrong.
        Au, Cu, Au_GolB, Cu_GolB = y
        Au, Cu = max(Au, 0.0), max(Cu, 0.0)
        Au_GolB, Cu_GolB = max(Au_GolB, 0.0), max(Cu_GolB, 0.0)
        S_free = max(S_total - Au_GolB - Cu_GolB, 0.0)
        r_Au = k_on_Au*Au*S_free - off_Au*Au_GolB
        r_Cu = on_Cu*Cu*S_free - off_Cu*Cu_GolB
        return [-r_Au, -r_Cu, r_Au, r_Cu]

    t = np.linspace(0.0, t_end, points)
    solution = solve_ivp(rhs, (0.0, t_end), [Au_0, Cu_0, 0.0, 0.0],
                         t_eval=t, method="LSODA", rtol=1e-10, atol=1e-12)
    if not solution.success:
        raise RuntimeError("capture integration failed: " + solution.message)
    Au, Cu, Au_GolB, Cu_GolB = solution.y
    residual = float(np.max(np.abs(Au + Au_GolB - Au_0)))
    return dict(t_h=t, Au=Au, Cu=Cu, Au_GolB=Au_GolB, Cu_GolB=Cu_GolB,
                eta_capture_t=Au_GolB/Au_0 if Au_0 else np.zeros_like(t),
                gold_balance_residual_uM=residual)
