---
title: "Gold Biorecovery — The End-to-End Model"
subtitle: "One chain, plain language, nine steps"
date: "2026-09-07"
---

**Tier 3, synthesis.** The end-to-end chain in plain language, nine steps. Every number here must match the code today. `AGENTS.md` section 11.

# What this file is

`MODEL.md` holds the three source documents reproduced word for word. This
file is different. This file is the single end-to-end model, written once, in
plain language, with the three documents merged into one chain.

For the equations alone, with no explanation, see [EQUATIONS.md](EQUATIONS.md).

**Rules for this file.**

1. Every symbol is named in words before it is used in an equation.
2. Every number carries its unit, every time it appears.
3. Where the sources disagree, this file states the disagreement and names
   the `ISSUES.md` item. It does not silently pick a side.
4. Nothing in `docs/source/`, `docs/00_*`, `docs/01_*` or `docs/02_*` is
   edited. Those stay verbatim.
5. A step is written only after it has been walked through and checked.

**Status: the walkthrough is complete, end to end.**

| Block | Source |
|---|---|
| The culture vessel — producing and harvesting the enzyme | bioleaching document §1 |
| The conversion vessel — tetrathionate to thiosulfate | bioleaching document §2 |
| The leach vessel — dissolving gold and copper | bioleaching document §3 |
| Handover 1 — the leach liquor becomes the capture feed | `src/interfaces.py` |
| GolB display, and Handover 2 — `q_max` | GolB display document |
| Capture on the cell surface | recovery-chain document §2 |
| Elution, reduction, `eta_total` | recovery-chain document §3–6 |

---

# Decisions on record

Everything here changed the model. Nothing here changed a source document.

| Date | Decision | Effect |
|---|---|---|
| 2026-09-18 | Adopt the closest fitted GolB-based literature proxy for `K_Au` | 0.1 → 0.7 µM; S78. `K_Cu` stays unmeasured; `alpha` = 52 is a labelled GolS-derived scenario from S79 |
| 2026-08-10 | **The GolB display document is the authority for every protein-model quantity** | `q_max` 4.4 → 0.0163, `μ` 0.7 → 1.2 h⁻¹ |
| 2026-08-10 | `K_Au` deliberately **not** adopted from the GolB display document | kept the 0.1 µM proxy instead of its 10 µM placeholder; superseded 2026-09-18 |
| 2026-08-10 | Apply leaching stoichiometry per pathway | fixes Cu(II) going negative, ISSUES 5 and 18 |
| 2026-08-10 | Operating window revised 10–20 µM → 1–2 µM | conditional on reaching the display target |
| 2026-08-09 | Solid inventories in µmol, not mol | ISSUES 4 |
| 2026-08-10 | **Symbols renamed to remove four collisions** | `A`, `k1`, `m`, `X`; see below |
| 2026-08-11 | **_E. coli_ is the organism throughout, and it makes the thiosulfate** | the enzyme pool rebuilt from the GolB display cascade; `μ` 0 → 0.02 min⁻¹; biomass 0.1 → 4.0 g/L. ISSUES 30 |
| 2026-08-11 | `k_cat` = 220 min⁻¹ written as sourced | was "unmeasured", ISSUES 15 |
| 2026-08-11 | `Y` wired into the thiosulfate production term | no number moved, `Y` = 1. ISSUES 6 |
| 2026-08-11 | **Capture equilibrium solved properly**, isotherm plus mass balance | the published numbers were right; the code was missing. ISSUES 31 |
| 2026-08-11 | `m` → `k_maint`, `Xmax` → `X_max` applied in the parameter file | the rename table had announced them without applying them |
| 2026-08-11 | 🔴 **Source audit: TetH does not fold actively in *E. coli*** | the enzyme stage is unvalidated. ISSUES 32 |
| 2026-08-11 | **`cells_per_g` corrected** 3.57e12 → 2.36e12, matched to our own growth rate | `q_max` 0.0163 → 0.0108, enzyme 14.3 → 9.49, window 1–2 → 0.4–0.8 µM. ISSUES 33 |
| 2026-08-19 | **Plasmid confirmed pUC-type high-copy**, `N` 20 → 300, and the closed form made saturating | Sites/cell 2,749 → 23,301; `q_max` 0.0108 → 0.0913; ceiling 0.054 → 0.457 µM; `Vmax` 9.49 → 80.36. ISSUES 61, 62 |
| 2026-08-24 | **`k_nuc` rescaled to the enzyme, `k_grow` recentred** | Nucleation here is the reductase turning over, not a chance collision, so `k_nuc` = `(k_cat/K_M)*E_tot` = 0.96 /h. The concentration threshold and the seeding lever below are superseded: reduction now converts the delivered gold in about 3 h. ISSUES 80 to 82 |
| 2026-08-20 | **Seeding added to the reduction vessel**, off by default | A 1 % gold seed cuts the concentration factor from 10× to 4×, giving 89 % in 24 h against 0.30 % today. More reductase gives nothing. ISSUES 64 |
| 2026-08-20 | **`Rech_0` read from the file, not the harness** | The reduction tests fed 100 µM of dithionite where the YAML says 4.6. Every published `eta_reduce` moved, and conversion turns out not to be monotonic in gold. ISSUES 65 |
| 2026-08-11 | `P_s,max` = 1e5 is a demonstrated **floor**, not a ceiling | the 0.1961 target is a design anchor, not a physical limit. [S29] |
| 2026-08-11 | **PRCC recomputed in three regimes** | `k_nuc` went 6th → 1st; reduction now dominates. ISSUES 27 |
| 2026-08-11 | The GolB display document's 5.5% self-disagreement is exactly the saturation term | the ODE is authoritative. ISSUES 3 |
| 2026-08-19 | **The ligand is glycine, not ammonia** | ammonia is volatile and the air pump would strip it. Ammonia wins on 72 h gold and is still not chosen. ISSUES 54, 59 |
| 2026-08-19 | **All Cu(II) constants are ammonia-free**: `k_Au,Cu` = 21.0, `k_par` = 1.20e-5 | the Cu(II) gold route collapses from 9.6 points to 0.1. gold at 72 h 38.4% → 28.5% |
| 2026-08-19 | `K_S2O3` = 3376, the **geometric** mean of the measured `K_ads` band | supersedes the 3900 below; the band is 3x wide, so the centre is geometric |
| 2026-08-19 | **pH is an input, not an output** | the team has a dosing pump, so the model reports titrant demand. Window 9.3-10.5, set point 10.0-10.3 |
| 2026-08-19 | Every structural change of 2026-08-19 is a **switch, false by default** | nothing already reported moved. ISSUES 60 |
| 2026-08-12 | **Bioleaching is the three-vessel sequential process** | culture, then conversion, then leach. Adopted because it is the only version that answers ISSUES 32. ISSUES 36 |
| 2026-08-12 | **Five null leaching rate constants adopted**, all sourced | bioleaching runs end to end for the first time. ISSUES 8, 20 |
| 2026-08-12 | `K_S2O3` = 3900, sourced, beat this repository's own 5e4 placeholder | gold at 72 h 22.6% → 38.4%. ISSUES 42 |
| 2026-08-12 | `K_S4O6` = 300 chosen; `t_film` = 0.5 µm **assumed**, mixed e-waste has no supplier spec | ISSUES 17 closed. ISSUES 19 stays open: the number is chosen, the 5.2× uncertainty is not removed |
| 2026-08-12 | Proton balance tracks **alkalinity, never free `[H+]`** | free protons diverge by construction. ISSUES 37 |
| 2026-08-12 | 🔑 **Cu(I) re-oxidation by oxygen is the reaction that decides the process** | recovery peaks at `[O2]` ≈ 80 µmol/L, not 500: 28% → 52%. **ISSUES 41** |

