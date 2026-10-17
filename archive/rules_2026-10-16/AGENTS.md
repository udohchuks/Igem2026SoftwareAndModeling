# Working in this repository

**Tier 3, synthesis. This file is the only home for rules.** If a rule belongs
to the project it goes here, so that no two files can drift apart on it.
Section 11 says what every other document is for.

This is the iGEM 2026 gold-biorecovery model. Three source documents describe
one process chain. This repository merges them, records where they disagree,
and pins each disagreement with a test.

Read this file before changing anything. It is the operating manual.
`CLAUDE.md` points here.

---

## 1. The five rules. Do not break these.

1. **Never edit a source document.** `docs/source/`, `docs/00_*`, `docs/01_*`,
   `docs/02_*` and `docs/MODEL.md` are verbatim. Errors in them are recorded in
   `docs/ISSUES.md` and **left standing in the text**. Only their authors
   correct them.
2. **No number in a `.py` file.** Every value lives in `params/*.yaml` with its
   unit, status and source. `src/params.py` loads them.
3. **No equation in the notebook.** Equations live in `src/`. The notebook
   imports and plots. If you write a `def` in a cell, move it to `src/`.
4. **A parameter with no value stays `null`.** Loading it must raise
   `KeyError`, never substitute a guess. Part III §0 records that every
   parameter assumed without a source, then sourced, turned out to be wrong.
5. **Discrepancies get a test, not a silent fix.** Where the documents
   disagree, a test pins the disagreement so a later edit cannot hide it.

A sixth rule, softer: **do not delete the record.** Superseded values move to a
`superseded:` or `retired_*:` block in the same YAML file, with the reason.
Reversed conclusions in `ISSUES.md` are restated, not erased.

---

## 2. What is where

```
docs/ISSUES.md        52 findings. Items 32 and 44 are BLOCKING; 41 is the
                      one with the free win. START HERE.
docs/MASTER.md        the end-to-end model in plain language
docs/EQUATIONS.md     every equation, one line of English each. Equations
                      and annotation only; history lives in ISSUES.md
docs/SOURCES.md       41 papers, each tied to the number it supplies
STRUCTURE.md          file-by-file layout and setup

src/leach.py          Part I, bioleaching. Three vessels:
                      simulate_stage2, simulate_stage3, simulate_sequential
src/expression.py     Part II, GolB surface display
src/recovery_chain.py Part III closed forms and compatibility entry points
src/recovery_process.py Explicit stage amounts, volumes and lysate mixing
src/reduction.py      Reduction trajectories and gold/electron checks
src/interfaces.py     the joints, with unit checks
src/params.py         YAML loader; lists unsourced parameters
src/sensitivity.py    Latin hypercube + PRCC; the Finke-Watzky reduction ODE

params/*.yaml         one file per part, plus conversions.yaml
tests/                75 tests
model.ipynb           narrative and every figure
```

**`docs/ISSUES.md` is the entry point for any reconciliation work.** Its Open
table is ordered by what the item costs. Do not start work on an item without
reading its section in full.

---

## 3. The chain, and where the parts touch

```
Part I  leaching   ──Au_feed──►  Part III  capture ─► elute ─► reduce ─► recover
                                    ▲
Part II expression ──q_max──────────┘
                   ──[TetH]──►  Part I's Vmax
```

Three joints, all in `src/interfaces.py` or `params/leach.yaml`:

| Joint | Quantity | From | To |
|---|---|---|---|
| 1 | `Au_feed`, dissolved gold | Part I | Part III |
| 2 | `q_max`, capacity per gram | Part II | Part III |
| 3 | `Vmax`, enzyme capacity | Part II | Part I |

Joint 3 was added 2026-08-11. Part II's expression cascade now supplies both
GolB sites and TetH enzyme, because one organism runs the whole chain.

---

## 4. Standing decisions. Do not relitigate these.

