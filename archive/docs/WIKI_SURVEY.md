---
title: "Wiki survey — how strong teams present a hard process"
date: "2026-09-07"
---

# What this file is

**Tier 3, synthesis.** The evidence base under
[WIKI_DESIGN.md](WIKI_DESIGN.md). This file records what other teams did and
what it cost them to do it; `WIKI_DESIGN.md` turns that into our rubric,
[WIKI_PLAN.md](WIKI_PLAN.md) commits a layout, and
[WIKI_CONTENT.md](WIKI_CONTENT.md) writes the copy. Read them in that order.
`AGENTS.md` section 11.

Twenty-nine pages across twenty-seven teams were opened and read on
2026-09-06, spanning 2013 to 2025. Five more returned 404 or 504 and are
recorded in section 1. Every heading list quoted below was taken from the live
page on that date, **with two exceptions named in section 4**: SCUT-China-L
2025 and IISc-Software 2024 were not opened, and both are carried forward from
the earlier survey in [WIKI_DESIGN.md](WIKI_DESIGN.md) section 1.

**This file carries no model numbers.** Our numbers live in
[REVIEW.md](REVIEW.md) and `params/*.yaml`, and a number copied into a survey
would be a second home for a fact that already has one. Everything here is
wiki craft: flow, structure, headings, and the order a reader meets things in.

**It is not a layout.** It proposes no page map and commits nothing. That is
[WIKI_PLAN.md](WIKI_PLAN.md) section 3.

---

# 1. Method, and what it cannot tell us

Award records came from the iGEM results site, `competition.igem.org/results`.
That site serves a Special Prizes tab for 2019 and for 2022 onward. It serves
none for 2016, so **the Best Model record before 2019 was not retrievable and
is not guessed here.** Pages from 2013 to 2018 in this survey were chosen by
subject, not by award.

Two pages were opened and found empty of usable structure: AshesiGhana 2025
publishes no Model page, and Stuttgart 2025 publishes one equation. Both are
recorded because a negative result is still a result.

**What was not read.** Five requests failed. Four were 404s for a Model page
that does not exist, at MSP-Maastricht 2025, Stuttgart 2025 under that path,
AshesiGhana 2025 and EPFL 2025; in each case the correct page was found from
the site navigation and read instead. The fifth is
**GO-Paris-Saclay 2019**, the overgraduate Best Model winner that year. The
2019 wiki server returned 504 on every attempt, so that page is named in the
award table below and nowhere else. It remains the one award winner in this
survey whose page we have not seen.

## The Best Model record

| Year | Undergrad | Overgrad | High school |
|---|---|---|---|
| 2025 | Peking | Heidelberg | GreatBay-SCIE |
| 2024 | Heidelberg | UToronto | IEA |
| 2023 | ZJU-China | Toronto | BJEA-China |
| 2022 | TU-Eindhoven | TAU-Israel | GEMS-Taiwan |
| 2019 | NCKU-Tainan | GO-Paris-Saclay | GENAS-China |

## The 2025 presentation record

Best Wiki went to EPFL and MSP-Maastricht jointly in the undergraduate
division, and to Munich in the overgraduate division. Best Presentation went
to EPFL and TU-Eindhoven, and to Brno Czech Republic. Rochester, TU-Eindhoven,
Heidelberg, DTU-Denmark and AshesiGhana were among the Best Wiki nominees.

Two teams appear in both records in the same year: EPFL and TU-Eindhoven. Both
are read below for flow rather than for mathematics.

---

# 2. Eight things the strong pages have in common

Ordered by what they would change about our pages, most first.

**1. The page follows the substance, not the mathematics.**
Peking 2025 runs eight models in the order a drug particle meets them:
dissolution, propulsion, diffusion, penetration, binding, signalling,
transport, outcome. ZJU-China 2023 numbers four models along the journey of a
plant virus, wind field to antibody. Sheffield 2023 splits a bioreactor by
subsystem, and one of its six subsystems is aeration. None of the three
organises by technique.

