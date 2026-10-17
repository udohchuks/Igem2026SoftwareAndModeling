# Copper competition for the GolB sites

**Tier 3, synthesis.** Copper competition for the GolB sites, 2026-09-13.

**What this file is.** It explains how gold and copper are modelled as
competitors for one GolB site inventory, what the model says today, and what
the wet lab must measure before any of it becomes a prediction. Its numbers
come from `src/competition.py` and are pinned by `tests/test_competition.py`.
Formulae are written in plain text, as in
[CAPTURE_INVESTIGATION.md](CAPTURE_INVESTIGATION.md); the LaTeX forms belong in
[EQUATIONS.md](EQUATIONS.md).

**What it is not.** It is not an adoption of a copper binding constant. No such
constant has been measured in this project's liquor, and none is stored in
`params/`. Every capture number below is conditional on a swept unknown.

Read [ISSUES.md](ISSUES.md) item 22 for the apparent-constant problem and item
92 for the capacity problem.

---

## 1. The question

The comb is meant to work as a selective filter. Leaching hands it about 29 µM
gold and about 818 µM total copper, so copper outnumbers gold 28 to 1. The
capture model has until now bound gold and ignored copper. That makes every
capture figure in the repository an **upper bound**, not evidence of
selectivity.

## 2. The standard way to model this

The field uses the **extended, or competitive, Langmuir isotherm**. Both metals
divide one denominator, and sharing that denominator is what makes them
competitors rather than two unrelated isotherms.

Write the two site fractions as:

    theta_Au = (C_Au/K_Au) / (1 + C_Au/K_Au + C_Cu/K_Cu)
    theta_Cu = (C_Cu/K_Cu) / (1 + C_Au/K_Au + C_Cu/K_Cu)

where C_Au and C_Cu are free concentrations in µmol/L, K_Au and K_Cu are
apparent dissociation constants in µmol/L, and theta is the fraction of the
site inventory held by that metal.

Three rules govern the use of this isotherm. Two of them are easy to get wrong.

**Rule 1. C_Au and C_Cu are free concentrations at equilibrium, never the
feed.** Binding depletes the liquid. At this operating point about 78% of the
gold binds, so feed and free differ by roughly a factor of five. Substituting
the feed overstates gold occupancy.

**Rule 2. The isotherm is solved together with the mass balances.** Two
balances share one site inventory S0, in µmol/L:

    Au_tot = C_Au + S0*theta_Au
    Cu_tot = C_Cu + S0*theta_Cu

`src.competition.capture_equilibrium` solves these with a bracketed root
finder. The one-metal version of the same argument is the quadratic in
`src.recovery_chain.capture_equilibrium`, and with no copper the two agree
exactly. `test_no_copper_reduces_to_the_one_metal_quadratic` pins that.

**Rule 3. Selectivity is reported as a separation factor**, the ratio of the
two distribution coefficients:

    S = (q_Au/C_Au) / (q_Cu/C_Cu)

S above 1 means the sorbent enriches gold. For the extended Langmuir, S equals
K_Cu/K_Au identically, which `test_separation_factor_is_the_swept_ratio` pins.
That identity is the reason section 4 sweeps that ratio and nothing else.

Escalate to IAST or to a Sips form only if measured data reject this isotherm.
Do not start there.

## 3. The unknown, and how to handle it honestly

K_Cu has not been measured for GolB in the project liquid. The working model
therefore uses a literature selectivity scenario rather than presenting a
derived number as a measurement.

The standard move is to collapse the unknown into one dimensionless ratio and
sweep it:

    alpha = K_Cu / K_Au

Gold and copper claim equal shares of the denominator when C_Au/K_Au equals
C_Cu/K_Cu, so the two metals tie at:

    alpha_tie = C_Cu / C_Au = 818 / 29 = 28.2

Wei et al. measured K_d,Au = 3.02e-37 M and K_d,Cu = 1.61e-17 M on purified
GolB, an alpha of about 5.3e19. Those constants were obtained with Au(CN)2- by
cyanide titration, not with Au(I)-thiosulfate, so they bound the question
rather than answer it.

Checa et al. measured matched whole-cell response constants for the related
GolS regulator: 0.2 µM for gold and 10.4 µM for copper, giving alpha = 52
[S79](SOURCES.md). GolS is not GolB, so 52 is used as a conservative working
scenario. With the adopted GolB-based gold proxy K_Au = 0.7 µM [S78](SOURCES.md),
that scenario gives K_Cu = 36.4 µM.

