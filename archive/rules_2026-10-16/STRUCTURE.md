# Repository structure

Three modelling documents, one process chain, one notebook. Updated 2026-09-07.

**Tier 3, synthesis.** This file is the layout and nothing else: one line per
file, kept in step with what is on disk. What each document is *for*, and what
may be done to it, is `AGENTS.md` section 11. The rules themselves are
`AGENTS.md`.

**Agents: read [AGENTS.md](AGENTS.md) before changing anything.**

```
README.md                   the front door. Points everywhere else, holds
                            no detail of its own
model.ipynb                 the notebook — narrative and every figure
AGENTS.md                   how to navigate and how to reconcile. Read first.
                            Section 11 says what each document is for
CLAUDE.md                   Claude Code notes; points at AGENTS.md
STRUCTURE.md                this file
requirements.txt            six packages; no database and no web service
prcc_results.json           the PRCC run behind MASTER.md. Its sampling ranges
                            are not tracked, so it cannot be reproduced from
                            the repository as it stands. ISSUES 63

docs/
  REVIEW.md                 THE DELIVERABLE. The model, its figures, and the
                            decisions the team must confirm. Built to .docx by
                            build_review.py
  MASTER.md                 the end-to-end model in plain language, complete
  EQUATIONS.md              every equation, one line of English each
  ISSUES.md                 65 findings; 32 and 44 BLOCKING, 41 the free win
  SOURCES.md                41 papers we found, and the number each supplies
  SUPERVISOR_BRIEF.md       short progress note
  MODEL.md                  all three documents in one file, verbatim
  MODEL.docx                the same, with a table of contents and figures
  WIKI_SURVEY.md            26 team wikis read live, 2013-2025, and what each
                            one does. Feeds WIKI_DESIGN.md; carries no numbers
  WIKI_DESIGN.md            the rubric and the survey for the wiki pages
  WIKI_PLAN.md              the layout those commit to
  WIKI_CONTENT.md           the copy itself. Read the three in that order
  WIKI_FLOW_NOTES.md        agreed stage order, repeated model-section rhythm
                            and visual-production workflow
  WIKI_REFERENCE_NOTES.md   selected external-wiki lessons for the writing team
  WIKI_ISSUES.md            concise source-document issues organised by wiki
                            stage; full evidence remains in ISSUES.md
  build_review.py           regenerates figures, appendix and REVIEW.docx
  make_review_figures.py    every figure in REVIEW.docx, from params/ and src/
  make_review_tables.py     Appendix A, from params/*.yaml
  check_docs.py             enforces AGENTS.md section 11: links, tiers, and
                            whether a generated file was hand-edited
  _frontmatter.md           the chain map and joint definitions
  _review_parameters.md     GENERATED — Appendix A. Do not hand-edit
  _REVIEW_build.md          GENERATED — REVIEW.md with the appendix spliced in.
                            Gitignored. Do not hand-edit
  media/review/             GENERATED — every figure in REVIEW.docx
  00_overview_gold_biorecovery.md    Part III, verbatim
  01_bioleaching.md                  Part I,  verbatim
  02_golb_expression.md              Part II, verbatim
  media/                    figures extracted from the Part II document
  source/                   untouched originals (2 .docx + 1 .md)
    sequential_2026-08-12/  Part I as delivered 2026-08-12. See its README:
                            the three-vessel write-up and MATLAB are in use,
                            the one-pot pair is retired but kept

src/
  params.py                 loads params/*.yaml; lists unsourced parameters
  leach.py                  Part I   — the three-vessel sequential process
  expression.py             Part II  — implemented
  recovery_chain.py         Part III — closed forms only; ODE code is a shim.
                            Elution is Ho-McKay pseudo-second-order, eta_elute.
                            The superseded Lagergren first-order law is kept as
                            eta_elute_pfo. ISSUES 47.
  interfaces.py             the two joints, with unit checks
  sensitivity.py            Latin hypercube, PRCC, Finke-Watzky reduction
  reductase.py              Arm B — growing the reductase in E. coli and when
                            to lyse. Part II's cascade with k_sec = 0, coupled
                            to logistic growth. ISSUES 52.

params/
  leach.yaml                Part I parameter table, transcribed
  expression.yaml           Part II parameter table, transcribed
  recovery_chain.yaml       Part III parameter table, transcribed
  conversions.yaml          constants needed by the joints, not from the docs

tests/
  test_expression.py        reproduces every number Part II prints
  test_leach.py             conservation, geometry, limit checks, and every
                            number Part I's sequential model reports
  test_interfaces.py        unit handling, and the numbers the joints produce
  test_sensitivity.py       the recomputed PRCC, the reduction threshold, the
                            electron ceiling, and seeding. ISSUES 64, 65
  test_reductase.py         harvest timing, and the 2.5x protein shortfall
```

## Rules that keep this iterable

1. **No number in a `.py` file.** Every value lives in `params/*.yaml` with its
   unit, its status, and its source attached. `src/params.py` loads them.
2. **No equation in the notebook.** Equations live in `src/`. The notebook
   imports and plots. If you write a `def` in a cell, move it.
3. **A parameter with no value stays `null`.** Loading it raises a `KeyError`
   rather than substituting a guess. `model.md` §0 records that every parameter
   assumed without a source, then sourced, turned out to be wrong.
