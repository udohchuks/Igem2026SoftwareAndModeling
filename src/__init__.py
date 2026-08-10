"""Gold biorecovery from e-waste — coupled process models.

Part I    src/leach.py        bioleaching, PCB -> dissolved Au(S2O3)2 3-
Part II   src/expression.py   GolB surface site density
Part III  src/recovery_chain.py  capture -> elution -> reduction -> recovery

The two joints between them live in src/interfaces.py.
All numbers live in params/*.yaml and are loaded through src/params.py.
"""

__all__ = ["params", "leach", "expression", "interfaces", "recovery_chain"]