| Date | Decision |
|---|---|
| 2026-09-19 | **`Bioleaching Modelling - Summary.docx` is the current authority for Parts I and II.** Where it disagrees with a row below, it wins and the row is marked superseded. It is the source for `docs/WIKI_MODEL_UPDATE.md` Stages 1 and 2 |
| 2026-08-19 | ~~**The ligand is glycine, not ammonia.** Ammonia is volatile and the air pump would strip it. ISSUES 54~~ **Superseded 2026-09-19.** The bioleaching summary models 260 mM ammonia and reports 36.6 % gold leached in 24 h against 19.69 % with no ammonia. The volatility objection is not retracted and is not yet answered by that document |
| 2026-08-19 | **Superseded 2026-09-19.** The Cu(II) constants are no longer ammonia-free only. The bioleaching summary carries both branches: `k_Au,Cu` = 21.0 ammonia-free or 1500 with ammonia, `k_1`/`k_3` = 1.20e-5 ammonia-free or 1e-5 with ammonia. They still move together within a branch |
| 2026-08-19 | `K_S2O3` = 3376, the **geometric** mean of the measured `K_ads` band, superseding the 3900 below |
| 2026-08-19 | **pH is an input, not an output.** The team has a dosing pump, so the model reports titrant demand. `pH_control` |
| 2026-08-19 | The pH window is **9.3 to 10.5**, set point 10.0 to 10.3. Gold is flat over it; the window is about lixiviant survival |
| 2026-08-19 | Every 2026-08-19 structural change is a **switch, false by default**. Nothing already reported moved |
| 2026-08-12 | **Part I is the three-vessel sequential process.** The one-pot model is retired and no longer implemented. ISSUES 36 |
| 2026-08-12 | `K_S2O3` = 3900, sourced, beat this repository's own 5e4 placeholder. ISSUES 42 |
| 2026-08-12 | The proton balance tracks **alkalinity, never free `[H+]`**. ISSUES 37 |
| 2026-08-12 | Part I's five null rate constants adopted from his models. ISSUES 8, 20 |
| 2026-08-12 | `t_film` = 0.5 µm is a **team assumption**, not a spec. Mixed e-waste has no supplier. ISSUES 19 |
| 2026-08-11 | ***E. coli* is the organism in all three parts**, and it makes the thiosulfate itself |
| 2026-08-11 | `Vmax` comes from `k_cat × [TetH]`, not from a growth yield. ISSUES 30 |
| 2026-08-10 | **Part II is the authority for every protein-model quantity.** `q_max` = 0.0913, `μ` = 1.2 h⁻¹. The value was 0.0108 until 2026-08-19; the authority rule is what did not change |
| 2026-08-20 | **A joint value must be recomputed, not copied.** Anything Part II supplies downstream carries a test that recomputes it through `src/interfaces.py`. ISSUES 62 |
| 2026-08-20 | **Reduction is fixed by seeding, not by more protein.** `seeding_on` defaults false and `seed_frac` is null. A 1 % seed cuts the concentration factor from 10× to 4×. ISSUES 64 |
| 2026-08-20 | **Every test helper reads the YAML.** A parameter is not centralised until every caller reads it. `test_sensitivity.py` held `Rech_0` = 100 against a file that said 4.6, and it produced every published reduction number. ISSUES 65 |
| 2026-08-11 | 🔴 **TetH does not fold actively in *E. coli*.** Part I's enzyme block is unvalidated. ISSUES 32 |
| 2026-08-11 | `cells_per_g` = 2.36e12, interpolated at our own `μ`. ISSUES 33 |
| 2026-09-18 | `K_Au` = **0.7 µM**, the closest fitted GolB-based literature proxy, supersedes the unsourced 0.1 µM. `K_Cu` remains unmeasured; `alpha` = 52 is a labelled GolS-derived design scenario only. ISSUES 1, 22; S78, S79 |
| 2026-08-10 | `K_Au` deliberately **not** adopted from Part II; the 0.1 µM proxy was kept instead of Part II's 10 µM placeholder. Superseded 2026-09-18. ISSUES 1 |
| 2026-08-10 | Leaching stoichiometry applied per pathway, not to lumped rates. ISSUES 18 |
| 2026-08-09 | Solid inventories in µmol, never mol. ISSUES 4 |

**Any `eta_total` from before 2026-08-10 used `q_max` = 4.4 and is too high by
about two orders of magnitude.**

---

## 5. Naming rules, in force since 2026-08-11

- **Upper case Latin is per litre. Lower case is per cell.** `X` is cells or
  grams per litre; `s` is sites per cell; `a_Au` is an area.
- **`k` is always a rate constant, named by what it does.** Never numbered.
  `k_par`, `k_nuc`, `k_elute`, `k_ox_Cu`.
- **`K` is always a concentration, named by its species.** `K_S4O6`, `K_S2O3`,
  `K_CuII`, `K_Au`, `K_inh`.

