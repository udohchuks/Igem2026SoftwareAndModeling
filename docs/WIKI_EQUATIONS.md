---
title: "The equations on the wiki — stage 3 downwards"
date: "2026-10-17"
---

**Tier 3, synthesis.** Every equation the live wiki Model page shows from the
leach handover onward, transcribed in page order. This is a **record of what
the wiki says today**, not a statement of what the model should say. Where the
wiki and the repository disagree, the disagreement is named in the last
section and belongs in [ISSUES.md](ISSUES.md).

The repository's own equation list is [EQUATIONS.md](EQUATIONS.md). That file
must match `src/`. This file must match the wiki.

**Source.** `ashesighana` repository, branch `software`, read 2026-10-17:

| File | What it holds |
|---|---|
| `src/contents/model-equations.ts` | every equation, authored as MathML |
| `src/contents/model.tsx` | the page, and the prose around each equation |
| `src/contents/model-biorecovery-section.tsx` | the same equations in the standalone biorecovery section |

The page numbers its sections with a `SectionBand index`. Those indices are
used below. Stage 3 of the wiki is **capture**; the upstream team's "Stage 3"
is the leach, which is wiki stage 2. See
`docs/source/bioleaching_2026-10-17/README.md`.

---

# Section 4. From leaching to biorecovery

No numbered equation is rendered. The handover is stated in prose: the
leaching model supplies the dissolved gold entering biorecovery, and
**amounts, not concentrations, cross each vessel boundary**.

`model-equations.ts` defines one inline expression for this handover that the
page does not currently render:

    Au_feed = [Au(S₂O₃)₂³⁻]

Exported as `EQ_AU_FEED`. Unused. Recorded here so it is not mistaken for a
missing equation.

---

# Section 5. Capturing dissolved gold

**W1 — simplified capture chemistry.** `EQ_CAPTURE_REACTION`

    Au(S₂O₃)₂³⁻ + GolB-(SH)₂  ⇌  Au-GolB + released thiosulfate

Reversible, as drawn. One class of sites. Copper able to occupy GolB draws on
the same effective capacity. Permanent site damage is not represented.

| Symbol | Meaning |
|---|---|
| `[Au]` | dissolved gold-thiosulfate |
| `[Au-GolB]` | gold held on the comb, divided by the capture-liquid volume |
| `[S_free]` | unoccupied effective capacity |

---

# Section 6. Connecting comb area to capacity

**W2 — attached biomass from wetted area.** `EQ_COMB_BIOMASS`

    m_X = ρ_X · A_wet

**W3 — comb capacity from biomass.** `EQ_COMB_CAPACITY`

    Q_Au,comb = q_Au · m_X

**W4 — capacity as a concentration.** `EQ_SITE_CAPACITY`

    [S_total] = Q_Au,comb / V_capture

| Symbol | Meaning |
|---|---|
| `m_X` | attached dry biomass, g |
| `ρ_X` | dry biomass per wetted area, g/m² |
| `A_wet` | wetted area, counting both faces of every leaf, m² |
| `q_Au` | whole-cell gold loading, µmol/g |
| `V_capture` | contacted liquid volume, L |

**W5 — attached growth.** `EQ_ATTACHED_GROWTH`, inside a drop-down.

    dm_X/dt = μ_att · m_X · (1 − m_X / m_X,max)

Logistic. The page states that `m_X,0` and `μ_att` are unmeasured, and gives
no clock-time growth prediction.

---

# Section 7. Capture kinetics

**W6 — gold binding rate.** `EQ_CAPTURE_RATE_AU`

    r_Au = k_on,Au · [Au] · [S_free] − k_off,Au · [Au-GolB]

**W7 — free sites.** `EQ_FREE_SITES`

    [S_free] = [S_total] − [Au-GolB] − [Cu-GolB]

**W8 — copper binding rate.** `EQ_CAPTURE_RATE_CU`, inside a drop-down.

    r_Cu = k_on,Cu · [Cu_effective] · [S_free] − k_off,Cu · [Cu-GolB]

`[Cu_effective]` is only the copper able to occupy GolB reversibly, not the
total dissolved copper.

---

# Section 8. Copper competition

**W9 — gold at equilibrium.** `EQ_EQUILIBRIUM_AU`

    [Au-GolB] = [S_total] · ([Au]/K_Au) / (1 + [Au]/K_Au + [Cu_effective]/K_Cu)

**W10 — copper at equilibrium.** `EQ_EQUILIBRIUM_CU`

    [Cu-GolB] = [S_total] · ([Cu_eff]/K_Cu) / (1 + [Au]/K_Au + [Cu_eff]/K_Cu)

