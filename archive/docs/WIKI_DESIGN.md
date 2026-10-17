---
title: "Wiki design proposal — the Model pages"
date: "2026-09-07"
---

# What this file is

**Tier 3, synthesis.** First of three: this sets the rubric and the survey,
[WIKI_PLAN.md](WIKI_PLAN.md) commits a layout, [WIKI_CONTENT.md](WIKI_CONTENT.md)
writes the copy. Read them in that order. `AGENTS.md` section 11.

A design proposal for the Model section of the team wiki. It maps the
end-to-end model in `docs/MASTER.md` onto a page structure a judge can read in
ten minutes and a modeller can audit in an hour.

Source documents are unchanged. This file proposes presentation only.

---

# 1. What winning model pages do

Surveyed nine model pages, 2023-2025. Grand Prize and Best Model contenders
first, then pages whose subject matter matches ours.

| Team | Why it was read | The design choice worth copying |
|---|---|---|
| Heidelberg 2024 | Grand Prize | Every model claim names the wet-lab test that checked it |
| Rochester 2025 | Bioreactor ODEs, closest to Part I | Six fixed headings per model, one of them Assumptions |
| Cornell 2024 | Michaelis-Menten plus CSTR scale-up | Assumptions as a numbered list in its own subsection |
| SCUT-China-L 2025 | Fermentation ODEs plus techno-economics | Parameter tables carry symbol, value, unit and citation |
| IISER-Berhampur 2025 | Competitive Langmuir, our capture stage | One hard equation gets one page of its own |
| TU-Eindhoven 2024 | Modelling special prize | A worked example walked end to end through the pipeline |
| KULeuven 2025 | Metal recovery | Embedded simulation the reader can run |
| UZurich 2024 | Flux balance | An explicit Assumptions and Limitations section |
| IISc-Software 2024 | Self-nominated Best Model | A named "Key highlights" block aimed at the judge |
| UNT 2024 | The counter-example | It described modelling instead of showing a model |

**Five choices recur across the strong pages.**

1. A fixed section template, repeated for every model. Rochester runs
   introduction, methods, assumptions, results, impact, summary.
2. Assumptions get their own heading, numbered, not buried in prose.
3. Parameter tables carry four columns: symbol, value, unit, source. Rochester
   marks its guesses as guesses in the table itself.
4. Figure captions state the finding, not the axes.
5. Depth is tiered. Rochester puts long derivations in a linked PDF. Heidelberg
   collapses detail. The main page stays readable end to end.

**Two choices to copy deliberately.**

- **TU-Eindhoven walked one patient through the whole pipeline.** Our
  equivalent is one litre of leach liquor walked through all nine steps, with
  the number at each step. This is the single best device for our chain.
- **IISER-Berhampur gave one equation its own page.** Our capture isotherm and
  the Ho-McKay elution law each earn that treatment.

**Two to avoid.**

- Rochester and SCUT render equations as images. Images do not scale, do not
  copy and do not read aloud. Render LaTeX.
- IISc-Software carried two figures for a whole model page. Too few.

The weak page failed on one axis only: it described modelling instead of
showing a model. Avoid abstract framing anywhere.

---

# 1a. What the judges actually score

Source: the 2025 iGEM Judge Handbook, Chapter 4, the Model and Wiki prizes.
This is the primary document. Everything in §1 is a team's interpretation of
it; this section is the rule itself.

**A judge must be able to understand four things.** The handbook lists them as
what excellent, well-documented model development shows:

1. What kind of modelling is being done, and what information it will provide.
2. What assumptions were made, and why.
3. What kind of data was used to build or assess the model.
4. How the model results affected project design and development.

**The rubric then asks four questions.**

1. How impressive is the modelling?
2. Did the model help the team understand a part, device, or system?
3. Did the team use measurements of a part, device or system to develop it?
4. Does the approach provide a good example for others?

**Read those against our project.** Questions 1 and 4 we win on: nine coupled
stages, PRCC in three regimes, and a repository where every number carries a
source. Question 3 is our exposure, because our parameters come from
literature, not from our own bench. Question 2 is answered by the oxygen
result and by the capacity mismatch, and both must be visible on the Overview.

**The handbook names the failure mode twice.** Sample judge comments include
that a kinetics model's link to the design was not clear, and that good
modelling work had documentation that was hard to follow. Both are
presentation failures, not modelling failures.

**On assumptions, the handbook is explicit and forgiving.** The GEMS_Taiwan
2022 write-up is praised partly because the team could not measure its
parameters in the season, said so, and described what it would do with more
time. Stating a gap is scored, not punished. `ISSUES.md` is therefore an asset
to publish, not a liability to hide.

**The Wiki prize adds five more questions**, of which two bind on us: whether
the design helps a visitor find and understand the content, and whether every
figure and prior result is properly cited.

---

# 2. The proposed structure

```
Model/
  Overview          the process, three questions, four findings, judgment
  Leachant          TetH supply and tetrathionate conversion
  Leaching          coupled gold, copper, oxygen and ligand chemistry
  Leach-to-capture  the real-liquor compatibility gate
  Capture           GolB display, the isotherm and whole-cell capacity
  Recovery          elution, reductase supply and metal formation
  Recovery 2.0      the model-informed process design
  Evidence          validation, limits, equations, parameters and code
```