4. **Discrepancies get a test, not a fix.** Where the documents disagree, a
   test pins the disagreement so a later edit cannot hide it. See
   `docs/ISSUES.md`.
5. **The source documents are never edited.** Corrections are proposed in
   `docs/ISSUES.md` and applied by their authors.

## Setup

```
pip install -r requirements.txt
python -m pytest tests -q          # 85 tests
jupyter lab model.ipynb
```

## Recovery review, 2026-09-06

[RECOVERY.md](docs/RECOVERY.md) is the Tier 3 technical recovery review;
[WIKI_RECOVERY.md](docs/WIKI_RECOVERY.md) is the Tier 3 recovery-only wiki draft.
`src/recovery_audit.py` loads the report scenario and recomputes Joint 2.
`params/recovery_audit.yaml` supplies its scenario and verification settings.
`docs/make_recovery_figures.py` generates the current recovery figures and
`docs/media/recovery/audit_results.json`; these are Tier 4 and never edited by
hand. `docs/build_recovery.py --figures` builds the recovery deliverable.
Historical unreferenced recovery images are retained as a record, not current
figures. The review describes why previous harvest and certainty claims changed.

## Historical integration note

The note below predates the current implementation in `src/sensitivity.py`.
The three-stage chain now runs there; the stub exports in `recovery_chain.py`
remain compatibility placeholders.

## To complete Part III

`src/recovery_chain.py` is a shim. `model.md` names three existing files as the
working code for that part: `pipeline_model.py`, `r9L_fw.py`, `ensemble.py`.
Copy them into `src/`, then re-export their entry points as described in the
module docstring. They were not re-implemented here because `model.md` §2 and
§4.1 record verification checks that already pass against them, and a second
version would drift from the first.

Once they are in place, extend `ensemble.py` to sample across all three parts.
The current 90% CI on `eta_total`, [0.0%, 49.4%], excludes leaching and
expression uncertainty entirely. Closing that is the payoff of the merge.

## Read this first

`docs/ISSUES.md`, then `AGENTS.md`.

**Current position, 2026-08-12.** Part I is a three-vessel process: culture,
then conversion, then leach. The one-pot design is retired. *E. coli* runs all
three parts and makes the thiosulfate itself. `Vmax` comes from Part II's
expression cascade pointed at TetH, not from a growth yield:
`Vmax = k_cat x [TetH]` = 9.49 umol/L/min at 4.0 g/L of cells. ISSUES 30, 36.

**Part II is the authority for every protein-model quantity.** `q_max` = 0.0913
uM/(g/L), `mu` = 1.2 h^-1. Superseded values are kept beside them in the same
YAML file. `K_Au` is the deliberate exception: the recovery model uses the
fitted GolB-based literature proxy 0.7 uM rather than Part II's 10 uM
placeholder. The earlier 0.1 uM proxy is retained as superseded.

**What that costs.** The capacity ceiling falls from 22 uM to 0.0539 uM, and
`eta_total` at a 10 uM feed from 64.2% to 0.64%. There is currently no feed
concentration at which capture is not capacity-limited. The engineering target
is `q_max` = 0.1961, every surface anchor occupied, 2.15x away. ISSUES 26 has the
levers. That target is a design anchor, not a physical ceiling: [S29] says
autodisplay reaches "more than" 1e5 molecules per cell.

Any `eta_total` quoted from an earlier version of this repository used
`q_max` = 4.4 and is too high by about two orders of magnitude.

**52 items: 2 BLOCKING (items 32 and 44), 25 open needing a decision, 3 cosmetic, 22 closed.**
See the two tables at the top of `docs/ISSUES.md`.


## Technical recovery model, 2026-09-07

- [RECOVERY_MODEL.md](docs/RECOVERY_MODEL.md): current technical report with live-table placeholders, separate from the earlier audit and wiki copy.
- [RECOVERY_MODEL.docx](docs/RECOVERY_MODEL.docx): generated reader-facing report.
- [build_recovery_model.py](docs/build_recovery_model.py): fills tables from the model and builds Word; `--figures` rebuilds plots.
- [make_recovery_model_figures.py](docs/make_recovery_model_figures.py): five scenario figures and a numerical ledger in [media/recovery_model](docs/media/recovery_model).
- [recovery_process.py](src/recovery_process.py): descriptive inputs and gold amounts through capture, wash and lysate mixing.
- [reduction.py](src/reduction.py): trajectories, donor accounting, physical checks and optional protein-dose hypothesis.
- [recovery_process.yaml](params/recovery_process.yaml): illustrative volume basis.
- [reduction_solver.yaml](params/reduction_solver.yaml): integration and verification controls.
- [recovery_model_figures.yaml](params/recovery_model_figures.yaml): figure scenario grid.
- [test_recovery_process.py](tests/test_recovery_process.py) and [test_reduction.py](tests/test_reduction.py): volume, donor and mechanism-limit verification.


Capture investigation, 2026-09-07: [CAPTURE_INVESTIGATION.md](docs/CAPTURE_INVESTIGATION.md)

Copper competition, 2026-09-13: [COMPETITION.md](docs/COMPETITION.md)
uses [capture_design.py](src/capture_design.py) and
[capture_design.yaml](params/capture_design.yaml); the plot is generated by
[make_capture_design_figures.py](docs/make_capture_design_figures.py).
The checked primary manuscript is archived under [source/capture_investigation](docs/source/capture_investigation).
