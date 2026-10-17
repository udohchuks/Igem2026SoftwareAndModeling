# Part I source files, delivered 2026-08-12

**Nothing in this directory is edited.** These are the author's files as
received. Errors found in them are recorded in `docs/ISSUES.md` and left
standing in the text. Only the author corrects them.

## In use

| File | What it is |
|---|---|
| `Bioleaching_Models_Sequential.docx` | the write-up for the three-vessel process |
| `bioleaching_model_sequential.m` | its MATLAB implementation |
| `leaching.png`, `sulphur species.png` | its figures |

This is Part I. `src/leach.py` implements it and
`tests/test_leach.py` reproduces the numbers it reports.

## Retired 2026-08-12

| File | What it is |
|---|---|
| `Bioleaching_Models_Simultaneous.docx` | the one-pot write-up |
| `bioleaching_model.m` | its MATLAB implementation |
| `3 days model.png` | its figure |

The one-pot design ran every reaction in a single vessel from t = 0. It is no
longer implemented anywhere in `src/`, and no result in this repository comes
from it.

**Why it was retired.** It needs TetH to fold and turn over on a living
*E. coli* surface at pH 7. Published, replicated work says TetH forms inactive
inclusion bodies in *E. coli* and recovers activity only by refolding in acid
outside the cell (`docs/ISSUES.md` item 32). The three-vessel design harvests,
extracts and refolds the enzyme before use, which is that published procedure.
It was not retired on yield: it was worth 1.9 percentage points less gold.

**Kept because the record is not deleted** (`AGENTS.md` rule 6). Two findings
still cite it:

- Its proton block divides a rate by `(1 + beta)` with beta in µmol/L, which is
  dimensionally inconsistent. The sequential file tracks alkalinity instead,
  which is correct, and that is the form implemented. ISSUES 37.
- Its `O2_mode = 'mtc'` branch charges oxygen consumption to the whole copper
  rate rather than the oxygen route alone. ISSUES 37, and ISSUES 41 needs that
  branch fixed before oxygen mass transfer can be modelled.