Eight pages. The Overview is a short hub, Pages 2–6 are focused scientific
chapters, Page 7 reunites their findings as a changed design, and Page 8 makes
the work auditable. [WIKI_PLAN.md](WIKI_PLAN.md) section 3 is authoritative for
the full outline.

---

# 3. The Overview page

The Overview carries the whole argument. Everything else is evidence.

1. **The question.** Can biology recover gold from electronic waste?
2. **The material-flow diagram.** Gold moves through the centre; TetH, GolB and
   reductase production enter as three supply arms.
3. **Three project questions.** Leachant feasibility, real-liquor capture and
   return to metal.
4. **Four finding cards.** Oxygen, TetH, whole-cell capacity and conditional
   reduction.
5. **One paragraph of scope.** Metal formation is the boundary; physical
   collection and product purity are outside it.
6. **The current judgment.** The model has not proved a yield; it has stopped
   the team optimising the wrong things.
7. **A link row** to Pages 2–8.

---

# 4. The section template

Use one template on every evidence page. Repetition is the teaching device: a
reader who learns the pattern once reads the other pages fast.

**Adopt the GEMS_Taiwan 2022 headings**, because the Judge Handbook praises
that page by name for describing each model as an academic paper. Their
economic model page runs: Overview, Methods, Obtaining Parameters, Results,
Discussion, Conclusion, Limitations, References. Their toxin-antitoxin page
runs the same shape with Assumptions as its own numbered list.

Our version, repeated on Pages 2–6:

1. **Question** — the project decision the model must support.
2. **In plain language** — what happens, without symbols.
3. **Model and assumptions** — equations, parameter provenance and limits.
4. **Finding** — a sentence that states the result.
5. **Project impact** — what changes for hardware, wet lab or process design.
6. **Next experiment** — the evidence that could confirm or reverse the
   decision.

The technical material formerly separated into Obtaining Parameters,
Limitations and References remains available inside Model and Assumptions and
in the evidence appendix. Project Impact answers the rubric criterion that
teams most often omit.

---

# 5. Making the complexity readable

Five devices, ranked by return on effort.

1. **Progressive disclosure.** Plain sentence first, then the equation in a
   collapsed block. The judge reads the sentence; the modeller opens the block.
2. **One colour per stage**, held across every figure, the chain strip and the
   page headers. Colour becomes the index.
3. **The gate metaphor for the leach-to-capture interface.** A handover carries
   composition, amount, volume and units, and can fail even when both adjacent
   models work. Show the gate on the material path.
4. **A parameter card** on hover or click: symbol, value, unit, status, source.
   One component, fed by the YAML, used everywhere.
5. **A one-slider figure** for oxygen. Move `[O2]`, watch recovery move. One
   interactive element only. More than one costs build time and teaches less.

---

# 6. Build path

Generate, do not hand-copy. The rules in `STRUCTURE.md` already forbid loose
numbers, so the wiki should read the same files the tests read.

1. Export the parameter tables from `params/*.yaml` to HTML with a script that
   sits beside `docs/make_review_tables.py`.
2. Export figures from the notebook to `docs/media/review/` as today.
3. Render the equation blocks from `EQUATIONS.md`.
4. Render the open-issue lists from `ISSUES.md` by stage tag.
5. Fail the wiki build if any parameter reaches a page with `status: null`.

Step 5 makes the wiki a fifth check alongside the four in `AGENTS.md` §7.

---

# 7. Changes the survey forces

The 2026-08-18 survey and the larger 2026-09-06 survey now resolve into eight
decisions in [WIKI_PLAN.md](WIKI_PLAN.md):

1. **Use a short hub plus focused chapters.** Toulouse shows how a complex
   cascade can be introduced once and then split without losing its unity.
2. **Follow the physical process.** Peking orders different model types by the
   journey of the product rather than by mathematical technique.
3. **Repeat one chapter template.** Rochester makes multiple models auditable
   through predictable headings.
4. **State findings in headings.** Heidelberg lets a scanning reader leave with
   the results.
5. **Give integration its own page.** Gold Recovery 2.0 shows the original
   concept beside the process the combined model now supports.
6. **Make assumptions and evidence visible.** Unknown quantities are labelled
   and become future experiments rather than hidden precision.
7. **Generate parameter tables and render equations as LaTeX.** Every value
   retains unit, status and source; equations remain accessible.
8. **Cite every figure and borrowed result where it appears.** The Wiki prize
   scores citation directly.

---

# 8. The gap we cannot close by design

The rubric asks whether the team used **its own measurements** of a part or
device to develop the model. Our parameters are literature-sourced, and
ISSUES 32 records that the enzyme stage is unvalidated.

Do not hide this and do not over-claim. Two honest moves:

1. State on the Overview which parameters would be measured first, and what
   each measurement would settle. `t_film` and the TetH pH window rank first.
2. Show the model earning its keep without new data: the oxygen optimum came
   out of the model alone, costs nothing, and moves recovery 38% to 61%.

That is a model informing design, which is what the prize is named for.
