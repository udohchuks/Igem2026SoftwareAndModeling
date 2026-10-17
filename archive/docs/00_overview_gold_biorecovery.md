# Gold Biorecovery — Model

**v3.0 (2026-08-04)** · Code: `pipeline_model.py`, `r9L_fw.py`, `ensemble.py`
**Units:** µM, hours, g/L · **Companion:** build plan v2.5 (decisions, audit trail, citations)

*This document is current state only. Change history, superseded results and
provenance disputes live in the build plan.*

---

## 0. Validation status — read first

**No part of this model has been checked against a measurement of this system.**
Every parameter is literature-transplanted, proxy-bounded, or declared. The
verification checks confirm the code solves the equations; they say nothing
about whether the equations describe reality.

Three facts bound every claim below:

- **No demonstration exists** that this construct reduces gold in a lysate. The
  source paper used purified protein + added dithionite on pure HAuCl₄; the
  process uses crude lysate + native reductants on thiourea eluate.
- **Conversion has never been quantified** by anyone, in any version of this
  chemistry. Both source papers detect product by colour and TEM only.
- **Selectivity against Cu/Ag/Ni is unknown.** Both source papers used pure gold.

**The deliverable is a ranked measurement priority list, not a yield prediction.**

**Track record: every parameter assumed without a source, then sourced, was
wrong** — `A_tox` (wrong regime), `K_D` (≥12 orders), `k_red` (7×),
`eta_spin` (2×). `eta_wash` is the last unsourced parameter and should be
treated as an upper bound.

---

## 1. The chain

$$\eta_{total}=\eta_{capture}\cdot\eta_{elute}\cdot\eta_{reduce}\cdot\eta_{phys}$$

Two parallel arms converge at reduction:

```
ARM A (gold)                              ARM B (reagent)
  leach (out of scope) → sets Au_feed       grow E. coli BL21 + ABC construct
        ↓                                   induce 1 mM IPTG, 4 h
  V1 capture biofilm, 13-16 h               lyse: sonicate, 100,000 g 90 min
        ↓ thiourea elution, 3 h                    ↓
  conditioning (not modelled) ──────→  V2 lysate reduction, 12-24 h, pH 7.4
                                              ↓
                                       recovery: spin → wash → ash
```

**Critical path ≈ 42 h/batch.** Conditioning is the only unmodelled series step
(assumed lossless).

**Current: `eta_total` = 10.5% median, 90% CI [0.0%, 49.4%].**

---

## 2. V1 — capture

Living *E. coli* displaying GolB in an LB-like (chelating) medium.
States: `X` biomass, `C` bound gold, `D` damage.

$$A=Au_{tot}-C \qquad S_0=q_{max}X \qquad G=A+wC$$

$$\frac{dX}{dt}=\mu X\left(1-\frac{X}{X_{max}}\right)-mX-\lambda_D DX$$
$$\frac{dC}{dt}=k_{on}A(S_0-C)-k_{off}C$$
$$\frac{dD}{dt}=k_{dam}G-k_{rep}D \qquad \lambda_D=\frac{\mu k_{rep0}}{A_{tox}}$$

Lethality is pinned to a fixed value rather than scaled with repair, so slow
repair appears as harm rather than compensation.

**Verification (all pass):** Langmuir limit ($C_{eq}=S_0A/(A+K_D)$, err 2e-09);
binding half-time; gold mass balance; zero-gold logistic limit; capacity ceiling
$\eta \le q_{max}X_{max}/Au_{tot}$.

### 2.1 Two results that matter

**No harvest-time optimum exists.** In an LB-like medium at sub-onset feed,
capture is flat: 79.5% at 12 h, 79.8% at 24 h, 79.7% at 72 h. **Harvest any time
after ~12 h.** The earlier "toxicity racing binding" result was an artefact of a
buffer-regime `A_tox`.

**`Au_feed` is the dominant design variable**, and an input from the
out-of-scope leaching model:

| `Au_feed` | η (`A_tox`=250) | η (`A_tox`=30) | Au captured | limited by |
|---|---|---|---|---|
| 3 µM | 85.2% | 84.2% | 2.56 µM | equilibrium |
| 10 µM | 79.9% | 73.3% | 7.99 µM | equilibrium |
| 22 µM | 64.8% | 37.7% | 14.26 µM | ← transition |
| 50 µM | 33.7% | 4.1% | 16.84 µM (peak) | capacity |
| 300 µM | 1.6% | 0.1% | 4.70 µM | capacity |

The transition is exactly the capacity ceiling $q_{max}X_{max}$ = 22 µM.
**Absolute capture peaks near 50 µM feed** but that is where `A_tox` uncertainty
swings capture ~8×.

**Recommended operating point: 10–20 µM feed** — below the absolute peak, but
the `A_tox` disagreement costs <10% there vs 63–96% above 30 µM. **Dilution is
a legitimate design lever.**

