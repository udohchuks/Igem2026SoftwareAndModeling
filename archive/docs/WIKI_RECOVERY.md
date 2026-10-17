---
title: "Wiki proposal: from dissolved gold to metal"
date: "2026-09-06"
---

**Tier 3, synthesis.** Proposed recovery-only wiki copy for the team to adapt.
This is a draft, not a record of completed experiments. Its results are
conditional simulations. Technical detail and the audit are in
[RECOVERY.md](RECOVERY.md); the corrections are in [ISSUES.md](ISSUES.md),
items 84–89. The existing site plan is [WIKI_PLAN.md](WIKI_PLAN.md).

# From dissolved gold to metal

## Our question

Gold dissolved during leaching is not yet a product. It must bind to our
engineered cells, be released into a suitable solution, and then be reduced
to metal. We modelled these stages together to ask: **which stage limits the
amount of metal formed, and what should we measure before improving the process?**

Our recovery model starts with dissolved gold supplied by the leaching model.
The surface-display model supplies the estimated gold-binding capacity.
We keep track of gold through capture, elution and reduction, so an improvement
in one stage cannot be mistaken for an improvement in the entire chain.
The boundary ends at metal formation; particle collection is not modelled.

## What the reference calculation tells us

At a feed of 29 µM gold and biomass of 5 g dry weight/L, the display model
provides approximately 0.457 µM binding sites. Accounting for equilibrium and
gold conservation gives approximately 0.455 µM bound gold, or 1.57 % of the
feed. The reference wash transfers approximately 0.365 µmol of gold per
initial litre to reduction.

![The conditional reference mass balance from feed to metal. Amounts are shown per initial litre on a logarithmic axis. The final bar assumes the reference kinetic proxy and excludes collection.](media/recovery/figR8_stage_balance.png)

The calculation assumes equal stage volumes, quantitative transfers and the
target protein dose. It predicts approximately 1.26 % of feed gold reaching
metal **under the reference reduction kinetics**. It is not a measured process
yield: the model can give much less metal when the reduction kinetics change.

## Capture: count the sites before improving the rate

We combined a Langmuir binding model with a gold mass balance. This matters
because the isotherm uses free gold, not all the gold added. Using total gold
in its place can predict more bound gold than exists.

![Capture shown as both bound amount and fraction of feed. Increasing feed eventually fills the modelled sites; further gold stays in solution.](media/recovery/figR1_capture_regimes.png)

At our reference feed, the modelled sites are nearly full. This suggests
measuring active binding capacity and accessible biomass before investing in
faster binding. Increasing the fraction captured by dilution is a different
objective from increasing gold recovered per original litre, and we keep
those quantities separate.

The capacity is an expression-model estimate, not a measurement of our capture
vessel. Unmodified cells may also bind gold, and the leachate may inhibit the
engineered binding sites. Our validation priority is therefore to compare
engineered cells, unmodified cells and a cell-free blank in representative
leachate, while measuring both dissolved and cell-associated gold.

## Elution: a faster wash and a better endpoint are different improvements

We describe elution with an empirical model containing an elutable fraction
and a rate of approach to it. At the reference settings, the 6 h wash releases
80.3 % of captured gold. Longer washing approaches the assumed endpoint;
it cannot overcome that endpoint within this model.

![Candidate elution curves distinguish the endpoint from the time needed to approach it. These are scenario curves, not fitted experimental data.](media/recovery/figR4_elution.png)

We retain pseudo-second-order and first-order curves as hypotheses to compare
with data. Neither establishes a molecular mechanism, and published rate
constants may not transfer between loadings and materials
[Bullen et al.](https://doi.org/10.1021/acs.langmuir.1c00142).
An elution time course at the intended loading will test the curve shape and
endpoint. The eluate must also support reduction: better desorption is useful
only if the released gold can complete the next stage.

## Reduction: an uncertain step, not a solved one

Our reduction model represents nucleation, autocatalytic growth and a finite
electron supply. It conserves gold, tracks protein redox states and excludes
added seed particles from newly formed metal. The electron inventory provides
a necessary ceiling, but sufficient electrons do not guarantee fast conversion.

![Reduction after 24 h across both declared kinetic ranges. The star marks the reference proxy. The colour shows simulated conversion, not a probability or confidence level.](media/recovery/figR5_reduction_threshold.png)

The reference kinetic choice predicts nearly complete conversion. At the slow
corner of the declared ranges, only approximately 0.12 % of the eluate converts
after 24 h. This difference changes our interpretation: **the model cannot yet
establish that reduction will be complete in our process.**

The reference nucleation estimate transfers electron-transfer kinetics from a
different enzyme into a particle-formation model. Our eluate also differs from
the Au(III) substrate used in the project's protein study
[Erasmus et al.](https://doi.org/10.1007/s11756-024-01733-2).
These are explicit hypotheses to test, not measured properties of our vessel.

We propose time courses using the actual eluate chemistry, with chemical and
protein controls. Quantitative gold measurements and product characterization
will separate disappearance from solution from formation of metal. Optical
spectra are useful alongside those measurements, but particle size changes the
optical response [Haiss et al.](https://doi.org/10.1021/ac0702084).
The fitting routine therefore requires calibrated data and never assumes that
the largest observed signal represents complete conversion.

## How the model guides the next iteration

The model identifies two immediate priorities: measure effective capture
capacity in leachate and measure reduction in the actual eluate. An elution
time course connects those stages. Active-protein measurements over culture
time are also needed before recommending a harvest schedule.

We have verified conservation and numerical behaviour, and corrected errors
found during review. We have not yet validated recovery predictions against
our team's experiments. The next iteration should fit parameters using one
set of conditions, test predictions on a held-out condition, and document
whether that evidence changes biomass, wash or reduction choices.

The code, parameter provenance and regeneration instructions accompany the
[technical report](RECOVERY.md). Sharing both what the model predicts and what
it cannot yet establish makes it useful for subsequent teams as well as our own.

---

## Editorial notes for the team

The copy above deliberately makes no claim that proposed experiments have been
performed. Before publication, replace internal file links with the team's
actual code and model-page links; add contributor attribution and experimental
results only when available. The [official model rubric](https://competition.igem.org/judging/special-prizes)
rewards useful modelling and relevant data, not simply a large equation count.

Keep all four figures if space allows. If space is limited, prioritise the
capture and reduction panels, and turn the stage balance into a compact table.
Keep full derivations and parameter records downloadable. Do not use the old
capture-harvest, reductase-harvest or historical PRCC graphics as current results.