**Naming rules now in force.** Upper case Latin is per litre, lower case is per
cell. `k` is always a rate constant named by what it does, never numbered. `K`
is always a concentration named by its species. Full mapping in
[EQUATIONS.md](EQUATIONS.md). The three source documents keep their original
symbols; only `MASTER.md`, `EQUATIONS.md` and the code were renamed.

Two issues closed by this alone: **16**, because `k1` and `k3` became one
`k_par`, and **25**, because `A` now means only soluble gold.

**Any `eta_total` quoted before 2026-08-10 used `q_max` = 4.4 and is about two
orders of magnitude too high.**

---

# The three things that decide whether this works

1. **Display density.** `q_max` = 0.0913 today, target 0.1961, **2.15× away**.
   It was 18× away until 2026-08-19. Filling every remaining anchor is now
   worth a factor of two and nothing more, so this has stopped being the lever
   it was and the volume reduction below has become the main one.
   ISSUES 26, 61.
2. **The concentration squeeze.** Capture wants gold below 0.8 µM, reduction
   wants it above 3 µM. Nothing concentrates between them, and a 10× volume
   reduction at elution fixes it. **ISSUES 35.**
3. **Leach pH, and whether TetH works at all.** TetH needs pH ~4 to fold and
   pH 3.0 to turn over; *E. coli* needs pH 7; every published thiosulfate gold
   leach runs at pH 9.3–10.5. A three-way conflict spanning 6.5 pH units.
   **ISSUES 32 and 23. This now outranks the other two.**

**Added 2026-08-12: one thing that decides whether it works *well*, and it is
free.** The three above are hard problems needing wet-lab work or a redesign.
This one is a valve. Turn the oxygen down from 500 to about 80 µmol/L and gold
recovery goes from 38% to 61%, because dissolved oxygen is the only thing in
the model that manufactures the Cu(II) that destroys the leachant. **ISSUES
41.** It does not rescue the chain on its own, but it is the highest ratio of
gain to effort anywhere in the project.

---

# The bottom line

**Physical collection is out of scope.** All reduced gold is taken to be
recovered, so the chain ends at reduction and `eta_total` answers *how much
gold reaches metal*, not *how much reaches the crucible*. Every number below is
therefore an **upper bound**. The centrifuge, wash and ash parameters are not
deleted; they are in `params/recovery_chain.yaml` under
`recovery.eta_phys.superseded`, with the two constraints that bind if the step
ever returns: nanoparticles do not settle under gravity, and ashing must stay
at 500-600 C or gold leaves with the off-gas.

Particle size entered the chain **only** through recovery, so the 10 nm and
>200 nm variants of each scenario have collapsed into one row.

Feed 0.4 uM throughout except the last row.

| Scenario | Gold at reduction | `eta_reduce` | `eta_total` |
|---|---|---|---|
| As built, no concentration | 0.04 uM | 0.001 | **0.02%** |
| Target display, no concentration | 0.30 uM | 0.003 | 0.17% |
| As built **+ 100x concentration** | 3.7 uM | 1.000 | 7.9% |
| **Target display + 10x concentration** | 3.0 uM | 0.994 | **64%** |
| Retired `q_max` = 4.4, as originally published | 8.6 uM | 1.000 | 74% |

**Read the `eta_reduce` column.** Without a concentration step nothing else
matters: display density and elution chemistry both multiply into a reduction
efficiency of 0.003. Fixing the display alone takes the chain from 0.02% to
0.17%.

**One 10x volume reduction between elution and reduction is worth more than
every other lever combined**, and it is the cheapest thing on the list. With
it the chain reaches 64% resting on a reachable site density and a named
process step. ISSUES 35.

**Two cautions on that 64%.** It assumes perfect physical recovery, which is
the decision above. And it assumes the lysate carrying the reducing protein is
concentrated enough not to undo the 10x it depends on. ISSUES 48.

---

# The chain in one picture

```
  VESSEL 1   E. coli culture
             bacteria build the enzyme TetH, which is
             harvested, refolded and purified
                  │
                  ▼
  VESSEL 2   purified TetH + tetrathionate broth
             TetH converts tetrathionate to thiosulfate,
             which banks because no copper is present
                  │
                  ▼
  VESSEL 3   thiosulfate liquor + crushed circuit board
             thiosulfate dissolves the gold, and the copper,
             and copper(II) destroys the thiosulfate
                  │
                  ▼
             HANDOVER 1: dissolved gold becomes the capture feed
                  │
                  ▼
             gold sticks to GolB on the cell surface
                  ▲
             HANDOVER 2: how many sticky sites each cell has
                  │
                  ▼
             strip the gold off, reduce it to metal, spin, wash, ash
                  │
                  ▼
             recovered gold, and one number: eta_total
```

---

# Units: the one rule

The three documents use three unit systems. This file does not force them
into one. Each block keeps the units its authors used, and conversion happens
once, at the joints, inside `src/interfaces.py`.

| Block | Concentration | Time |
|---|---|---|
| Bioleaching, all three vessels | µmol L⁻¹ | minutes |
| GolB display | molecules per cell | minutes |
| Recovery chain | µM | hours |

µmol L⁻¹ and µM are the same unit under two names, so concentrations need no
conversion. Time does: a rate written per minute is 60× larger when written
per hour.

**Convert only quantities that carry a time dimension.**

| Quantity | Example | Converts? |
|---|---|---|
| First-order rate constant, min⁻¹ | `k_deg`, `delta_m`, `k_sec` | yes, × 60 |
| Second-order constant, µM⁻¹ min⁻¹ | `k_par`, `k_on` | yes, × 60 |
| Half-saturation or dissociation constant | `K_S4O6`, `K_S2O3`, `K_Au` | **no** — these are concentrations |
| Half-life or residence time, min | mRNA half-life | yes, ÷ 60 |
| Yield, area, density, count | `Y`, `a_Au`, `P_s,max` | no |

The `K_S4O6` row is where this usually goes wrong. It sits in a kinetic
equation and it is not a kinetic parameter.

---
# Bioleaching happens in three vessels

**Source:** *Bioleaching Modelling [Sequential]*, in
`docs/source/sequential_2026-08-12/`. **Code:** `src/leach.py`.
**Parameters:** `params/leach.yaml`.

