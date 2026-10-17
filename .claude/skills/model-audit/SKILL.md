---
name: model-audit
description: Full consistency audit of the gold-biorecovery model repository. Checks that code, parameter files, tests, documents and the notebook all tell the same story, and that every claim traces to a source or an issue. Use before a commit, a supervisor hand-off, or after any joint value changes.
---

# Model audit

Audit this repository for internal consistency. The model is correct only if
five artefacts agree: `src/`, `params/`, `tests/`, `docs/` and `model.ipynb`.

**Read `AGENTS.md` before starting.** This skill assumes its five rules.

Report findings, do not fix them, unless the user asks. A wrong number in a
document is a finding. A wrong number in a source document is **not** a finding
here; it belongs in `docs/ISSUES.md` and stays in the text.

Work through all seven phases in order. Do not skip a phase because an earlier
one passed.

---

## Phase 1 — Does it run

Four checks. Record the real output of each.

```bash
python -m pytest tests -q
```

```bash
python -c "import yaml,io; [yaml.safe_load(io.open(f'params/{f}.yaml',encoding='utf-8')) for f in ('leach','expression','recovery_chain','conversions')]; print('yaml ok')"
```

```bash
python -c "
import json,io,sys
nb=json.load(io.open('model.ipynb',encoding='utf-8'))
g={}
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code': continue
    try: exec(compile(''.join(c['source']),f'<cell {i}>','exec'),g)
    except Exception as e: print('FAIL cell',i,type(e).__name__,e); sys.exit(1)
print('notebook ok')"
```

```bash
python -c "from src import params; [params.load(f) for f in ('leach','expression','recovery_chain','conversions')]; print('loader ok')"
```

**Fail here and stop.** Report the failure and do not continue; later phases
read values that may not load.

---

## Phase 2 — Numbers agree across artefacts

For every number that appears in more than one place, confirm the copies match.

1. **Joint values.** `q_max`, `Au_feed` range, `mu`, `K_Au`, `Vmax`,
   `teth_per_cell`, `k_cat`, `cells_per_g`. Read each from its YAML, then grep
   `docs/*.md` and `model.ipynb` for the digits. Every hit must match or be
   explicitly labelled `superseded`, `retired` or historical.

2. **Derived numbers.** Recompute them, do not trust the text.
   - `Vmax = k_cat × teth_per_cell × biomass × cells_per_g / N_A × 1e6`
   - `q_max = sites_per_cell × cells_per_g / N_A × 1e6`
   - capacity ceiling `= q_max × X_max`
   - `teth_per_cell = f × P_s` from `expression.simulate`

3. **Counts.** The issue count, the test count and the source count appear in
   several documents. Count them from the files, not from the prose.

Report any mismatch as: file, line, value found, value expected, which is right.

---

## Phase 3 — Every parameter is accounted for

```bash
python -c "from src import params; params.report()" 2>/dev/null || python -c "
from src import params
for f in ('leach','expression','recovery_chain'):
    b=params.load(f); print(f)"
```

For each parameter in each YAML file, confirm:

- It has `value`, `unit`, `meaning`, `status` and `source`.
- `status: sourced` carries a real citation, not `null`.
- `value: null` parameters are genuinely unavailable, and a run without them
  raises `KeyError` rather than substituting a guess.
- Any `superseded` or `retired_*` block states **why** it was superseded.

Then check the reverse direction: every parameter `src/` reads with `p["..."]`
exists in a YAML file or is documented as test-only.

```bash
grep -oh 'p\["[a-zA-Z_0-9]*"\]' src/*.py | sort -u
```

---

## Phase 4 — Symbols are consistent

The naming rules are in `AGENTS.md` §5 and the was/now map in
`docs/EQUATIONS.md`.

```bash
grep -rn "K_d\b\|K_D\b\|\bk1\b\|\bk2\b\|\bk3\b\|\bk4\b\|A_Au\|A_Cu\b\|k_max\|K_i\b\|K_m\b\|K_S\b\|K_Cu\b" src/ params/ tests/ docs/MASTER.md docs/EQUATIONS.md model.ipynb
```

Every hit must be one of:

- inside the intentional was/now mapping table in `docs/EQUATIONS.md`;
- inside prose that is explicitly quoting a source document;
- inside an `ISSUES.md` item describing the old name.

Anything else is a stale symbol. **Do not grep the source documents**; they
keep their original symbols by rule.

---

## Phase 5 — Claims trace to evidence

Sample at least eight claims across the documents. For each, follow the chain:

```
claim in MASTER.md  ->  number in params/*.yaml  ->  source in SOURCES.md
                                                 or  issue in ISSUES.md
```

A claim fails this phase if it has no number behind it, if the number has no
source or issue behind it, or if the source says something different from what
the claim says.

Pay attention to:

- **Conditional results.** A sensitivity ranking or an operating window is
  valid only at the operating point it was computed at. Check that each says so.
- **Bounds.** A number marked `bound: lower` must not be quoted as a value.
- **Reversed conclusions.** `ISSUES.md` contains items whose headline was later
  reversed. Confirm the reversal is stated at the top of the item, not buried.

---

## Phase 6 — Documents agree with each other

- `docs/ISSUES.md` Open and Closed tables against the section headings that
  follow. Every numbered item appears exactly once in exactly one table.
- Per-step "Open issues touching this step" tables in `docs/MASTER.md` must
  list only items the `ISSUES.md` index calls open.
- `STRUCTURE.md` counts and its "Read this first" against the current position.
- `docs/EQUATIONS.md` equations against `src/`. Read the code, not the prose.
- `docs/SOURCES.md` reference numbers against every `[S..]` citation used
  anywhere.

```bash
grep -oh "\[S[0-9]*\]" docs/*.md params/*.yaml | sort -u -V
```

---

## Phase 7 — What the model cannot currently tell you

List the parameters that are `null`, `fitted`, `assumed` or `placeholder`, and
say which downstream number each one controls. This is the honest limits
section. It is not a failure list; it is what a reader needs before quoting any
result.

Rank by how much each moves the answer, and say so in multiples.

---

## Reporting

Structure the report as:

1. **Verdict in one line**, then the four Phase 1 results as a table.
2. **Findings**, ranked most severe first. For each: what, where as
   `file:line`, why it is wrong, and the fix.
3. **What is sound**, briefly. Say what you checked and found correct, so the
   reader knows the scope of the audit.
4. **Limits of this audit.** What you did not check, and why.

Severity:

- **Blocking** — a number in use is wrong, or the chain does not run.
- **Serious** — two artefacts disagree, and a reader could quote the wrong one.
- **Minor** — stale text, wrong count, broken cross-reference.

Do not pad the report. A finding with no consequence is not a finding.