`docs/EQUATIONS.md` carries the symbol table. **The source documents keep
their original symbols**, so `ISSUES.md` item 25 is how you read them side by
side.

---

## 6. How to reconcile something

This is the core workflow. Follow it in order.

**Step 1. Find where the two parts actually touch.** Not where they use the
same word. `ISSUES.md` item 29 has the full integration table: every quantity,
what each part calls it, and whether it is reconciled.

**Step 2. Check the units before the values.** Part I and II use minutes,
Part III uses hours. µmol/L and µM are the same unit. A rate constant crossing
a joint without conversion is wrong by 60×. Only quantities with a time
dimension convert; `K`-type constants never do.

**Step 3. Ask which document has the better claim**, and say why in writing.
The usual grounds, in order:

1. A measurement beats a derivation.
2. A derivation beats an assumption.
3. A stated placeholder loses to anything else, even a proxy.
4. A physical ceiling beats any value that exceeds it.

Item 2 is the worked example: Part III's `q_max` = 4.4 lost to Part II's
0.0108 because 4.4 needed 742,225 anchor points on a cell that has 100,000.
Part II's own value has since moved to 0.0913, which does not disturb the
ranking — the derivation still beat the assumption, and by less.

**Step 4. Recompute everything downstream.** A joint value never moves alone.
When `q_max` changed, the capacity ceiling, the operating window, `eta_capture`
and `eta_total` all moved, and one PRCC ranking flipped from insensitive to a
2.6× lever — then flipped back when `q_max` moved again. Search for the old
number before you assume nothing else used it.

⚠ **Search the generated files too.** `docs/_review_parameters.md` and every
figure in `docs/media/review/` are built from the YAML. On 2026-08-19 a joint
value was updated in three parameter files and not the fourth, and the built
report stated both values — the new one in its body, the old one in its
appendix and in the figure printed above that body. ISSUES 62.

**Step 5. Write the decision into the YAML, not only into prose.**

```yaml
q_max:
  value: 0.0913
  status: adopted_from_part_II
  superseded_2026_08_19:
    value: 0.0108
    reason: >-
      Part II's cascade at N = 20, before the pUC backbone was confirmed.
  superseded:
    value: 4.4
    reason: >-
      Needed 742,225 sites on a cell with 100,000 anchors.
```

**Step 6. Add a test that fails if someone reverses it.** Name it after the
decision, not after the function.
`test_K_Au_uses_closest_GolB_literature_proxy`.

**Step 7. If the value crosses a joint, recompute it in the test rather than
pinning it.** A test that asserts `q_max == 0.0108` passes happily after the
upstream model has moved; a test that recomputes `q_max` from
`params/expression.yaml` through `src/interfaces.py` does not. Three tests
pinned the stale number on 2026-08-19 and all three passed.
`test_qmax_is_part_II_pushed_through_joint_2` is the pattern. ISSUES 62.

**Step 7. Update `ISSUES.md`, `MASTER.md` and `EQUATIONS.md`** in that order,
then the notebook. Change the Open/Closed tables at the top of `ISSUES.md`.

**Step 8. Run the full verification below.** All four checks, every time.

---