**Capture is capacity-limited, not affinity-limited.** At 10 µM feed, sites must
exceed 10 µM, requiring X > 2.27 g/L.

---

## 3. Elution

**Mechanism: thiourea competitive ligand exchange, not acid.** One Au atom is
chelated between two sulfur atoms of two thiourea molecules — a better bidentate
site than GolB's Cys10/Cys13. Acid (pH 1.4–1.8) is a co-requirement, not the
mechanism.

⚠️ **The project architecture assumed an acid wash. If the wet lab plans
acid-only, elution may recover far less than $(1-\phi)$ predicts and the model
would not show it** — `k_max` is a fitted rate that silently absorbs "the eluent
doesn't work." **Confirm the eluent.**

Thiourea at ~1 M against micromolar gold is a ~10⁴ excess, so the exchange is
pseudo-first-order:

$$\frac{dC}{dt}=-\underbrace{k[TU]^n}_{k_{max}}\big(C-\phi C_0\big)^{+}$$

$$\boxed{\ \eta_{elute}(t_k)=(1-\phi)\left(1-e^{-k_{max}t_k}\right)\ }$$

- $(1-\phi)$ — **ceiling.** Chemistry. Not improvable by time or acid strength.
- $(1-e^{-k_{max}t_k})$ — **approach.** 95% of ceiling at $3/k_{max}$.

**Different fixes:** a short wash is cured by patience; a low ceiling is not.
Sampling at 0.5/1/2/4 h distinguishes them.

`pKa_GolB` and `n_H` leave the model — below pH 2 the thiourea route is fully
open.

**`k_max` is a design lever** since $k_{max}=k[TU]^n$: at 2 M the wash finishes
in an hour; at 0.1 M six hours is not enough.

---

## 4. Reduction (rung 9L)

Cell-free metabolic engineering with crude extract. The protein is a
**stoichiometric redox reactant, not a catalyst** — one exterior Cys337–Cys481
disulfide, 2 electrons, consumed per use.

**Crude lysate reduces gold with no added reductant** (published); only
*purified* protein needs dithionite, because purification dialyses the native
reductants out. **Do not dialyse the V2 lysate.**

States: `A` soluble Au, `E_r` fresh sites, `E_o` spent sites, `R` carried-over
reductant (finite, no regeneration), `B` Au(0).

$$v_{red}=k_{red}AE_r \qquad v_{FW}=(k_1+k_2B)A \qquad v=\min(v_{red},v_{FW})$$

$$\frac{dA}{dt}=-v \quad \frac{dB}{dt}=+v \quad
\frac{dE_r}{dt}=-\nu v+v_{rech}-k_{ox}E_r \quad \frac{dR}{dt}=-\nu_R v_{rech}$$

$$v_{rech}=k_{rech}E_o\frac{R}{1+A/K_i}$$

with $\nu=n_{e,Au}/2$: **0.5 for Au(I)** (our feed), 1.5 for Au(III).

**The slow step is nucleation, not electron transfer.** Thiol+gold redox
completes in ~100 s, but the observed process takes 8–48 h — a factor of ~300.
$k_1$ is nucleation (slow); $k_2B$ is autocatalytic growth, accelerating as
surface accumulates.

### 4.1 Electron budget — the rate-free ceiling

$$\eta_{reduce}\le\frac{2E_{tot}+2R_0}{n_{e,Au}A_0}$$

Needs no rate constant. **At 5.78 µM Au(I), 0.2 g/L protein already supplies
98.9% of the electrons needed**, so $\eta_{reduce}\approx 1$ on the budget.

The same arithmetic reproduces the source papers' regime: at 2 mM Au(III) with
0.1 g/L protein the budget covers **0.048%** — which is why they never measured
conversion.

**Regeneration does not decide the outcome.** Sweeping $k_{rech}$ over five
orders and $R_0$ over four leaves $\eta_{reduce}$ at 97.7–100%. Even with zero
regeneration, 97.7%. The carried-over reductant's real role is **buffering
against aerobic inactivation** ($k_{ox}$), not driving turnover.

**Verification (all pass):** fast-limit exponential decay (err 1.3e-09);
stoichiometric limit $B_\infty=E_{tot}/\nu$ exact; site conservation (6e-13);
gold mass balance (2e-10).

### 4.2 The testable prediction

| t (h) | 1 | 2 | 4 | **8** | **12** | 24 |
|---|---|---|---|---|---|---|
| η_reduce | 0.01% | 0.04% | 0.4% | **31%** | **98%** | 100% |

**Sigmoid with a pronounced induction period.** A non-nucleation model predicts
monotone-decelerating decay — fastest at t=0. **Opposite shapes in the first
four hours.**

