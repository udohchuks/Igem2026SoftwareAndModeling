# Working in this repository

**Tier 3, synthesis. This file is the only home for rules.** If a rule belongs
to the project it goes here, so that no two files can drift apart on it.

This is the iGEM 2026 gold-biorecovery model behind the Ashesi Ghana wiki
Model page (https://2026.igem.wiki/ashesighana/). The wiki source lives in a
separate repository, `ashesighana`. This repository holds the model code, its
parameters, and the drafts and figures the wiki is built from.

Read this file before changing anything. `CLAUDE.md` points here.

Rewritten 2026-10-16, when everything the current wiki does not use moved to
`archive/`. The previous version is `archive/rules_2026-10-16/AGENTS.md`.

---

## 0. The archive. Do not look in it.

`archive/` holds retired files at the same paths they had before
2026-10-16. `archive/MANIFEST.txt` lists them.

- **Do not read, search, cite or edit anything in `archive/` unless the user
  asks for it by name.** The `.ignore` file at the root makes the search tools
  skip it.
- Do not move a file back out of `archive/` without being asked.
- **The current wiki decides what lives outside the archive.** A file that no
  wiki content, wiki figure or wiki build depends on belongs in `archive/`.

---

## 1. The rules. Do not break these.

1. **Never edit a source document.** `docs/source/` is verbatim. An error
   found there is recorded in `docs/ISSUES.md` and **left standing in the
   text**. Only its author corrects it.
2. **No number in a `.py` file.** Every value lives in `params/*.yaml` with its
   unit, status and source. `src/params.py` loads them.
3. **A parameter with no value stays `null`.** Loading it must raise
   `KeyError`, never substitute a guess.
4. **Discrepancies get a test, not a silent fix.** Where two sources
   disagree, a test pins the disagreement so a later edit cannot hide it.
5. **Do not delete the record.** Superseded values move to a `superseded:` or
   `retired_*:` block in the same YAML file, with the reason.
6. **Do not edit `docs/WIKI_BIORECOVERY_DRAFT.md`.** It is the author's text.
   Propose wording and wait. Section 7 has the rest.

---

## 2. What is where

```
src/                  the model. Every module is in use; they import each other
params/*.yaml         every number, with unit, status and source
tests/                one test file per module

docs/WIKI_MODEL_UPDATE.md        wiki stages 1 and 2: make thiosulfate, leach
docs/WIKI_BIORECOVERY_DRAFT.md   wiki stages 3 to 5: capture, release, reduce
docs/CAPTURE_DESIGN.md           stage 3 rework: design analyses for scale-up
docs/capture_design_analysis.py  the stage 3 design questions, Q1 onward
docs/WIKI_EQUATIONS.md           the equations the live wiki shows, stage 3 down
docs/ISSUES.md        findings record; params cite its item numbers
docs/SOURCES.md       papers, each tied to the number it supplies ([Sxx])
docs/EQUATIONS.md     equation notation; params cite it
docs/source/          verbatim source documents; params cite them

docs/make_wiki_leaching_figures.py   wiki plots in docs/media/wiki/plots/
docs/make_leach_budget.py            docs/media/wiki/concepts/leaching-budget.svg
docs/make_biorecovery_figures.py     docs/media/biorecovery/
docs/build_biorecovery.py            docs/BIORECOVERY.docx from the draft
docs/make_software_data.py           the wiki Software page data, from
                                     dashboard-prototype/*.yaml
dashboard-prototype/  the measurement console the Software page describes
```

The wiki's process overview art comes from
`docs/media/wiki/concepts/overview-stage-*-approved.png`.

---

## 3. The chain

```
1 make thiosulfate ─► 2 leach PCB ─► 3 capture ─► 4 release ─► 5 reduce
     src/leach.py                    src/capture_design.py, capture_kinetics.py,
                                     competition.py, recovery_*.py, reduction.py,
                                     reductase.py
```

Stages hand over **amounts (µmol), not concentrations**. The joints and their
unit checks are in `src/interfaces.py`.

**Open conflict.** Capture is 73.10 % from `q_Au` = 4.62 µmol/g in
`params/capture_design.yaml`, and 1.54 % from `q_max` = 0.0913 µmol/g in
`params/recovery_chain.yaml`. The team is resolving it in the model. Do not
pick a side, and do not put either number into new wiki text until the edited
model gives one value.

**Resolved for the stage 3 rework, 2026-10-17.** The stage 3 owner chose
`q_Au` = 4.62 µmol/g (S76) for `docs/CAPTURE_DESIGN.md` and
`docs/capture_design_analysis.py`. The old figures and
`params/recovery_chain.yaml` still carry 0.0913; align them when the model is
edited.

---

## 4. Standing decisions. Do not relitigate these.

| Date | Decision |
|---|---|
| 2026-10-17 | **One dip is second order in both pools.** Q3 of `CAPTURE_DESIGN.md` uses `dx/dt = k_on(a0-x)(s0-x)`, not first-order decay. Neither the gold nor the sites is in excess, so the dip time depends on both, and it peaks where they match |
| 2026-10-17 | **`dip_time_h` is 1.0 h, a design choice set by Q3**, not a measurement. One fixed dip time covers every dip of a batch. A cycle is therefore 7 h, so three fit in a day, not four |
| 2026-10-17 | **Stage 3 work is Python, not MATLAB.** The author asked for Python on 2026-10-17; `matlab/capture_design.m` was ported to `docs/capture_design_analysis.py` and removed, so there is one implementation |
| 2026-10-17 | **Stage 3 uses GolB's own measured constants directly, and no selectivity ratio.** S76 reports `K_d(Au(I))` = 3.02e-37 M and `K_d(Cu(I))` = 1.61e-17 M on GolB itself. Used as they stand they make binding stoichiometric: gold takes every site it needs and copper takes the rest, so the design loading is one site per gold atom and copper never reduces gold capture. This supersedes `K_Au` = 0.7 µM (S78) and the GolS `alpha` = 52 **for stage 3 only**; the recovery chain still uses 0.7 µM. The constants are bare-ion values, so the result is an **upper bound** in thiosulfate leachate. The thiosulfate-corrected band is retired. ISSUES 93 |
| 2026-10-17 | **Stage 3 uses `q_Au` = 4.62 µmol/g, from S76** (whole-cell displayed GolB in *E. coli*). Decided by the stage 3 owner. No sweep over other loadings |
| 2026-10-16 | **Plant basis is 1 tonne of PCB a day.** Analyse each stage on the 1 L bench basis in `params/leach.yaml` (`feed_basis`), report at 1 t/day. Stage values are checked against literature and computation |
| 2026-09-19 | **`Bioleaching Modelling - Summary.docx` is the current authority for stages 1 and 2.** It is the source for `docs/WIKI_MODEL_UPDATE.md`. It models 260 mM ammonia: 36.6 % gold leached in 24 h, against 19.69 % with no ammonia. Ammonia volatility is not yet answered |
| 2026-09-19 | The Cu(II) constants carry two branches: `k_Au,Cu` = 21.0 ammonia-free or 1500 with ammonia; `k_1`/`k_3` = 1.20e-5 ammonia-free or 1e-5 with ammonia. They move together within a branch |
| 2026-09-18 | `K_Au` = **0.7 µM**, the closest fitted GolB literature proxy. `K_Cu` is unmeasured; `alpha` = 52 is a labelled GolS-derived design scenario only. ISSUES 1, 22; S78, S79 |
| 2026-08-20 | **A joint value must be recomputed, not copied.** A value passed downstream carries a test that recomputes it through `src/interfaces.py`. ISSUES 62 |
| 2026-08-20 | **Reduction is fixed by seeding, not by more protein.** `seeding_on` defaults false. ISSUES 64 |
| 2026-08-20 | **Every test helper reads the YAML.** ISSUES 65 |
| 2026-08-19 | `K_S2O3` = 3376, the geometric mean of the measured `K_ads` band |
| 2026-08-19 | **pH is an input, not an output.** The dosing pump holds 9.3 to 10.5, set point 10.0 to 10.3; the model reports titrant demand |
| 2026-08-12 | **Stages 1 and 2 are the three-vessel sequential process.** The one-pot model is retired. ISSUES 36 |
| 2026-08-12 | The proton balance tracks **alkalinity, never free `[H+]`**. ISSUES 37 |
| 2026-08-12 | `t_film` = 0.5 µm is a **team assumption**, not a spec. ISSUES 19 |
| 2026-08-11 | ***E. coli* is the organism in every stage**, and it makes the thiosulfate itself. `Vmax` = `k_cat × [TetH]`. ISSUES 30 |
| 2026-08-11 | 🔴 **TetH does not fold actively in *E. coli*.** The enzyme block is unvalidated. ISSUES 32 |
| 2026-08-11 | `cells_per_g` = 2.36e12, interpolated at our own `μ`. ISSUES 33 |
| 2026-08-11 | **Deferred by the team: temperature, and the V1 to V2 vessel transfer.** Do not start these |
| 2026-08-09 | Solid inventories in µmol, never mol. ISSUES 4 |

---

## 5. Naming

- **Upper case Latin is per litre. Lower case is per cell.** `X` is cells or
  grams per litre; `s` is sites per cell.
- **`k` is always a rate constant, named by what it does.** Never numbered:
  `k_elute`, `k_ox_Cu`.
- **`K` is always a concentration, named by its species:** `K_S2O3`, `K_Au`.
- The source documents keep their original symbols.

---

## 6. Changing a value

1. **Check the units first.** Stages 1 and 2 use minutes; stages 3 to 5 use
   hours. A rate constant crossing a joint without conversion is wrong by 60×.
   `K`-type constants never convert.
2. **Decide which source has the better claim, in writing.** A measurement
   beats a derivation; a derivation beats an assumption; a placeholder loses to
   anything, even a proxy; a physical ceiling beats any value above it.
3. **Write the decision into the YAML**, with the old value in a
   `superseded:` block and its reason.
4. **Add a test that fails if someone reverses it.** Name it after the
   decision. If the value crosses a joint, recompute it in the test rather than
   pinning it.
5. **Recompute downstream and search for the old number** in `src/`,
   `params/`, `tests/`, the two wiki drafts and the generated figures.
6. **Regenerate the wiki figures** the value feeds (section 2).
7. **Run the checks** in section 8.

---

## 7. The wiki drafts and figures

- `docs/WIKI_BIORECOVERY_DRAFT.md` is ahead of the rest of the repository.
  Treat it as the current statement of stages 3 to 5. A disagreement with
  another file means the other file is stale. **Do not edit it** (rule 6).
  Add figure calls and captions only when asked, and log errors in
  `docs/ISSUES.md`.
- Draft figures come from `params/capture_design.yaml` and are written to
  `docs/media/biorecovery/` by `docs/make_biorecovery_figures.py`.
- Build the document with `python docs/build_biorecovery.py --figures`. Never
  hand-edit `docs/_BIORECOVERY_build.md`, `docs/BIORECOVERY.docx` or
  `docs/media/biorecovery/*`; they are regenerated.
- `docs/media/wiki/` holds the figures the wiki copies. Regenerate them with
  their scripts; never hand-edit them.

---

## 8. Verification. Run all three.

```bash
python -m pytest tests -q
```

```bash
python -c "import yaml,io,glob; [yaml.safe_load(io.open(f,encoding='utf-8')) for f in glob.glob('params/*.yaml')]; print('yaml ok')"
```

```bash
python docs/check_docs.py
```

Then grep `src/`, `params/`, `tests/` and the two wiki drafts for the symbol
or number you changed. Report the real output. If a check fails, say which and
paste it.

---

## 9. Traps that have already cost time

- **Chained regex substitutions cascade.** Use one simultaneous alternation
  pass, never a sequence.
- **YAML reads `3.57e12` as a string.** Write `3.57e+12`.
- **A terminal event that is zero at `t=0` fires immediately** and `solve_ivp`
  returns one point.
- **A sensitivity result is conditional on the operating point.** Do not quote
  a PRCC computed at a retired value.
- **Do not sweep a geometry parameter without calling `leach.refresh`.**
  `simulate_sequential` and `simulate_stage3` refresh on entry; `simulate`
  does not.

---

## 10. Tone for written output

The documents are read by wet-lab teammates, not modellers.

- Name every symbol in words before using it in an equation.
- Every number carries its unit.
- State a disagreement and name the `ISSUES.md` item. Do not silently pick a
  side.
- Report failures with the real output.

---

## 11. Document tiers

| Tier | Files | Rule |
|---|---|---|
| **1 Source** | `docs/source/` | **Never edited.** |
| **2 Record** | `docs/ISSUES.md`, `docs/SOURCES.md` | **Append and supersede, never rewrite.** A correction goes in a dated banner. |
| **3 Synthesis** | `README.md`, `STRUCTURE.md`, `AGENTS.md`, `CLAUDE.md`, `docs/EQUATIONS.md`, `docs/WIKI_MODEL_UPDATE.md`, `docs/WIKI_BIORECOVERY_DRAFT.md`, `docs/CAPTURE_DESIGN.md`, `docs/WIKI_EQUATIONS.md` | **Rewritten as the model moves**, except the biorecovery draft (rule 6). A stale number is a defect. |
| **4 Generated** | `docs/_BIORECOVERY_build.md`, `docs/BIORECOVERY.docx`, `docs/media/biorecovery/*`, `docs/media/wiki/plots/*`, `docs/media/wiki/concepts/leaching-budget.svg` | **Never hand-edited.** Regenerate with the script in section 2. |

Every Tier 3 and Tier 4 markdown file says its tier in its opening lines.
Numbers live in `params/*.yaml`; documents point to them rather than restate
them. Every number traces to an `ISSUES.md` item, a named test or an `[Sxx]`
entry. Nothing describes code or data that does not exist.

---

## 12. Wiki Model presentation and dropdowns

These rules govern every Model page and Model section on the wiki, its source
components and the `docs/WIKI_*.md` drafts.

The 2026 Best Model ballot asks four questions:

1. How impressive is the modelling or computational approach?
2. Did the model help the team understand, predict or design a part, device or
   system?
3. Did experimental or other relevant data develop, train or validate it?
4. Is the work a good example for another team to reuse?

**Dropdowns provide depth; they never hide the answer to a ballot question.**

### What must remain visible

1. One plain-language answer to each ballot question, in visible text near
   the top of the relevant section.
2. The assumptions, parameters with units and sources, and the origin of the
   data. Literature values are distinguished from this team's measurements.
3. The design decision the model changed: the parameter, the prediction and
   the resulting lab or process action.
4. Validation: model output against the relevant data, with the mismatch
   reported honestly. If project data do not exist, say the model is not
   experimentally validated; never present a literature proxy as project
   validation.
5. The code and a reproducible method, hosted on the iGEM wiki and its
   repository.
6. Each section's headline result as a visible figure plus one sentence.

### What may be collapsed

Full derivations, complete parameter tables, solver settings, extra plots and
failed variants. Label a dropdown with its content, such as **Full ODE
derivation (6 equations)**, never **Read more**. Do not nest dropdowns. Use
`<details>`/`<summary>` or a React control that keeps the content in the DOM.

**Removal test:** if removing every dropdown leaves a complete, defensible
Model page that answers all four ballot questions, the structure is correct.

Criteria: [2026 Special Awards](https://competition.igem.org/judging/special-prizes),
[2026 example Model page](https://2026.igem.wiki/example/model),
[2026 Medals](https://competition.igem.org/judging/medals).
