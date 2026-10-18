# Capturing dissolved gold: design analysis

<!-- **Tier 3, synthesis.** Stage 3 rework, started 2026-10-16. Repository marker; do not copy this comment to the wiki. -->

<!--
Working skeleton. Each design question moves one lever the team controls,
computes how captured gold responds, and ends in a choice. Template:
  Question -> Lever -> Response -> Equations -> Result (Output, Check)
  -> Design decision.
If a section does not end in a choice, it is not a design analysis.
Equations are numbered (3.x) and introduced by one sentence in words.
Assumptions are numbered and cited at the equation that uses them.
Plant basis: 1 tonne of PCB a day (AGENTS.md section 4). Analyse on the 1 L
bench basis in params/leach.yaml feed_basis, report at 1 t/day.
q_Au = 4.62 umol/g from S76, the author's decision of 2026-10-17 (AGENTS.md section 4).
Every number used by docs/capture_design_analysis.py lives in params/capture_design.yaml.
-->

## Introduction

After leaching, gold is dissolved as gold-thiosulfate. To pull the gold out,
we grow *E. coli* that display GolB on the leaves of a comb, and we dip the
comb into the liquid. GolB holds metal between two sulfur atoms, from the two
cysteines in its Cys-X-X-Cys motif.

However, leaching dissolves much more copper than gold, and copper can bind
to the same spot. Every site that holds copper is a site that cannot hold
gold.

<!-- TODO: closing sentence, pending author's confirmation:
"So we wanted to know how much gold the comb can hold, how fast it fills, and
how much of it copper takes away." -->

## Approach

<!-- TODO: one paragraph, no numbers, written last. -->

Capture has three levers. Each design question below moves one of them and
asks what happens to the gold we capture.

| # | Design question | Lever | Response | Choice it makes |
|---:|---|---|---|---|
| Q1 | How many cells per litre of leachate? | Dry cells per litre | Gold captured | The cell loading where adding cells stops adding gold |
| Q2 | How much comb area, and how many dips? | Panel area, dips | Area needed per litre | The area per litre, and the comb that delivers it |
| Q3 | How long do we dip? | Contact time | Gold captured over time | The dip time, and whether to stir |

The fraction of gold captured is a result of these choices, not a target we
set.

<!-- TODO: schematic of the five levers and what each hands on. -->

## Input from bioleaching

Capture uses the same starting basis as the bioleaching model: **1 L of
leachate from 100 g of crushed board carrying 20 mg (101.5 µmol) of gold**
(`Bioleaching_Models_v8.docx`, stage 3 parameters;
`params/leach.yaml` `feed_basis`).

The design case is the one the bioleaching model recommends: a 24 h leach
with ammonia, which dissolves 36.6 % of the gold. Capture therefore
receives:

    (3.0)  n_Au,in = 37.2 µmol of dissolved gold, in V = 1 L of leachate

Capture is sized against three feeds, so the design does not depend on which
leach chemistry the project settles on:

| Case | Gold | Copper that can compete | Source |
|---|---:|---:|---|
| No ammonia | 20.0 µM | none counted | bioleaching v8, 24 h, 19.69 % leached |
| Ammonia | 37.2 µM | up to 858 µM | bioleaching v8, 24 h; 858 µM is the Cu(II) peak at about 29 h |
| High-grade case | 44.0 µM | 6000 µM | the author's case; not in the bioleaching documents |

Capture takes these as given. When the bioleaching model changes, only these
inputs change here, and every capture result follows.

## Definitions

<!-- TODO: one table for the whole stage. Columns: Symbol | Unit | Meaning |
Value [source]. Levers are swept. Results carry "-". Literature values are
marked apart from this team's measurements. -->