## In plain language

The original design was one pot. Bacteria, enzyme, broth, crushed board, all
together from the first minute. The design in use splits it into three tanks
that run one after another:

| Vessel | What is in the tank | What comes out |
|---|---|---|
| **the culture vessel** | *E. coli* culture | harvested, purified TetH enzyme |
| **the conversion vessel** | purified TetH + tetrathionate broth | thiosulfate liquor |
| **the leach vessel** | thiosulfate liquor + crushed board | dissolved gold, and copper |

Three things follow, and they are the whole difference:

1. **The conversion vessel has no cells.** The enzyme is something you pour in, at whatever
   concentration you like, rather than something the model has to grow. So the
   enzyme equation leaves the reaction tank entirely and becomes a sizing
   calculation.
2. **The conversion vessel has no copper.** Nothing in that tank can destroy thiosulfate, so
   the whole broth charge converts and banks: 94.4 mM, against the 0.1 M the
   gold literature calls ideal. In one pot it never got past a few mM.
3. **The leach vessel has no enzyme.** Thiosulfate is a fixed budget, charged at the
   start and spent. Nothing tops it up.

## Why it was adopted, and it is not the yield

Splitting the tanks is worth 1.9 percentage points of gold. Both figures
predate the 2026-08-19 ammonia-free constants; the gap between the two
architectures is what this line is about, not the level.
That is almost nothing. **Both designs die the same death**, thiosulfate
annihilated by copper(II), and the sequential one dies slightly harder because
it has more thiosulfate to lose.

The real reason is the enzyme's blocking problem. TetH will not fold into a
working enzyme inside *E. coli*; it clumps into inclusion bodies and has to be
refolded in acid, in a test tube (ISSUES 32). The one-pot design needs TetH to
work on a living cell at pH 7, which the literature says it does not do. **The
three-vessel design harvests and refolds the enzyme before using it, which is
exactly the published procedure.** It is the first version of the bioleaching
model that could work at all.

**Audit:** reproduced line for line before adoption. Fourteen of fourteen
reported numbers matched, and three mass balances the original does not test
also close. ISSUES 36.

**The one-pot model has been removed from the code.** Its write-up and MATLAB
file are kept, marked retired, in `docs/source/sequential_2026-08-12/`.

---

# The culture vessel — producing and harvesting the enzyme

**Code:** `src/leach.py :: stage1_enzyme_steady_state`.
**Parameters:** `params/leach.yaml :: enzyme_capacity`.

**This stage sizes the culture and then stops.** It does not appear in the
conversion or leach differential equations at all.

## In plain language

The bacteria are a factory that makes one product: an enzyme called
tetrathionate hydrolase, or TetH. The factory runs at a steady rate. The enzyme
is lost two ways: the cell's proteases break it down, and every division shares
it between two cells. The amount in the tank is the balance of those.

## The equation

```
d[E]/dt  =  k_syn·X  −  (k_deg + μ)·[E]
            ───────     ──────────────
            cells make  breakdown, plus dilution by division
```

| Symbol | In words | Unit | Value |
|---|---|---|---|
| `[E]` | active TetH in the culture | µmol L⁻¹ | steady state, below |
| `k_syn` | enzyme built per cell | µmol cell⁻¹ min⁻¹ | 8.74×10⁻¹⁷ |
| `X` | cells per litre | cell L⁻¹ | 1×10¹² |
| `k_deg` | how fast the enzyme is broken down | min⁻¹ | 1.1×10⁻³ |
| `μ` | how fast the cells divide | min⁻¹ | 0.0173, 40 min doubling |

The culture reaches steady state in 1/(k_deg + μ) ≈ 55 minutes, far faster than
anything downstream, so only the steady state is used:

```
[E]_culture  =  k_syn·X / (k_deg + μ)  =  4.75×10⁻³ µmol L⁻¹
```

That is about 2,860 molecules per cell, roughly 0.3% of the cell's total
protein — a modest and realistic burden.

**Note which loss dominates.** `μ` = 0.0173 min⁻¹ against `k_deg` = 0.0011
min⁻¹, so division removes enzyme about sixteen times faster than proteolysis.
Engineering a protease-resistant enzyme buys almost nothing. Growing slower, or
expressing more, buys a great deal.

## Sizing the culture

```
V_culture / V_stage2  =  E_2 / [E]_culture
```

Charging the conversion vessel to `E₂` = 0.043 µmol L⁻¹ takes **9.1 litres of culture per
litre of conversion vessel**, which is 2.15 mg of purified TetH. The protein
mass is trivial. **The culture volume is the real constraint**, and it is what
expression engineering — promoter strength, copy number, RBS — acts on.

The trade is direct: three days of conversion on 9 L of culture, one day on
27 L, about 27 days at the in-situ enzyme concentration.

## 🔴 BLOCKING — this route may not work at all. ISSUES 32

Read `ISSUES.md` item 32 before quoting any enzyme number. Four papers report
that TetH expressed in *E. coli* forms **inactive inclusion bodies**, and that
activity is recovered only by refolding at pH 4 in a tube. Its catalytic
optimum is pH 3.0 and its mechanism needs a protonated Asp325, so it cannot
turn over at the pH *E. coli* lives at.

The culture vessel harvests and purifies rather than using the enzyme in place, which is
the published procedure and is why this design was adopted. It does not remove
the problem: the folding step is assumed to work and nothing accounts for its
yield.

## What the model does not account for

Purification losses. Real recovery is perhaps a third to two thirds, so
9.1 litres is a floor, not an estimate. ISSUES 40.

## Open issues touching this stage

| Issue | One line |
|---|---|
| [32](ISSUES.md) | 🔴 **BLOCKING.** TetH does not fold actively in *E. coli*. |
| [40](ISSUES.md) | No purification yield term. The culture volume is a floor. |
| [11](ISSUES.md) | **Cosmetic.** The parameter table writes the growth rate with a Greek capital Mu. |

---

# The conversion vessel — converting tetrathionate to thiosulfate

**Code:** `src/leach.py :: stage2_derivatives`, `simulate_stage2`.
**Parameters:** `params/leach.yaml :: tetrathionate`, `:: broth`.

## In plain language

Tetrathionate is the raw material. The purified enzyme breaks it apart, and the
useful piece that comes out is thiosulfate, which is what dissolves the gold.
Nothing else happens in this tank.

## The reaction

```
S4O6(2-) + H2O  →  S2O3(2-) + S(0) + SO4(2-) + 2H+
```

TetH works through a disulfane-monosulfonic-acid intermediate, lumped here into
one overall reaction.

## Where the starting concentrations come from

The 46 g L⁻¹ broth base contains 30 g L⁻¹ sodium thiosulfate pentahydrate and
**no tetrathionate**. Tetrathionate is made in situ when the iodine solution is
added at the point of use:

```
I2 + 2 S2O3(2-)  →  2 I(-) + S4O6(2-)
```

Iodine is the limiting reagent, so only part of the thiosulfate converts:
23.2 mM tetrathionate and 72.1 mM thiosulfate. **Both are initial conditions
inherited from the medium, not model outputs.**

