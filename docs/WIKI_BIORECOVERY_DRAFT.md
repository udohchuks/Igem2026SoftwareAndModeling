# Biorecovery

<!-- **Tier 3, synthesis.** Repository marker; do not copy this comment to the wiki. -->

This section explains how the biorecovery model connects the capture comb,
gold release and reduction to metallic gold. It uses literature-derived
working parameters, and its predictions will be updated with measurements from
the project system.

## From leaching to biorecovery

The previous stage dissolves gold from printed circuit boards. After the
remaining solids are filtered out, the liquid contains dissolved gold and
copper. GolB-displaying *Escherichia coli* are grown on the flat leaves of a
branched comb. The comb is dipped into the filtered liquid, removed after
capture, washed and transferred to the gold-release stage.

Biorecovery is represented in three steps:

1. GolB on the comb captures dissolved gold.
2. Acidic thiourea releases the captured gold into a smaller liquid volume.
3. A reductase converts dissolved Au(I) into metallic Au(0).

## Capturing dissolved gold

Gold enters the stage mainly as gold-thiosulfate. GolB binds metal through the
two cysteine sulfur atoms in its Cys-X-X-Cys motif. The capture chemistry is
represented by the simplified reaction scheme:

    Au(S₂O₃)₂³⁻ + GolB-(SH)₂ ⇌ Au-GolB + released thiosulfate

Copper able to bind GolB can occupy the same effective capacity:

    Cu_effective + GolB-(SH)₂ ⇌ Cu-GolB

A capacity occupied by copper is unavailable to gold. The simplified model
therefore represents copper as an effective reversible competitor. Permanent
damage to GolB is assumed negligible.

### Symbols

| Symbol | Meaning | Unit |
|---|---|---:|
| `[Au]` | Dissolved `Au(S₂O₃)₂³⁻` | µM |
| `[Cu_effective]` | Copper represented as able to compete with gold | µM |
| `[Au-GolB]` | Gold bound to the comb per capture volume | µM |
| `[Cu-GolB]` | Copper bound to the comb per capture volume | µM |
| `[S_free]` | Unoccupied effective capture capacity | µM |
| `[S_total]` | Total effective capture capacity on the comb | µM |
| `q_Au` | Gold loading per gram of attached dry biomass | µmol/g |
| `m_X` | Dry biomass attached to the comb | g |
| `A_wet` | Wetted leaf area, counting both sides | m² |
| `ρ_X` | Attached dry biomass per wetted area | g/m² |
| `V_capture` | Liquid volume contacted by the comb | L |
| `k_on,Au`, `k_on,Cu` | Association-rate constants | µM⁻¹ h⁻¹ |
| `k_off,Au`, `k_off,Cu` | Dissociation-rate constants | h⁻¹ |
| `K_Au`, `K_Cu` | Equilibrium dissociation constants | µM |

### Connecting the comb to capture capacity

At complete surface coverage, the attached biomass is:

    m_X = ρ_X A_wet

The maximum effective gold loading of that biomass is:

    Q_Au,comb = q_Au m_X

The effective capacity used in the concentration model is:

    [S_total] = Q_Au,comb / V_capture

The working literature value is `q_Au = 4.62 µmol/g dry cells` [S76](SOURCES.md).
The area therefore controls how much biomass the hardware supports, while
`q_Au` controls the capacity of that biomass.

With `ρ_X = 0.212 g/m²` and complete coverage, one square metre supplies:

    4.62 µmol/g × 0.212 g/m² = 0.979 µmol Au/m²

### Time-dependent capture model

The gold-binding rate is:

    r_Au = k_on,Au[Au][S_free] − k_off,Au[Au-GolB]

Gold in solution and gold on the comb change together:

    d[Au]/dt = −r_Au

    d[Au-GolB]/dt = r_Au

The equivalent copper equations are:

    r_Cu = k_on,Cu[Cu_effective][S_free] − k_off,Cu[Cu-GolB]

    d[Cu_effective]/dt = −r_Cu

    d[Cu-GolB]/dt = r_Cu

Both metals draw from the same capacity:

    [S_free] = [S_total] − [Au-GolB] − [Cu-GolB]

At the start of capture:

    [Au-GolB]₀ = 0

    [Cu-GolB]₀ = 0