**Experiment: gold + lysate, sample 0/1/2/4/8/24 h, read A₅₂₀.**

| observation | conclusion |
|---|---|
| little happens, then rapid conversion | nucleation-limited — confirmed |
| fastest at t=0, gradually slowing | electron-transfer-limited |
| never completes | budget- or reductant-limited |

⚠️ **$k_1$ and $k_2$ are calibrated against one qualitative observation**
("nanoparticles visible at 8 h"), checked only against a published gold F-W fit
via the dimensionless shape group $k_2[A]_0/k_1$ — ours 23,120 vs literature
10,685, a factor of 2.2. **They are the joint #1 driver of the pipeline and are
not measured.**

---

## 5. Recovery (rung 11)

$$\eta_{phys}=\eta_{spin}\cdot\eta_{wash}\cdot\eta_{ash}$$

**Centrifugation, not gravity settling.** Stokes ($v\propto r^2$, gold 19.3
g/cm³), time to fall 10 cm: 10 nm → 290 days; 100 nm → 3 days; 1 µm → 42 min.
Nanoparticles never settle unaided.

⚠️ **But centrifugation does not remove the size dependence.** A commercial
protocol reports **~50% recovery for 10 nm gold after a 30-minute size-matched
spin.**

| term | value | basis |
|---|---|---|
| `eta_spin` | **0.50 (10 nm) – 0.97 (>200 nm)** | sourced only at 10 nm |
| `eta_wash` | 0.95 | **unsourced — upper bound** |
| `eta_ash` | 0.98 | conditional on temperature ↓ |

**Hard process constraint: ash at 500–600 °C, do not exceed.** Biomass fully
decomposes there and gold is retained. Above it, gold partially volatilises into
the off-gas and recondenses in fine ash — in a lab furnace, on the walls.

### 5.1 The trade-off this creates

High protein → better conversion → **smaller particles** → worse recovery.
$\eta_{reduce}$ and $\eta_{phys}$ pull against each other through protein
loading. **Rung 12 must optimise their product, not each separately.**
Particle-size distribution therefore re-enters the model.

### 5.2 Purity

Core is verified metallic fcc Au(0) (XRD Bragg reflections, SAED, EDX). Every
particle carries a protein coat — the reducing protein is also the stabilising
agent. **The organic fraction has never been quantified**; the obvious EDX
measurement is confounded by the carbon TEM grid.

Purity scales with size (5 nm coat assumed): ~86% Au at 10 nm core, ~98% at
50 nm, ~99.5% at 200 nm. Calcination removes the remainder.

**Context:** the V2 output is **0.02–0.07% gold by mass** — comparable to raw
e-waste PCBs. The gain is *form* (discrete separable metal), not grade.

---

## 6. Optimisation

**Two objectives, and they conflict.** $\eta_{total}$ is a *fraction*;
maximising it starves the feed.

| `Au_feed` | $\eta_{total}$ | Au recovered |
|---|---|---|
| 3 µM | 63.1% | 1.89 µM |
| 10 µM | 59.2% | 5.92 µM |
| 50 µM | 24.8% | **12.41 µM** |
| 100 µM | 10.8% | 10.77 µM |

**Optimum A (maximise fraction):** feed 10 µM, $t_{harvest}$ 16 h, $t_k$ 6 h.

| particle size | $\eta_{phys}$ | $\eta_{total}$ |
|---|---|---|
| **10 nm (only sourced value)** | 0.465 | **32.3%** |
| 50 nm | 0.745 | 51.8% |
| >200 nm | 0.903 | 62.8% |

**Optimum B (maximise absolute gold):** feed 50 µM → 12.9 µM recovered, but that
is where `A_tox` uncertainty is worst. **Operate at 10–20 µM.**

**Lever behaviour:** $t_{harvest}$ is flat (not an optimisation variable);
$t_k$ has diminishing returns past $3/k_{max}$; protein loading saturates for
conversion at 0.2 g/L and worsens recovery above it; **`Au_feed` dominates**.

### 6.1 Where the losses are

At Optimum A, 10 µM feed, $\phi$=0.13, $\eta_{phys}$=0.465:

| stage | efficiency | points lost |
|---|---|---|
| **recovery** | 46.5% | **53.5** |
| capture | 79.9% | 20.1 |
| elution | 87.0% | 13.0 |
| reduction | 100.0% | 0.0 |

**Recovery is the largest loss — and the least-modelled stage.** If particles
are large (>200 nm) the ranking reverts to capture-first, so it is contingent on
a quantity nobody has measured.

---

## 7. Parameters