## The equations

```
d[S4O6]/dt  =  −  k_cat·E_2 · [S4O6]/(K_S4O6 + [S4O6])
d[S2O3]/dt  =  + Y·k_cat·E_2 · [S4O6]/(K_S4O6 + [S4O6])
```

| Symbol | In words | Unit | Value |
|---|---|---|---|
| `E_2` | purified TetH in the conversion vessel | µmol L⁻¹ | 0.043, a design variable |
| `k_cat` | reactions one enzyme molecule runs per minute | min⁻¹ | 125 |
| `K_S4O6` | tetrathionate at which the enzyme runs half speed | µmol L⁻¹ | 300 |
| `Y` | thiosulfate produced per tetrathionate | — | 1 |
| `t_2` | stage duration | min | 4,320, three days |

**The enzyme concentration is a constant input, not a state variable.** There
are no cells in this tank, so `k_syn`, `k_deg` and `μ` do not appear.

## The saturating factor

```
[S4O6] / (K_S4O6 + [S4O6])        how busy the enzyme is, 0 to 1
```

That fraction is the only shape needed for the whole bioleaching model. It
appears again for oxygen, thiosulfate and copper in the leach vessel, and it always
means the same thing: **how close is this reactant to keeping every site busy.**

`K_S4O6` is the concentration at which the enzyme runs at exactly half speed.
Below it, adding substrate helps a lot. Above it, adding more barely helps.

## Two free checks

Since `Y` = 1, no sulfur leaves the tank:

```
[S4O6] + [S2O3]  =  constant
```

A solver run that breaks that sum is wrong. And because nothing else is
happening, the tank has an exact solution to check the solver against:

```
K_S4O6·ln(S_0/S) + (S_0 − S)  =  k_cat·E_2·t
```

## What it produces

Tetrathionate falls from 23,200 to 941 µmol L⁻¹; thiosulfate rises from 72,100
to 94,359 µmol L⁻¹. That is **95.9% conversion in three days** at
`k_cat·E₂` = 5.375 µmol L⁻¹ min⁻¹.

The reaction is effectively zero-order for almost the whole run. With 23,200
µmol L⁻¹ of substrate against `K_S4O6` = 300, the saturation term starts at
0.987, so the enzyme runs flat out until substrate is nearly exhausted. That is
why the curve is close to a straight line rather than a decaying exponential.

**The final 94.4 mM thiosulfate is the single largest benefit of the
three-vessel design.** In one pot, thiosulfate and copper coexisted from the
first minute and thiosulfate never accumulated past a few millimolar. Removing
copper from this stage lets the full broth charge convert and bank before
leaching begins.

## What the model does not account for

`k_cat` = 125 min⁻¹ comes from assays at pH 3, 30 °C, in molar sulfate. The conversion vessel
would have to run near those conditions to reach the modelled rate, and
thiosulfate decomposes in acid. The two requirements point in opposite
directions and there is no term for the loss. ISSUES 38.

## Open issues touching this stage

| Issue | One line |
|---|---|
| [38](ISSUES.md) | `k_cat` is a pH 3 number; thiosulfate needs alkaline conditions. No decomposition term. |
| [23](ISSUES.md) | The pH conflict across the whole chain, 6.5 units wide. |

Closed and touching this stage: 17 (`K_S4O6` chosen), 16, 6 (`Y` wired in), 13.

## The one decision this stage forces

Choose the enzyme loading deliberately. It trades directly against culture
volume: three days on 9 L per litre, one day on 27 L. Nothing else in the stage
is adjustable.

---

# The leach vessel — leaching the board

**Code:** `src/leach.py :: stage3_derivatives`, `simulate_stage3`.
**Parameters:** `params/leach.yaml :: gold`, `:: copper`, `:: oxygen`.

The conversion vessel's product is charged into the leach vessel with crushed PCB
powder. **There is no enzyme and no tetrathionate feed**, so thiosulfate has no
source and can only be consumed.

## In plain language

Gold does not dissolve on its own. Two things must happen at the same spot on
the metal surface.

1. Something must pull an electron off the gold atom. That is the **oxidant**.
2. Something must wrap the atom up and carry it into solution. That is the
   **thiosulfate**.

Two oxidants are available: oxygen, which is always there, and copper(II),
which appears once copper starts dissolving. Copper(II) is about 1,000 times
better at it.

A circuit board is mostly copper, so copper dissolves too, whether you want it
or not. It does three things, and only the first is obvious.

1. It eats thiosulfate you wanted for gold.
2. It turns thiosulfate back into tetrathionate, undoing the conversion vessel.
3. **It carries electrons for you**, far faster than oxygen can.

## Gold: the reactions

```
Au(0) + 2 S2O3(2-)  →  Au(S2O3)2(3-) + e(-)                   anodic half-reaction
4 Au(0) + 8 S2O3(2-) + O2 + 2 H2O  →  4 Au(S2O3)2(3-) + 4 OH(-)     O2 route
Au(0) + 2 S2O3(2-) + Cu(II)  →  Au(S2O3)2(3-) + Cu(I)               Cu(II) route
```

## Gold: the area, a film not a lump

Copper on a board is bulk metal. Gold is a thin plated layer, so it does not
shrink inward. It gets thinner over the same face area until it is gone,
independent of how finely you crush.

```
a_Au = m_Au / (rho_Au · t_film)  =  2.07e-3 m²
```

Same mass of gold, plated thinner, covers more area. More area leaches faster.

| Plating thickness | Gold in solution at 600 min |
|---|---|
| 0.05 µm | 384.5 µM |
| 0.20 µm | 96.3 µM |
| **0.50 µm ← assumed** | **38.5 µM** |
| 1.00 µm | 19.3 µM |

**That is a 20-fold range and it is the biggest lever in the bioleaching
model.** It is larger than any rate constant here, and you do not control it —
the boards you feed in control it. Mixed e-waste has no supplier specification,
so 0.5 µm is a team assumption, not a measurement. ISSUES 19.

## Gold: the rate

```
R_Au = a_Au(t) · θ(S2O3) · [ k_Au,O2·θ(O2) + k_Au,Cu·θ(Cu(II)) ]
                             ─────────────   ─────────────────
                               slow route      fast route

dn_Au/dt = −R_Au              d[Au(S2O3)2]/dt = +R_Au / V
```

**The two oxidant terms add. Everything else multiplies.** Either oxidant alone
can do the job, so they add. But nothing happens without exposed area and
without thiosulfate, so those multiply through both. Oxygen enters only its own
term, because Cu(II) does not need oxygen at the gold surface.

## Why the fast route does not win by 1,000×

Copper(II) is 1,000× better per event, but each gold atom it dissolves consumes
one copper(II). **It is a reagent, not a catalyst.** Run it and it runs out.
Only re-oxidation of copper(I) by oxygen keeps it alive.

## Copper: the reactions