`K_Au` and `K_Cu` are apparent dissociation constants; smaller means stronger
binding. The two free concentrations are solved together with both metal
balances. The page runs its baseline at **zero** effective competing copper
and treats the upstream copper peak as a stress test.

---

# Section 9. Transferring gold between vessels

**W11 — the transfer ledger.** `EQ_TRANSFER_LEDGER`

    n_Au,bound  = V_capture · [Au-GolB]
    n_Au,eluted = η_Au,elute · n_Au,bound

**W12 — reduction volume.** `EQ_REDUCTION_VOLUME`

    V_reduction = V_elution + V_reductase

A concentration cannot be copied into a vessel of a different volume. Amounts
cross the boundary; the eluted amount is divided by the combined eluate and
reductase volumes.

---

# Section 10. Releasing gold from the comb

**W13 — elution fraction.** `EQ_ELUTION_FRACTION`

    η_Au,elute = (1 − f_Au,res) · (1 − e^(−k_elute · t))

**W14 — eluted amount.** `EQ_ELUTED_AMOUNT`

    n_Au,eluted = n_Au,bound · η_Au,elute

`f_Au,res` is the fraction that stays on the comb after complete elution.
Rebinding is neglected while thiourea is in excess. The page's proxy is S60:
0.1 M thiourea, 0.1 M sulfuric acid, 50 °C, on a porphyrin polymer rather
than GolB.

---

# Section 11. Producing the reductase

All three are inside a drop-down.

**W15 — reductase growth.** `EQ_REDUCTASE_GROWTH`

    g_R = μ_R · (1 − X_R / X_R,max)
    dX_R/dt = g_R · X_R

**W16 — expression and dilution.** `EQ_REDUCTASE_EXPRESSION`

    dm*_R/dt = G_R · I − (δ_m,R + g_R) · m*_R
    dp_R/dt  = m*_R − (δ_p,R + g_R) · p_R

**W17 — reductase in the lysate.** `EQ_REDUCTASE_LYSATE`

    R_lysate = p_R · X_R · y_lysis · F_conc · 10⁶ / N_A

`G_R = α_R · N_R · β_R` is used as one identifiable product rather than three
separately known constants. Growth dilutes both the transcript state and the
intracellular protein.

---

# Section 12. Reducing dissolved gold to Au(0)

**W18 — reduction chemistry.** `EQ_REDUCTION_REACTION`

    [Au(TU)₂]⁺ + e⁻  ⟶  Au⁰ + 2 TU

**W19 — reduction rate.** `EQ_REDUCTION_RATE`

    r_Au,reduce = (k_nucleation + k_growth · [Au⁰]) · [Au(I)-TU] · [R_red]/[R_total]

Initial particle formation plus growth on existing Au(0), scaled by the
reduced fraction of the reductase pool.

---

# Section 15. End-to-end process

**W20 — efficiencies.** `EQ_EFFICIENCIES`

    η_Au,biorecovery = n_Au,recovered / n_Au,leached
    η_Au,PCB-to-metal = η_Au,leach · η_Au,biorecovery

**W21 — process time.** `EQ_PROCESS_TIME`

    t_preparation = max(t_leaching, t_comb growth, t_reductase production)
    t_total = t_preparation + t_capture + t_wash + t_elution + t_reduction

The page marks `t_total` **pending**, because comb growth, wash time and other
durations are not all defined. No missing duration is filled with a guess.

---

# Where the wiki and the repository now disagree

Recorded, not resolved. Each one is a wiki edit waiting to be made.

1. **W1, W6 and W9 keep binding reversible, with `K_Au` and `K_Cu` as
   apparent constants.** `docs/CAPTURE_DESIGN.md` uses GolB's own measured
   dissociation constants from S76, which sit more than thirty orders of
   magnitude below the feed. At that strength the equilibrium expressions
   collapse to bookkeeping: gold fills the sites it needs, copper takes what
   is left, and copper never reduces gold capture.
2. **W9 and W10 are driven by `[Cu_effective]`, a quantity the page cannot
   measure.** The capture rework drops it.
3. **The page's `ρ_X` and `A_wet` are the one-layer geometric assumption.**
   `CAPTURE_DESIGN.md` uses an areal density `ρ_A` over a stated number of
   cell layers, and names it as the single measurement the design rests on.
4. **The page still quotes 0.0504 m² for "twelve 7 cm × 3 cm combs".** The
   current comb is 10 cm × 10 cm, two panels per comb.
5. **W21 leaves `t_capture` undefined.** `CAPTURE_DESIGN.md` Q3 now computes
   it from the cells on the comb and the gold in the feed.

Items 1 to 4 are already open in [ISSUES.md](ISSUES.md). Item 5 is new work,
not a defect.
