---
title: "Gold biorecovery — the equations"
date: "2026-09-07"
---

**Tier 3, synthesis.** Every equation in the model, in the order the process
runs, with one line of English each. It carries the mathematics for the chain
[MASTER.md](MASTER.md) walks in prose; reasoning, numbers and open questions
belong there and in [ISSUES.md](ISSUES.md), not here. `AGENTS.md` section 11.

**This file must match `src/` today.** A stale equation here is a defect, not
history.

# Notation

| | |
|---|---|
| `d[X]/dt` | rate of change of X |
| upper case | quantity per litre of liquid |
| lower case | quantity per cell or per particle |
| `k` | rate constant |
| `K` | half-saturation concentration |
| `μ` | cell growth rate |
| `V` | reactor volume, litres |
| units | µmol L⁻¹ (= µM); solid metal in µmol; area in m²; minutes for leaching and expression, hours for recovery |

Symbols renamed from the source documents, which keep their originals:
`K_m` → `K_S4O6`, `K_S` → `K_S2O3`, `K_Cu` → `K_CuII`, `A` → `a` for area,
`k₃` → `k_par`, `k₄` → `k_ox,Cu`.

**`R` is the recharging agent in the reduction stage and nothing else.** The
working variable in the elution derivation is `C_elut = C − φC_0`, the
**elutable** part of the bound gold — elutable, not eluted. It stays in the `C`
family: `C`, `C_0`, `C_eq`, `C_elut` are all gold bound to cells. Gold actually
recovered is `C_0 − C` and has no symbol of its own.

Recorded 2026-08-15. A draft of `REVIEW.md` §6.2 used `R` for this quantity,
which both collided with the reductant and read as "recovered gold".

**Reduction renamed 2026-08-16**, because single letters said nothing and `E`
collided with Part I's TetH:

| Source document | Here | Meaning |
|---|---|---|
| `A` | `Au_aq` | gold dissolved in the liquor |
| `B` | `Au_s` | gold as solid particles |
| `E_r` | `E_red` | reductase carrying its electrons |
| `E_o` | `E_ox` | reductase spent, awaiting recharge |
| `R` | `Rech` | the reductant that recharges it; matches `k_rech`, `v_rech` |
| `k_red` | *retired* | was `k_donor`; the branch it controlled no longer exists, ISSUES 50 |
| `v_FW` | `v` | the only rate. There is no second branch to distinguish it from |

---

# Bioleaching

Source: *Bioleaching Modelling [Sequential]*, in
[`docs/source/sequential_2026-08-12/`](source/sequential_2026-08-12/). Three
vessels in series.

| Vessel | Contents | What it makes |
|---|---|---|
| **culture** | *E. coli* culture | the enzyme: TetH, harvested and purified |
| **conversion** | purified TetH + tetrathionate broth | the leachant: thiosulfate liquor |
| **leach** | thiosulfate liquor + crushed PCB | dissolved gold, and unavoidably copper |

## The culture vessel — enzyme production and harvest

$$\frac{dE}{dt}=k_{syn}X-(k_{deg}+\mu)E$$

*Enzyme in the culture vessel: production per cell, first-order degradation,
and dilution by growth.*

$$E_{culture}=\frac{k_{syn}X}{k_{deg}+\mu}$$

*The culture reaches steady state in 1/(k_deg + μ), far faster than anything
downstream, so only the steady state is used. The culture does not appear in the
conversion or leach differential equations.*

$$\frac{V_{culture}}{V_{conversion}}=\frac{E_2}{E_{culture}}$$

*Litres of culture needed to charge one litre of the conversion vessel to enzyme
concentration `E₂`.*

## The conversion vessel — tetrathionate to thiosulfate

$$S_4O_6^{2-}+H_2O\;\rightarrow\;S_2O_3^{2-}+S^0+SO_4^{2-}+2H^+$$

*TetH hydrolyses tetrathionate through a disulfane-monosulfonic-acid
intermediate, lumped into one overall reaction.*

$$I_2+2S_2O_3^{2-}\;\rightarrow\;2I^-+S_4O_6^{2-}$$

*Tetrathionate is generated in situ when iodine is added to the thiosulfate
broth. Iodine is limiting, so both sulfur species are initial conditions
inherited from the medium, not model outputs.*

$$\frac{d[S_4O_6^{2-}]}{dt}=-\frac{k_{cat}E_2\,[S_4O_6^{2-}]}{K_{S4O6}+[S_4O_6^{2-}]}$$