**2. One template, repeated on every model, without variation.**
Peking 2025 repeats Background, Model Assumptions, Mathematical Model,
Results, eight times. Rochester 2025 repeats Introduction, Methods,
Assumptions, Results, Impact, Future Experiments, Summary, References, four
times. The repetition is what makes the fourth model fast to read.

**3. Assumptions is a heading, never a paragraph.**
Present as its own heading on Rochester 2025, Peking 2025, TU-Eindhoven 2022,
Cornell 2024 and William-and-Mary 2023. Heidelberg 2024 names it **Core
Assumptions** and places it in the introduction, before any result.

**4. Result headings state the finding as a sentence.**
Heidelberg 2024 is the clearest case. Its result subheadings read *Plasmid
Proximity is Not Sustained Without a Staple*, *Simulated Binding Energy
Matches Experimental EMSA Data*, and *Cas Staple Forces do Not Disturb DNA
Strand Integrity*. A judge who reads only the headings still leaves with the
answers.

**5. Every model closes by naming what it changed, and who it changed it for.**
Rochester 2025 uses **Impact on Hardware**, **Impact on Wet Lab** and **Impact
on Policy and Practice**. Munich 2025 splits its conclusion into **Drylab
Impact** and **Wetlab Impact**. TU-Eindhoven 2025 ends on **Integration into
Project**. Heidelberg 2025 gives the subject a whole section, **Model-guided
PHOENICS Cell Design**. Toulouse-INSA-UPS 2023 gives it a page, *Liposome
2.0*, whose only job is the modifications the model forced.

**6. Validation and limits are headings, not apologies.**
TU-Eindhoven 2022 runs **Model validation** with two subheadings, **Internal
correctness** and **The system behavior**, then a multiple-parameter
sensitivity analysis, then **Improvement** and **Outlook**. William-and-Mary
2023 runs **Validating the Computation** before it runs Results. UToronto 2024
carries **Limitations** and **Next Steps** inside its Discussion. Heidelberg
2025 closes on **Limitations and The Road Ahead**.

**7. Depth is tiered, and the tier is visible.**
UToronto 2024 pushes training details, hyperparameters and hardware into an
**Appendix** and keeps the body to a paper. Rochester 2025 moves its two-axis
derivation to the end and links its solver repository. Toulouse-INSA-UPS 2023
splits one model across four pages from a hub. IISER-Berhampur 2025 gives one
equation a page.

**8. Plain language comes before mathematics, on every page.**
Peking 2025 opens with the patient problem and reaches its first equation
several paragraphs later. Heidelberg 2024 carries a named block, *DaVinci in a
Nutshell*, and repeats it. EPFL 2025 puts a one-line subtitle under the page
title saying what the page is for. MSP-Maastricht 2025 runs **Problem**,
**Solution** and **Description** on its project pages, and opens with a
question addressed to the reader.

---

# 3. The pages, and what we take from each

Read in the order most useful to us. The right column is the action, in our
terms.

## Story shape

| Team | What they did | How we emulate it |
|---|---|---|
| **Heidelberg 2013**, gold from electronic waste | Page title is a question, *Would It Be Feasible?* Opens on **Highlights**, four one-line claims. Closes on **Final judgment**, then **Outlook**. The judgment states the shortfall in orders of magnitude and does not soften it. | The nearest match to our position in the whole survey. Page 1 takes a four-finding Highlights block and a Current judgment. The capture statement uses the corrected scope in [ISSUES.md](ISSUES.md) item 92. |
| **Peking 2025**, Best Model | Eight stage models in physical order, one repeated four-heading template, a plain-language opening. | Pages 2–6 follow the material journey and repeat one six-part template. The leach-to-capture interface is a chapter because its composition can stop the chain. |
| **Heidelberg 2025**, Best Model | Per-layer models, **Sensing Layer** then **Processing Layer**, then **Integrated Modeling**, then a section for the design changes. | Page 7 is the integration: it reunites the five focused chapters as the model-informed Gold Recovery 2.0 design. |
| **Toulouse-INSA-UPS 2023**, Best Model nominee | A hub page names its four sub-pages in four lines, calls the process a cascade, then poses the three questions the model must answer. | Page 1 poses three questions and links Pages 2–8. Questions read better than a contents list, and they commit us to answering. |