The main time graph uses the gold-only working model with `k_on,Au =
1.0 µM⁻¹ h⁻¹` [S57](SOURCES.md), `K_Au = 0.7 µM` [S78](SOURCES.md) and:

    k_off,Au = K_Au k_on,Au = 0.7 h⁻¹

It shows dissolved gold decreasing and captured gold increasing after the comb
is dipped.

![Capture over time](media/biorecovery/fig1_capture_time.png)

*Figure 1. Capture over time. The comb transfers gold from the liquid to GolB
until the available capacity approaches equilibrium.*

Copper equilibrates in seconds [S80](SOURCES.md), so no time-varying copper
curve is plotted. Copper appears only in the equilibrium competition graph, at
different effective competing copper concentrations.

### Equilibrium capture

At equilibrium:

    [Au-GolB]_eq =
        [S_total] × ([Au]_eq/K_Au)
        / (1 + [Au]_eq/K_Au + [Cu_effective]_eq/K_Cu)

    [Cu-GolB]_eq =
        [S_total] × ([Cu_effective]_eq/K_Cu)
        / (1 + [Au]_eq/K_Au + [Cu_effective]_eq/K_Cu)

The free equilibrium concentrations are found from the two balances:

    [Au]₀ = [Au]_eq + [Au-GolB]_eq

    [Cu_effective]₀ = [Cu_effective]_eq + [Cu-GolB]_eq

The dissociation constants are related to the rate constants by:

    K_Au = k_off,Au/k_on,Au

    K_Cu = k_off,Cu/k_on,Cu

Smaller `K` means stronger apparent binding. The working selectivity is:

    α = K_Cu/K_Au = 52

Using `K_Au = 0.7 µM` gives:

    K_Cu = 52 × 0.7 µM = 36.4 µM

### Capture graphs

The stage uses two separate graphs:

1. **Capture over time.** The comb transfers gold from the liquid to GolB until
   the available capacity approaches equilibrium.
2. **Capacity against comb area.** Increasing wetted area increases capture
   only until the dissolved-gold inventory becomes limiting.

![Capacity against comb area](media/biorecovery/fig2_capacity_area.png)

*Figure 2. Capacity against comb area. Increasing wetted area increases
capture only until the dissolved-gold inventory becomes limiting.*