$$\frac{d[S_2O_3^{2-}]}{dt}=+Y\,\frac{k_{cat}E_2\,[S_4O_6^{2-}]}{K_{S4O6}+[S_4O_6^{2-}]}$$

*Irreversible Michaelis-Menten kinetics with the enzyme concentration a
constant input. There are no cells, no copper and no metal surface here, so
every loss term vanishes.*

$$[S_4O_6^{2-}]+[S_2O_3^{2-}]=\text{constant}$$

*Since `Y` = 1, total sulfur is conserved. This is a numerical check.*

$$K_{S4O6}\ln\frac{S_0}{S}+(S_0-S)=k_{cat}E_2\,t$$

*The integrated form, giving an analytical solution for the closed vessel.*

## The leach vessel — dissolving gold and copper

The conversion vessel's product is charged into the leach vessel with crushed PCB
powder. There is no enzyme and no tetrathionate feed, so thiosulfate has no
source and can only be consumed.

### Gold

$$Au^0+2S_2O_3^{2-}\;\rightarrow\;Au(S_2O_3)_2^{3-}+e^-$$
$$4Au^0+8S_2O_3^{2-}+O_2+2H_2O\;\rightarrow\;4Au(S_2O_3)_2^{3-}+4OH^-$$
$$Au^0+2S_2O_3^{2-}+Cu(II)\;\rightarrow\;Au(S_2O_3)_2^{3-}+Cu(I)$$

*The anodic half-reaction, then the two terminal oxidants: oxygen, and
copper(II) leached from the board.*

$$a_{Au}=\frac{m_{Au}}{\rho_{Au}\,t_{film}}$$

*Gold is a thin plated film, so it dissolves by thinning at constant face area
until exhausted, independent of crush size.*

$$R_{Au}=a_{Au}(t)\cdot\frac{[S_2O_3^{2-}]}{K_{S2O3}+[S_2O_3^{2-}]}
\left(k_{Au,O2}\frac{[O_2]}{K_{O2}+[O_2]}
+k_{Au,Cu}\frac{[Cu(II)]}{K_{CuII}+[Cu(II)]}\right)$$

*Parallel oxidant pathways add; area and thiosulfate multiply. Oxygen enters
only its own term, since Cu(II) does not need O₂ at the gold surface.*

$$\frac{dn_{Au}}{dt}=-R_{Au}\qquad\frac{d[Au(S_2O_3)_2^{3-}]}{dt}=+\frac{R_{Au}}{V}$$

*Solid gold in µmol falls as fast as dissolved gold rises.*

### Copper and the Cu(I)/Cu(II) balance

$$4Cu^0+O_2+8S_2O_3^{2-}+2H_2O\;\rightarrow\;4[Cu(S_2O_3)_2]^{3-}+4OH^-$$
$$Cu^0+Cu^{2+}+4S_2O_3^{2-}\;\rightarrow\;2[Cu(S_2O_3)_2]^{3-}$$
$$4Cu(I)+O_2+2H_2O\;\rightarrow\;4Cu(II)+4OH^-$$
$$2Cu(II)+2S_2O_3^{2-}\;\rightarrow\;2Cu(I)+S_4O_6^{2-}$$

*In order: the oxygen route, the comproportionating route, re-oxidation of
copper(I), and the parasitic reaction that destroys thiosulfate.*

$$a_{Cu}(0)=\frac{6\,m_{Cu}}{\rho_{Cu}\,d}\qquad
a_{Cu}(t)=a_{Cu}(0)\left(\frac{n_{Cu}}{n_{Cu}(0)}\right)^{2/3}$$

*Copper is bulk metal, so it follows shrinking-particle geometry with crushed
particle size `d`.*

$$v_{Cu,O2}=k_{Cu,O2}\,a_{Cu}(t)\frac{[O_2]}{K_{O2}+[O_2]}
\cdot\frac{[S_2O_3^{2-}]}{K_{S2O3}+[S_2O_3^{2-}]}$$

$$v_{Cu,Cu}=k_{Cu,Cu}\,a_{Cu}(t)\frac{[Cu(II)]}{K_{CuII}+[Cu(II)]}
\cdot\frac{[S_2O_3^{2-}]}{K_{S2O3}+[S_2O_3^{2-}]}$$

*Copper dissolves by the same two oxidants as gold, on the same shape. The
source writes these together as `v₁A` and `v₁B`, with the stoichiometric
coefficients folded in; they are kept separate here and applied in the balances
below.*

$$v_3=k_{par}[Cu(II)][S_2O_3^{2-}]\qquad
v_4=k_{ox,Cu}[O_2][Cu(I)]$$