## Structure and template

| Team | What they did | How we emulate it |
|---|---|---|
| **Rochester 2025**, Best Wiki nominee | Seven or eight fixed headings per model, one of them **Impact on** a named team. Sticky sidebar over four long sections. Derivations at the end. | Pages 2–6 repeat Question, Plain language, Model and assumptions, Finding, Project impact and Next experiment. Page 7 splits impact into hardware, wet lab and modelling. |
| **UToronto 2024**, Best Model | The page is a paper: Abstract, Background, Objectives, Methods, Discussion, Limitations, Next Steps, Conclusion, References, Appendix. | We already hold [REVIEW.md](REVIEW.md) in this shape. The deep-dive pages can be near-direct lifts, with the heavy tables moved into an appendix. |
| **TU-Eindhoven 2025**, Best Wiki and Best Presentation nominee | Five headings only: Introduction, Model Description, Evaluation, Results, **Integration into Project**. | The floor. A short chapter may combine Plain language with Question, but it must retain Finding, Project impact and Next experiment. |
| **Cornell 2024** | An **Executive Summary** opens each model, and a named **Conclusion** for that model closes it. | Each page opens on its project question and closes on its named project consequence, so the five conclusions do not blur together. |
| **KULeuven 2024**, metal binding | A numbered five-step pipeline: selection, baseline assessment, optimisation, verification, machine learning. | Number Pages 2–6 along the material journey in the navigation and presentation. Page 7 visibly reunites them. |

## Honesty, where we have no measurements

| Team | What they did | How we emulate it |
|---|---|---|
| **TU-Eindhoven 2022**, Best Model | **Model validation**, then **Internal correctness** and **The system behavior**. They check the model against itself, and against expected behaviour, before any parameter study. | This is the substitute for wet-lab validation, and the work is already done: the leach rebuild matched every number the source reports and closed three mass balances the source does not test. That belongs under an Internal correctness heading, not in a footnote. |
| **Calgary 2021**, electronic-waste metal recovery | A **Pessimistic-Optimistic** workflow brackets each model with a worst and a best case. **Modelling Goals** are written as the questions that arose, one of them being how to give the wet lab better estimates. | Bracket every blocked parameter instead of quoting one value. A bracket is honest where a point estimate is not. |
| **William-and-Mary 2023**, Best Model nominee | Reviews prior modelling in the introduction. Closes on **How to Use Our Model** and **Contributions to the Field**. | Our deliverable is a ranked list of what to measure, so *How to Use Our Model* is its natural home. |
| **IISER-Berhampur 2025**, competitive Langmuir | Under each equation, one line per symbol: meaning, then units, the sink term included. A section, **Facts Regarding Our Math Model**, answers four questions as Q&A. | The capture page takes both. The Q&A pre-empts the questions a judge asks about the isotherm and the elution law. |

## Flow and presentation

| Team | What they did | How we emulate it |
|---|---|---|
| **EPFL 2025**, Best Wiki and Best Presentation | A one-line subtitle under every page title, saying what the page is for. A visible table of contents at the top of the page body, not only in the chrome. Pages close on *Future Directions & Conclusion*. | One sentence under each of the nine cell headers. It costs nine sentences and it tells a lost reader where they are. |
| **MSP-Maastricht 2025**, Best Wiki | Project pages run **Problem**, **Solution**, **Description**. The opening line is a question to the reader. Wet-lab work is organised as **DBTL Cycle 1, 2 and 3**, each with dated attempts and a closing **Lessons & Integration into DBTL**. Failed attempts are numbered and shown, not hidden. | Two things. Open the Overview with a question, not a definition. Present the three-vessel rebuild as a cycle with its failures visible, because the three-vessel route exists only because the single-vessel route could not work. |
| **Munich 2025**, Best Wiki | The conclusion splits into **Drylab Impact** and **Wetlab Impact**. A section is named for the problem it solves, not the method it uses. | Split our closing section the same way. The wet lab reads one half and the modellers read the other. |
| **Heidelberg 2024**, Best Model and Grand Prize | Result headings are findings. A named summary block repeats near the top. | The cheapest change in this document. Rewrite every results heading on every page as a sentence that states the finding. |

