---
name: igem-wiki-writing
description: How award-winning iGEM teams write model and wiki pages, turned into rules for this project. Covers the overview, the section template, parameter tables, assumptions, limitations, figure captions and the judging rubric. Use when drafting, reviewing or restructuring any wiki page, especially the Model section.
---

# Writing the iGEM wiki

Write pages the way the teams that win Best Model and Best Wiki write them.
This skill is the distilled evidence, not opinion. Its sources are the 2025
iGEM Judge Handbook and ten team pages read in full, listed in §9.

Layout and behaviour live in `docs/WIKI_PLAN.md`. The rubric and the survey
live in `docs/WIKI_DESIGN.md`. Confirmed page copy lives in
`docs/WIKI_CONTENT.md`. **Read `AGENTS.md` first**; its five rules bind here
too, and rule 5 in particular: source documents are never edited.

---

## 1. What a judge must be able to understand

The Judge Handbook, Chapter 4, says excellent model documentation lets a judge
understand four things. Every model page must answer all four, in this order.

1. What kind of modelling is being done, and what information it will provide.
2. What assumptions were made, and why.
3. What data was used to build or assess the model.
4. How the model results affected project design and development.

The rubric then scores four questions: how impressive the modelling is, whether
it helped the team understand the system, whether the team used its own
measurements, and whether the approach is a good example for others.

**The handbook names the failure mode twice, and both times it is
presentation.** Sample judge comments cite a kinetics model whose link to the
design was unclear, and good modelling whose documentation was hard to follow.
A page that hides a good model scores as a bad model.

---

## 2. The overview

Six award-winning overviews were measured, then the rules below were tested
against eleven rounds of live feedback on this project's own introduction.
What survived both is below. Where the two disagreed, the live feedback wins;
it is evidence about this team's ear, and the ten team pages are evidence
about the genre.

**Structure**

1. **Keep it short.** 130-280 words for the whole opening. If the page then
   breaks into named sub-problems, each gets one short paragraph, not a
   section.
2. **Open on the work, not on the reader's prior knowledge of the field.**
   State what the model covers and why it was built, in that order. Do not
   open by explaining the real-world problem if the home or description page
   already does — a reader on the Model page has been told what the project
   is. Do not open by explaining what modelling is in general, or by
   contrasting a model with a bench experiment. The reader already accepts
   that models are useful; asserting it wastes the first sentence.
3. **State the purpose as a plain infinitive clause once**, and do not restate
   it. "The purpose was to model the end-to-end process" is one clause,
   asserted once. Do not follow it with a second sentence that explains the
   same purpose in different words — that is where drafts go generic.
4. **Keep numbers out entirely**, including percentages, counts and named
   thresholds. If a number must appear, it is unavoidable context, not a
   result.
5. **Name what changed, and tie each change to the team that acted on it in
   the same sentence.** "On the hardware side, this led to X" is correct
   because the attribution and the change are in one clause. Do not separate
   attribution from outcome into two sentences, and do not list outcomes
   without saying who used them.
6. **If the model splits into named sub-problems, state the split as a fact,
   not as a device.** "The chain breaks into four problems" is enough. Do not
   add a sentence explaining why breaking it down was necessary — the reader
   sees why once the four are named.

**Sentence-level, from the parts of the drafting process that needed the most
correction**

7. **Do not open consecutive sentences, or consecutive paragraphs, with the
   same construction.** "It informed X, and it informed Y" and "That surfacing
   shaped both. On the hardware side..." were both rejected for this reason.
   Vary the subject of each sentence.
8. **Avoid abstract connective phrases that restate the previous sentence
   instead of adding to it** — "those findings shaped both", "that surfacing",
   "this makes the process predictable" said as its own sentence rather than
   folded into a concrete clause. If a sentence's only job is to summarise the
   sentence before it, cut it.
9. **Do not open with "We" if it can be avoided**, and do not default to
   first-person plural as a reflex. Passive-voice science writing
   ("Culture and conversion are modelled as separate vessels") is acceptable
   and was preferred here once identified.
10. **Use an em dash only when nothing else will do**, and check for it
    specifically before presenting a draft — it recurs by default and has to
    be actively removed.
11. **Match the process's own vocabulary exactly.** "PCB grinding" was wrong
    where "shredded PCB" was right, because the model's own inputs use the
    second. Check `docs/MASTER.md` for the term actually used before writing
    the opening line, rather than paraphrasing.

**Before presenting any draft to the team**, run it against items 7-11 as a
checklist. These are the corrections that took multiple rounds to reach in
practice, so they are the ones most likely to recur.

---

## 3. The section template