*`v₃` is the parasitic reaction, `v₄` copper(I) re-oxidation. Neither involves
a metal surface.*

$$\frac{dn_{Cu}}{dt}=-(v_{Cu,O2}+v_{Cu,Cu})$$

$$\frac{d[S_2O_3^{2-}]}{dt}=-\frac{2R_{Au}}{V}
-\frac{2v_{Cu,O2}+4v_{Cu,Cu}}{V}-2v_3+\nu_{S2}\,v_{alk}$$

$$\frac{d[S_4O_6^{2-}]}{dt}=+v_3-v_{alk}
\qquad\frac{d[S_3O_6^{2-}]}{dt}=+\nu_{S3}\,v_{alk}$$

*Thiosulfate is a budget: two per gold atom, two or four per copper atom by
route, and two per parasitic turnover. Tetrathionate is regenerated by the
parasitic reaction.*

**The alkaline route, added 2026-08-19 and off by default.** Without it
tetrathionate is a dead end and pH changes no rate anywhere in the model.

$$4S_4O_6^{2-}+6OH^-\;\rightarrow\;5S_2O_3^{2-}+2S_3O_6^{2-}+3H_2O$$

$$v_{alk}=k_{alk}\,[OH^-]\,[S_4O_6^{2-}]
\qquad \nu_{S2}=\tfrac54,\;\nu_{S3}=\tfrac12,\;\nu_{OH}=\tfrac32$$

*Hydroxide is in mol L⁻¹ here and tetrathionate in µmol L⁻¹, because that is
how `k_alk` was measured. The three coefficients are read off the balanced
equation, not fitted; sulfur closes as 4 = 2ν_S2 + 3ν_S3. Trithionate has no
sink: `k_tri` is null because no 25 °C measurement exists, so it accumulates
and the model says so.*

$$\frac{d[Cu(I)]}{dt}=\frac{v_{Cu,O2}+2v_{Cu,Cu}+R_{Au,Cu}}{V}+2v_3-4v_4$$

$$\frac{d[Cu(II)]}{dt}=4v_4-\frac{v_{Cu,Cu}+R_{Au,Cu}}{V}-2v_3$$

*Copper metal dissolves as copper(I) on both routes, so `v_4` is the only
source of copper(II). The oxygen routes consume no copper(II) at all.*

### Acidity, and pH as an input

$$\frac{d\,Alk}{dt}=4v_4+\frac{R_{Au,O2}}{V}+\frac{v_{Cu,O2}}{V}
-2v_{hyd}-\nu_{OH}\,v_{alk}
\qquad pH=pH_0+\frac{Alk}{\beta}$$

*Hydroxide released by re-oxidation and by the two oxygen routes, consumed by
the Stage-2 hydrolysis if enzyme was carried over and by the alkaline route.
Tracked as alkalinity — net base added since the start. `β` is the buffer
capacity, and it carries `status: calibrate` with no source.*

**With a dosing pump, pH is an input and this equation inverts.** Alkalinity
stops moving, `β` drops out entirely, and the reported quantity becomes the
titrant the pump must deliver — negative meaning acid:

$$pH=pH_{set}\qquad\frac{d\,Alk}{dt}=0
\qquad\frac{d\,Dose}{dt}=-\left.\frac{d\,Alk}{dt}\right|_{chem}$$

### Oxygen

*Imposed as a constant in the base model. With the air pump modelled it is a
state, and saturation `C*` = 259 µmol L⁻¹ is a ceiling the old imposed 500
sat above.*

$$\frac{d[O_2]}{dt}=k_La\,(C^{*}-[O_2])
-\frac{R_{Au,O2}+v_{Cu,O2}}{4V}-v_4$$

*A quarter of an oxygen per gold and per copper atom, because both reactions
take four metal atoms per O₂; one whole oxygen per `v₄`, because `v₄` is
already the per-O₂ extent.*

### The ligand

*Glycine holds Cu(II) as copper glycinate. Only the free fraction plus a small
share `ε` of the complex attacks thiosulfate; the gold term keeps the full
Cu(II) pool, because copper glycinate still oxidises gold. That asymmetry is
the whole mechanism.*

$$[Gly^-]=G_T\frac{K_{a2}}{K_{a2}+[H^+]}
\qquad \alpha=\frac{1}{1+\beta_1[Gly^-]+\beta_2[Gly^-]^2}$$

$$v_3=k_{par}\,[Cu(II)]\left(\alpha+\varepsilon(1-\alpha)\right)[S_2O_3^{2-}]$$