| Symbol | Unit | Meaning | Value [source] |
|---|---|---|---|
| `n_Au,in` | µmol | Dissolved gold received from bioleaching, per batch | 37.2 [bioleaching model, 24 h with ammonia; see Input from bioleaching] |
| `V` | L | Leachate volume per batch | 1 [bioleaching model basis] |
| `q_Au` | µmol/g | Gold held per gram of attached dry cells | 4.62 [S76, whole-cell displayed GolB in *E. coli*; literature, other conditions] |
| `Kd_Au`, `Kd_Cu` | µM | Dissociation constants of GolB for Au(I) and Cu(I) | 3.0 × 10⁻³¹ and 1.6 × 10⁻¹¹ [S76, measured on GolB: 3.02 × 10⁻³⁷ M and 1.61 × 10⁻¹⁷ M] |
| `[Cu]_in` | µM | Copper able to compete, reaching the comb | 0 to 6000 [see Input from bioleaching] |

| `X` | g/L | Dry cells per litre of leachate | Lever, Q1; chosen 9.5 |
| `A` | m² | Panel area, both faces counted | Output of Q2 |
| `L`, `W`, `t_panel` | m | Panel length, width and thickness | 0.10, 0.10 and 0.001 [the 1 L comb] |
| `n_panel` | – | Panels on one comb | 2 [the printed comb as built] |
| `n_comb` | – | Combs on one branch | 12 [design choice] |
| `V_leach` | L | Leachate the comb is dipped into | 1.0 [bioleaching batch basis] |
| `g` | mm | Gap between adjacent leaf faces | – (fixed by `A` and `V_leach`) |
| `ρ_A` | g/m² | Dry cells one m² of colonised panel carries | 6.36 [measured on the project's combs, see Q2] |
| `D` | – | Dips the comb makes per batch | 4 [design choice] |
| `φ`, `k_elute`, `t_elute` | –, h⁻¹, h | Gold left bound after elution, first-order release rate, elution time | 0.03, 0.22 and 6 [S60, transferred; not measured on GolB. `t_elute` is the wiki reference scenario] |
| `C` | µmol | Gold a freshly released comb can hold | – |
| `f_rel` | – | Share of the held gold that one elution releases | – |
| `n` | – | Dips needed to capture the gold in a batch | – |
| `t_c` | min | Contact time of one dip | Output of Q3 |
| `a₀` | µM | Gold in the batch when a dip starts | – |
| `s₀` | µM | Free sites on the comb when a dip starts | – |
| `x` | µM | Gold bound so far in the dip | – |
| `f` | – | Share of the scarcer pool a dip must consume | 0.99 [design choice] |
| `k_on` | µM⁻¹ h⁻¹ | Association rate of gold onto a GolB site | 1.0 [S57, a floor; see Q3] |
| `D_w` | m²/s | Diffusivity of the gold complex in water | 6 × 10⁻¹⁰ [order of magnitude, **not sourced**] |
| `t_film` | µm | Biofilm thickness | 30 [assumption, not measured] |
| `[Au]_in` | µM | Dissolved gold in the leachate reaching capture | – |
| `[B]` | µM | Binding sites the cells supply per litre of leachate | – |
| `[Au]`, `[Cu]` | µM | Free dissolved gold and copper left in the leachate | – |
| `[AuB]`, `[CuB]` | µM | Gold and copper bound to the cells, per litre of leachate | – |
| `a` | m²/L | Wetted comb area per litre of leachate, both faces | – |

## Assumptions

1. All dissolved gold from the leach reaches the comb: filtration loses none,
   and the gold stays as gold-thiosulfate.
2. Each binding site holds one gold atom, and `q_Au` counts the sites per gram
   of cells.
3. The cells cover the whole growing surface of the comb, at `ρ_A` grams per
   square metre. The comb's two flat panel faces are the growing surface; the
   rib and the 1 cm depth are structure.
4. The vessel is well mixed, so every dip time is set by binding and not by
   transport. Q3 shows what a still vessel would cost.
5. Gold and copper bind one shared class of sites, reversibly, one metal per
   site.
6. All the copper in the stated total is able to bind: it counts as effective
   competing copper.
7. One `k_on` describes binding on the comb. Q3 uses the only published
   value, measured on another organism, and treats it as a floor.
8. GolB's measured dissociation constants apply in the leachate. The
   thiosulfate that holds the gold does not weaken the binding.
9. Each dip fills every site that the last elution freed, from a leachate that
   still holds gold. How long a dip takes is Q3.
10. Elution is first-order with a residual that stays bound. The gold left
   behind keeps its sites occupied, so a dip refills only the released share.

## Conversions

These equations are not analyses. They convert between gold, sites, cells
and comb area, and every design question uses them. All are per litre of
leachate, so they hold at any scale.

The dissolved gold reaching capture (assumption 1):

    (3.1)  [Au]_in = n_Au,in / V

The binding sites a cell loading supplies (assumption 2):

    (3.2)  [B] = q_Au · X

The comb area that carries that cell loading (assumption 3):

    (3.3)  a = X / ρ_A

For reference, one site for every gold atom, `[B]` = `[Au]_in`, needs
`X` = 8.04 g/L at the 37.2 µM feed and the S76 loading of 4.62 µmol/g. At
`ρ_A` = 6.36 g/m² that is 1.26 m² of comb per litre. Q1 decides how many cells
are worth adding; Q2 decides how to hold them.

Computed by `docs/capture_design_analysis.py`: `sites`, `comb_area` and
`cells_for_sites`.

## Q1. How many cells per litre of leachate?

**Lever.** Dry cells per litre, `X`.

**Response.** Gold captured at equilibrium, with copper competing for the same
sites.

### Equations

Gold is either still dissolved or bound to the cells, and the same holds for
copper (assumption 1):

    (3.4)  [Au]_in = [Au] + [AuB]
           [Cu]_in = [Cu] + [CuB]

Both metals draw on one shared class of sites. At equilibrium each metal's
share of the sites follows its own concentration divided by its dissociation
constant (assumptions 2, 4, 5, 6 and 7):

    (3.5)  [AuB] = [B] · ([Au]/Kd_Au) / (1 + [Au]/Kd_Au + [Cu]/Kd_Cu)
           [CuB] = [B] · ([Cu]/Kd_Cu) / (1 + [Au]/Kd_Au + [Cu]/Kd_Cu)

The constants are GolB's own, measured by Wei et al. (S76): `Kd_Au` =
3.0 × 10⁻³¹ µM and `Kd_Cu` = 1.6 × 10⁻¹¹ µM. Both lie more than thirty orders
of magnitude below the gold in the leachate, and gold is held 5 × 10¹⁹ times
more tightly than copper. In that limit (3.5) reduces to a bookkeeping rule:

    (3.6)  [AuB] = min( [Au]_in , [B] )
           [CuB] = min( [Cu]_in , [B] − [AuB] )

Gold takes every site it needs. Copper takes only what is left.

Capture therefore climbs in a straight line, one gold atom per site, until
every gold atom has a site, and then stops. There is no bend to optimise. The
copper in the leachate does not reduce gold capture at any concentration: it
can only occupy sites that gold has no use for.

The cell loading follows from the margin `m`, the binding sites supplied per
gold atom, with `m` = 1 the floor:

    (3.7)  X = m · [Au]_in / q_Au

### Result

**Output.** Gold captured (%), at `q_Au` = 4.62 µmol/g:

| `X` (g/L) | No ammonia, 20.0 µM | Ammonia, 37.2 µM | High-grade, 44.0 µM |
|---:|---:|---:|---:|
| 4 | 92.4 | 49.7 | 42.0 |
| 8 | 100.0 | 99.5 | 84.0 |
| 12 | 100.0 | 100.0 | 100.0 |
| 20 | 100.0 | 100.0 | 100.0 |

Copper held on the comb (µM), with 858 µM copper for the ammonia feed and
6000 µM for the high-grade feed:

| `X` (g/L) | No ammonia | Ammonia | High-grade |
|---:|---:|---:|---:|
| 4 | 0.0 | 0.0 | 0.0 |
| 8 | 0.0 | 0.0 | 0.0 |
| 12 | 0.0 | 18.3 | 11.4 |
| 20 | 0.0 | 55.2 | 48.4 |
| 40 | 0.0 | 147.6 | 140.8 |

The floor, one site per gold atom, is the same rule for every feed: **0.216 g
of dry cells per µmol of gold**.

| Feed | Gold | Cells at the floor | Comb at 6.36 g/m² |
|---|---:|---:|---:|
| No ammonia | 20.0 µM | 4.33 g/L | 0.68 m²/L |
| Ammonia | 37.2 µM | 8.04 g/L | 1.26 m²/L |
| High-grade | 44.0 µM | 9.52 g/L | 1.50 m²/L |

Computed by `docs/capture_design_analysis.py`.

<!-- TODO: graph, to be chosen with the author. -->

**Check.**

<!-- TODO: compare the straight-line rise with a published whole-cell gold
loading curve. -->

Not yet checked.

### Design decision

**Load 9.5 g of dry cells per litre of leachate**, the floor for the richest
feed, 44 µM (`m` = 1.0).

It serves every feed above it. At 9.5 g/L the cells capture all the gold in the
20.0 µM, 37.2 µM and 44.0 µM feeds. The spare sites in the leaner feeds hold
copper, 6.8 µM in the ammonia feed.

**Why not more.** Every gram above the floor captures copper, not gold: 4.6 µM
more copper for each extra g/L. At 12 g/L the high-grade feed carries 11.4 µM
of copper on the comb for no extra gold.

**Why not less.** Capture falls in a straight line below the floor. Each gram
short of 9.5 g/L loses 4.6 µmol of the 44 µmol of gold.

**This is an upper bound.** The floor has no margin, and the result rests on
assumption 7: that GolB's bare-ion constants hold in the leachate. S76 measured
them with no competing ligand, and in the leachate thiosulfate holds the
gold. If that weakens the binding, capture falls below the 100 % shown and the
loading needs a margin, `m` > 1. The margin is the parameter `design_margin`
in `params/capture_design.yaml`; set it once gold capture against cell loading
has been measured in the real leachate. Each 0.1 adds 4.4 µM of copper to the
comb at the high-grade feed (Q5).

Q2 now asks how big a comb must be to deliver that, and how many dips it takes.

## Q2. How much comb area, and how many dips?

**Lever.** The panel area the cells are grown on, and the dips the comb makes
per batch.

**Response.** Whether the area carries the cells Q1 asked for.

### Equations

Q1 gave the cells one litre needs: `X` = 9.52 g/L. Cells grow on the panel
surface, so the area follows from one number: how many dry grams of cells a
square metre of colonised panel carries.

    (3.8)  ρ_A = 6.36 g of dry cells per m² of panel

    (3.9)  A = X · V / ρ_A

`ρ_A` is a measurement, not a calculation. The wet lab grew the culture on a
comb, dried it and weighed it, and divided by the comb's area.

A comb used once must carry all the cells at once. Dipping again reuses the
same panels, so the area divides by the dips (assumption 8):

    (3.10)  A = X · V / (ρ_A · D)

### Result

**Output.** The area one litre of leachate needs, at 6.36 g of dry cells per
m²:

    A = 9.52 g/L ÷ 6.36 g/m² = 1.50 m² per litre, used once

| Leachate | Cells needed | Area, used once |
|---:|---:|---:|
| 1 L | 9.5 g | 1.50 m² |
| 2 L | 19.0 g | 2.99 m² |
| 5 L | 47.6 g | 7.48 m² |
| 10 L | 95.2 g | 14.97 m² |
| 20 L | 190 g | 29.9 m² |
| 50 L | 476 g | 74.8 m² |
| 100 L | 952 g | 150 m² |

It is a straight proportion: **1.50 m² for every litre**, whatever the scale.

Dipping the same comb again divides that area:

| Dips per batch | Area per litre |
|---:|---:|
| 1 | 1.50 m² |
| 2 | 0.75 m² |
| **3** | **0.50 m²** |
| 5 | 0.30 m² |

Computed by `docs/capture_design_analysis.py`: `areal_density` and
`area_needed`.

<!-- TODO: graph, to be chosen with the author. -->

**Check.**

`ρ_A` comes from the project's own combs, so it needs no transfer from the
literature. No published areal biomass figure was found for a comparable
biofilm to compare it against.

### Design decision

**1.50 m² of panel per litre of leachate, or 0.50 m² per litre at three dips.**

The area is a straight proportion, so it carries to any volume without a new
calculation. What it does **not** fix is how the area is built. That is a
hardware choice, and the 1 L comb below is the worked example of one.

**It rests on one measured number.** `ρ_A` = 6.36 g/m² was weighed on the
project's own combs. Halve it and the area doubles, so this is the parameter
every area in this stage is most sensitive to. The raw area and mass behind it
are not recorded here.

## Q2 worked: the 1 L comb

This is how 0.50 m² was built at the bench, and how the same steps give a comb
at any other volume.

**The unit.** One comb is two panels of 10 × 5 cm on a central rib, with a stem
and disc that plug into a branch. Both flat faces of each panel carry cells;
the 1 cm depth of the rib is structure, not growing surface:

    one comb = 2 panels × 2 faces × 0.10 × 0.05 = 0.0200 m²

**Each dip is fresh.** A dip starts with a comb whose sites are all free, so a
dip takes the comb's whole capacity, not a share of it:

    gold per dip = A · ρ_A · q_Au = 0.0200 × 6.36 × 4.62 = 0.588 µmol per comb

The 6 h strip then releases 71.1 % of what the comb holds, which is how much
of the captured gold reaches the next stage, not how much the next dip can
take:

    (3.11)  f_rel = (1 − φ) · (1 − e^(−k_elute · t_elute)) = 0.711

**The count.** 0.50 m² is 25 combs. Thirty were chosen, and the reason is
Q3: the dip time blows up when a dip's capacity lands on the gold still in the
batch. Thirty combs clears the batch in three dips with no such collision.

| Combs | Area | Cells | Gold per dip | Dips | Contact time |
|---:|---:|---:|---:|---:|---:|
| 20 | 0.400 m² | 2.54 g | 11.8 µmol | 4 | 116 min |
| 24 | 0.480 m² | 3.05 g | 14.1 µmol | 4 | 124 min |
| 28 | 0.560 m² | 3.56 g | 16.5 µmol | 3 | 70 min |
| **30** | **0.600 m²** | **3.82 g** | **17.6 µmol** | **3** | **60 min** |
| 36 | 0.720 m² | 4.58 g | 21.2 µmol | 3 | 95 min |

**The dips.** Dips are whole: a dip is a full cycle of dipping, lifting and a
6 h strip, and it cannot be stopped part way.

| Feed | Gold | Dips at 30 combs |
|---|---:|---:|
| No ammonia | 20.0 µM | 2 |
| **Ammonia (design case)** | **37.2 µM** | **3** |
| High-grade | 44.0 µM | 3 |

A cycle is one 30 min dip plus one 6 h strip, so three cycles fit in 24 h and
a batch is cleared inside a working day.

**The spacing.** The leachate sits between the panels, so the gap is fixed once
the area and the batch are set:

    (3.12)  g = V / (A / 2) = 1 L ÷ 0.30 m² = 3.33 mm

    (3.13)  V_vessel = (A / 2) · (g + t_panel) = 1.30 L

**The bench comb:**

| Quantity | Value |
|---|---:|
| Combs | 30 |
| Panels of 10 × 5 cm | 60 |
| Area, both faces | 0.600 m² |
| Cells carried | 3.82 g |
| Gold per dip | 17.6 µmol |
| Dips, design feed | 3 |
| Gap between panel faces | 3.33 mm |
| Stack height, one column | 26.0 cm |
| Vessel | 1.30 L |

**What this shows for a larger comb.** The area scales, the comb need not. At
10 L the area is 5.0 m² at three dips. Reaching that with 10 × 5 cm panels
takes 300 combs, which is not the sensible build: fewer, larger panels give
the same area, and the model treats them the same way. The one thing that does
not improve with size is the area a vessel can pack: it is 2 ÷ (gap + panel
thickness) per cubic metre, about 0.5 m² per litre of vessel at a 3 mm gap, at
every scale.

**Two open hardware questions:**

1. **Drainage.** In the printed comb the panels are recessed inside a raised
   frame, so each is a shallow tray that holds liquid when lifted. That liquid
   is carried into the thiourea, where it dilutes the product. The frame should
   be flush or removed.
2. **The gap.** 3.33 mm is tighter than the 4 mm of the first sketch. A larger
   comb in the same litre closes it further, and the gap at which a lifted
   stack stops draining is not known.

## Q3. How long do we dip?

**Lever.** The contact time of one dip, `t_c`.

**Response.** The share of the scarcer pool consumed by the end of the dip.

Q1 and Q2 assumed each dip reaches equilibrium (assumption 4). Q3 asks how
long that takes, and whether the comb or the liquid sets the pace.

### Equations

Binding is effectively irreversible (Q1) and one site takes one gold atom, so
the gold bound in a dip, `x`, grows at a rate set by what is left of both
pools: the gold still in the batch and the sites still free on the comb.

    (3.14)  dx/dt = k_on · (a₀ − x) · (s₀ − x)

`a₀` is the gold in the batch at the start of the dip and `s₀` the free sites
on the comb, both in µM. Neither one is in large excess over the other —
Q1 sizes them to match — so the dip time depends on both. Integrating:

    (3.14a)  t_c = ln[ s₀(a₀ − x) / (a₀(s₀ − x)) ] / (k_on · (a₀ − s₀))

    (3.14b)  x = f · min(a₀, s₀)

`f` is measured against whichever pool runs out first, because the other one
cannot be emptied. When the two pools are equal, (3.14a) is 0/0 and the limit
is `t_c = f / (k_on · a₀ · (1 − f))`.

Two transport steps happen alongside the binding. Gold must cross the liquid
between the panels, and then diffuse into the biofilm:

    (3.15)  t_film = 30 µm

    (3.16)  t_diff ≈ L² / (2 · D_w)

`L` is the distance to cross: half the panel gap for the liquid, the film
thickness for the biofilm.

A batch takes several dips, and each dip starts poorer than the last. Dip `i`
begins with the gold the previous dips left, against the sites the strip
released:

    (3.17)  a₀,ᵢ₊₁ = a₀,ᵢ − f · min(s₀, a₀,ᵢ)

### Result

**Output.** The 1 L comb carries 3.82 g of cells, which is 17.6 µM of sites.
At `k_on` = 1.0 µM⁻¹ h⁻¹, against the 44 µM design feed:

| Consumed | Dip time |
|---:|---:|
| 50 % | 1.1 min |
| 90 % | 4.2 min |
| **99 %** | **9.3 min** |
| 99.9 % | 14.6 min |

**The dip time depends on both levers.** Minutes to 99 %:

| Cells on the comb | Sites | 20 µM feed | 37 µM feed | 44 µM feed |
|---:|---:|---:|---:|---:|
| 1.00 g | 4.6 µM | 17.0 | 8.2 | 6.8 |
| 2.00 g | 9.2 µM | 22.3 | 9.3 | 7.5 |
| **3.82 g (the 1 L comb)** | **17.6 µM** | **64.9** | **12.2** | **9.3** |
| 6.00 g | 27.7 µM | 26.0 | 20.7 | 13.4 |
| 9.52 g (Q1, one dip) | 44.0 µM | 10.0 | 24.6 | **132.4** |

Read down a column and the time does not fall as the cells rise. It peaks
where the sites match the gold, and that peak is sharp. At 9.52 g against the
44 µM feed the two pools are equal, and the last per cent of a one-for-one
reaction takes longer than everything before it: 132 min, against 9 min for
the same feed on the 30-comb branch. The 3.82 g row shows the same trap from
the other side: against the lean 20 µM feed, that branch is itself almost an
exact match, and the dip stretches to 65 min.

**Dip by dip**, the 1 L comb clearing the 44 µM batch. Each dip starts with a
fresh comb and the gold the dip before it left:

| Dip | Gold left | Dip time |
|---:|---:|---:|
| 1 | 44.0 µM | 9.3 min |
| 2 | 26.5 µM | 23.8 min |
| 3 | 9.1 µM | **27.3 min** |
| | | **60 min total** |

The later dips are the slow ones. Dip 3 meets 9.1 µM of gold with 17.6 µM of
sites, so the gold is what runs out, and finding the last atom takes time.

**This is what fixed the comb at 30.** The dip time blows up when a dip's
capacity lands near the gold left in the batch, so the comb count is not free:

| Combs | Dips | Contact time | Slowest dip |
|---:|---:|---:|---:|
| 20 | 4 | 116 min | 71 min |
| 24 | 4 | 124 min | 78 min |
| 28 | 3 | 70 min | 41 min |
| **30** | **3** | **60 min** | **27 min** |
| 36 | 3 | 95 min | 70 min |
| 38 | 2 | 158 min | 148 min |

Fewer combs is not simply slower, and more combs is not simply faster. The
good counts are the ones whose capacity never collides with the remainder.

**What else takes time**, as an order of magnitude only. Both diffusivities
are estimates, not sourced:

| Step | Distance | Time |
|---|---:|---:|
| Into the biofilm | 30 µm | 1.5 s |
| Across half the panel gap, still liquid | 1.7 mm | 39 min |
| Binding, slowest dip | – | 27 min |

Computed by `docs/capture_design_analysis.py`: `dip_time`, `binding_time`,
`dip_schedule`, `film_thickness` and `diffusion_time`.

<!-- TODO: graph, to be chosen with the author. -->

**Check.**

S58 reports surface-engineered *E. coli* reaching adsorption equilibrium in
**40 min**. The three dips here run from 9 to 27 min, the same order. The two
are not the same system, so this is a sanity check, not a validation.

### Design decision

**Dip for 30 minutes, the same 30 minutes every dip, and stir the vessel.**

**Why 30 minutes.** The slowest of the three dips reaches 99 % in 27 min. One
fixed time covers all three, so the operator times no dip individually and no
dip is lifted early. Three dips is 1.5 h of contact against three 6 h strips.

**Why stir.** The biofilm is not the limit: gold crosses a 30 µm film in
seconds. The liquid is. In a still vessel gold takes about 39 min to diffuse
across half the 3.33 mm gap, which is longer than any of the three dips.
Stirring or circulating the leachate removes that limit and leaves binding in
control. Without it the dip time is set by transport, not by the comb.

**Do not size the comb to match the gold.** This is the design result of Q3,
and it chose the comb in Q2 worked. Q1 gives the floor — one site per gold
atom — and a comb built at that floor is the slowest comb there is, because
the reaction has to find the last free site with the last gold atom. Several
smaller dips are faster in total than one dip on a comb large enough to take
everything.

**The dip time scales with the cells and the feed, not the batch volume.** Two
litres with twice the comb holds the same cells per litre and the same gold
per litre, so every dip time above is unchanged. Scale moves the hardware,
not the clock.

**What is uncertain.** `k_on` = 1.0 µM⁻¹ h⁻¹ was measured on wild-type
*Pseudomonas* with gold chloride at pH 3, and its own source note calls it a
**floor**, so the real binding may be faster and the dip shorter. Every time
in this section is inversely proportional to it: a `k_on` twice as large
halves all of them. The diffusivities are order-of-magnitude estimates with no
source. What they support is the comparison, not the numbers: transport in a
still vessel is slower than binding, so the vessel must be stirred.

<!-- Inconsistency to log: WIKI_BIORECOVERY_DRAFT.md uses 29 uM gold in the
leachate; (3.1) gives 37.2 uM (ammonia) or 20.0 uM (no ammonia) from the
bioleaching model. Log in ISSUES.md once the author confirms which leach case
applies. -->

## Stage ledger

The analyses work per litre of leachate. The ledger reports them at the plant
basis of 1 tonne of board a day (AGENTS.md section 4). At the bench pulp
density of 100 g of board per litre (`params/leach.yaml`
`feed_basis.pcb_loading`), that is 10 000 L (10 m³) of leachate a day.

**The plant column is our projection** from the 1 L result. The bioleaching
documents are per litre and contain no tonne basis.

Ammonia feed (37.2 µM gold, 858 µM copper) at `X` = 9.5 g/L. The capture shown
is an upper bound (see Q1):

| Quantity | Bench, 1 L | Plant, 1 t board/day |
|---|---:|---:|
| Leachate treated | 1 L | 10 000 L/day |
| Gold in | 7.32 mg | 73.2 g/day |
| Gold captured (100 %, upper bound) | 7.32 mg | 73.2 g/day |
| Gold lost in the spent leachate | 0 | 0 |
| Dry cells to hold one batch once, no reuse | 9.5 g | 95.2 kg/day |
| Copper held with the gold | 0.43 mg | 4.3 g/day |
| Panel area at three dips | 0.50 m² | 4 216 m² |

Computed by `docs/capture_design_analysis.py`, the ledger section.

## Limitations

- **The result is an upper bound.** S76 measured GolB's dissociation constants
  with no competing ligand. In the leachate, thiosulfate holds the gold, and
  if that weakens the binding, capture falls below 100 % and the loading needs
  a margin. An earlier run that corrected for thiosulfate with estimated
  stability constants gave about 90 % capture at 12 g/L. That correction was
  retired at the author's direction and is recorded in ISSUES 93. Gold capture
  against cell loading in the real leachate settles it.
- The copper that actually reaches the comb is unknown. The bioleaching model
  reports a Cu(II) peak of 858 µM at about 29 h, but not the value at 24 h,
  and it does not say how much of it is Cu(I), the form GolB binds. This
  affects the purity of the eluate (Q5), not gold capture (Q1).
- The 44 µM gold and 6000 µM copper case was supplied by the author and is not
  in the bioleaching documents. The model's own copper peak is 858 µM.
- The gold loading `q_Au` = 4.62 µmol/g comes from S76: *E. coli* displaying
  GolB, grown overnight with 50 µM gold chloride in LB. The concentration is
  close to this project's feed, but it is an end-point loading, not a fitted
  maximum, and it was not measured in gold-thiosulfate leachate. The floor in
  Q1 moves in direct proportion to it.
- The dip time rests on `k_on` = 1.0 µM⁻¹ h⁻¹, measured on a different
  organism with a different gold species at pH 3, and recorded in its own
  source note as a floor rather than a best estimate.
- The diffusivity of the gold complex, 6 × 10⁻¹⁰ m²/s, is an order-of-magnitude
  estimate with no source, as is the halving inside a biofilm. They are used
  only to compare transport with binding, never to set the dip time.
- The release parameters `φ` and `k_elute` come from an acid-thiourea study on a
  porphyrin polymer (S60), not on GolB, and the 6 h elution is a wiki reference
  scenario. The 3 cycles a day and the 71 % release follow from them.
- The later dips of a batch are the slow ones, because the leachate is leaner
  (3.17). Q3 answers this by fixing one dip time long enough for the slowest
  dip, which wastes time on the first dips.

## Held for later

- Comb reuse: S76 reports three adsorb-and-release cycles with an unchanged
  growth curve, and about 89 % gold release with papain. The project's acid
  thiourea route is untested for reuse.
- Plant scale: 3 162 m² of panel is a bench method scaled up. Industrial
  practice for gold from thiosulfate leach is a packed bed of resin or carrier
  particles, sized by bed volumes and cycles a day, with 500 to 3 600 m² of
  surface per m³ of bed. A bed of cell-coated carriers would replace the
  combs at scale. The industrial figures are unverified.
- Sensitivity: which parameter moves recovery most.
- Cost per gram of gold recovered.

<details>
<summary>Derivations</summary>

<!-- TODO: steps from the rate equations to the equilibrium forms; logistic
comb growth; staging derivation. -->

</details>