```
4 Cu(0) + O2 + 8 S2O3(2-) + 2 H2O  →  4 [Cu(S2O3)2](3-) + 4 OH(-)   O2 route
Cu(0) + Cu(2+) + 4 S2O3(2-)  →  2 [Cu(S2O3)2](3-)                   comproportionating
4 Cu(I) + O2 + 2 H2O  →  4 Cu(II) + 4 OH(-)                         re-oxidation
2 Cu(II) + 2 S2O3(2-)  →  2 Cu(I) + S4O6(2-)                        parasitic
```

## Copper: the area, a lump not a film

Copper is solid metal running through the board, so its particles erode inward
and shrink:

```
a_Cu(0) = 6·m_Cu / (rho_Cu · d)          d = crushed particle size
a_Cu(t) = a_Cu(0) · (n_Cu/n_Cu(0))^(2/3)
```

The two-thirds power is geometry: surface goes as radius squared, volume as
radius cubed. The `6/d` is the surface-to-volume ratio of a crushed particle.
**Crush finer, get more area.**

| Particle size | Copper area |
|---|---|
| 2 mm | 0.00335 m² |
| 4 mm | 0.00167 m² |
| **6 mm ← in use** | 0.00112 m² |

Note the contrast with gold. Plating thickness is set by your feedstock and you
cannot change it. Particle size is set by how hard you crush, and you can.

## The rates

```
v_Cu,O2 = k_Cu,O2 · a_Cu(t) · θ(O2)     · θ(S2O3)
v_Cu,Cu = k_Cu,Cu · a_Cu(t) · θ(Cu(II)) · θ(S2O3)
v_3     = k_par   · [Cu(II)] · [S2O3]                parasitic
v_4     = k_ox,Cu · [O2] · [Cu(I)]                   re-oxidation
```

| Symbol | In words | Unit | Value |
|---|---|---|---|
| `k_Au,O2` / `k_Au,Cu` | gold rate constants, two routes | µmol m⁻² min⁻¹ | 11.4 / **21.0** |
| `k_Cu,O2` / `k_Cu,Cu` | copper rate constants | µmol m⁻² min⁻¹ | 200 / 200 |
| `K_O2` | oxygen half-saturation | µmol L⁻¹ | 50 |
| `K_S2O3` | thiosulfate half-saturation | µmol L⁻¹ | **3,376** |
| `K_CuII` | Cu(II) half-saturation | µmol L⁻¹ | 5×10⁴ |
| `k_par` | parasitic rate constant | L µmol⁻¹ min⁻¹ | **1.2×10⁻⁵** |
| `k_ox,Cu` | Cu(I) re-oxidation constant | L µmol⁻¹ min⁻¹ | 1×10⁻⁴ |
| `[O2]` | dissolved oxygen, held constant | µmol L⁻¹ | 500 |

**Three of those moved and this table did not follow, until 2026-08-20.**
`k_Au,Cu` was 1,500, `K_S2O3` was 3,900 and `k_par` was 1×10⁻⁵. The first two
changed on 2026-08-12 when the ammoniacal constants were replaced with
ammonia-free ones and `K_S2O3` was reset to the geometric mean of the measured
band; `k_par` moves with `k_Au,Cu` or not at all. `docs/check_docs.py` check 4
now looks for exactly this. `ISSUES.md` items 42 and 54.

## The balances

```
dn_Cu/dt    = −(v_Cu,O2 + v_Cu,Cu)

d[S2O3]/dt  = −2·R_Au/V  −  (2·v_Cu,O2 + 4·v_Cu,Cu)/V  −  2·v_3
              ─────────     ──────────────────────       ──────
              gold          copper                       parasitic

d[S4O6]/dt  = +v_3

d[Cu(I)]/dt  = (v_Cu,O2 + 2·v_Cu,Cu + R_Au,Cu)/V + 2·v_3 − 4·v_4
d[Cu(II)]/dt = 4·v_4 − (v_Cu,Cu + R_Au,Cu)/V − 2·v_3
```

The numbers in front are counts of molecules, read off the balanced reactions
above. Two per gold atom, because it dissolves as `Au(S2O3)2`. Two or four per
copper atom, depending on the route. Two per parasitic turnover, which destroys
two thiosulfate to rebuild one tetrathionate.

**The oxygen routes consume no copper(II) at all.** An earlier version charged
them for it anyway and drove the copper(II) pool negative. ISSUES 18.

**Tetrathionate is a dead end here, unless the pH is held.** The parasitic
reaction regenerates it and there is no enzyme in this tank to hydrolyse it
back, so it accumulates untouched: 47,272 µmol L⁻¹ by the end of a run.

Holding the pH alkaline opens a second route that breaks it down again:

```
4 S4O6(2-) + 6 OH-  ->  5 S2O3(2-) + 2 S3O6(2-) + 3 H2O
```

This is the largest single term in the model — gold at 72 h goes from 28.5% to
50.2% at pH 10.3 — and **it is not free**: five of every eight sulfur atoms
return as thiosulfate and the other three leave as trithionate, which nothing
consumes at 25 °C. It is off by default, because it needs a pH set point and
because `k_alk` has been read only in secondary sources. ISSUES 60.

## The copper loop, which decides the whole stage

```
   Cu(0) metal
      │  dissolves as Cu(I) on both routes
      ▼
    Cu(I)  ──── oxygen re-oxidises it (v_4) ────►  Cu(II)
      ▲                                             │
      │                                             │ strips electrons
      └──────────── from gold leaching ◄────────────┘ off gold, fast
                    and from the parasitic reaction
```

🔑 **`v_4` is the only source of Cu(II) anywhere in the model.** Copper metal
dissolves as copper(I) on both routes. So dissolved oxygen manufactures both
the oxidant that helps and, through the parasitic reaction, the poison that
destroys the leachant. They are the same substance.

Because of that, gold recovery does **not** rise with aeration. It peaks:

| `[O2]` µmol L⁻¹ | Gold recovered at 72 h |
|---|---|
| 50 | 47.9% |
| **80** | **51.5% ← optimum** |
| 200 | 38.8% |
| **500 ← baseline** | **28.5%** |

Turning the oxygen down from 500 to 80 is worth 23 percentage points and costs
nothing. **ISSUES 41.**

Note the baseline is not merely high, it is **unreachable**: air saturates
water at 259 µmol L⁻¹ at 25 °C, so 500 needs pure-oxygen sparging. Modelling
the air pump instead of imposing a constant gives 35.9% on its own, and turning
the pump down carries it to 48%.

## Acidity

The reactions release and consume protons, so pH moves. It is tracked as
**alkalinity**, the net base added since the start:

```
d(Alk)/dt = 4·v_4 + R_Au,O2/V + v_Cu,O2/V - 2·v_hyd - 1.5·v_alk

pH = pH_0 + Alk/β
```

Four hydroxides per re-oxidation, one per gold atom and one per copper atom
dissolved by oxygen, less two protons per hydrolysis and 1.5 hydroxides per
tetrathionate broken down in alkali. `β` is the buffer capacity, and it carries
`status: calibrate` with no source.

