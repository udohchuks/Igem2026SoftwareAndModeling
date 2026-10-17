# Bioreactor dashboard — product specification

**Tier 3, synthesis. Specification only.**

> ⚠ **Most of the software in this file does not exist yet.** §12 lists the
> only parts that do: a browser prototype with no probe and no pump attached.
> Everything else is future tense. `AGENTS.md` §11 rule 5 forbids a file that
> claims infrastructure that was never written, so this warning stays until
> §12 covers the whole document. When a section ships, move it into §12.

**Who reads this:** whoever writes the dashboard, and the wet lab team who
will operate it.
**What this is not:** a model document. Every equation and every number stays
in `src/` and `params/`. This file specifies only the software around them.

Date: 2026-09-18.

---

## 1. The one job

Tell the operator how much reagent this batch needs **before** the run starts,
then hold the set point during the run and report the deviation.

Commercial bioprocess software is reactive; it holds a set point measured now.
This project already computes demand ahead of time. That prediction is the
product. Everything else is plumbing.

---

## 2. Users

| User | Needs |
|---|---|
| Wet lab operator | One number before the run. One alarm during it |
| Modeller | Measured trace against predicted trace, exportable |
| iGEM judge | Evidence the model drives hardware, not a slide |

---

## 3. Scope

**In:** pH read, dissolved oxygen read, titrant dosing, air pump state, run log,
predicted-versus-measured chart, CSV export.

**Out:** temperature control and the V1→V2 vessel transfer. The team deferred
both on 2026-08-11. Also out: user accounts, cloud sync, multi-vessel.

One vessel. One run at a time.

---

## 4. Architecture

Five layers. Copy the Pioreactor shape; do not copy its code.

```
  probes, pumps                    ADC + GPIO, calibration
       │  MQTT
  message bus                      Mosquitto, one topic per channel
       │
  store                            SQLite, one file per run
       │
  control + predict                Python. Imports src/. PID with deadband
       │
  UI                               web page, charts, set point, alarms
```

Python throughout, so the control layer imports `src/leach.py` directly rather
than reimplementing it. Raspberry Pi host.

---

## 4a. The sensor boundary

Added 2026-09-18, and it governs every screen.

**The Run screen may show a value only if a probe produces it.** A quantity the
model computes but no instrument can measure is a prediction. Predictions live
on Setup and on Report, never on the live view.

The inventory is [`dashboard-prototype/sensors.yaml`](../dashboard-prototype/sensors.yaml).

| Channel | Device | Feed today |
|---|---|---|
| pH | pH probe | model trajectory |
| Dissolved oxygen | DO probe | model oxygen balance, `kLa` scaled by air pump rate |
| Temperature | temperature probe | **none.** Deferred 2026-08-11; the model has no temperature state |
| Supply voltage | voltage monitor | **none.** Equipment, not process. See below |
| Titrant delivered | flow meter or balance | model trajectory |

**Not measurable by anything on the rig**, and therefore off the Run screen:
gold dissolved, tetrathionate conversion, Cu(II), and the gold handed to
capture. Each needs an assay or a titration on a drawn sample.

**Titrant is measured, not inferred.** Pump run-time times calibrated flow is a
*commanded* quantity, and it reports liquid a stalled pump never delivered. The
console tracks both and trips when they diverge by more than 1 mL. That is the
fourth interlock and it is the reason the flow meter is on the list.

**Voltage is the supply rail**, confirmed by the team on 2026-09-18, in
volts. It is an *equipment* variable. It says nothing about the chemistry, so
it carries no set point and it does not sit among the probe readings; it sits
with the pump states.

It earns that place because the pumps run off it. A sagging rail is the
physical cause of the stall that the flow-divergence interlock catches as a
symptom, so the supply reading is what tells an operator *why* the pump fell
behind.

It is **not** solution potential. Eh or ORP in millivolts is a different
measurement and this rig does not take it, so the Cu(II)/Cu(I) couple stays
unmeasured.

Two values must come from the team before this channel can raise an alarm: the
nominal rail and the low threshold. Both are `null` in `sensors.yaml`
(`nominal_V`, `alarm_low_V`), so nothing can read a guess. Until they are set
and the power supply emits telemetry, the row reads `no feed`.

### Control surface

The dashboard commands actuators to **stop** or to **run slower**. Nothing else.

| Actuator | Count | Commands | Stopped by an interlock? |
|---|---|---|---|
| Titrant pump | **one per vessel**, V1 to V4 | stop, rate 100 / 50 / 25 % | Yes |
| Air pump | V3 only; `null`, not decided, elsewhere | stop, rate 100 / 50 / 25 % | No, alarm only |