## 4. What the model says

Feed 29 µmol gold and 818 µmol total copper into 1 L, with 4.62 µmol/g against
5 g dry cells, so S0 = 23.1 µmol/L, and K_Au = 0.7 µmol/L.

| alpha = K_Cu/K_Au | Gold captured | theta_Au | theta_Cu | Copper captured |
|---:|---:|---:|---:|---:|
| 1e6 | 73.09 % | 0.9176 | 0.0001 | 0.00 % |
| 1e4 | 72.54 % | 0.9106 | 0.0093 | 0.03 % |
| 1e3 | 68.36 % | 0.8582 | 0.0763 | 0.22 % |
| 1e2 | 49.69 % | 0.6238 | 0.3463 | 0.98 % |
| **52, working scenario** | **40.91 %** | **0.5136** | **0.4654** | **1.31 %** |
| 28.2 | 32.07 % | 0.4026 | 0.5831 | 1.65 % |
| 10 | 18.11 % | 0.2273 | 0.7660 | 2.16 % |
| 1 | 2.72 % | 0.0342 | 0.9649 | 2.72 % |

**Degradation starts far above the tie point.** Measured against the
copper-free capture of 73.10%:

| Relative loss of gold capture | Occurs at alpha |
|---|---:|
| 1 % | 7.63e3 |
| 10 % | 586 |
| 50 % | 38.4 |

Quoting the tie point alone is therefore too generous. **The comb needs an
apparent selectivity near 600, not near 30, to lose less than a tenth of its
gold.**

At the 24 h handoff the picture is milder. There the model carries 200 µM Cu(I)
and 28.2 µM gold, so the tie sits at 7.1, the 10% loss at alpha = 148, and
copper-free capture is 74.62%.

## 5. What this model cannot represent

**Cu(II) oxidation of the binding site.** At the 72 h handoff `src/leach.py`
returns Cu(I) = 0 and Cu(II) = 818 µM, because thiosulfate is exhausted and
oxygen has taken the Cu(I) pool. Cu(II) oxidises cysteine thiolates to
disulfide and is reduced to Cu(I) in the process, and a CXXC motif locked as a
disulfide binds no metal at all. Wei's cysteine mutants, which lost both Au and
Cu binding, are the direct evidence that both cysteines are required.

That is **irreversible site loss, not competition**. It belongs in S0 as a
decay term, not in K_Cu. Fitting it as an affinity would hide a destroyed comb
inside a plausible-looking constant. Tetrathionate is a second oxidant with the
same target.

**The wash and the elution.** This module ends at equilibrium binding. A filter
also needs the wash to remove copper and keep gold, and [ISSUES.md](ISSUES.md)
records the Au-S bond in GolB at 165 pN, about six times weaker than Au-S on a
gold surface. Gold loss during washing is a live risk, so neither wash
retention can be assumed.

## 6. What the wet lab must measure

No binding constants are needed first. Run the intended sequence once and
measure gold and copper by ICP-MS in four liquids: the filtered leachate, the
liquid after capture, the combined wash, and the final eluate. That yields the
gold and copper capture fractions, the two wash retentions, and the eluate
enrichment. Label the eluate ratio an enrichment factor; it is not the
separation factor of section 2, because it carries the wash and the elution
too.

Add copper oxidation state as an arm, because sections 4 and 5 are different
experiments. Cu(I)-thiosulfate under nitrogen tests competition. Cu(II) tests
damage. A DTNB free-thiol count on the washed cells, with a DTT rescue,
separates the two directly.

## 7. Status

- K_Cu has no adopted GolB measurement. The labelled working scenario uses
  alpha = 52 and derives K_Cu = 36.4 µM from K_Au = 0.7 µM.
- `whole_cell_capacity` stays null. The 4.62 µmol/g used above is
  `params/capture_design.yaml :: literature.wei2012_loading`, a single endpoint
  measured with Au(III) chloride in growing cells, and it is a scenario label.
- Every capture number in this file is conditional on alpha and on
  K_Au = 0.7 µmol/L, the GolB-based literature proxy recorded in
  [ISSUES.md](ISSUES.md) item 1 and [S78](SOURCES.md).
