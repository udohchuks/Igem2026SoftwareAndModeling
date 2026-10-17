# Repository structure

Updated 2026-10-16, after everything the current wiki does not use moved to
`archive/`.

**Tier 3, synthesis.** This file is the layout and nothing else: one line per
file, kept in step with what is on disk. The rules are in
[AGENTS.md](AGENTS.md). **Agents: read it before changing anything.**

```
README.md                   the front door
AGENTS.md                   the rules. Read first
CLAUDE.md                   Claude Code notes; points at AGENTS.md
STRUCTURE.md                this file
requirements.txt            Python packages
.ignore                     makes search tools skip archive/

archive/                    retired files at their old paths. Do not read
                            unless asked. MANIFEST.txt lists them

src/
  params.py                 loads params/*.yaml; lists unsourced parameters
  leach.py                  stages 1 and 2: three-vessel sequential process
  expression.py             GolB and TetH expression in E. coli
  interfaces.py             the joints between stages, with unit checks
  capture_design.py         stage 3: comb capacity and capture design
  capture_kinetics.py       stage 3: time-dependent capture
  competition.py            stage 3: gold and copper competition at equilibrium
  recovery_chain.py         stages 3 to 5: closed forms and entry points
  recovery_process.py       stage amounts, volumes and lysate mixing
  recovery_audit.py         recovery checks
  reduction.py              stage 5: reduction trajectories, gold and electron checks
  reductase.py              stage 5: growing the reductase and when to lyse
  sensitivity.py            Latin hypercube, PRCC, Finke-Watzky reduction
  fit_fw.py                 Finke-Watzky fitting

params/                     one YAML file per model, plus conversions.yaml
tests/                      one test file per src module

docs/
  WIKI_MODEL_UPDATE.md      wiki stages 1 and 2
  WIKI_BIORECOVERY_DRAFT.md wiki stages 3 to 5. The author's text: do not edit
  ISSUES.md                 findings record
  SOURCES.md                papers, each tied to the number it supplies
  EQUATIONS.md              equation notation
  check_docs.py             links and tier declarations
  make_wiki_leaching_figures.py  media/wiki/plots/
  make_leach_budget.py      media/wiki/concepts/leaching-budget.svg
  make_biorecovery_figures.py    media/biorecovery/
  build_biorecovery.py      BIORECOVERY.docx from the stages 3 to 5 draft
  biorecovery_equations.py  equations for that build
  reference_biorecovery.docx     style reference for that build
  _BIORECOVERY_build.md     GENERATED. Do not hand-edit
  BIORECOVERY.docx          GENERATED. Do not hand-edit
  make_software_data.py     wiki Software page data, from dashboard-prototype/
  source/                   verbatim source documents. Never edited
  media/bioleaching/        stage 1 and 2 figures in WIKI_MODEL_UPDATE.md
  media/biorecovery/        GENERATED stage 3 to 5 figures
  media/wiki/plots/         GENERATED wiki plots
  media/wiki/concepts/      process overview art and the leaching budget figure

dashboard-prototype/        the measurement console; sensors.yaml and
                            stage_ph.yaml feed the wiki Software page
```

## Setup

```bash
pip install -r requirements.txt
```

```bash
python -m pytest tests -q
```