**Each vessel owns its titrant pump.** One global rate and one global stop
were wrong: stopping the pump on a vessel you are not using should not stop the
batch. The Equipment panel commands one
vessel at a time, chosen from a dropdown, and snaps to whichever vessel takes
over at a stage change. The control loop always uses the *running* vessel's
pump, not whichever one the panel happens to show.

**Link state comes before activity.** A pump reading said `Idle` on every
vessel, which asserted that a pump was attached and waiting. On V1 and V4
nothing is attached, so the console had no standing to say it. The states, in
precedence order:

| State | Meaning |
|---|---|
| `not connected` | Nothing attached. The vessel's `feed` is `none`, so there is no path to its pump either |
| `stopped` | The operator stopped it |
| `no target` | Attached, but its stage records no set point and no window, so there is nothing to hold |
| `dosing` | This vessel is running and the pump is on |
| `idle` | This vessel is running, between doses |
| `connected` | Attached, and not part of the run in progress |

Nothing below `not connected` is knowable without a link, which is why it is
first. The vessel table and the Equipment panel read the same function, so they
cannot disagree.

**Every number names its reference.** A bare `Rate 100 %`, `Duty 0.27 %` or
`Commanded 18.47 mL` names a quantity with nothing to measure it against. Each
label now carries the reference it is relative to:

| Readout | Reference | What it is |
|---|---|---|
| Rate, titrant | the vessel's `Pump, mL/min` from Setup | The pump runs at this share of its calibrated flow |
| Rate, air | `kLa`, from `params/leach.yaml` | Scales `kLa` linearly in the oxygen balance |
| Duty | elapsed run time | The share of the run so far that the pump has been on. A high duty means it is struggling to hold the set point |
| Commanded | none; it is a total | Cumulative titrant the console asked for |
| Drift | the flow meter | Commanded less measured. **This is the quantity the fourth interlock trips on**, so it is shown rather than left to be inferred |

Drift turns amber at half the tolerance and red at it. The tolerance appears in
its own label and is read from the same constant the interlock uses, so the two
cannot disagree.

Only V3 is aerated in the model: `params/leach.yaml` carries `kLa` and
`C_star` for the leach and for no other stage. `air_pump` is `null` on the
other three, which records that nobody has decided, not that there is no pump.

Air pump rate scales `kLa` in the model's own oxygen balance, so stopping it
drives the DO reading down through the model rather than through a guess.

---

## 5. Data contract

Topic shape, one metric per topic:

```
biorecovery/{vessel}/{run_id}/{channel}/{metric}
```

| Channel | Metrics | Direction |
|---|---|---|
| `ph` | `reading`, `calibration_age_h` | sensor → bus |
| `do` | `reading_pct`, `reading_uM` | sensor → bus |
| `pump_titrant` | `state`, `dose_mL`, `total_mL` | both |
| `pump_air` | `state`, `duty` | both |
| `predict` | `titrant_mL`, `au_feed_uM`, `eta` | model → bus |

Dose events publish at QoS 2. A dose recorded twice is a wrong reagent budget.

SQLite tables: `runs`, `readings`, `dose_events`, `predictions`, `alarms`,
`calibrations`. One row per reading. No aggregation at write time.

---

## 6. Screens

Three. No more.

1. **Before the run.** Enter charge mass and scenario. Show predicted titrant in
   millilitres, predicted gold in the liquor, predicted batch time.
2. **During the run.** pH trace with the set point band drawn on it. Cumulative
   titrant delivered against cumulative titrant predicted. DO trace. Alarm list.
3. **After the run.** Export CSV. Show measured against predicted, one chart.

---

## 7. Control logic

**pH.** Set point `pH_set`. Deadband ±0.1 pH, so the pump does not chatter and
does not over-dose. Outside the band, run the titrant pump for a fixed pulse, then
wait one mixing time before reading again. Never dose on a reading older than 30 s.

**The titrant is acid, not base.** `titrant_demand()` is signed, and every
scenario in `params/leach.yaml` returns a negative value: −35,658 µmol/L for
glycine at the mid band, −68,758 for ammonia. The leach is net base-producing,
because the alkaline return leg makes two protons per trithionate. The pump
therefore delivers acid. Size the reagent order accordingly.

**Six stages sit in four vessels**, so V3 and V4 host two stages each.

**The vessel is the unit, not the stage.** Set 2026-09-18. Every vessel carries
a pH probe and a titrant pump, and the inventory is the `vessels` block of
[`sensors.yaml`](../dashboard-prototype/sensors.yaml). Two rules follow, and
they are not the same rule:

- **Monitoring is unconditional.** A vessel on that list has its pH read and
  shown, whatever else is unknown about it. All four appear on the Run screen.