🔑 **With a dosing pump, this inverts.** pH becomes an input held at a set
point, alkalinity stops moving, `β` drops out of the model entirely, and the
reported quantity becomes the **titrant demand**: how much acid or base the
pump must deliver. That is what the equipment produces and what a reagent
budget needs. Demand is negative — acid — throughout.

**Do not track free `[H+]` here.** A run produces about 100,000 µmol L⁻¹ of net
base against a free proton pool of 0.1 µmol L⁻¹ at pH 7. Subtracting drives it
negative and the pH diverges. ISSUES 37.

## What actually happens over 72 hours

Leaching runs in two phases.

**To 27 hours.** Thiosulfate is abundant, its saturation factor sits near 0.96,
and gold leaches close to its maximum. Gold recovery reaches 27.8% at 24 hours.
The Cu(II) route contributes almost nothing: at the ammonia-free `k_Au,Cu` of
21.0 it is worth 0.1 percentage points over the whole run, so the rate starts
near its maximum and declines rather than rising to a Cu(II)-driven peak.

**After 27 hours.** Leaching stops for want of thiosulfate. Its saturation
factor collapses from 0.96 to near zero while oxygen's stays flat at 0.91.
Cu(II) keeps accumulating to its maximum of 818 µmol L⁻¹ **more than a day
after there is any thiosulfate left for it to destroy.** Gold reaches 28.5% at
72 hours, so the second and third days are worth 0.7 points. **Thiosulfate is
the limiting factor, copper(II) is what removed it, and it bought nothing in
return.**

Where the thiosulfate went:

| Sink | µmol L⁻¹ | Share |
|---|---|---|
| Gold leaching, 2 per Au | 58 | 0.06% |
| Copper leaching | ≈1,640 | 1.7% |
| **Parasitic Cu(II) reaction** | **92,661** | **98.2%** |
| Total | 94,359 | 100% |

**The leachant is not consumed by leaching.** It is consumed by copper(II).

⚠️ **The 98.2% is a gross figure.** Once the alkaline route is open, thiosulfate
handed back can be destroyed again, so the gross draw double-counts. At pH 10.3
with glycine the gross draw is 80,871 µmol L⁻¹, 47,921 comes back, and the
**net** destroyed is 35,871 — 38% of the charge, not 98%. Quote the net.

## What the model does not account for

**The parasitic constants are borrowed.** `k_par` and `k_ox,Cu` come from
ammoniacal systems, where ammonia deliberately stabilises Cu(II) and slows the
parasitic reaction. In an ammonia-free system `k_par` may be substantially
larger, which would shorten the productive phase further. These are the most
consequential unmeasured parameters in the model.

**Oxygen is imposed, not solved.** `[O2]` is held at 500 µmol L⁻¹, so its flat
saturation trace is an assumption. A real reactor would show depletion during
peak copper oxidation.

**No passivation term.** The source text says passivation multiplies these
rates, but no such term appears in the equations. In ammonia-free thiosulfate a
sulfur film is known to build on the gold surface and slow it. ISSUES 45.

**No re-precipitation term.** Free thiosulfate reaches zero while 30 g of
metallic copper is still in the tank, and dissolved gold is known to plate back
onto copper under exactly those conditions. ISSUES 46.

**Idealised physics.** Perfect mixing, no mass-transfer resistance, uniform
spherical particles, isothermal operation, uniform gold film thickness on every
particle.

## Open issues touching this stage

| Issue | One line |
|---|---|
| [41](ISSUES.md) | 🔑 **The free win.** Oxygen has an optimum near 80 µmol L⁻¹, not 500. 28% → 52%. |
| [19](ISSUES.md) | Gold rate goes as 1/`t_film`, spanning 5.2×, and the thickness is assumed. |
| [45](ISSUES.md) | Passivation is described in the text and absent from the equations. |
| [46](ISSUES.md) | No gold re-precipitation onto metallic copper. |
| [37](ISSUES.md) | Closed: alkalinity, never free `[H+]`. |

Closed and touching this stage: 18 (stoichiometry per pathway), 20, 8, 42, 16, 5.

## The three decisions this stage forces

1. **Turn the oxygen down.** 80 µmol L⁻¹, not 500. Free, and worth 22 points.
2. **Protect thiosulfate from Cu(II)**, with a ligand such as citrate, glycine,
   oxalate or EDTA. It attacks the 98.2% loss term directly. Alternatively
   pre-leach the copper out, at the cost of an extra unit operation.
3. **Run for one day, not three.** The extra 48 hours add 3.3 percentage
   points. Batch turnaround is worth more than residence time.

---
---

# Handover 1 — the leach liquor becomes the capture feed

**Source:** the gap between the bioleaching document §4 and the recovery-chain document §2.
**Code:** `src/interfaces.py :: au_feed_from_leach`.

## In plain language

the bioleaching document finishes with a tank of liquid holding dissolved gold. the recovery-chain document starts
by asking how much dissolved gold is in the tank. They are the same number.

the recovery-chain document §10 says outright: *"`Au_feed` has no upstream model though it
dominates V1."* the bioleaching document is that missing upstream model. That is the whole joint.

## There is no conversion

```
Au_feed [µM]  =  [Au(S2O3)2 3-] [µmol/L]
```

the bioleaching document writes µmol L⁻¹. the recovery-chain document writes µM. **These are the same unit under two
names.** Nothing is multiplied or divided.

The adapter still checks the unit and refuses anything else:

```
au_feed_from_leach(19.27, unit="mol/L")
  -> UnitError: expects umol/L or uM
```

It costs nothing and it stops the one mistake that would silently be 10⁶ out.

## What does need converting: time

the bioleaching document runs in minutes. the recovery-chain document runs in hours. Any **rate** crossing the joint
is wrong by 60× if you forget. Concentrations are not rates, so `Au_feed` is
safe. Use `per_hour` and `per_minute` for anything that is a rate.

## The result that neither document could have produced alone

the recovery-chain document §2.1 sets three thresholds on `Au_feed`:

| Threshold | What happens above it |
|---|---|
| 10 µM | below this, capture fraction is high but absolute gold is low |
| 22 µM | the capacity ceiling; capture becomes capacity-limited |
| 30 µM | toxicity starts costing 63–96% of capture |

A leach run climbs straight through all three:

| Leachate reaches | Time |
|---|---|
| 10 µM | 314 min |
| 20 µM | 623 min |
| 22 µM, capacity ceiling | 684 min |
| 30 µM, toxicity onset | 929 min |

**So the leach has a stopping time, and leaching chemistry does not set it.
The capture model does.** Run past about 700 minutes here and the extra gold
you dissolve is gold your cells cannot hold. Run past 929 and it starts
poisoning them.

Before the merge, the bioleaching document had no reason to stop and the recovery-chain document had no idea where
its feed came from. Coupling them produced a rule neither one contains.

⚠️ **Those minutes are not a prediction.** They inherit `t_film`, unknown by
20×, and two placeholder rate constants. What is robust is the shape of the
result: a stopping rule exists, and it is imposed from downstream.

