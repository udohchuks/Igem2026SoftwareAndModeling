# Improvements

Tier 3. Internal only. Nothing here goes on the public wiki.

Defects found while building `docs/WIKI_MODEL_UPDATE.md` from
`Bioleaching Modelling - Summary.docx` on 2026-09-19. The current wiki build
ships past all of them. Each one needs a redone figure, a corrected number or
a decision.

## Open

### 1. Figure stage numbering drove the wiki numbering

The five figures are titled STAGE 2 and STAGE 3. The document's prose calls the
same work Stage 1 and Stage 2. We made the wiki match the figures, so the wiki
now runs Stage 1 enzymes, Stage 2 thiosulphate, Stage 3 leaching. The document
was not changed. Decide which numbering is canonical, then make all three
agree.

### 2. The parameter tables still carry the document's numbering

The tables inside the dropdowns read Stage 1A, Stage 1B and Stage 2. Under the
new headings those read as Stage 1, Stage 2 and Stage 3. Retitle them when
item 1 is settled.

### 3. A MATLAB data cursor is published in a figure

`stage2-no-ammonia.png` panel (c) carries a data tip reading X 26.0685,
Y 28.8318. Remove the cursor and replot.

### 4. The 28.93 % figure does not match its own plot

The document quotes 28.93 % at 72 hours. Panel (d) of the same figure shows
gold recovery flat at about 28.5 % from hour 26 onward. Read the number off
the plateau.

### 5. The pH panel is uninformative and contradicts the pH decision

Panel (h) is a flat line at pH 7 in all three leaching figures. The repository
sets the operating window at 9.3 to 10.5. Either the run really is at pH 7,
which the document never states, or the panel is a placeholder. Drop it or
explain it.

### 6. The rate-limited oxygen result is stated as a delta, not a level

The document says a 7 % increase over 40.97 %. The figure shows about 48 %
recovery. Publish the level.

### 7. Eight-panel montages will not read at wiki width

Each leaching figure carries panels (a) to (h). The finding rests on (c), (d)
and (f). Crop for the visible page and keep the montage in the dropdown.

### 8. The two Stage 2 figures are not comparable as drawn

`stage1-sequential.png` is two panels to 10e4. `stage1-simultaneous.png` is one
cropped panel to 8e4. The text asks the reader to compare them. Replot at
matched axes.

### 9. The sequential figure shows only one arm of an open trade

The figure is titled purified TetH 0.043 µmol L-1, which is the 3 day, 9.1 L
case. The text presents the 1 day, 27 L case as equally available. Plot both
or say which is the design case.

### 10. TetH steady state disagrees with itself

The Stage 1A analysis says 7.791e-3 µmol L-1. The Stage 1A table says
4.75e-3 µmol L-1. The wiki carries the analysis value.

### 11. Two drafting artifacts in the source document

"Thus, the sequential model was chosen?" still ends in a question mark. One
assumption reads "All other sulphur species are relevant or present", which
appears to mean the opposite. Both are reproduced verbatim on the wiki.

### 12. Stage 3 and Stage 2 have no question line

The document gives a question only for Stage 1A. Stage 2 and Stage 3 open with
design decisions instead. Write one question each.

### 13. Next experiment is TBD in all three stages

The document proposes no experiment. Ballot question 3 asks what data would
develop or validate the model. Name one measurement per stage.

### 14. Ammonia volatility is still unanswered

`AGENTS.md` retired ammonia on 2026-08-19 because the air pump would strip it.
The bioleaching summary models 260 mM ammonia and does not address volatility.
The standing decision is marked superseded, the objection is not withdrawn.

### 15. The simultaneous-model PNG is upscaled 3.5x on the page

`stage1-simultaneous.png` is 264 x 292 px and renders at 911 px wide. It was
cropped out of the document at screen resolution. Re-export it at the same size
as the other four, which are 1280 x 680.

### 16. Wiki stage numbering now differs from the source document

The page runs Stage 1 enzymes, Stage 2 thiosulphate, Stage 3 leaching, taken
from the figure titles. The document runs Stage 1 with sub-stages 1A and 1B,
then Stage 2. Settle item 1 and make both agree.

### 17. The interpolated cell mass differs between the record and the parameter file

`SOURCES.md` S30 says the dry mass interpolated at `μ = 1.2 h⁻¹` is about
**415 fg**, which is `2.41 × 10¹² cells/g`. `params/conversions.yaml` uses
**423 fg**, which is the `2.36 × 10¹² cells/g` the model runs on. A 2 % gap
between the record and the number in use. Nothing downstream turns on it, but
the two should state the same figure.

Found 2026-09-19 while adding `n_cells/g` to the `R_lysate` equation in
`docs/WIKI_BIORECOVERY_DRAFT.md`, which had multiplied molecules per cell by
grams per litre with no bridge between them. That equation is now corrected;
this item is the leftover.
