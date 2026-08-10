# Issues found while compiling the three documents

**Nothing in the three source documents was changed.** Every item below is
recorded here and left standing in the text. Where a discrepancy could be
pinned by a test, the test is named so that a future edit cannot hide it.

Found on 2026-08-09 while building this repository. Each item states what was
observed, how it was observed, and what decision it needs.

---

## 1. Two different values for the GolB–gold dissociation constant

| Document | Symbol | Value | Status given |
|---|---|---|---|
| Part II §4 | `K_d` | **10 µM** | "Placeholder — no clean experimental K_d; source or fit" |
| Part III §7 | `K_D` | **0.1 µM**, sweep 1e-4–0.1 | "insensitive (PRCC ≈0); bounded by CXXC proxies" |

The two differ by 100×, and Part III's sweep upper bound (0.1 µM) is 100×
below Part II's single value. Both describe GolB binding Au(I).

Part III §0 lists `K_D` among the parameters that were assumed, then sourced,
then found wrong "by ≥12 orders", so the 0.1 µM figure is the later and
better-supported one.

**Impact is limited but not zero.** Part III reports `K_D` as insensitive
(PRCC ≈ 0), so the chain result barely moves. Part II's Figure 2 is a
different matter: its half-saturation point is `K_d` by construction, so the
whole x-axis of that figure shifts by 100× if 0.1 µM is correct.

**Decision needed:** adopt one value. Recorded in `params/expression.yaml`
under `K_d.conflict`.

---

## 2. The two `q_max` estimates disagree by about 255× — this is the big one

This is the most consequential finding, and it is the joint the two documents
were supposed to close.

| Route | `q_max` |
|---|---|
| Part II §5 → active sites → conversion | **0.017 µM/(g/L)** |
| Part III §7, value in use | **4.4 µM/(g/L)** |
| Part III §7, low end of its own sweep | 0.33 µM/(g/L) |

Arithmetic, from `src/interfaces.py :: qmax_from_expression`:

```
2,909 sites/cell x 3.57e12 cells/g / 6.022e23 mol^-1 x 1e6
  = 0.0172 umol per g, i.e. 0.017 uM per (g/L)
```

Part III already flags `q_max` as *"may be 5–13× optimistic vs published
display ceiling"*. The expression model says the gap is **255×**, and Part III
is still **19×** above the bottom of its own sweep range.

**Why this matters more than the number suggests.** Part III §2.1 states that
the capture transition sits exactly at the capacity ceiling
`q_max · X_max` = 22 µM, and §8 gives `q_max` a PRCC of +0.783, the second
strongest driver in the whole chain. If `q_max` is 0.017 rather than 4.4, the
capacity ceiling falls from 22 µM to about 0.086 µM at `X_max` = 5 g/L. The
recommended 10–20 µM operating window would then be two orders of magnitude
above the capacity ceiling, and capture would be capacity-limited everywhere.

**This is not yet a conclusion.** Three things could each move it:

1. `cells_per_g_dry_weight` = 3.57e12 carries a factor of about 2.5 across
   growth conditions (see `params/conversions.yaml`).
2. Part II's `k_sec` and `f` are both fitted, not measured.
3. Part III's 4.4 may derive from a published biosorption isotherm rather
   than from a display-density calculation, in which case the two are
   measuring different things and the comparison needs restating.

**Decision needed:** resolve before any coupled run is quoted. This is the
single highest-value item in this list.

Pinned by `tests/test_interfaces.py::test_joint2_disagrees_with_part_III_and_says_so`.

---

## 3. Part II's reported steady-state numbers do not satisfy its own equation

Part II §5 reports ≈5,500 surface protein and ≈2,900 active sites. §7 panel
(b) describes the active sites as "being half the surface pool", and §3 gives
`A = f·P_s` with `f` = 0.5.

Half of 5,500 is 2,750, not 2,900.

Recomputing both ways explains it:

| Quantity | Closed form (§5) | ODE with saturation (§3) | Reported |
|---|---|---|---|
| m | 45.5 | 45.5 | 45 |
| P_c | 1,454.5 | 1,454.5 | 1,460 |
| P_s | 5,818.2 | 5,498.3 | **5,500** |
| A | 2,909.1 | 2,749.1 | **2,900** |

The reported `P_s` comes from the ODE; the reported `A` comes from the closed
form. They were taken from different calculations.

The gap is 5.5%, caused by the saturation factor `(1 − P_s/P_s,max)` that the
closed form drops. §8 argues this term is negligible here; at 5.5% it is
small but not zero.

**Decision needed:** state which calculation the reported numbers come from,
and use it consistently. Low urgency — the error is 5.5%.

Pinned by `tests/test_expression.py::test_reported_numbers_are_internally_inconsistent`.

---

## 4. Part I mixes mol and µmol in the gold and copper inventories

Part I §4's parameter table gives `n_Au` as **"mol (or µmol)"** while `R_Au`
is in **µmol min⁻¹**, and the equation is `dn_Au/dt = −R_Au`. The two are
consistent only if `n_Au` is in µmol.

The same ambiguity applies to `n_Cu` in §5.

Using mol makes the gold inventory deplete about 10⁶ times too fast. The
first version of `tests/test_leach.py` did exactly that, and the integration
became so stiff it did not terminate.

**Resolved in this repository by choosing µmol**, which is one of the two
options the table itself offers. `src/leach.py` does not enforce it; the test
file states the choice explicitly.

**Decision needed:** delete "(or mol)" from the Part I table.

---

## 5. Part I's Cu(II) pool has no production route and goes negative