## Same subject, weaker execution

| Team | What we found |
|---|---|
| **Athens 2024**, *e-PHAESTUS* | The closest process twin in iGEM: engineered *E. coli* makes glutathione, which leaches electronic waste and forms metal nanoparticles. The Model page carries four sections, no assumptions heading and no results template. Cite them as prior art; do not copy the page. |
| **AshesiGhana 2023 and 2025** | The 2023 Model page describes direct and indirect bioleaching mechanisms and stops. The 2025 wiki was a Best Wiki nominee and publishes no Model page at all. A Ghanaian precedent exists; a modelling precedent does not. |
| **Stuttgart 2025**, platinum-group metals | One oxalate equation on the Modeling page. A close subject, no transferable structure. |
| **NCKU-Tainan 2019**, Best Model | Overview, a co-culture model in two scenarios, a bacteriocin model. Clear, but too thin a template for nine stages. |

## Read, and set aside

Both were opened in full. Neither models a physical process, so neither offers
a template we can use. They are recorded so that the survey states what it
rejected as well as what it took.

| Team | What we found |
|---|---|
| **TAU-Israel 2022**, Best Model, overgrad | A sequence-design pipeline: a linear-regression metric for toehold efficiency, trigger selection, pseudoknot avoidance, immune-response avoidance, codon optimisation. Excellent of its kind, and entirely a software pipeline. No stages, no assumptions heading, nothing to carry across. |
| **DTU-Denmark 2025**, Best Model nominee and Best Wiki nominee | A protein-design pipeline built around a generative model, with rounds of single and multiple mutations and a closing catalogue of the other tools used. Same verdict as TAU-Israel 2022. |

---

# 4. What not to copy

Items 1 and 2 name SCUT-China-L 2025 and IISc-Software 2024. **Neither was
opened for this survey.** Both findings are carried forward from the earlier
survey in [WIKI_DESIGN.md](WIKI_DESIGN.md) section 1 and have not been
re-checked against the live pages. The Rochester half of item 1 was checked.

1. **Equations as images.** Rochester 2025 and SCUT-China-L 2025 both render
   equations as pictures. Images do not scale, do not copy, and are not read
   aloud by a screen reader. Render LaTeX. This confirms
   [WIKI_DESIGN.md](WIKI_DESIGN.md) section 1.
2. **A model page carrying two figures.** IISc-Software 2024 did, and it reads
   as an essay about a model rather than a model.
3. **Describing modelling instead of showing a model.** The failure mode named
   in [WIKI_DESIGN.md](WIKI_DESIGN.md) section 1. Nothing in this survey
   changes that verdict.
4. **A dated laboratory log presented as results.** MSP-Maastricht 2025 wins
   Best Wiki with its failures visible, but its Workflow and Results page runs
   to roughly forty dated attempt headings. Take the cycle and take the
   visible failures. Keep the log on its own page.

---

# 5. Corrections this survey forces on WIKI_DESIGN.md

Two entries in the survey table at [WIKI_DESIGN.md](WIKI_DESIGN.md) section 1
do not match the live pages, checked 2026-09-06.

1. **KULeuven, metal recovery, is 2024 and not 2025.** KULeuven 2025 is a cacao
   biocontrol project built around *Phytophthora* sensing and antimicrobial
   peptides. The metal-binding project, whose Model page is the numbered
   five-step pipeline described in section 3 above, is KULeuven 2024. The
   embedded-simulation observation still holds for 2025, which carries a
   NetLogo agent-based model walked through four named scenarios.
2. **Rochester 2025 runs seven or eight headings, not six.** The live headings
   are Introduction, Methods, Assumptions, Results, Impact on a named team,
   Future Experiments, Summary and References. Two of the four models omit
   Future Experiments. That omitted heading is one we want.

Neither correction changes a model number, so neither is an `ISSUES.md` item
under `AGENTS.md` section 1. Both are recorded here and are due in
`WIKI_DESIGN.md` at its next revision.
