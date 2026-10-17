---
title: "Wiki plan — Model section, v3"
date: "2026-09-07"
---

# What this file is

**Tier 3, synthesis.** The current information architecture for the Model
section of the team wiki. [WIKI_DESIGN.md](WIKI_DESIGN.md) sets the rubric and
[WIKI_SURVEY.md](WIKI_SURVEY.md) records the precedent; this file commits the
page order and reading flow; [WIKI_CONTENT.md](WIKI_CONTENT.md) writes the
copy. `AGENTS.md` section 11.

This is an outline, not the scientific source of record. Current results live
in [REVIEW.md](REVIEW.md), [RECOVERY_MODEL.md](RECOVERY_MODEL.md) and
`params/*.yaml`.

**v3 change, 2026-09-07.** The nine equal cells in v2 are replaced by a short
hub, five focused chapters, one integration page and one technical appendix.
The material journey stays central, while TetH, GolB and reductase production
are shown as supply arms rather than false sequential process stages.

---

# 1. The story in one sentence

We followed gold from crushed circuit boards to newly formed metal, asked
whether every stage could successfully hand it to the next, and used the
failures and opportunities we found to change what the team should build and
measure.

That sentence governs the page order and the presentation. The wiki is not
organised by mathematical technique. It follows the material, then reunites
the models as a design decision.

---

# 2. Three reading depths

The same content must work for three readers without forcing any of them into
the wrong level of detail.

| Reader | Time | What they should read | What they should leave knowing |
|---|---:|---|---|
| Judge scanning the contribution | 1 minute | Page 1 | the process, four findings and current judgment |
| Judge reviewing the model | 10 minutes | Pages 1–7 | how each model changed the project |
| Modeller auditing the work | 1 hour | Pages 2–8 and repository | assumptions, equations, parameters, limitations and code |

The answer is always visible. Equations, parameter tables and issue histories
use progressive disclosure or the appendix.

---

# 3. The eight-page outline

## Page 1 — Model overview: Can biology recover gold from e-waste?

**Purpose:** give the complete modelling contribution in one screen-length
argument.

**Order:**

1. The question in one sentence.
2. The complete process diagram.
3. The three questions that organise the work.
4. Four finding cards.
5. The current judgment.
6. Links to Pages 2–8.

**The three questions:**

1. Can we biologically produce and protect the leachant?
2. Can GolB capture gold from the actual leach liquor?
3. Can the recovered gold be converted back into metal?

**The four finding lines:**

1. Less oxygen may recover more gold.
2. TetH activity is the first feasibility gate.
3. Displayed-site counts are not measured whole-cell capacity.
4. Reduction could be fast or nearly stall across the declared kinetic range.

**Closing judgment:** the model has not yet proved a process yield. It has
prevented the team from optimising the wrong things.

## Page 2 — Making the leachant

**Question:** can engineered *E. coli* produce active TetH under workable
process conditions?

**Finding heading:** **TetH production, not reaction speed, is the first
feasibility gate.**

**Contents:**

1. Why thiosulfate is needed.
2. Why the team proposes making it biologically.
3. TetH expression and enzyme supply.
4. Tetrathionate-to-thiosulfate conversion.
5. Folding, recovery and pH compatibility.
6. Consequence: validate activity before sizing the vessel.
7. Next experiment: activity assay after the intended recovery procedure.

## Page 3 — Dissolving the gold

**Question:** how do we dissolve gold without copper destroying the
leachant?

**Finding heading:** **Copper chemistry controls the leach, and oxygen is the
cheapest available handle.**

**Contents:**

1. Gold and copper in the printed-circuit-board feed.
2. Coupled gold dissolution and copper redox chemistry.
3. The oxygen optimum.
4. Glycine as the selected copper ligand.
5. pH control and the dosing hardware.
6. Limits: plating thickness, liberation and passivation.
7. Next experiment: otherwise identical leaches at two oxygen levels.

## Page 4 — Leach to capture

**Question:** is the liquid leaving the leach compatible with the cells that
must capture its gold?

**Finding heading:** **Successful leaching does not guarantee compatible
capture.**

**Contents:**

1. Dissolved gold crossing the interface.
2. Copper crossing with it.
3. Tetrathionate and trithionate crossing with it.
4. Possible reaction with the cysteines GolB uses for binding.
5. Why concentration alone cannot describe this handover.
6. Possible conditioning strategies, presented as options rather than adopted
   design.
7. Next experiment: binding in clean solution, representative leachate and
   treated leachate.

## Page 5 — Capturing the gold

**Question:** how much gold can the whole engineered cell actually hold?

**Finding heading:** **Site counting gives a conditional capacity, not a
measured whole-cell ceiling.**

**Contents:**

1. GolB surface display.
2. The conditional single-occupancy site inventory.
3. The mass-conserving Langmuir calculation.
4. Bound amount versus captured fraction.
5. Literature whole-cell capacity scenarios.
6. Consequence: do not optimise display rate before measuring effective
   capacity in the process matrix.
7. Next experiment: engineered cells, unmodified cells and a cell-free blank
   across a gold concentration series in representative leachate.

The older 63-fold mismatch may appear only as the result of the conditional
single-occupancy model. It must not be presented as a proven physical ceiling
after [ISSUES.md](ISSUES.md) item 92.

## Page 6 — Returning gold to metal

**Question:** can captured gold be released and reduced under the intended
eluate conditions?

**Finding heading:** **Recovery is a sequence: release the gold, then prove it
forms metal.**

**Contents:**

1. Gold amount entering elution.
2. Elution endpoint versus elution speed.
3. The separate reductase culture and lysate supply arm.
4. Reduction kinetics and the electron ceiling.
5. The full kinetic scenario map.
6. Consequence: report conditional scenarios rather than one expected yield.
7. Next experiments: elution and reduction time courses in the intended
   matrices with quantitative gold balances and controls.

