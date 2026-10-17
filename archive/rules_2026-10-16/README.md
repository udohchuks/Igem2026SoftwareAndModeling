# Gold biorecovery from e-waste — model

iGEM 2026, Ghana. The modelling half of a project that recovers gold from
crushed printed circuit boards using engineered *E. coli*.

**Tier 3, synthesis.** This file is the front door and holds no detail. It
points at the files that do.

---

## What this file is

A one-screen orientation for someone opening the repository for the first time:
what the project models, what the model currently says, and which file to open
next. It is not a manual, not a results document, and not a layout map. Those
are [AGENTS.md](AGENTS.md), [docs/REVIEW.md](docs/REVIEW.md) and
[STRUCTURE.md](STRUCTURE.md) respectively.

## The process being modelled

Three vessels in sequence, and two handovers between them.

```
crushed PCB  ->  STAGE 1  culture         E. coli expressing tetrathionate hydrolase
                 STAGE 2  conversion      TetH turns tetrathionate into thiosulfate
                 STAGE 3  leach           thiosulfate dissolves gold, and copper
                    |
              JOINT 1  leachate gold becomes the capture feed
                    v
                 CAPTURE                  GolB displayed on the cell surface
                 ELUTION                  thiourea strips the gold back off
                    |
              JOINT 2  display density becomes the capture capacity q_max
                    v
                 REDUCTION                a reductase makes metallic nanoparticles
                 RECOVERY                 spin, wash, ash
```

Copper is the antagonist throughout. It is not consumed: Cu(II) destroys
thiosulfate, becomes Cu(I), and oxygen regenerates it. That loop, not the gold
chemistry, sets how much leachant the process needs.

## What the model currently says

| | Base model | With process control |
|---|---|---|
| Gold leached at 72 h | 28.5 % | **83.9 %** |
| Thiosulfate destroyed by copper, net | 98.2 % | 38 % |
| Gold delivered to capture | 28.9 µM | 27.9 µM |
| Gold the capture step can hold | **0.457 µM** | **0.457 µM** |

**The two halves of the process are sized about 63× apart.** That gap, not the
leach chemistry, is the finding the project turns on. Full reasoning, figures
and the decisions we need confirmed are in
[docs/REVIEW.md](docs/REVIEW.md).

⚠ **No part of this model has been checked against a measurement of this
system.** The deliverable is a ranked list of what to measure, not a yield
prediction. Two items are marked BLOCKING in [docs/ISSUES.md](docs/ISSUES.md).

## Where to go next

| If you want | Open |
|---|---|
| The results, the figures, the decisions to confirm | [docs/REVIEW.md](docs/REVIEW.md) |
| To change anything in the repository | [AGENTS.md](AGENTS.md) — read first |
| The layout, one line per file | [STRUCTURE.md](STRUCTURE.md) |
| The chain in plain language, end to end | [docs/MASTER.md](docs/MASTER.md) |
| Every equation, one line of English each | [docs/EQUATIONS.md](docs/EQUATIONS.md) |
| Every disagreement found, and what was done | [docs/ISSUES.md](docs/ISSUES.md) |
| The papers, and the number each supplies | [docs/SOURCES.md](docs/SOURCES.md) |
| Every parameter, with unit and provenance | `params/*.yaml` |

## Running it

Python 3.9 or newer. No database, no web service, no container.

```bash
pip install -r requirements.txt
```

```bash
python -m pytest tests -q
```

That is the real check on this repository: 116 tests, and every published
number is pinned by one of them. To reproduce the review document, including
its figures and its parameter appendix:

```bash
python docs/build_review.py
```

`pandoc` must be on `PATH` for that last one. The notebook, `model.ipynb`, runs
the whole chain end to end and prints every headline number.

## How the numbers are kept honest

Five rules, and a softer sixth, in [AGENTS.md](AGENTS.md) section 1. In short:
no number lives in a `.py` file, a parameter with no measured value stays
`null` and raises rather than guessing, a disagreement gets a test rather than
a silent fix, and the record is never deleted.

**They are not restated here.** `AGENTS.md` is the only home for a rule, so
that no two files can drift apart on one. This paragraph already did drift
once, and said four.

66 issues have been logged this way, 25 of them closed. 41 papers are recorded
with the number each supplies.

## Contact

Chukwuemeka Udoh — chukwuemekaudoh16@gmail.com
