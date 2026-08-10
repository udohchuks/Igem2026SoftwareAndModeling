---
title: "Gold Biorecovery from E-Waste — Combined Modelling Document"
subtitle: "Bioleaching · GolB Surface Display · Capture, Elution, Reduction, Recovery"
date: "2026-08-09"
---

# About this document

This is a compilation of three modelling documents that together describe one
process chain, from crushed printed circuit boards to recovered metallic gold.

**The three source documents are reproduced verbatim.** Nothing has been
deleted, reworded, corrected, or renumbered. Where the sources disagree with
each other, or contain an apparent error, the disagreement is recorded in
[ISSUES.md](ISSUES.md) and left standing in the text.

| Part | Source file | Stage of the chain |
|---|---|---|
| I | `Bioleaching Models.docx` | Leaching — PCB → dissolved Au(S₂O₃)₂³⁻ |
| II | `GolB_model_writeup.docx` | Expression — GolB surface site density |
| III | `model.md` v3.0 | Capture → elution → reduction → recovery |

Pristine copies of all three originals are kept in `docs/source/`.

## The chain

```
  crushed PCB
      │
      │  PART I — Bioleaching (TetH → thiosulfate → Au/Cu leaching)
      ▼
  leachate:  [Au(S2O3)2 3-],  [Cu(I)],  [Cu(II)],  [S2O3 2-]
      │
      │  ══ JOINT 1 ══  Au_feed
      ▼
  PART III §2 — V1 capture on GolB-displaying E. coli
      ▲
      │  ══ JOINT 2 ══  q_max
      │
  PART II — GolB expression cascade (mRNA → Pc → Ps → active sites A)

  PART III continues:  capture → elution → reduction → recovery → eta_total
```

## The two joints

The three models are not three separate topics. Two named quantities connect
them, and each is a quantity that one document declares missing and another
document supplies.

**Joint 1 — `Au_feed`.**
Part III §10 states: *"`Au_feed` has no upstream model though it dominates
V1."* Part I computes exactly that quantity as `[Au(S₂O₃)₂³⁻](t)`.
Adapter: `src/interfaces.py :: au_feed_from_leach`.

**Joint 2 — `q_max`.**
Part III §9 ranks `q_max` as measurement priority 2 and notes it is *"being
addressed by the secretion model."* Part II §5 computes the active-site count
`A*` per cell, which converts to `q_max` in µM/(g/L).
Adapter: `src/interfaces.py :: qmax_from_expression`.

## Unit systems in use

The three documents were written in different unit systems. They are **not**
harmonised in the text below. Conversion happens once, inside the adapters.

| Part | Concentration | Time | Amount |
|---|---|---|---|
| I — Bioleaching | µmol L⁻¹ | minutes | µmol, mol |
| II — Expression | molecules/cell | minutes | molecules |
| III — Recovery chain | µM | hours | µM, g/L |

Note that µmol L⁻¹ and µM are the same unit under two names. Time is not the
same: Part I and Part II are per-minute, Part III is per-hour.

## Validation status

Part III §0 opens with a statement that governs the whole compilation:

> No part of this model has been checked against a measurement of this system.

That statement was written about Part III. It applies at least as strongly to
Parts I and II, whose parameter tables carry the entries *calibrate*,
*unmeasured*, *fitted*, *assumed*, and *placeholder*.

---