## Page 7 — Gold Recovery 2.0

**Purpose:** reunite the five focused chapters as one model-informed process
design. This is the primary integration and prize-facing page.

**Opening:** the model did not merely describe the process. It changed the
process we would build.

| Original concept | Model-informed design | Evidence required |
|---|---|---|
| Aerate strongly | Meter oxygen deliberately | two-level oxygen leach |
| Size the TetH vessels | Validate active TetH first | active-enzyme assay |
| Send leachate directly to GolB | Add a compatibility gate | matrix binding comparison |
| Infer capacity from displayed sites | Measure whole-cell capacity | isotherm in representative leachate |
| Quote one recovery efficiency | Report conditional scenarios | actual-matrix elution and reduction time courses |

Close with three named subsections:

1. **Impact on hardware** — aeration and pH-control decisions.
2. **Impact on wet lab** — the ranked measurement programme.
3. **Impact on modelling** — parameters or model branches that remain null
   until those measurements exist.

## Page 8 — Evidence and technical resources

**Purpose:** make the work auditable without interrupting the main story.

**Order:**

1. Internal verification.
2. Literature support and proxy transfer.
3. Unvalidated assumptions and limitations.
4. Ranked experiments.
5. Equations.
6. Parameter tables with value, unit, status and source.
7. Code and reproduction instructions.
8. References and open issues.

---

# 4. The repeated template for Pages 2–6

Every scientific chapter uses the same six-part rhythm.

| Order | Section | Question it answers |
|---:|---|---|
| 1 | **Question** | What project decision must this model support? |
| 2 | **In plain language** | What happens physically or biologically? |
| 3 | **Model and assumptions** | How was it represented, and what was assumed? |
| 4 | **Finding** | What did the model actually show? |
| 5 | **Project impact** | What changes for hardware, wet lab or process design? |
| 6 | **Next experiment** | What evidence could confirm or reverse the decision? |

The finding is a sentence and is always visible. Model detail and assumptions
may collapse, but print and no-JavaScript views expand them.

---

# 5. The process diagram

The diagram must distinguish material flow from biological supply.

```text
MAIN MATERIAL FLOW
PCB -> leachant -> leach -> conditioning -> capture -> elution -> reduction -> metal
          ^                       ^                         ^
SUPPLY    |                       |                         |
ARMS      TetH expression         GolB expression           reductase culture
          supplies activity       supplies capacity         supplies lysate
```

Do not place “sites become capacity” after capture as though it were a vessel.
It is a model interface feeding capture. The same distinction applies to the
reductase culture, which runs in parallel and supplies the reduction vessel.

Each process step links to its page and exposes a plain text equivalent for
screen readers. Colour indicates process family; evidence state uses text and
an independent visual marker.

---

# 6. Evidence labels

Do not force scientific provenance and project readiness into one pill. They
answer different questions.

**Evidence source:** measured by team, measured in literature, derived,
modelled, proxy or unmeasured.

**Decision state:** adopted, proposed for testing or blocked.

A stage may therefore be “literature proxy” and “blocked” at the same time.
The page header displays decision state; the parameter table displays evidence
source.

---

# 7. Navigation and behaviour

1. Page 1 is a short hub, not the entire report.
2. Pages 2–6 are individually addressable and use identical local navigation.
3. Page 7 is reachable from every scientific chapter through its project
   impact section.
4. Page 8 is reachable from every Model or Assumptions disclosure.
5. A visible contents list marks the current section.
6. Equations are rendered as LaTeX, never images.
7. Figures and finding lines remain visible without a click.
8. Parameter tables are generated from YAML; no scientific value is typed into
   the wiki by hand.
9. Print and no-JavaScript views expose all content.
10. Motion honours `prefers-reduced-motion`.

---

# 8. The matching presentation

The presentation uses the same names and the same order so a judge recognises
the wiki after hearing the talk.

| Beat | Spoken purpose | Wiki destination |
|---:|---|---|
| 1 | Gold is trapped in copper-rich electronic waste | Page 1 |
| 2 | Show the complete material journey and three supply arms | Page 1 diagram |
| 3 | Ask whether every stage can hand gold to the next | Page 1 questions |
| 4 | TetH is the first feasibility gate | Page 2 |
| 5 | Oxygen is a controllable opportunity | Page 3 |
| 6 | The leach-to-capture interface may fail | Page 4 |
| 7 | Site count is not measured capacity | Page 5 |
| 8 | Metal formation remains conditional | Page 6 |
| 9 | The model changed what the team builds and tests | Page 7 |
| 10 | State the current judgment and next evidence | Pages 7–8 |

One figure should own each major spoken finding. Do not introduce a figure in
the presentation under a different name or interpretation from the wiki.

---

# 9. Build order

1. Page 1 with the material-flow diagram and four finding cards.
2. Page 7 with the before-and-after design table.
3. Pages 2–6 using the repeated template and existing reviewed figures.
4. Page 8 generated from the repository records.
5. Deep links, parameter cards and print behaviour.
6. One optional live control: the oxygen scenario. Nothing else needs to be
   interactive to communicate the contribution.

Pages 1 and 7 establish the story. Pages 2–6 prove it. Page 8 makes it
auditable.

---

# 10. Open editorial decisions

1. Confirm the public project name used instead of “Gold Recovery 2.0”.
2. Confirm whether liquor conditioning is a proposed design option or an
   adopted process step.
3. Name the exact hardware response to the oxygen and pH findings.
4. Decide which team members own the material-flow diagram and each page.
5. Replace internal repository links with final wiki routes before publication.
