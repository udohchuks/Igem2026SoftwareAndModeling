# Dashboard design prompt

**Tier 3, synthesis. A brief, not a specification.**

**What this is:** a copy-and-paste prompt for a design tool or a designer, to
produce a simple, modern look for the bioreactor console.
**What this is not:** the product specification. That is
[`DASHBOARD_SPEC.md`](DASHBOARD_SPEC.md), and it governs behaviour. This file
governs appearance only. Where the two disagree, the specification wins.

Every figure quoted in the prompt is real output from this repository, so the
designer works against the shape of the actual data. Regenerate them with
`python dashboard-prototype/export_runs.py`.

Date: 2026-09-18.

---

## How to use it

Paste the block below into a code-generating tool, an image tool or a brief for
a person. Change one line only:

| Target | Change the first line to |
|---|---|
| A code tool | `Deliver one self-contained HTML file with inline CSS.` |
| Figma or an image tool | `Deliver three frames at 1440 wide and three at 390 wide.` |
| A person | `Deliver whatever you normally hand to a front-end developer.` |

---

## The prompt

```text
Design the interface for a laboratory bioreactor control console.
Deliver one self-contained HTML file with inline CSS.

WHAT IT IS
A console for a single bench bioreactor that recovers gold from electronic
waste. It does one thing no commercial bioprocess software does: it predicts
how much acid or base a batch will need BEFORE the run starts, then holds each
process stage's own pH set point during the run and reports the deviation.

WHO USES IT
A student standing at a bench, glancing at the screen while both hands are
busy. Secondarily, someone reading the traces afterwards to check the model.

THE ONE THING
The predicted reagent volume on the first screen is the product. It should be
the largest element on the page. Everything else defers to it.

THREE SCREENS
1  Setup   Pick the leach scenario, enter vessel volume and titrant stock,
           read one number: total titrant in millilitres.
2  Run     Live pH against the active stage's set point band, pump state,
           cumulative titrant delivered against predicted, an event log.
3  Report  Measured against predicted in a table, then a CSV block to copy.

REAL CONTENT. Use these exact values. Invent nothing else.
  Six stages, each with its own pH set point:
    01  Culture and expression      pH 7.0    no window recorded
    02  Tetrathionate hydrolysis    pH 3.0    no window recorded
    03  Bioleaching                 pH 10.0   window 9.3 to 10.5
    04  Capture on displayed GolB   no set point   window 9.0 to 10.5
    05  Elution                     no set point   no window recorded
    06  Reduction to metal          pH 7.0    no window recorded
  Headline on Setup:   37.4 mL total
  Live readouts:       pH 10.04   deviation +0.04 pH   gold 83.8 %   48.63 mL
  Report row:          predicted 48.54 mL, measured 48.63 mL, +0.2 %, pass
  Time axis:           0 h to 145 h, stage change marked at 72 h
  Event log lines:     "Stage change to Bioleaching. Set point now pH 10.0."
                       "No pH reading for 120 s. Pumps stopped."
  Three interlocks:    stale reading, dose ceiling, pH outside the window

SIMPLE AND MODERN MEANS
  Restraint, not emptiness. The page is dense with real numbers and quiet
  everywhere else.
  One neutral ramp and exactly one accent colour. Semantic green, amber and
  red exist for state only and are never used as decoration.
  One sans-serif for every word. One monospace for every number, always with
  tabular figures, so digits do not shift as values update.
  Two weights maximum in the sans. Large numerals set light, not bold.
  Hairline rules and whitespace carry the structure. Reach for a border, a
  fill, a radius or a shadow only where something genuinely separates.
  Charts with no frame and no background fill: three gridlines, muted labels,
  one emphasised endpoint per series.
  Nothing moves unless the data moved.

STATES TO DESIGN, NOT JUST THE HAPPY ONE
  Idle before a run, running, held, and an interlock tripped.
  A stage that cannot be run, because no set point is sourced for it. It must
  read as deliberately blocked, not as broken or unfinished.
  A report with no run yet.

CONSTRAINTS
  Light and dark, both designed, neither an inversion of the other.
  Works at 400 px wide with no horizontal scroll.
  Every number monospaced and tabular.
  Keyboard focus is visible everywhere.

DO NOT
  Warm cream grounds with a serif display face and a terracotta accent.
  A purple or blue gradient hero.
  Inter or Space Grotesk.
  Emoji as section markers.
  Rounded cards with a coloured bar down one edge.
  A hero that fills the viewport before any data appears.
  Any number not listed above.
```

---

## Applied, 2026-09-18

The prompt was run against
[`../dashboard-prototype/index.html`](../dashboard-prototype/index.html). The
choices it produced, recorded so the next pass does not relitigate them:

| Decision | Choice | Why |
|---|---|---|
| Family | **Poppins**, 300 / 400 / 500 / 600, for text and numbers alike | Chosen by the team on 2026-09-18, superseding Instrument Sans plus DM Mono |
| Figures | Proportional, not tabular | Poppins ships no tabular-figure feature. `1` is about half the width of `0`. Changing values sit in fixed slots so the layout holds still, but digit widths differ |
| Prose | Removed from every screen | Explanations became tags: `modelled`, `estimate`, `assumed`, `not modelled`. Provenance moved into one collapsed `Sources` block |
| Scale | 7 steps, declared as `--t-*` tokens | 10, 11, 12, 13, 20, 30, and a hero stepped 48 / 64 / 78 at breakpoints. Every size on the page is one of these |
| Borders | Only on things you operate | Inputs, buttons, the control bar. Charts and panels lost their boxes |
| Gridlines | Three | Down from five |
| Blocked stage | Muted name on a grey rule | Reads as context rather than as a control |
| Muted grey | `#6E6E76` light, `#909099` dark | The first pass sat near 3.6:1 at 10 px, below AA |
| Stage set points | **Off every screen.** Data only | First the six cards went to a 71 px strip, because cards implied a control that did nothing. Then the strip went too: only stages 2 and 3 are runnable, so showing six claimed a scope the console lacks. The set points stay in `stage_ph.yaml`, drive the control loop, and appear under `Sources` |
| Run wayfinding | Progress strip built from the active plan | The only strip that survived. It shows the 1 to 3 segments actually running, sized by real duration, filling as the batch advances. It changes during a batch, which is what earned it the space |

---

## See also

- [`DASHBOARD_SPEC.md`](DASHBOARD_SPEC.md) — behaviour, data contract, milestones
- [`../dashboard-prototype/index.html`](../dashboard-prototype/index.html) — the current build
- [`../dashboard-prototype/stage_ph.yaml`](../dashboard-prototype/stage_ph.yaml) — where the six set points come from