- **Dosing is conditional.** A loop needs a target, and the target comes from
  the stage running in the vessel. A vessel whose stages record neither a set
  point nor a window is **monitored and not dosed**, and the screen says so.

Set points are graded, because they are not equal. `measured_optimum` and
`operating_choice` read firm; `analogue_only`, `organism_requirement` and
`undetermined` read muted. The grade is `status` in
[`stage_ph.yaml`](../dashboard-prototype/stage_ph.yaml); the console reads it
rather than presenting all four alike.

Only V2 and V3 have a data feed today, so only they show a live reading. V1 and
V4 show `no feed`: both have a time course in the model, but neither carries a
pH state, so nothing can drive the probe.

**Adding a vessel takes no code.** Add an entry to the `vessels` block and give
its stages a matching `vessel` in `stage_ph.yaml`. Nothing in `index.html`
enumerates V1 to V4; the dropdowns, the vessel table and the per-vessel reagent
and pump records all build from that list.

**The leach and capture share V3, and their windows overlap.** The leach runs
at 9.3 to 10.5 and capture wants 9.0 to 10.5, so the leach operating pH already
sits inside capture's window, and nothing needs adjusting between them in the
same vessel. That is a convenience, not a licence: capture's window is a thiol
analogue, not a GolB measurement, per `ISSUES.md` item 23.

**Every stage holds its own set point.** The chain does not have one pH, it has
six, and they do not agree. `ISSUES.md` item 23 states the conflict plainly:
TetH at pH 3, *E. coli* at pH 7, the leach at pH 9.3 to 10.5. That is about
6.5 pH units inside one process, and nothing in the model costs the titrant
that crossing it needs.

| # | Vessel | Stage | Set point | Window | Status |
|---|---|---|---|---|---|
| 1 | V1 | Culture and expression | 7.0 | none recorded | organism requirement, ISSUES 23, 32 |
| 2 | V2 | Tetrathionate hydrolysis | 3.0 | none recorded | measured optimum, ISSUES 38 |
| 3 | V3 | Bioleaching | from the scenario | 9.3 – 10.5 | operating choice, `params/leach.yaml` |
| 4 | V3 | Capture on GolB | **null** | 9.0 – 10.5 | thiol analogue only, ISSUES 23 |
| 5 | V4 | Elution | **null** | none recorded | undetermined, ISSUES 28 |
| 6 | V4 | Reduction | 7.0 | none recorded | GolR analogue only, SOURCES S53 |

The table lives in [`dashboard-prototype/stage_ph.yaml`](../dashboard-prototype/stage_ph.yaml),
which cites a source for every row. A stage whose set point is null cannot be
run: the console refuses it rather than guessing, which is rule 4 expressed in
the interface.

Two rows carry a warning the operator must see on screen:

1. **Stage 2 is a standing conflict.** TetH needs pH 3 and thiosulfate does not
   survive there. The model has no term for the acid loss, so it cannot see the
   problem. Treat the 95.9 % conversion in three days as an upper bound.
2. **Only stage 3 has a modelled titrant demand.** Stage 2 has no proton
   balance anywhere in the repository, and the swing from pH 3 to pH 10 is not
   costed at all.

**Dissolved oxygen.** Monitor and alarm only, in the first version. The model
has no DO controller: [leach.py](../src/leach.py) L666 treats aeration as a fixed `kLa`, not
as a manipulated variable. A DO set point needs a model decision first, §9.

**Interlocks.** Four, all hard stops on the titrant pump. A fifth, on low
supply voltage, is listed in section 9 and is **not built**, because its
threshold has no value yet:

1. Stale reading. No pH value for 60 s.
2. Flow divergence. Commanded and measured titrant differ by more than 1 mL.
3. Dose ceiling. Measured delivery passes the predicted batch demand.
4. Out of window. pH outside the active stage's window.

---

## 8. Interface to the model

The dashboard calls these. It does not reimplement them.

| Need | Call | Returns |
|---|---|---|
| Predicted titrant demand | `titrant_demand`, [leach.py](../src/leach.py) L811 | µmol/L, signed. Negative means acid |
| Trajectory | `simulate_sequential`, [leach.py](../src/leach.py) L735 | dict of state arrays |
| Named operating point | `run_scenario`, [leach.py](../src/leach.py) L938 | ledger dict |
| Gold in the liquor | `au_feed_from_leach`, [interfaces.py](../src/interfaces.py) L64 | µM |
| Parameters | `load`, [params.py](../src/params.py) L16 | dict from `params/*.yaml` |

Two repository rules carry into the dashboard code unchanged:

- **No number in a `.py` file** (`AGENTS.md` §1 rule 2). Deadband, pulse width,
  interlock timeouts and pump calibration all go in `params/dashboard.yaml`.
