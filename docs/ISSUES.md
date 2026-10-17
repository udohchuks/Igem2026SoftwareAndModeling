# Issues found while compiling the three documents

**Tier 2, record.** Append and supersede; never rewrite. A closed item keeps
the arithmetic it was closed with, and a later correction goes in a dated
banner above it rather than replacing the text. That is why numbers in closed
items disagree with the model today, and why chasing them is wasted effort.
`AGENTS.md` section 11.

**Nothing in the three source documents was changed.** Every item is recorded
here and left standing in the text. Where a discrepancy could be pinned by a
test, the test is named so that a future edit cannot hide it.

Open items are written in full, because they still need a decision. Closed
items are compressed to what was wrong, what was done, and what pins it.

| Status | Count |
|---|---|
| 🔴 **BLOCKING** | **2** |
| Open, needing a decision | 36 |
| Open, cosmetic only | 3 |
| Closed | 25 |
| **Total** | **66** |

**Second audit, 2026-08-12.** The first pass checked that Part I's new model
reproduces its own numbers. It does. The second pass asked what the model does
not contain at all, and found four things. Items 43 to 46.

🔴 **Item 44 is the second blocking item.** The leach vessel accumulates 47 mM
of tetrathionate and calls it an inert dead-end product. Tetrathionate is a
cysteine-blocking reagent, and the capture protein binds gold through a pair of
cysteines. The excess is 51,753 to 1, and was 437,506 to 1 before the cysteine
pool rose 8.5x on 2026-08-19. Nothing about the item turns on which figure it
is.

**Item 43 supersedes the advice given with item 39.** The Part I to Part III
joint is a scale mismatch of about **63x**, not a concentration that a stopping
rule can tune. It takes **11 grams** of dry cells per gram of board. Those two
figures were 2000x and 94 g until 2026-08-19; the shape of the problem did not
change with them.

**Updated 2026-08-12.** Part I's author delivered two finished models: the
original simultaneous one, and a new three-vessel sequential one. Each comes
with a write-up and a MATLAB implementation, both now in
`docs/source/sequential_2026-08-12/`. The sequential model is the primary
Part I process from today. Items 36 to 42 come from integrating and auditing
it. Items 8, 17 and 20 closed, because it supplied the values they waited for.

**Item 41 is the one to read.** The audit found that the process is decided by
a reaction nobody was watching, and that the fix costs nothing.

🔴 **Item 32 is blocking.** It was found on 2026-08-11 by reading the full texts
of papers this repository already cited. Published, replicated evidence says
TetH cannot fold into an active form in *E. coli* at the pH *E. coli* lives at.
Read it before quoting any Part I result.

---


**Capture investigation, 2026-09-07. Item 91:** single-site sizing verified;
whole-cell interpretation corrected; project-matrix capacity remains unmeasured.

**Capacity category error, 2026-09-07. Item 92:** `q_max` is a derived site
inventory standing in a slot the biosorption field fills by measurement. The
secretion model cannot reach the published loadings at any setting, so the gap
is a missing mechanism and not a parameter error. Three literature capacities
are recorded as labelled scenarios; none is adopted. Carries item 69 forward
and names the isotherm that closes both.

**Recovery implementation update, 2026-09-07.** Item 90 closes the missing
trajectory, volume-accounting and public-interface implementation work.
Kinetic transfer and wet-lab validation remain open.

| # | Finding | Status |
|---|---|---|
| 90 | Explicit gold/electron ledgers, volumes, dose hypotheses and readable inputs | Computational work closed; experimental calibration open |

**Recovery audit, 2026-09-06.** Items 84–89 supersede the recovery conclusions
below where stated. The older count table is a historical snapshot, not a
current census. Computational fixes do not constitute experimental validation.

| # | Current recovery finding | Status |
|---|---|---|
| 84 | Full kinetic ranges reverse the claim that reduction is unimportant | Analysis fixed; chemistry unvalidated |
| 85 | Fitter forced the largest observation to complete conversion | Fixed; calibrated measurement required |
| 86 | Ensemble requested removed stage; tied ranks and dilute capture were wrong | Fixed, regression tested |
| 87 | Protein dilution continued after growth stopped | Equation fixed; expression and harvest prediction need calibration |
| 88 | Damage coefficient and reaction descriptions did not match units or evidence | Invalid growth recommendation withdrawn; coefficient remains null |
| 89 | Wiki must distinguish scenario analysis, verification and validation | Revised report and wiki draft; wet-lab validation pending |

## Status at a glance

Updated 2026-08-12. **Closed** means this repository behaves correctly. Where a
source document still needs a matching edit, the item says so.

### Open

| # | Item | Who decides |
|---|---|---|
| **32** | 🔴 **BLOCKING — TetH forms inactive inclusion bodies in *E. coli* and needs acid to fold** | team, urgently |
| **44** | 🔴 **BLOCKING — the leach makes 47 mM tetrathionate, which blocks the cysteines GolB binds gold with** | wet lab, one experiment |
| 62 | Part II's copy number reached three parameter files and not the fourth, so the report quoted `q_max` twice with different values. Fixed and pinned 2026-08-20 | done; read it before the next joint change |
| **43** | **11 g of dry cells per g of board. The joint is a 63x scale mismatch, not a stopping-rule problem.** Was 94 g and 2000x before 2026-08-19 | team. Supersedes 39 |
| **41** | **Cu(I) re-oxidation decides the process. Oxygen has an interior optimum at about a sixth of the baseline** | team, cheap to act on |
| 45 | Part I names passivation in its prose and has no passivation term. Recovery is linear in the gold rate | Part I author |
| 53 | No liberation term. `A_Au` is constant at every crush size, so the coarse-crushing recommendation runs off the end of the model | team + wet lab, one leach |
| **54** | **Glycine replaces ammonia as the Cu(II) stabiliser. Doubles 24 h gold, halves thiosulfate use, food grade** | wet lab, two leaches |
| 55 | v5 reports 19.69 % gold at 24 h; its own rate description implies 27.75 %, which is what the model gives | document author |
| 56 | v5's sulfur conservation check counts molecules, not atoms, and misses 18.8 % of the charge | document author; fixed this side |
| 57 | v5's `k_cat` prose says 2.2 U/mg, its arithmetic uses 2.5. Stage-2 conversion is 85.6 % or 95.9 % | document author |
| 58 | v5's Stage-1 enzyme yield contradicts v5's own derivation by 1.64x, and the document uses both values | document author |
| **59** | **Ammonia beats glycine on 72 h gold, 100 % against 84 %. The two tie at 24 h and glycine hands downstream 7.5x less polythionate. Decision unchanged** | team, and it is made |
| 60 | Trithionate was dropped at Joint 1, understating the polythionate load 3.0x to 6.4x. Fixed 2026-08-19; the relative reactivity is still unmeasured | wet lab, one binding assay |
| **61** | **The plasmid is pUC-type high-copy, N = 20 -> 300. Sites per cell 2,749 -> 23,301; the capture ceiling and every downstream number move 8.5x. Closes item 3** | team, and it is confirmed |
| 63 | Every PRCC in the adopted regime was computed at `q_max` = 0.0108 and describes a regime the chain has left. The `K_Au` row is already known to be wrong | modelling, half a day |
| **64** | **Reduction has no slow step, it has a late start. A 1 % gold seed cuts the concentration factor from 10x to 4x, giving 89 % in 24 h. More reductase does nothing at all** | wet lab, one seeded reduction |
| 65 | The reduction test harness fed 100 uM of dithionite where the file says 4.6. Every published eta_reduce moved; conversion turns out not to be monotonic in gold. Fixed and pinned 2026-08-20 | done; read it before trusting a reduction number |
| **67** | **The reductase is on pET-24(+), a different vector family from the pJUMP proxy it borrows. `N` falls about 7.5x and `alpha` rises by an unknown T7 factor, so the 2.5x shortfall is unanchored in both directions.** GolB and TetH resolved 2026-08-20: both on pJUMP24-1A, pRO1600/ColE1, high copy, so N = 300 stands for both. Reductase expression lumped into one identifiable parameter, alpha_N_beta = 500, band 30-4080: the arm-B shortfall lands at **3.0x** and eta_reduce at 0.90 after lysis. **The band still spans 49.4x to 0.36x, so it decides the stage, and it is in no error bar in this repository** | wet lab: one gel lane, reductase as a fraction of total protein on the induced pET-24(+) strain |
| **68** | **The culture vessel is sized on a route the repository retired.** `k_syn` x `X` gives 0.00475 uM of TetH and 9.1 L of culture per litre; `enzyme_capacity`, the block that replaced it on 2026-08-11, gives 0.3653 uM and 0.12 L. **77x apart, and opposite in direction**: one concentrates the harvest, the other dilutes it. The gap is GolB's 23,301 molecules per cell standing in for TetH | modelling + wet lab: one activity assay on the induced TetH strain |
| **92** | **`q_max` is a parts count sitting where the field puts a measurement.** Building it multiplies surface protein by an unfitted `f` = 0.5, an assumed one gold per site and an interpolated `cells_per_g`; none of the four steps involves gold. The cascade's hard ceiling is 0.196 umol/g and the most favourable corner of every input reaches 0.753, against 4.62 and 5.2 umol/g measured for displayed GolB, so **no setting of the secretion model reproduces the measurement.** Literature capacities now run as labelled scenarios: 78-87% capture at the GolB loadings against 1.57% today. **None adopted**; `whole_cell_capacity` stays null. Supersedes the framing of 69 | wet lab, one isotherm, half a day |
| **69** | **Measured gold biosorption onto plain Gram-negative cells is 3,600x this model's engineered capacity.** Tsuruta 2004 reports 329 umol/g at 50.5 uM and 992 umol/g as a Langmuir maximum; `q_max` here is 0.0913 umol/g. If any of it transfers to Au(I) thiosulfate at pH 10, the capacity mismatch that drives this whole report is an artefact of counting only GolB sites | team + wet lab |
| 66 | The parameter files contradicted themselves: duplicate YAML keys served the wrong derivation, `Vmax` disagreed with its own arithmetic, and two notes quoted pre-ammonia-free recoveries. Fixed and pinned 2026-08-20 | done; two new tests enforce it |
| 46 | Gold accumulates to 29 uM with zero free thiosulfate and 30 g of metallic copper present. The 39 uM in the body predates the ammonia-free constants | Part I author + wet lab |
| 38 | Stage 2 needs pH 3 for the enzyme; thiosulfate is unstable below pH 4 | team + wet lab |
| 39 | Joint 1 delivers 29 uM gold, below the 30 uM cliff since the ammonia-free constants. **Read 43 first** | team |
| 36 | Sequential or simultaneous: which is the real process | team + wet lab |
| 33 | `cells_per_g` is a slow-growth value used for a fast-growth culture, about 1.5x out | team |
| 34 | `k_cat` has two published values 8 to 10x apart, 2.2 and 21 U/mg | Part I author |
| **35** | **Capture wants low gold, reduction wants high gold. Nothing concentrates between them** | team |
| **48** | **The reducing protein had no upstream model. Arm B is drawn and never built; the lysate volume dilutes the gold 1.1x to 21x** | team + wet lab. Read with 35 |
| **49** | **The reduction chemistry is not the demonstrated chemistry.** Au(I) is reducible in principle and is the published intermediate, but the driving force is 0.6 V lower and **1 M thiourea competes for the same cysteines the mechanism needs**. The methyl viologen mediator is also absent from the model | wet lab, then modelling |
| **52** | **The culture plateaus about 37x below the 0.2 g/L of reductase every reduction number assumes. Harvest timing is a window, not a moment** | modelling done; wet lab to measure burden and lysis yield |
| **51** | **[S35] supplied 0.6% of the electrons its own gold required, so no published number confirms any conversion. `Rech` is dosed dithionite, not lysate carryover** | modelling, then costing |
| 19 | Gold leaching scales as 1/`t_film`; the range spans 20x. Now a joint largest lever | team, from board spec |
| 23 | Leach chemistry published only at pH 9-10.5 | team |
| 40 | No purification yield in Stage 1, no enzyme decay in Stage 2 | wet lab |
| 37 | The sequential write-up prints the lumped rates its own code does not use | Part I author |
| **71** | **Finke-Watzky constants may not transfer across precursor concentration. A second gold study's numbering is ambiguous: on the favoured reading the band is fine, on the other the floor is 23x too high** | one full text, paywalled |
| 83 | REVIEW, MASTER, EQUATIONS and WIKI_CONTENT swept onto the current recovery model; REVIEW section 6 is now generated from RECOVERY.md | done 2026-08-24 |
| **82** | **k_nuc recentred from 5.0e-5 to 0.96 /h (enzyme-scaled) and k_grow from 0.2 to 0.082. The concentration cliff disappears; eight tests re-derived** | **done 2026-08-24** |
| 81 | A fitter for the two Finke-Watzky constants now exists, `src/fit_fw.py`, with the assay it needs written into it | ready; needs data |
| **80** | **Michaelis-Menten with MEASURED constants is available for the reduction step, and under it the concentration cliff disappears. Two-limit model proposed** | **team decision** |
| 79 | Sourcing k_nuc and k_grow again, 2026-08-24: the ceiling traced to its primary data, still no protein fit, and the 0.4 mM assumption stands | searched twice; open |
| 78 | SOURCES.md sends S51, S52 and S53 to ISSUES item 67, which is about plasmid backbones. The right item is 71 | Tier 2, not rewritten |
| 77 | Reduction timing symbols renamed (`t_cross`->`t_ind`, `t_50`->`t_1/2`); RECOVERY 4.3 now reports `t_95` | done, recorded |
| 76 | `v_rech` verified: structure standard, dithionite order should be sqrt, worth 0.001 point | recorded, no action |
| 75 | `model.md` has no citations; its trail is a companion document not in the repository | ask the Part III author |
| 74 | The donor sub-system is exactly replaceable by the electron cap. Two tests pin it | done, recorded |
| **73** | **`lambda_D` = `mu*k_rep0/A_tox` is dimensionally one power of time out. In a SOURCE document, so left standing. Worth 1.1% on captured gold** | Part III author |
| 72 | `k_rech` unit did not balance; corrected. Third label defect in one file, and nothing checks units | modelling, half a day |
| 70 | `k_ox` labelled as gold re-oxidation, coded as enzyme re-oxidation. No published number moves | modelling |
| 28 | S60 acid-thiourea is the working eluent; GolB time course still required | wet lab |
| 47 | Elution rate law: **PFO adopted provisionally 2026-09-18** with `k_elute = 0.22 h^-1`; confirmation is the **same experiment as 28** | wet lab, one experiment |
| 22 | `K_Au` and `A_tox` are apparent constants tied to untracked conditions | team + Part III author |
| 26 | `q_max` engineering target 0.1961, and the window it implies | team |
| 1 | `K_Au` = 0.7 uM adopted from S78; project-matrix transfer remains open | team |
| 21 | No stopping rule for the leach; Part III's window implies one. Now load-bearing, see 39 | team |
| 29 | Temperature and the V1 to V2 transfer are unmodelled | team, deferred |

Cosmetic, needing source-document edits only: **7** (`AuO3 3-` typo),
**11** (Greek capital Mu in a table), **10** (heading levels).

### Closed

| # | Item | Closed by |
|---|---|---|
| 50 | Reduction rate law standardised; min() removed, protein pool conserved, k_donor retired | 2026-08-16 |
| 42 | `K_S2O3` was a placeholder 8.6x above the measured band | 2026-08-12 |
| 8 | `k_Au,Cu` and `k_Cu,O2` existed only as ratios; both now have values | 2026-08-12 |
| 17 | `K_S4O6` had no chosen value; 300 chosen from the sourced range | 2026-08-12 |
| 20 | Model B had no `k_ox,Cu`; it has one, and item 41 restates the conclusion | 2026-08-12 |
| 31 | The capture numbers had no solver behind them | 2026-08-11 |
| 27 | Every PRCC recomputed in three regimes; reduction now dominates | 2026-08-11 |
| 3 | Part II's 5.5% self-disagreement is exactly the saturation term | 2026-08-11 |
| 30 | *E. coli* throughout; `Vmax` rebuilt from Part II's cascade | 2026-08-11 |
| 12 | Enzyme equation mixed bulk and intracellular frames; no `X(t)` | item 30 |
| 2 | `q_max` 255x too high and over a physical ceiling | 2026-08-10 |
| 18 | `v1` and `R_Au` each used as two quantities | 2026-08-10 |
| 5 | Cu(II) goes negative | item 18 |
| 13 | `k_syn` and `k_cat` not separately identifiable | lumped into `Vmax` |
| 16 | One reaction, two rate constants | the rename |
| 25 | `A` meant area, sites and soluble gold | the rename |
| 15 | `k_cat` marked unmeasured; it is published at 220 min^-1 | 2026-08-11 |
| 6 | `Y` defined and never used | 2026-08-11 |
| 24 | Parts II and III used different *E. coli* growth rates | 2026-08-10 |
| 4 | mol vs umol in solid inventories | umol chosen |
| 9 | Three unit systems | `src/interfaces.py` |
| 14 | `k_syn` placeholder 7,000x too large | superseded by 13 |

---


# Open

> **Note on items 17 and 20.** Both closed on 2026-08-12. Their full analyses
> are left in place under this heading rather than compressed into the closed
> record, because the sweeps in them are the evidence for items 41 and 38 and
> deleting them would delete the record. Each carries a `CLOSED 2026-08-12`
> subsection at its end. Item 8's analysis was short and moved to the closed
> record in full.


## 44. 🔴 BLOCKING — the leach manufactures a reagent that destroys the capture protein

Found 2026-08-12 by auditing what actually crosses Joint 1, rather than only
the gold. **Nothing in any of the three documents mentions this.**

### The mechanism

GolB binds Au(I) through a **Cys-X-X-Cys** motif: two cysteine thiols, close
together, that must be free and reduced to bind anything. Part II §5 is built
on this and Part III's whole capture step depends on it.

**Tetrathionate is a thiol-blocking reagent.** It is used as one in
biochemistry. It attacks free -SH groups to form a sulfenylthiosulfate,
S-sulfonating the cysteine. Where two cysteines sit close together, as in a
Cys-X-X-Cys motif, the reaction proceeds further and closes an **intramolecular
disulfide**. Either outcome removes the binding site. [S33](SOURCES.md).

### The quantity

In the sequential design, tetrathionate made by the parasitic reaction in
Stage 3 is a **dead-end product**: with no enzyme in the vessel, nothing
converts it back. It accumulates, and it goes to Part III with the gold.

| | µmol/L |
|---|---|
| GolB binding sites available, `q_max`·`X_max` | 0.054 |
| Cysteine thiols on those sites, two each | 0.108 |
| **Tetrathionate delivered with the gold** | **47 251** |
| Molar excess over the cysteines | **437,506 : 1** |

At that excess the reaction does not need to be fast or efficient. Every
GolB site is blocked long before any gold is captured.

### Why nobody saw it

Part I tracks tetrathionate carefully as a *substrate*, and once it stops being
a substrate the model stops caring. `src/interfaces.py` carries gold across
Joint 1 and, since 2026-08-12, copper. It never carried the sulfur species,
because nothing suggested they mattered. They are the largest thing in the
stream by three orders of magnitude.

### It is reversible, which makes it actionable

S-sulfonation is undone by thiol reducing agents; treatment with a
thiol-containing reductant frees the sulfenylthiosulfate and restores activity.
[S33](SOURCES.md). So the fix is a conditioning step between the vessels, not a
redesign:

1. **Reduce before capture.** DTT or TCEP, or a thiol wash, on the liquor or on
   the cells. Cheap, and it is standard practice for any cysteine-dependent
   protein.
2. **Do not make the tetrathionate.** Carrying the enzyme into Stage 3 converts
   it back and cuts the load from 47 251 to 35 667 µmol/L, while also raising
   gold from 38.4 % to 54.3 %. A 25 % cut, not a solution on its own.
3. **Separate the gold from the liquor** before it meets the cells at all.

**Note which way the architecture points here.** The sequential design makes
this *worse* than the one-pot design, because removing the enzyme from the
leach vessel is exactly what turns tetrathionate into a dead end. This is the
first cost anybody has found for the three-vessel choice.

**Who decides:** the wet lab, and quickly. Item 32 asks whether the enzyme
works. This asks whether the capture protein survives contact with the enzyme's
own product.

**What would settle it:** incubate GolB, or the display strain, in 47 mM
tetrathionate and assay gold binding against an untreated control. One
experiment, one day.

---

## 43. The Part I to Part III joint is a scale mismatch, and no stopping rule fixes it

**Capture interpretation superseded, 2026-09-07, item 91.** The expression-derived
number bounds single-site occupancy, not all whole-cell gold accumulation.
S76 supplies experimental whole-cell evidence that the earlier search missed.
Original arithmetic remains below as a record.

⚠ **UPDATED 2026-08-19 and 2026-08-20. Every number below moved, and the
conclusion did not.** The original arithmetic is left standing per AGENTS.md
rule 6; read this banner first.

| | As written 2026-08-12 | Now |
|---|---|---|
| Gold dissolved at 72 h | 39.0 uM | **28.9 uM** (ammonia-free constants, item 54) |
| What 5 g/L of cells can hold | 0.054 uM | **0.457 uM** (item 61) |
| Over capacity above | 0.053 % recovery | **0.45 % recovery** |
| **Dry cells per gram of board** | **94 g** | **11 g** |
| A litre of culture takes the gold from | 53 mg of board | **450 mg of board** |
| **The scale mismatch** | **2000x** | **63x** |
| Both stretch targets together | 1.5x short | **1.13x short** |

**11 grams of engineered cells per gram of circuit board is still not something
a stopping rule tunes.** What changed is that both stretch targets together now
very nearly close it, where before they left it half a factor short. The
recomputation is pinned by
`tests/test_interfaces.py::test_capture_capacity_is_a_scale_mismatch_not_a_concentration`.

Found 2026-08-12. **This supersedes the framing in item 39 and in the advice
given with it**, which treated the 39 µM feed as something a stopping rule
could tune away. It cannot. Restated here rather than erased, per AGENTS.md
rule 6.

### The arithmetic

| | |
|---|---|
| Gold on the board, per litre | 101.5 µmol |
| Gold dissolved at 72 h | 39.0 µmol |
| **What 5 g/L of GolB cells can hold** | **0.054 µmol** |

The capture step is over capacity at **any leach recovery above 0.053 %**. The
stopping rule of item 21 chooses between 39 µM and 20 µM. Both are hundreds of
times over. **There is no stopping point that makes this fit**, short of
stopping the leach before it starts.

### Say it as a mass ratio, because that is the number people can act on

Gold on the board is 1.0154 µmol per gram. Capture capacity is 0.0108 µmol per
gram of dry cells. So, in one pass:

> **94 grams of dry engineered cells per gram of circuit board.**

Or the other way round: a litre of culture at 5 g/L can take the gold from
**53 milligrams of board.** Part I is written for 100 grams.

The two halves of the project were designed at scales about 2000× apart, and
because each was checked on its own, neither noticed.

### What closes it, and what does not

| | Helps | By how much |
|---|---|---|
| Stop the leach early, item 21 | barely | 39 µM to 20 µM, still 370× over |
| Dilute the liquor | not at all | capacity is a total, not a concentration |
| `q_max` to its 0.1961 target, item 26 | 18× | 94 : 1 becomes 5.2 : 1 |
| `X_max` to published densities, item 26 | 26× | ceiling 0.054 to 25.5 µM |
| Reuse the cells over N elution cycles | N× | 722 cycles is 181 days |

**Both stretch targets together still leave it 1.5× short**, at a cell-to-board
ratio of 5.2 : 1. That is the honest best case, and it is the number the wiki
should carry rather than a recovery percentage.

### What this actually means

It is not a bug. It is the discovery that **Part III's capacity, not Part I's
chemistry, sets the size of the whole process.** Every hour spent raising leach
recovery is spent on the half that is already 2000× ahead.

Item 26, raising display density, was already ranked first. This is the
quantitative case for it, and it is much stronger than the one item 26 makes.

**Recomputable, no wet lab needed:** the throughput of the plant in grams of
board per day, as a function of `q_max`, `X_max` and cycle time. Nobody has
written that number down and it is the one a judge will ask for.

---

## 45. Part I names passivation in its prose and has no passivation term

Found 2026-08-12. Part I §4 reads:

> "area, thiosulfate, and passivation multiply everything (all are required
> regardless of oxidant)"

**There is no passivation factor in the equation.** `R_Au` has three factors:
area, the thiosulfate saturation term, and the oxidant term. Passivation was
named and never written, in both the simultaneous and the sequential documents.

### It is not a small omission

In ammonia-free thiosulfate systems, thiosulfate decomposes on the gold surface
and lays down a sulfur film that passivates it; sulfur and copper sulfide are
the identified film components, and the gold dissolution rate is observed to
fall as leaching proceeds. **Our system is ammonia-free.** [S34](SOURCES.md).

And it comes straight off the headline, because gold recovery in this model is
almost exactly linear in the gold rate constant:

| gold rate × | 0.03 | 0.1 | 0.3 | **1.0** | 3.0 |
|---|---|---|---|---|---|
| Au at 72 h | 1.2 % | 3.8 % | 11.5 % | **38.4 %** | 100 % |

Gold spends 0.08 % of the thiosulfate budget, so it never competes for leachant
and never saturates. Whatever a passivation factor turns out to be, it
multiplies 38.4 % by that factor. A threefold late-stage penalty takes the
result to about 13 %.

**One thing pushes the other way.** Copper(II) is reported to strip the sulfur
film from the gold surface, so a copper-rich liquor passivates less than a
clean one. Our liquor is copper-rich by design. That is a reason the penalty
may be mild, not a reason it is absent, and it is a third role for copper on
top of the two in item 41.

**Who decides:** Part I's author, since it is his equation and his prose.

**What would settle it:** a leach run long enough to show the rate falling
faster than area and thiosulfate alone predict. The residual is the passivation
term.

---

## 61. The plasmid was high-copy all along, and it moves every number downstream

Supplied 2026-08-19 by *GolB_model_writeup_draft4.docx*. The wet lab confirms a
**pUC-type high-copy backbone**, not the pBR322-like one this repository
assumed. `N` moves from 20 to 300, and nothing downstream is untouched.

Draft 4 was checked before adoption, not after: every number in it reproduces
here, including all ten normalised sensitivities to two decimals and the
growth-rate table. Nothing below is taken on trust.

### It closes item 3

The repository carried only the **non-saturating** closed form, so it disagreed
with its own ODE by 5.5 % at N = 20. Item 3 recorded that as an inconsistency
in the source document. It was not one — the document quoted `P_s` from the ODE
and `A` from the closed form, two different calculations of the same thing.

Draft 4 supplies the saturating closed form, which stays closed-form because
`P_c` is decoupled from `P_s`:

    J   = k_sec * Pc*
    Ps* = J / (J/P_s_max + delta_s + mu)

**It reproduces the ODE exactly, to 1e-14, at both copy numbers.** There is one
model, and now one closed form for it.

### The linear form is not a small correction any more

| N | linear `P_s` | true `P_s` | error |
|---|---|---|---|
| 20 | 5,818 | 5,498 | 5.8 % |
| 100 | 29,091 | 22,535 | 29 % |
| **300** | 87,273 | **46,602** | **87 %** |
| 350 | 101,818 | 50,450 | exceeds `P_s,max`: physically impossible |

### The limiting resource moved from the gene to the membrane

The surface is now **46.6 % full**, not 5.5 %. The sensitivity ranking changes
with it, and this is the design message:

| | linear, N = 20 | saturating, N = 300 |
|---|---|---|
| `f` folding | +1.00 | **+1.00** — unchanged, still first |
| `α`, `N`, `β` | +1.00 | **+0.53** — halved by crowding |
| `P_s,max` anchor capacity | +0.00 | **+0.47 — newly co-limiting** |
| `δ_m` | −0.91 | −0.49 |
| `μ` | −1.05 | −0.56 |

`f` alone keeps its full +1.00, because it multiplies `P_s` **after** all the
saturation has happened. **The productive handles are now the folding fraction
and the display scaffold, not the promoter, the copy number or the RBS.**