| symbol | value | status |
|---|---|---|
| **V1** | | |
| `mu`, `Xmax`, `X0`, `m` | 0.70, 5.0, 0.05, 0.005 | standard *E. coli* |
| `q_max` | 4.4 µM/(g/L), sweep 0.33–4.4 | **⚠️ may be 5–13× optimistic vs published display ceiling** |
| `K_D` | 0.1 µM (conservative), sweep 1e-4–0.1 | **insensitive** (PRCC ≈0); bounded by CXXC proxies |
| `k_on` | 1.0 | unsourced; only `K_D` matters |
| `A_tox` | 250 µM (LB MIC), pessimistic 30 | LB regime; two sources agree on ~30 µM onset |
| `k_dam`, `k_rep0` | 1.0, 0.1 | **unsourced; `k_dam`/`A_tox` non-identifiable — only the ratio is determined** |
| `w` | 1.0 | **insensitive** (PRCC −0.02) |
| `Au_feed` | 10–20 µM target | **input from out-of-scope leaching model** |
| **Elution** | | |
| `phi` | 0.13, sweep 0.05–0.30 | 87% desorption, protein biosorbent + 1 M thiourea. May be formulation-dependent (95–98% with additives) |
| `k_max` | 2.0 /h at 1 M thiourea | design lever via [TU] |
| **Reduction** | | |
| `k_red` | 0.0072–158 µM⁻¹h⁻¹, log | literature thiol-Au bracket; **insensitive** given F-W |
| `k1`, `k2` | 5e-5 /h, 0.2 µM⁻¹h⁻¹ | **weakly calibrated — joint #1 driver** |
| `k_ox` | 0.02 /h | unsourced; measurable (air vs N₂) |
| `k_rech`, `K_i` | 0.1, 500 | **insensitive** |
| `R0` | 10–1000 µM | lysis-dilution choice, not a literature value |
| `nu` | 0.5 (Au(I)) | stoichiometric |
| `E_tot` | protein/70000 × 1e6 | measurable; set by induction |
| **Recovery** | | |
| `eta_spin` | 0.45–0.99 | sourced only at 10 nm (~0.50) |
| `eta_wash` | 0.95 | **unsourced — upper bound** |
| `eta_ash` | 0.98 | conditional on 500–600 °C |

---

## 8. Uncertainty

Latin hypercube, n=3000, log-scale priors on rate constants, PRCC global
sensitivity. Design variables are held at the optimum, not sampled.

| term | 5% | median | 95% |
|---|---|---|---|
| eta_capture | 15.0% | 53.5% | 100.0% |
| eta_elute | 51.6% | 69.3% | 87.4% |
| eta_reduce | 0.0% | 73.0% | 100.0% |
| eta_phys | 39.9% | 60.6% | 83.4% |
| **ETA_TOTAL** | **0.0%** | **10.5%** | **49.4%** |

**Report the interval, not the median.** A point estimate built from many
uncertain parameters lands wherever the favourable ends coincide.

**PRCC:** `k2` +0.785, `q_max` +0.783, `Xmax` +0.370, `k1` +0.366,
$\phi$ −0.321, `eta_spin` +0.313, `k_red` +0.214.
Insensitive (<0.05): `K_D`, `K_i`, `k_on`, `k_max`, `w`.

**The 0.0% floor** comes from slow-$k_1$/$k_2$ draws where reduction does not
complete in 24 h. Only the §4.2 experiment closes it.

**Re-run** after any prior change — the interactions are the point:

```
from ensemble import sample, chain, prcc, NAMES
import numpy as np
X = sample(3000, seed=7); res = np.array([chain(r) for r in X])
print(np.percentile(res[:,4], [5,50,95]))
```

~75 s. PRCC ranks stable above ~2000 samples.

---

## 9. Measurement priority

1. **Reduction time course** — gold + lysate, 0/1/2/4/8/24 h, A₅₂₀.
   Addresses `k1`+`k2` (joint #1), tests model *structure*, and is the only
   route to closing the 0.0% floor. Also the only test of whether the chemistry
   works at all.
2. **`q_max`** — display density. Being addressed by the secretion model.
3. **Conversion quantification** (ICP-MS or colorimetric, not colour/TEM).
4. **$\eta_{spin}$ and particle size** on real product.
5. **Eluent confirmation** — thiourea or acid-only.
6. **$\eta_{wash}$** — last unsourced parameter.

---

## 10. What the model cannot tell you

**Wet-lab facts:** whether the construct reduces gold in lysate at all; what
fraction of gold converts; selectivity against Cu/Ag/Ni in real leachate;
whether GolB's own Cys10/Cys13 oxidise shut during a 13 h aerobic run.

**Structural gaps:** `Au_feed` has no upstream model though it dominates V1;
conditioning (V1→V2 transfer) is assumed lossless; particle-size distribution is
absent though it now couples two η terms; `k_dam`/`A_tox` are structurally
non-identifiable.

**Open branch:** incineration could replace elution entirely, deleting elution
and conditioning, at the cost of destroying the biofilm.