## Copper crosses too, and nobody knows how much

`cu_feed_from_leach` carries copper(I) and copper(II) across, tagged
`consumed_by_part_III: False`, so the stream is visible rather than quietly
dropped.

The model currently reports 0.03 copper per gold. **That is certainly wrong.**
A circuit board is mostly copper. Both copper rate constants are `null`, so
the model has no opinion on selectivity at all. the recovery-chain document §0 already lists
selectivity against Cu, Ag and Ni as unknown.

## Open issues touching this step

| Issue | One line |
|---|---|
| [21](ISSUES.md) | No stopping rule exists; the recovery-chain document's window implies one. First genuinely coupled result. |
| [8](ISSUES.md) | Copper rate constants are `null`, so the copper:gold ratio at the joint is meaningless. |

Closed and touching this step: 9, three unit systems, handled by the adapters.

## The one decision this step forces

Decide the leach on a target `Au_feed`, not a target time. Dilution is a
legitimate lever, and the recovery-chain document §2.1 already says so.

---

# Building the sticky sites, and Handover 2

**Source:** the GolB display document, all sections. **Code:** `src/expression.py`.
**Parameters:** `params/expression.yaml`.

## In plain language

Handover 1 delivered dissolved gold. Now you need something to grab it.

The cells are engineered to grow a gold-binding protein, GolB, on their outer
surface. Each cell ends up with a certain number of grabbing points. the GolB display document
counts them.

The count is not one step. It is a queue of four, and each stage loses some of
what the stage before it made.

```
  DNA
   │  transcription
   ▼
  mRNA  m
   │  translation
   ▼
  protein inside the cell  P_c
   │  export to the surface
   ▼
  protein on the surface  P_s
   │  only some folds correctly
   ▼
  working sites  A
```

Every pool leaks in two ways: the molecule falls apart, and the cell divides
and dilutes it. For a stable protein, dilution is the larger loss. That is the
`μ` term, and here it is genuinely correct — these are per-cell counts, so
doubling the cell volume really does halve them. Contrast the bioleaching document, where the
same term was borrowed into a bulk balance by mistake (issue 12).

## The four equations

```
dm/dt   = α·N            − (δ_m + μ)·m
dP_c/dt = β·m            − (k_sec + δ_c + μ)·P_c
dP_s/dt = k_sec·P_c·(1 − P_s/P_s,max) − (δ_s + μ)·P_s
A       = f·P_s
```

| Symbol | In words | Value |
|---|---|---|
| `α` | how fast one DNA copy makes mRNA | 0.5 mRNA min⁻¹ copy⁻¹ |
| `N` | how many DNA copies per cell | 20 |
| `β` | how many proteins one mRNA makes per minute | 4.0 |
| `k_sec` | how fast protein moves to the surface | 0.10 min⁻¹ |
| `δ_m`, `δ_c`, `δ_s` | how fast each pool falls apart | 0.20, 0.005, 0.005 min⁻¹ |
| `μ` | how fast cells divide | 0.02 min⁻¹, doubling in 35 min |
| `f` | fraction that folds correctly | 0.5, **fitted** |
| `P_s,max` | how many anchor points the surface has | 1×10⁵ per cell |

The only term that is not a straight in-and-out balance is
`(1 − P_s/P_s,max)`. That is the surface filling up. As anchors run out, new
protein stops arriving. It is the same saturating idea as the conversion vessel, written the
other way round.

## The numbers

Draft 4 of the display document, 2026-08-19, supplies the **saturating**
closed form and confirms a **pUC-type high-copy backbone**, `N` = 300:

| Pool | Saturating closed form | ODE | Draft 4 reports |
|---|---|---|---|
| mRNA | 681.8 | 681.8 | 682 |
| Protein inside | 21,818.2 | 21,818.2 | 21,818 |
| Protein on surface | 46,601.9 | 46,601.9 | **46,602** |
| **Working sites** | **23,301.0** | **23,301.0** | **23,301** |

**The closed form and the ODE now agree to 1e-14**, which closes issue 3. The
old 5.5% gap was never an inconsistency in the model: the document quoted `P_s`
from the ODE and `A` from the non-saturating closed form, two different
calculations of the same thing.

| At `N` = 20, retired | Closed form | ODE |
|---|---|---|
| Protein on surface | 5,818.2 | 5,498.3 |
| Working sites | 2,909.1 | 2,749.1 |

**The surface is now 46.6% full**, not 5.5%. 46,602 anchors used of 100,000
available. That matters in a moment, and it matters in the opposite direction
to how it used to.

## What actually raises the site count

Normalised sensitivity of `A*`. A value of +1.0 means doubling that parameter
doubles the sites.

| Parameter | At `N` = 300 | At `N` = 20, retired |
|---|---|---|
| `f` folding fraction | **+1.000** | +1.000 |
| `P_s,max` anchor capacity | **+0.466** | +0.000 |
| `α` promoter strength | +0.534 | +1.000 |
| `N` copy number | +0.534 | +1.000 |
| `β` RBS strength | +0.534 | +1.000 |
| `k_sec` export rate | +0.107 | +0.200 |
| `μ` growth rate | −0.561 | −1.051 |
| `δ_m` mRNA decay | −0.486 | −0.909 |
| `δ_s` surface loss | −0.107 | −0.200 |
| `δ_c` cytoplasmic loss | −0.021 | −0.038 |

Three design messages fall out, and the first one is new.

**The limiting resource moved from the gene to the membrane.** At 46.6%
occupancy the promoter, copy number and RBS are halved to +0.53, and anchor
capacity arrives at +0.47 having been irrelevant. **Only `f` keeps its full
+1.00**, because it multiplies the surface pool after all the saturation has
happened. The productive handles are the folding fraction and the display
scaffold. No copy number whatever can pass `f`·`P_s,max` = 50,000 sites.

**`k_sec` is a weak lever, and weaker than it looked.** It appears in the
numerator and the denominator of the closed form, so raising it mostly moves
protein from inside the cell to the surface without making more of it. Above
about 1 min⁻¹ the site count flattens near 26,000 and export stops limiting
anything at all. Do not spend effort there.

⚠ **Growing faster does not cost you sites per litre.** `μ` is the strongest
negative sensitivity, which invites exactly the wrong conclusion. Site density
is weakly hyperbolic in `μ`; biomass is exponential in it. Slowing growth
four-fold raises per-cell density 1.6× and cuts capture **per litre** about a
thousand-fold. The steady state above is a **pre-load target reached in a
separate vessel**, not a condition to hold in the leach liquor. ISSUES 61.

## Handover 2 — turning sites per cell into `q_max`

the recovery-chain document needs capacity per gram of cells, not per cell:

```
q_max [µM/(g/L)]  =  A [sites/cell] × cells_per_g / N_A × 1e6
```

