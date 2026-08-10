"""Part III — capture, elution, reduction, recovery.

This module is a SHIM, not an implementation.

model.md v3.0 names three existing files as the code for this part:

    pipeline_model.py    V1 capture, elution, the full chain
    r9L_fw.py            rung 9L reduction, Finke-Watzky nucleation
    ensemble.py          Latin hypercube sampling, PRCC

Those files were not re-implemented here, deliberately. Re-deriving equations
that already have working, verified code would create a second version that
drifts from the first, and model.md sections 2 and 4.1 record verification
checks that pass against the existing code.

TO COMPLETE THIS MODULE
-----------------------
Copy pipeline_model.py, r9L_fw.py and ensemble.py into src/, then delete the
_missing() calls below and re-export their entry points, for example:

    from .pipeline_model import chain, eta_capture, eta_elute
    from .r9L_fw import eta_reduce
    from .ensemble import sample, prcc, NAMES

The closed-form results that model.md states in the text are implemented
below, because they need no ODE and they are useful on their own.
"""

import numpy as np

_MISSING = (
    "Part III code is not in this repository yet. Copy {f} into src/ and "
    "wire it up in src/recovery_chain.py. See the module docstring."
)


def chain(*args, **kwargs):
    raise NotImplementedError(_MISSING.format(f="pipeline_model.py"))


def eta_reduce_ode(*args, **kwargs):
    raise NotImplementedError(_MISSING.format(f="r9L_fw.py"))


def sample(*args, **kwargs):
    raise NotImplementedError(_MISSING.format(f="ensemble.py"))


# --- closed forms stated directly in model.md -----------------------------

def eta_elute(t_k, phi, k_max):
    """model.md section 3 — the boxed elution result.

        eta_elute(t_k) = (1 - phi) * (1 - exp(-k_max * t_k))

    (1 - phi) is a chemistry ceiling, not improvable by time or acid
    strength. The exponential term reaches 95% of that ceiling at 3/k_max.
    """
    return (1.0 - phi) * (1.0 - np.exp(-k_max * np.asarray(t_k, dtype=float)))


def capture_langmuir_equilibrium(A, S0, K_D):
    """model.md section 2 — the Langmuir limit used as a verification check.

        C_eq = S0 * A / (A + K_D)
    """
    return S0 * A / (A + K_D)


def capacity_ceiling(q_max, X_max, Au_tot):
    """model.md section 2 — eta <= q_max * X_max / Au_tot.

    A capture efficiency above this value is impossible regardless of rates,
    so it is the first thing to check when a capture number looks good.
    """
    return q_max * X_max / Au_tot


def electron_budget_ceiling(E_tot, R0, A0, n_e_Au):
    """model.md section 4.1 — the rate-free reduction ceiling.

        eta_reduce <= (2*E_tot + 2*R0) / (n_e_Au * A0)

    Needs no rate constant. Section 4.1 uses it twice: to show that 0.2 g/L
    protein already supplies 98.9% of the electrons at 5.78 uM Au(I), and to
    show that the source papers' regime covers only 0.048%.
    """
    return (2.0 * E_tot + 2.0 * R0) / (n_e_Au * A0)


def eta_phys(eta_spin, eta_wash, eta_ash):
    """model.md section 5 — eta_phys = eta_spin * eta_wash * eta_ash."""
    return eta_spin * eta_wash * eta_ash


def eta_total(eta_capture, eta_elute_, eta_reduce, eta_phys_):
    """model.md section 1 — the product of the four stage efficiencies."""
    return eta_capture * eta_elute_ * eta_reduce * eta_phys_