*`ε` is unmeasured and held null, so a glycine run without it raises rather
than guessing. At `ε` = 1 the expression collapses to the no-glycine case
exactly, which is pinned by a test.*

---

# Handover: leach liquor to capture

$$Au_{feed}\,[\mu M]=[Au(S_2O_3)_2^{3-}]\,[\mu mol\,L^{-1}]$$

*The same quantity under two names. The leach runs in minutes, capture in
hours.*

---

# GolB surface display

Source: `docs/02_golb_expression.md`.

$$\frac{dm}{dt}=\alpha N-(\delta_m+\mu)m$$
$$\frac{dP_c}{dt}=\beta m-(k_{sec}+\delta_c+\mu)P_c$$
$$\frac{dP_s}{dt}=k_{sec}P_c\left(1-\frac{P_s}{P_{s,max}}\right)-(\delta_s+\mu)P_s$$

*`m` mRNA per cell, `P_c` cytoplasmic protein, `P_s` surface protein. `α`
promoter strength, `N` plasmid copy number, `β` translation rate, `k_sec`
export rate, each `δ` a decay rate. The bracket is surface crowding.*

$$s=f\,P_s$$

*Working binding sites per cell; `f` is the correctly folded fraction.*

$$s^{*}=\frac{f\,\alpha N\beta k_{sec}}
{(\delta_m+\mu)(k_{sec}+\delta_c+\mu)(\delta_s+\mu)}$$

*Steady state of the cascade.*

$$q(C)=\frac{s\,C}{K_{Au}+C}$$

*Gold bound per cell at dissolved gold concentration `C`.*

---

# Handover: sites per cell to capacity per gram

$$q_{max}\left[\frac{\mu M}{g/L}\right]
=\frac{s\times n_{cells/g}}{N_A}\times10^{6}$$

*Sites per cell times cells per gram, divided by Avogadro's number and scaled
to µmol.*

---

# Recovery chain

Implemented in [recovery_chain.py](../src/recovery_chain.py),
[recovery_process.py](../src/recovery_process.py),
[reduction.py](../src/reduction.py) and [reductase.py](../src/reductase.py).
Interpretation and parameter provenance: [RECOVERY_MODEL.md](RECOVERY_MODEL.md) and
[ISSUES.md](ISSUES.md), items 84–90. Concentrations are µM and time is h,
except the expression cascade, whose time is min.

## Amount-based stage efficiencies

Capture, elution and reduction efficiencies are the fraction of gold amount
passed from each stage to the next. Physical collection is outside the model.

$$\eta_{total}=\eta_{capture}\eta_{elute}\eta_{reduce}.$$

For transferred gold amount $n$ and receiving volume $V$, the next concentration
is $n/V$. Multiplying concentrations as if volumes were unchanged is invalid.

Feed amount is $n_f=A_fV_f$; capture concentration is $A_T=n_f/V_c$.
Dry biomass is $m_X$, so site concentration is $S=q_{max}m_X/V_c$. Eluted
amount is $n_e=CV_c\eta_{elute}$. Eluate and lysate volumes are $V_e,V_l$;
lysate protein concentration is $E_l$. Their mixture obeys

$$V_r=V_e+V_l,\qquad A(0)=n_e/V_r,\qquad E_T=E_lV_l/V_r.$$

All volumes are L, amounts are µmol, and concentrations are µmol/L.
The target-protein supply mode instead specifies the final $E_T$ directly.

## Capture

These equations describe single-occupancy sites; total whole-cell accumulation
is not bounded by this model without establishing that no other mechanism
contributes. For target fraction $f$, feed amount $n_f$ in µmol and volume
$V_c$ in L, inverse sizing gives

$$n_{sites,required}=f n_f+K_{Au}V_c f/(1-f),\quad 0\le f<1.$$

Required dry biomass in g is $n_{sites,required}/q_{max}$.

Total gold is $A_T$, free gold is $A$, bound gold is $C$, site inventory is
$S=q_{max}X$, and apparent dissociation concentration is $K_{Au}$.

$$A=A_T-C,\qquad C=\frac{SA}{K_{Au}+A},\qquad b=S+K_{Au}+A_T.$$

$$C=\frac{2SA_T}{b+\sqrt{(A_T-S)^2+K_{Au}(K_{Au}+2A_T+2S)}},
\qquad \eta_{capture}=C/A_T.$$