After introducing competition, a third graph shows equilibrium gold capture
against `[Cu_effective]₀`. The main process baseline uses
`[Cu_effective]₀ = 0 µM` because the upstream model predicts Cu(II), rather
than competing Cu(I), at the late handoff. The `818 µM` case deliberately
treats the upstream model's peak Cu(II) inventory as though it could all
compete reversibly. It is therefore an upper-bound stress test, not the
expected feed composition [Part I result](REVIEW.md#the-leach-vessel).

![Equilibrium gold capture against effective competing copper](media/biorecovery/fig3_copper_competition.png)

*Figure 3. Equilibrium gold capture against `[Cu_effective]₀`. The `818 µM`
case is an upper-bound stress test, not the expected feed composition.*

For the reference case, the competition model gives:

| Case | Gold captured at equilibrium | Interpretation |
|---|---:|---|
| No effective competing copper | 73.10% | Working process baseline |
| `818 µM` effective competing copper | 40.91% | Deliberately conservative stress test |

<details>
<summary>Comb growth and area</summary>

Before capture, attached biomass can be described by logistic growth:

    dm_X/dt = μ_att m_X(1 − m_X/m_X,max)

    m_X(t) = m_X,max
             / [1 + ((m_X,max − m_X,0)/m_X,0)e^(−μ_att t)]

    m_X,max = ρ_X A_wet

The working geometric value `ρ_X = 0.212 g/m²` represents one complete cell
layer. It is derived from a `2.0 µm²/cell` footprint and
`2.36 × 10¹² cells/g dry weight`. Both sides of every wetted leaf count toward
`A_wet`.

For example, supporting `5 g` of dry biomass as one complete layer requires:

    A_wet = 5 g / 0.212 g/m² = 23.6 m²

At `q_Au = 4.62 µmol/g`, that biomass has a working gold capacity of:

    Q_Au,comb = 4.62 µmol/g × 5 g = 23.1 µmol

This equation shows the expected shape of attached growth, but it does not yet
predict clock time because `m_X,0` and `μ_att` have not been measured. The
current numerical model starts from a fully colonised comb and uses the
area-defined capacity. A timed growth graph should be added only after those
two measurements are available.

</details>

<details>
<summary>Competition calculation</summary>

The reference example uses `29 µM` dissolved gold, `[S_total] = 23.1 µM`,
`K_Au = 0.7 µM` and `K_Cu = 36.4 µM`.

Solving the two metal balances with these values gives `73.10%` capture when
`[Cu_effective]₀ = 0 µM` and `40.91%` capture in the `818 µM` stress test.

</details>

### Capture assumptions

| # | Assumption | Why it is used | Consequence if it is wrong |
|---:|---|---|---|
| 1 | The liquid is well mixed and its volume is constant. | This keeps the model to binding rather than fluid transport. | Poor mixing makes the predicted capture time too short. |
| 2 | One completely covered cell layer supplies `ρ_X = 0.212 g/m²`. | It connects comb geometry to biomass before hardware measurements exist. | Capacity changes in direct proportion to the true attached biomass density. |
| 3 | `q_Au = 4.62 µmol/g` transfers to the project comb. | It is the closest whole-cell GolB loading measurement [S76](SOURCES.md). | Every predicted comb capacity changes in direct proportion to the measured project value. |
| 4 | Gold and effective copper bind one shared class of sites reversibly. | It gives the smallest model that represents competition. | Multiple site classes or irreversible binding change the competition curve. |
| 5 | Permanent GolB damage is negligible. | No project measurement currently quantifies it. | Site damage would lower `[S_total]` and make both capture scenarios optimistic. |
| 6 | The working baseline contains no effective competing copper. | The upstream late-handoff copper is modelled as Cu(II), not Cu(I). | Residual competing copper moves the result from the baseline toward the stress-test curve. |
| 7 | The GolS gold/copper selectivity transfers to GolB, giving `K_Cu = α K_Au = 36.4 µM`. | No matched GolB gold/copper measurement exists, and GolS is the closest matched experiment [S79](SOURCES.md). | A different true GolB selectivity moves the whole competition curve, and with it the `40.91%` stress-test result. |
| 8 | Effective copper competition reaches equilibrium within the capture contact. | Cu(I) binding to related Cys-X-X-Cys proteins is complete in seconds [S80](SOURCES.md), while the contact lasts hours. | If copper binds slowly, early capture would retain more gold than the equilibrium competition graph shows. |

The cost of assumptions 2 and 3 is especially direct: their product sets the
capacity per square metre. They should therefore be replaced first.

<details>
<summary>Obtaining capture parameters and proposed experiments</summary>

`K_Au = 0.7 µM` comes from soluble GolB, while `α = 52` comes from a matched
GolS gold/copper response [S78–S79](SOURCES.md). The project should measure:

1. Attached dry biomass per unit wetted area and its growth over time.
2. Gold remaining in the liquid and gold retained by the comb over time.
3. A gold-loading isotherm in the filtered project liquid.
4. Gold capture with and without copper under the same solution conditions.
5. Gold and copper lost during washing.

</details>

## Transferring captured gold between stages

The model passes amounts, rather than concentrations, between vessels. Gold
retained after washing is:

    n_Au,bound = V_capture[Au-GolB]_pre-elution

Gold transferred into the eluate is:

    n_Au,eluted = η_Au,elute n_Au,bound

The reduction volume contains the eluate and the reductase preparation:

    V_reduction = V_elution + V_reductase

The starting gold concentration for reduction is:

    [Au(I)-TU]₀ = n_Au,eluted/V_reduction

This amount ledger prevents a concentration from one vessel being copied
directly into a vessel with a different volume.

## Releasing gold from the comb

After capture, the comb is removed and washed. Acidic thiourea then transfers
the retained gold into solution:

    Au-GolB + 2TU → [Au(TU)₂]⁺ + GolB

`TU` is thiourea. The forward arrow shows that rebinding is neglected while
thiourea is in excess.

### Symbols

| Symbol | Meaning | Unit |
|---|---|---:|
| `[Au-GolB]₀` | Gold on the comb at the start of elution | µM |
| `[Au-GolB]_elutable` | Gold that can still be released | µM |
| `[Au-GolB]_remaining` | Total gold remaining on the comb | µM |
| `f_Au,res` | Fraction remaining after complete elution | dimensionless |
| `k_elute` | First-order release rate | h⁻¹ |
| `η_Au,elute` | Fraction of starting comb gold released | dimensionless |

### Elution model

Initially:

    [Au-GolB]_elutable,0 = (1 − f_Au,res)[Au-GolB]₀

The elutable gold follows first-order release:

    d[Au-GolB]_elutable/dt = −k_elute[Au-GolB]_elutable

    [Au-GolB]_elutable(t) =
        (1 − f_Au,res)[Au-GolB]₀e^(−k_elute t)

Total gold remaining on the comb is:

    [Au-GolB]_remaining(t) =
        f_Au,res[Au-GolB]₀ + [Au-GolB]_elutable(t)

The fraction released into the eluate is:

    η_Au,elute(t) =
        (1 − f_Au,res)(1 − e^(−k_elute t))

**Elution graph finding.** Gold release is fastest at the start and slows as
the elutable pool is depleted. At six hours the working model has transferred
`71.1%` of the pre-elution gold to the eluate. The remaining and released curves
sum to 100%, which provides a visual mass-balance check.

![Gold released and gold remaining during elution](media/biorecovery/fig4_elution.png)

*Figure 4. Gold release is fastest at the start and slows as the elutable pool
is depleted. At six hours the working model has transferred `71.1%` of the
pre-elution gold to the eluate.*

<details>
<summary>Elution parameters, evidence and experiment</summary>

The working condition comes entirely from one acid-thiourea study [S60](SOURCES.md):

| Quantity | Working value |
|---|---:|
| Thiourea | 0.1 M |
| Sulfuric acid | 0.1 M |
| Temperature | 50 °C |
| Sorbent-to-liquid ratio | 1 g/L |
| `f_Au,res` | 0.03 |
| `k_elute` | 0.22 h⁻¹ |

S60 reports more than 90% release at 12 hours and up to 97% overall. The
first-order fit to those two numbers gives:

    k_elute = −ln(1 − 0.90/0.97)/12 h = 0.22 h⁻¹

</details>

## Reducing dissolved gold to metal

The eluate carries gold as soluble gold(I)-thiourea. In a separate reagent
arm, reductase-producing cells are grown and induced, and the reductase
preparation is mixed with the eluate. This mixing sets both the starting gold
concentration and the reductase concentration.

### Producing the reductase

The reductase is produced inside *E. coli*. Its available quantity therefore
depends on culture growth and protein expression before the cells are lysed.
Let `X_R` be reductase-producing dry biomass, `m*_R` be a
translation-weighted transcript state and `p_R` be reductase molecules per
cell. The three expression constants cannot be identified separately, so the
model uses their measurable product, `G_R = α_R N_R β_R`.

#### Symbols

| Symbol | Meaning | Unit |
|---|---|---:|
| `X_R` | Reductase-producing dry biomass | g/L |
| `m*_R` | Translation-weighted transcript state | protein min⁻¹ cell⁻¹ |
| `p_R` | Reductase molecules per cell | protein/cell |
| `g_R` | Instantaneous specific growth rate | min⁻¹ |
| `μ_R` | Maximum specific growth rate of *E. coli* | h⁻¹ |
| `X_R,max` | Carrying capacity of the culture | g/L |
| `α_R` | Promoter strength | mRNA min⁻¹ per plasmid copy |
| `N_R` | Plasmid copy number | copies/cell |
| `β_R` | Translation rate | protein min⁻¹ per mRNA |
| `G_R` | Lumped expression constant, `α_R N_R β_R` | protein min⁻² cell⁻¹ |
| `I` | Induction switch, zero before and one after | dimensionless |
| `δ_m,R` | Transcript degradation rate | min⁻¹ |
| `δ_p,R` | Protein turnover rate | min⁻¹ |

The culture model is:

    g_R = μ_R(1 − X_R/X_R,max)

    dX_R/dt = g_R X_R

    dm*_R/dt = G_R I − (δ_m,R + g_R)m*_R

    dp_R/dt = m*_R − (δ_p,R + g_R)p_R

`I` is zero before induction and one after induction. Growth dilutes both mRNA
and intracellular protein through `g_R`.

After harvesting and lysis, the active reductase concentration in the lysate
is:

    R_lysate(t) =
        p_R(t) X_R(t) n_cells/g y_lysis F_conc × 10⁶/N_A

Here, `n_cells/g` converts dry biomass to cells, `y_lysis` is the recovered
soluble-active fraction, `F_conc` is the concentration factor and `N_A` is
Avogadro's constant. Mixing the lysate with the eluate gives:

    [R_total]₀ = R_lysate(t_harvest)V_reductase/V_reduction

The literature recipe induces at `OD600 = 0.9` and harvests four hours later
[S35](SOURCES.md). The production curve is a provisional description of how
protein changes with cultivation time. It does not yet set `[R_total]₀`,
because active-protein recovery and the lysate concentration factor have not
been measured. The reduction reference scenario therefore uses the separate
design target of `0.2 g/L` reductase after mixing.

The reduction is represented as:

    [Au(TU)₂]⁺ + e⁻ → Au(0) + 2TU

For this model, all Au(0) formed is counted as recovered gold.

### Symbols

| Symbol | Meaning | Unit |
|---|---|---:|
| `[Au(I)-TU]` | Dissolved gold(I)-thiourea | µM |
| `[Au(0)]` | Solid gold atoms per suspension volume | µM |
| `[R_red]` | Reduced reductase | µM |
| `[R_ox]` | Oxidised reductase | µM |
| `[R_total]` | Total reductase | µM |
| `[D]` | Dithionite electron donor | µM |
| `k_nucleation` | Effective initial particle-formation rate | h⁻¹ |
| `k_growth` | Effective particle-growth rate | µM⁻¹ h⁻¹ |
| `ν_R,Au` | Reduced-reductase equivalents used per Au(I) | mol/mol |
| `ν_D,R` | Dithionite equivalents used per reductase recharge | mol/mol |

### Reduction model

The reduction rate contains initial particle formation and growth on existing
gold:

    r_Au,reduce =
        (k_nucleation + k_growth[Au(0)])
        × [Au(I)-TU] × ([R_red]/[R_total])

The gold balances are:

    d[Au(I)-TU]/dt = −r_Au,reduce

    d[Au(0)]/dt = r_Au,reduce

The fraction converted to newly formed metallic gold is:

    η_Au,reduce(t) =
        ([Au(0)]_t − [Au(0)]₀)/[Au(I)-TU]₀

**Reduction graph finding.** Under the reference scenario, dissolved
Au(I)-thiourea falls while Au(0) rises to near-complete conversion. For the
unseeded baseline, `[Au(0)]₀ = 0`, so the curves sum to 100%, providing a
second visual mass-balance check.

![Dissolved gold and metallic gold during reduction](media/biorecovery/fig5_reduction.png)

*Figure 5. Under the reference scenario, dissolved Au(I)-thiourea falls while
Au(0) rises to near-complete conversion.*

<details>
<summary>Reductase recharge</summary>

Electron transfer oxidises the reductase:

    [R_ox] = [R_total] − [R_red]

Dithionite recharges it through the redox system:

    r_recharge =
        k_recharge[R_ox][D]
        / (1 + [Au(I)-TU]/K_Au,inhibition)

    d[R_red]/dt =
        −ν_R,Au r_Au,reduce + r_recharge − k_ox[R_red]

    d[D]/dt = −ν_D,R r_recharge

The working stoichiometries are `ν_R,Au = 0.5 mol reductase/mol Au` and
`ν_D,R = 1 mol donor/mol reductase recharge`. Methyl viologen, present at
`0.1 µM` in the source experiment, is treated as an instantaneous electron
shuttle and is therefore included within the effective recharge step.

</details>

<details>
<summary>Reduction parameters, evidence and experiment</summary>

The fixed reference trajectory uses:

| Quantity | Working value | Source status |
|---|---:|---|
| `k_nucleation` | 0.96 h⁻¹ | Enzyme-scaled literature proxy |
| `k_growth` | 0.082 µM⁻¹ h⁻¹ | Centre of the literature-anchored range |
| Initial dithionite | 50 µM | Process design value |
| Methyl viologen | 0.1 µM | Source experimental recipe |

The source reductase experiment used Au(III), dithionite and methyl viologen,
whereas this stage receives Au(I)-thiourea [S35](SOURCES.md). The first project
experiment should therefore test whether the complete reductase system
converts Au(I)-thiourea at all. If activity is observed, dissolved gold or the
particle signal should be measured frequently during the initial period and
then to a clear plateau. That time course is used to fit `k_nucleation` and
`k_growth` for this system.

The protein-production experiment should measure cell density, intracellular
reductase and soluble active reductase after lysis across cultivation time.
These measurements set the harvest time, lysis yield and the `R_lysate(t)`
curve used by the model.

</details>

## Fixed parameters and adaptable design inputs

The wiki must generate this table and the graphs from the same parameter
object, so a displayed value cannot drift from the calculation.

| Symbol | Value | Unit | Status | Source |
|---|---:|---|---|---|
| `q_Au` | 4.62 | µmol/g dry biomass | Measured in another GolB whole-cell system | [S76](SOURCES.md) |
| `ρ_X` | 0.212 | g dry biomass/m² | Provisional geometric derivation | `params/capture_design.yaml` |
| `k_on,Au` | 1.0 | µM⁻¹ h⁻¹ | Literature proxy | [S57](SOURCES.md) |
| `K_Au` | 0.7 | µM | Soluble-GolB literature proxy | [S78](SOURCES.md) |
| `α = K_Cu/K_Au` | 52 | dimensionless | Related-protein selectivity proxy | [S79](SOURCES.md) |
| `K_Cu` | 36.4 | µM | Derived working scenario | `αK_Au` |
| `[Cu_effective]₀` stress | 818 | µM | Upper-bound reinterpretation of upstream Cu(II) peak | Part I model; `tests/test_leach.py` |
| `f_Au,res` | 0.03 | dimensionless | Transferred elution proxy | [S60](SOURCES.md) |
| `k_elute` | 0.22 | h⁻¹ | Derived from the same elution study | [S60](SOURCES.md) |
| `G_R` | 500 | protein min⁻² cell⁻¹ | Lumped expression proxy | `params/recovery_chain.yaml` |
| `δ_m,R` | 0.20 | min⁻¹ | Literature-derived | `params/expression.yaml` |
| `δ_p,R` | 0.005 | min⁻¹ | Protein-turnover proxy | `params/recovery_chain.yaml` |
| `μ_R` | 1.2 | h⁻¹ | *E. coli* growth rate, adopted from Part II | `params/recovery_chain.yaml` |
| `X_R,0` | 0.02 | g dry biomass/L | Inoculation assumption | `params/recovery_chain.yaml` |
| `X_R,max` | 2.0 | g dry biomass/L | Conservative medium design value | `params/recovery_chain.yaml` |
| `y_lysis` | 0.70 | dimensionless | Lysis-literature proxy | `params/recovery_chain.yaml` |
| `n_cells/g` | 2.36 × 10¹² | cells/g dry weight | Interpolated from a literature curve at `μ = 1.2 h⁻¹` | [S30](SOURCES.md); `params/conversions.yaml` |
| `[R_total]₀` target | 2.86 | µM | Design target derived from 0.2 g/L and 70 kDa | `params/recovery_chain.yaml` |
| `k_nucleation` | 0.96 | h⁻¹ | Enzyme-scaled reference proxy | [S51, S52, S74](SOURCES.md) |
| `k_growth` | 0.082 | µM⁻¹ h⁻¹ | Literature-anchored reference proxy | [S51–S53](SOURCES.md) |
| `[D]₀` | 50 | µM | Reduction design value | `params/recovery_chain.yaml`; [S35](SOURCES.md) |
| `k_recharge` | 0.10 | µM⁻¹ h⁻¹ | Unmeasured working proxy | `params/recovery_chain.yaml` |
| `K_Au,inhibition` | 500 | µM | Unmeasured working proxy | `params/recovery_chain.yaml` |
| `k_ox` | 0.02 | h⁻¹ | Unmeasured working proxy | `params/recovery_chain.yaml` |
| `ν_R,Au` | 0.5 | mol/mol | Mechanism-based stoichiometry | [S63](SOURCES.md) |
| `ν_D,R` | 1.0 | mol/mol | Stoichiometric model value | `params/recovery_chain.yaml` |

The following quantities remain design inputs rather than fixed parameters:
`V_elution`, `V_reductase`, `F_conc`, capture contact time and wash time.
The comb-growth values `m_X,0` and `μ_att` also remain unmeasured. The page
must not report a numerical growth duration or total process time until these
inputs are chosen or measured.

The interactive model is deliberately small. It changes only:

- wetted comb area;
- capture-liquid volume;
- starting dissolved-gold concentration; and
- copper competition, using an off/on stress-test switch.

Time remains the horizontal axis of the kinetic graphs rather than a user
input. Changing the three continuous design inputs or the copper switch
updates comb capacity, captured gold, eluted gold and recovered Au(0) through
the full amount ledger. The fixed parameters and their sources remain visible
in a dropdown.

## Model outputs

For the `23.6 m²`, `5 g` dry-biomass reference in `1 L` containing `29 µM`
gold, the model gives:

| Output | Main baseline | Copper stress test |
|---|---:|---:|
| Effective comb capacity | 23.1 µmol | 23.1 µmol |
| Gold captured at equilibrium | 73.10% | 40.91% |
| Gold released after 6 h | 71.1% of captured gold | 71.1% of captured gold |
| Gold reaching reduction | 52.0% of biorecovery feed | 29.1% of biorecovery feed |

Without effective copper competition, capture leaves `26.9%` of the dissolved
gold in the leachate. Elution then lowers the amount entering reduction to
`52.0%` of the dissolved gold entering biorecovery. Under the fixed reference reduction parameters,
conversion of that remaining gold is nearly complete, giving approximately
`52.0%` overall recovery.

In the upper-bound copper stress test, only `29.1%` of the original gold
reaches reduction and is recovered as Au(0). This is a `22.9` percentage-point
decrease from the main baseline. The model therefore identifies comb capacity,
copper competition and elution as the main limits at this operating point;
the reference reduction step is not limiting.

## End-to-end animation

The final animation follows one gold inventory through the complete model:

    PCB gold
      → dissolved gold after leaching
      → gold captured on the comb
      → gold released into the eluate
      → gold converted to recovered Au(0)

For each stage it displays the gold amount, the fraction retained from the
previous stage and the cumulative process time:

    n_Au,leached = η_Au,leach n_Au,PCB

    n_Au,captured = η_Au,capture n_Au,leached

    n_Au,eluted = η_Au,elute n_Au,captured

    n_Au,recovered = η_Au,reduce n_Au,eluted

    η_Au,biorecovery = n_Au,recovered/n_Au,leached

    η_Au,PCB-to-metal = η_Au,leach η_Au,biorecovery

Here, `η_Au,leach` is supplied by the upstream leaching model; it is not a
parameter fitted in this section. The open outputs table uses dissolved gold
entering biorecovery as its baseline. The animation may additionally show the
PCB-relative result only when the upstream leaching output is supplied.

If the comb culture, reductase culture and leaching run in parallel, the
preparation time is the longest of those three branches:

    t_preparation = max(t_leach, t_comb-growth, t_reductase-growth)

The total process time is then:

    t_total = t_preparation + t_capture + t_wash + t_elution + t_reduction

The animation always reports recovered gold. It reports total time only when
all five duration inputs are available; otherwise it labels the unfinished
duration explicitly instead of substituting a guess. Changing wetted comb
area, capture volume or starting dissolved gold updates the biorecovery
amounts throughout the same sequence.

## Discussion: what the model changes

The reference calculation turns the biological model into two design
requirements. First, the hardware team must provide about `23.6 m²` of wetted
leaf area to support the assumed `5 g` dry biomass monolayer. Second, the wet
lab should prioritise attached biomass density, comb gold loading and elution
measurements because these quantities control the largest losses. The current
reference reduction trajectory is not the bottleneck, but its chemistry must
still be demonstrated with Au(I)-thiourea before it is treated as validated.

The copper stress test is a robustness question, not the process baseline. It
shows that capture could fall from `73.10%` to `40.91%` if the full upstream
copper inventory behaved as a reversible GolB competitor. This result supports
measuring copper speciation at the handoff rather than designing the whole
process around the stress case.

## Limitations

The model transfers capacity, affinity, elution and reduction-rate values from
related systems. It assumes complete attached-cell coverage, ideal mixing and
no permanent loss of GolB activity. It does not yet predict comb cultivation
time, washing time or an absolute end-to-end duration. Reduction ends at
Au(0); downstream particle collection is outside the model, so all Au(0)
formed is counted as recovered.

## Conclusion

For the reference comb and dissolved-gold feed, the model predicts `52.0%`
recovery to Au(0), falling to `29.1%` in the conservative copper stress test.
The next design gains should come from increasing verified comb capacity and
improving gold release, while targeted experiments replace the transferred
parameters.