Saturation also compresses the copy-number uncertainty: `N` is quoted anywhere
from 75 (NEB's own pUC19 datasheet) to 700, a 9.3× spread, and the answer moves
only 3.7× across it. No copy number can pass `f·P_s,max` = 50,000 sites.

### What moved downstream

| Quantity | Was | Now | Factor |
|---|---|---|---|
| Active sites per cell | 2,749 | **23,301** | 8.5× |
| `q_max` | 0.0108 | 0.0913 µM/(g/L) | 8.5× |
| **Capture ceiling at 5 g/L** | **0.054 µM** | **0.457 µM** | 8.5× |
| Leach-to-capture mismatch | 537× | **63×** | 8.5× better |
| `q_max` gap against Part III's retired 4.4 | 386× | 48× | item 2 narrows |
| Stage-1 `Vmax` | 9.49 | 80.36 µmol/L/min | 8.5× |
| Culture per litre of conversion vessel | 2.35 L | **0.28 L** | 8.5× less |
| Reagent-arm protein shortfall | 37× | **2.5×** | item 48 nearly closes |
| Reduction `t_cross` at the delivered gold | 93 h | **11 h** | now inside a run |

**`t_cross` is the one to notice.** Reduction previously did not start inside a
24-hour batch — the run ended while the reaction was still nucleating. At
11 hours it starts. It is not fast, and the 3 µM threshold still wants a
concentration step, but the step is no longer the difference between working
and not working.

### Two cautions

**1. The proxy now carries an unconfirmed backbone.** `teth_per_cell` in Part I
and the whole reagent arm in Part III borrow Part II's cascade as a *labelled
proxy*, because their own `α`, `N`, `β` and `δ_c` are null. They have therefore
inherited a pUC assumption confirmed for the **GolB display construct only**.
Nobody has confirmed the backbone of the TetH construct or the reductase
construct. If either differs, divide back down — and note that Part I's leach
result does not move either way, because `teth_per_cell` sizes the culture and
nothing else.

**2. The reagent-arm shortfall did not close because anything was built.** It
closed because a proxy was corrected. Treat 2.5× as provisional until the
reductase construct's own copy number is known.

### The growth-rate trap, which arrives with the new ranking

`μ` is the largest negative sensitivity, which invites the conclusion that mild
stress — cooler, leaner, off-pH — raises capture. Per litre it does the
opposite:

| `μ` | doubling | sites/cell | biomass at 8 h | total capture |
|---|---|---|---|---|
| 0.005 | 139 min | 36,342 | ×11 | **×0.001** |
| 0.020 | 35 min | 23,301 | ×14,765 | ×1 |
| 0.030 | 23 min | 17,786 | ×1,794,075 | **×93** |

Site density is weakly hyperbolic in `μ`; biomass is exponential in it. Growth
wins, overwhelmingly and always. **This caveat must travel with the sensitivity
figure wherever it is reproduced.**

The design resolution is to separate the stages in time: grow and express in
rich medium, then harvest and resuspend in the leachate, where `μ` ≈ 0 and the
site count is whatever was built beforehand. That reframes the steady state as
a **pre-load target reached in a separate vessel**, not a condition held in the
leach liquor — where it could not be held anyway.

**Pinned by** `tests/test_expression.py`, six tests including
`::test_ode_converges_to_the_saturating_closed_form_exactly`,
`::test_the_sensitivity_ranking_changed_when_the_membrane_filled`,
`::test_the_growth_rate_trap` and
`::test_saturation_compresses_the_copy_number_uncertainty`.

⚠ **The propagation was incomplete when this item was written.**
`params/recovery_chain.yaml` was missed, so `q_max` stayed at 0.0108 for a day
while the report quoted 0.0913 in its body. **Item 62 records what that cost
and what now prevents it.** Read that item before making the next joint change.

**Read with:** item 62, the propagation failure this item caused; item 3, which
it closes; item 2, whose gap narrows to 48×; item 43, whose 2000× scale
mismatch becomes 63×; item 48, whose shortfall becomes 2.5×; item 63, the PRCC
table it invalidated.

---

## 62. Part II moved and Part III did not, and the report carried both numbers

Found 2026-08-20 by auditing the documents against the parameter files.

Item 61 changed Part II's copy number and propagated it to
`params/expression.yaml`, to `teth_per_cell` and `Vmax` in
`params/leach.yaml`, and to the reductase proxy. **It did not reach
`params/recovery_chain.yaml`,** which went on carrying `q_max` = 0.0108 with a
derivation line reading "2,749 active sites per cell".

Nothing failed. The 107 tests passed, because three of them asserted the stale
value: the capacity ceiling at 0.0539 uM, the window headroom at 18.2x, and the
thiol ratio at 437,506 : 1. **A test that pins a number is not a test that the
number is right.**

### What it did to the report

`docs/_review_parameters.md` is generated from the YAML and spliced into
`REVIEW.docx` as Appendix A. So the built document stated both values:

| Where | Said |
|---|---|
| Section 7 body | `q_max` 0.0913, ceiling 0.46 uM |
| **Appendix A** | **`q_max` 0.0108** |
| **Figure 8**, printed above section 7 | **bar at 0.054 uM** |

`docs/make_review_figures.py` reads `q_max` from the YAML, so the figure and
the paragraph under it gave different answers to the same question. Sections
6.2 and 6.3 were never converted either, so the report still told the reader
reduction cannot start inside a run.

### What was done

`q_max` 0.0108 -> 0.0913, with the retired value kept in a
`superseded_2026_08_19` block. Everything derived from it was recomputed rather
than scaled: the capacity ceiling, the thiol ratios of items 44 and 60, the
cell-to-board ratio of item 43, the mixing table of item 48, the elution feed,
the reduction landmarks, and the `eta_capture` and `K_Au` tables in MASTER.md.

### What stops it recurring

`tests/test_interfaces.py::test_qmax_is_part_II_pushed_through_joint_2`
recomputes `q_max` from `params/expression.yaml` through
`interfaces.qmax_from_expression` and compares it with the stored value. If
Part II moves and Part III does not, that test fails. **This is the check that
was missing, not a number that was wrong.** Joint 1 has the same shape of guard
since item 60; Joint 2 did not have one until now.

**Read with:** item 61, which caused it; item 60, which was the same failure at
the other joint five days earlier.

---

## 66. The parameter files contradicted themselves, and nothing was looking

Found 2026-08-20 by auditing `params/*.yaml` directly rather than through the
code that loads it. Four defects, in the files that are the authority for every
number in the model.

### 1. Two YAML keys with the same name, and the loader said nothing

`tetrathionate.k_cat_per_subunit` carried **two `derivation` keys, two `note`
keys and two `source` keys**. `yaml.safe_load` keeps the last of each and
reports nothing, so the derivation the file actually served was

    2.2 U/mg / 0.01 umol = 220 /min

attached to a parameter whose value is **125**. The correct derivation, 2.5
U/mg on a 50 kDa subunit, was present in the file and silently discarded. The
220 material belonged to `k_cat` and has been moved there.

`reduction.retired_k_donor` had the same scar: duplicate `unit` and `status`,
where the second `status` overwrote `retired` with a description of the
literature range.

### 2. `Vmax` contradicted its own derivation for a day

    value:      80.36
    derivation: 2749 molecules/cell ... = 9.49 umol/L/min

Item 61 moved the value on 2026-08-19 and left the derivation, the
`scales_with_biomass` table and the closing note at the old copy number. All
six rows of that table were 8.5x low. **This is item 62 again, one layer
further in:** the propagation reached the value and not the reasoning beside
it.

### 3. Two notes still quoted pre-ammonia-free recoveries

`k_cat_per_subunit` said gold at 72 h is 38.0 / 38.4 / 38.6 % across the
110 / 125 / 220 range. `K_S2O3` said 38.4 % at 3900 and 22.6 % at 5e4, and
called itself a 1.7x lever. Recomputed:

| | quoted | actual |
|---|---|---|
| k_cat 110 / 125 / 220 | 38.0 / 38.4 / 38.6 % | **28.16 / 28.49 / 28.62 %** |
| K_S2O3 3376 / 3900 / 5e4 | -- / 38.4 / 22.6 % | **28.49 / 28.18 / 19.12 %** |
| K_S2O3 as a lever | 1.7x | **1.5x** |

The k_cat range moves Stage 2 conversion far more than it moves gold: **85.57 %
at 110, 95.94 % at 125, 100 % at 220.** That is item 57, and it is the reason
to care about which specific activity is right.

### 4. Provenance gaps

`k_cat` and `k_cat_per_subunit` were both marked `status: sourced` with **no
`source` key at all**. Both are now cited to [S1] Kanao 2023, and a caveat is
recorded: **220 uses the 2.2 U/mg figure measured in *A. ferrooxidans*, while
our host is *E. coli*, for which [S1] reports 2.5 U/mg.** The two overlap
inside their error bars and gold moves 0.13 points across the whole range, so
this is recorded rather than resolved. `reagent_arm.burden` was missing its
`source: null` key.

### What now prevents all four

Two tests in `tests/test_interfaces.py`:

`::test_no_yaml_file_has_a_duplicate_key` parses each file with a loader that
refuses to let a duplicate pass unseen.

`::test_every_derived_value_still_equals_its_own_derivation` recomputes
`teth_per_cell`, `Vmax`, every row of `scales_with_biomass`, `q_max`, its
engineering target, both `k_cat` values, `K_S2O3` from its measured band, and
the agreement between the two files that carry `cells_per_g`. **A derivation
that stops reproducing its value now fails the suite.**

**Read with:** item 62, the same failure one layer out; item 61, which caused
the `Vmax` drift; item 57, which the k_cat conversion figures belong to; item
54, which moved the recoveries these notes quoted.

---

## 65. The reduction test harness fed 100 uM of dithionite where the file says 4.6

Found 2026-08-20 while drawing the seeding figure for item 64, which reads the
YAML, against the table for item 64, which came from the test harness. They
disagreed.

`params/recovery_chain.yaml` has carried `Rech_0` = **4.6 uM** since
2026-08-17, when item 51 traced it to [S35]'s own methods: 100 uL of 46 uM
sodium dithionite into a 1000 uL reaction. `tests/test_sensitivity.py`
hard-coded **100.0**. Every `eta_reduce` this repository has published came
from the harness, so every one of them used a dithionite pool 22x too large.

The same file also hard-coded `E_tot` as `0.2 / 70000 * 1e6`. That one happens
to equal the YAML, but it is the same defect and it is now read from the file
too.

### What moved

| | harness, 100 uM | file, 4.6 uM |
|---|---|---|
| eta at 0.457 uM, 24 h | 0.43 % | **0.39 %** |
| eta at 1.0 uM, 24 h | 2.9 % | **2.4 %** |
| eta at 3.0 uM, 24 h | 99.3 % | **97.3 %** |
| eta at 5.78 uM, 12 h | 97.9 % | **84.9 %** |

**Small where the chain operates, large where it was heading.** The
concentration step of item 35 aims at 3 uM and above, which is where the gap
opens.

### It exposed a second thing, and this one is a result

`test_reduction_is_monotonic_in_starting_gold` asserted that conversion rises
with starting gold. It passed for months. **It is false**, and it passed only
because 100 uM of dithionite covers 206 uM of Au(I), so nothing in the tested
range ever ran out of electrons. At the sourced 4.6 uM the budget covers
14.9 uM, and conversion peaks near there and then falls:

| Au(I) | eta_reduce, ODE | closed-form ceiling |
|---|---|---|
| 10 uM | 1.000 | 1.000 |
| 20 uM | 0.727 | 0.746 |
| 30 uM | 0.489 | 0.497 |
| 50 uM | 0.295 | 0.298 |

The falling limb tracks `(2*E_tot + 2*Rech_0)/(n_e_Au*Au_aq0)` to within 3 %,
and the ODE knows nothing about that expression. **Two independent routes
agreeing across the starved region is a real cross-check of the reduction
model**, and it was invisible while the harness was overfeeding the vessel.

The test now asserts the true shape: rising to the budget, falling along the
ceiling beyond it. That is strictly more than it checked before.

### Why it was not caught

`tests/test_reductase.py` reads `Rech_0` from the YAML. `tests/test_interfaces.py`
asserts the YAML value directly, including its provenance. Only
`test_sensitivity.py` carried a literal, and it is the file that produces every
published reduction number. **A parameter is not centralised until every caller
reads it**; AGENTS.md rule 2 says no number in a .py file, and the rule was
broken in the one place where it decided a result.

**Pinned by** `tests/test_sensitivity.py::reduction_params`, which now reads
both `Rech_0` and `E_tot` from `params/recovery_chain.yaml`, and by
`::test_reduction_rises_to_the_electron_ceiling_and_then_falls_along_it`.

**Read with:** item 51, which sourced `Rech_0`; item 62, the same class of
failure at Joint 2; item 64, whose numbers this corrects.

---

## 64. Reduction has no slow step; it has a late start, and a seed removes it

Found 2026-08-20, asking what would actually fix the 0.33 % conversion left
standing by item 61.

Finke-Watzky is autocatalytic: gold metal catalyses its own formation. Growth
overtakes nucleation only once `Au_s` reaches `k_nuc/k_grow`, which nucleation
alone needs

    t_cross = 1 / (k_grow * Au_aq) = 13.6 h

to build at the 0.367 uM the elution delivers. A 24-hour batch spends most of
itself in induction and then stops. **The rate constant is not the problem.
The empty solid pool at t = 0 is.**

### The five levers, priced

Conversion at 24 h, on the delivered 0.367 uM. Every figure here is at the
YAML's `Rech_0` = 4.6 uM, not the 100 uM the test harness had been using until
item 65 was found on the same day:

| Lever | Result | Verdict |
|---|---|---|
| 4x concentrate + 1 % seed | **88.5 %** | the recommendation |
| 4x concentrate + 10 % seed | 99.2 % | if seed is cheap |
| 10x concentrate, no seed | 99.7 % | what concentration alone costs |
| 6.6x concentrate, no seed | 83.0 % | not enough |
| 10 % seed, no concentration | 32.9 % | not enough |
| More reductase or dithionite | **0.30 %** | **no effect whatever** |

**Concentration alone can finish the job; it needs about 10x. A 1 % seed cuts
that to 4x.** That is the finding. Eluting into a quarter of the volume is
ordinary process design and eluting into a tenth is not.

⚠ **The seed does NOT beat concentration head to head**, and an earlier draft
of this item said it did. At 1x a 1 % seed reaches 4.5 % against the 4x
concentration's 12.4 %. The seed is the cheaper half of a pair, not a
substitute for the other half.

### The negative result matters as much as the positive one

Ten times the reductase and ten times the dithionite change the delivered
conversion by less than a tenth of a point. Gold consumes 6.4 % of the donor
pool, so electrons are not the constraint **at the gold we deliver**. The
reagent-arm shortfall of items 48 and 52 does not touch this problem, and
anyone about to spend wet-lab time raising the lysate concentration for the
sake of reduction should stop.

They do become the constraint above about 15 uM, where the electron budget of
item 65 runs out. That is an argument for sizing the concentration step rather
than maximising it: a 40x concentration would starve the vessel.

### Seeding takes an unmeasured constant out of the answer

Seeding needs `sigma >> k_nuc/(k_grow*Au_aq)` = 6.8e-04, so a 1 % seed clears
the bar by a factor of fifteen. Past that, `k_nuc` has left the problem: a
hundredfold rise in `k_nuc` moves the seeded answer by under 10 %, against more
than 5x unseeded.

That is worth having on its own. `k_nuc` and `k_grow` are both flagged *weakly
calibrated --- joint #1 driver* and neither is measured. **`k_grow` alone spans
the whole outcome:** at 0.2 the conversion is 0.33 %, at 1.0 it is 47 %, at 2.0
it is 100 %, with nothing else changed. Every figure in this item is
conditional on `k_grow` = 0.2 being right.

### What was built

`Au_s(0)` was hard-coded to zero, so the repository could not express the fix
it was recommending. `src/sensitivity.py :: reduce_finke_watzky` now takes
`seeding_on` and `seed_frac`, following the switch-and-default-off pattern of
items 54 and 61: off by default, and every eta_reduce published before today is
reproduced exactly when off.

Two details that are easy to get wrong and are pinned by tests:

1. **The seed is subtracted from the product.** `eta_reduce` is metal the
   vessel MADE. Counting the seed would report a factor of two at a 100 % seed.
2. **`seed_frac` is `null` and raises.** No seeding experiment has been run.
   The 1--10 % band in the YAML is labelled `modelled_band`, not a value.

**Pinned by** `tests/test_sensitivity.py`, six tests including
`::test_seeding_beats_concentration_and_the_two_together_finish_the_job`,
`::test_the_seed_is_not_counted_as_product`,
`::test_seeding_substitutes_for_the_unmeasured_nucleation_constant` and
`::test_electrons_are_not_what_limits_the_delivered_conversion`.

**What it needs from the wet lab:** one reduction run with and without a 1 %
seed of citrate gold. That measures `seed_frac` and constrains `k_grow` at the
same time, and it is the cheapest experiment in Part III.

**Read with:** item 65, found the same day and which every number here is
computed against; item 35, the concentration squeeze this shrinks from 70x to
about 4x; item 61, which moved the delivered gold; items 48 and 52, which this
rules out as causes.

---

## 63. Every PRCC in the adopted regime was computed at the retired `q_max`

> **Update 2026-09-18.** `K_Au` now uses the sourced `0.7 µM` proxy and the
> S78 range `0.2-1.15 µM`. At `q_max = 0.0913`, that range changes capture by
> 2.20-2.45-fold at 0.02-0.5 µM feed and 1.10-fold at 10 µM. The PRCC still
> needs rerunning; the old `1e-4-0.1 µM` range and its coefficient are no
> longer current inputs.

Found 2026-08-20, with item 62.

`MASTER.md` carries a PRCC table with three columns: the retired `q_max` = 4.4,
the adopted 0.0108, and the 0.1961 target. **The middle column now describes a
regime the chain has left**, in exactly the way the first column describes one
it left before that. The document already makes this argument about `q_max` =
4.4; it applies again.

One row is already known to be wrong. `K_Au` sits at -0.14 in that column
because the low capacity forced the model down to feeds comparable with
`K_Au` = 0.1 uM. At `q_max` = 0.0913 the swing across the `K_Au` range collapses
from 3.45x to **1.24x**, so `K_Au` returns to being insensitive, which is what
the recovery-chain document said in the first place. `MASTER.md` has that
recomputation; the PRCC table beneath it does not.

**Not recomputed here, and not guessed.** The sampling ranges behind
`prcc_results.json` are not recorded in any tracked file, so the run cannot be
reproduced from the repository as it stands. Inventing ranges to fill the table
would be worse than the banner now standing above it.

**What it needs:** the Latin-hypercube ranges written into a tracked file, then
one rerun of `src/sensitivity.py` at `q_max` = 0.0913. Half a day, no wet lab.

**Read with:** items 27 and 41, the previous PRCC recomputations; item 62.

---

## 67. The reductase is on pET-24(+), not the backbone the proxy assumed

Supplied 2026-08-20 by the team, in answer to the caution written into item 61
on 2026-08-19. That caution said the reagent arm had inherited a pUC assumption
confirmed for the GolB display construct only, and that nobody had confirmed
the backbone of the TetH construct or the reductase construct. Half of it is
now answered, and the answer is that the proxy is wrong.

**The three constructs, as reported:**

| Construct | Backbone | Confirmed |
|---|---|---|
| GolB, displayed | pJUMP | family only; the variant is not yet named |
| TetH, harvested | pJUMP | family only; the variant is not yet named |
| Reductase, cytoplasmic | **pET-24(+)** | family named |

### Why this is not a simple division

`golb_proxy_cascade` in `src/reductase.py` hands the reductase GolB's `alpha`,
`N`, `beta` and `delta_c`. Two of those move in opposite directions on pET-24(+)
and the model cannot net them without values:

1. **`N` falls.** pET-24(+) carries a pBR322-derived origin, medium copy, not
   the pUC-type high-copy origin `params/expression.yaml` records. At the
   cascade's current constants the cytoplasmic yield is 109,091 molecules per
   cell at `N` = 300 and 14,545 at `N` = 40. That is a 7.5x cut.
2. **`alpha` rises.** pET-24(+) is a T7 expression vector. `alpha` = 0.5 in
   `params/expression.yaml` is a generic *E. coli* promoter output, and T7 RNA
   polymerase is not one. The promoter term goes up, and nobody here knows by
   how much.

**So the direction of the net change is unknown.** Dividing by 7.5 would be a
guess dressed as a correction. `alpha`, `N`, `beta` and `delta_c` stay null for
this construct, as item 48 requires. What changes is the label on the proxy:
it is no longer "GolB's numbers, pending this construct's own". It is "GolB's
numbers, for a construct now known to sit on a different vector family".

### Three consequences

**1. The 2.5x reagent-arm shortfall is no longer provisional in one direction.**
Item 61 said to treat it as provisional until the reductase's own copy number
is known. The copy number is still not known, but the *family* is, and it is
not the family the 2.5x was computed on.

**2. pET-24(+) needs a DE3 host and IPTG.** The arm-B model induces and lyses,
and `burden` in `params/recovery_chain.yaml` has `source: null`. A T7 system
under full induction is not the same burden as the display construct. Not
modelled, and not claimed to be.

**3. A stale number is in the file.** The note on `reductase.alpha` in
`params/recovery_chain.yaml` says the proxy gives "about 7,300 molecules per
cell". That was true at `N` = 20 and was not updated on 2026-08-19 when `N`
became 300. The current figure is 109,091. Corrected in the note the same day
this item was written; the value stays null.

### What is still open

The pJUMP **variant** for GolB and for TetH. pJUMP is a modular toolkit and the
origin of replication is one of the swappable parts, so "pJUMP" does not by
itself say high copy. `params/expression.yaml` records `N` = 300 from
"pUC-type high-copy backbone, wet lab confirmed" with an honest band of 75 to
700. If the GolB vector turns out to carry a medium- or low-copy origin, then
`N` = 300 is wrong for GolB too, and `q_max`, the capture ceiling and the
headline recovery all move with it. Nothing here assumes that; it is the
question the variant number answers.

**Who decides:** the wet lab. Read the vector number off the GolB and TetH
constructs.

**What would settle it:** two numbers, and a copy-number measurement on the
pET-24(+) reductase strain if the arm is to be quantitative rather than
order-of-magnitude.

**Read with:** item 48, which holds the reductase cascade null; item 52, the
arm-B shortfall; item 61, whose caution this answers.

### Update, later the same day: the pJUMP variant is named, and it is high copy

The team supplied the vector: **pJUMP24-1A(sfGFP)**, for the GolB construct and
the TetH construct both. Checked against Addgene #126971 and the JUMP paper
rather than taken on trust:

| Field | Value | Where from |
|---|---|---|
| Naming | pJUMP**2**4 = AbR #2, OriV #4, in SEVA nomenclature | JUMP paper, Valenzuela-Ortega & French 2021 |
| Marker | kanamycin, 50 ug/mL | Addgene #126971 |
| Origin | **pRO1600/ColE1**, a Pseudomonas-E. coli shuttle module taken from pUCP24 | Addgene #126971; SEVA |
| Copy number | **High copy** | Addgene #126971 |
| sfGFP | the dropout marker of the Level 1 acceptor, replaced by the insert | JUMP paper |

**`N` = 300 survives, and it now covers TetH as well.** `params/expression.yaml`
records "pUC-type high-copy backbone, wet lab confirmed". pRO1600/ColE1 is a
pUC-derived high-copy module, so the classification the file relies on is the
right one, and the two constructs share one vector. The caution in item 61 that
"nobody has confirmed the backbone of the TetH construct" is answered: it is the
same plasmid as GolB.

**What is confirmed is the class, not a count.** Neither Addgene nor the JUMP
paper gives copies per cell for OriV #4, and no measurement of this strain
exists. The 75 to 700 band in `params/expression.yaml` stays exactly as it is,
and 300 remains a mid-range choice inside it. Saturation limits the damage: the
9.3x band compresses to 3.7x in sites per cell, because anchor capacity
co-limits above about N = 350.

**One thing the shared vector does not settle.** pJUMP24-1A is a Level 1
acceptor. The promoter and RBS are the *inserted* parts, not the backbone, so
`alpha` and `beta` may still differ between the GolB and TetH constructs. The
backbone fixes `N` and the host, and nothing else.

**Still open:** only the reductase. pET-24(+) is a different family and the
paragraphs above it stand unchanged.

### Update: the reductase copy number is now sourced, and the shortfall reopened

Asked for 2026-08-20. No measurement of this strain exists, so this is the
literature, banded, in the same way GolB's `N` is:

| Source | Copies per cell |
|---|---|
| pBR322 itself, rom present | 15 to 20 |
| pBR322-derived expression vectors, general | 25 to 50 |
| pGEX-6p-1, pBR322-derived, measured | 51 +/- 8 |
| **Adopted** | **40, banded 15 to 60** |

pET-24(+) carries the pBR322 replicon with RNAI, RNAII and Rom intact, per
Sathiamoorthy & Shin 2012, PLoS ONE 7(10) e47259, which is also where the
pGEX-6p-1 measurement comes from. `params/recovery_chain.yaml` now carries
`reagent_arm.N` = 40 with `status: sourced_from_an_inconsistent_literature` and
`range: [15, 60]`. `alpha`, `beta` and `delta_c` stay null.

**What it does to arm B.** Recomputed, not adjusted:

| | plateau | shortfall against 0.2 g/L |
|---|---|---|
| Proxy, N = 300 | 0.0810 g/L | 2.5x |
| **pET-24(+), N = 40** | **0.0108 g/L** | **18.5x** |
| Band low, N = 15 | 0.0040 g/L | 49.4x |
| Band high, N = 60 | 0.0162 g/L | 12.4x |

The fed batch no longer clears the target. At `X_cap` = 20 g/L the culture
reaches 0.108 g/L, still 1.85x short, and 3.7x short after a 50 % lysis yield.
Biomass alone would need about 37 g/L. The harvest time does not move: 24.0 h
at every copy number in the band, which is the claim `harvest_time_is_robust`
has always made and it survives.

**18.5x IS AN UPPER BOUND.** Only the pessimistic half of the vector change is
in the model. `alpha` is still GolB's 0.5, a generic *E. coli* promoter output,
and pET-24(+) is a T7 vector. The T7 factor is unmeasured, so the true plateau
is higher than 0.0108 g/L by an amount nobody here can name. Do not quote
18.5x as an estimate; quote it as the worst case with the promoter unimproved.

**How it reaches the model.** `golb_proxy_cascade` now takes an optional
`construct` argument: any of `alpha`, `N`, `beta`, `delta_c` that carries a
real value in the reagent arm replaces GolB's, and `borrowed_keys` reports
what is still borrowed. The test harness passes the block rather than the
value, so `alpha` will arrive the same way when it is measured. Item 62 was a
value that reached three files and not the fourth, and item 65 was a harness
carrying its own copy; this is built so neither can recur here.

**A coincidence that will look like a bug.** The new plateau is 0.0108 g/L and
the retired `q_max` was 0.0108 uM/(g/L). `docs/check_docs.py` check 4 matches on
digits, not units, so it now reports two false positives in `REVIEW.md` section
6.3. They are the reductase plateau, not a stale `q_max`. Left standing rather
than worked around, because the check is advisory and suppressing it would cost
more than reading it.

**Who decides:** the wet lab, for a real copy number and a real promoter
strength on this strain.

**What would settle it:** one gel lane. `alpha`, `N` and `beta` enter the model
ONLY as their product -- scaling `alpha` by 4 and scaling `N` by 4 give
byte-identical output, checked -- so the model cannot separate them and does
not need to. Reductase as a fraction of total protein on an induced-versus-
uninduced gel pins all three at once. The target is 18.2 % of total cell
protein, which is an ordinary T7 result against Studier and Moffatt's
benchmark of more than 50 %.

### Update: alpha is not in the literature, and the medium was the real problem

Searched 2026-08-20 for a T7 promoter strength in this model's units. **It does
not exist, and that is an answer rather than a gap.** The T7 literature gives
in vitro constants -- 79 /s initiation at the phi10 promoter, 3.5 /s
pre-steady-state, about 74 nt/s elongation -- and none of them transfers to a
transcription rate per plasmid copy inside a growing cell, where the limit is
how much T7 RNA polymerase the DE3 lysogen makes. Reported pET yields span
three orders of magnitude by protein. There is no generic `alpha` to borrow, so
`alpha` stays null and the gel lane above is the only route to it.

**What the search did turn up is a parameter nobody was looking at.** `X_cap`
was `status: assumed` with `source: null`, carrying 2.0 g/L, "about OD600 5 in
LB batch". It multiplies the volumetric yield linearly. Against the published
shake-flask numbers:

| Medium | Dry cell weight | Plateau | Shortfall |
|---|---|---|---|
| **LB, the value in use** | 2.0 g/L | 0.0108 g/L | **18.5x** |
| Terrific Broth, ZYM-5052 | 8.1 | 0.0437 | **4.6x** |
| EnBase, Erlenmeyer | 10.3 | 0.0556 | 3.6x |
| EnBase, Ultra Yield flask | 20.4 | 0.1101 | 1.8x |

**Terrific Broth alone is worth 4x, for the price of different medium.** LB was
never chosen for this arm; it was an unexamined default, and it has been
carrying a large part of what looked like a construct problem. `X_cap` is now
`status: design_choice` with `range: [2.0, 20.4]` and both ends sourced:
Sezonov 2007 for the LB ceiling of OD600 7, Ukkonen 2011 for the measured
8.1, 10.3 and 19.7-21.1 g/L. New sources S40 and S41.

**Biomass alone does not close it.** 37 g/L would be needed, which is a
fermenter and not a flask. A rich medium plus a T7 promoter only 5x a generic
one does clear it, at 0.91x. That is the likely outcome, and it is not a claim
this repository can make until the gel lane exists.

**⚠ Two things the band does not carry.** Ukkonen's host is RB791 with pQE30, a
T5 promoter, not BL21(DE3) with pET -- the biomass transfers, the expression
system does not. And high biomass with high T7 expression is where inclusion
bodies appear, which is BLOCKING item 32 for TetH and would be the same
chemistry here.

**Read also:** item 52, which is where the arm-B shortfall was first found.

### Update: both borrowed constants replaced, and the shortfall falls to 3.0x

Asked for 2026-08-20, after the 40 was challenged. Both parts of the challenge
were right.

**The copy number was too low.** 40 was a mid-range reading of a wide
literature. The nearest MEASURED relative is pGEX-6p-1 -- pBR322-derived and
rom-intact, like pET-24(+) -- at **51 +/- 8 copies per cell** by qPCR in
Sathiamoorthy & Shin's own hands, with 18 +/- 4 for a p15A derivative in the
same experiment. pETDuet is separately quoted at about 40. `N` moves to **50**,
the measured figure rounded, and 40 goes to `superseded`. The band stays 15 to
60, deliberately asymmetric, because the classic rom-intact pBR322 figure of
15 to 20 cannot simply be dismissed.

**rop is on the vector, checked.** The pET-24(+) map annotates rop, the RNA one
modulator that holds pBR322-family plasmids down. That is the mechanism, and it
is why the "high copy number" label on some vector pages is wrong for this
plasmid: the same page annotates rop as maintaining low copy number two lines
below. Do not trust that label.

**The promoter now has a value, and it is the loosest number in the arm.**
`alpha` = **2.5**, five times GolB's 0.5, `status: sourced_by_proxy`, banded
0.5 to 20.4.

| End of the band | Basis |
|---|---|
| 0.5 | a generic E. coli promoter. A T7 vector will not be worse. A floor, not a belief |
| **2.5** | **T7 elongates about 230 nt/s at 37 C, about 5x E. coli RNA polymerase** |
| 20.4 | where the reductase reaches 50 % of total cell protein, Studier & Moffatt's benchmark |

**IT IS AN ELONGATION RATIO STANDING IN FOR AN INITIATION RATE.** Those are not
the same quantity. No in-vivo T7 initiation rate exists in the literature: the
T7 literature is in vitro kinetics, and in the cell the limit is how much T7
RNAP the DE3 lysogen makes, not the enzyme's own speed. This is the closest
defensible approximation and it must never be quoted as a measurement.

**What the two changes do together:**

| | plateau | shortfall | eta_reduce after 50 % lysis |
|---|---|---|---|
| Before, N = 40 and generic alpha | 0.0108 g/L | 18.5x | 0.24 |
| **After, N = 50 and alpha = 2.5** | **0.0675 g/L** | **3.0x** | **0.90** |
| At the alpha floor, 0.5 | 0.0135 | 14.8x | 0.29 |
| At the alpha ceiling, 20.4 | 0.6882 | clears | 1.00 |

**Reduction moves from failing to working with no margin.** And the medium
ladder moves with it: Terrific Broth now CLEARS the target, 0.73x, where before
it only reached 4.6x. That conclusion leans on `alpha`, and at the `alpha`
floor Terrific Broth does not clear it -- the shortfall is still 3.7x. The
medium and the promoter have to be right together, and only the medium is a
choice the team makes.

**Nothing here is a measurement of this strain.** `N` is a relative's qPCR,
`alpha` is a proxy for a different quantity, and both bands are wide enough to
change the answer. The gel lane above still settles all of it.

**New sources:** S42, Sathiamoorthy & Shin 2012, for the copy number; S43,
Studier & Moffatt 1986 and the T7 kinetics literature, for both ends of the
`alpha` band.

### Update: three parameters became one, because only one is identifiable

Restructured 2026-08-20 after a survey of how comparable models handle this.

**The three constants were never three.** The cascade's steady state is

    P_c* = alpha * N * beta / ((delta_m + mu) * (delta_c + mu))

so alpha, N and beta appear only as a product and no protein measurement can
separate them. This is **structural non-identifiability** in the sense of
Raue et al. 2009, and the prescribed treatment is model reduction: lump the
group, estimate the lump. Checked directly rather than argued: scaling alpha
by 4 and scaling N by 4 give byte-identical trajectories.

**Carrying them separately was actively harmful, not merely untidy.** Each had
its own band -- alpha spanned 40x, N spanned 4x -- and sampling them
independently spreads a single number over about 160x. That is uncertainty the
model does not have, resting on structure it cannot see.

`params/recovery_chain.yaml` now carries `reagent_arm.alpha_N_beta` = **500**,
`status: sourced_by_proxy`, banded **30 to 4080**. `alpha`, `N` and `beta` stay
as keys, null, with `status: not_separately_identifiable` and their retired
values in `superseded`. The distinction matters: "nobody has measured it" and
"nothing can measure it" are different problems and want different experiments.

**Both ends of the new band are anchored, and neither is a product of guesses:**

| End | Basis | Shortfall |
|---|---|---|
| 30 | generic E. coli promoter on a low-copy pBR322 plasmid, 0.5 x 15 x 4.0. A floor, not a belief | 49.4x |
| **500** | **the adopted proxy, 2.5 x 50 x 4.0** | **3.0x** |
| 4080 | reductase at 50 % of total cell protein, Studier & Moffatt's T7 benchmark | clears, 0.36x |

The ceiling is checked against its own physical basis in the tests: at 4080 the
plateau is 0.5505 g/L, which is 50.0 % of total cell protein at 55 % protein by
dry weight.

**A result that was hidden by the split.** GolB's group is 0.5 x 300 x 4.0 =
600; the reductase's is 500. **The two vector differences very nearly cancel** --
copy number falls about 6x on a rom-intact pBR322 replicon, promoter strength
rises about 5x on T7 -- so the pET-24(+) arm lands within a factor of two of
where the proxy had it. By cancellation, not because the proxy was right. That
was invisible while the two moved in separate parameters, and it is now a test.

### A bug the wider band found

`src/reductase.py::simulate` used a flat `atol = 1e-12` for all three states.
X is order 1, but m and P_c are molecules per cell and run to 1e4 and 1e7, so
that asked LSODA for nineteen significant figures on P_c. At the top of the
`alpha_N_beta` band the step size collapses and **the call never returns**. It
never bit while the expression constants were narrow.

Fixed by scaling `atol` per state from the analytic steady states. **No result
moved**: the plateau, the shortfall, the medium ladder and the 24.0 h harvest
time are identical to the digits already published. The bug was reachable only
in the region the old parameterisation could not express.

### What the survey found, and what was not adopted

Three other practices were checked and are recorded here rather than acted on:

1. **Relative Promoter Units.** Kelly & Endy 2009 established that promoter
   strength is reported relative to a reference promoter, BBa_J23101, not in
   absolute units, which cut between-lab variation by about half. This is why
   no absolute alpha could be found: the field stopped publishing them. If the
   wet lab measures the promoter it will be in RPU, and this repository will
   need a conversion at the interface. NOT BUILT.
2. **Product-specific parameters.** The pET/BL21(DE3) modelling literature is
   explicit that model parameters depend strongly on the recombinant product,
   and prescribes a minimum experiment set per product rather than a lookup
   table. So the labelled-proxy pattern is not a shortcut the field takes; it
   is one the field has tested and rejected for absolute yields. It remains
   sound for shape and timing, which is what the arm is used for.
3. **The reagent-arm bands are not in the Monte Carlo.** `docs/make_analysis_
   figures.py` propagates `eps_gly`, `k_alk` and `kLa` -- three leach
   parameters -- and the published error bar therefore describes the half of
   the process that is not the risk. `alpha_N_beta` spans 49.4x to 0.36x on
   the shortfall and appears in no error bar. NOT BUILT. This is the largest
   remaining gap between this model and standard practice.

**New source:** S44, Raue et al. 2009, for the identifiability treatment.

### Update 2026-08-21: a sourcing sweep. Six closed, two refused

Asked for after the survey. Every unsourced parameter that a paper could
plausibly settle was chased. Six now carry a citation and a band; two cannot be
sourced at all, and that is itself the finding.

| Parameter | Was | Now | Source |
|---|---|---|---|
| `V1_capture.X_max` | 5.0, "standard E. coli", source null | 5.0, band 2.8-20.4, design_choice | S40, S41 |
| `reagent_arm.burden` | null | 0.30, band 0.10-0.45 | S47 |
| `reagent_arm.lysis_yield` | null | 0.70, band 0.50-0.90 | S49 |
| `reagent_arm.delta_c` | null, borrowed GolB's | 0.005, band 0.0-0.0116 | S48 |
| `reagent_arm.g_dw_per_OD600` | 0.4, assumed, source null | 0.4, band 0.30-0.50 | S46 |
| `recovery.eta_spin` | null, source null | still null, now with a source | S50 |

**`X_max` is the one that mattered.** It is the largest lever in the entire
model -- 8,713x on end-to-end gold against 799x for the next -- and it was
carrying `status: "standard E. coli"` with `source: null`. That is not a status
and not a source. It is now banded on the same published flask ladder as
`reagent_arm.X_cap`, and 5.0 is identified for what it is: a scoping value
sitting between LB and Terrific Broth, matching no published medium.

**`burden` was being supplied by the test harness.** It was null in the YAML
while `tests/test_reductase.py` passed 0.3 by hand. The hand-passed number was
right and had nothing behind it -- the same shape as item 65, caught before it
could publish anything.

**`delta_c` is now known to be conservative rather than merely borrowed.** The
E. coli proteome is mostly stable in exponential growth; the value in use is a
139 min half-life, and the low end of the band, a stable protein diluted only
by growth, is the more likely case. At `delta_c` = 0 the plateau rises about
25 %, so the error here runs in the favourable direction.

**`eta_spin` stays null on purpose, and now says why.** The physics is
sourceable -- sedimentation goes as diameter squared, about 50 % for 10 nm gold
-- but THE MODEL DOES NOT PREDICT PARTICLE SIZE. Choosing a value would be a
guess about a quantity this repository has no equation for. One TEM or DLS
distribution from a reduction run settles it.

#### The two that refused: `k_nuc` and `k_grow`

These are the joint #1 driver of the pipeline, 799x and 98x in the tornado, and
both are marked "weakly calibrated". **No transferable value exists.**
Finke-Watzky constants are published for many systems and none for
protein-mediated gold reduction; the literature states that they are
system-dependent and fitted per curve. They stay uncalibrated, and no amount of
reading will change that.

**A challenge to the mechanism, and its answer.** There is a published
challenge to Finke-Watzky itself: "Particle Size Is a Primary Determinant for
Sigmoidal Kinetics of Nanoparticle Formation: A 'Disproof' of the F-W
Mechanism", Chemistry of Materials 2019. **It was answered in print**, Chem.
Mater. 2020, doi:10.1021/acs.chemmater.0c00780. This entry originally recorded
the challenge alone and called it a larger problem; that was written before the
Response was found, and it overstated the position. Corrected the same day.
The mechanism stands. See the update below.

**What is left unsourced and why.** `concentration_factor`, `pH_set`, `G_T`,
`biomass`, `seed_frac` and `protein_target_g_per_L` are process choices, not
properties of anything, and no paper decides them. `k_par` and `k_ox_Cu` remain
`sourced_by_proxy` from ammoniacal systems in an ammonia-free process; that is
recorded in `params/leach.yaml` and was not re-searched.

**New sources:** S46 to S51.

### Update: the mechanism was checked and kept, and recovery left the model

Two decisions, 2026-08-21.

#### 1. Physical recovery is out of scope, permanently

Team decision. There is no physical-recovery model here and there will not be
one. Whatever gold reaches metal is the gold we have.

`eta_phys` was already 1 by a scoping decision of 2026-08-16, but the stage was
not actually gone, and that hid a real inconsistency:

**`docs/make_analysis_figures.py` was still multiplying by a recovery stage,
with `eta_spin` HARD-CODED at 0.50 inside the .py file.** So section 8's
figures answered "how much gold reaches the crucible" while the notebook and
`src/sensitivity.py` answered "how much reaches metal". The hard-coded number
also broke AGENTS.md rule 2, no number in a .py file. Neither had been caught
because nothing compared the two paths.

Now: `eta_spin`, `eta_wash` and `eta_ash` are null and `out_of_scope`, with
their values in `superseded`. `recovery_chain.eta_phys` raises instead of
computing, `sensitivity.chain_eta_total` raises if any of the four is passed to
it, and the tornado has lost its `eta_spin` row. **Every absolute figure from
`make_analysis_figures.py` rises by 1/(0.50*0.95*0.98) = 2.148x; every ratio,
which is what the tornado reports, is unchanged.** The chain test now asserts
0.7965 where it asserted 0.371, and reconstructs both published figures by
putting the retired stage back by hand so neither is lost.

⚠ **eta_total has changed meaning, not just value.** It answers "how much gold
reaches metal". Anything quoting a figure that included centrifugation,
washing and ashing is answering a different question.

#### 2. Finke-Watzky is kept, and the reason is now on the record

The wet lab cannot run the shape experiment, so the mechanism had to be settled
from the literature. It was.

**The 2019 disproof was answered in print in 2020.** F-W remains the standard
model for sigmoidal nanoparticle formation, and the biogenic gold literature
describes the same picture independently: reduction to Au(0), cluster
formation, autocatalytic growth.

**The field's own extension adds to F-W rather than replacing it.**
Mechanism-Enabled Population Balance Modelling inserts a third step,
A + C -> 1.5C, on top of the F-W two. What it buys is the PARTICLE SIZE
DISTRIBUTION -- and that is exactly what decision 1 above just removed from
scope. Two steps is the right level for a model whose deliverable is
conversion.

**What was rejected.** LaMer burst nucleation does not fit a continuously
nucleating system. KJMA/Avrami fits sigmoids too, but the literature warns that
it "affords radically different rate constants for equivalent reaction
conditions" -- so switching families would invalidate every constant without
improving the answer.

**THE RISK WAS NEVER THE MECHANISM. IT IS THE TWO CONSTANTS.** `k_nuc` and
`k_grow` are unmeasured, unsourceable, and the joint #1 driver at 799x and 98x.
`k_grow` now carries `range: [0.02, 2.0]` -- one order of magnitude either way.
That is not a literature band, because there is no literature value; it is the
range section 8.5 already swept, moved out of a figure script and into params/
so the sweep is reproducible. **Any conversion figure from the reduction stage
should be read beside it.**

**New source:** S51, rewritten to carry the Response and the model-family
warning as well as the original mechanism.

### Update: the reduction constants ARE anchorable, and the model is pessimistic

The first search asked for constants for THIS system, protein-mediated gold
reduction, and correctly found none. Asked again, more widely: constants for
GOLD, by any reductant. Those exist, and they change what can be said.

| System | k1 | Converted |
|---|---|---|
| Cinnamon extract, Au(III), 40 C | 0.0056 /min | **0.0858 /h** at 25 C on its own E1 = 70.6 kJ/mol |
| Ascorbate-PVP, HAuCl4, refitted | 2.19e-5 /s | **0.0788 /h** |
| **This model** | | **5e-5 /h** |

**Two independent chemistries agree at about 0.08 /h, and this model is 1,600x
below them.** That looks damning until the units are read: k1 is
pseudo-first-order and absorbs the REDUCTANT concentration. Those systems carry
millimolar reductant; this one carries about 9.2 uM of electrons from Rech_0 at
2 e-, roughly a thousandfold less. Scaling 0.086 down by 1000 gives 8.6e-5 /h,
**within a factor of two of the 5e-5 already in use.** The value survives the
comparison, and it survives it for a reason that can be written down.

**k_grow does not come out as comfortably.** The ascorbate fit gives
k2*[A]0 = 842 /h at full precursor; at the 0.4 mM typical of such preparations
that is **2.1 uM^-1.h^-1** against the **0.2** in use. The 0.4 mM is OUR
assumption, and the answer is linear in it, so treat 2.1 as an order of
magnitude and not a value.

**A tenfold difference in k_grow is the whole reduction stage:**

| k_grow | t_cross | conversion at 24 h of the delivered 0.367 uM |
|---|---|---|
| 0.02, band floor | 136 h | 0.1 % |
| **0.2, in use** | **13.6 h** | **0.3 %** |
| 0.842 | 3.2 h | 16 % |
| **2.1, published-anchored** | **1.3 h** | **99.9 %** |

⚠ **Section 6.3's headline finding -- that reduction does not fail slowly, it
fails to start -- rests on a constant ten times slower than the only published
gold fit available.** At the anchored end the delivered eluate converts
completely with NO concentration step and NO seed.

**0.2 IS KEPT, and that is a decision rather than an oversight.** The published
fits are chemical reductants at millimolar loading; this is a protein at
micromolar, and enzyme-mediated surface growth has no reason to match ascorbate.
Adopting a borrowed constant would rewrite the headline of an entire section on
somebody else's chemistry.

**AND IT IS NOT A CONSERVATIVE VALUE, WHICH THIS ITEM FIRST SAID IT WAS.**
Corrected the same day. The geometric mean of 0.02 and 2.1 is 0.205, so the
adopted 0.2 is the LOG-CENTRE of its own band to within 2 %. For a rate
constant spanning two orders of magnitude the log-centre is the neutral
estimate; the arithmetic mean would be 1.06 and would quietly assume the fast
end. `k_nuc` is the same, 5e-5 against a log-centre of 6.6e-5. Both values are
centred, not pessimistic, and a test now pins each to within a factor of two of
its log-centre so that recentring either is a visible decision.

**What follows from that.** The model is not being pessimistic about reduction;
it is being neutral about a constant nobody has measured, and the neutral answer
happens to be 0.3 % conversion. The right response is not to move the value. It
is to stop quoting a single conversion number.

**What changed in status.** Both constants moved from "weakly calibrated ---
joint #1 driver" with `source: null` to `sourced_by_proxy` with a band and a
citation. They are still the joint #1 driver. What they are no longer is
unanchored.

**THE RECOMMENDATION THIS CHANGES.** `k_grow` was already the most valuable
thing to measure. It is now also the parameter on which this repository openly
disagrees with the published gold literature by an order of magnitude. One
seeded and one unseeded run at a 4x concentration, sampled over 24 h, settles
it -- and if the answer lands near the anchored end, the concentration step and
the seed both stop being necessary.

**New source:** S52.

### Update: the constants are unmeasurable, so the vessel was designed around them

The wet lab has no route to `k_nuc` or `k_grow`, and no published fit exists
for protein-mediated gold reduction. **Waiting for a number is not a plan**, so
the model was asked a different question: not "what is k_grow" but "is there a
vessel that clears the target whatever k_grow turns out to be".

There is. `src/sensitivity.py::reduce_worst_case` evaluates every corner of the
two bands and returns the minimum. Corners suffice because conversion is
monotonic in both constants, which the test pins.

| Vessel | Worst corner of both bands |
|---|---|
| As delivered, 24 h | 0.3 %, fails |
| 4x concentration, 1 % seed, 24 h | 1.1 %, fails |
| 6x concentration, 50 % seed, 72 h | 95.8 % |
| 8x concentration, 25 % seed, 72 h | 95.2 % |
| **10x concentration, 25 % seed, 72 h** | **98.2 %** |

**At the recommended vessel, conversion is at least 98 % at the slowest corner
of both bands and 100 % everywhere else. The true value of k_grow cannot change
the outcome, so it leaves the critical path.** Recorded as
`reagent_arm.robust_design`, with `status: design_recommendation` on each term
so nothing mistakes them for measurements.

**Why it is affordable.** The seed is a quarter of the previous batch, held
back and returned: product, not reagent. Time is the cheapest of the three
levers and it is the one that covers the slow end. The concentration step was
already required for other reasons.

⚠ **NOTHING TESTED CLEARS THE WORST CORNER IN 24 HOURS at any concentration.**
The 72 h batch is not optional, and that is the one real cost of this approach.

⚠ **It is insurance, not a requirement.** At the centred constants 4x and a 1 %
seed already give 89 %. The extra buys immunity to a number nobody can measure,
and the team may decide that is not worth 72 h.

**What this does NOT do.** It does not make the constants known, and it does not
narrow their bands. Every conversion figure in section 6.3 still needs its band
quoted with it. What it does is remove the constants from the list of things
that must be settled before the process can be designed.

### Update: an ENZYME anchor for k_grow, and the design that survives it

Asked to search harder for a cited approximation. The right search was not
"Finke-Watzky constants for our protein" but "has anyone characterised ANY
purified Au(III) reductase". Someone has.

**GolR, from *Erwinia* sp. IMH, JACS Au 2022.** A purified, cytoplasmic Au(III)
reductase. In vitro: **about 67 % of 2 mM Au(III) reduced in 2 h at 30 C and
pH 7 with 1 mM NADH and 1 mM GolR.** Fitting that endpoint through this
repository's own reduction model gives **k_grow = 3.2e-3 uM^-1.h^-1**; a plain
Finke-Watzky fit gives 0.9e-3 to 3.7e-3 depending on the k_nuc assumed.

**A purified enzyme is about sixty times slower than the value in use, and six
hundred times slower than ascorbate.** That is the expected direction and it is
the first anchor in this repository that is the RIGHT KIND of reductant.

**Its electron ledger closes**, which is why the odd "1 mM GolR" can be taken at
face value: 67 % of 2 mM Au(III) at 3 e- is 4 mM of electrons, and 1 mM NADH
plus 1 mM GolR at 2 e- each is exactly 4 mM. Re-running those conditions at
1 uM protein caps conversion at 4 %, so it is not a typographical error.

⚠ **Three limits, all real.** One endpoint and not a time course, so k_nuc and
k_grow cannot be separated from it. Measured at 2 mM gold, applied here at
0.37 uM, five thousandfold lower -- exactly the extrapolation the 2019 particle
size critique warns about. And a different protein from ours.

#### The band, and a bias now declared

`k_grow` range moves from [0.02, 2.1] to **[3.2e-3, 2.1]**, 656-fold, with a
citation at each end. The VALUE did not move, and that is now a bias rather
than a neutral choice: 0.2 was the log-centre of the OLD band, and the
log-centre of the anchored band is 0.082, so **the value in use sits 2.4x above
centre, on the fast side.**

It was kept for two reasons, and neither is that it is right. Moving it fails
eleven pinned tests and re-derives every published reduction figure. And the
design below is sized on the BAND, not on the value, so the bias does not reach
the recommendation. **Recentring to 0.082 is an open decision for the team.** A
test now pins the SIZE of the bias, between 2x and 3x, so it cannot drift
unnoticed.

#### The design had to change, and dithionite is what saved it

The previous recommendation -- 10x, 25 % seed, 72 h -- gives **25 %** at the new
floor. It fails. Raising concentration and time alone does not fix it either:
30x with a 50 % seed over 168 h reaches 82 % and then STOPS, and 336 h gives
the same 82 %.

**It stops because it runs out of electrons, not because it is slow.** At 30x
the vessel holds 11 uM of gold, and S35's own 4.6 uM of dithionite supplies
14.9 uM of electrons in total. **Starved of electrons, more time is no cure**,
and a test now pins exactly that.

| Vessel | Worst corner |
|---|---|
| As delivered, 24 h | 0.1 % |
| 10x, 25 % seed, 72 h | 25 % |
| 30x, 50 % seed, 168 h, 4.6 uM dithionite | 82 %, and stuck |
| **30x, 50 % seed, 96 h, 50 uM dithionite** | **98.0 %** |

Dithionite is a bought reagent (item 51), not something the process must make,
so it is the cheapest term in the design. `robust_design` now carries it.

**New source:** S53.

### Update: S35 read directly, and the dithionite question is already settled

The team asked whether the lab can obtain sodium dithionite. **The source
protocol cannot be run without it.** S35's methods, read from the PDF on
2026-08-21, verbatim:

> "The reaction was activated by adding 100 uL sodium dithionite (46 uM)
> dissolved in sodium hydrogen carbonate (100 uM)."

The paper's own word is **activated**. So the design does not introduce a new
chemical; it asks for MORE of one the protocol already requires. The whole
recipe was re-read and every number this repository took from it checks out:
1000 uL total, giving **4.6 uM dithionite and 0.1 uM methyl viologen final**.

**The quantity is milligrams.** Na2S2O4 is 174.1 g/mol, so the design's 50 uM
is **8.7 mg per litre**. S35's own 4.6 uM is 0.8 mg/L.

#### And nothing else can do the job

The obvious alternative is more reductase. **It does not work, and it makes
things worse.** Holding dithionite at S35's 4.6 uM and raising the protein
target from 0.2 to 4.0 g/L moves the worst corner from 0.80 DOWN to 0.75.

The reason is in the rate law: it carries `E_red/E_tot`, the FRACTION of enzyme
that is reduced. Adding enzyme against a fixed donor pool dilutes the reducing
power per molecule. This sharpens item 64's finding that more reductase does
nothing: at the electron ceiling it is actively counterproductive. A test now
pins it.

**The electron donor is the only lever.** If dithionite genuinely cannot be
obtained in quantity, the reduction stage needs a different donor -- GolR in
S53 uses NADH -- and that is a chemistry decision, not a modelling one.

#### One tension in S35, left standing

The concentration and pH series for the mesophilic host were run **at 30 C**,
yet the same paper's temperature results say *"Nanoparticle formation in
mesophilic host proteins was observed to begin at 55 C, with optimum formation
at 65 C."* If formation begins at 55 C, the 30 C series should show little.

**Not resolved here, and not modelled.** Temperature is deferred, item 29, and
the reduction stage of this repository is silent about temperature altogether.
Recorded because it bears directly on whether the reduction vessel needs
heating -- which nothing in the current design accounts for.

### Update: dithionite adopted at 50 uM, and it changes more than reduction

Team decision 2026-08-21, after reading S35's methods: the reagent is not
optional in the source protocol, so the only question was quantity.
`reduction.Rech_0` moves from **4.6 uM to 50 uM**, `status: design_choice`.
S35's own 4.6 uM is preserved in `superseded` and the 2026-08-17 lysate-
carryover record is preserved beside it under `superseded_2026_08_17`, so
neither retirement overwrites the other.

**The electron budget moves 14.9 -> 105.7 uM**, and the donor now carries
**94.6 %** of it against the enzyme's 5.4 %. Everything below follows from that
one ratio.

| | Before, 4.6 uM | After, 50 uM |
|---|---|---|
| Electron budget | 14.9 uM | **105.7 uM** |
| eta_reduce at 1 uM gold | 0.024 | 0.029 |
| eta_reduce at 3 uM gold | 0.973 | **0.9925** |
| 4x concentration, 1 % seed | 0.885 | **0.922** |
| 6.6x concentration, no seed | 0.830 | **0.913** |
| Where the ceiling bites | near 15 uM gold | **near 100 uM** |

#### The consequence nobody asked for: the arm-B shortfall stopped mattering

`protein_target_g_per_L` = 0.2 was set because E_tot fed the electron ceiling.
With the donor carrying 95 % of the electrons, that target is now only a
KINETIC requirement, and the kinetics barely notice it:

| Reductase | eta_reduce at 4.33 uM, before | after |
|---|---|---|
| 0.20 g/L, the target | 0.9996 | 1.0000 |
| 0.05 g/L | 0.978 | 1.0000 |
| 0.02 g/L | < 0.75 | **> 0.99** |
| 0.0054 g/L, raw lysate at 50 % lysis | < 0.30 | **> 0.99** |

**The old floor is gone.** Before, the raw lysate converted under 30 % because
the protein WAS the electron supply. Now it clears 99 %. The 3.0x reagent-arm
shortfall of item 52 is still real as a mixing constraint, but it has stopped
being a reduction constraint. THE CONCENTRATION STEP ON THE GOLD IS STILL
REQUIRED; it is the protein side that relaxed.

#### What did not change

The kinetics. At the delivered 0.367 uM, conversion is 0.32 % against 0.30 %
before. **Dithionite buys electrons, not speed.** The concentration step, the
seed and the batch length are all still needed, and the k_grow band still spans
the stage.

#### Tests

Seven failed on the change and all seven were wrong rather than the model:
five pinned pre-dithionite conversions, one pinned the old electron budget, and
one read S35's recipe from `value` instead of from `superseded`. That last one
is the important repair: **a test that pins what a SOURCE did must not read the
field this project is free to change.** It now reads `superseded` explicitly.

---

## 60. Trithionate was dropped at Joint 1, the same way tetrathionate once was

Found 2026-08-19 by the model audit, hours after the change that caused it,
and fixed the same day. It never reached a report.

**Was wrong.** The alkaline decomposition route added to Part I on 2026-08-19
makes trithionate: two per four tetrathionate decomposed, and nothing consumes
it at 25 C. It became the largest sulfur pool in the vessel.
`src/interfaces.py::sulfur_feed_from_leach` still carried tetrathionate and
thiosulfate only, so the polythionate load reaching GolB was under-reported:

| scenario | reported | actual | understated by |
|---|---|---|---|
| ammonia | 84,235 : 1 | 540,152 : 1 | **6.4x** |
| glycine | 76,110 : 1 | 229,614 : 1 | **3.0x** |

This is precisely the failure item 44 was raised to stop: a sulfur species
dropped silently at the joint while every number still looked plausible. It
was reintroduced in the same file, seven days after item 44's fix landed, by
the change that added the alkaline route. The joint is not a place where a new
species can arrive by default.

**What was done.**

1. `sulfur_feed_from_leach` now takes `s3o6` as a **required** argument with
   no default, and returns `S3O6_uM` and `polythionate_uM`. A default of zero
   would have recreated the bug; the missing argument instead broke the only
   caller immediately, which is what it is for.
2. `thiol_blocking_warning` takes `s3o6_uM` and reports **two ratios**.
3. `model.ipynb` now prints the sulfur handover. It never called either
   function, so before this the blocking item's number appeared nowhere in the
   presented results at all.

**The second ratio is a bound, not a result.** Tetrathionate's mechanism is
established: the cysteine thiolate attacks its outer sulfur to give a
cysteine-S-sulfonate, and across a Cys-X-X-Cys motif the sulfenylthiosulfate
intermediate closes an intramolecular disulfide. **Trithionate's reactivity
relative to tetrathionate is not published.** It is a polythionate and it does
react with thiols, but no comparison was found in the accessible literature,
and the structures differ in a way that should matter: tetrathionate carries
two sulfane sulfurs joined by an S-S bond, trithionate carries one, flanked by
two sulfonates. No relative rate constant is invented. The combined ratio
assumes equal reactivity, which is the worst case, and says so wherever it is
printed.

**What would settle it.** One GolB binding assay in trithionate, against the
same assay in tetrathionate. Same protein, same gold, one variable. That
number turns the bound into a result and it is the same experiment item 44
already needs.

**Pinned by** `tests/test_interfaces.py::
test_trithionate_is_required_at_the_joint_and_never_defaulted`,
`::test_the_warning_reports_the_bound_separately_from_the_measured_ratio` and
`::test_the_joint_sees_what_the_leach_scenarios_actually_produce`. The last
one reads the sulfur states off a finished leach rather than from a literal,
so a new species added to Part I and not to the joint fails there. That is the
check that was missing.

**Read with:** item 44, which it feeds and which stays blocking; item 59,
where the polythionate gap is the reason glycine wins.

---

## 59. Ammonia beats glycine on gold, and glycine is still the right choice

Found 2026-08-19 by building the two-ligand scenario comparison that item 54
recommended, and getting the opposite of the expected answer on the headline
number.

### What item 54 said, and why it does not transfer

Item 54 reports that glycine roughly doubles 24-hour gold recovery. That was
measured against **no ligand at all**, which is the comparison v5 draws
("WITH AMMONIA" against "WITHOUT AMMONIA"). It is true and it is not the
decision. Nobody proposed running with no ligand; copper destroys 98 % of the
charge and the leach fails. The decision is **which** ligand.

Run properly, at one operating point, ammonia wins on gold:

| | 6 h | 12 h | 24 h | 48 h | 72 h |
|---|---|---|---|---|---|
| ammonia, 266 mM | 6.88 % | 13.96 % | 28.94 % | 69.82 % | **100.00 %** |
| glycine, eps 0.0024 | 6.80 % | 13.66 % | 27.53 % | 55.87 % | 84.97 % |
| glycine, eps 0.0116 | 6.80 % | 13.64 % | 27.43 % | 55.40 % | 83.79 % |
| glycine, eps 0.0421 | 6.79 % | 13.59 % | 27.24 % | 54.52 % | 81.10 % |

Both at pH 10.0 held by the pump, air-pump oxygen, 6 mm crush, 72 h.

**Why ammonia now runs to completion**, when in the 2026-08-12 model it stalled
at 41 %: with the alkaline return leg open, thiosulfate no longer runs out.
Tetrathionate is recycled, the leachant survives, and ammonia's fast Cu(II)
route (`k_Au_Cu` = 1500 against glycine's 21.0) then has something to work
with for the whole 72 hours. Ammonia's advantage is real and it is entirely
in the 24-to-72-hour window.

### Why the decision does not change

**1. At 24 hours the two are the same.** 28.94 % against 27.24 to 27.53 %,
under 1.7 points. v5's own recommendation is to run one day, not three,
because "batch turnaround is worth more than residence time". At the batch
time this project actually plans, the gold difference is inside the noise of
every constant involved.

**2. Glycine hands downstream far less polythionate, and item 44 is BLOCKING.**

| | tetrathionate | trithionate | total polythionate |
|---|---|---|---|
| ammonia | 9 097 | 49 239 | **58 336** |
| glycine, eps 0.0024 | 2 720 | 5 097 | **7 817** |
| glycine, eps 0.0421 | 12 353 | 31 833 | **44 187** |

Item 44 blocks because tetrathionate attacks the cysteine pair GolB binds gold
through. Ammonia reaching 100 % gold is worth nothing if the capture stage
cannot take it, and ammonia gets there by pushing 7.5x more polythionate at
the protein. **The two blocking items pull in opposite directions and the leach
optimum is not the process optimum.** Same trap as item 39.

**3. Glycine costs about half the reagent.** Titrant demand is -68 758 umol/L
for ammonia against -13 415 to -58 960 for glycine. Both are acid demands.

**4. The ammonia column is an upper bound that the real vessel cannot reach.**
Ammonia above pH 9.25 is mostly free NH3. The team has an air pump, and
sparging air through alkaline ammoniacal liquor is the standard method for
stripping ammonia out of water. No stripping rate has been measured, so the
scenario assumes none happens. It would.

### The comparison is deliberately generous to ammonia

Three handicaps run against glycine, all recorded beside the scenarios in
`params/leach.yaml`:

1. no ammonia stripping, as above
2. ammonia keeps its own measured constants; glycine's decisive constant
   `eps_gly` is unmeasured and spans 17x
3. `k_ox_Cu` is ammoniacal in **both** columns, because no ammonia-free value
   exists. Ammonia slows Cu(I) re-oxidation, so the true ammonia-free value is
   probably larger, meaning more Cu(II) and a larger job for glycine

Glycine loses the gold column under all three handicaps and still wins the
decision. That is a safer place to be than winning on a number.

### What this does not settle

Whether the 72-hour gap matters at all depends on batch time, and batch time
depends on what the capture stage can absorb. That is item 39 and item 43, and
neither is closed.

**Pinned by** `tests/test_leach.py::
test_ammonia_beats_glycine_on_gold_and_glycine_is_still_the_choice`, which
asserts the ammonia win, the 24-hour tie, the polythionate gap and the titrant
gap together, so the uncomfortable half cannot be dropped while the convenient
half is kept.

**Read with:** item 54, whose 24-hour claim this narrows; item 44, which it
partly relieves; item 39, whose trap it repeats.

---

## 58. v5's Stage-1 enzyme yield contradicts v5's own derivation

Found 2026-08-19 while auditing "Bioleaching_Models_v5.docx" before adopting
its parameter changes.

The Stage-1 parameter table gives `[E]_culture = 4.75e-3 umol/L`, "about 2 860
molecules per cell". The Supplementary Material derives `k_syn` from the golB
site-density cascade and gets `1.43356e-16 umol cell^-1 min^-1`. Substituting
that back into the document's own steady-state equation:

    [E] = k_syn * X / (k_deg + mu)
        = 1.43356e-16 * 1e12 / (0.0011 + 0.0173)
        = 7.791e-3 umol/L

I reproduced the intermediate `4691.81 proteins cell^-1 min^-1` and `k_syn`
exactly, so the derivation is sound and **the table value is the one that is
wrong, low by a factor of 1.64**.

The document then uses **both**, in different sections:

| section | value used | culture volume it gives |
|---|---|---|
| Stage 1 Analysis | 7.791e-3 | "5.5 litres of culture per litre" |
| Stage 2 Analysis | 4.75e-3 | "needs 9.1 L of culture per litre" |

Same quantity, same document, two answers. The Analysis text even prints
`0.007791 umol/L (4692 molecules/cell)` two lines below a table saying 2 860.

**What it costs.** Nothing downstream: Stage 1 is algebraic and does not enter
the Stage-2 or Stage-3 differential equations. It costs the sizing claim, which
is the one thing Stage 1 exists to produce. 5.5 L against 9.1 L of culture per
litre of conversion vessel is a 65 % difference in the largest capital item in
the process.

**Who decides:** the document's author. **Left standing in the text.**

**Read with:** item 39, which records that there is no purification-yield term
anywhere, so both figures are floors regardless of which is right.

---

## 57. v5's `k_cat` reasoning says 2.2 U/mg and its arithmetic uses 2.5

Found 2026-08-19, same audit as item 58.

The Supplementary Material states: "The reported TetH activity when expressed
in E. coli can be modelled as 2.2 U mg^-1", then computes

    k_cat = 2.5 umol min^-1 mg^-1 x 50 mg umol^-1 = 125 min^-1

The parameter table also carries "2.5 U mg^-1". So the prose says 2.2 and
everything else says 2.5.

**This one is decision-relevant, unlike item 58.** Integrating the closed-form
Michaelis-Menten solution the document itself provides,
`K_m ln(S0/S) + (S0 - S) = Vmax t`, over the 3-day Stage 2:

| k_cat | conversion in 3 days | S2O3 delivered to Stage 3 |
|---|---|---|
| 125, as computed | 95.9 % | 94 359 |
| 110, as stated | **85.6 %** | 91 965 |

The headline "95.9 % conversion in three days" does not survive the stated
value. The Stage-3 answer barely moves, because 2.5 % less thiosulfate is
noise next to what Cu(II) destroys.

**Which is right is not knowable from the document.** 2.2 U/mg is the figure
attributed to the E. coli-expressed enzyme; 2.5 appears only in the
calculation. This repository already carries `k_cat_per_subunit` from a
different route and is unaffected.

**Who decides:** the document's author. **Left standing in the text.**

---

## 56. v5's sulfur conservation check counts molecules, not sulfur atoms

Found 2026-08-19, same audit as item 58. This is the one worth fixing, because
a check that passes on the wrong quantity is worse than no check.

v5 Stage 2 states: "Since Y = 1, the total sulfur is conserved:
`[S4O6] + [S2O3] = constant`. This gives a useful numerical check."

That sum is a **molecule count**. Tetrathionate carries four sulfur atoms and
thiosulfate carries two. Using v5's own reported endpoints:

```
molecules   23 200 + 72 100 = 95 300      ->    941 + 94 359 = 95 300   flat
S atoms   4(23 200) + 2(72 100) = 237 000 -> 4(941) + 2(94 359) = 192 482
```

**44 518 umol/L of sulfur, 18.8 % of the charge, leaves the vessel unaccounted
for.** It is not lost: v5's own Stage-2 reaction is
`S4O6(2-) + H2O -> S2O3(2-) + S(0) + SO4(2-) + 2H+`, which produces elemental
sulfur and sulfate. Neither is tracked, and the check cannot see them because
it is not counting atoms.

The sum is constant because the reaction is one molecule in, one molecule out.
It would stay constant under almost any error in the coefficients, so it
**cannot catch anything**.

**Fixed on this side, not in the document.** `src/leach.py::sulfur_audit`
counts atoms, 4 / 2 / 3 for tetrathionate / thiosulfate / trithionate, plus an
accumulator for the thiosulfate drawn into the metal complexes. Pinned by
`tests/test_leach.py::test_sulfur_atoms_are_conserved_once_the_alkaline_route_is_open`,
which also asserts that the molecule count does **not** close, so nobody
reintroduces it.

The audit earned its place twice while it was being written. It caught
trithionate being given six sulfur atoms instead of three, and then a 3 %
drift from the metal-complex draw that no end-state sum can reconstruct,
because copper takes 2 thiosulfate on the oxygen route and 4 on the Cu(II)
route.

**Who decides:** the document's author, for the document. The repository side
is done. **Left standing in the text.**

---

## 55. v5's 24-hour gold figure disagrees with v5's own rate description

Found 2026-08-19 while checking the ammonia-free parameter change against v5.

Adopting v5's three ammonia-free constants, this repository reproduces the
whole of v5's ammonia-free section **except one number**:

| quantity | v5 reports | here |
|---|---|---|
| thiosulfate to gold | 57.9 | 57.9 |
| thiosulfate to copper | ~1 640 | 1 639.7 |
| thiosulfate to the parasitic reaction | 92 661 | 92 661.1 |
| Cu(II) peak | 818 | 818.0 |
| gold at 72 h | 28.93 % | 28.49 % |
| **gold at 24 h** | **19.69 %** | **27.75 %** |

Four figures to the digit, and one that is 8 points out.

**v5's own text argues against its own number.** The same section says f_S
"falls below 0.5 by 23.7 hours and is effectively zero by 26-28 hours", and
that the rate "starts near its maximum at 0.6 hours and declines monotonically".
A run that is chemically over by 26 hours cannot have banked only 68 % of its
gold at 24. It has banked essentially all of it, which is the 97 % this
repository gets.

The 19.69 % looks read off the ammoniacal figure or an adjacent curve.

**What it costs.** It is the number the batch-time recommendation rests on.
"Run Stage 3 for one day, not three" is right, and it is *more* right than v5
says: the extra 48 hours are worth 0.7 points, not 9.2.

**Pinned by**
`tests/test_leach.py::test_ammonia_free_constants_reproduce_the_v5_thiosulfate_ledger`,
which asserts all four agreeing numbers and both of the disagreeing ones, so
the disagreement cannot quietly close.

**Who decides:** the document's author. **Left standing in the text.**

---

## 54. Glycine is the ammonia-free way to stop copper destroying the lixiviant

Found 2026-08-19 while looking at the process rather than the equations.

Both Part I write-ups reach the same conclusion by different routes: copper
destroys the thiosulfate, and the fix is a ligand that holds Cu(II) still.
Both then reach for **ammonia**, and item 41 recommends lowering oxygen as the
cheaper alternative. There is a third option neither considered, and it is the
one the recent literature has converged on.

### The mechanism

Glycine holds Cu(II) as copper glycinate. The complex **still oxidises gold**
-- electrochemical work reports the Cu(II)-glycine complexes are themselves the
catalysts for anodic gold dissolution -- while free Cu(2+), the species that
attacks thiosulfate, is suppressed. That asymmetry is the whole point. Ammonia
does the same job; glycine does it without the toxicity.

It also explains the published operating window. Gly- is the chelating form and
its pKa is about 9.8, so below pH 9.3 there is too little of it. That is why
every glycine-thiosulfate paper reports pH 9.3-10.5, and it is the same window
this project already needs for thiosulfate stability (item 23).

### Why it suits this project specifically

| | ammonia | glycine |
|---|---|---|
| toxicity | volatile, needs fume control | food grade |
| deployable at Agbogbloshie | no | yes |
| biodegradable | - | yes |
| fits a biological process narrative | no | it is an amino acid |
| pH ceiling on Cu(II) | raises it | raises it |

The first two rows are Human Practices constraints deciding a chemistry
choice, which is the right way round for this project.

### The number, and how far to trust it

The reactivity of copper glycinate toward thiosulfate is not published
directly. Its consequence is: thiosulfate consumption falls from **5.2 g/L to
2.2 g/L** when glycine is added, a 58 % reduction. Calibrating the model
against that observable, and never against gold, gives

    eps_gly ~ 0.012      copper glycinate is about 1 % as reactive
                         toward thiosulfate as free Cu(2+)

Re-calibrating under five different operating conditions gives 0.0024 to
0.0421, a **17x spread**. The constant is therefore not clean, and the
single-parameter form is an approximation. But the conclusion survives the
whole band:

| case | gold at 24 h | hours to 50 % |
|---|---|---|
| no glycine | 29.1 % | 37.5 |
| glycine, across the full 17x band | 50.9 - 56.6 % | 22.1 - 23.7 |

Gold was not used in the calibration, so those figures are a prediction.

**Two caveats, both real.** The 5.2 -> 2.2 g/L measurement is on an auriferous
ORE with copper dosed at 5 mM. A waste PCB is 30 wt% copper and generates its
own continuously; the mechanism transfers, the number is from a different feed.
And the published glycine-thiosulfate work runs at 30-60 C, while this model is
isothermal at 25 C and temperature is a deferred item.

### What it changes elsewhere in the model

1. **It weakens item 41's oxygen recommendation.** Starving oxygen protects
   the lixiviant geometrically. Glycine protects it chemically, and better.
2. **It reverses item 53's crush-size direction at short batch times.** With
   the lixiviant chemically protected, finer crushing wins on rate because
   more Cu(II) leaches gold faster. Coarse still wins on ultimate recovery.
   Crush size trades rate against final yield, and the trade moves with
   glycine.
3. **It helps item 44.** Less parasitic reaction means less tetrathionate
   reaching the GolB cysteines.

### The open question nothing in the literature answers

**Does glycine interfere with GolB?** Glycine is not a thiol, so it should not
compete for the cysteine pair, and gold(I)-glycine is weak against
gold(I)-thiosulfate. Neither statement was found stated anywhere. This is the
one thing that could make the recommendation wrong for this project
specifically, and it is a binding-assay question, not a leaching one.

**Who decides:** the wet lab, and it is a leach they can run.

**What would settle it:** two leaches side by side, same feed, same pH, one
with 20 g/L glycine and one without. Assay gold and thiosulfate at 6, 24 and
48 h. The thiosulfate curves pin `eps_gly` for this feedstock directly, and
the gold curves test the prediction above. Then one GolB binding assay in the
presence of glycine.

**Read with:** item 41, whose recommendation this partly supersedes; item 53,
whose direction it reverses at short batch times; item 23, whose pH window it
explains mechanistically for the first time.

---

## 53. No liberation term: the crush-size recommendation runs off the end of the model

Found 2026-08-19 while walking the crush-size result through with the team.

Both Part I models compute the exposed gold area as a constant:

    A_Au = m_Au / (rho_Au * t_film) = 2.07e-3 m^2

There is no `d` in that expression, so **crushing never changes the gold area**,
while copper area goes as `6/d`. That asymmetry is real, and it is why both
models agree that coarser crushing is better:

| crush | A_Au | A_Cu | gold at 72 h, v7 | gold at 72 h, Model M |
|---|---|---|---|---|
| 2 mm | 2.07e-3 | 10.04e-3 | 32.0 % | 72.8 % |
| 4 mm | 2.07e-3 | 5.02e-3 | 41.0 % | 91.4 % |
| 6 mm | 2.07e-3 | 3.35e-3 | 47.7 % | 100 % |

The two models disagree about magnitude by a factor of two and agree exactly
about the direction. The direction is probably real.

### The problem is what happens past 6 mm

`A_Au` is constant **for every value of `d`**, including values where the
assumption behind it is false. Ask either model about 20 mm chunks and it will
report still-better recovery. Ask about whole uncrushed boards and it will
report better again. Neither model can decline the question.

The missing physics is that gold on a PCB is not one population:

- **exposed plating** on edge fingers, pads and connectors, wetted at any size
- **encapsulated gold** in bond wires and leadframes inside IC packages, wetted
  only once the package is broken open

`t_film` = 0.5 um describes the first. Nothing in either model describes the
second. Part I's author names the limit in his own §18 — "above some particle
size, gold on internal surfaces stops being accessible to the liquor at all,
and the thin-film assumption breaks down. The model does not capture that
limit" — and then publishes a coarse-crushing recommendation anyway.

### What the term should look like

Two limits are known without any experiment:

    d -> 0     every package broken            f_lib -> 1
    d -> large only surface plating accessible f_lib -> f_exposed

The separating scale is the size of the components themselves. The simplest
shape hitting both limits:

    A_Au(d) = [ m_Au / (rho_Au * t_film) ] * f_lib(d)

    f_lib(d) = f_exposed + (1 - f_exposed) / (1 + (d / d_pkg)^n)

### Why this term is worth adding and most are not

Both new parameters are measurable here, cheaply, without literature access:

| parameter | how to measure it |
|---|---|
| `f_exposed` | leach an **uncrushed** board. Nothing is liberated, so the gold that comes out is the exposed fraction, directly |
| `d_pkg` | measure the IC packages on your own boards with callipers |

That is two afternoons and no paywall. Compare with `k_par`, `k_ox_Cu` and
`k_alk`, none of which can be settled locally.

**Do not fit these two.** Between them they can move gold recovery almost
anywhere, so a fitted `f_lib` would absorb error from every other term in the
model and make the result untestable. This is the same trap item 41's
`k_ox_Cu` sensitivity warns about, and the trap the v7 write-up fell into with
its fitted `n_OH`. Per AGENTS.md rule 4, both stay `null` and the term stays
off until they are measured.

### What this changes today

Nothing in the numbers. It changes what may be **said** about them. Until the
term exists, the honest form of the recommendation is:

> within the 2-6 mm range tested, coarser is better

and not "crush coarser", because the model is blind to the failure mode at the
coarse end and will not warn anyone who asks it.

**Who decides:** the team, with the wet lab. The uncrushed-board leach is the
whole experiment.

**What would settle it:** leach at 2, 4, 6 mm and uncrushed, on the same feed,
and assay gold. A monotone rise confirms the model inside the range. A turning
point locates `d_pkg` and is the number the model cannot compute.

**Read with:** item 19, which records that `t_film` = 0.5 um is a team
assumption and not a board spec, and that recovery scales as 1/`t_film` across
a 20x range. Item 53 is the second assumption sitting under the same headline.

---

## 46. Gold is allowed to accumulate in a liquor that cannot hold it

Found 2026-08-12. Two facts sit next to each other in the model and are never
put together.

1. Free thiosulfate reaches **zero** by the end of Stage 3. All 94 359 µmol/L
   is consumed, 98 % of it by the parasitic reaction.
2. **30 grams of metallic copper is still in the vessel.** Copper recovery is
   0.176 %, so 99.8 % of it never dissolves and sits in contact with the liquor
   for the whole run.

Meanwhile `Au(S2O3)2 3-` climbs to 39 µmol/L and the model treats it as an
inert accumulator. It has no decomposition term and no re-precipitation term.

### Why that is not safe

**The complex needs the ligand it no longer has.** Published stability
constants for gold(I) thiosulfate complexes are determined with a large ligand
excess, over Au:S2O3 ratios of about 1:5 to 1:200, and excess thiosulfate is
what polarises gold against depositing out of the complex.
[S35](SOURCES.md). Our end state is 39 µmol/L of gold against **zero** free
thiosulfate. That is outside any regime the constants were measured in, and it
is on the wrong side of it.

**Metallic copper cements gold out of thiosulfate solution.** It is a used
recovery technique, not a hypothetical: copper cementation avoids introducing
foreign cations, and the practical difficulty reported with it is the reverse
problem, that dissolving copper raises the potential and **re-dissolves** the
gold. [S36](SOURCES.md). Both directions are live in our vessel, which holds
metallic copper, Cu(II) at 829 µmol/L, and dissolved gold, all at once.

**So the 39 µmol/L may be gold the vessel never actually holds.** It may plate
back onto the copper as the leachant runs out, which is precisely when the
model says the gold peaks.

### What this changes

If gold does cement back, then the second half of the run is worse than
useless: it destroys the leachant *and* gives the gold back. That would
strengthen the case for stopping early on completely different grounds from
item 21, and it makes the oxygen optimum of item 41 more valuable, since the
run that leaves 15 000 µmol/L of thiosulfate unspent is also the one that keeps
its gold in solution.

**Who decides:** Part I's author, with a wet-lab measurement.

**What would settle it:** assay dissolved gold in the liquor at 24, 48 and
72 hours. If it peaks and falls while solid gold keeps dissolving, cementation
is real and needs a term. This uses a leach the team will run anyway.

---

## 41. Cu(I) re-oxidation decides the process, and the oxygen level is the handle

Found 2026-08-12 while auditing Part I's sequential model. **This reverses the
conclusion written in item 20, and it is the most actionable finding in the
project so far.**

### What everyone believed

Copper is the villain. It dissolves off the board, becomes Cu(II), and Cu(II)
destroys thiosulfate:

    2 Cu(II) + 2 S2O3(2-)  ->  2 Cu(I) + S4O6(2-)

Both of Part I's write-ups say so, and the ledger agrees: **98.2 % of the
thiosulfate charge goes down this reaction**, against 1.8 % to copper metal and
0.08 % to gold. The recommendation that follows is to add a ligand, ammonia or
citrate or EDTA, to hold the Cu(II) still.

### What is actually true

Cu(II) is not what comes off the board. **Copper metal dissolves as Cu(I)**, on
both routes. There is exactly one reaction anywhere in Part I that makes
Cu(II), and it is oxygen:

    4 Cu(I) + O2 + 2 H2O  ->  4 Cu(II) + 4 OH-        rate k_ox_Cu * [O2] * [Cu(I)]

Switch that one reaction off and the Cu(II) pool never forms at all. The
thiosulfate survives. Gold keeps leaching on the oxygen route alone:

| `k_ox_Cu` | Cu(II) peak, umol/L | S2O3 left at 72 h | Gold at 72 h |
|---|---|---|---|
| 0 | 0.00 | 89 145 | **87.6 %** |
| 1e-4 (baseline) | 829 | 0 | 38.4 % |

The board is not the source of the poison. **The sparger is.**

### The handle, and it is free

`k_ox_Cu = 0` is not available: at 500 umol/L of dissolved oxygen, Cu(I) will
be oxidised. But the rate is proportional to `[O2]`, and `[O2]` is an operating
choice. Oxygen pulls in two directions at once. It drives the gold and copper
leaching routes, and it manufactures the Cu(II) that destroys the leachant. So
recovery peaks at an interior oxygen level:

| `[O2]`, umol/L | 50 | 60 | **80** | 100 | 150 | 500 (baseline) | 1000 |
|---|---|---|---|---|---|---|---|
| Gold at 72 h | 50.4 % | 56.0 % | **60.9 %** | 57.8 % | 52.2 % | 38.4 % | 33.2 % |

**Turning the sparger down from 500 to about 80 umol/L takes gold recovery from
38 % to 61 %.** It costs nothing, needs no new reagent, and needs no new unit
operation. Below the optimum the leach is starved of oxidant; above it, the
reactor poisons itself faster than it leaches.

Compare that with the intervention both write-ups recommend. A ligand that
stabilises Cu(II) attacks the symptom. Lowering the oxygen stops the Cu(II)
being made in the first place.

### What is solid and what is not

Solid: the existence of the optimum. It survives every value of `k_par` tested,
though its position moves, to 200 umol/L at `k_par` = 1e-6 and to 50 umol/L at
1e-4.

Not solid: the number 80. It rests on `k_par` and `k_ox_Cu`, both borrowed from
ammoniacal literature where ammonia deliberately stabilises Cu(II). Do not put
80 umol/L on a set-point sheet.

There is also no oxygen mass-transfer model anywhere in Part I. `[O2]` is held,
not solved. Running deliberately oxygen-poor is exactly the regime where that
assumption is worst, because a held `[O2]` cannot deplete.

### What to do

1. Wet lab: run the leach at two oxygen levels, sparged and lightly aerated.
   This is the cheapest high-value experiment available.
2. Measure `k_ox_Cu` and `k_par` in the actual, ammonia-free liquor.
3. Modeller: add a `kLa` term so oxygen can deplete. Part I's simultaneous file
   has an `O2_mode = 'mtc'` branch already, but it charges oxygen to the whole
   copper rate instead of the oxygen route only. Fix that before using it.

Pinned by `tests/test_leach.py ::
test_cu_I_reoxidation_is_what_makes_copper_fatal` and
`test_dissolved_oxygen_has_an_interior_optimum_well_below_the_baseline`.

**Supersedes the reasoning in item 20**, which read as though a small
`k_ox_Cu` would hurt. It helps. Item 20 is closed and this restates it, per
AGENTS.md rule 6.

---

## 38. Stage 2 needs pH 3 for the enzyme, and thiosulfate is unstable there

Found 2026-08-12. Part I's author names half of this in his Limitations
section; the other half is not in either document.

The sequential design puts tetrathionate hydrolysis in its own vessel, Stage 2,
with purified enzyme and nothing else. That is a good answer to item 32: the
enzyme can be refolded at pH 4 in vitro and then used at whatever pH it likes,
because no living cell has to tolerate that pH.

But it inherits the pH with it. `k_cat` = 125 min^-1 comes from assays at pH 3
and 30 C. TetH's catalytic optimum is pH 3.0 and its mechanism needs a
protonated Asp325. So Stage 2 must run at about pH 3 to convert in three days.

**Thiosulfate does not survive at pH 3.** It disproportionates in acid:

    S2O3(2-) + 2 H+  ->  S(0) + SO2 + H2O

Stage 2's entire purpose is to accumulate 94 mM of thiosulfate and bank it. The
model has no term for this loss, so the model cannot see the problem.

The two constraints point opposite ways, and the gap is large:

| | Wants |
|---|---|
| TetH turnover | pH 3 |
| Thiosulfate stability | pH above about 4, comfortably above 5 |
| Gold leach chemistry (item 23) | pH 9 to 10.5 |

The author writes "Stage 2 would need to run near those conditions ... which
conflicts with the alkaline conditions thiosulfate prefers." He is right, and
the disproportionation reaction is the mechanism, and there is no rate for it.

**Who decides:** the team, with the wet lab.

**What would settle it:** the acid decomposition rate of thiosulfate at pH 3 to
5 and 30 C, and TetH's activity at pH 5 to 6. If activity at pH 5 is even a
tenth of the pH 3 value, Stage 2 simply runs longer at a stable pH, and the
whole conflict disappears into a larger `E_stage2` or a longer `t_stage2`.
Neither costs anything the model cannot absorb.

**Until then:** treat the 95.9 % conversion in three days as an upper bound.

---

## 39. Joint 1 now delivers 39 uM gold, and Part III falls off a cliff at 30

Found 2026-08-12. This is the first time Part I has produced a number for
Joint 1 at all, and it lands outside the window Part III can use.

> **Corrected the same day. Read item 43 first.** This item was written as
> though 39 µM were a concentration to be tuned, and it recommended a stopping
> rule as the free fix. That was the wrong frame. The capture step is over
> capacity at any leach recovery above 0.053 %, so no stopping point makes it
> fit. The analysis below is correct on the toxicity ceiling and on why
> dilution fails, and it stays. The conclusion it reaches is superseded by
> item 43. Restated, not erased, per AGENTS.md rule 6.

`src/interfaces.py :: feed_warning` fires above 30 uM, quoting Part III section
2.1: the `A_tox` disagreement costs 63 to 96 % of capture above that. Part III
recommends operating at 10 to 20 uM.

The sequential leach ends at **39.0 uM** of Au(S2O3)2(3-). Worse, every change
that improves the leach makes the joint worse, because they are the same
number:

| Case | Gold recovered | Au feed to Part III |
|---|---|---|
| Baseline | 38.4 % | 39.0 uM |
| Oxygen at 80 uM (item 41) | 60.9 % | 61.8 uM |
| `t_film` = 0.05 um (item 19) | 100 % | 101.5 uM |
| Enzyme carried into Stage 3 | 54.3 % | 55.1 uM |

Optimising Part I in isolation drives Part III further off its cliff. This is
the third genuinely coupled result in the project, after items 35 and 41.

### There are two separate ceilings, and the 30 uM one is the milder

**Ceiling 1, toxicity, at about 30 uM.** Soluble gold damages the cells. Above
roughly 30 uM the damage outruns repair and capture falls away. This is a
CONCENTRATION problem, so **dilution fixes it.**

**Ceiling 2, capacity, at 0.457 uM since 2026-08-19; 0.054 uM as written.**
The cells have a finite number of binding
sites: `q_max * X_max` = 0.0108 uM per g/L times 5.0 g/L = **0.054 uM of gold
per litre of liquor**. The leach delivers 39 uM. That is **722x over**, against
1.3x over on toxicity.

**Dilution does NOT fix ceiling 2, and this is the part that is easy to get
wrong.** Capacity is a TOTAL AMOUNT problem, not a concentration one. Diluting
39 umol of gold into 722 litres puts each litre inside the window, but it also
needs 5 g/L of cells in each of those 722 litres. The total cell mass required
is unchanged, because the total gold is unchanged. Dilution buys the toxicity
ceiling and buys nothing at all against the capacity ceiling.

**What each option actually does:**

| Option | Fixes toxicity | Fixes capacity | Cost |
|---|---|---|---|
| Dilute the liquor | yes | **no** | volume to process |
| More biomass or more cycles | no | yes | 722x is not reachable |
| Hit both Part III targets, item 26 | yes | **almost** | ceiling 0.054 -> 25.5 uM |
| Stop the leach early, item 21 | yes | yes | gold left on the board |

The third row is the interesting one. With `q_max` at its 0.1961 engineering
target and `X_max` raised to the published *E. coli* densities item 26 argues
for, the ceiling becomes 25.5 uM. The leach delivers 39. **Still 1.5x over,
after both stretch targets are met.**

The fourth row closes that last 1.5x for free. Stop when the liquor reaches
about 20 uM and everything fits, at the price of leaving gold undissolved.

**So this is not a bug with a fix. It is an optimisation across the joint.**
Leach recovery and capture efficiency pull against each other, and the two
parts have to be tuned together rather than each maximised alone. That is
exactly what items 35 and 41 also say, in different words.

Part I's author independently recommends running one day rather than three on
throughput grounds. That recommendation and this one agree.

**Item 21 is no longer academic.** It was open with nothing forcing it. It is
now the difference between 96 % and 4 % of the gold being captured.

---

## 36. Three vessels or one: the one-pot design is retired, the cost is not settled

Opened 2026-08-12. **Resolved in the code the same day: `src/` implements the
three-vessel process only, and the one-pot model is retired.** What is still
open is whether the wet lab can pay for three vessels. The comparison below is
kept because it is the evidence for the choice.

| | Simultaneous | Sequential |
|---|---|---|
| Vessels | 1 | 3 |
| Enzyme in the leach | yes, made continuously | no |
| Thiosulfate at leach start | 72 100 umol/L, from the broth | 94 359 umol/L, banked in Stage 2 |
| Gold at 24 h | 33.8 % | 35.1 % |
| Gold at 72 h | 36.5 % | 38.4 % |
| Thiosulfate lost to Cu(II) | 94.3 % | 98.2 % |
| Answers item 32 | no | plausibly, see below |

**The honest reading: separating the vessels does not fix the chemistry.** It
buys 1.9 percentage points of gold. Both runs die the same death, thiosulfate
annihilated by Cu(II), and the sequential run dies slightly harder because it
has more thiosulfate to lose.

**Retired on chemistry, not on yield. The real reason is item 32.** TetH forms inactive inclusion
bodies in *E. coli* and recovers activity only by refolding at pH 4 in vitro.
The simultaneous design needs TetH to fold and turn over on a living *E. coli*
surface at pH 7, which the literature says it does not do. The sequential
design harvests, extracts, purifies and refolds the enzyme before use, which is
exactly the published procedure. Part I's author cites the paper, reference
[19], Kanao 2010, in his sequential document.

That makes the sequential model the first version of Part I that could work at
all. It is adopted on that ground, not on its yield.

**What is still open:** whether three vessels is acceptable to the wet lab, and
at what cost. Stage 2 needs 9.1 litres of culture per litre of conversion
vessel, before any purification losses (item 40). That is the real price.

**What the audit found.** The sequential model was reproduced line for line in
Python before adoption. Fourteen of fourteen reported numbers matched to three
significant figures: areas, inventories, the broth stoichiometry, the enzyme
steady state, Stage 2 conversion, the gold rate peak and its oxidant split, the
Cu(II) maximum, and all four rows of the thiosulfate ledger. Three balances the
author does not test also close: sulfur atoms to one part in 100 000, copper to
0.00 umol/L, gold to 4e-13 umol.

His `'split'` stoichiometry is chemically identical to this repository's
`stoichiometry="balanced"`. Two authors fixed item 18 the same way without
consulting each other.

Reproduced by `tests/test_leach.py ::
test_sequential_reproduces_the_numbers_part_I_reports`.

---

## 37. The sequential write-up prints the lumped rates its own code does not use

Found 2026-08-12. Cosmetic in effect but dangerous in practice, so it is here
rather than in the cosmetic list.

Section 3.2 of the sequential document prints:

    v1A = 2 k_Cu,O2 A_Cu f_O2 f_S
    v1B = A_Cu f_S { 2 k_Cu,O2 f_O2 + 4 k_Cu,Cu f_Cu }
    v2  = R_Au

These are the old lumped forms, carried over unchanged from the simultaneous
document. They fold the stoichiometric coefficients 2 and 4 into the rate
itself, which is exactly the error item 18 records: one number cannot serve two
pathways that do not share coefficients.

**His code does not do this.** `bioleaching_model_sequential.m` computes

    v1A = k_Cu_O2 * A_Cu * fO2 * fS
    v1B = k_Cu_Cu * A_Cu * fS  * fCu

with no factor 2 or 4, and puts the coefficients on the thiosulfate and Cu(I)
terms where they belong. The code is right. The prose is stale. The sequential
document also never prints its own `dCu(I)/dt` or `dCu(II)/dt`, so a reader
falls back on the simultaneous document's, which are the lumped ones.

**Anyone implementing Part I from the sequential prose alone gets twice the
copper rate.**

Two further stale items in the same document:

- The pH panel of Figure 2 is presented as a result. `p.pH_on = false` in the
  defaults, so it is a flat line at 7.0 by construction. Switching the balance
  on gives a final pH of 7.94. Recorded in `params/leach.yaml :: pH_balance`.
- "Cu(II) is at its maximum of 829 umol/L precisely when leaching ceases."
  829 umol/L is the value at 72 h. Cu(II) rises monotonically to the last
  timestep and is still rising. At 27 h, when leaching stops, it is lower.

The simultaneous file carries two more, both in code paths that are off by
default and neither reached by any figure:

- Its pH block divides a proton rate by `(1 + beta)` with `beta` in umol/L,
  which is dimensionally inconsistent. Its sequential file tracks alkalinity
  instead, which is correct, and that is the form implemented here.
- Its `O2_mode = 'mtc'` branch charges oxygen consumption to the whole copper
  rate `R_Cu` rather than to the oxygen route alone. Fix before use; item 41
  step 3 needs this branch.

**Nothing in the source documents was changed.** Only their author corrects
them.

---

## 40. Nothing accounts for purification losses or enzyme decay in the vessel

Opened 2026-08-12. Two missing terms, both in the same direction: they make
Stage 1 and Stage 2 look cheaper than they are.

**Stage 1 has no purification yield.** The model says 9.1 litres of culture
charge one litre of conversion vessel. That assumes every TetH molecule in the
culture survives harvest, extraction and purification. Real recovery for a
purified protein is perhaps 0.3 to 0.6, so the honest figure is 15 to 30 litres
of culture per litre. Held as
`params/leach.yaml :: sequential.purification_yield`, value null.

**Stage 2 has no enzyme decay.** The concentration is held constant for 4320
minutes. `k_deg` was dropped along with the cells, correctly, because it is a
proteolysis rate and there are no proteases. But proteolysis is not the only
way an enzyme is lost over three days at 30 C. Held as
`sequential.enzyme_half_life_stage2`, value null.

Both are null rather than guessed, so a run that needs them fails loudly. That
is AGENTS.md rule 4.

**Who decides:** the wet lab, from its own purification.

**Why it matters:** culture volume is the real cost of the sequential design,
and it is the quantity expression engineering acts on. Understating it by
three-fold understates the case for a stronger promoter by three-fold.

---

## 35. The chain is squeezed: capture wants low gold, reduction wants high gold

Found 2026-08-11 while recomputing item 27. **Neither document could have seen
this alone.** It is the second genuinely coupled result in the project, after
item 21's stopping rule.

### The two constraints point in opposite directions

| Stage | Wants | Why |
|---|---|---|
| **Capture** | **low** gold, ≤ 0.8 µM | above `q_max·X_max` the sites are full and the surplus washes through |
| **Reduction** | **high** gold, ≥ 3 µM | Finke-Watzky is autocatalytic; below ~1 µM nucleation never gets going |

Between them the gold only ever goes **down**: capture keeps a fraction of the
feed, elution releases a fraction of that.

Gold arriving at reduction, at the two operating points:

| Regime | Feed | × `eta_capture` | × `eta_elute` | **At reduction** | `eta_reduce` |
|---|---|---|---|---|---|
| Adopted | 0.4 µM | 0.090 | 0.87 | **0.031 µM** | ~0.002 |
| Target | 0.4 µM | 0.979 | 0.87 | **0.34 µM** | ~0.05 |

**Both sit below the cliff**, and the engineering target does not fix it. Even
a perfect capture stage delivers only 0.34 µM into a step that needs 3 µM.

### The fix is a volume ratio, and it is not in any model

Elute into a **smaller volume than you captured in**. Concentration is the only
free variable that raises gold without raising the feed.

| Concentration factor V1:V2 | Gold at reduction, target regime | `eta_reduce` |
|---|---|---|
| 1× | 0.34 µM | ~0.05 |
| 10× | 3.4 µM | ~0.99 |
| 30× | 10 µM | 1.00 |

**About 10× is enough.** That is an ordinary bench operation: capture in 1 L,
elute in 100 mL.

Part III §1 lists the V1→V2 transfer as *not modelled* and *assumed lossless*.
Item 29 row 13 records it as unreconciled. **It is not merely unmodelled; its
volume ratio is now one of the most consequential numbers in the chain, and
nobody has chosen it.**

### Why this changes the sensitivity story

It explains why `k_nuc` is the top PRCC term at the adopted `q_max`, at +0.96.
`k_nuc` matters enormously *only because the model is operating below the
concentration where nucleation works*. Fix the volume ratio and `k_nuc` should
drop back down the ranking. **A sensitivity result can be an artefact of a bad
operating point rather than a property of the chemistry**, which is the same
lesson item 27 taught about `q_max` = 4.4.

### Decision needed

1. **Set the V1:V2 volume ratio**, and model the transfer rather than assuming
   it lossless. Target ≥ 3 µM at the reduction step. About 10× at the
   engineering target, about 100× as built today.
2. Recheck `A_tox` afterwards. Concentrating gold 10× before reduction is fine
   for a cell-free lysate, but if any live cells are carried across, 3–10 µM is
   approaching the range item 22 flags as untrustworthy.
3. Re-run item 27's ensemble once the ratio is set, to confirm `k_nuc` falls
   back.

---

## 32. 🔴 BLOCKING — TetH cannot fold into an active form in *E. coli* at neutral pH

Found 2026-08-11 by the source audit, reading the full texts of papers this
repository already cited. **This is published, replicated, and mechanistically
explained. It is not a risk estimate.**

Item 30 flagged inclusion-body formation as "a live risk". It is not a risk.
It is the reported result, four times, from the group that discovered the
enzyme.

### The evidence

| Source | What it says |
|---|---|
| [S27](SOURCES.md) Kanao 2010 | "heterologous expression of *Af-tth* in *E. coli* resulted in the formation of **inclusion bodies of the protein in an inactive form**" |
| [S27](SOURCES.md) | "*Af*-Tth **required exposure to an acidic environment during protein folding** for activation" — recovered only after 6 M guanidine, then pH 4.0, 14 h at 4 °C |
| [S28](SOURCES.md) Kanao 2013 | independent replication: "expressed as inclusion bodies in recombinant *E. coli* ... activated by refolding under acidic conditions" |
| [S1](SOURCES.md) Kanao 2023 | "recombinant *Af*-Tth was synthesized in the **inclusion bodies of *E. coli*** and acid-refolding treatment was necessary to recover the activity" |
| [S3](SOURCES.md) Kanao 2024 review | "owing to differential growth conditions, **particularly pH**, it is frequently impossible to obtain a recombinant protein in its functional form" |

### Why, mechanistically

[S3](SOURCES.md) Table 1: **every** TTH ever purified has an acidic optimum.

| Organism | Subunit | Optimum pH |
|---|---|---|
| *A. ferrooxidans* ATCC 23270, **our enzyme** | 50 × 2 kDa | **3.0** |
| *A. caldus* | 52 × 2 | 4.0 |
| *A. thiooxidans* Funis 2-1 | 50 | 3.5 |
| *Acidianus ambivalens* | 54 × 2 | 1.0 |

And the catalysis itself needs acid: Asp325 "acts as **an acid** for the
tetrathionate hydrolysis reaction", protonating a sulfur atom so that water can
attack it. A D325N variant has **no activity at all**. At pH 7 that aspartate
is deprotonated.

### What this does to the model

Part I's operating route, set on 2026-08-11, is *E. coli* surface-displaying
TetH, with `Vmax = k_cat × [TetH]` = 14.3 µmol L⁻¹ min⁻¹ at 4 g/L.

**Three things must all be true for that number to mean anything, and the
literature says none of them is:**

1. TetH folds in *E. coli*. It does not; it aggregates into inclusion bodies.
2. It folds where the display scaffold puts it, at pH ~7. It needs pH ~4.
3. It then turns over at the reactor pH. Its optimum is pH 3.0.

`f` = 0.5 is not conservative. **The published expectation for active fraction
in *E. coli* at neutral pH is closer to zero.** `f` scales `Vmax` linearly, so
`Vmax` is not a lower bound. It may be an overestimate without limit.

### This also re-opens item 23, and the 2026-08-11 narrowing of it was wrong

Item 23 was narrowed that day from a 7 pH-unit conflict to about 2.5, on the
ground that the acidophile was gone. **That was wrong.** The organism left; its
enzyme's pH requirement did not.

| Needs | pH |
|---|---|
| TetH folding | ~4 |
| TetH catalysis | **3.0 optimum** |
| *E. coli* growth and display | ~7 |
| Thiosulfate gold leach, every published system | **9.3–10.5** |

That is a **three-way conflict spanning about 6.5 pH units**, and it is worse
than the original, because the acidic requirement is no longer an organism
preference that could be argued with. It is an enzyme mechanism with a crystal
structure behind it.

### Options, none free

1. **Buy the thiosulfate.** Delete Part I's enzyme block. The leach chemistry
   stays, the pH conflict drops to two-way, and Part II's cascade supplies only
   GolB. Simplest, and it removes an entire iGEM story.
2. **Two vessels with an acid stage.** Produce TetH in *E. coli*, refold it
   outside the cell at pH 4, and run a cell-free acidic tetrathionate stage.
   That is enzyme production plus in-vitro refolding, not a living bioreactor.
3. **Keep the acidophile for Part I only.** Reverts the one-organism decision
   for the leach vessel. Eccleston's numbers become valid again and item 30's
   derivation returns.
4. **Engineer folding.** Periplasmic chaperones, an acid-tolerant variant,
   directed evolution for neutral-pH activity. A research project, not a
   parameter change.
5. **A different tetrathionate route.** [S3](SOURCES.md) notes TTH-independent
   tetrathionate metabolism was recently reported in a new isolate. Unproven
   and unquantified.

**Decision needed, and it is the team's, before any Part I result is quoted.**
Treat `params/leach.yaml :: enzyme_capacity` as unvalidated until it is
answered.

Also unmodelled and now visible: TetH's optimum temperature is **60 °C**
([S3](SOURCES.md) Table 1), against *E. coli* at 37 °C.

---

## 33. `cells_per_g` is a slow-growth value applied to a fast-growth culture

Found 2026-08-11 by the source audit.

`params/conversions.yaml` carries `cells_per_g_dry_weight` = 3.57×10¹², from an
*E. coli* single-cell dry mass of 0.28 pg. **It converts every per-cell number
in the chain into a per-gram one**: `q_max`, `Vmax` and the capacity ceiling all
pass through it.

[S30](SOURCES.md) reports that dry mass per cell varies **more than five-fold
with growth rate**, because faster cells are bigger:

| Doubling time | Dry mass per cell |
|---|---|
| 100 min | 148 fg |
| **34.7 min, our `μ` = 1.2 h⁻¹** | **423 fg, interpolated** |
| 24 min | 865 fg |

**0.28 pg = 280 fg sits near the slow end.** The model runs at a 34.7 min
doubling time, where cells are about 1.5× heavier, so there are 1.51× fewer per
gram.

| Quantity | At 3.57e12 | At 2.36e12 |
|---|---|---|
| `q_max` | 0.0163 | **0.0108** |
| `Vmax` at 4 g/L | 14.3 | **9.49** |
| Capacity ceiling at `X_max` = 5 g/L | 0.0815 µM | **0.0539 µM** |

Both move in the unfavourable direction. Item 2 already noted this constant
"carries a factor of about 2.5 across growth conditions". What is new is that
**the model uses it at the wrong end of that range for its own stated growth
rate.**

### ✅ APPLIED 2026-08-11 — interpolated at the operating growth rate

`cells_per_g` = **2.36e12**, from 423 fg per cell at our 34.7 min doubling
time, log-linear in growth rate between [S30](SOURCES.md)'s two anchor points.
3.57e12 is kept as `superseded` in `params/conversions.yaml`.

Everything downstream moved:

| | Was | Now |
|---|---|---|
| `q_max` | 0.0163 | **0.0108** |
| `q_max` engineering target | 0.2964 | **0.1961** |
| Capacity ceiling at 5 g/L | 0.0815 µM | **0.0539 µM** |
| `Vmax` at 4 g/L | 14.3 | **9.49** |
| Operating window | 1–2 µM | **0.4–0.8 µM** |
| *E. coli* penalty per gram | 40x | **60x** |
| `K_Au` swing at low feed | 2.6x | **3.5x** |

Biomass was **not** raised to hold `Vmax` at 14.3. It stays at 4.0 g/L, and
6.0 g/L would reach 14.2 if that is wanted.

**Still open, and better:** this is an interpolation from a literature curve,
not a measurement. One OD600 curve plus one dry-weight measurement on your own
culture removes the constant entirely. That is the recommended fix and it is a
half-day of wet-lab work.

---

## 34. `k_cat` has two published values 8 to 10× apart

Found 2026-08-11 by the source audit. Both figures come from the same group, on
the same enzyme.

| Source | Specific activity | Preparation |
|---|---|---|
| [S27](SOURCES.md) Kanao 2010 | **21.0 ± 9.4 U mg⁻¹** | refolded from *E. coli* inclusion bodies |
| [S1](SOURCES.md) Kanao 2023 | 2.5 ± 0.18 U mg⁻¹ | acid-refolded from *E. coli* |
| [S1](SOURCES.md) Kanao 2023 | 2.2 ± 0.37 U mg⁻¹ | purified from recombinant *A. ferrooxidans* |

`params/leach.yaml` uses 2.2, giving `k_cat` = 220 min⁻¹. The 2010 figure gives
**2,100 min⁻¹**, and `Vmax` scales linearly with it.

The 2024 review ([S3](SOURCES.md)) states the 2.2 and 2.5 equivalence and
**does not mention the 21.0 figure at all**, so the discrepancy is unexplained
rather than resolved. The 2010 value also carries a ±45% error bar, consistent
with variable refolding yield.

**This is a separate uncertainty from the 220-versus-110 dimer question**,
which is a factor of 2 and cancels in `Vmax`. This one is a factor of 10 and
does not cancel.

**Decision needed:** keep 220 min⁻¹ as the conservative choice, which is what
the file does, and record that `Vmax` may be 10× higher. Or assay your own
preparation. Item 32 may make this moot.

---

## 19. Gold leaching speed is inversely proportional to plating thickness

Part I §4 sets the exposed gold area from the plating geometry:

```
A_Au = m_Au / (rho_Au * t_film)
```

`t_film` is given as the range **0.05–1 ×10⁻⁶ m**, status "board spec". That is
a 20-fold range, and because `t_film` sits in the denominator, the leaching
rate inherits all 20× of it.

Measured over a 600-minute Model B run, same gold mass throughout:

| `t_film` | Exposed area | Gold in solution at 600 min |
|---|---|---|
| 0.05 µm | 0.1036 m² | 384.5 µM |
| 0.20 µm | 0.0259 m² | 96.3 µM |
| 0.50 µm | 0.0104 m² | 38.5 µM |
| 1.00 µm | 0.0052 m² | 19.3 µM |

Exactly 20× between the ends, as the algebra requires.

**Updated 2026-08-12, and it got worse.** `t_film` = 0.5 µm is now the working
value in `params/leach.yaml`, taken from Part I's models. It is a midpoint, not
a board specification, and the item stays open.

In the full sequential run the 20× in the rate does not become 20× in the
recovery, because the leachant runs out first. It becomes this:

| `t_film` | Gold recovered at 72 h | Au feed to Part III |
|---|---|---|
| 0.05 µm | **100 %** | 101.5 µM |
| 0.5 µm | 38.4 % | 39.0 µM |
| 1.0 µm | **19.2 %** | 19.5 µM |

A factor of 5.2 in the headline result, from a number nobody has looked up.
That makes `t_film` a joint largest lever with `k_par`.

Note the right-hand column against item 39. At 0.05 µm the leach recovers all
the gold and hands Part III a feed 3.4× above the concentration at which its
capture collapses.

### Team decision, 2026-08-12: assume 0.5 µm and move on

The earlier version of this item said to ask the board supplier. **The team
ruled that out, correctly: the feed is mixed electronic waste, not boards from
a named supplier, so there is no specification to obtain.** `t_film` = 0.5 µm
is now a stated assumption in `params/leach.yaml` with `status:
team_assumption`, and work continues on it.

**The item stays open, because assuming a number does not remove its
uncertainty.** Mixed waste genuinely spans the whole range. Immersion-gold
surface finishes are sub-tenth-micron and cover most of a board's area; hard
gold on edge connectors is around a micron and covers very little of it. The
model needs the area-weighted mean over the real feed, and 0.5 µm is a
midpoint, not a measurement of that mean.

The direction of the error is worth noting. If the feed is dominated by thin
immersion-gold finishes, the true value sits below 0.5 µm, and the model is
**understating** recovery, possibly by a lot. That is the pleasant direction,
and it is also the direction that makes item 39 worse.

**What would settle it, and neither needs a supplier:** weigh the gold and
measure the plated area on a sample of the actual feed, or leach a known mass
of feed to completion and fit `t_film` to the observed rate. Either turns an
assumption into a measurement using material the team already has.

**Until then:** every recovery figure in this repository is quoted at
`t_film` = 0.5 µm, and the sentence saying so travels with the number.

**This is physics, not an error.** The same mass of gold spread thinner covers
more area, and leaching happens on area. Thin plating leaches faster. The
total gold recoverable does not change; only the time to get it does.

**Why it still needs a decision.** `t_film` is the single largest lever on
leaching rate in Part I, larger than any rate constant currently in the model,
and it is set by which boards you feed in, not by anything you control in the
reactor. It is currently `null` in `params/leach.yaml`.

**Decision needed:** measure or specify the plating thickness of your actual
feedstock. One number from the board supplier, or one cross-section
measurement. Until then, every leaching timescale in this model is uncertain
by 20×.

Found while walking through Part I §4 on 2026-08-10.

---

## 23. The leach chemistry is published only at pH 9–10.5

Part I §1's contents list ends with "pH change (to be built)". It was never
built. There is no pH variable anywhere in the three documents.

### ⚠️ The 2026-08-11 narrowing below was WRONG. See item 32.

Narrowing this item to 2.5 pH units assumed that removing the acidophile
removed the acidic requirement. **It did not.** TetH's catalytic optimum is
pH 3.0 and its folding needs pH ~4, both published with a crystal structure
behind them. The conflict is **three-way and about 6.5 pH units**: TetH at 3,
*E. coli* at 7, the leach at 9.3-10.5. Item 32 has the evidence.

The superseded narrowing is left standing below.

### Narrowed 2026-08-11 by item 30, SUPERSEDED by item 32

The acidophile is gone. *E. coli* runs the whole chain and wants roughly
neutral, not pH 1.8.

| | Before | After |
|---|---|---|
| Organism wants | pH 1.8, *A. ferrooxidans* | pH ~7, *E. coli* |
| Leach chemistry published at | pH 9.3–10.5 | unchanged |
| Gap | about 7 pH units | **about 2.5 pH units** |

### What survives, and it is still real

**Every published thiosulfate gold leach found is alkaline.**
[S16](SOURCES.md) optimises over pH 9.3–10.5 and reaches 89.3% gold in 6 h;
[S17](SOURCES.md) is a second, independent non-ammoniacal system, also
alkaline. Thiol capture of the complex is documented at pH 9.0–10.5
([S12](SOURCES.md), [S13](SOURCES.md)).

**Part I's one absolute gold rate constant is an alkaline measurement.**
`k_Au,O2` = 11 µmol m⁻² min⁻¹ is sourced to Zhang & Nicol 2003, whose title
states "Part I: Alkaline solutions". References [10] and [11] are likewise
reviews of alkaline systems.

*E. coli* does not grow at pH 9.5 either, so a single vessel still has to
compromise. Thiosulfate is also not stable in acid, which is why the industry
runs these leaches alkaline.

### And the chain still swings after that

The liquid must reach ~7 for the *E. coli*, then 1.4–1.8 for elution, then 7.4
for reduction. Part III §1 lists conditioning as not modelled and assumed
lossless. [S14](SOURCES.md) reports that `Au(S₂O₃)₂³⁻` is dominant only under
acidic conditions, so the species arriving at capture after neutralisation may
not be the one Part III assumes.

**Decision needed:** state the intended leach pH. One vessel at a compromise
pH, or two vessels with a transfer. If the leach is not alkaline, `k_Au,O2`
needs a source measured at the chosen pH.

---

## 27. Every sensitivity ranking in Part III §8 was computed at `q_max` = 4.4

Part III §8 reports PRCC values that order the whole chain:

```
k2 +0.785, q_max +0.783, Xmax +0.370, k1 +0.366, phi -0.321,
eta_spin +0.313, k_red +0.214
Insensitive (<0.05): K_D, K_i, k_on, k_max, w
```

Those were produced by sampling around `q_max` = 4.4, where capture was
comfortably above the capacity ceiling and far above `K_D`. **Adopting
the adopted `q_max` moves the operating point into a different regime**, and at
least one ranking is now known to be wrong: `K_D`, listed as insensitive,
swings capture by 2.6× at the feeds the new capacity forces. See item 1.

**What is likely to move, and in which direction:**

| Parameter | Was | Expected now | Why |
|---|---|---|---|
| `q_max` | +0.783 | **higher** | it is now the binding constraint everywhere |
| `Xmax` | +0.370 | **higher** | capacity is `q_max·X_max`, both halves now bind |
| `K_D` | insensitive | **2.6× at low feed** | feed is now comparable to `K_D` |
| `k2`, `k1` | +0.785, +0.366 | **lower in relative terms** | reduction cannot matter if capture delivers almost nothing |
| `A_tox`, `k_dam` | drove the >30 µM analysis | **irrelevant** | capacity limits capture long before toxicity does |

**Decision needed:** re-run the Latin hypercube and PRCC at the adopted
`q_max`, and again at the engineering target 0.1961, and publish both. A
single ranking cannot describe both regimes.

Until then, no sensitivity claim from Part III §8 should be quoted.

Found while walking through Step 8 on 2026-08-10.

### ✅ RECOMPUTED AND CLOSED 2026-08-11

Latin hypercube, n = 800 per regime, PRCC on `eta_total`.
Code: `src/sensitivity.py`. Ranges are the sweeps in
`params/recovery_chain.yaml`; `X_max`, `k_nuc` and `k_grow` had no published
ranges and were given 1–10 g/L and one order of magnitude either side.

**Validation.** Re-run in Part III's own regime the ensemble gives an
`eta_total` median of **0.142** against Part III's reported **0.105**, and a
90% CI of [0.0001, 0.659] against [0.0, 0.494]. Close, given three invented
ranges. Good enough to trust the rankings, not the third decimal.

### The three rankings

| Rank | Retired, `q_max` 0.33–4.4 | **Adopted, 0.0108** | Target, 0.1961 |
|---|---|---|---|
| 1 | `q_max` +0.83 | **`k_nuc` +0.96** | `k_grow` +0.89 |
| 2 | `X_max` +0.73 | `X_max` +0.87 | `k_nuc` +0.76 |
| 3 | `k_grow` +0.71 | `q_max` +0.80 | `X_max` +0.39 |
| 4 | `eta_spin` +0.33 | `k_grow` +0.61 | `q_max` +0.26 |
| 5 | `phi` −0.22 | `eta_spin` +0.49 | `eta_spin` +0.24 |
| 6 | `k_nuc` +0.16 | **`Au_feed` −0.44** | `phi` −0.14 |
| 7 | `Au_feed` −0.12 | `phi` −0.22 | **`K_Au` −0.11** |
| — | `K_Au` +0.02, insensitive | **`K_Au` −0.14** | `Au_feed` +0.11 |

**Every prediction made when this item was opened was directionally right
except one.**

| Parameter | Predicted | Found |
|---|---|---|
| `q_max` | higher | ✅ +0.78 → +0.80, and it stays top three |
| `X_max` | higher | ✅ +0.37 → +0.87, the largest single move |
| `K_Au` | stops being insensitive | ✅ +0.02 → −0.14 |
| `k_grow`, `k_nuc` | lower in relative terms | ❌ **wrong. `k_nuc` went from 6th to 1st** |

### The finding that was not predicted: reduction now dominates

Median `eta_reduce` across the ensemble:

| Regime | median `eta_capture` | median `eta_reduce` |
|---|---|---|
| Retired | 0.376 | **0.9998** |
| Adopted | 0.090 | **0.0017** |
| Target | 0.979 | **0.0071** |

**The reduction step has all but stopped**, and it is not because capture
starves it of gold in absolute terms. It is a threshold. Finke-Watzky growth is
autocatalytic, `v = (k_nuc + k_grow·B)·A`: with little gold, `k_nuc·A` is tiny,
`B` never builds, and the induction period never ends.

Gold presented to reduction, 24 h, all other parameters at their central values:

| `A₀` at reduction | `eta_reduce` | time to 50% |
|---|---|---|
| 0.05 µM | 0.001 | **never, inside 200 h** |
| 0.5 µM | — | 76 h |
| 1 µM | 0.029 | — |
| **3 µM** | **0.993** | — |
| 5 µM | — | 9.9 h |
| 50 µM | 1.000 | 1.2 h |

**The cliff is between 1 and 3 µM.** That is why `k_nuc`, the parameter that
starts the first particles, is now the single strongest term in the chain.

This is the subject of new item 35. It is a design problem, not a parameter
problem.

### What to quote from now on

Quote the **adopted** column for the state of the build, and the **target**
column for where the engineering is heading. Do not quote Part III §8. A single
ranking cannot describe both regimes, which is what this item said when it was
opened; that is now demonstrated rather than asserted.


---

> **Working selection, 2026-09-18.** The reference model now uses one
> internally consistent S60 condition: 0.1 M thiourea in 0.1 M sulfuric acid,
> 50 °C and 1 g sorbent/L. S60 supplies both `phi = 0.03` and the observations
> used to derive the first-order lower bound `k_elute = 0.22 h^-1`. The former
> S59/S60 hybrid is retained in parameter history. This does not close the
> issue: S60 used a porphyrin polymer, so one GolB-comb time course must still
> replace both transferred values.

## 28. The eluent is not finalised, and `phi` swings `eta_total` by 5×

The team confirms on 2026-08-10 that the elution reagent has not been chosen.
Part III §3 already flagged this: *"the project architecture assumed an acid
wash. If the wet lab plans acid-only, elution may recover far less than
(1−φ) predicts and the model would not show it"*, because `k_max` is fitted
and would silently absorb a failing eluent.

### What the choice is worth

`eta_total` at the engineering display target with >200 nm particles:

| `φ` | Ceiling `1−φ` | `eta_total` | Corresponds to |
|---|---|---|---|
| 0.02 | 98% | **76.0%** | best reported, with additives |
| **0.043** | **96%** | **~73%** | **0.4 M thiourea + 0.8 M HCl** [S24](SOURCES.md) |
| 0.13 | 87% | 67.5% | value in the model, 1 M thiourea |
| 0.30 | 70% | 54.3% | high end of the model's own sweep |
| 0.50 | 50% | 38.8% | a poor eluent |
| 0.80 | 20% | **15.5%** | acid-only, if it barely works |

**A 5× swing on the final number**, decided by a reagent choice that has not
been made.

### Update 2026-08-24: both constants now have anchors, neither has a measurement

`phi` **is traced to its origin.** The line it entered on, *"87% desorption,
protein biosorbent + 1 M thiourea"*, is Han et al. (2019), *Biochemical
Engineering Journal* **152**, 107388, [S59](SOURCES.md): 1 M thiourea was the
best of several agents tested on a gold-binding protein immobilised on
amino-grafted silica. It is the closest analogue available, because the sorbent
is a protein, and it is the most pessimistic of the sourced options.
The 87% is in the paywalled body, not the abstract, so it is marked ⚠️.

`k_elute` **has one anchor, not three.** No desorption time course exists for a
sorbent like ours. [S60](SOURCES.md) reports a ceiling of 97% and a separate
point above 90% at 12 h, which is 0.928 of the ceiling and gives
`k_elute` >= **1.1 h⁻¹**. [S24](SOURCES.md) and [S61](SOURCES.md) report
plateaux, the ceiling already reached at 80 and 60 min, so they bound the
constant without fixing it. The 2.0 in use is within a factor of two of the
only derived value.

**A first version of this update was wrong and is withdrawn.** It read all
three endpoints as 95% of the ceiling and quoted 0.75, 14.3 and 19 h⁻¹. Two
faults: [S24]'s 95.7% is already used as the CEILING behind `phi` = 0.043, so
reading it again as a share of the ceiling counts `phi` twice; and the 95%
convention was invented, since 99% moves the same numbers about fourfold.
[S62](SOURCES.md) adds the general limit: a PSO rate constant depends on the
concentrations it was measured at and does not transfer between systems.

**This item stays open.** Anchors are not a measurement on GolB cells, and the
reagent decision is still unmade.

### The best documented option

[S24](SOURCES.md) tested several eluents and found **0.4 mol/L thiourea plus
0.8 mol/L HCl** gave **95.7 ± 0.3% desorption in 80 minutes**. Note that it
beats 1 M thiourea while using *less* thiourea, because the acid is part of
the eluent rather than a separate wash. [S25](SOURCES.md) independently
reports ~100% extraction with thiourea under strongly acidic conditions.

**The evidence says thiourea and acid together, not either alone.** No source
found in this search supports acid-only elution of gold from a thiol.

### Speed is a separate, cheaper decision

`k_max = k·[TU]^n`, so concentration buys time, not ceiling:

⚠️ **The table below assumes `n` = 1 and `n` has never been measured.** It is
`null` in `params/recovery_chain.yaml`. Every row except the 1 M row is
therefore an illustration of what a linear response would look like, not a
prediction. Added 2026-08-15; see also item 47, which questions the rate law
the table is built on.

| [Thiourea] | `k_max` | 1 h | 3 h | 6 h |
|---|---|---|---|---|
| 0.1 M | 0.2 /h | 15.8% | 39.3% | 60.8% |
| 0.5 M | 1.0 /h | 55.0% | 82.7% | 86.8% |
| **1 M** | **2.0 /h** | 75.2% | **86.8%** | 87.0% |
| 2 M | 4.0 /h | 85.4% | 87.0% | 87.0% |

Above about 1 M there is nothing left to buy. Below 0.5 M the wash does not
finish in a shift.

### Two warnings before adopting thiourea

1. **Thiourea decomposes in the presence of iron sulfides.**
   [S25](SOURCES.md) required a bio-oxidation step first to remove them. Our
   leachate is a sulfur system carrying copper. Thiourea stability in it is
   untested.
2. **The gold changes charge across this step.** It enters capture as the
   anion `Au(S₂O₃)₂³⁻` and leaves elution as the cation
   `Au(CS(NH₂)₂)₂⁺` [S25](SOURCES.md). Anything downstream that assumes a
   charge, including the reduction step and any ion-exchange polishing, needs
   to know that.

**Decision needed, and it is a wet-lab decision with a 5× consequence.**
Choose the eluent. If it is thiourea plus acid, `φ` should be set to about
0.05 rather than 0.13, and `eta_total` rises. If it is acid-only, the model
has no support for it and `φ` is unknown.

**Run this with item 47.** One time course — 0.25, 0.5, 1, 2, 4, 6 h — gives
`φ` from the endpoint and the rate law from the shape. Two open items, six
samples.

Found while walking through Step 9 on 2026-08-10.

---

## 22. `K_Au` and `A_tox` are apparent constants tied to untracked conditions

> **Update 2026-09-18.** The closest published apparent GolB value is now
> adopted as a proxy: `K_Au = 0.7 µM` from the fitted wild-type GolSeN
> saturation curve [S78](SOURCES.md). It replaces the unsourced `0.1 µM`
> proxy, but it does not close this issue because the assay used soluble
> ECFP-GolB-Venus and HAuCl4 in MOPS, not displayed GolB in Au(I)-thiosulfate
> leachate. No matched GolB copper constant was found. For design only, the
> model uses the conservative matched GolS ratio `alpha = 52` [S79](SOURCES.md),
> which gives `K_Cu = 36.4 µM` when combined with `K_Au = 0.7 µM`.

Researched 2026-08-10 in answer to "does GolB bind gold uniquely, with no
competition?"

Part III §2 defines `A` as soluble gold supplied by `Au_feed`, which is
`Au(S₂O₃)₂³⁻`. **The complex is the tracked species, and the ligand exchange
onto the protein thiol is already inside `k_on` and `K_Au`.** That is the right
modelling choice, and it creates the problem below.

### `K_Au` is apparent, not intrinsic

Capture is an exchange, and thiosulfate is a **product** of it:

```
Au(S2O3)2 3-  +  GolB(SH)2   <->   GolB-Au  +  2 S2O3 2-
```

So the equilibrium position depends on how much free thiosulfate is already
present, and `K_Au` is valid only at the thiosulfate concentration it was
determined at. [S11](SOURCES.md) confirms the same mechanism on
thiol-functionalised silica and lists thiosulfate concentration among the
variables that change adsorption.

Free thiosulfate in raw leachate is about 104,000–109,000 µM. After
conditioning it is unspecified, because conditioning is unmodelled. **One
`K_Au` cannot cover both ends of that range.**

`K_Au` = 0.1 µM is recorded as "bounded by CXXC proxies". Those proxies measure
a thiol binding **free Au(I)**. The model uses `K_Au` for a thiol **displacing
thiosulfate from a complex**. Different equilibria. Part III §0 already records
`K_Au` among the parameters that were assumed, then sourced, then found wrong
by ≥12 orders. Same failure mode, not yet closed.

### `A_tox` has the same problem and is not insensitive

`A_tox` = 250 µM, status "LB MIC". MIC studies use soluble gold salts,
typically chloroaurate. The model applies that number to the thiosulfate
complex. **Different species, different bioavailability**; gold enters cells by
non-specific intake ([S7](SOURCES.md)). Part III §2.1 shows the `A_tox`
disagreement costing 63–96% of capture above a 30 µM feed.

### Selectivity, answered precisely

Most published work on "gold-specific" *Salmonella* proteins concerns **GolS**,
the regulator, not **GolB**, the binding protein.

| Claim | Evidence | Verdict |
|---|---|---|
| GolS prefers Au over Ag and Cu | [S6](SOURCES.md)–[S8](SOURCES.md) | strong, experimental |
| GolS binds *only* Au | — | **false**; Ag and Cu still activate it |
| GolB prefers Au over other cations | [S9](SOURCES.md) | **weak**; computational, hedged |
| GolB never binds copper | — | **contradicted**; it also sequesters cytoplasmic copper |
| A measured competitive constant for GolB vs Cu(I) or Ag(I) | — | **none found** |

**Two unmodelled competitors for the same sites.** Copper, arriving as
`Cu(S₂O₃)₂³⁻` and chemically analogous to the gold complex, which Part I now
supplies directly; and silver, the closest analogue of Au(I), present in
printed circuit boards and mentioned in none of the three documents. The
direction of the error is known even though its size is not: a competitor can
only reduce capture, so `eta_capture` is an upper bound.

### One favourable finding

[S10](SOURCES.md) measures the Au–S bond in GolB at **165 pN**, about six times
weaker than Au–S on a gold surface, with an unusually long bond. Good for
elution, a warning for washing. Neither Part II nor Part III uses this number.

**Decision needed.** State the free thiosulfate concentration that `K_Au`
applies at, and say whether the leachate is conditioned before capture.
Part III §1 lists conditioning as unmodelled and assumed lossless. This item
says conditioning may set `K_Au` itself.

---

## 26. The engineering target for `q_max`, and the operating window it implies

**Capture interpretation superseded, 2026-09-07, item 91.** The expression-derived
number bounds single-site occupancy, not all whole-cell gold accumulation.
S76 supplies experimental whole-cell evidence that the earlier search missed.
Original arithmetic remains below as a record.

### The target

```
f x P_s_max  =  0.5 x 1e5  =  50,000 active sites per cell
50,000 x 3.57e12 cells/g / 6.022e23 x 1e6  =  0.2964 uM/(g/L)
```

Every one of Part II's surface anchors occupied. **A design anchor, not a
physical ceiling**: [S29](SOURCES.md) says autodisplay reaches "more than" 1e5
molecules per cell, so 1e5 is a demonstrated floor. Stored as `V1_capture.q_max.engineering_target` and pinned by
`test_engineering_target_is_the_physical_anchor_ceiling`.

| | `q_max` | Capacity at `X_max` = 5 g/L |
|---|---|---|
| Adopted, as built | 0.0108 | 0.0539 µM |
| **Engineering target** | **0.1961** | **0.980 µM** |
| Retired Part III value | 4.4 | 22 µM |

*Corrected 2026-08-11 by item 33; previously 0.0163 and 0.2964.*

The gap is **18x**, and it is real: 2,749 of 50,000 possible sites, 5.5%
occupancy.

### The four levers that reach it

Each has normalised sensitivity +1.0, so the gain is the product of what you
achieve on each.

| Lever | Symbol | Now | Status |
|---|---|---|---|
| Promoter strength | `α` | 0.5 | sourced, generic *E. coli* |
| Plasmid copy number | `N` | 20 | medium-copy backbone |
| RBS strength | `β` | 4.0 | sourced, generic *E. coli* |
| Folded and accessible fraction | `f` | 0.5 | **fitted, not measured** |

`k_sec` is **not** a useful lever: sensitivity +0.2, because it appears in both
numerator and denominator. Growth rate `μ` is the strongest single term at
−1.05, so slower-growing cells carry more sites each.

### The second lever: biomass

Part III's `X_max` = 5 g/L is **26x below** what is routinely published for
*E. coli*: 20.7 g/L in shake flasks ([S18](SOURCES.md)), 128–148 g/L in
carbon-limited fed-batch ([S19](SOURCES.md)), 190 g/L as the field record
([S23](SOURCES.md)).

`eta_total` at a 10 µM feed:

| `X_max` | at `q_max` 0.0163 | at 0.2964 | |
|---|---|---|---|
| 5 g/L | 0.33% | 6.00% | Part III's assumption |
| 20.7 g/L | 1.37% | 24.85% | shake flask |
| 128 g/L | 8.45% | **32.36%** | fed-batch |
| 190 g/L | 12.54% | **32.36%** | field record |
| 330 g/L | 21.78% | 32.36% | solid pellet, impossible |

**Read the left column.** Even at a physically impossible density, today's
display density never reaches 22%. **Biomass cannot substitute for display
density.** To restore 32.4% at a 10 µM feed the current `q_max` would need
490 g/L, which is 1.5x the mass of a solid block of cells with no liquid
between them. There is nowhere to put them.

**Read the right column.** At the engineering target, 27 g/L restores 32.4%
and 88.9 g/L saturates the result. Everything above that is wasted biomass.

**So both levers are needed and either alone is insufficient.** Feed dilution
then becomes optional rather than necessary. The 1–2 µM window in
`Au_feed.range` is marked `conditional_on: q_max.engineering_target` for
exactly this reason: at today's `q_max` even 1 µM is above capacity.

### Two structural options this opens

1. **Non-viable biomass.** [S21](SOURCES.md) and [S22](SOURCES.md) show
   biosorption columns routinely use dead or immobilised cells, reused over ten
   cycles without losing capacity. If the cells need not be alive, `A_tox`,
   `k_dam`, `k_rep` and the damage state `D` all leave the capture model, and
   `X` is set by loading rather than growth.
2. **Grow elsewhere, load in.** Part III's logistic `X_max` is a growth
   carrying capacity. If cells are grown in a fermenter and concentrated into
   the capture vessel, `X` is an operator setting, not a biological limit.

⚠️ [S22](SOURCES.md) reports that in mixed-metal solutions capacity for each
metal fell by about half, and that in 10:1 solutions the more abundant metal
adsorbed better. Our leachate is copper-rich and gold-poor. See item 22.

**Decision needed:** set a display-density milestone as a multiple of the
current 2,749 sites per cell, and decide the leachate dilution factor. Those
two numbers set `eta_capture`.

---

## 1. Two different values for the GolB–gold dissociation constant

> **Superseded 2026-09-18.** The recovery model now uses `K_Au = 0.7 µM`
> from Nazir et al.'s fitted wild-type GolB-based sensor saturation curve
> [S78](SOURCES.md). This replaces the unsourced `0.1 µM` proxy and still
> rejects Part II's admitted `10 µM` placeholder. The literature study used a
> soluble fusion protein and HAuCl4 rather than displayed GolB and
> Au(I)-thiosulfate, so `0.7 µM` is recorded as a transferable proxy, not a
> project-matrix measurement. The same study's `0.2-1.15 µM` variant range is
> the model sweep. The original decision and arithmetic remain below as the
> record they supersede.

At the current `q_max = 0.0913 µmol/g` and `X_max = 5 g/L`, that sourced
range changes capture by 2.20-2.45-fold at feeds from 0.02 to 0.5 µM and by
1.10-fold at 10 µM. The parameter therefore remains important at low feed,
but its uncertainty now comes from a published GolB-based range rather than an
unsourced four-order-of-magnitude sweep.

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

**Decided 2026-08-10:** Part III's 0.1 µM is kept. Part II's 10 µM carries the
status "placeholder — no clean experimental K_d"; adopting it would replace a
proxy-bounded number with an admitted placeholder. This is the single
exception to the adopt-Part-II decision in item 2. Recorded in
`params/recovery_chain.yaml :: V1_capture.K_Au.decision_2026_08_10` and pinned
by `tests/test_interfaces.py::test_K_Au_was_deliberately_not_adopted_from_part_II`.

### ⚠️ Update: `K_D` is no longer insensitive at the new operating point

Part III §8 reports `K_D` with a PRCC below 0.05 and lists it among the
insensitive parameters. **That result was conditional on `q_max` = 4.4.**

With `q_max` = 4.4 the sites were abundant, so the model operated at feeds far
above `K_D` and the isotherm was saturated. Adopting `q_max` = 0.0163 pushes
the usable feed down to where `K_D` = 0.1 µM is comparable to the gold
concentration, and the isotherm shape starts to matter.

Equilibrium capture, `X_max` = 5 g/L, sweeping `K_D` across its own stated
range of 1e-4 to 0.1 µM:

| Feed | `K_D` = 1e-4 | `K_D` = 0.1 | Swing |
|---|---|---|---|
| 0.02 µM | 99.8% | 42.2% | **2.36×** |
| 0.05 µM | 99.7% | 38.4% | **2.60×** |
| 0.10 µM | 81.1% | 32.8% | **2.47×** |
| 0.50 µM | 16.3% | 13.2% | 1.23× |
| 10 µM | 0.8% | 0.8% | 1.01× |

At the engineering target `q_max` = 0.2964 the swing falls back to 1.07–1.14×,
because capacity is high enough to operate above `K_D` again.

**Consequence.** Sensitivity rankings in Part III §8 were computed at
`q_max` = 4.4 and should be recomputed. `K_D` moved from insensitive to a
factor of 2.6 at the feeds the adopted `q_max` forces. The same caution
applies to every other PRCC in that table.

**Decision needed:** measure `K_D`, or operate at the engineering target where
it stops mattering. Until then it is a 2.6× uncertainty on capture, not a
negligible one.

---

## 21. Nothing tells the leach when to stop, and Part III implies a deadline

**Promoted 2026-08-12. This item used to be theoretical. It is now the
difference between capturing most of the gold and capturing almost none of it.
Read item 39 with it.**

Part I integrates until gold runs out. Part III takes a single `Au_feed`
number. Neither document says which moment of the leach that number comes
from, and the choice is not free.

The sequential model has now put a number on it. The leach ends at 39.0 µM,
above the 30 µM cliff, and every improvement to the leach pushes it further
out. A stopping rule at about 20 µM lands inside Part III's recommended
window, and in the baseline run that is roughly 12 hours rather than 72.

Part I's author independently recommends running one day rather than three,
on throughput grounds. The two arguments agree. Stopping early is free, it
raises batch turnover, and it fixes the joint.

Part III §2.1 gives three thresholds on `Au_feed`:

| Threshold | What happens above it |
|---|---|
| 10 µM | below this, fraction captured is high but absolute gold is low |
| 22 µM | the capacity ceiling `q_max·X_max`; capture becomes capacity-limited |
| 30 µM | the `A_tox` disagreement starts costing 63–96% of capture |

A leach run crosses all three. With the placeholder rate constants and
`t_film` = 1 µm, the crossings land at:

| Reaches | Time |
|---|---|
| 10 µM | 314 min |
| 20 µM | 623 min |
| 22 µM, capacity ceiling | 684 min |
| 30 µM, toxicity onset | 929 min |

**So the leach has an optimal stop time, and it is set by the capture model,
not by the leaching chemistry.** Run past roughly 700 minutes in this
configuration and the extra gold you dissolve is gold the cells cannot hold.
Run past 929 and it starts poisoning them.

**This is the first result that could not have come from either document
alone.** It is the payoff of coupling them.

⚠️ **The specific minutes above are not a prediction.** They depend on
`t_film`, which is unknown by 20× (item 19), and on rate constants that are
placeholders (item 8). The *structure* of the result is robust: a stopping
rule exists and is imposed from downstream. The numbers are not.

**Also unresolvable today: the copper-to-gold ratio at the joint.** The model
currently reports 0.03 copper per gold, which is certainly wrong; a printed
circuit board is mostly copper. Both copper rate constants are `null`, so the
model has no opinion on selectivity at all. Part III §0 already records
selectivity against Cu/Ag/Ni as unknown. The joint carries copper forward
through `cu_feed_from_leach` marked `consumed_by_part_III: False`, so it stays
visible rather than silently dropped.

**Decision needed:** add a stopping rule to the coupled model, expressed as a
target `Au_feed` rather than a target time. Dilution is a legitimate lever,
which Part III §2.1 already says.

Found while walking through Joint 1 on 2026-08-10.

---

## 29. Every point where the three models touch, reconciled

Written 2026-08-10, revised 2026-08-11 after item 30.

**`μ` is settled.** One organism, one growth rate: 1.2 h⁻¹ = 0.02 min⁻¹, now
carried by all three parts. The original version of this item argued the two
rates must stay separate because the organisms differ. Item 30 reversed that.

**The biomass equation proposed here must not be applied.**
`dB/dt = Y(v_hyd − k_maint·B)` is built from `Y` and `k_maint`, the retired
*A. ferrooxidans* numbers. Use Part III's logistic growth equation instead.

### Every integration point

| # | Quantity | Part I | Parts II / III | Status |
|---|---|---|---|---|
| 1 | Growth rate `μ` | 0.02 min⁻¹ | 0.02 min⁻¹ | ✅ unified, item 30 |
| 2 | Biomass symbol `X` | cells L⁻¹ | g L⁻¹ | conversion at the joint, `cells_per_g` |
| 3 | `cells_per_g` = 3.57e12 | *E. coli* | *E. coli* | ✅ now valid in both directions |
| 4 | Symbol `k1` | parasitic rate | Finke–Watzky nucleation | ✅ renamed `k_par` / `k_nuc` |
| 5 | Symbol `m` | — | mRNA (II), maintenance (III) | ✅ renamed `k_maint` |
| 6 | Symbol `A` | metal area | sites (II), soluble gold (III) | ✅ renamed, item 25 |
| 7 | `K_m` / `K_d` / `K_D` | Michaelis | GolB | ✅ renamed `K_S4O6` / `K_Au` |
| 8 | Time base | minutes | minutes (II), hours (III) | ✅ adapters |
| 9 | Enzyme supply | was Eccleston | Part II cascade | ✅ unified, item 30 |
| 10 | pH | ~7 needed | ~7 (III), 1.4–1.8 elution, 9–10.5 leach | 🔴 item 23 |
| 11 | Temperature | ~30 °C | 37 °C, then 500–600 °C ashing | 🔴 **not modelled anywhere** |
| 12 | Oxygen | fixed input, 250 µM | needed, not tracked | both assume constant |
| 13 | Reactor volume | explicit `V_R` | V1 and V2 vessels | 🔴 **transfer unmodelled** |
| 14 | Thiosulfate | ~105,000 µM produced | no term for it | 🔴 item 22 |
| 15 | Copper | produced and tracked | no term for it | 🔴 carried but unconsumed, item 22 |

**Still open here:** rows 11 and 13, temperature and vessel transfer. Nobody
has claimed them, and the team deferred them on 2026-08-11.

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

### ✅ CLOSED 2026-08-11 — the gap is exactly the saturation term

The two calculations are related by one factor, and it closes to four figures:

```
closed form P_s  x  (1 - P_s/P_s_max)  =  ODE P_s
    5818.2       x        0.9450       =    5498.3
```

So the 5.5% is not a rounding difference or a second model. **It is the
saturation term `(1 - P_s/P_s,max)` that the closed form drops**, evaluated at
5,498 sites against a 1e5 ceiling. Nothing else differs.

**Decision taken: the ODE is authoritative.** It keeps the term; the closed
form is the non-saturating limit of the same equations. This repository was
already ODE-consistent without saying so: `teth_per_cell` = 2,749 and every
`q_max` derived from it use `f x P_s(ODE)`, not the closed form.

**Part III's reported `A` = 2,900 is the closed-form number.** Its reported
`P_s` = 5,500 is the ODE number. `f x 5500 = 2750`, not 2900, which is how the
inconsistency shows on the face of the document. Nothing in this repository
uses 2,900.

**Effect of the decision: none.** Every number already followed the ODE. What
changes is that the reason is now written down.

The doc correction for Part II's author is a single figure: report
`A` = 2,750, or state that `A` comes from the non-saturating closed form.

Pinned by `tests/test_expression.py::test_reported_numbers_are_internally_inconsistent`
and by `test_closed_form_times_saturation_equals_the_ode`.


Pinned by `tests/test_expression.py::test_reported_numbers_are_internally_inconsistent`.

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

## 11. Part I §1's parameter table uses Greek capital Mu for the growth rate

The table row for the growth-dilution rate is written with `U+039C`, Greek
capital letter Mu. Every equation in the document uses `U+03BC`, Greek small
letter mu. Confirmed by codepoint inspection of `docs/01_bioleaching.md`
line 62.

Cosmetic, with one practical cost: a text search for the symbol used in the
equations will not find the table row that defines it.

**Decision needed:** replace the capital with the lower-case letter.

Found while walking through Part I §1 on 2026-08-10.

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


# Closed, the record

## 42. `K_S2O3` was a placeholder sitting 8.6x above the measured band

**Was wrong.** `params/leach.yaml` carried `K_S2O3` = 5.0e4 µmol/L with
`status: calibrate` and the note "calibrate (~5e4)". A placeholder by its own
admission, with no source.

**What was done.** Adopted 3900 µmol/L from Part I's models on 2026-08-12.
It is 1/K_ads with K_ads measured at 172 to 510 M⁻¹, so the sourced band is
1960 to 5800 µmol/L and 3900 is its midpoint. The old value sat 8.6× above the
top of that band. AGENTS.md §6 step 3 decides this without a meeting: a sourced
value beats a stated placeholder.

**What it moved.** Gold recovered at 72 h goes from 22.6 % to 38.4 %, a 1.7×
lever on the headline result, because `K_S2O3` sets how hard the thiosulfate
saturation term throttles both metals.

**Pinned by** `test_K_S2O3_sourced_value_beat_the_repository_placeholder`,
which asserts the value, the retained `superseded` block, and the size of the
lever. Source: [18] Senanayake 2005.

---

## 8. Two rate constants existed only as relative values

**Was wrong.** `k_Au,Cu` was given as "≈10³× larger" than `k_Au,O2`, and
`k_Cu,O2` as "calibrate (Ea≈25.8 kJ/mol)", an activation energy rather than a
rate. `params/leach.yaml` held both as `null` with `status: calibrate`, so Part I
could not be run end to end at all.

**What was done.** Part I's author supplied both on 2026-08-12, along with
`k_Cu,Cu`, `k_par` and `k_ox,Cu`: `k_Au,Cu` = 1500 and `k_Cu,O2` = 200
µmol m⁻² min⁻¹, sourced to Aylmore & Muir 2001, Maharaj 2024 and
Salinas-Rodríguez 2022.

**One thing worth noting.** 1500 / 11.4 = 132, not 1000. The "≈10³×" in the
source table was itself approximate, by about eightfold. The source document is
unchanged.

The 132× ratio never shows up as a 132× rate, because `K_CuII` = 5e4 µmol/L and
Cu(II) never exceeds 829 µmol/L, so `f_Cu` stays below 0.017. Copper(II) is a
better oxidant per event and a scarce one.

**Pinned by** `test_every_part_I_rate_constant_now_has_a_value`.

**Still open:** `k_Cu,Cu` is assumed equal to `k_Cu,O2` rather than measured.
It is held separately in the YAML so that measuring one does not silently move
the other.

---

## 20. Model B's advantage rested on `k4`, which had no value

**Reversed twice, and the second reversal is the one that matters.**

1. **2026-08-12.** `k_ox,Cu` was supplied, the Cu(II) pool built, and Model B
   beat Model A by 9.6 percentage points. The item closed.
2. **2026-08-19.** `k_Au,Cu` moved from the ammoniacal 1,500 to the
   ammonia-free 21.0, because the team chose glycine over ammonia. The pool
   still builds to the same 818 umol/L and now buys **0.1 points, not 9.6**.
   The saturation factor is not the difference; the rate constant is.

So Model B and Model A are again almost the same model, for a completely
different reason than the one this item was raised about. **Copper still
destroys 98 % of the thiosulfate and no longer pays for it in gold.** That is
the case against ammonia stated as a number, and it is why item 59 exists.

Both regimes are pinned by
`tests/test_leach.py::test_the_cu_II_oxidant_route_dies_with_ammonia`, so
neither reversal can be undone silently.

---

**Was wrong.** No value for the Cu(I) re-oxidation constant, so Model B could
not be distinguished from Model A.

**What was done.** `k_ox,Cu` = 1e-4 L µmol⁻¹ min⁻¹ supplied 2026-08-12,
sourced to Breuer & Jeffrey 2003. Model B is worth 9.6 percentage points over
Model A.

**And the conclusion reversed.** The item framed a small `k_ox,Cu` as the bad
case. It is the good case: the Cu(II) pool that feeds the fast gold route is
the same pool that destroys 98 % of the leachant. **Item 41 restates this and
is the one to read**, though item 41's own numbers moved on 2026-08-19: the
optimum is 28 % to 52 %, not 38 % to 61 %. The original sweep is kept below.

**Pinned by** `test_the_cu_II_oxidant_route_dies_with_ammonia`, which
replaced `test_model_B_beats_model_A_now_that_k_ox_Cu_has_a_value` on
2026-08-19 and asserts BOTH regimes, and by
`test_cu_I_reoxidation_is_what_makes_copper_fatal`.

### The original statement of this item, kept for the record

*Written before the item closed. It is preserved because AGENTS.md
does not permit deleting the record, and it is here rather than in
the open section because the item is closed. Read the reversal
above first: the text below is superseded, not current.*

> **20. Model B's entire advantage rests on `k4`, which has no value**

> Part I §4 offers Model B as the realistic case, with copper(II) as a gold
> oxidant about 1,000× faster than oxygen. That advantage is real only while
> copper(II) exists in solution.
>
> Copper(II) is consumed by every gold atom it dissolves. Its only source is
> `v4 = k4·[O2]·[Cu(I)]`, the re-oxidation of copper(I) by oxygen. `k4` is
> listed as **calibrate** with no value, and carries `value: null` in
> `params/leach.yaml`.
>
> Sweeping `k4` over eight orders of magnitude, 600-minute run, everything else
> held fixed:
>
> | `k4` | Cu(II) at 600 min | Gold dissolved | vs Model A |
> |---|---|---|---|
> | Model A | — | 19.24 µmol | 1.00× |
> | 1e-8 | 0.0000 µM | 19.24 µmol | **1.00×** |
> | 1e-6 | 0.0002 µM | 19.27 µmol | 1.00× |
> | 1e-4 | 0.0214 µM | 21.76 µmol | 1.13× |
> | 1e-2 | 0.4519 µM | 71.37 µmol | 3.71× |
> | 1e0 | 0.5654 µM | 84.16 µmol | **4.37×** |
>
> **At the low end Model B is Model A.** The copper(II) pool never builds, the
> fast route never fires, and the two models give identical answers to three
> decimal places. At the high end Model B is 4.4× faster. Nothing in the
> document says which end is right.
>
> **A second observation, independent of `k4`.** Seeding the run with 500 µM
> copper(II) shows it collapsing to 0.21 µM within 30 minutes while copper(I)
> rises to 500 µM. Copper(II) is spent almost immediately and then held at a low
> steady state set by `k4`. So added copper(II) buys a **one-time bonus**
> proportional to the amount added, not a sustained faster rate.
>
> **Why the 1,000× never appears.** Copper(II) is a reagent per event, not a
> catalyst. It becomes a catalyst only through `k4`, and only as fast as `k4`
> allows.
>
> **Decision needed:** `k4` is the parameter that decides whether Model B is
> worth having. Measure the copper(I) re-oxidation rate under your conditions,
> or state that Model A is the operating assumption and drop Model B. Note that
> this also makes aeration a design lever, since `v4` scales with `[O2]`.
>
> Found while walking through Part I §5 on 2026-08-10.
>
> ### CLOSED 2026-08-12, and the conclusion above is wrong
>
> Part I's author supplied `k_ox,Cu` = 1e-4 L µmol⁻¹ min⁻¹, sourced to Breuer &
> Jeffrey 2003. At that value the copper(II) pool does build, and Model B is
> worth 9.6 percentage points of gold over Model A, 38.4 % against 28.8 %.
>
> The decision above framed a small `k_ox,Cu` as the bad case. **It is the good
> case.** The same copper(II) pool that feeds the fast gold route destroys 98 %
> of the thiosulfate, and killing the re-oxidation route takes recovery to 88 %.
> The last sentence above, that aeration is a design lever, is the part that
> survived, and it turned out to be the most valuable sentence in this file.
>
> **Read item 41.** It restates this properly and gives the oxygen sweep.
>
> Pinned by `test_model_B_beats_model_A_now_that_k_ox_Cu_has_a_value`.

## 17. `K_m` had no single value, and the range mattered at low tetrathionate

**Was wrong.** `K_S4O6` given only as the range 50 to 2400 µmol/L, a 48-fold
spread, with no value chosen.

**What was done.** Part I's author chose 300 µmol/L and used it in both models.
Held as `status: chosen_from_sourced_range`.

**Why it stopped mattering.** The item's own table shows the range costs less
than 10 % above 10 000 µmol/L of tetrathionate. The broth recipe charges 23 200
µmol/L, so the saturating factor is 0.987 at the start of Stage 2 and the
enzyme runs at `Vmax` for almost the whole vessel. The item recommended fixing
the operating concentration high enough that the choice stops mattering; the
broth does that without anyone deciding anything. Full analysis left in place
under `# Open`.

---

**Unchanged since it closed.** `K_S4O6` = 300 was chosen from the sourced
50 to 2,400 range on 2026-08-12 and nothing since has moved it. The choice
barely matters: tetrathionate starts at 23,200 umol/L against `K_S4O6` = 300,
so the saturating factor is 0.987 at t = 0 and Stage 2 runs at `Vmax` for
almost its whole length.

### The original statement of this item, kept for the record

*Written before the item closed. It is preserved because AGENTS.md
does not permit deleting the record, and it is here rather than in
the open section because the item is closed. Read the reversal
above first: the text below is superseded, not current.*

> **17. `K_m` has no single value, and the range matters at low tetrathionate**

> Part I §2 gives `K_m` as the range **50–2400 µmol/L**, sourced to Kanao 2007,
> with no value chosen. That is a 48-fold spread.
>
> Its effect depends entirely on where you operate, because it enters only
> through `θ = S4O6/(K_m + S4O6)`:
>
> | `[S4O6]` µmol/L | θ at `K_m`=50 | θ at `K_m`=2400 | Ratio |
> |---|---|---|---|
> | 100 | 0.667 | 0.040 | **16.7×** |
> | 500 | 0.909 | 0.172 | 5.3× |
> | 1,000 | 0.952 | 0.294 | 3.2× |
> | 5,000 | 0.990 | 0.676 | 1.5× |
> | 10,000 | 0.995 | 0.806 | **1.2×** |
> | 20,000 | 0.998 | 0.893 | 1.1× |
>
> **Practical consequence.** Run tetrathionate at or above 10,000 µmol/L and the
> choice of `K_m` costs at most 23%. Run below 1,000 µmol/L and it costs a
> factor of 3 to 17. The uncertainty is removable by an operating decision, not
> by a measurement.
>
> **Independent cross-check.** Eccleston & Kelly 1978 ([S5](SOURCES.md)) report
> an apparent `K_m` for tetrathionate oxidation of 0.13–8.33 mM, that is
> 130–8330 µmol/L, and note it is pH dependent. That overlaps Part I's range and
> extends it upward, which strengthens the case for operating well above 10 mM.
>
> **Decision needed:** either choose a value with a stated pH, or fix the
> operating concentration high enough that the choice stops mattering. The
> second is cheaper.
>
> Found while walking through Part I §2 on 2026-08-10.
>
> ### CLOSED 2026-08-12, and by the cheaper route
>
> Part I's author chose `K_S4O6` = 300 µmol/L from the range, and used it in both
> of his models. `params/leach.yaml` now carries it as
> `status: chosen_from_sourced_range`.
>
> The choice barely matters, exactly as the table above predicts, because the
> broth charges tetrathionate at 23 200 µmol/L. That is above the top row, where
> the 48-fold range costs less than 10 %. The saturating factor is 0.987 at the
> start of Stage 2, so the enzyme runs at `Vmax` for almost the whole vessel.
>
> The recommendation in this item, to fix the operating concentration high enough
> that the choice stops mattering, is what the broth recipe does on its own.

## 31. Every capture number was computed by a solver that was not in the repository

Found by the 2026-08-11 audit. Not a fault in any source document.

`MASTER.md` step 8 and `ISSUES.md` items 1, 2, 22 and 26 all quote capture
efficiencies. They were computed by solving the Langmuir isotherm together with
the mass balance `Au_tot = A + C`, which reduces to one quadratic:

```
C^2 - (S0 + K_Au + Au_tot)*C + S0*Au_tot = 0
```

**No function in `src/` did that.** What existed was
`capture_langmuir_equilibrium(A, S0, K_Au)` returning `S0*A/(A + K_Au)`, the
isotherm applied to **total** gold instead of free gold. At `S0` = 22 uM and a
10 uM feed it returns 21.8 uM bound, **218% of what was added**. It was called
by nothing: no test, no notebook cell, no other module.

So the repository's central claim, that every number traces to code, did not
hold for the capture stage.

**Fixed 2026-08-11.**

| Function | Does |
|---|---|
| `capture_langmuir_isotherm(A_free, S0, K_Au)` | the isotherm as `model.md` prints it, needing **free** gold. Renamed so the argument cannot be mistaken. |
| `capture_equilibrium(A_tot, S0, K_Au)` | solves the quadratic, takes the gold you added |
| `eta_capture(A_tot, S0, K_Au)` | the fraction captured, between 0 and 1 |

Verified: the solver reproduces all fifteen cells of `MASTER.md` step 8 and all
five rows of item 1's `K_Au` swing table, to one decimal place. **The published
numbers were right; only the code was missing.**

Pinned by six tests in `tests/test_interfaces.py`, including
`test_isotherm_applied_to_total_gold_is_unphysical`, which keeps the reason the
two functions are separate visible, and
`test_capture_never_exceeds_the_feed_or_the_sites`.

---

## 30. *E. coli* runs the whole chain, and Part I assumed an acidophile

Raised and answered 2026-08-11. The team confirmed *E. coli* throughout, and
that the *E. coli* makes the thiosulfate.

### What was wrong

`Vmax` = 14.3 came from Eccleston & Kelly's growth yield and maintenance
coefficient for *Acidithiobacillus ferrooxidans*. That argument works only
because **its whole energy budget runs through tetrathionate**: measure growth
and its substrate cost, and you have measured the enzyme. *E. coli* has no
native tetrathionate metabolism, so there is no growth yield to measure and the
argument has nothing to stand on.

### The route that fits an engineered host

```
Vmax = k_cat * [TetH]          [TetH] = f*P_s * X / N_A
```

Point Part II's cascade at TetH instead of GolB. Every parameter in it except
`f` describes the host and the display scaffold, not GolB, so nothing is
refitted.

| Step | Value |
|---|---|
| `P_s`, surface protein per cell | 5,498 molecules/cell |
| × `f` = 0.5 folded and active | **2,749 molecules/cell** |
| × 4.0 g/L × 3.57e12 cells/g ÷ N_A | **0.0652 µM TetH** |
| × `k_cat` = 220 min⁻¹ | **`Vmax` = 14.3 µmol L⁻¹ min⁻¹** |

### The headline: 40x weaker per gram

| Biomass | `Vmax` |
|---|---|
| 0.1 g/L | 0.36 |
| 1.0 g/L | 3.59 |
| **4.0 g/L** | **14.3, in use** |
| 30 g/L | 108 |

The retired route claimed 14.3 at **0.1 g/L**. The engineered host needs
**4.0 g/L** for the same number. **Not a blocker**: a routine aerobic batch
reaches 3 to 5 g/L, and item 26 establishes that far higher is published.

### Consequences elsewhere

- **Item 12 closes.** `μ` acts per cell inside the cascade, not on bulk `Vmax`.
- **Item 15's factor of 2 cancels**, because `teth_per_cell` counts monomers.
- **Item 29's headline reverses.** One organism, so 0.092 against 1.2 h⁻¹ was a
  real conflict. 1.2 h⁻¹ wins. Its biomass equation must **not** be applied.
- **Item 23 narrows** from about 7 pH units to about 2.5.
- `enzyme_production.mu` moved 0.0 → 0.02 min⁻¹.

### The weak number, and the new risk

`f` = 0.5 is Part II's fitted folding fraction **for GolB**. TetH is a 100 kDa
homodimer needing a disulfide bond, so its active fraction is not known to be
0.5, and it scales `Vmax` linearly. This is the largest uncertainty in the
block, and an activity assay on the displayed cells settles it.

**TetH inclusion-body formation in *E. coli* is now a live risk.** Nothing in
the three documents addresses it, and `f` is exactly where it shows up.

The Eccleston numbers are retired, unchanged, under
`enzyme_capacity.retired_A_ferrooxidans_route`. Pinned by five tests under
"Joint 3" in `tests/test_interfaces.py`.

---

## 12. Part I's enzyme equation mixed a bulk balance with an intracellular one

Part I §1 gives `d[E]/dt = k_syn·X − (k_deg + μ)·E`, citing Alon for the `−μ·E`
term. The two halves belong to different frames. Production `k_syn·X` is per
litre of reactor. Growth dilution `−μ·E` is Alon's term for a concentration
measured **inside a cell**. In a sealed batch reactor growing cells **raise**
bulk enzyme per litre; they do not dilute it.

Escalated when the team confirmed the cells grow, so `μ` > 0 and Part I has no
equation for `X(t)`.

**Resolved 2026-08-11 by item 30's expression route.** Batch, and the frame
question dissolves:

- `μ` acts **inside Part II's per-cell cascade**, on `m`, `P_c` and `P_s`.
  Those are per-cell quantities, so Alon's term is correct exactly where
  Part II already had it.
- Bulk `Vmax = k_cat · teth_per_cell · X / N_A` rises with biomass. There is no
  `−μ·Vmax` term in the operating route. **`μ` must not be applied twice.**
- `X(t)` comes from Part III's logistic equation, legitimate now that item 30
  confirmed one organism throughout.

`enzyme_production.mu` moved 0.0 → 0.02 min⁻¹. The standalone `dVmax/dt` ODE is
kept in `src/leach.py` for the isolated enzyme block only.

---

## 2. `q_max` was 255x too high, and 15x over a physical ceiling

**Capture interpretation superseded, 2026-09-07, item 91.** The expression-derived
number bounds single-site occupancy, not all whole-cell gold accumulation.
S76 supplies experimental whole-cell evidence that the earlier search missed.
Original arithmetic remains below as a record.

| Route | `q_max` µM/(g/L) | Sites/cell implied |
|---|---|---|
| Part II cascade, derived | **0.0108** | 2,749 |
| **Every anchor occupied** | **0.1961** | 50,000 |
| Part III sweep low end | 0.33 | 55,667 |
| Part III value in use | 4.4 | 742,225 |

*Values corrected 2026-08-11 by item 33. They were 0.0163 and 0.2964.*

Part III's 4.4 is neither a published isotherm nor a shown calculation; its
author confirmed it is assumed. Part II's `P_s,max` = 1e5 anchors with `f` = 0.5
caps active sites at 50,000/cell, so 4.4 needs 15x more anchors than a cell
has. The `cells_per_g` uncertainty of about 2.5x does not rescue it.

**DECIDED 2026-08-10: Part II is the authority for every protein-model
quantity.** `q_max` = 0.0163, `μ` = 1.2 h⁻¹. `K_Au` deliberately not adopted,
see item 1.

**What it cost.** The capacity ceiling at `X_max` = 5 g/L fell from 22 µM to
0.0539 µM, a factor of 408. At a 10 µM feed `eta_total` fell from 32.4% to
0.22%. **No feed concentration is currently free of the capacity limit.**

There is 18x of genuine engineering headroom, not 255x. See item 26.

Pinned by `test_capacity_ceiling_after_adopting_part_II`,
`test_joint2_historical_disagreement_stays_on_the_record` and
`test_part_II_and_part_III_now_agree_on_growth_rate`.

**Sub-question answered 2026-08-11 by the source audit.** [S29](SOURCES.md)
Jose & Meyer 2007 says autodisplay exports "**more than** 100,000 recombinant
molecules per single cell". So 1e5 is a **demonstrated floor, not a hard
ceiling**, and the 0.1961 engineering target is a design anchor that a better
construct could exceed. The argument that 4.4 is unreachable still holds:
742,225 sites/cell is 7x above a figure the field describes as its high end.

---

## 18. `v1` and `R_Au` were each used as two quantities at once

Part I writes three rates that lump two chemical pathways together, then
applies one stoichiometric coefficient to the lumped total. The pathways do not
share coefficients, so no single number is right for both.

| Rate | O₂ route | Cu(II) route |
|---|---|---|
| `v1`, copper dissolving | 2 S₂O₃ per Cu, 1 Cu(I) | 4 S₂O₃ per Cu, 2 Cu(I), 1 Cu(II) used |
| `R_Au`, gold dissolving | **no copper at all** | 1 Cu(II) per Au |

The coefficients sit **inside** `v1`'s own definition, which is why the
thiosulfate equation shows no visible 2 in front of it. So `v1` is a
thiosulfate consumption rate in §3 and a copper dissolution rate in §5, and it
cannot be both.

**Resolved 2026-08-10.** `src/leach.py` splits each rate by oxidant and charges
each pathway its own coefficients, read off the balanced reactions printed in
§4 and §5:

```
s2o3_draw_Cu    = 2*v1_O2 + 4*v1_Cu
cu_I_from_leach = 1*v1_O2 + 2*v1_Cu
cu_II_used      = 1*v1_Cu           (+ R_Au_Cu from the gold side)
```

`stoichiometry="source"` reproduces Part I exactly as written;
`stoichiometry="balanced"` is the default. **This also resolved item 5.**

Pinned by `test_balanced_stoichiometry_keeps_cu_II_non_negative` and
`test_balanced_stoichiometry_charges_thiosulfate_per_copper_route`.

---

## 5. Part I's Cu(II) pool has no production route and goes negative

Section 5 states Cu(II) is produced only by oxygen re-oxidation of Cu(I). From
a copper-free start that rate is zero. Part I then subtracts the **whole** gold
rate `R_Au` from Cu(II), including its oxygen pathway, which consumes no
copper. A sink with no source drives the pool below zero.

Model B also collapses to Model A from a copper-free start, because the fast
pathway needs a Cu(II) pool that never forms.

**Resolved as a side effect of item 18.** Splitting `R_Au` by oxidant means
only the Cu(II)-driven pathway draws on Cu(II), so the sink vanishes exactly
when the pool does.

Pinned by `test_cu_II_goes_negative_under_source_stoichiometry`, which keeps
the documented behaviour visible, and
`test_balanced_stoichiometry_keeps_cu_II_non_negative`, which pins the fix.

---

## 13. `k_syn` and `k_cat` are not separately identifiable

The enzyme enters the model in exactly one place. At the enzyme steady state
`E = k_syn·X/(k_deg + μ)`, so

```
v_hyd = [ k_cat * k_syn * X / (k_deg + mu) ] * theta(S4O6, K_S4O6)
                ^^^^^^^^^^^^^^ one lumped quantity
```

Doubling one and halving the other leaves every trajectory unchanged. Verified:
three runs with the same product and factors spread over 5,000x agree on
thiosulfate at 1,000 min to 2e-10 relative. Fitting both returns a ridge, not a
pair. Same failure mode as `k_dam`/`A_tox` in Part III §7.

**Resolved: lumped into one state.**

```
Vmax(t) = k_cat * E(t)          umol L^-1 min^-1
```

`Vmax` is what an activity assay reports directly, in U per litre.
`src/leach.py` tracks it as state 0. `k_syn` and `k_cat` stay transcribed in
the parameter file, so the source table is still fully represented. Part I's
text is unchanged.

Superseded in practice by item 30, which gets `Vmax` from the expression
cascade and needs neither constant.

---

## 16. One reaction was given two rate constants, `k1` and `k3`

The parasitic reaction `2Cu(II) + 2S2O3 → 2Cu(I) + S4O6` appears twice. Its
sulfur side used `k1`, in §2 and §3; its copper side used `k3`, in §5. One
reaction must have one rate: reading the extent off each side gives
`k1·[Cu(II)][S2O3]` and `k3·[Cu(II)][S2O3]`, which agree only when `k1 = k3`.
With `k3` five times larger, copper turns over five times per tetrathionate
produced and elements are not conserved. The table hid this by giving `k3` as
"≈ `k1`", with both marked `calibrate`, so nothing enforced equality.

**Resolved 2026-08-11 by the symbol rename.** Both are now **`k_par`**, a
single entry under `tetrathionate`. `copper.k3` is deleted. `src/leach.py` uses
`p["k_par"]` on both sides. **There is no longer any way to give this reaction
two rates.** The source table is unchanged.

---

## 25. The symbol `A` meant three different things

Part I used `A` for metal surface area, Part II for active sites per cell, and
Part III for soluble gold. Parts II and III meet at Joint 2, so a reader
following the chain saw `A` become `q_max` become `S_0`, while a different `A`
was the thing being captured.

**Resolved 2026-08-11 by the rename.**

| Quantity | Was | Now |
|---|---|---|
| Part III soluble gold | `A` | **`A`**, unchanged |
| Part II active sites per cell | `A` | **`s`** |
| Part I metal areas | `A_Au`, `A_Cu` | **`a_Au`**, **`a_Cu`** |

`A` now means one thing across the chain: soluble gold. Joint 2 reads
`s` → `q_max` → `S_0`. Applied in `src/`, `params/`, `tests/`, `model.ipynb`,
`EQUATIONS.md` and `MASTER.md`, which carries the full was/now table. The three
source documents keep their original symbols.

---

## 15. Part I marks `k_cat` unmeasured; it is published

Specific activity of the purified enzyme **is** `k_cat`, once divided by molar
mass.

```
1 mg pure Af-Tth = 1e-3 g / 1.0e5 g/mol = 0.01 umol
that mg turns over 2.2 umol tetrathionate per minute      [S1]
k_cat = 2.2 / 0.01 = 220 /min = 3.7 /s
```

**Resolved 2026-08-11.** `params/leach.yaml :: tetrathionate.k_cat` is
220 min⁻¹, status `sourced`, with the derivation written into the file.

**The dimer ambiguity is carried, not resolved.** 220 min⁻¹ is per 100 kDa
dimer; 110 per 50 kDa subunit if each carries its own site. The sources do not
settle it. **It cancels in `Vmax`**, because `teth_per_cell` counts monomers:
monomers × 110 equals dimers × 220. Pinned by
`test_dimer_ambiguity_cancels_in_vmax`.

Part I's table still reads "unmeasured --- calibrate". That is a one-line doc
correction and no result depends on it.

---

## 6. Part I §3 defines a yield `Y` and never uses it

The table gives `Y` = 1, "stoichiometric yield, S₂O₃ per S₄O₆". Neither
equation in §3 contains it. Harmless while `Y` = 1, a silent error the moment
anyone changes it.

**Resolved 2026-08-11 by inserting `Y` into the production term:**

```
dS2O3 = Y*v_hyd - 2*k_par*[Cu(II)]*[S2O3] - (2/V_R)*R_Au - (1/V_R)*s2o3_draw_Cu
```

No number moved. `Y` is required, not defaulted, so a run that omits it raises
`KeyError`. Pinned by `test_stoichiometric_yield_scales_thiosulfate_production`.

---

## 24. Parts II and III disagreed about how fast *E. coli* grows

| Document | `μ` | Doubling |
|---|---|---|
| Part II §4 | 0.02 min⁻¹ = **1.2 h⁻¹** | 34.7 min |
| Part III §7 | **0.7 h⁻¹** | 59.4 min |

Not cosmetic: Part II §8 gives `μ` a normalised sensitivity of −1.051, the
largest of any parameter, and dilution accounts for 80% of the loss from the
surface-protein pool. At 0.7 h⁻¹ the cascade gives 4,429 sites/cell and
`q_max` = 0.0263, against 2,749 and 0.0163 at 1.2 h⁻¹.

**Resolved 2026-08-10: Part II's 1.2 h⁻¹ adopted**, as part of the item 2
decision. Item 30 later extended the same value to Part I. Pinned by
`test_part_II_and_part_III_now_agree_on_growth_rate`.

---

## 4. Part I mixes mol and µmol in the solid inventories

Section 4's table gives `n_Au` as "mol (or µmol)" while `R_Au` is in µmol/min,
and `dn_Au/dt = −R_Au`. Only µmol makes those consistent.

**Resolved: µmol throughout**, in `src/leach.py`, `tests/` and `model.ipynb`.
A doc correction to Part I is still outstanding and changes no result.

---

## 9. The three documents use three unit systems

| Part | Concentration | Time |
|---|---|---|
| I | µmol/L | minutes |
| II | molecules/cell | minutes |
| III | µM | **hours** |

µmol/L and µM are the same unit, so concentrations need no conversion. Time
does: a rate constant moved across a joint without conversion is wrong by 60x.

**Resolved** by `interfaces.per_hour` and `interfaces.per_minute`. Only
quantities carrying a time dimension convert; `K_m`-type constants must not.

---

## 14. The `k_syn` placeholder was 7,000x too large

Superseded by item 13. Kept because the placeholder's size matters to anyone
reading an old figure.

No direct measurement of `k_syn` exists, which is expected: nobody reports
enzyme synthesis rate per cell. A proxy route through specific activities
([S1](SOURCES.md), 2.2 U/mg purified; [S2](SOURCES.md), 0.28 U/mg in extract)
gives about 77,000 TetH molecules per cell and `k_syn` ≈ 1.4e-16
µmol cell⁻¹ min⁻¹.

**It rests on an assumed `protein_per_cell` = 1e-13 g, and mixes an archaeal
extract with an *Acidithiobacillus* purified enzyme.** It is a proxy, not a
measurement, and is stored under `k_syn.literature_estimate`, never as a value.

**The placeholder used in old test files and figures was 1e-12**, 7,143x
larger, implying 909 µmol/L of enzyme. No figure drawn with it has a meaningful
vertical scale.

---


## 47. The elution rate law: pseudo-second-order adopted

> **Superseded 2026-09-18.** The working model is now first order:
> `eta_elute = (1-phi)(1-exp(-k_elute*t))`. The value
> `k_elute = 0.22 h^-1` is the conservative lower bound obtained from S60:
> more than 90% release at 12 h against a 97% ceiling gives
> `-ln(1-0.90/0.97)/12 = 0.219 h^-1`. The earlier `2.0 h^-1` was an apparent
> PSO rate and is retained under `superseded` in the parameter file. Neither
> rate law is validated on GolB; the time course requested in item 28 remains
> the deciding experiment.

Found 2026-08-15 while rewriting `REVIEW.md` section 6.2. **Decided
2026-08-16: the model uses pseudo-second-order.**

**What the model used to do.** `dC/dt = -k_elute(C - phiC_0)`, integrating to
`eta_elute = (1 - phi)(1 - e^{-kt})`. That is the **Lagergren
pseudo-first-order (PFO)** law of 1898 [S33] run backwards. Section 6.2 derived
it from first principles without naming it, which made a standard model look
invented.

**Why it was replaced.**

1. Ho and McKay [S34] tested 12 sorption systems that had been published as
   first order. **Pseudo-second-order (PSO) gave the higher correlation in all
   12.**
2. The two thiourea papers already cited here, [S24] and [S25], report PSO.
3. PFO is widely reported to track only the first 20-30 minutes of a
   chemisorption time course. GolB binds gold through the Cys10/Cys13 thiolate
   pair, which is chemisorption, and the wash runs for hours.

**What changed, and what did not.**

$$\eta_{elute}(t)=(1-\phi)\,\frac{k_{elute}t}{1+k_{elute}t}$$

| | PFO, superseded | PSO, in use |
|---|---|---|
| Ceiling `1 - phi` | 0.87 | **0.87, identical** |
| 50% of the ceiling | `0.69/k` | `1/k`, 0.5 h |
| 95% of the ceiling | `3/k`, 1.5 h | **`19/k`, 9.5 h** |
| `eta_elute` at the 6 h operating point | 0.870 | **0.803** |

**The ceiling is untouched**, so `phi`, item 28, and every ceiling argument in
section 6.2 stand exactly as written. Only the contact time moved, and it moved
by about 4x.

**One rate constant, not two.** A second symbol `k_elute_pso` existed from
2026-08-15 to 2026-08-16 and was dropped. The step has one rate constant,
`k_elute`, whatever the rate law: the PSO apparent constant is `k2*C_elut(0)`,
which carries the same units and gives the same stripping rate at `t = 0`, so
no new number entered the model.

**`k_elute` is provisional because the eluent is.** It follows the eluent
choice, item 28, and 2.0 h^-1 at 1 M thiourea is a placeholder until that
choice is made. Choosing the eluent fixes `k_elute` and `phi` together.

**A subtlety worth having ready, because a reviewer will find it.** The source
document does use the words "pseudo-first-order", at
`docs/00_overview_gold_biorecovery.md` line 122. Its argument is the excess
argument: thiourea at ~1 M against micromolar gold is a ~10^4 excess, so `[TU]`
is constant through the wash and `k[TU]^n` collapses to one rate constant.
**That argument is sound and it is a different claim.** It establishes first
order *in thiourea*. The order *in the bound gold*, which is the exponent that
sets the wash time, was never tested. Nothing in the source text needs changing
- AGENTS.md rule 1 - because nothing in it is an error.

**Downstream effect.** Every `eta_total` in this repository moved by the factor
0.8031/0.870 = 0.923 and nothing else changed. `MASTER.md` bottom-line table,
the notebook loss table and `STRUCTURE.md` are all recomputed. **Any
`eta_total` quoted before 2026-08-16 is optimistic on elution.**

**What was done.**

- `recovery_chain.eta_elute` is now PSO. PFO is retained as
  `recovery_chain.eta_elute_pfo` for the comparison figure and to reproduce
  earlier numbers.
- `elution.kinetic_model` = PSO in `params/recovery_chain.yaml`, with PFO in a
  `superseded:` block.
- Pinned by `test_elution_uses_pseudo_second_order_and_the_ceiling_is_unchanged`,
  `test_pfo_is_retained_and_is_the_optimistic_law`,
  `test_elution_has_one_rate_constant_and_the_model_is_PSO` and
  `test_switching_to_pso_elution_costs_the_chain_three_points`.

**What would still overturn it. One time course, the same run item 28 needs.**
Sample the eluate at 0.25, 0.5, 1, 2, 4 and 6 h. Then:

- `t/(C_0 - C)` against `t` straight => PSO, as adopted.
- `ln(C - phiC_0)` against `t` straight => PFO, and the wash is 4x shorter.

The 6 h endpoint gives `phi` directly. **Six samples close item 28 and confirm
or overturn item 47**, which makes it the cheapest open item in the file.

**Who decides:** wet lab, one experiment.

---


## 48. The reducing protein has no upstream model. Arm B is drawn, never built

Found 2026-08-16, from the question "where does the reducing protein come
from?". The answer is that nothing in this repository says.

**The source document draws it.** `docs/00_overview_gold_biorecovery.md` section
1 shows two arms converging at reduction:

```
ARM A (gold)                        ARM B (reagent)
  leach -> Au_feed                    grow E. coli BL21 + ABC construct
      |                               induce 1 mM IPTG, 4 h
  V1 capture, 13-16 h                 lyse: sonicate, 100,000 g 90 min
      | thiourea elution                     |
  conditioning ----------------> V2 lysate reduction, 12-24 h
```

**Arm A is fully modelled. Arm B is not modelled at all.** There is no growth
equation, no expression cascade, no lysis yield and no volume ratio for the
reagent arm anywhere in `src/` or `params/`.

**What that costs, concretely.**

1. `E_tot` has **no value** in `params/recovery_chain.yaml`. It carries only a
   formula, `protein/70000*1e6`, and the status "measurable; set by induction".
2. The 0.2 g/L that every reduction number depends on is **hard-coded in two
   places**: `model.ipynb` cell 34 and `tests/test_sensitivity.py` line 29.
   That breaks AGENTS.md rule 2, no number in a `.py` file.
3. `R0`, the reductant pool from lysis, is **null**, status "lysis-dilution
   choice, not a literature value". `src/sensitivity.py` reads `p["R0"]` and
   only runs because the caller supplies one by hand.

**Compare Part I, which had exactly this gap and closed it.** Its culture vessel
is modelled, and the answer is a number the wet lab can act on: **9.1 litres of
culture per litre of conversion vessel**. The identical calculation for the
reductase does not exist.

### The size of it, to an order of magnitude

The V2 vessel needs 0.2 g/L of a 70 kDa protein, which is **2.86 uM**.

Running Part II's cascade with export switched off, since a cytoplasmic
reductase is not displayed, gives about 7,300 molecules per cell:

| Culture density | Reductase in the culture | Concentration needed |
|---|---|---|
| 1e12 cells/L | 0.012 uM | **237x** |
| 1e13 cells/L | 0.121 uM | **24x** |

**These are estimates using GolB's promoter, plasmid copy number and
translation rate**, because the reductase construct has none of its own. They
are the right order of magnitude and nothing more. Getting a real number is the
work this item asks for.

### The consequence nobody has priced, and it is the important half

**The lysate is mixed with the eluate, so the volumes add and the gold is
diluted.** Reduction already has a threshold at about 3 uM (section 6.3) and
capture delivers 0.054 uM, 55x below it. Every litre of lysate added makes that
worse.

Two constraints fall straight out of the mixing arithmetic:

**The lysate must be more concentrated in reductase than the target.** Mixing
can only dilute, so a lysate at exactly 2.86 uM can never bring the vessel to
2.86 uM at any ratio. It must exceed it, and by a comfortable margin.

**How much margin decides how badly the gold is diluted:**

| Lysate reductase | Relative to target | Lysate:eluate | Gold diluted by | Gold from 0.054 uM |
|---|---|---|---|---|
| 3.00 uM | 1.05x | 20:1 | **21x** | 0.0026 uM |
| 4.29 uM | 1.5x | 2:1 | 3.0x | 0.018 uM |
| 5.71 uM | 2x | 1:1 | 2.0x | 0.027 uM |
| 14.3 uM | 5x | 0.25:1 | 1.25x | 0.043 uM |
| 28.6 uM | 10x | 0.11:1 | **1.11x** | 0.049 uM |

**A weakly concentrated lysate costs a factor of 21 on the gold.** A strongly
concentrated one costs 11%. The reagent arm is therefore not a side branch: it
sets a multiplier on the quantity that item 35 says is already the binding
constraint.

**This also cuts the other way and is worth stating.** Item 35 recommends a 10x
volume reduction between elution and reduction. That reduction has to survive
the lysate addition, so the two steps must be designed together, not in series.

### What is needed

1. **The reductase's own expression parameters**: promoter strength, copy
   number, translation rate, decay. Part II's machinery then runs unchanged;
   only the numbers differ, and `k_sec` is zero.
2. **Lysis yield.** What fraction of cell protein ends up soluble in the
   supernatant after sonication and 100,000 g for 90 min.
3. **The concentration step.** Whatever takes the lysate from culture density
   to the 10x-above-target figure the table above wants.
4. **The mixing ratio**, as a design variable, jointly with item 35.

Only then do `E_tot` and `R0` get values, and only then does the electron
ceiling in section 6.3 rest on anything. **Note that the ceiling itself is not
in doubt**: at 98.9% it has a wide margin, and it depends on `E_tot` being
roughly right rather than exactly right. What is in doubt is the volume, and
therefore the gold concentration.

**Who decides:** team plus wet lab. The expression parameters are a
construct-design question; the lysis yield and the concentration step are
bench measurements.

---


## 49. The reduction chemistry is not the chemistry that was demonstrated

Found 2026-08-16, from the question "is the chemistry ignored?". It is. The
model carries a rate law and no reactions, and the reactions it stands on are
not the ones our chain produces.

**The source.** The reducing protein is the ABC transporter peptide-binding
protein of *Thermus scotoductus* SA-01, expressed in *E. coli* BL21(DE3) and
*T. thermophilus* HB27, about 70 kDa. Erasmus M., Idris O. A., Adetunji A. I.,
Cason E. D. (2024), *Biologia* 79:2605-2619,
doi:10.1007/s11756-024-01733-2. Filed as **S35**.

**Their reaction, which is the only demonstration that exists**, in a 1 mL
total volume:

| Component | Stock | Role |
|---|---|---|
| purified ABC protein | 100 uL | the reductase |
| HAuCl4, **Au(III)** | 100 uL of 0-10 mM | the gold |
| **methyl viologen** | 100 uL of 1 uM | **electron shuttle** |
| **sodium dithionite** | 100 uL of 46 uM | **the electron source** |
| phosphate buffer pH 7.4 | 100 uL of 50 mM | |
| water | 500 uL | |

Incubated 24 h. Reduction read as a colour change and a 520-560 nm plasmon
band. Optimum quoted at 0.5-2 mM HAuCl4. Boiled protein does not work, so the
activity is the folded protein and not a buffer artefact.

### Three gaps, in order of how much they matter

**1. The electron chain has a mediator, and the model does not.** The published
route is

```
   dithionite  ->  methyl viologen  ->  ABC protein  ->  Au(III)
```

Four steps, not two. `src/sensitivity.py` has the protein donating directly to
gold, with `Rech` recharging it. Methyl viologen appears nowhere in this
repository. Whether crude lysate supplies a native mediator is unknown, and the
process design says "do not dialyse" precisely because something in the lysate
is doing a job nobody has named.

**2. The protein has only ever reduced Au(III) from chloride. Our chain
delivers Au(I) from thiourea.**

| | Published | Ours |
|---|---|---|
| Oxidation state | Au(III) | **Au(I)** |
| Ligand | chloride, AuCl4- | **thiourea, Au(CS(NH2)2)2+** |
| Charge | anion | **cation** |
| Electrons per gold | 3 | **1** |

Item 28 already records that the charge reverses across elution. What was never
recorded is that the reduction step then receives a species the protein has
never been shown to touch. `nu` = 0.5 in `params/recovery_chain.yaml` is the
Au(I) stoichiometry, so the model has already committed to the untested case.

**Searched 2026-08-16, and the concern is weaker than first written.** Three
findings, all pointing the same way:

1. **Au(I) is the obligatory intermediate, not a different reaction.**
   Protein-mediated gold reduction is documented as stepwise: Au(III) is
   reduced to Au(I) and only then to Au(0), through hydroxyl, amine, carboxyl
   and sulfhydryl groups [S36]. **Every published Au(III) demonstration
   therefore already contains an Au(I) reduction step.** The protein makes its
   own Au(I) in situ; we would hand it Au(I) directly.
2. **The mechanism is thiophilic, which suits Au(I).** The gold-reducing
   activity of this protein is attributed to a **cysteine-disulfide bridge
   electron shuttle** [S37]. Au(I) is a soft acid with a strong preference for
   sulfur donors, so a thiolate mechanism is if anything better matched to
   Au(I) than to Au(III).
3. **Au(I)-thiourea specifically is a known nanoparticle precursor.** The
   di(thiourea)gold(I) complex is published as a convenient precursor for
   preparing gold nanoparticles [S38], so the species itself is reducible to
   metal.

**A fourth finding supports the rate model rather than the chemistry:** the
same protein is reported to act as **nucleation seed sites** as well as a
reductant [S37]. That is the `k_nuc` term, and it is the only independent
support the Finke-Watzky structure has.

### What the search leaves standing, and it is not nothing

**Risk 1, the driving force is much lower.** Reduction potentials:

| Couple | E, V | Relative to ours |
|---|---|---|
| AuCl4- / Au, **as demonstrated** | ~ +1.00 | |
| **Au(CS(NH2)2)2+ / Au, ours** [S38] | **~ +0.38** | **0.6 V weaker** |
| Au(S2O3)2(3-) / Au, before elution | ~ +0.15 | |

The thiourea complex is about 0.6 V less oxidising than the chloride the
protein was tested on. The reaction stays thermodynamically downhill against a
dithionite or thiolate donor, but with far less margin, and rate constants
fitted at +1.00 V should not be assumed at +0.38 V.

**Risk 2, and this is the real one: ligand competition for the same
cysteines.** The mechanism needs gold to reach the protein's cysteine-disulfide
pair. Elution delivers the gold already wrapped in **1 M thiourea**, a strong
sulfur donor whose whole purpose two steps earlier was to **out-compete GolB's
Cys10 and Cys13**. Nothing guarantees it stops competing when it meets the
reductase.

**This is structurally the same problem as item 44**, where tetrathionate
blocks the capture cysteines. Same failure mode, different reagent, different
step, and equally unmodelled.

**Risk 3, concentration**, unchanged: 0.5-2 mM demonstrated against 0.054 uM
delivered.

**3. The concentration regime is four orders of magnitude apart.** The
published optimum is 0.5-2 mM. Capture delivers **0.054 uM**. Every rate
constant in the reduction block was fitted, loosely, to observations in the
millimolar regime and is being applied at sub-micromolar.

### One arithmetic caveat worth checking

The 0.5-2 mM optimum is quoted against the **stock** concentrations listed as
0-10 mM. The reaction dilutes each component tenfold into 1 mL, so the gold in
the tube may be 0.05-0.2 mM rather than 0.5-2 mM. Both readings leave the
published work short of electrons: dithionite at 4.6 uM in the tube supplies
about 9.2 uM of electrons against a demand of 150-600 uM even on the generous
reading. The "2000x short" figure in section 4.1 should be re-derived from the
tube concentrations rather than the stocks. **Nothing else depends on it**, so
it is recorded rather than acted on.

### What is needed

1. **Run the reduction on real eluate, not on HAuCl4.** This is the experiment
   already ranked first in section 10, with the substrate swapped. The
   literature says Au(I) is reducible in principle; what is untested is Au(I)
   **in 1 M thiourea**, which is a competition experiment, not a
   thermodynamics one.
1b. **Include a thiourea titration.** If activity falls as thiourea rises, risk
   2 is real and the fix is the same class as item 44: reduce the eluent
   concentration, or exchange the buffer before reduction. Note that the
   volume reduction of item 35 would dilute the thiourea as a side effect, so
   one process change may address both.
2. **Decide whether a mediator is required**, and if so whether the lysate
   supplies one or it must be added. Methyl viologen is cheap; the point is
   that the model claims it is unnecessary and has no basis for that.
3. **Write the reactions into the model**, not only the rate law. Section 2.3
   does this for the leach and section 6.3 did not.

**Related:** item 48 covers where the protein comes from; this item covers
what it does when it gets there. Neither is modelled. Item 35 covers the
concentration squeeze that gap 3 makes worse.

**Who decides:** wet lab, then the modelling team.

---


## 50. The reduction rate law was not standard, and it hid a conservation error

Found and closed 2026-08-16, from the question "is the min() standard?". It is
not, and replacing it exposed a second, unrelated fault.

### What was wrong

**The `min()` was an engineering shortcut wearing a kinetic coat.**

    v = min(k_donor*Au_aq*E_red, (k_nuc + k_grow*Au_s)*Au_aq)

The second branch is textbook: Finke-Watzky two-step nucleation and
autocatalytic growth [S39], `A -> B` then `A + B -> 2B`, giving
`-d[A]/dt = (k1 + k2[B])[A]`. That part was always right.

**Taking the minimum of two mechanisms is not a standard kinetic form.** It is
the classical rate-determining-step approximation hard-coded. Chemical kinetics
handles steps in series by series resistance, `1/v = 1/v1 + 1/v2`, or by
quasi-steady state on the intermediate. Neither produces a hard switch, and the
modern view is that several steps control the rate to varying degrees rather
than one owning it. Finke and Watzky themselves have no such branch: they ran
under constant H2 pressure and folded the reductant into k1 and k2.

**And the min() was concealing a conservation error.** `E_ox` was fixed at
`E_tot` while `E_red` also started at `E_tot`, so the model held **2x E_tot** of
protein at t = 0 and the oxidised pool never depleted, letting `E_red` grow
without bound. The error was **inert**, because `v_part` always won the minimum
and `E_red` therefore never entered `v` at all. It would have become live the
instant anyone made the rate depend on the donor.

### What the model does now

    v = (k_nuc + k_grow*Au_s) * Au_aq * (E_red/E_tot)
    E_ox = E_tot - E_red

Standard Finke-Watzky with the electron donor carried by **plain mass action**.
The factor equals 1 while the donor is in excess, so this reproduces textbook
F-W exactly in that limit, and it closes the reaction down smoothly when the
donor runs out instead of switching branches.

**Why the factor is explicit rather than assumed away.** F-W's excess condition
cannot simply be asserted across our operating range. At `nu` = 0.5:

| Gold at reduction | Donor consumed | Share of `E_tot` | Excess holds? |
|---|---|---|---|
| 0.054 uM, as delivered | 0.027 uM | **0.95%** | yes |
| 0.3 uM | 0.15 uM | 5.3% | marginal |
| 3.0 uM, **after a 10x concentration** | 1.5 uM | **52%** | **no** |
| 5.78 uM | 2.9 uM | 101% | no |

The regime item 35 recommends moving to is precisely the regime where the
assumption fails. Keeping the factor costs nothing and removes the trap.

### What it changed

**Nothing.** Every reduction number is identical to four decimal places,
because `min()` always selected `v_part` in this regime and the conservation
error never propagated. This was defensibility for free.

| Gold at reduction | Before | After |
|---|---|---|
| 0.054 uM | 0.0014 | 0.0014 |
| 1.0 uM | 0.029 | 0.029 |
| 3.0 uM | 0.993 | 0.993 |
| 5.78 uM | 1.000 | 1.000 |

`k_donor` is **retired**, in a `retired_k_donor` block with its literature
bracket kept. The branch it controlled no longer exists. It never affected a
result: `v_part` was smaller by about 57,000x at t = 0 and the vessel never
held enough gold to reverse that, which is what its old status "insensitive
given F-W" meant.

Pinned by `test_reduction_follows_standard_finke_watzky_with_the_donor_in_mass_action`
and `test_the_reduction_numbers_did_not_move_when_the_rate_law_was_standardised`.

### What is still not standard, and is deliberately left alone

The F-W lineage does not stop at two steps. The **three-step** form adds
bimolecular agglomeration `B + B -> C`, and the **four-step** form adds
autocatalytic agglomeration `B + C -> 1.5C` [S41]. Those steps are what set
the **particle size distribution**.

We do not model them, and the reason is that section 6.4 was descoped on the
same day: `eta_phys` = 1, so particle size no longer enters `eta_total`.
**If physical recovery is ever brought back into scope, the three- or four-step
mechanism is the route to predicting the particle size it depends on**, rather
than treating size as an unmeasured input. Recorded here so the link is not
lost.

**Who decides:** closed by the modelling team. No wet-lab input needed.

---


## 51. The source reaction was electron-starved, and `Rech` is a bought reagent

**Status: open.** Found 2026-08-17 by reading [S35]'s methods section directly
rather than its abstract and figures.

### What the recipe actually is

[S35], "Gold reduction and nanoparticle formation". Into a 1000 uL reaction:

| Component | Volume | Stock | Final |
|---|---|---|---|
| purified protein | 100 uL | — | — |
| HAuCl4 | 100 uL | 0-10 mM | 0-1000 uM |
| methyl viologen | 100 uL | 1 uM | **0.1 uM** |
| phosphate buffer pH 7.4 | 100 uL | 50 mM | 5 mM |
| double distilled water | 500 uL | — | — |
| sodium dithionite | 100 uL | 46 uM | **4.6 uM** |

The paper says the reaction is *activated* by adding the dithionite. It is the
trigger, not an optional extra.

### Finding 1: the electron ledger does not close

```
  dithionite supplied   4.6 uM x 2 e-   =     9.2 uM of electrons
  gold at 0.5 mM needs  500 uM x 3 e-   =  1500   uM of electrons
  gold at  10 mM needs 10000 uM x 3 e-  = 30000   uM of electrons
  ------------------------------------------------------------
  supply / demand                       = 0.6% down to 0.03%
```

This does not invalidate the paper. It explains it. [S35] measures a UV-Vis
peak at 520-560 nm and TEM images, and reports neither a conversion nor a
yield anywhere. On this ledger it could not have. A visible plasmon peak
appears when a small fraction of the gold forms particles.

**Consequence.** Point 2 of the carried-over list below says conversion has
never been quantified by anyone. This item supplies the arithmetic for why,
and closes off the hope that a number is hiding in the source. Every
`eta_reduce` this repository prints is a prediction of `src/sensitivity.py`,
calibrated against a colour change. It is not corroborated by any measurement,
and it must not be quoted as though it were.

### Finding 2: `Rech` was recorded as the wrong kind of thing

`params/recovery_chain.yaml` carried `Rech_0` with
`status: "lysis-dilution choice, not a literature value"`, and
`docs/REVIEW.md` 6.3 said the reductant is crude lysate that must not be
dialysed. Nothing in [S35] supports either. The protein is **purified first**
and the dithionite is **added afterwards**.

The old range [10, 1000] uM also excluded the only value the source used,
4.6 uM.

**Consequence.** `Rech` is a consumable to buy, dose, cost and risk-assess,
not something that arrives free with the cells. So is the methyl viologen. The
reagent arm of item 48 gains two purchased inputs it did not have.

### What was changed on 2026-08-17

- `Rech_0` now 4.6 uM, `source: S35`, range [4.6, 1000], with the old status
  and range kept under `superseded:`.
- New `reduction.mediator_0` = 0.1 uM records methyl viologen, and records
  that it appears in no equation in this model.
- `docs/REVIEW.md` 6.3 replaced the lysate paragraph with the recipe, the
  ledger, and the warning about quoting `eta_reduce`. Assumption row 18
  rewritten.

### What is still open

1. **Does the dithionite reduce the gold on its own?** It is a strong chemical
   reductant. [S35] ran a no-protein control and a boiled-protein control, so
   the question is answerable from that work, and this repository has not yet
   extracted the answer. Until it does, the split between enzymatic and
   chemical reduction is unknown.
2. **Is the mediator required?** If methyl viologen is needed, it belongs in
   the equations with a rate constant, and in the cost model. See item 49.
3. **What dose does our process need?** 4.6 uM was matched to a colour change,
   not to a conversion. Sizing it against our gold is unstarted.

**Who decides:** modelling extracts the control result from [S35] first; then
the team costs the two reagents.

---


## 52. Arm B modelled: the culture cannot reach the protein target

**Status: open.** Built 2026-08-17. `src/reductase.py`, `tests/test_reductase.py`,
and the `reagent_arm` block of `params/recovery_chain.yaml`.

Item 48 recorded that the reagent arm was drawn in the source document and
never modelled. This item is what happened when it was.

### The model

Biomass is a population, expression is per cell, and they meet in the
volumetric yield.

```
  dX/dt   = mu_eff * X * (1 - X/X_cap)          logistic, g dry weight/L
  mu_eff  = mu                    before induction
          = mu * (1 - burden)     after                 metabolic cost

  dm/dt   = alpha*N*I(t) - (delta_m + mu_eff)*m         I = 0 then 1
  dPc/dt  = beta*m       - (delta_c + mu_eff)*Pc

  C_prot  = Pc * X * cells_per_g / N_A * M_r            g/L
```

That is Part II's cascade with `k_sec` = 0, because the reductase stays
cytoplasmic instead of being displayed, coupled to a growth model that Part II
did not need.

Induction follows [S35]: 1 mM IPTG at OD600 0.8-1.0, so `X_ind` = 0.36 g/L.

### Finding 1: harvest is a window, and the timing does not wait on the construct

`alpha`, `N`, `beta` and `delta_c` for this construct are still null and stay
null; `golb_proxy_cascade` borrows GolB's values, clearly labelled. **The
timing answer survives that ignorance.** Those three constants enter dPc/dt
linearly, so scaling them scales the curve without moving its shape in time.
Scaling each by 0.1x to 10x moves the harvest time by 0.0 h.

The model has no cell death, no protease and no inclusion bodies, so protein
per litre rises to a plateau and stays there. **There is no late penalty in
this model**, which makes the operational answer an earliest-safe time:

| Time after induction | Fraction of plateau |
|---|---|
| 2 h | 45% |
| **4 h, the [S35] schedule** | **84%** |
| 5.5 h | 95% |
| 8 h | 97% |
| 12 h and beyond | 100% |

**Recommendation: lyse about 8 h after induction rather than 4.** It costs
nothing and recovers the last sixth. [S35]'s 4 h is not a mistake; that work
was making nanoparticles, not maximising a volumetric yield.

⚠ The absence of a late penalty is a property of the model, not of a culture.
Cell death, proteolysis, plasmid loss and inclusion-body formation all create
one, and none is represented. Item 32 records that a different protein in this
project does form inclusion bodies in *E. coli*. Until a real growth curve
exists, "later is never worse" must not be read as advice to leave it overnight.

### Finding 2: `burden` is the one constant worth measuring first

The contrast with finding 1 is the point. Timing is insensitive to four
unmeasured cascade constants and sensitive to one unmeasured growth constant:

| `burden` | 95% of plateau reached, after induction | Plateau |
|---|---|---|
| 0.0 | 3.9 h | 0.0040 g/L |
| 0.3 | 5.5 h | 0.0054 g/L |
| 0.7 | 12.7 h | 0.0097 g/L |

Slower growth raises the plateau, because growth dilution is a loss term in
dPc/dt, and delays it. **One growth curve with and without IPTG fixes this.**
It is the cheapest useful measurement in the arm.

### Finding 3, the one that matters: a 37x shortfall

Every reduction number in this repository is computed at `E_tot` from 0.2 g/L
of reductase. On the proxy cascade the culture plateaus at **0.0054 g/L**.

```
  target                     0.2    g/L
  culture plateau            0.0054 g/L
  ------------------------------------------
  shortfall                  37x, before any lysis loss
```

Lysis multiplies it rather than adding to it:

| `lysis_yield` | Lysate | Concentration needed |
|---|---|---|
| 1.0 | 0.0054 g/L | 37x |
| 0.5 | 0.0027 g/L | 74x |
| 0.3 | 0.0016 g/L | 123x |

**And reaching the target exactly is not enough.** Mixing only dilutes, so the
lysate must *exceed* 0.2 g/L for the mixed vessel to reach it;
`recovery_chain.lysate_mixing_ratio` raises on the equality. The real
requirement is 37x plus whatever headroom the mixing ratio needs, and item 48's
table shows a lysate only 1.05x above target costs 21x on the gold.

### What this does to the process design

There are now **two** concentration steps to build, not one, and they fight:

```
  the gold arm     concentrate the eluate     70-100x     item 35
  the reagent arm  concentrate the lysate     37-123x     this item
  and then they are mixed, which dilutes the gold again   item 48
```

Sizing any of the three alone will waste the other two.

### The lever with no unknown in it

`X_cap` multiplies the volumetric yield directly. A fed-batch at 20 g dry
weight per litre instead of 2 turns the 37x into 3.7x, and it needs no new
biology. **This is the cheapest route to closing the shortfall** and should be
priced before anyone tries to raise expression per cell.

### Finding 4: the target itself is loose, and relaxing it is free

`protein_target_g_per_L` = 0.2 is a design choice with nothing behind it. It
was a literal in the notebook before item 48. Asking what it actually buys,
at the 4.33 uM the gold arm must reach anyway:

| Protein | `E_tot` | Protein turnovers needed | `eta_reduce` at 4.33 uM |
|---|---|---|---|
| 0.2 g/L | 2.86 uM | 0.76 | 0.9996 |
| 0.1 g/L | 1.43 uM | 1.5 | 0.9984 |
| **0.05 g/L** | **0.71 uM** | **3.0** | **0.9776** |
| 0.04 g/L | 0.57 uM | 3.8 | 0.9446 |
| 0.02 g/L | 0.29 uM | 7.6 | 0.6830 |
| 0.0054 g/L, raw culture | 0.077 uM | 28 | 0.2422 |

**The target can drop from 0.2 to about 0.05 g/L for 2 points of `eta_reduce`.**
That takes the shortfall from 37x to **9.3x**, which is the difference between
a hard concentration step and an easy one.

Note what carries it: above 0.1 g/L each protein is used less than twice, but
at 0.05 g/L it must be recharged three times over. **The dithionite of item 51
becomes load-bearing exactly here** -- it is optional at the current gold, and
it is what makes a lower protein target possible.

Below about 0.04 g/L the yield falls away, and the raw culture at 0.0054 g/L
reaches only 24%. **So the shortfall cannot be argued away entirely, only
reduced fourfold.**

### What is still open

1. **`burden`**, from one growth curve. Ranks first on cost.
2. **`lysis_yield`**, one Bradford or A280 before and after the spin.
3. **`alpha`, `N`, `beta`, `delta_c`** for the real construct. These decide the
   absolute yield and, as shown above, not the timing.
4. **Whether to adopt 0.05 g/L as the target.** Modelling's recommendation is
   yes: it costs 2 points of `eta_reduce` and removes three quarters of the
   lysate concentration problem.

**Who decides:** modelling has done its part. Items 1 and 2 are wet lab.
Item 4 is a team decision on a design choice, and it should be taken before
any concentration hardware is specified.

---


---

## 68. The culture vessel is sized on a route the repository retired

Found 2026-08-21 while checking whether the `k_syn` caveat in `REVIEW.md` 2.1
was still true. It is true, and it is incomplete: the whole section runs on
constants the rest of the repository stopped using on 2026-08-11.

### The two routes

| Route | Where it lives | TetH in the culture | Culture per litre of conversion vessel |
|---|---|---|---|
| `k_syn` x `X` / (`k_deg` + `mu`) | the source document, transcribed into `enzyme_production` | 0.00475 uM | 9.1 L |
| `enzyme_capacity` via Part II's cascade | `params/leach.yaml`, and it is what the leach runs on | 0.3653 uM | 0.12 L |

The second is 77x the first. The arithmetic is the one already recorded under
`enzyme_capacity.Vmax`:

    23301 molecules/cell x 4.0 g/L x 2.36e12 cells/g / 6.022e23
        = 0.3653 umol/L of TetH
    x k_cat 220 /min = 80.36 umol/L/min, which is the Vmax in the file

So the second route is not a candidate. It is the live one, and it reproduces
a number the file already publishes.

### Why this is not a sourcing problem

`k_syn` is null and stays null; `params/leach.yaml` says plainly that
`enzyme_capacity` exists because no measurement can separate `k_syn` from
`k_cat`. Sourcing `k_syn` would not close the gap, because the gap is not in
`k_syn`. It is in what stands in for TetH:

1. The source document built 0.00475 uM from *Acidithiobacillus* and *Acidianus*
   specific activities, cross-species, and recorded it as
   `derived_from_proxies`.
2. `enzyme_capacity` builds 0.3653 uM from **GolB's 23,301 molecules per cell**,
   a labelled proxy for a displayed protein applied to a harvested cytoplasmic
   one.

Both are proxies. They disagree about TetH by almost two orders of magnitude,
and no measurement in this repository distinguishes them.

### What changes if the live route is right

The concentration step disappears. At 0.3653 uM the culture sits 8.5x **above**
the 0.043 uM the conversion vessel needs, so the harvest is diluted, not
concentrated, and section 2.1's headline of 9.1 L per litre becomes 0.12 L.
That is the difference between the culture vessel being the largest volume in
the process and being a rounding error against it.

### What does not change

Nothing downstream. The culture vessel sizes itself and then leaves the model:
it does not appear in the conversion or leach equations, and `E_stage2` = 0.043
is charged as a design variable either way. No published figure in `REVIEW.md`
outside 2.1 moves on this item.

### A second, smaller finding in the same section

`src/leach.py :: simulate` reads `k_syn` with `.get`, so a run with it null
does **not** raise. It returns an empty `stage1` dict and continues. The
culture vessel vanishes from the result silently. `params.values()` does raise
a `KeyError` on direct access, which is what `REVIEW.md` 2.1 was describing,
but that is the loader and not the model.

Left as it is deliberately: the leach vessel is the object of that function and
it does not need stage 1. Recorded so the behaviour is not mistaken for a
guard.

### Pinned by

`tests/test_leach.py :: test_two_enzyme_routes_disagree_77x`, which fails if
either route moves without the other. It asserts the ratio, not either value,
so it does not freeze a number this repository has not measured.

### Who decides

Wet lab, one measurement: TetH as a fraction of total protein on the induced
strain, by gel lane or activity assay. It settles which proxy to keep and it is
the same measurement item 67 asks for on the reductase.


## Carried over from Part III, still open

Already stated in `model.md`. Not new findings, listed so one file covers the
whole chain.

1. No demonstration exists that the construct reduces gold in a lysate.
2. Conversion has never been quantified by anyone, in any version of this
   chemistry.
3. Selectivity against Cu/Ag/Ni is unknown, and Part I now supplies a
   copper-bearing leachate directly into that unknown.
4. `k_nuc` and `k_grow` are the joint #1 driver of the pipeline and are
   calibrated against one qualitative observation.
5. `eta_wash` = 0.95 is the last unsourced parameter and is an upper bound.
6. Conditioning, the V1 to V2 transfer, is assumed lossless and unmodelled.

---

## 69. The capacity model counts only the engineered sites

Found 2026-08-24 while sourcing `k_on` for the capture time course in
`docs/RECOVERY.md`.

`q_max` is the display cascade's output: 23,301 GolB molecules per cell
becomes 0.0913 umol of gold per gram of dry cells. Every capture number in the
repository follows from it, including the 63x mismatch between what the leach
delivers and what capture can hold.

**The biosorption literature measures something else, and it is much larger.**

| | Basis | Capacity |
|---|---|---|
| `q_max`, in use | GolB sites from the display model | 0.0913 umol/g |
| `q_max.engineering_target` | every one of the cell's 1e5 anchors filled | 0.1961 umol/g |
| Tsuruta 2004, Qe | **wild-type** *P. maltophilia*, 50.5 uM Au(III), pH 3 | **329 umol/g** |
| Tsuruta 2004, Langmuir max | same | **992 umol/g** |

Those cells carry no engineered protein at all. The uptake is the cell wall's
own: amine, carboxyl and phosphate groups, plus reduction to metal on the wall
at that pH.

### Why this is not yet a correction

1. **Wrong gold species.** Au(III) chloride is a cation-forming, strongly
   oxidising species that plates onto biomass. Ours is Au(I) thiosulfate, an
   anionic complex, and a negatively charged cell surface repels it.
2. **Wrong pH.** pH 3.0 against our 9-10. Surface charge inverts across that
   range, and so does the argument above.
3. **Part of it is not sorption.** At pH 3 gold reduces on the cell wall, so
   the measurement includes metal the cells made rather than bound.

### What would settle it

One equilibrium point on **wild-type** *E. coli* in the actual leachate: cells
at a known dry weight, the real Au(I) thiosulfate feed, measure the gold left
in solution. If plain cells bind appreciably, `q_max` is the wrong model of
capture and the display density is not the lever the report says it is. If
they do not, the specific-site model stands and this item closes.

**Until then nothing changes.** The value in use is the conservative one, and
this item exists so that the assumption is visible rather than implicit.
`SOURCES.md` S57.

## 70. `k_ox` is labelled as gold re-oxidation and coded as enzyme re-oxidation

Found 2026-08-24 while writing `docs/RECOVERY.md` 4.2.

`params/recovery_chain.yaml :: reduction.k_ox` carries the meaning
*"Re-oxidation of Au(0) back to solution"*, value 0.02 h^-1, unsourced.

`src/sensitivity.py :: reduce_finke_watzky` applies it to the **reductase**:

    dE_red/dt = -nu*v + v_rech - k_ox*E_red
    dAu_s/dt  = +v                              <- no loss term at all

So in the code, gold once solid is never re-dissolved, and the term named for
that process is instead a slow leak of electrons off the charged enzyme.

**Which is right cannot be settled from this repository.** Both processes are
real: colloidal gold does re-oxidise in an aerated liquor, and a reduced
disulfide does lose electrons to oxygen. The two put the same constant in
different places and have different consequences.

- As coded, `k_ox` costs electrons and is covered by the dithionite budget.
- As labelled, it would cap `Au_s` at long times, which matters directly to
  the 96 h batch that item 4.6 of RECOVERY.md recommends.

**Nothing published moves because of this.** At the operating point the
electron budget is 10x oversupplied, so a leak at 0.02 h^-1 changes no
conversion in the table. It is filed because the label and the code disagree,
which is exactly the kind of drift the audit exists to catch.

**What to do.** Decide which process is meant, then either rename the
parameter or add the missing term to `dAu_s/dt`. If gold re-oxidation is
wanted it needs its own constant and a source; the 0.02 h^-1 has neither.
`docs/RECOVERY.md` 4.1 describes the symbol as the code uses it.


## 71. The Finke-Watzky constants may not transfer; the 23x alarm is narrowed, not confirmed

Raised 2026-08-24. **Updated the same day after chasing the full text.**

**The transferability problem is citable and stands.** [S64](SOURCES.md) fits
Finke-Watzky to gold nanoparticle formation and finds that **the initial
precursor concentration controls the fitted nucleation and growth constants**.
Both of this model's anchors, [S52](SOURCES.md), are millimolar-precursor fits
against a vessel running at 0.367 to 11 uM. The constants are orders of
magnitude, not values. Same defect as [S62](SOURCES.md) in elution.

### The second finding, and what chasing it settled

[S66](SOURCES.md) fits a modified Finke-Watzky scheme to Au(III) plus hydrazine
and reports `k1` = 1.188 M^-1 s^-1, `k3` = 3.87e-2 M^-1 s^-1 and
`k4` = 7.53e5 M^-2 s^-1. Which of these is this model's `k_grow` decides
whether the band floor is wrong by 23x.

**The full text could not be obtained.** The paper is paywalled and the one
repository copy, at Szeged, is marked archive-maintainer-only. What follows
comes from the abstract and the authors' own plain-language summary of it.

**Two readings, and the second is now the more likely.**

| Reading | `k_grow` equivalent | Effect on the band |
|---|---|---|
| `k3` is the autocatalytic growth term | 1.4e-4 uM^-1 h^-1 | floor 23x too high |
| **`k4` is the autocatalytic growth term** | **`k4` x [reductant]**: 0.027 to 2.7 uM^-1 h^-1 at 1e-5 to 1e-3 M hydrazine | **band is fine, and it brackets the 0.2 in use** |

**Why `k4` is the better reading.** The authors state that the particles
catalyse the reduction of **both** Au(III) and Au(I), so the scheme carries
**two** autocatalytic constants, and that **each elementary step transfers one
electron**. `k4` is third order, which is the shape an autocatalytic step takes
when the reductant appears explicitly beside the gold and the particle surface.
This model's growth term, `k_grow*Au_s*Au_aq*(E_red/E_tot)`, is that same shape
with the donor factored out into its own dimensionless ratio. `k3` is second
order and fits the Au(III)-on-particle step, which this project does not run:
elution delivers Au(I).

**Status: narrowed, still open.** Under the favoured reading nothing changes.
Under the other, the floor moves 23x and the robust design of
`docs/RECOVERY.md` 4.5 must be re-run with
`src/sensitivity.py :: reduce_worst_case` before its 98% is quoted again.

**What would close it.** One page of the [S66](SOURCES.md) full text: the
scheme with its constant numbering, and the hydrazine concentrations used. An
interlibrary request or an author email settles it. Until then the band is
unchanged, and this item is the record of why.

## 72. `k_rech` carried a unit that does not balance

Found 2026-08-24, explaining the donor equations for `docs/RECOVERY.md` 4.2.

`params/recovery_chain.yaml :: reduction.k_rech` was labelled **h^-1**. The
code computes

    v_rech = k_rech * E_ox * Rech / (1 + Au_aq/K_inh)

with `E_ox` and `Rech` both in uM. For `v_rech` to be a uM/h rate, as every
other term in `dE_red/dt` is, `k_rech` must be **uM^-1 h^-1**. At the labelled
unit the equation would produce uM^2/h and could not be added to the others.

**No number moves.** The code multiplies the value as given; only the label was
wrong. The unit is corrected and the value, 0.1, is unchanged.

**This is the third label defect found in the same file**, after `k_ox`
(item 70) and `nu`, whose unit read "mol e- per mol Au" against a value that is
protein per gold. Two of the three were caught only because the equations were
being written out for a reader. **The parameter file has no unit check.**
`docs/check_docs.py` verifies links, tiers and regeneration; adding a
dimensional check on the terms of each equation would have caught all three.

**Suggested fix, not yet done.** A test that asserts the units of every term in
`reduce_finke_watzky` agree, using the `unit` fields as declared. It is a
half-day and it would make this class of drift impossible.

## 73. `lambda_D` does not balance dimensionally, and it is in a source document

Found 2026-08-24, running a dimensional check over every equation in the chain
after item 72. **It is the only failure out of nineteen terms checked.**

`docs/source/model.md` section 2 defines the gold-damage death term as

    dX/dt = mu*X*(1 - X/X_max) - m*X - lambda_D*D*X
    dD/dt = k_dam*G - k_rep*D          lambda_D = mu*k_rep0/A_tox

Take the units as the parameter file declares them. `k_dam` is h^-1 and `G` is
uM, so `D` is **uM**. For `lambda_D*D*X` to be a biomass rate, g/L/h,
`lambda_D` must be **uM^-1 h^-1**. But

    mu*k_rep0/A_tox = h^-1 * h^-1 / uM = uM^-1 h^-2

which is **one power of time too many**. The term as written is g/L/h^2.
Dropping `mu` gives `k_rep0/A_tox` = uM^-1 h^-1, which balances.

**THE SOURCE DOCUMENT IS NOT EDITED.** This is recorded and left standing, per
the repository rule. `docs/RECOVERY.md` 2.4 and
`docs/make_recovery_figures.py` both reproduce the formula as written, which is
correct: they must show the model as it is defined.

### What it costs, numerically

`mu` = 1.2 h^-1, so the formula multiplies lethality by 1.2 against the
dimensionally consistent version. Running the capture model both ways:

| `lambda_D` | value | peak biomass | X at 24 h | peak bound gold |
|---|---|---|---|---|
| `mu*k_rep0/A_tox`, as written | 4.80e-4 | 4.668 g/L at 8.5 h | 4.478 | 0.4248 uM |
| `k_rep0/A_tox`, dimensional | 4.00e-4 | 4.721 g/L at 8.6 h | 4.565 | 0.4295 uM |

**1.1% on the gold and 2% on the biomass.** Nothing published changes and no
conclusion moves; the harvest time stays 8.5 h.

**Which is intended cannot be settled here.** Including `mu` may be deliberate,
scaling lethality to how fast the culture is dividing, in which case the
formula needs a second time constant to stay dimensional. Only the document's
author can say. Until then the model runs the formula as written and the
1.2x is documented here.

**Related:** items 70 and 72 are the same class of defect in the parameter
labels. This one is in an equation, and it is the reason the unit check
proposed in item 72 should cover equations and not only parameters.

## 74. The donor sub-system can be replaced by one inequality

Found 2026-08-24, asking whether `v_rech` could be simplified.

The reduction model carries five states. Two of them, `E_red` and `Rech`, exist
only because the reductant is not in excess. **Both can be removed without
changing an answer**, and the tests now pin that.

### 1. The inhibition factor is inert

`v_rech` divides by `1 + Au_aq/K_inh`, competitive inhibition by dissolved
gold. `K_inh` = 500 uM, and the highest concentration this project designs for
is 11 uM, where the factor is **1.022**. Setting `K_inh` to infinity moves
conversion by **less than 0.01 of a point** at 0.367, 1.5, 3, 11 and 120 uM.
The form is standard -- it is the `1 + [I]/K_i` of Cheng and Prusoff (1973),
*Biochem Pharmacol* 22:3099 -- and standard practice is to drop it when the
inhibitor sits far below `K_i`, which it does here by a factor of 45.

### 2. The whole donor system reduces to the electron cap

Recharging reaches 14 uM/h against a gold demand of 5.5 uM over the entire
96 h batch, so `E_red/E_tot` stays at 1 until the dithionite is spent, and the
reaction then **stops** rather than slows. Plain two-state Finke-Watzky, capped
at `2*E_tot + 2*Rech_0` of gold, reproduces the five-state integration:

| Charged | Batch | Five states | Two states + cap |
|---|---|---|---|
| 0.367 uM | 24 h | 0.325 % | 0.328 % |
| 3 uM | 24 h | 99.25 % | 99.34 % |
| 11 uM, 50 % seed | 96 h | 100 % | 100 % |
| 11 uM, 50 % seed, `k_grow` floor | 96 h | 98.06 % | 98.15 % |
| 120 uM | 96 h | 88.04 % | 88.10 % |
| 200 uM | 96 h | 52.84 % | 52.86 % |

**Worst disagreement 0.47 of a point**, across three orders of magnitude of
charge, with and without a seed, at both ends of the `k_grow` band, and with
raw-lysate protein.

### What to do with that

**Not to delete the five-state code.** It is validated, it is what
`docs/source/model.md` specifies, and the cost of running it is trivial.

**But the reduced form is the honest explanation**, and `docs/RECOVERY.md`
already tells the story in that order: the electron budget is checked first, then whether the reaction starts in time. This item records that
the two-question structure is not a narrative device -- it is a numerically
exact reduction of the model.

**Two tests now hold it**, `test_the_inhibition_term_in_v_rech_never_fires` and
`test_the_donor_system_reduces_to_an_electron_cap`. If a future change makes
the donor equations matter, they fail, and that failure is informative.

**When the reduction would break.** Gold above about 100 uM, where the budget
binds during the run rather than at the end; or `k_rech` two orders of
magnitude lower, where recharging becomes slow enough to throttle the rate.
Neither is in any design here.

## 75. The source document's citation trail is in a companion nobody has

Found 2026-08-24, tracing where `v_rech` came from.

`docs/source/model.md` contains **no citations**. Its header says the citations
live in a *"build plan v2.5 (decisions, audit trail, citations)"*, and that
document is **not in this repository**. Every equation in the source is
therefore uncited by construction, including:

    v_rech = k_rech * E_o * R / (1 + A/K_i)          section 4
    lambda_D = mu * k_rep0 / A_tox                    section 2, see item 73
    v = min(v_red, v_FW)                              section 4, replaced, item 50

**What this repository has done about it.** `docs/SOURCES.md` now carries 70
entries built by working backwards from the values: `phi` to [S59], `k_on` to
[S57], `nu` to [S63], the rate law to [S39] and [S67], the electron count to
[S65], the algebraic form of the `v_rech` denominator to [S70]. That is
reconstruction, not the original trail.

**Why it matters.** Where reconstruction found the origin, it also found the
qualification -- [S59]'s 87% is in a paywalled body, [S63]'s disulfide is
"speculated", [S66]'s mapping is unresolved. A citation trail that existed
would have carried those with the numbers from the start.

**Ask for the build plan.** One document closes the largest remaining gap in
`SOURCES.md`. If it no longer exists, say so here and the reconstruction
becomes the record.

## 76. `v_rech` verified against the literature: structure right, order wrong, nothing moves

Found 2026-08-24, checking `v_rech` against how redox enzymes are modelled
elsewhere. Four findings, in descending order of how much they matter.

**1. The structure is standard.** [S71.1](SOURCES.md) analyses a flavoprotein
oxidoreductase as two half-reactions with their own rate constants, then shows
they account for overall turnover by ping-pong Bi-Bi. `E_red` spent by gold and
`E_ox` recharged by donor is that same treatment. Not an invention.

**2. The order in dithionite is wrong.** [S71.3](SOURCES.md), Lambeth and
Palmer 1973, established that dithionite reduces proteins through the **SO2
radical**, `S2O4^2- <=> 2 SO2^.-`, so observed rates go as
**sqrt(dithionite)**. [S71.2](SOURCES.md) confirms it for a copper nitrite
reductase 29 years later. This model uses `Rech` to the first power.

**Tested, and it changes nothing.** Exponent set to 0.5, constant rescaled to
match at `t` = 0: conversion moves by at most **0.001 of a point** at 0.367, 3,
11, 60, 120 and 200 uM. The order is invisible because recharging is not close
to limiting; only the electron count binds, which is item 74.

**3. `k_rech` is 110,000x below a measured protein-dithionite rate.**
[S71.2](SOURCES.md) reports 3.06e6 M^-1 s^-1, which is 1.1e4 uM^-1 h^-1 here,
against 0.1 in use. Whatever else is uncertain, this model does not overstate
the recharge, and the "insensitive" label is justified from the other side too.

**4. The gold inhibition term has no support found.** No paper located models
dissolved metal forming a dead-end complex with the *oxidised* enzyme. It is an
assumption of `docs/source/model.md`, uncited like the rest of that file
(item 75), and it never fires here (item 74). If anyone wants to keep it, it
needs a source; if not, dropping it removes a parameter.

**Net.** One structural correction is available and worth 0.001 of a point.
The recommendation is to leave the equation as written, record the
approximation, and spend nothing on it. **The reason it survives scrutiny is
not that it is exactly right -- it is that this vessel is never donor-limited
in rate, only in total electrons.**

## 77. Reduction timing symbols renamed, and the reported time moved from 50 % to 95 %

**Opened 2026-08-24. Done, recorded.**

**Two names changed, no arithmetic changed.**

| Old | New | Why |
|---|---|---|
| `t_cross` | `t_ind` | "Induction time" is the Finke-Watzky term for exactly this quantity. `t_cross` was invented here. |
| `t_50` | `t_1/2` | `t_50` reads as a percentage in documents that write percentages with a `%`. |

Renamed in `docs/RECOVERY.md`, `docs/EQUATIONS.md`, `docs/REVIEW.md`,
`src/sensitivity.py`, `tests/test_sensitivity.py` and
`params/recovery_chain.yaml`. **Not renamed in Tier 2 files**, per AGENTS.md
section 11: items above this one and the `[S67]` entry in `SOURCES.md` keep
`t_cross`, and it means `t_ind`.

**The general form replaces the single case.** Inverting the closed form at
`Au_s` = `f*Au_aq(0)` gives the time to any conversion `f`:

    t_f = ln((1 + f*R)/(1 - f)) / (k_nuc + k_grow*Au_aq(0)),
    R   = k_grow*Au_aq(0)/k_nuc

`t_1/2` and `t_95` are that expression at `f` = 0.5 and 0.95. `R` = 1468 at the
delivered gold, so the prefactor is `t_ind` to within 0.1 %.

**`docs/RECOVERY.md` 4.3 now reports `t_95`, not `t_1/2`.** Nothing in this
project accepts half the gold, so the half-time understated the vessel the
design needs.

| Charged | `t_ind` | `t_1/2` (was reported) | `t_95` (now reported) |
|---|---|---|---|
| 0.367 uM, as delivered | 13.6 h | 99 h | **139 h** |
| 1.5 uM | 3.3 h | 29 h | **39 h** |
| 3.0 uM | 1.7 h | 16 h | **21 h** |

**The conclusion is unchanged and slightly stronger.** 3 uM still clears a 24 h
batch, now with 3 h of margin rather than 8 h. Below about 3 uM reduction still
does not start.

**Checked three ways.** The approximate form, the exact form, and a direct
integration of `dAu_s/dt = (k_nuc + k_grow*Au_s)(Au_aq(0) - Au_s)` stopped at
the `Au_s` = `f*Au_aq(0)` event agree to 0.1 h at 0.367, 1.5, 3.0 and 11 uM,
for both `f` = 0.5 and `f` = 0.95. Pinned by
`test_the_time_to_a_given_conversion_matches_the_ode`.

## 78. The Finke-Watzky sources point at the wrong issue number

Found 2026-08-24 while verifying the provenance of `k_nuc` and `k_grow`.

[S51](SOURCES.md), [S52](SOURCES.md) and [S53](SOURCES.md) each close with
**"Used in: reduction.k_nuc, reduction.k_grow; ISSUES.md item 67."** Item 67 is
*The reductase is on pET-24(+), not the backbone the proxy assumed*. It is
about plasmid backbones and names neither constant.

**The item that carries these constants is 71**, transferability of the
Finke-Watzky fits, with 35 and 64 for what the constants imply.

**Not corrected in place.** `SOURCES.md` is Tier 2 by AGENTS.md section 11:
append and supersede, never rewrite. This entry is the supersession. A reader
following the pointer in S51 to S53 should read item 71.

**Nothing numeric moves.** The pointer is wrong; every value, band and caveat
in those three entries stands as written.

## 79. `k_nuc` and `k_grow` sourced again, and what the second search found

Searched 2026-08-24, on the question of what actually backs the two constants
that jointly drive the whole chain.

**Three things changed, none of them a number.**

**1. The ceiling now traces to primary data.** [S52](SOURCES.md)'s
ascorbate-PVP fit is not an independent measurement. Watzky and Finke digitised
the curves of [S72](SOURCES.md), Zhou et al. 2013, and refitted them. The
provenance of `k_grow`'s ceiling is one experiment, refitted twice, and it is
now cited as such.

**2. The gap in that ceiling is confirmed, not closed.** The refit reports its
constants for a normalised `[A]0` = 1.00, and neither paper's abstract names
the HAuCl4 concentration. **The 0.4 mM used to convert `k2` into uM^-1 h^-1 is
still this project's own assumption, and the ceiling is linear in it.** The
2013 full text is paywalled at Elsevier. Anyone with institutional access can
settle this in ten minutes, and it is the single cheapest improvement available
to the reduction block.

**3. Two candidate sources were checked and rejected**, recorded in
[S73](SOURCES.md) so nobody spends the search again. One paper's title promises
Finke-Watzky constants for gold and the paper reports none. The other is a
purified enzyme making gold, but its published rate constants describe the
finished particles degrading dyes, not the enzyme reducing gold.

**The standing position, unchanged.** No Finke-Watzky fit exists for
protein-mediated gold reduction, in two searches nine days apart.
[S53](SOURCES.md), GolR refitted through this repository's own model, is the
only enzyme anchor and it sits at the band floor, sixty times below the value
in use.

**Two findings that support the model rather than the constants.**
[S72](SOURCES.md) reports that the biogenic route nucleates **heterogeneously**
where the chemical route does not, which is an independent argument for seeding
(item 64), and that **crystallisation, not the redox chemistry, is
rate-determining** -- which is where this model already puts the limit, since
`E_red/E_tot` holds at 0.996 and only the particle terms bind (item 74).

**What would actually calibrate these two.** One turbidity or plasmon time
course of this project's own reductase with its own gold, fitted to
Finke-Watzky. Everything above is transfer with an argument attached. It is the
experiment named in `docs/RECOVERY.md` 4.6.
## 80. A better parameterisation for reduction exists, and it removes the concentration cliff

Raised 2026-08-24, after items 71 and 79 established that neither Finke-Watzky
constant can be sourced for this system. **This is a proposal, not a change.
Nothing in the code or the parameter files has moved.**

### The problem in one line

`docs/RECOVERY.md` 4.3 predicts that reduction fails below about 3 uM. That
prediction rests entirely on `k_grow`, which is **not measured, not measurable
from any published source, and spans a 656-fold band**.

### The alternative

[S74](SOURCES.md) reports Michaelis-Menten constants for an enzyme reducing
gold, assayed by NADPH oxidation at 340 nm. Converted to this repository's
units:

| Enzyme | `k_cat` | `K_M` | `k_cat/K_M` |
|---|---|---|---|
| WT MerA | 97 h^-1 | 290 uM | 0.335 uM^-1 h^-1 |
| G415I variant | 245 h^-1 | 50 uM | 4.90 uM^-1 h^-1 |

`K_M` is 50-290 uM and this vessel runs at 0.367-11 uM, so the enzyme is far
below saturation and the rate law is first order in gold:

    v      = k_cat * E_tot * Au / (K_M + Au)  ~  (k_cat/K_M) * E_tot * Au
    t_95   = ln(20) / ((k_cat/K_M) * E_tot)

### The two models disagree completely

At `E_tot` = 2.857 uM, time to 95 % conversion:

| Gold charged | Finke-Watzky, in use | Michaelis-Menten, WT MerA | MM, G415I |
|---|---|---|---|
| 0.367 uM | 139 h | **3.1 h** | 0.21 h |
| 3.0 uM | 21 h | **3.1 h** | 0.21 h |
| 11 uM | 6.2 h | **3.1 h** | 0.23 h |

**`t_95` does not depend on the gold charged** under Michaelis-Menten, because
below `K_M` the reaction is first order. **The concentration cliff is a
property of the Finke-Watzky parameterisation, not an observed fact.**

### Which is right

Probably neither alone. They describe **different halves of the same process**:

- Michaelis-Menten describes the **electron transfer**, and its constants are
  measured.
- Finke-Watzky describes the **particle formation**, and its constants are not.
- [S72](SOURCES.md) states that of the two, **crystallisation is
  rate-determining**, which argues the Michaelis-Menten rate is an upper bound.

**The proposal is therefore a two-limit model**: run both, report the slower,
and let the electron cap of item 74 stand as the third limit. That is honest
about which half is measured and which is transferred, and it makes the
concentration recommendation fall out of evidence rather than out of `k_grow`.

### What it costs and what it buys

Costs: one new rate law in `src/sensitivity.py`, two parameters in
`params/recovery_chain.yaml`, a rewrite of `docs/RECOVERY.md` 4.3 to 4.5, and
re-derivation of the pinned reduction tests.

Buys: **the headline parameter becomes measurable in this team's own lab.**
NADPH oxidation at 340 nm, epsilon = 6220 M^-1 cm^-1, initial velocity against
a gold series, nonlinear fit. A plate reader and an afternoon. Two literature
searches have failed to source `k_grow`; `k_cat` and `K_M` do not need
sourcing, they need an assay.

### Four caveats, all real

1. MerA is not this project's reductase.
2. The constants are for Au(III); elution delivers Au(I) thiourea.
3. The assay measures NADPH consumption, so it bounds the redox step only.
4. Gold was 10-1000 uM in the assay, above this vessel's range, so the same
   extrapolation warning as item 71 applies -- in the other direction.

### Decision needed

**This is the team's call, not a unilateral change.** The options are: keep
Finke-Watzky and label the cliff as parameter-dependent; switch to
Michaelis-Menten and lose the cliff; or build the two-limit model and report
the slower. **Recommendation: the two-limit model**, because it is the only one
of the three that cannot be accused of choosing the answer through the
parameterisation.

## 81. The Finke-Watzky constants can now be fitted, `src/fit_fw.py`

Written 2026-08-24, in answer to items 71, 79 and 80: two literature searches
have failed to source `k_nuc` and `k_grow`, so the remaining route is to
measure them here.

**What the module does.** `fit_finke_watzky(t_h, signal, Au_aq0)` fits the
closed form of `docs/RECOVERY.md` 4.3 to one time course and returns both
constants with one-sigma errors. `t_to_conversion(Au_aq0, k_nuc, k_grow, f)`
turns a fitted pair into the number the vessel is sized on.

**What the wet lab has to produce.** Absorbance at the plasmon peak, about
520-530 nm, against time, at a gold concentration in this vessel's range and
with the reductant in excess. **The scale divides out**, so arbitrary units are
a valid input and no extinction coefficient is needed. Gold remaining in
solution by ICP-MS works equally well, with `dissolved=True`.

**Sampling matters more than precision.** All the information about `k_nuc` is
in the induction period. Every 5 min for the first 2 h, every 30 min after, and
run to a clear plateau; the plateau sets the scale.

**Run it at three gold concentrations, not one.** One curve returns two
numbers. Three curves test whether they are constants at all, which is exactly
the failure [S64](SOURCES.md) reports and item 71 records. If the fitted pair
drifts with the gold charged, the constants are effective values for one
condition and the band stays.

**Pinned by six tests** in `tests/test_fit_fw.py`: recovery of known constants
across three decades of gold, invariance to the absorbance scale, the dissolved
gold path, survival of 2 % noise, agreement between `t_to_conversion` and the
curve it came from, and refusal of data that cannot be fitted.

## 82. `k_nuc` is enzyme-scaled and `k_grow` recentred; the concentration cliff is gone

Applied 2026-08-24 on the team's instruction, following items 79, 80 and 81.

| Constant | Was | Now | Basis |
|---|---|---|---|
| `k_nuc` | 5.0e-5 /h | **0.96 /h** | `(k_cat/K_M)*E_tot` = 0.335*2.857, wild-type MerA, [S74](SOURCES.md) |
| `k_grow` | 0.2 uM^-1 h^-1 | **0.082** | log-centre of the anchored band; the 2.4x fast-side bias declared on 2026-08-21 is closed |
| `k_nuc` band | 5.0e-6 to 8.6e-4 | **5.0e-5 to 14.0** | floor = the retired chemical value, kept as a pessimistic bound; ceiling = the engineered MerA variant |

**The argument for `k_nuc`.** 5.0e-5 was a CHEMICAL nucleation rate, transferred
from ascorbate and plant-extract fits and scaled down for reductant. In this
vessel nucleation is not spontaneous chemistry -- the reductase performs it --
so the rate belongs to the enzyme.

**What moved.**

| | Before | After |
|---|---|---|
| `t_95` at the delivered 0.367 uM | 139 h | **3.1 h** |
| Conversion at 24 h, as delivered | 0.3 % | **100 %** |
| Concentration step | mandatory, 8x to 10x | **not needed for the rate** |
| Seeding | the cheapest lever | **inert** |
| `k_grow` across its whole 656-fold band | 0.1 % to 99.9 % | **100 % throughout** |
| Binding constraint | the induction period | **the electron ceiling, 105.7 uM** |

`R` = `k_grow*Au_aq/k_nuc` is now 0.03 to 0.94 across the operating range.
**Below `R` = 1 nucleation never hands over to growth**, so there is no
induction period, `t_ind` is not the vessel's timescale, and `t_f` collapses to
`ln(20)/k_nuc` = 3.1 h.

**UPDATE, same day: the robust-design section was deleted from
`docs/RECOVERY.md` on the team's instruction.** Its arithmetic is kept here.
The robust design was unchanged by the recentring, because the worst
corner is still the retired chemical `k_nuc` kept as the band floor: 30x, 50 %
seed, 96 h and 50 uM dithionite still clears 98 %. The 10x row moved from 25 %
to 28 % with the floor.

**Eight tests re-derived**, not deleted, so the size of the change stays in the
history: the cliff test now asserts there is no cliff, the concentration test
that concentration is not needed for the rate, the three seeding tests that
seeding is inert, the landmarks that all five are complete conversion, the band
test that the k_grow band no longer spans the stage, and the `t_f` test that the
`t_ind` shortcut may no longer be used.

**The risk that remains is one-sided.** A tenfold drop in `k_nuc` costs 6
points. A hundredfold drop brings the cliff back. `docs/RECOVERY.md` 4.6 now
carries the assay that measures it, and `src/fit_fw.py` fits it.

**Still carrying the old numbers:** `docs/REVIEW.md`, `docs/MASTER.md`,
`docs/EQUATIONS.md` and `docs/WIKI_CONTENT.md`. They are Tier 3, so those are
defects, not history. `docs/RECOVERY.md` and the reduction tests are current.

**Two things left orphaned by that deletion**, recorded so they are not lost:
`params/recovery_chain.yaml :: reagent_arm.robust_design` (30x, 50 % seed, 96 h)
is no longer cited by any document, and `figR7_kgrow_robustness.png` is no
longer referenced. Both still build and both still hold at the band floor.

## 83. The four synthesis documents swept onto the current recovery model

Done 2026-08-24, closing the stale-number defect item 82 recorded.

**`docs/REVIEW.md`.** Section 6 was replaced wholesale by the current
`docs/RECOVERY.md`, flattened one heading level, figures included: it now
carries the capture derivation, the elution PSO derivation, the reduction
chemistry and rate law, `t_f`, the constants' bands and the assay. Section 8
was recomputed. Four stale claims elsewhere were repaired: the process diagram
no longer seeds the reduction vessel, `F` and `f_seed` left the symbol table,
assumption 24 is retired, and "what to measure" item 1 is now the plasmon time
course with its sampling schedule. **`docs/RECOVERY.md` is the source for
REVIEW section 6 from now on; edit it there.**

**`docs/EQUATIONS.md`.** The reduction block keeps `t_ind` and `t_f` and states
that `R` < 1 here, so there is no induction period. The seeding paragraph is
marked inert. The donor factor reads 0.996, not 1, and `Rech_0` reads 50 uM.

**`docs/MASTER.md`.** The squeeze section now says capture squeezes the chain,
not reduction; 9b is rewritten around the electron budget, the enzyme-set rate
and the harvest time; the final-number table is recomputed at the current
`q_max` and drops the retired physical-recovery column; the losses table drops
"grow bigger particles"; the closing three replace seeding with the reduction
constants. A dated row was ADDED to the decision log rather than rewriting the
2026-08-20 seeding row, which is history.

**`docs/WIKI_CONTENT.md`.** Cells c5, c6 and c9 carried retired numbers: 2,700
sites, a 0.05 uM ceiling, and a reduction that "needs gold above 3 uM to start".
All three now match the model.

**Still stale, and deliberately left:** `AGENTS.md` quotes `q_max` = 0.0108 in
three places as an EXAMPLE of a retired value, and `docs/MASTER.md` line 988
quotes 2,749 sites in the same way. Both read correctly in context.

`REVIEW.docx` rebuilt. 132 tests pass; `check_docs` reports 0 broken links and
0 tier problems.


## 84. Full reduction ranges restore the missing uncertainty

2026-09-06. Supersedes the general conclusions in items 82 and 83, while
preserving their nominal parameter choice. The tornado in
`docs/make_analysis_figures.py` sampled nucleation only from the reference
value divided by ten to the reference value multiplied by ten. The actual
YAML range is 5.0e-5 to 14.0 h^-1. Keeping the slow end out of the chart
concealed the dominant uncertainty. Both kinetic ranges now come from YAML.
The recovery figure evaluates their full rectangular grid at the report feed.
It is a scenario envelope, not a probability distribution or a confidence interval.

The reference 0.96 h^-1 is transferred from MerA electron-transfer kinetics,
not measured nanoparticle nucleation by this project's protein. Equal units
are necessary, not sufficient, for this transfer. No defensible replacement
measurement is available, so the nominal value is retained as a labelled
scenario. Complete conversion and the absence of a concentration threshold
are conditional on it. The low kinetic corner predicts incomplete reduction.
A zero-activity scenario remains possible outside the selected proxy range.

`test_reduction_uncertainty_includes_the_declared_slow_scenario` prevents the
narrow reference sweep from being confused with coverage of the declared range.
`src/recovery_audit.py` recomputes display capacity through Joint 2 and uses
actual equilibrium-bound gold, rather than all available sites, for elution.
The reference assumes equal liquid volumes and a separately supplied protein
target. It does not establish that the culture can supply that target.

## 85. Fitting must not manufacture full conversion

2026-09-06. Supersedes item 81's calibration advice. `fit_finke_watzky` divided
all observations by their maximum, including dissolved gold measurements.
Consequently an experiment stopped during its rise was treated as complete.
The dissolved path also subtracted the first observation instead of the known
initial charge, losing the initial balance when the first sample was delayed.

The fitter now accepts absolute metal concentrations, absolute dissolved
gold, or an explicitly calibrated optical signal with a blank. It never uses
the observed maximum as a calibration. A synthetic partial time course checks
all three paths against known constants. Finite, ordered times are required.
The old scale-invariance test now supplies its calibration explicitly.

An optical plateau alone is not proof of conversion. Particle size, shape,
aggregation and medium alter extinction: see the newly verified S75.
Dissolved-gold disappearance alone also cannot distinguish metal formation
from adsorption or precipitation. The proposed experiment must close a gold
mass balance and independently establish the metallic product. Numerical
parameter recovery is verification of the fitter, not validation of chemistry.

## 86. Passing tests had missed executable and numerical defects

2026-09-06. The baseline suite passed all 132 tests. Nevertheless,
`sensitivity.run` requested `eta_phys` after `chain_eta_total` had removed it.
The runner now returns only the three in-scope stages and their product.
Ranks used sequential positions for equal values; they now use average ranks.
Constant-output PRCC is undefined and returns NaN rather than a fabricated
association. PRCC still requires checking monotonicity and sampling assumptions.

The Langmuir smaller root lost precision through subtraction at very dilute
feed. A rationalised root preserves the mass balance, and zero-feed efficiency
uses a masked division. Negative/nonfinite equilibrium inputs are rejected.
Zero protein gives zero protein-mediated reduction; failed integrations raise.
Regression tests in `tests/test_recovery_audit.py` exercise these paths.

## 87. Logistic cultures cannot dilute protein at their maximum growth rate

2026-09-06. Supersedes the numerical yield and harvest conclusions in items
52 and 67. Biomass obeys logistic growth but the per-cell cascade previously
used maximum specific growth as dilution, even at stationary biomass. Product
rule differentiation of total molecules shows a fictitious loss. Dilution is
now the actual specific growth, mu_eff*(1-X/X_cap), in both per-cell equations.

An independent constant-biomass analytic cascade test verifies the correction.
At the existing proxy, the computed protein at 24 h changes from approximately
0.0675 g/L to 0.2733 g/L. These are model outputs, not measurements. The old
3.0-fold deficit and eight-hour recommendation no longer follow. Old tests
that pinned those conclusions have been superseded with balance, amplitude,
decay and mixing tests; their failed output was inspected before rewriting.

The correction exposes another limit: constitutive production continues after
nutrients stop biomass growth. At zero protein decay it has no finite protein
plateau, and the upper expression proxy can exceed the available dry mass.
The lump's old physical-ceiling calibration therefore does not transfer to
this corrected equation. Do not claim a yield or harvest optimum until active
soluble protein, stationary-phase expression and decay are measured. The
unmeasured calibration stays unmeasured; no artificial capacity was invented.

## 88. Mechanistic language and units outran the implementation

2026-09-06. Supersedes item 73's instruction to repeat an invalid equation in
synthesis documents. Source documents remain untouched. The dimensionally
invalid mu*k_rep0/A_tox death coefficient cannot be repaired uniquely by unit
analysis; the replacement coefficient is null, with units uM^-1 h^-1.
The damage-based capture harvest recommendation and its plots are withdrawn
from the current report. Equilibrium capture does not use that coefficient.

PSO is an empirical candidate, not evidence that a two-body ligand exchange
makes desorption second order in loaded sites. A reactant held in excess does
not by itself imply the square of the remaining loaded sites. Both candidate
laws must be fitted at the actual loading and matrix; S62 supports the warning
about transferring PSO constants, not the mechanistic claim.

`k_rech` is uM^-1 h^-1, not h^-1. The report omitted the inhibition denominator
that the code retains. `k_ox` oxidises the protein pool, not metallic gold.
These descriptions now match the implementation. The cysteine-disulfide
cycle is a proposed mechanism, not demonstrated stoichiometry for this chain.

The fixed effective FW rate constants do not rescale with protein abundance.
Consequently protein sweeps under those constants cannot validate the claim
that protein quantity is irrelevant, or implement the enzyme-scaled argument
used to choose the reference. An explicit protein-dependent model needs its
own data. No new kinetic law or unsupported measurement was silently inserted.

## 89. What the recovery model can demonstrate to iGEM judges

2026-09-06. Official 2026 Best Model guidance assesses the computational
approach, usefulness to understanding/design, relevant data, and example value.
The correct evidence is a traceable conditional model, verification, honest
limitations and a documented design-to-measurement loop. A passing test suite
cannot guarantee a medal or experimental accuracy.

The revised `RECOVERY.md` is the technical review and `WIKI_RECOVERY.md` is a
recovery-only proposed narrative with captions and validation priorities.
Generated graphs distinguish amount from percentage and kinetics from a
confidence interval. No wet-lab results were supplied to fit or validate the
recovery chemistry. The initial leach and expression documents were not changed.


### Verification of items 84–89, 2026-09-06

Final suite: **140 passed in 49.84 s**. All five YAML files parsed. Every
notebook code cell executed successfully; the final reference metal amount is
0.3653789222351048 µmol per initial litre, recomputed through the chain.
`docs/check_docs.py --regen` passed: zero fixable broken links, zero tier
problems and zero drift among the three generated Markdown files. Two
chemical-formula link warnings in protected source files were left unchanged.
Six stale-value advisories were inspected: the MASTER retired-value table,
REVIEW's explicit ammonia comparison, and AGENTS' historical examples.

The Word recovery report was rebuilt and checked for its corrected findings
and four embedded figures. All four current recovery images were inspected.
The broad tornado was also regenerated: varying nucleation over its full
YAML range spans approximately 573-fold in metal output with the other inputs
fixed, reversing its former insensitive ranking. This ratio is conditional
on that sweep, not a universal sensitivity or measured uncertainty.


## 90. Explicit recovery inventories and trajectories, 2026-09-07

**Computational implementation closed; chemical calibration remains open.**
The older endpoint-only implementation clipped returned conversion into the
physical interval and did not expose the donor ledger. Equal-volume stage
calculations also left mixing to the reader. The new reduction module exposes
time courses and integrates cumulative protein-oxidation loss. Gold and
protein-equivalent electron conservation are checked separately, so excess
donor cannot hide a gold-balance error. Raw solver results are checked rather
than clipped. Seed gold remains excluded from new product.

The formerly implicit recharge stoichiometry is now `nu_rech` = 1 mol donor
per mol protein recharged in YAML. This retains the earlier two-electron
bookkeeping assumption; it does not supply a measured recharge efficiency.
The existing effective-rate model is retained by default. An optional
`linear_reference` protein factor uses a fixed reference concentration and
represents an unvalidated dose hypothesis. At one-hundredth reference dose,
the two assumptions give essentially complete versus about 20.37% conversion
under reference kinetics. That difference is structural uncertainty, not a
measured dose response. Model settings and this comparison are reproducible
from `params/recovery_model_figures.yaml`.

The new process wrapper carries gold amounts through explicit feed, capture,
elution and lysate volumes. It preserves biomass inventory during a volume
change, requires lysate protein concentration in lysate mode, and distinguishes
a supplied target dose from a predicted production yield. Reference volumes
are illustrative assumptions in `params/recovery_process.yaml`. The terminal
metric remains newly formed metal before collection. Changing wash volume
while retaining the apparent elution constant remains an unvalidated transfer
assumption; quantitative transfer is an idealisation, not measured recovery.

Public inputs now use descriptive names with units. Existing symbols remain
readable through an explicit mapping, and main parameter entries carry
`descriptive_name`. Metadata describing unmeasured affinity, recharge and
inhibition as universally insensitive has been superseded, not erased.
The unused shim entry points now delegate to implemented process, reduction
and sampling functions instead of requesting absent historical source files.

The harvest interpolation helper previously returned an endpoint for a request
outside its simulation window. It now rejects that request, including in
mistiming comparisons, rather than fabricating an unsupported yield.

Pinned by `tests/test_reduction.py` (independent closed-form limit, seed,
donor starvation, separate balances and dose hypotheses),
`tests/test_recovery_process.py` (volume and lysate inventories) and the
out-of-window tests in `tests/test_reductase.py`. The new technical report is
built from live tables and five focused figures. No source document was edited.


### Verification of item 90, 2026-09-07

Full suite: **176 passed in 51.22 s**, with pytest's optional cache disabled
because this environment previously refused cache writes. All eight parameter
YAML files parsed. Every notebook code cell executed successfully with the
noninteractive Agg plotting backend. The first notebook attempt failed in
cell 13 with `TclError: Can't find a usable init.tcl`; choosing the headless
backend resolved the environment failure without changing model results.

The first documentation regeneration detected two stale generated files after
the parameter metadata changes (`_REVIEW_build.md`, `_review_parameters.md`).
They were regenerated through their builder. The repeat `check_docs.py --regen`
passed with **0 of 4 generated Markdown files drifting**, zero tier problems
and zero fixable broken links. The same two protected chemical-formula link
warnings and six inspected historical-value advisories remain.

The new Word report contains about 2,300 words, two tables and five figures.
Its XML parts parse, the live reference result is present, and no table
placeholder remains. The reference process gold-balance residual is
7.77e-16 µmol; maximum trajectory gold and electron residuals are
6.66e-16 µmol/L and 5.68e-14 µmol/L, respectively. These are numerical
conservation errors, not experimental error bars.


## 91. A single-occupancy inventory was mistaken for whole-cell capacity

**2026-09-07. Interpretation corrected; empirical capacity remains open.**
User challenged the low capture result. Recomputing the expression joint gives
23,300.97 active sites/cell, 0.0913135 µmol/g dry cells, and 0.456568 µmol
sites at 5 g dry cells. Equilibrium binding gives 0.454974 µmol from 29 µmol,
so 99.651% of those sites are occupied. Units and arithmetic are consistent.
Waiting longer cannot overcome that fixed inventory in this equilibrium model.

The defect was extending that conditional site inventory into a statement about
all gold accumulated by engineered cells. S 76, omitted from the earlier source
search, provides experimental surface-GolB whole-cell evidence under different
conditions. Molecular occupancy and total cell-associated gold need not be the
same observable. Extra deposition, background binding or replenished display
must not be claimed quantified merely because they could explain the difference.
The rejected 4.4 µmol/g placeholder is not thereby validated, but an argument
that it is impossible for every whole-cell mechanism is withdrawn.

A new explicit whole-cell capacity entry stays null. The existing q_max remains
the expression-derived single-occupancy input; its descriptive name and report
scope now say so. No fitted rate or capacity was invented to raise recovery.
The new inverse sizing calculation is S_required = f*n_feed + Kd*V*f/(1-f),
in µmol, where f is target capture fraction. For 90% capture of 29 µmol in 1 L,
this requires 27 µmol sites: 295.685 g dry cells at current q, or 5.4 µmol/g at
5 g dry cells. These are conditional sizing requirements, not feasible slurry
recommendations. Fifty-eight fresh 5 g contacts also cross 90% capture, but use
290 g total fresh cells; repeated circulation over the same saturated cells
cannot be substituted for those fresh contacts. Regeneration needs its own
capacity-retention measurements.

`tests/test_capture_design.py` verifies inverse sizing, contact conservation,
invalid targets and fixed-biomass dilution. The investigation and plot are in
the current synthesis documents; the original source documents remain unchanged.

---

## 92. `q_max` is a derived site inventory sitting in a slot the field fills by measurement

> **Update 2026-09-18.** The scenario table below used the superseded
> `K_Au = 0.1 µM`. With the adopted S78 proxy `K_Au = 0.7 µM`, the rows become:
>
> | Capacity, µmol/g | Captured, µmol | % of feed | Site occupancy | New metal, % of feed |
> |---:|---:|---:|---:|---:|
> | 0.0913 | 0.4456 | 1.54 % | 97.61 % | 1.23 % |
> | 4.62 | 21.1981 | 73.10 % | 91.77 % | 58.70 % |
> | 5.2 | 23.2000 | 80.00 % | 89.23 % | 64.25 % |
> | 329 | 28.9874 | 99.96 % | 1.76 % | 80.28 % |
> | 992 | 28.9959 | 99.99 % | 0.58 % | 80.30 % |
>
> The original table remains below as the superseded record.

**2026-09-07. Opened after a user challenge to the low capture number.**
Item 91 corrected the interpretation. This item states the category error
behind it, prices the parameters that carry it, and writes down the experiment
that closes it.

### The category error

`q_max` is built by counting parts. Four multiplications, none of which
involves gold:

| Step | Quantity | Value |
|---|---|---:|
| 1 | Surface protein per cell, `expression.steady_state` `P_s` | 46,602 |
| 2 | x `f`, folded and gold-accessible fraction | 0.5 |
| 3 | = `A`, accessible sites per cell | 23,301 |
| 4 | x `cells_per_g` 2.36e12 / N_A x 1e6 | **0.0913 µmol/g** |

In the biosorption literature `q_max` is not a mechanistic quantity at all. It
is the saturation parameter of a fitted isotherm, defined by the experiment
that produces it: cells of known dry mass, a known gold charge, and the gold
remaining in solution afterwards. It cannot be derived, in principle, from any
protein model however correct, because it counts every uptake route and a
protein model counts one.

The two numbers were therefore never the same observable, and the repository
has been reading the smaller one as if it were the larger.

### The expression model refutes the substitution itself

The gap is not a parameter error, and this is checkable inside the repository.
Ask what site count the measured whole-cell loadings would require at
`cells_per_g` = 2.36e12:

| Measured loading | Sites/cell required | Against `P_s_max` = 100,000 |
|---|---:|---:|
| S76, 4.62 µmol/g | 1,178,911 | 11.8x over the anchor ceiling |
| S77, 5.2 µmol/g | 1,326,912 | 13.3x over the anchor ceiling |

The hard ceiling of the cascade is `f`*`P_s_max` = 50,000 sites = 0.196 µmol/g,
which is the engineering target of item 26 and is the membrane saturating
rather than a stretch goal. Setting every input to its most favourable
published corner at once, `N` = 700, `f` = 1.0, and the 148 fg cell that gives
6.76e12 cells/g, reaches 0.753 µmol/g and still misses S76 by 6.1x.

**No setting of the secretion model reproduces the measurement.** Whatever the
measurements are counting is not GolB pocket occupancy. Item 91 said the two
observables need not be the same; this is the arithmetic that shows they are
not.

### What actually carries the risk inside `q_max`

Ranked. None of these closes the 50x gap, which is the point.

| # | Input | Exposure | State |
|---|---|---|---|
| 1 | One Au per GolB site | 2x to 3x if it is two or three | **Assumed. No stoichiometry citation exists in `SOURCES.md`.** S10 gives the Au-S structure and no site count |
| 2 | `f` = 0.5 | 2x | **`status: fitted`, `source: "Folding/accessibility; fitted parameter"`. It is fitted to nothing.** No fit target, no data, no residual |
| 3 | `cells_per_g` = 2.36e12 | about 2.5x across growth conditions | Interpolated from S30, not measured on this culture. Item 33 already moved it once |
| 4 | `P_s_max` = 1e5 | sets the ceiling | From Jose and Meyer autodisplay, the AIDA-I autotransporter, a different anchor from this construct |
| 5 | `N` = 300 | 3.7x on `A` after saturation | Band 75-700, honestly carried, and the least of the five |

Item 2 is the one to fix first, and it is a labelling fix, not a value change.
A parameter whose status is `fitted` and whose source names no fit is
indistinguishable from a guess, and `src/params.py::unsourced` already flags it.

### Literature capacities, and what they give at the operating feed

Three published whole-cell loadings are now recorded in
`params/capture_design.yaml` under `literature:`, each with its conditions and
each labelled `measured_in_other_system`. **None is adopted.**
`V1_capture.whole_cell_capacity` stays null, and
`test_literature_capacities_are_other_system_and_not_adopted_as_the_project_capacity`
fails if any of that is reversed.

Run as scenarios through the existing equilibrium at `Au_feed` = 29 µM,
`X_max` = 5 g/L, `K_Au` = 0.1 µM, in 1 L:

| Capacity, µmol/g | Source | Captured, µmol | % of feed | Site occupancy | New metal, % of feed |
|---:|---|---:|---:|---:|---:|
| 0.0913 | this model, derived | 0.4550 | 1.57 % | 99.65 % | 1.26 % |
| 4.62 | S76, GolB on *E. coli* | 22.7370 | 78.40 % | 98.43 % | 62.96 % |
| 5.2 | S77, GolB on *B. subtilis* | 25.3134 | 87.29 % | 97.36 % | 70.10 % |
| 329 | S57, wild-type, Qe | 28.9982 | 99.99 % | 1.76 % | 80.30 % |
| 992 | S57, Langmuir maximum | 28.9994 | 100.00 % | 0.58 % | 80.31 % |

**These are conditional scenarios, not predictions.** Every capacity in the
table was measured in a different gold chemistry: S76 and S77 in Au(III)
chloride during growth, S57 in Au(III) chloride at pH 3 on wild-type cells.
This project runs Au(I) thiosulfate at pH 9 to 10. Nothing licenses the
transfer, and item 44 stands in front of all of it: 47 mM of tetrathionate
blocks the cysteines the binding depends on, and none of these scenarios
contains that.

Two structural readings do survive the caveat, because they are about the
shape of the table rather than its values:

1. **The bottleneck moves off capture between 4.62 and 329.** At the two GolB
   loadings occupancy is still above 97 %, so the sorbent remains the limit. By
   329 occupancy has collapsed to 1.76 % and the feed is exhausted instead.
2. **80.31 % is the ceiling of the whole table**, and it is `eta_elute` at the
   6 h wash, not capture. Once capacity is adequate the binding constraint
   becomes item 28, the unchosen eluent.

### The measurement that closes this item

One equilibrium isotherm in the project matrix. Half a day of bench time, and
it replaces all five inputs above with one measured pair.

1. **Grow and induce as the process will.** Harvest, wash into the capture
   liquor, and record dry weight directly: lyophilise or dry to constant mass
   at 105 C. Do not convert from OD600 through a literature factor; that factor
   is `cells_per_g`, and measuring the weight here is what removes it.
2. **Fix biomass, vary gold.** One biomass, `X_max` = 5 g/L, against six to
   eight gold charges spanning roughly 0.1x to 10x the expected capacity. Use
   the real leachate, or a synthetic Au(I) thiosulfate at the operating pH and
   the operating copper and polythionate load. Gold chloride at pH 3 measures a
   different system, which is exactly how this item arose.
3. **Run three arms, not one.** Displayed GolB, the un-displayed host, and a
   binding-deficient GolB mutant. The difference between arms is the only thing
   that attributes uptake to the protein. S77 reports its result as a fold
   change over an un-displayed control for this reason.
4. **Measure gold in the liquid, not on the cells.** ICP-MS or ICP-OES on the
   supernatant before and after, to equilibrium. S58 reaches equilibrium in
   about 40 min for a displayed protein, so allow 4 h and sample the approach.
   Loading is (charged minus remaining) divided by dry grams. Filter or
   centrifuge identically in every arm, and carry a no-cell blank for wall
   losses.
5. **Fit Langmuir, and report both parameters.** `q = q_max*C/(K_d + C)` gives
   `whole_cell_capacity` and a competitive `K_Au` in the project matrix. Both
   slots are null today. Report the fit residual and the concentration range
   fitted; a `q_max` extrapolated beyond its data is how item 91 started.

Two additions worth their marginal cost, because they separate mechanisms this
model does not contain:

- **Elute the loaded cells and measure the eluate.** Gold that binds but does
  not release is not recovered gold. This gives `phi` in the project matrix and
  closes item 28 from the same experiment.
- **Fractionate one loaded sample.** Wash, then acid-strip, then digest the
  pellet. Ionic gold released by washing, gold held by the biomass, and gold
  reduced to particles on the cell are three different fates, and only the
  first two reach the reduction stage.

### What must not happen

Copying 4.62 or 5.2 into `whole_cell_capacity` because it makes the recovery
figure look better. That is the failure mode item 91 named and the failure mode
rule 4 exists to prevent. The scenarios above are labelled, tested and reported
as conditional precisely so that no one is tempted.

### What was done

`params/capture_design.yaml` gains three literature entries beside the existing
S76 one, each with `status`, `source` and `conditions`.
`src/capture_design.py::capacity_scenario` is the forward equilibrium that
`required_site_amount` already inverts. Three tests in
`tests/test_capture_design.py` pin the round trip, the monotonicity and the
non-adoption. `docs/SOURCES.md` gains S77 with an explicit verification caveat:
**the Registry page was not read directly and a human must confirm it.**
`docs/CAPTURE_INVESTIGATION.md` carries the scenario table.

No parameter value changed. No source document was touched.


---

## 93. GolB's own copper constant exists, and it is 18 orders from the surrogate

**Found 2026-10-17**, when the author supplied the full text of S76 (Wei et
al. 2012) and asked for a high-copper case to be run.

### What was found

The paper reports dissociation constants measured on **GolB itself**, not on
the GolS reporter:

| Constant | Value | How it was measured |
|---|---:|---|
| `K_d(GolB, Au(I))` | 3.02e-37 M | Au(I)-S absorption at 250 nm, competitive cyanide titration |
| `K_d(GolB, Cu(I))` | 1.61e-17 M | A published protocol, cited in the paper |

The ratio is a gold preference of **5.3e19**. The repository had been using
`alpha` = 52, taken from the GolS whole-cell reporter response in S79, and
AGENTS.md recorded it as "a labelled GolS-derived design scenario only"
because no GolB value was thought to exist. One does.

### Why the measured ratio cannot simply replace 52

Both numbers are the right shape but neither is the quantity the capture
model needs:

- **52 is a response constant**, the half-maximal transcriptional response of
  a different protein. It was always a surrogate.
- **5.3e19 is a bare-ion ratio.** The titrations carry no competing ligand.
  In the project leachate both metals are held by thiosulfate, and
  thiosulfate holds Au(I) far more strongly than Cu(I). The conditional
  selectivity is therefore **lower** than the measured ratio by roughly the
  ratio of the two thiosulfate stability constants.

The measured ratio is therefore adopted as the **upper bound** of a band
whose lower bound is the GolS surrogate.

### What it changes

At 6000 uM copper against 37 uM gold, with 12 g/L of cells:

| `alpha` | Gold captured | Sites held by copper |
|---:|---:|---:|
| 52 | 28.1 % | 80.7 % |
| 1e4 | 94.0 % | 17.0 % |
| 5.3e19 | 96.5 % | 0.0 % |

Above about 1e4 the cell loading for 90 % capture changes by less than
1.5 g/L across fifteen orders of magnitude of selectivity. Below about 1e3,
copper decides the design. **The open question is therefore not the exact
selectivity but which side of about 1e3 it falls on.**

### What is still missing

1. **The thiosulfate correction.** The conditional selectivity needs the
   stability constants of Au(I) and Cu(I) with thiosulfate, from a source.
   Until then the 1e4 working value in
   `params/capture_design.yaml :: stage3_design.selectivity_band` is an
   unsourced order-of-magnitude estimate.
2. **The copper that reaches the comb.** The bioleaching model reports a
   Cu(II) peak of 858 uM at about 29 h but not the value at 24 h, and it does
   not resolve how much is Cu(I), the form GolB binds.

### What was done

`params/capture_design.yaml` gains `binding_proxies.wei2012_golb_Kd_Au`,
`wei2012_golb_Kd_Cu` and `wei2012_golb_selectivity_alpha`, each with its
bare-ion caveat; `checa2007_gols_selectivity_alpha` is relabelled as the lower
bound rather than the sole scenario, with its value unchanged. `docs/SOURCES.md`
S76 gains a dated update with the constants and three further findings from the
same read. `docs/CAPTURE_DESIGN.md` Q1 runs the selectivity as a band.
`docs/capture_design_analysis.py` computes it.

No existing parameter value was changed or deleted.

> **Update 2026-10-17, later the same day. `alpha` = 52 is retired, and the
> band is now derived rather than guessed.**
>
> The author asked to use the literature constants going forward. The GolS
> value is therefore moved to a `superseded:` block in
> `params/capture_design.yaml` with its reason, and
> `binding_proxies.conditional_selectivity_band` replaces it:
>
>     alpha = 5.33e19 x 10^(logB_Cu - logB_Au)
>
> Reported gold values give `logB_Au` = 24 to 26, as estimates rather than
> direct measurements (Senanayake et al., via eprints.ncl.ac.uk/71846). No
> usable Cu(I)-thiosulfate value was found; 10 to 13 brackets the range quoted
> for such complexes, and Etschmann et al. 2011 (10.1039/c1ra00708d) report
> the common Cu(I) thiosulfate species is LESS stable than earlier work
> assumed, which raises the selectivity. The four corners give **5.3e3 to
> 5.3e8**, and sizing uses the lowest corner.
>
> **Why 52 is not a safe conservative floor.** It is a transcriptional
> half-maximal response of GolS, not a binding constant of GolB: the wrong
> quantity from the wrong protein. A surrogate can err in either direction,
> so treating it as a bound implies a confidence nobody has. Every principled
> corner sits three to seven orders of magnitude above it.
>
> **The design conclusion does not rest on the exact value.** Across the whole
> band the cell loading for 90 % capture moves from 12.1 to 9.9 g/L. The
> experiment that would close it is gold capture with and without copper in
> the project leachate, which measures the conditional selectivity directly.

> **Update 2026-10-17, later still. The thiosulfate-corrected band is retired,
> and stage 3 uses GolB's measured constants directly.**
>
> The author asked for the literature dissociation constants to be used
> consistently, with no selectivity ratio. `docs/capture_design_analysis.py`
> now reads `Kd_Au` = 3.02e-37 M and `Kd_Cu` = 1.61e-17 M (S76) and nothing
> else for binding. The retired entries stay in `params/capture_design.yaml`
> in `superseded:` blocks with their reasons: `stage3_design.selectivity_band`
> and `selectivity_design`, and `binding_proxies.conditional_selectivity_band`.
>
> **What this changes.** Both constants are more than thirty orders of
> magnitude below the gold feed, so binding is stoichiometric. Gold takes every
> site it needs and copper takes only what is left. Capture rises in a straight
> line to 100 % at one site per gold atom (0.216 g of dry cells per umol of
> gold, 9.52 g/L at 44 uM) and copper never reduces it. The earlier loading of
> 12 g/L, which was sized on the retired band, is withdrawn.
>
> **What it costs.** The result is an **upper bound**. The constants are
> bare-ion values and were measured with no competing ligand, while in the
> leachate thiosulfate holds the gold. The correction this issue first
> estimated, using thiosulfate stability constants that are themselves
> estimates, gave about 90 % capture at 12 g/L, not 100 %. The design carries
> its uncertainty as one parameter, `design_margin` in
> `params/capture_design.yaml` (1.0 = the floor), to raise once gold capture
> against cell loading has been measured in the project leachate. That
> measurement, not a better estimate, is what closes this issue.
>
> **Tests.** `tests/test_capture_design_analysis.py` pins the numbers the
> write-up quotes and fails if the stoichiometric limit ever stops being valid.
> `tests/test_competition.py` pins that the measured constants and their
> bare-ion caveat stay on record.


## 94. The dip time peaks where the comb matches the gold

**Found 2026-10-17**, writing Q3 of `docs/CAPTURE_DESIGN.md`.

### What was found

The first Q3 draft treated the dip as first-order decay of the dissolved
gold, `t_c = ln(1/(1-f)) / (k_on·[B])`, on the grounds that the sites
outnumber the gold. They do not. Q1 sizes the cells so that one site exists
per gold atom, and Q2 then splits that across several dips, so in every dip
the two pools are within a factor of a few of each other. The honest model is
second order in both:

    dx/dt = k_on · (a0 - x) · (s0 - x)

### Why it matters

The first-order form is not merely imprecise; it points the design the wrong
way. It says more cells always mean a shorter dip. The second-order form says
the dip time **peaks** where the sites equal the gold, because the last site
has to find the last gold atom. At the 44 µM feed:

| Cells on the comb | Sites | Minutes to 99 % |
|---:|---:|---:|
| 3.05 g | 14.1 µM | 8.5 |
| 9.52 g | 44.0 µM | 132.4 |

The comb sized exactly to the batch is fifteen times slower than one a third
its size dipped five times. Q2's choice of several small dips was made on
hardware grounds and turns out to be the fast choice as well.

### What changed

- `binding_time` in `docs/capture_design_analysis.py` was rewritten as
  `dip_time(p, s0, a0, fraction)`, with `binding_time` kept as the
  cells-based wrapper. `dip_schedule` was added for (3.17).
- `dip_time_h` moved from null to **1.0 h**, a design choice, because the
  slowest dip of the batch needs 49 min. `cycles_per_day` now counts the dip,
  so a cycle is 7 h and three fit in a day rather than four.
- The Q1 and Q2 answers are unchanged. They are equilibrium statements and do
  not depend on the rate.

### What is still open

`k_on` = 1.0 µM⁻¹ h⁻¹ is a floor from another organism. Every time in Q3
scales inversely with it, so a measured `k_on` moves all of them together.
