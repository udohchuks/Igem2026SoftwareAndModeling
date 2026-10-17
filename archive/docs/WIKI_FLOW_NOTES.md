---
title: "Wiki write-up — agreed flow"
date: "2026-09-10"
---

# Recovering Gold from E-waste

**Tier 3, synthesis.** This file records the agreed writing flow for the wiki
team: page order, repeated model-section structure and visual approval steps.
It is a planning document, not public wiki copy or a source for scientific
values. Current values remain in `params/*.yaml`.

## Opening question

**Can engineered *E. coli* effectively recover gold from electronic waste?**

*Annotation: The entire page should work towards answering this question.*

## 1. Introduction

*Annotation: Briefly establish the e-waste problem, introduce our engineered
E. coli recovery system, explain why modelling was needed to assess its
feasibility, and tell the reader that the models follow gold through the
complete recovery process.*

## 2. Process overview

*Annotation: Present the main process diagram before explaining the individual
models.*

The diagram should:

- Follow the movement of gold through the system.
- Distinguish that journey from the biological components supporting each
  stage.
- Show how the stages and models connect.
- Make the inputs and outputs between stages visible.
- Potentially compare our biological process with the conventional process,
  although we have not yet decided whether that belongs here or in a separate
  graphic.

A side content menu begins here and follows the same process order:

- Process overview
- Making the leachant
- Dissolving the gold
- Leach-to-capture handover
- Capturing the gold
- Releasing the gold
- Returning gold to metal
- Integrated recovery
- Final judgment

## 3. Making the leachant

*Annotation: Explain the model responsible for the biological production of
the leaching agent.*

## 4. Dissolving the gold

*Annotation: Explain how the model predicts the release of gold from the
electronic waste.*

Agreed Stage 2 flow:

- Answer from the start: gold dissolves only during a productive window before
  copper-driven chemistry exhausts the usable thiosulfate.
- Use the supplied document's ammoniacal process, including 266 mM ammonia and
  the current one-day batch decision.
- Animate the desired gold pathway and competing copper redox loop.
- Use one time-course figure for the productive window and one oxygen sweep for
  the aeration decision; titles and interpretation sit below the figures.
- Keep complete balances, assumptions, parameters, checks and an experimental-
  evidence placeholder in dropdowns.
- End with a process-stream handover to capture.

## 5. Leach-to-capture handover

*Annotation: State the quantity leaving the leaching model, its unit, its
uncertainty or evidence status, and the conditions under which the capture
model can accept it.*

## 6. Capturing the gold

*Annotation: Explain how the engineered cells capture the dissolved gold.*

## 7. Releasing the gold

*Annotation: Explain how the captured gold is released for the next recovery
stage.*

## 8. Returning gold to metal

*Annotation: Explain the reduction of the released gold into its metallic
form.*

## 9. Integrated recovery

*Annotation: Reconnect the individual models and evaluate the complete recovery
chain.*

Include:

- A system-level visualization.
- The transfer of gold between every stage.
- Losses or limitations across the chain.
- The combined recovery outcome.
- The stages or parameters that most strongly control overall performance.

## 10. Final judgment

*Annotation: Return directly to the opening question.*

The ending should:

- Give a clear answer based on the combined evidence.
- Distinguish demonstrated results from predictions and scenarios.
- State the important limitations honestly.
- Separate what the models have already changed from recommended experiments
  and longer-term possibilities.

# Repeated structure inside each model

Every model section should follow the same internal pattern:

## 1. Compact model summary

- Inputs
- Outputs
- Principal assumptions

## 2. Why this stage matters

- Its role in the gold-recovery process
- What or whom the model informs

## 3. Model question

- The specific question being answered

## 4. Success criterion

- The quantity used to judge success
- What outcome counts as success
- Whether the criterion is measured, sourced or assumed

## 5. Model setup and assumptions

- Relevant conditions
- Important parameters
- Evidence status of each input

## 6. Governing equation

- Meaning in words
- Equation
- Symbols and units
- Why the equation matters

## 7. Results and graphs

- The finding
- The supporting graph
- Validation using experiments, literature or controls

## 8. Effect on the project

- What the model changed
- The operating condition, design choice or experimental time point it
  recommends

## 9. Wet-lab and software connection

- Relevant experiment
- Direct access to the implementation
- Parameter sources and graph data where appropriate

## 10. Next experiment

- The uncertainty or limitation to test next
- Clearly separated from completed work

## 11. Handover

- Quantity passed to the next model
- Unit
- Evidence status or uncertainty
- Required receiving conditions

## 12. Concise summary

- The main conclusion for readers who do not follow every equation

# Technical reading levels

## Main page

Only include the equations, assumptions and results needed to understand the
argument.

## Expandable technical sections

Place beneath the relevant model:

- Supporting equations
- Additional assumptions
- Derivations
- Initial and boundary conditions
- Numerical methods
- Parameter sources
- Model checks
- Technical diagnostic graphs

## Technical appendix

Include:

- Complete equation sets
- Long derivations
- Full parameter tables
- Unit conversions
- Implementation details
- Software links

# Graph rules

Every main graph must answer a question or justify a project decision.

Graphs should:

- Appear beside the claim they support.
- Show changes over time when the process is dynamic.
- Compare operating conditions when selecting a design.
- Show influential parameters and sensitivity.
- Use spatial views when movement or transfer matters.
- Place validation beside the prediction being validated.
- Use headings and captions that state the finding.
- Keep diagnostic plots in the deeper technical layer.

# Evidence rules

Throughout the page, visibly distinguish:

- Experimental measurements
- Literature values
- Derived parameters
- Assumptions
- Model predictions
- Scenarios
- Theoretical upper bounds

# Collaborative writing process

Work through the wiki one stage at a time:

1. State the current stage.
2. Gather the user's initial thoughts.
3. Draft that stage.
4. Let the user review and correct the draft.
5. Add it to the main wiki write-up only after approval.

Complete the planning for plots and diagrams before beginning the written
sections.

# Visual production plan

## Plots

- Keep plots simple, clear and visually polished.
- Avoid placing too many quantities, comparisons or messages in one graph.
- Each main plot should answer one question or support one project decision.
- Move technical or crowded diagnostic plots to the deeper technical layer.
- Produce data-based plots with Python plotting tools and export them as SVG.
- Create a PNG fallback only if the wiki requires one.
- Use interactive plots only when interaction materially improves the reader's
  understanding.

## Diagrams and SVG assets

- Use original, editable SVG assets for the process diagram, model handovers
  and biological explanations.
- Propose each SVG concept before creating the finished asset.
- Let the user approve the proposal and help refine it before production.
- Use a consistent visual system across the assets, including colours,
  typography, arrows and evidence markers.
- Keep labels as real SVG text where possible so they remain sharp and
  accessible.
- Use simple diagram drafts or wireframes to agree on relationships before
  producing polished SVGs.
- Use generated imagery only for early visual exploration, not for final
  scientific diagrams that require exact labels and details.

## Motion and animation

- Look for useful animation opportunities while designing every stage.
- Animate material movement, state changes or model behaviour when motion makes
  the explanation clearer.
- Keep animation smooth, restrained and consistent with the shared visual
  system.
- Agree on the question and purpose before producing an animated asset.
- Provide a clear static state and respect reduced-motion preferences.

## Visual inventory

Before creating a plot or diagram, agree on:

1. The question it answers.
2. The information or data it needs.
3. The most suitable visual form.
4. Where it belongs in the write-up.
5. Whether it is part of the main story or supporting technical material.
