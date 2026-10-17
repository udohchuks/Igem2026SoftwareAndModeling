# Gold biorecovery from e-waste — model

iGEM 2026, Ashesi Ghana. The model behind the wiki Model page
(https://2026.igem.wiki/ashesighana/). It follows gold from crushed printed
circuit boards to metal, using engineered *E. coli*.

**Tier 3, synthesis.** This file is the front door and holds no detail. It
points at the files that do.

## The process being modelled

```
1 make thiosulfate  E. coli makes TetH; TetH turns tetrathionate into thiosulfate
2 leach PCB         thiosulfate dissolves gold, and copper, from crushed boards
3 capture           GolB on the cell surface binds the dissolved gold
4 release           thiourea strips the gold back off
5 reduce            a reductase turns gold(I) into metallic gold
```

Each stage has its own model, and each stage's output is the next stage's
input. Copper is the antagonist throughout: Cu(II) destroys thiosulfate and
competes with gold for GolB.

⚠ **No part of this model has been checked against a measurement of this
system.** Stage values are checked against literature and computation.

## Where to go next

| If you want | Open |
|---|---|
| To change anything in the repository | [AGENTS.md](AGENTS.md), read first |
| The layout, one line per file | [STRUCTURE.md](STRUCTURE.md) |
| Wiki stages 1 and 2 | [docs/WIKI_MODEL_UPDATE.md](docs/WIKI_MODEL_UPDATE.md) |
| Wiki stages 3 to 5 | [docs/WIKI_BIORECOVERY_DRAFT.md](docs/WIKI_BIORECOVERY_DRAFT.md) |
| Every disagreement found, and what was done | [docs/ISSUES.md](docs/ISSUES.md) |
| The papers, and the number each supplies | [docs/SOURCES.md](docs/SOURCES.md) |
| Every parameter, with unit and provenance | `params/*.yaml` |

Retired reports, prototypes and drafts are in `archive/`. They do not
describe the current model.

## Running it

Python 3.9 or newer.

```bash
pip install -r requirements.txt
```

```bash
python -m pytest tests -q
```

To rebuild the stages 3 to 5 document and its figures (needs `pandoc`):

```bash
python docs/build_biorecovery.py --figures
```

## Contact

Chukwuemeka Udoh — chukwuemekaudoh16@gmail.com
