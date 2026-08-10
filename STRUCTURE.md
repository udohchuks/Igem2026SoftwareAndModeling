# Repository structure

Three modelling documents, one process chain, one notebook.

```
model.ipynb                 the notebook — narrative and every figure
STRUCTURE.md                this file

docs/
  MODEL.md                  all three documents in one file, verbatim
  MODEL.docx                the same, with a table of contents and figures
  ISSUES.md                 every discrepancy found while combining them
  _frontmatter.md           the chain map and joint definitions
  00_overview_gold_biorecovery.md    Part III, verbatim
  01_bioleaching.md                  Part I,  verbatim
  02_golb_expression.md              Part II, verbatim
  media/                    figures extracted from the Part II document
  source/                   untouched originals (2 .docx + 1 .md)

src/
  params.py                 loads params/*.yaml; lists unsourced parameters
  leach.py                  Part I   — implemented
  expression.py             Part II  — implemented
  recovery_chain.py         Part III — closed forms only; ODE code is a shim
  interfaces.py             the two joints, with unit checks

params/
  leach.yaml                Part I parameter table, transcribed
  expression.yaml           Part II parameter table, transcribed
  recovery_chain.yaml       Part III parameter table, transcribed
  conversions.yaml          constants needed by the joints, not from the docs

tests/
  test_expression.py        reproduces every number Part II prints
  test_leach.py             conservation, geometry, and limit checks
  test_interfaces.py        unit handling, and the numbers the joints produce
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
python -m pytest tests -q
jupyter lab model.ipynb
```

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

`docs/ISSUES.md` item 2. The two independent estimates of `q_max` differ by
about 255×, and `q_max` is the second strongest driver in the chain. No coupled
result should be quoted until that is settled.
