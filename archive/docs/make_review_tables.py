"""Regenerate the parameter appendix of docs/REVIEW.docx from params/*.yaml.

Run from the repository root:

    python docs/make_review_tables.py

Writes docs/_review_parameters.md, which docs/REVIEW.md includes. Every row is
read from the YAML, so a parameter cannot be quoted here with a value the model
does not hold. Retired and superseded blocks are skipped; they are recorded in
the YAML itself and in docs/ISSUES.md.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import params  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "_review_parameters.md"

SKIP_KEYS = {"meta", "reported_steady_state", "reported", "notes"}
SKIP_SUBKEYS = ("superseded", "retired", "was_", "previous")

FILES = [
    ("leach", "A.1 Bioleaching — all three vessels"),
    ("expression", "A.2 GolB surface display"),
    ("recovery_chain", "A.3 Recovery chain"),
    ("conversions", "A.4 Constants used at the handovers"),
]

STATUS_WORDS = {
    "sourced": "sourced",
    "team_assumption": "**assumed by us**",
    "team_decision": "team decision",
    "assumed": "**assumed**",
    "operating_choice": "operating choice",
    "unmeasured": "**unmeasured**",
    "calibrate": "**needs calibration**",
    "fitted": "**fitted**",
    "geometry": "geometry",
    "derived": "derived",
    "placeholder": "**placeholder**",
    "computed": "computed",
    "sourced_by_proxy": "sourced by proxy",
    "derived_from_recipe": "derived from the recipe",
    "assumed_equal_to_k_Cu_O2": "**assumed equal to `k_Cu_O2`**",
    "input_measured": "measured input",
    "derive_at_use": "derived at use",
    "design_choice": "design choice",
    "adopted_from_part_II": "adopted from the display model",
    "derived_from_part_II": "derived from the display model",
}


def leaves(node, trail=()):
    """Yield (path, block) for every mapping that carries a `value` key."""
    if not isinstance(node, dict):
        return
    if "value" in node:
        yield trail, node
        return
    for key, child in node.items():
        if key in SKIP_KEYS or any(key.startswith(p) for p in SKIP_SUBKEYS):
            continue
        yield from leaves(child, trail + (key,))


def cell(text):
    if text is None:
        return "—"
    text = str(text).replace("\n", " ").replace("|", "\\|").strip()
    return " ".join(text.split())


def fmt_value(v):
    if v is None:
        return "**null — model refuses to run**"
    if isinstance(v, float):
        if v != 0 and (abs(v) < 1e-3 or abs(v) >= 1e5):
            return f"{v:.3g}"
        return f"{v:g}"
    return cell(v)


def source_of(block):
    for key in ("source", "sources", "ref", "reference"):
        if block.get(key):
            return cell(block[key])
    note = block.get("note") or block.get("basis")
    return cell(note)[:110] if note else "—"


lines = [
    "# Appendix A — every parameter in the model",
    "",
    "**Tier 4, generated. Do not hand-edit this file.** It is rewritten from",
    "`params/*.yaml` by `docs/make_review_tables.py` every time",
    "`docs/build_review.py` runs, and any edit made here is discarded without",
    "warning. `AGENTS.md` section 11.",
    "",
    "Each row is read from the file the code loads, so no value here can differ",
    "from the one the model used to produce the figures above.",
    "",
    "**Read the status column first.** Anything marked *assumed*, *unmeasured*,",
    "*fitted* or *placeholder* is a number we chose rather than found. Every one",
    "of those appears in section 8, where we ask you to confirm it. A parameter",
    "with no value stays `null` and the model raises an error rather than",
    "substituting a guess.",
    "",
    "Where the source column says *Stage 1*, *Stage 2* or *Stage 3*, that is the",
    "source document's own numbering for the culture, conversion and leach",
    "vessels, quoted unchanged.",
    "",
]

total = 0
flagged = 0

for stem, title in FILES:
    raw = params.load(stem)
    rows = []
    for trail, block in leaves(raw):
        name = trail[-1]
        group = ".".join(trail[:-1]) or "—"
        status = str(block.get("status", "—"))
        rows.append((
            cell(name),
            cell(group),
            fmt_value(block.get("value")),
            cell(block.get("unit", "—")),
            STATUS_WORDS.get(status, cell(status)),
            source_of(block),
        ))
        total += 1
        if status in ("team_assumption", "assumed", "unmeasured", "calibrate",
                      "fitted", "placeholder") or block.get("value") is None:
            flagged += 1

    if not rows:
        continue

    lines += [
        f"## {title}",
        "",
        f"Source file: `params/{stem}.yaml`",
        "",
        "| Parameter | Block | Value | Unit | Status | Source or basis |",
        "|---|---|---|---|---|---|",
    ]
    lines += ["| " + " | ".join(r) + " |" for r in sorted(rows, key=lambda r: (r[1], r[0]))]
    lines.append("")

lines += [
    f"**{total} parameters in total. {flagged} of them are assumed, fitted, "
    f"unmeasured, or awaiting a value.** Those are the ones worth your time.",
    "",
]

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)}  ({total} parameters, {flagged} flagged)")
