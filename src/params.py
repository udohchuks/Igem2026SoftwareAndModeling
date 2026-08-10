"""Parameter loading.

Every number in the model comes from params/*.yaml, never from a literal in a
model module. This keeps the "value / unit / status / source" record attached
to the number itself, which is the discipline all three source documents
already follow in their parameter tables.
"""

from pathlib import Path

import yaml

PARAMS_DIR = Path(__file__).resolve().parent.parent / "params"


def load(name):
    """Load one parameter file, e.g. load('expression')."""
    with open(PARAMS_DIR / f"{name}.yaml", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def values(block):
    """Collapse a parameter block to a plain {symbol: value} dict.

    Entries whose value is null are omitted, so a missing calibration target
    raises a KeyError at the point of use rather than silently becoming None.
    """
    out = {}
    for symbol, spec in block.items():
        if symbol == "meta" or not isinstance(spec, dict):
            continue
        if spec.get("value") is not None:
            out[symbol] = spec["value"]
    return out


def unsourced(name):
    """List parameters that are fitted, assumed, placeholder, or to calibrate.

    model.md section 0 records that every parameter assumed without a source,
    then sourced, turned out to be wrong. This function is how that list stays
    visible instead of being buried in a table.
    """
    doc = load(name)
    flagged = []

    def walk(block, prefix=""):
        for symbol, spec in block.items():
            if symbol == "meta" or not isinstance(spec, dict):
                continue
            if "status" in spec or "value" in spec:
                status = str(spec.get("status", ""))
                if any(w in status.lower() for w in
                       ("calibrate", "fitted", "assumed", "placeholder",
                        "unsourced", "unmeasured", "upper bound")):
                    flagged.append((prefix + symbol, status))
            else:
                walk(spec, prefix + symbol + ".")

    walk(doc)
    return flagged