Part I §5 states Cu(II) is *"produced only by oxygen re-oxidation of Cu(I)"*:

```
d[Cu(II)]/dt = 4*v4 - (1/V)*v1B - (1/V)*v2 - 2*v3
```

with `v4 = k4·[O2]·[Cu(I)]`.

Starting from a copper-free solution, `[Cu(I)] = 0`, so `v4 = 0` and every
remaining term is a loss. Cu(II) goes negative immediately. Measured in a
200-minute run: Cu(II) reaches −0.017 µmol/L.

It does not stop there. Negative Cu(II) enters the tetrathionate equation
through the regeneration term `+k1·[Cu(II)]·[S2O3²⁻]`, which turns into a
sink, and tetrathionate also goes negative (−2.4 µmol/L in the same run).

**The physical chain is real** — copper metal dissolves as Cu(I), oxygen
oxidises it to Cu(II) — but as written, the first Cu(II) can never appear,
because `v1B` and `v2` consume Cu(II) rather than produce it.

Note also that §5 gives copper leaching as producing Cu(I), and the copper
oxygen route `v1A` produces Cu(I) too. So Cu(I) does grow from zero. The
problem is only that Cu(II)'s losses fire before its source does.

**Two candidate readings, both plausible, neither chosen here:**

1. The model is intended to start with Cu(II) already present in the
   leachate, in which case the initial condition must be stated.
2. A term is missing, or the sign convention on `v1B`/`v2` differs from what
   the concatenated equations imply.

**Decision needed: this is a modelling question for whoever wrote Part I.**
It is left exactly as written.

Pinned by `tests/test_leach.py::test_cu_II_goes_negative_from_a_copper_free_start`.

---

## 6. Part I §3 defines a stoichiometric yield `Y` and then never uses it

The parameter table gives `Y` = 1, "Stoichiometric yield (S₂O₃ per S₄O₆)".
Neither the production-only equation nor the full balance in §3 contains `Y`.

Harmless while `Y` = 1. It becomes a silent error the moment anyone changes
it. `src/leach.py` follows the equations, not the table, so `Y` is absent
from the code.

**Decision needed:** either insert `Y` into the production term or delete it
from the table.

---

## 7. Part I §4 Model B labels the dissolved gold product two different ways

The Model A equation writes the product as `[Au(S₂O₃)₂³⁻]`. The Model B
equation writes `d[AuO₃³⁻]/dt`. The parameter table lists only
`[Au(S₂O₃)₂³⁻]`.

`AuO₃³⁻` is not a species that appears anywhere else in the document, and the
Model B reaction above it produces `Au(S₂O₃)₂³⁻`. This reads as a typing
slip in a subscript.

`src/leach.py` treats both as the same state, `Au_complex`.

**Decision needed:** cosmetic correction to Part I. No effect on results.

---

## 8. Two rate constants exist only as relative values

| Symbol | Given as |
|---|---|
| `k_Au,Cu` | "≈10³× larger" than `k_Au,O2` |
| `k_Cu,O2` | "calibrate (Ea≈25.8 kJ/mol)" — an activation energy, not a rate |

Neither can be used without a decision. `params/leach.yaml` carries them as
`null` with `status: calibrate`, so any attempt to run the model without
supplying them raises a `KeyError` instead of silently substituting a guess.

That behaviour is deliberate: Part III §0 records that **every parameter
assumed without a source, then sourced, was wrong.**

---

## 9. The three documents use three unit systems, and two of them use minutes

| Part | Concentration | Time |
|---|---|---|
| I | µmol L⁻¹ | minutes |
| II | molecules/cell | minutes |
| III | µM | **hours** |

µmol L⁻¹ and µM are identical, so the concentration mismatch is cosmetic.
The time mismatch is not: a rate constant moved between Part I/II and Part III
without conversion is wrong by 60×.

Handled by `interfaces.per_hour` and `interfaces.per_minute`. No source
document was rewritten.

---

## 10. The combined document keeps the source heading levels

`docs/MODEL.md` concatenates the three documents verbatim, so heading depths
are inconsistent between parts: Part III uses `##` for its top-level
sections while Parts I and II mix `#` and `##`. The table of contents in
`MODEL.docx` reflects that.

Fixing it would mean editing the source text, which was ruled out. The
notebook, `model.ipynb`, provides the consistently structured version.

### Exactly what was changed in conversion

For the record, since "verbatim" should be checkable:

| File | Change |
|---|---|
| `docs/00_overview_gold_biorecovery.md` | none — byte-identical to `model.md` |
| `docs/01_bioleaching.md` | none — byte-identical to the pandoc conversion |
| `docs/02_golb_expression.md` | two image paths repointed to `media/`; line endings normalised to LF. No text changed. |

The two `.docx` originals and `model.md` are kept untouched in `docs/source/`.
Both figures are embedded in `docs/MODEL.docx`.

---

## Items carried over from Part III that are still open

These were already stated in `model.md` and are not new findings. They are
listed so that one list covers the whole chain.

1. No demonstration exists that the construct reduces gold in a lysate.
2. Conversion has never been quantified by anyone in any version of this
   chemistry.
3. Selectivity against Cu/Ag/Ni is unknown — and Part I now supplies a
   copper-bearing leachate directly into that unknown.
4. `k1` and `k2` are the joint #1 driver of the pipeline and are calibrated
   against one qualitative observation.
5. `eta_wash` = 0.95 is the last unsourced parameter and is an upper bound.
6. Conditioning, the V1→V2 transfer, is assumed lossless and is unmodelled.