Zero feed gives zero bound gold; efficiency is reported as zero at zero feed.
At low feed the limiting efficiency is $S/(S+K_{Au})$.
The growth-damage extension is not used in current results: its death
coefficient $\lambda_D$ remains null, requiring µM⁻¹ h⁻¹ when damage is µM.

## Elution

Initial bound gold is $C_0$, residual fraction is $\phi$, and remaining elutable
gold is $U$. The empirical second-order constant is $k_2$ in µM⁻¹ h⁻¹.

$$\dot U=-k_2U^2,\quad U(0)=(1-\phi)C_0,\quad
k_{elute}=k_2(1-\phi)C_0.$$

$$\eta_{elute}=(1-\phi)\frac{k_{elute}t}{1+k_{elute}t}.$$

The empirical first-order comparison is
$\eta_{elute,PFO}=(1-\phi)(1-e^{-k_{elute}t})$.
Constants in the two laws need separate fits; neither establishes a mechanism.

## Reduction

Dissolved and metallic gold are $A$ and $B$. Reduced, oxidised and total protein
are $E_r,E_o,E_T$; dithionite is $R_d$. Nucleation and growth constants are
$k_n,k_g$; recharge is $v_{rech}$; protein demand per gold is $\nu$ and
reductant demand per recharge is $\nu_{rech}$.

$$v=(k_n+k_gB)A E_r/E_T,\qquad \dot A=-v,\quad \dot B=v.$$

$$E_o=E_T-E_r,\qquad
v_{rech}=\frac{k_{rech}E_oR_d}{1+A/K_{inh}}.$$

$$\dot E_r=-\nu v+v_{rech}-k_{ox}E_r,\qquad
\dot R_d=-\nu_{rech}v_{rech}.$$

Here $k_{rech}$ is µM⁻¹ h⁻¹ and $k_{ox}$ is protein oxidation in h⁻¹.
At zero total protein this model's protein-mediated rate is zero.

Cumulative oxidation loss in reduced-protein equivalents is $L$, with
$\dot L=k_{ox}E_r$ and $L(0)=0$. The conserved inventories are

$$A+B=A(0)+B(0),$$
$$E_r+R_d/\nu_{rech}+\nu[B-B(0)]+L
=E_r(0)+R_d(0)/\nu_{rech}.$$

The optional linear-dose hypothesis replaces $E_r/E_T$ in the gold rate
with $E_r/E_{ref}$ for a fixed reference concentration. Neither rate scaling
has been calibrated for this protein/precursor mixture.


$$\eta_{reduce}=\frac{B(t)-B(0)}{A(0)}.$$

Initial seed is excluded from new metal. For no seed and constant fully reduced
protein, define $R=k_gA(0)/k_n$ and $\lambda=k_n+k_gA(0)$:

$$B(t)=A(0)\frac{k_n(1-e^{-\lambda t})}
{k_n+k_gA(0)e^{-\lambda t}},\qquad
 t_f=\frac{\ln((1+fR)/(1-f))}{\lambda}.$$

Growth equals nucleation when $B=k_n/k_g$. A finite crossing exists only for
$R>1$ and is $t_{cross}=\ln(2/(1-1/R))/\lambda$. The inverse growth-rate
shortcut is not this exact crossing time.

## Protein production

Biomass is $X$, capacity is $X_{cap}$, maximum specific growth after burden is
$\mu_{eff}$, and actual specific growth is $g=\mu_{eff}(1-X/X_{cap})$.
Transcript and protein per cell are $m,p$, with decay $\delta_m,\delta_p$.
Induction is $I$; transcription and translation supply $\alpha N$ and $\beta$.

$$\dot X=gX,\quad \dot m=\alpha NI-(\delta_m+g)m,\quad
\dot p=\beta m-(\delta_p+g)p.$$

Protein per litre uses cells per dry gram $n_{cells/g}$, Avogadro constant
$N_A$ and molar mass $M_r$:

$$C_{protein}=pX\frac{n_{cells/g}}{N_A}M_r.$$

At stationary biomass and positive decay, the ideal cascade has
$p^*=\alpha N\beta/(\delta_m\delta_p)$. This is a mathematical limit with
constant synthesis, not a measured feasible protein yield.

# Ceilings

| Quantity | Upper bound under model assumptions |
|---|---|
| Bound gold | $\min(A_T,q_{max}X)$ |
| Eluted fraction | $1-\phi$ |
| Metal fraction from electron inventory | $\min(1,[E_r(0)+R_d(0)/\nu_{rech}]/[\nu A(0)])$ |

An upper bound is necessary, not sufficient, for its corresponding yield.