- **A null parameter raises** (rule 4). The dashboard must refuse to start, not
  substitute a default.

`pH_control` defaults false at [leach.yaml](../params/leach.yaml) L1097. The dashboard sets it
true, because a real pump holds the pH.

---

## 9. Open decisions

Nothing is built until items 1 to 3 are answered. They are numbers, not code.

| # | Decision | State |
|---|---|---|
| 1 | `pH_set` | **Null at [leach.yaml](../params/leach.yaml) L1112.** Window 9.3–10.5, recommended 10.0–10.3 |
| 2 | Vessel working volume, `V_L` | **Null for all four vessels** in `sensors.yaml`. Needed once per vessel |
| 3 | Titrant stock concentration, `C_titrant` mol/L | **Null for all four vessels** in `sensors.yaml`. Needed once per vessel, and V2 holds pH 3 while V3 holds pH 10 |
| 4 | Pump calibration, mL per second | Measured on the bench, not modelled. One figure per pump |
| 5 | DO set point and cascade | Needs a model decision first, §7 |
| 6 | Supply voltage: nominal rail and low threshold | **Null** at [sensors.yaml](../dashboard-prototype/sensors.yaml) (nominal_V, alarm_low_V). Blocks the fifth interlock |
| 7 | Do V2 and V3 run in sequence or at the same time? | **Unconfirmed, 2026-09-18.** Sequential chaining was removed rather than left asserting something the team does not yet know. Concurrent running needs two independent sensor streams and two control loops |

Items 2 and 3 convert the model output into the number the operator reads:

```
V_titrant_mL = abs(titrant_demand_umol_per_L) * V_L / (1000 * C_titrant_mol_per_L)
```

That conversion belongs in `params/conversions.yaml`, not in dashboard code.

---

## 10. Build order

| M | Milestone | Done when |
|---|---|---|
| 1 | Read and log | pH and DO land in SQLite for 1 h with no gap |
| 2 | Display | Screen 2 draws both traces live |
| 3 | Predict | Screen 1 prints titrant demand in mL for a given charge |
| 4 | Dose, open loop | Operator confirms each dose; totaliser matches the bench |
| 5 | Close the loop | pH holds set point ±0.1 for 1 h unattended |

Milestone 3 is the iGEM deliverable. Milestones 4 and 5 are the demonstration.

---

## 11. Acceptance criteria

1. Predicted titrant demand and delivered titrant agree within 20 % over one batch.
2. pH stays inside ±0.1 of `pH_set` for 95 % of a 1 h unattended run.
3. Every interlock in §7 fires in a bench test, and each is logged.
4. A run exports a CSV that reproduces both charts with no manual editing.
5. The dashboard refuses to start when any parameter it needs is null.

---

## 12. What exists today

| Piece | Where |
|---|---|
| Trajectory export from the model | [`dashboard-prototype/export_runs.py`](../dashboard-prototype/export_runs.py) |
| Three-screen console, browser only | [`dashboard-prototype/index.html`](../dashboard-prototype/index.html) |
| Per-stage pH table, sourced row by row | [`dashboard-prototype/stage_ph.yaml`](../dashboard-prototype/stage_ph.yaml) |
| Sensor and actuator inventory | [`dashboard-prototype/sensors.yaml`](../dashboard-prototype/sensors.yaml) |

**The console runs one stage at a time.** Pick V2 or V3; it holds that
stage's set point for the whole run.

The old option that chained V2 into V3 through a 60 minute vessel swing was
removed on 2026-09-18. The team expects the two stages may instead run
**concurrently**, each on its own sensor stream, and that is **not confirmed**.
Nothing is built for it. Until the team decides, the console makes no claim
about how the two stages compose, which is open decision 7.

**Stages 1, 4, 5 and 6 are not on any screen.** Removed 2026-09-18 at the
team's direction. Only stages 2 and 3 have a pH set point and a titrant demand,
so only they give a controller anything to do; showing the other four implied a
scope the console does not have. Their set points stay in
[`stage_ph.yaml`](../dashboard-prototype/stage_ph.yaml) with the reason each one
cannot run, and the console surfaces them under `Sources`.

The prototype is **screens and logic only**. It replays an exported trajectory;
it reads no probe and drives no pump. Milestones 1, 4 and 5 in §10 are untouched.
Run it with `python -m http.server 8932 --directory dashboard-prototype`.

The buffer capacity that turns unmet titrant demand into a pH deviation is a
display assumption of the prototype page. It is not in `params/`, and it must
not be copied into the real controller without a source.

---

## See also

- [`AGENTS.md`](../AGENTS.md) — the rules this software inherits
- [`STRUCTURE.md`](../STRUCTURE.md) — repository layout
- [`docs/ISSUES.md`](ISSUES.md) — the findings record