## 7. Verification. Run all five.

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
python docs/check_docs.py
```

*Links, tier declarations, and whether a generated file has been
hand-edited. Add `--regen` to rebuild the .docx and compare. Section 11
says what the tiers are.*

Then grep the documents for the symbol or number you changed, and confirm the
only remaining hits are inside the intentional was/now table in
`docs/EQUATIONS.md`.

---

## 8. Traps that have already cost time

**Chained regex substitutions cascade.** Replacing `K_S` with `K_{S_2O_3}` and
then `K_S` again matches inside the first replacement. `EQUATIONS.md` reached
1.4 MB this way. **Use one simultaneous alternation pass, never a sequence.**

**YAML reads `3.57e12` as a string.** Write `3.57e+12`. The `+` is required.

**A terminal event that is zero at `t=0` fires immediately** and `solve_ivp`
returns a single point. `simulate()` only attaches an exhaustion event when
that inventory starts positive.

**Two symbols can rename to the same target.** `k1` and `k3` both became
`k_par`, which produced `SyntaxError: keyword argument repeated`. That was the
intended chemistry; the duplicate call sites had to go.

**A "sensitivity" result is conditional on the operating point.** Every PRCC in
Part III §8 was computed at the retired `q_max`. Do not quote them. ISSUES 27.

---

## 9. What is open right now

Top five by cost, from `docs/ISSUES.md`. Updated 2026-08-12.

| # | Item | Blocked on |
|---|---|---|
| 41 | Cu(I) re-oxidation decides the process; oxygen optimum is 6× below baseline | nothing. Act on it |
| 19 | Gold leaching goes as 1/`t_film`, range spans 20×. A joint largest lever | assumed 0.5 µm 2026-08-12; measure it on the real feed |
| 39 | Joint 1 delivers 39 µM; Part III collapses above 30 µM | team, with item 21 |
| 38 | The conversion vessel wants pH 3, thiosulfate dies below pH 4 | wet lab |
| 23 | Leach chemistry published only at pH 9–10.5 | team |

**Cheapest high-value experiment on the board:** run the leach at two oxygen
levels. Item 41.

**Deferred by the team on 2026-08-11:** temperature, and the V1 to V2 vessel
transfer. Do not start these.

**Do not sweep a geometry parameter without calling `leach.refresh`.** `m_Au`,
`m_Cu`, `rho_Au`, `rho_Cu`, `t_film` and `d` all feed the areas and the
starting inventories. Change one without refreshing and every crush size gives
the same answer. `simulate_sequential` and `simulate_stage3` refresh on entry;
`simulate` does not. This has already caught two people.

---

## 10. Tone for written output

The documents are read by wet-lab teammates, not modellers.

- Name every symbol in words before using it in an equation.
- Every number carries its unit, every time.
- State a disagreement and name the `ISSUES.md` item. Do not silently pick a
  side.
- Report failures with the real output. Never summarise a failing test as
  "mostly working".
- No em dashes in `docs/SUPERVISOR_BRIEF.md`. **This governs new text only.**
  That file is Tier 2, a record, and section 11 forbids rewriting one, so the
  em dashes already in the sent portion stay where they are. The two rules met
  on 2026-08-20 and this is how they were reconciled.
---

## 11. What each document is for

Added 2026-08-20. Every markdown file in this repository sits in one of four
tiers, and the tier decides what may be done to it.

| Tier | Files | Rule |
|---|---|---|
| **1 Source** | `docs/source/`, `docs/00_*`, `docs/01_*`, `docs/02_*`, `docs/MODEL.md`, `docs/_frontmatter.md` | **Never edited.** Verbatim transcriptions. An error found here is logged in `ISSUES.md` and left standing in the text. |
| **2 Record** | `docs/ISSUES.md`, `docs/SOURCES.md`, `docs/SUPERVISOR_BRIEF.md` | **Append and supersede, never rewrite.** A closed item keeps its original arithmetic; a correction goes in a dated banner above it. |
| **3 Synthesis** | `README.md`, `STRUCTURE.md`, `AGENTS.md`, `CLAUDE.md`, `docs/MASTER.md`, `docs/EQUATIONS.md`, `docs/REVIEW.md`, `docs/RECOVERY.md`, `docs/RECOVERY_MODEL.md`, `docs/CAPTURE_INVESTIGATION.md`, `docs/COMPETITION.md`, `docs/WIKI_*.md` | **Rewritten as the model moves.** Every number must match the code today. A stale number here is a defect, not history. |
| **4 Generated** | `docs/_REVIEW_build.md`, `docs/_review_parameters.md`, `docs/REVIEW.docx`, `docs/media/review/*`, `docs/_RECOVERY_build.md`, `docs/RECOVERY.docx`, `docs/media/recovery/*`, `docs/_RECOVERY_MODEL_build.md`, `docs/RECOVERY_MODEL.docx`, `docs/media/recovery_model/*`, `docs/_BIORECOVERY_build.md`, `docs/BIORECOVERY.docx`, `docs/media/biorecovery/*` | **Never hand-edited.** Regenerate review files with `python docs/build_review.py`, recovery-review files with `python docs/build_recovery.py --figures`, the technical recovery model with `python docs/build_recovery_model.py --figures`, and the biorecovery wiki document with `python docs/build_biorecovery.py --figures`. An edit here is overwritten without warning. |

### The seven rules

1. **Open by saying what the file is.** Purpose, who reads it, and what it is
   not. Tier 4 files also carry the warning in their own first lines, because
   hand-editing a generated file is a mistake that has been made. **Tier 1
   files carry no marker at all** — adding one would be editing them, which is
   the thing the tier forbids. Their tier is declared in `STRUCTURE.md` and in
   the table above, and nowhere else.
2. **One fact, one home.** Numbers live in `params/*.yaml`. Rules live in this
   file. Everything else points rather than restating.
3. **Every number is traceable** to an `ISSUES.md` item, a named test, or an
   `[Sxx]` entry in `SOURCES.md`.
4. **Cross-references are markdown links and they resolve.**
5. **Nothing aspirational.** No file describes code, data or infrastructure
   that does not exist. `README.md` described a React frontend and a PostgreSQL
   database for months; neither was ever written.
6. **A date says what the file was true of.** A Tier 3 file must not carry a
   date older than its last substantive change.
7. **Write for the wet lab**, per section 10.

### How they talk to each other

`README.md` is the front door and holds no detail; it points to `STRUCTURE.md`
for the layout, to this file for the rules, and to `docs/REVIEW.md` for the
results. `docs/MASTER.md` walks the chain in prose, `docs/EQUATIONS.md` carries
the mathematics for the same chain, and `docs/REVIEW.md` is the deliverable
built from both. All three cite `ISSUES.md` and `SOURCES.md`; neither of those
two cites back, because a record does not depend on a synthesis. The wiki files
run one way only: `WIKI_DESIGN` sets the rubric, `WIKI_PLAN` commits a layout,
`WIKI_CONTENT` writes the copy.

**The check:** `python docs/build_review.py` regenerates every Tier 4 file. If
a Tier 3 number and a Tier 4 number disagree afterwards, the Tier 3 file is
wrong. That failure is `ISSUES.md` item 62 and it is why this section exists.

---

## 12. Wiki Model presentation and dropdowns

Added 2026-09-19. These are the governing presentation rules for every Model
page and Model section on the iGEM wiki. They apply to the public page, its
source components and the `docs/WIKI_*.md` drafts. Scientific traceability and
the document-tier rules above still apply.

The 2026 Best Model ballot asks four questions:

1. How impressive is the modelling or computational approach?
2. Did the model help the team understand, predict or design a part, device or
   system?
3. Did experimental or other relevant data develop, train or validate it?
4. Is the work a good example for another team to reuse?

The Best Wiki criterion adds a presentation requirement: the design must help
visitors find and understand the content. **Dropdowns provide depth; they never
hide the answer to any of the four ballot questions.**

### What must remain visible

1. Put one plain-language answer to each ballot question in visible text above
   the fold of the relevant section.
2. State the assumptions, parameters with units and sources, and the origin of
   the data. Distinguish literature values from this team's measurements.
3. Show the design decision the model changed. Name the parameter, the
   prediction and the resulting lab action.
4. Show validation by placing model output against the relevant data and
   reporting the mismatch honestly. If project data do not yet exist, say
   explicitly that the model is not experimentally validated; never imply that
   verification or a literature proxy is project validation.
5. Publish the code and a reproducible method so another team can rerun the
   work. Model content and required assets must live on the iGEM wiki and its
   repository, not only on an external host or CDN.
6. Make each section's headline result a visible figure plus one sentence.
   Dropdowns may hold the detailed method, never the result or its project
   consequence.

### What may be collapsed

Use a dropdown only for supporting depth: full derivations, complete parameter
tables, solver settings, extra plots and failed variants. Label it with the
content, such as **Full ODE derivation (6 equations)**, never with an action
such as **Read more**. The closed label must remain informative enough to tell
a scanning reader what evidence is available.

Do not nest dropdowns. Do not open a page with a wall of closed accordions or
without a visible narrative. Implement dropdowns with semantic
`<details>`/`<summary>` elements or a React state control that keeps the content
in the DOM. Text must remain selectable and printable, and deep links must
continue to work.

### Prohibited presentation

- Do not hide a ballot-question answer in collapsed content.
- Do not present a model without stating its data basis, validation status and
  effect on the wet lab or process design.
- Do not fabricate a parameter, fit or citation. Every number follows the
  provenance rules in sections 1, 6 and 11.
- Do not use dropdowns to compensate for missing chronology. The visible text
  must first explain the current process, why it was modelled, what the model
  showed and what changed.

**Removal test:** if removing every dropdown leaves a complete, defensible
Model page that answers all four ballot questions, the structure is correct.

Criteria references: [2026 Special Awards](https://competition.igem.org/judging/special-prizes),
[2026 example Model page](https://2026.igem.wiki/example/model) and
[2026 Medals](https://competition.igem.org/judging/medals).
