---
title: "Wiki content — Model section"
date: "2026-09-07"
---

# What this file is

**Tier 3, synthesis.** Draft judge-facing copy for the Model section, following
the eight-page structure in [WIKI_PLAN.md](WIKI_PLAN.md). The rubric and survey
are in [WIKI_DESIGN.md](WIKI_DESIGN.md) and [WIKI_SURVEY.md](WIKI_SURVEY.md).
`AGENTS.md` section 11.

This file commits the narrative spine and page-level finding lines. It is not
the scientific source of record. Numbers and current technical interpretation
come from [REVIEW.md](REVIEW.md), [RECOVERY_MODEL.md](RECOVERY_MODEL.md) and
`params/*.yaml` when pages are built.

The former nine-cell outline was superseded on 2026-09-07. The current plan
uses eight pages: one hub, five scientific chapters, one integration page and
one evidence appendix.

---

# Page 1 — Model overview

## Title

**Can biology recover gold from electronic waste?**

## Introduction

Gold recovery is not one reaction. It is a chain: make the leachant, dissolve
gold from a copper-rich circuit board, capture the dissolved gold, release it
from the capture cells and turn it back into metal. An improvement in one step
matters only if the next step can accept what it produces.

We modelled that chain from crushed printed circuit board to newly formed
metal. At each boundary we asked the same question: **can this stage
successfully hand the gold to the next one?** The answer exposed both a
low-cost operating opportunity and several assumptions that must be tested
before the process can support a yield claim.

## Under the process diagram

Gold follows the central material path. TetH, GolB and the reductase are made
in separate biological supply arms and enter only where their function is
needed. Select a stage to see its model, evidence and next experiment.

## Three questions

1. Can we biologically produce and protect the leachant?
2. Can GolB capture gold from the actual leach liquor?
3. Can the recovered gold be converted back into metal?

## Four findings

### Less oxygen may recover more gold

Oxygen helps regenerate the copper species that drives leaching, but excess
oxygen also sustains the copper loop that destroys thiosulfate. The model
therefore predicts an optimum to test, not a reason to maximise aeration.

### TetH activity is the first feasibility gate

The conversion equations can describe how active TetH makes thiosulfate. They
cannot establish that the enzyme folds, survives recovery and remains active
under the intended process conditions. That activity must be demonstrated
before the vessel is sized.

### Displayed-site counts are not measured whole-cell capacity

The expression model supplies a conditional inventory of engineered binding
sites. It does not measure all gold associated with a whole cell, background
adsorption or loss of activity in leachate. The decisive quantity is effective
capacity in the real process matrix.

### Reduction could be fast or nearly stall

The reference kinetic proxy gives a favourable trajectory, but the full
declared parameter range contains very low conversion within the batch. The
result is a scenario map, not a confidence interval and not an expected yield.

## How to read this section

Read the five chapters in process order to follow the gold. Each chapter opens
with a question and keeps its finding visible. Open Model and Assumptions for
the working. Finish with **Gold Recovery 2.0** to see what the combined model
changed, and use **Evidence and technical resources** to audit the work.

## Scope

**Every recovery result is conditional.** The model ends when new metallic
gold forms. Physical collection, washing, ashing, particle size and product
purity are outside its boundary.

## Current judgment

The model has not yet proved a process yield. It has prevented the team from
optimising the wrong things.

---

# Pages 2–6 — finding lines and project consequences

These lines remain visible when technical detail is closed.

| Page | Finding line | Project consequence | Decision state |
|---:|---|---|---|
| 2. Making the leachant | TetH production, not reaction speed, is the first feasibility gate. | Demonstrate active enzyme before sizing the vessel. | blocked |
| 3. Dissolving the gold | Copper chemistry controls the leach, and oxygen is the cheapest available handle. | Meter air, control pH and test the predicted oxygen response. | proposed for testing |
| 4. Leach to capture | Successful leaching does not guarantee compatible capture. | Test the complete liquor and evaluate conditioning if binding is impaired. | blocked |
| 5. Capturing the gold | Site counting gives a conditional capacity, not a measured whole-cell ceiling. | Measure effective whole-cell capacity in representative leachate. | proposed for testing |
| 6. Returning to metal | Recovery is a sequence: release the gold, then prove it forms metal. | Fit elution and reduction in the intended matrices before quoting yield. | proposed for testing |

Each page follows the same order:

1. Question.
2. In plain language.
3. Model and assumptions.
4. Finding.
5. Project impact.
6. Next experiment.

---

# Page 7 — Gold Recovery 2.0

## Opening

The model did not merely describe the process. It changed the process we would
build.

The first concept treated active TetH, direct transfer into capture,
engineered-site capacity and reference reduction kinetics as workable inputs.
Following the gold through the full chain changed that interpretation. The
next design must validate the enzyme before scale-up, control oxygen rather
than maximise it, treat the leach-to-capture boundary as a compatibility gate,
measure whole-cell capacity in leachate and report recovery as conditional
until the actual eluate kinetics are known.

## Impact on hardware

The leach needs controlled aeration and pH dosing. Their purpose is not merely
automation: they hold the process near conditions selected by the coupled gold,
copper and thiosulfate balances. Exact hardware claims remain provisional
until the team names the implemented devices and their operating ranges.

## Impact on wet lab

The model ranks experiments by the decision each one resolves:

1. Active TetH after the intended expression and recovery procedure.
2. GolB capacity and background adsorption in representative leachate.
3. Capture compatibility with the sulfur species delivered by the leach.
4. Reduction time courses in the actual eluate with chemical and protein
   controls and an independent metal measurement.
5. Elution time courses at the intended loading.
6. Otherwise identical leaches at two oxygen levels.

## Impact on modelling

Unknown experimental quantities stay unknown. Effective whole-cell capacity,
matrix damage and fitted recovery kinetics are not replaced by guesses. When
the measurements arrive, they update the same parameter records and interfaces
used by the current model.

## Closing

The next iteration is therefore not “improve every stage.” It is to resolve
the feasibility gates first, then optimise only the stages that remain
limiting in the measured system.

---

# Page 8 — Evidence and technical resources

## Evidence levels

### Verified internally

Conservation, unit conversions, numerical behaviour and recomputation across
model interfaces are checked in the repository.

### Supported externally

Literature measurements and transferred kinetic proxies are individually
labelled with their sources and transfer limitations.

### Not yet validated

Performance in the team’s strains, leachate and eluate has not been measured.
These gaps become the ranked experimental programme rather than hidden error
bars.

## Builder note

Generate equations, parameter tables, evidence labels and references from the
repository sources. Do not hand-copy scientific values into this file. Replace
internal file links with final wiki routes and add contributor attribution
before publication.

## Presentation correspondence

Use the same page names, finding lines and figures in the oral presentation.
The spoken sequence is problem, system, question, five discoveries, changed
design, current judgment and next evidence. A judge should recognise every
presentation beat when opening the corresponding wiki page.