| Route | Sites/cell | `q_max` |
|---|---|---|
| the GolB display document ODE at `μ` = 1.2 h⁻¹, `N` = 300 | 23,301 | **0.0913 ← adopted** |
| **Every anchor filled** | **50,000** | **0.1961 ← engineering target** |
| Same ODE at `N` = 20, retired 2026-08-19 | 2,749 | 0.0108 |
| Retired value | 742,225 needed | 4.4000 |

That retired value needed 742,225 sites on a cell that has 100,000 anchor
points.

## What it does to the capacity ceiling

the recovery-chain document §2.1 says capture turns over at `q_max · X_max`. At `X_max` = 5 g/L:

| `q_max` | Capacity ceiling | |
|---|---|---|
| **0.0913, adopted** | **0.457 µM** | today |
| 0.1961, engineering target | 0.980 µM | 2.15× away |
| 0.0108, retired 2026-08-19 | 0.0539 µM | before the copy-number correction |
| 4.4, retired | 22.0 µM | needed an impossible cell |

**The bottom of the recommended window is now reachable.** The window was
revised from 10–20 µM to 0.4–0.8 µM on 2026-08-11, conditional on the
engineering target. Since 2026-08-19 the in-use ceiling, 0.457 µM, lands
**inside** that window rather than below all of it, so a 0.4 µM feed is the
first feed in the window that is not capacity-limited. At the feed the leach
actually delivers, 29 µM, capture is still capacity-limited by 63×.

What it costs, at a 10 µM feed: `eta_capture` falls from 99.2% at the retired
`q_max` = 4.4 to 4.5%. That is a factor of 22, not the factor of 100 it was
before the copy-number correction.

The `A_tox` analysis above 30 µM never comes into play, because capture is
capacity-limited long before toxicity matters.

## The one piece of good news

⚠ **This section used to be the good news and it is now the warning.** The
construct uses 23,301 of a possible 50,000 sites. That is 46.6%, not 5.5%. The
engineering headroom that was 18× is **2.15×**. Filling every remaining anchor
takes the ceiling from 0.457 to 0.980 µM and the mismatch against a 29 µM feed
from 63× to 30×. **Display density can no longer close this gap on its own,
and no copy number can, because `f`·`P_s,max` = 50,000 is a hard stop.**

Equilibrium capture at `X_max` = 5 g/L, recomputed 2026-09-18 with
`K_Au = 0.7 µM`:

| Feed | `q_max` = 4.4 | **0.0913, in use** | 0.1961 target |
|---|---|---|---|
| 0.05 µM | 96.9% | **38.5%** | 57.6% |
| 0.5 µM | 96.9% | **30.3%** | 50.9% |
| 1 µM | 96.8% | 23.8% | 43.7% |
| 10 µM | 94.7% | 4.3% | 9.1% |
| 50 µM | 43.0% | 0.9% | 1.9% |

The sourced affinity proxy lowers the low-feed result substantially. At the
current display density, dilution alone does not produce high capture; both
more usable GolB capacity and a lower feed concentration are required.

**Biomass is a second lever, and it is open.** *E. coli* is published at
128–148 g/L against the 5 g/L assumed here, so biomass is worth up to 26× — more
than display density now has left to give. **Biomass has become the larger of
the two levers.** ISSUES 26.

## Open issues touching this step

| Issue | One line |
|---|---|
| [3](ISSUES.md) | ~~The reported `P_s` and `A` come from different calculations. 5.5% gap.~~ **Closed 2026-08-19 by draft 4's saturating closed form, which reproduces the ODE to 1e-14.** ISSUES 61. |
| [1](ISSUES.md) | `K_Au` now uses the fitted 0.7 µM GolB-based literature proxy from S78; Part II's 10 µM remains a placeholder. |
| [22](ISSUES.md) | Project-matrix constants remain unknown. `alpha` = 52 from S79 is a conservative GolS-derived competition scenario, not a measured GolB constant. |

## The one decision this step forces

Set a display-density milestone for the wet lab, as a multiple of the current
23,301 sites per cell, and set the dilution factor for the leachate. Those two
numbers together fix `eta_capture`. **Since 2026-08-19 they are no longer equal
partners:** display density has 2.15× left in it and dilution has the rest.

**Answered 2026-08-11, and it weakens the target.** [S29](SOURCES.md) Jose &
Meyer says autodisplay exports "**more than** 100,000 recombinant molecules per
single cell". So 1×10⁵ is a demonstrated **floor**, not a hard ceiling, and
0.1961 is a design anchor rather than a physical limit. It may be exceeded.

---

# Capture and recovery

The current technical recovery report is [RECOVERY_MODEL.md](RECOVERY_MODEL.md),
built with live tables to [RECOVERY_MODEL.docx](RECOVERY_MODEL.docx). It owns the
recovery equations, results, graphs and calibration requirements. The earlier
[RECOVERY.md](RECOVERY.md) retains the review and correction narrative. The recovery-only wiki
proposal is [WIKI_RECOVERY.md](WIKI_RECOVERY.md).

The [capture investigation](CAPTURE_INVESTIGATION.md) corrects the scope:
expression predicts single-site occupancy, not a universal whole-cell loading
ceiling. S76 provides relevant whole-cell evidence in different chemistry.

Capture combines the Langmuir relation with a gold mass balance and recomputes
display capacity through Joint 2. In the report scenario, the GolB site pool is
small compared with the gold fed. This motivates measuring accessible capacity
and background adsorption in actual leachate. It does not establish that gold
is harmless or that upstream chemistry is irrelevant.

Elution is represented by a first-order release law. Its endpoint and rate are
one internally consistent S60 working scenario: `phi = 0.03` and
`k_elute = 0.22 h^-1`, under 0.1 M thiourea, 0.1 M sulfuric acid, 50 °C and
1 g sorbent/L. A GolB-comb time course must replace both the transferred values
and the provisional rate-law choice.

Reduction uses a donor-coupled Finke-Watzky scenario. The reference converts
nearly all delivered gold, but the full kinetic ranges include very low
conversion. MerA electron-transfer kinetics do not validate particle nucleation
by this project's protein in Au(I)-thiourea. Electron sufficiency is an upper
bound, not proof of completion. Fixed effective constants also do not establish
how rates change with protein dose. The trajectory model compares that default
with an explicitly hypothetical linear dose law and checks both gold and
reducing-capacity conservation throughout the batch.

The protein-production model now uses actual logistic growth for per-cell
dilution. Stationary synthesis and decay require calibration, so the old
protein-deficit and harvest-time recommendations are withdrawn. The damage
coefficient in the capture-growth model remains unmeasured because its source
formula has incompatible dimensions. Equilibrium capture does not require it.

The recovery metric is metal formed per initial volume under explicit stage
volume and transfer assumptions. The process interface computes lysate dilution
and preserves biomass inventory when volumes change. Physical collection remains out of scope.
Dilution must be evaluated with an amount balance and total biomass cost.

The earlier PRCC table is not a current result: its sampling design and model
regime do not support reuse. Historical reasoning is preserved in
[ISSUES.md](ISSUES.md), especially items 63 and 84–89. Current uncertainty
communication uses explicit kinetic scenarios, not a probability claim.