Use one template for every model, every time. Repetition teaches; a reader who
learns the pattern once reads the rest fast. These headings are taken from the
page the Judge Handbook praises by name for reading like an academic paper.

1. **Overview** — what this stage does, two sentences, no symbols.
2. **Methods** — the equations, each with one line of plain English.
3. **Assumptions** — a numbered list. Give a reason for each entry.
4. **Obtaining parameters** — the table. See §4.
5. **Results** — the figure, and what it shows.
6. **Discussion** — what the result changed about the design.
7. **Limitations** — what is still open, in one sentence each.
8. **References**.

Headings 3, 4 and 8 answer handbook criteria 2 and 3. Heading 6 answers
criterion 4, and it is the one most teams omit.

---

## 4. Parameter tables

**Never type a number into a page by hand.** Generate every table from
`params/*.yaml`. A number that exists in two places will disagree in two
months.

Columns, in this order: **symbol, value, unit, status, source**.

- Every row carries a source, or carries the word that says it has none.
- Mark an assumed value as assumed **in the table**, not in a footnote.
- Name the literature reference or the prior iGEM team the value came from.
- Any symbol used in prose is clickable and shows those five fields.

---

## 5. Assumptions and limitations

The handbook is explicit and forgiving here, and teams routinely leave points
on the table by hiding what they do not know.

1. **Assumptions get their own numbered heading.** Never bury them in prose.
2. **State the cost of each assumption**, not just its existence. An assumption
   with an unknown multiplier attached is a finding; an unqualified one is an
   excuse.
3. **Say plainly what you could not measure this season, and what you would do
   with more time.** A team was praised for exactly that. The season is short
   and judges know it.
4. **Where sources disagree, publish the disagreement** and name the issue.
   Do not silently pick a side.
5. **Never over-claim.** If a stage is unvalidated, the page says so on the
   stage, not in an appendix.

---

## 6. Figures, equations and captions

1. **The caption states the finding, not the axes.** "Recovery peaks at
   80 µmol/L, not 500" beats "Recovery against dissolved oxygen".
2. **Render equations as LaTeX, never as images.** Surveyed teams shipped
   `.webp` equations, which cannot be copied, scaled or read aloud.
3. **Every equation gets one line of English beside it.**
4. **One figure per result.** A page with two figures and 3,000 words reads as
   an essay, not a model.
5. **Colour carries meaning or it is not used.** If colour marks a vessel, it
   marks a vessel everywhere, on every figure and every header.

---

## 7. Navigation, because it is scored

The Best Wiki criteria ask whether the design helps a visitor find and
understand the content. Three rules follow from the winning pages and from
documentation UX practice.

1. **A static table of contents in a sticky column, with the current section
   highlighted as the reader scrolls.** The highlight is the half that matters;
   without it a reader is lost after two screens. No search box.
2. **Scrolling is the primary path.** Collapsed content cannot be scanned, so
   nothing that carries the story is ever behind a click. Close the working,
   never the finding.
3. **Every claim has an address.** Deep-link each section so an issue, a
   supervisor note or a presentation slide can point at one exact claim.

---

## 8. Anti-patterns

Five failures, each observed on a real page.

1. **Describing modelling instead of showing a model.** A page that explains
   what modelling is, and links to other teams, scores nothing.
2. **Opening the overview with a result or a raw number.** A reader who has not
   met the symbol cannot place the number.
3. **Equations as images.**
4. **Two figures for an entire model page.**
5. **Assumptions written as prose inside the methods.** They stop being
   findable, and findability is what the criterion measures.

---

## 9. Sources

The Judge Handbook, Chapter 4, prizes Model and Wiki:
`https://static.igem.org/websites/competition/2025/judging/2025-judge-handbook.pdf`

Pages read in full, with what each supplies:

| Team | Supplies |
|---|---|
| GEMS_Taiwan 2022 | the eight-heading template; parameter tables that cite their origin; the hub-plus-sub-page shape |
| Heidelberg 2024 | every model claim named the wet-lab test that checked it |
| Rochester 2025 | a fixed six-heading template; a sticky sidebar; guesses marked as guesses |
| Cornell 2024 | assumptions as numbered lists; an overview closing on a design change |
| UZurich 2024 | an Assumptions and Limitations section; the argument for why a model was the only route |
| SCUT-China-L 2025 | parameter tables with symbol, value, unit and citation |
| IISER-Berhampur 2025 | one hard equation given a page of its own |
| TU-Eindhoven 2024 | one worked example walked end to end through the pipeline |
| KULeuven 2025 | a two-sentence overview; an embedded simulation |
| UNT 2024 | the counter-example, §8 item 1 |
