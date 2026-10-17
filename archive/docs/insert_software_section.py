"""Place the software section into the wiki page.

Idempotent. Running it twice replaces the section rather than adding a second
one, so the wiki can be regenerated after any change to sensors.yaml or
stage_ph.yaml without hand-editing wiki-prototype/index.html.

Order of operations:

    python docs/make_software_tables.py     builds the tables from the YAML
    python docs/make_wiki_dashboard.py      builds the themed dashboard page
    python docs/insert_software_section.py  places the section and the nav link

The prose here is the only hand-written part, and it states the boundary the
prototype actually has. AGENTS.md section 11 rule 5 forbids describing
infrastructure that does not exist: the dashboard reads no probe and drives no
pump, and the section says so twice.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "wiki-prototype" / "index.html"
TABLES = ROOT / "docs" / "media" / "wiki" / "software_tables.html"

START = "    <!-- SOFTWARE SECTION START, generated -->"
END = "    <!-- SOFTWARE SECTION END -->"

NAV_LINK = """      <a class="nav-link" href="#software">
        <span aria-hidden="true">08</span>
        Monitoring software
      </a>
"""

CSS = """
/* ---------- software section ---------- */
.software-section .software-lede p { max-width: 62ch; }

.software-table { margin-bottom: 26px; }
.software-table col:nth-child(1) { width: 22%; }

.software-panel {
  display: grid;
  gap: 18px;
  margin: 26px 0;
  grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
}

.software-panel article {
  padding: 16px 18px 18px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: #fff;
}

.software-panel span {
  display: block;
  margin-bottom: 6px;
  color: var(--muted);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.software-panel strong {
  display: block;
  font-size: 19px;
  font-weight: 500;
  letter-spacing: -0.02em;
}

.software-panel p {
  margin: 7px 0 0;
  color: var(--muted);
  font-size: 13.5px;
  line-height: 1.55;
}

.software-open {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  margin: 8px 0 26px;
  padding: 13px 20px;
  border: 1px solid #d8c89e;
  border-radius: 9px;
  background: #f8efd6;
  color: #725817;
  font-size: 14.5px;
  font-weight: 600;
  text-decoration: none;
}

.software-open:hover { background: #f4e7c6; }
.software-open::after { content: "\\2197"; font-weight: 400; }

.software-caveat {
  margin: 0 0 26px;
  padding: 14px 18px;
  border-left: 3px solid var(--gold);
  background: #faf6ec;
  color: var(--ink);
  font-size: 13.5px;
  line-height: 1.6;
}
"""

SECTION = """    <!-- SOFTWARE SECTION START, generated -->
    <section class="model-section software-section" id="software" aria-labelledby="software-title">
      <div class="section-heading">
        <span class="section-number">08</span>
        <div>
          <p class="section-kicker">Hardware and software</p>
          <h2 id="software-title">Monitoring software</h2>
        </div>
      </div>

      <p class="stage-question">What can the bioreactor actually measure, and what can we tell it to do?</p>

      <div class="opening-answer">
        <span class="evidence prediction">Design rule</span>
        <p>The dashboard shows a value only when an instrument produces it. A quantity the model computes but no probe can measure is a prediction, and predictions are labelled as such rather than displayed beside live readings.</p>
      </div>

      <div class="body-copy software-lede">
        <p>The models on this page answer how much reagent a batch needs. Running the batch is a separate problem: the vessel drifts, and something has to notice and correct it. We built a browser dashboard that takes the model's titrant prediction as a feed-forward target, then holds each stage's pH against it using the probes on the rig.</p>
        <p>Its design rests on one boundary. Every reading comes from an instrument, and every command is either <em>stop</em> or <em>run slower</em>. Nothing on the live screen is inferred, and nothing the dashboard sends can drive a pump harder than its own calibration.</p>
      </div>

      <a class="software-open" href="dashboard.html" target="_blank" rel="noopener">Open the dashboard</a>

      <p class="software-caveat"><strong>No probe is attached.</strong> The prototype replays a trajectory exported from the models on this page, so that the interface and the control logic can be exercised before hardware exists. The dashboard labels its own data <em>simulated feed</em> in the top bar.</p>

      <section class="software-monitored" aria-labelledby="software-monitored-title">
        <div class="subsection-heading">
          <p class="section-kicker">What it monitors</p>
          <h3 id="software-monitored-title">Five channels, three of them fed</h3>
        </div>
        <div class="body-copy">
          <p>Each channel is one instrument. A channel with no data source is drawn as awaiting a sensor rather than filled with a plausible number.</p>
        </div>
__CHANNELS__
      </section>

      <section class="software-vessels" aria-labelledby="software-vessels-title">
        <div class="subsection-heading">
          <p class="section-kicker">Where it monitors</p>
          <h3 id="software-vessels-title">Four vessels, six stages</h3>
        </div>
        <div class="body-copy">
          <p>Monitoring is unconditional: every vessel has its pH read. Control is not, because a loop needs a target, and the targets are not equally well founded. A vessel whose stage records no set point is monitored and not dosed.</p>
        </div>
__VESSELS__
      </section>

      <section class="software-control" aria-labelledby="software-control-title">
        <div class="subsection-heading">
          <p class="section-kicker">What it controls</p>
          <h3 id="software-control-title">Stop or slow, and four interlocks</h3>
        </div>
        <div class="software-panel">
          <article>
            <span>Titrant pump</span>
            <strong>One per vessel</strong>
            <p>Stop, or run at 100, 50 or 25 per cent of its calibrated flow. Stopped by any interlock.</p>
          </article>
          <article>
            <span>Air pump</span>
            <strong>V3 only</strong>
            <p>Its rate scales the oxygen transfer coefficient in the model's own oxygen balance. Raises an alarm, never stops the batch.</p>
          </article>
          <article>
            <span>Interlocks</span>
            <strong>Four hard stops</strong>
            <p>Stale reading, flow divergence, dose ceiling, and pH outside the stage window.</p>
          </article>
        </div>
      </section>

      <aside class="finding-card software-finding">
        <span class="evidence prediction">Design consequence</span>
        <strong>A flow meter catches a stalled pump that a run-time totaliser reports as healthy.</strong>
        <p>Pump run-time multiplied by calibrated flow is a <em>commanded</em> quantity: it counts liquid a stalled pump never delivered. The dashboard tracks commanded and measured delivery separately and stops dosing when they diverge by more than one millilitre. In a fault test the command reached 1.03 mL while the flow meter read zero, and the interlock fired. A totaliser would have recorded a complete dose.</p>
      </aside>

      <section class="software-limits" aria-labelledby="software-limits-title">
        <div class="subsection-heading">
          <p class="section-kicker">What it cannot see</p>
          <h3 id="software-limits-title">Four quantities with no instrument</h3>
        </div>
        <div class="body-copy">
          <p>These are the quantities the models predict that no probe on the rig can confirm. They appear on the planning and reporting screens, never on the live one, and the report marks their measured column <em>no assay</em>.</p>
        </div>
__NOTMEASURABLE__
      </section>

      <div class="recovery-links" aria-label="Software resources">
        <a href="dashboard.html" target="_blank" rel="noopener"><strong>The dashboard</strong><span>Opens in a new tab</span></a>
        <a href="../docs/DASHBOARD_SPEC.md"><strong>Product specification</strong><span>Screens, control logic and open decisions</span></a>
        <a href="../dashboard-prototype/sensors.yaml"><strong>Instrument inventory</strong><span>Channels, actuators and vessels</span></a>
        <a href="../dashboard-prototype/stage_ph.yaml"><strong>Per-stage set points</strong><span>Each one with its status and source</span></a>
      </div>
    </section>
    <!-- SOFTWARE SECTION END -->
"""


def indent(block, pad="        "):
    return "\n".join(pad + line.strip() if line.strip() else ""
                     for line in block.strip().splitlines())


def split_tables(text):
    """The generator emits three tables in order: channels, vessels, limits."""
    parts, cur = [], []
    for line in text.splitlines():
        if line.startswith("<!--"):
            continue
        cur.append(line)
        if line.strip() == "</table>":
            parts.append("\n".join(cur))
            cur = []
    if len(parts) != 3:
        raise SystemExit("expected 3 tables from make_software_tables.py, got %d"
                         % len(parts))
    return parts


def build():
    if not TABLES.exists():
        raise SystemExit("run docs/make_software_tables.py first")
    channels, vessels, limits = split_tables(TABLES.read_text(encoding="utf-8"))

    section = (SECTION
               .replace("__CHANNELS__", indent(channels))
               .replace("__VESSELS__", indent(vessels))
               .replace("__NOTMEASURABLE__", indent(limits)))

    page = PAGE.read_text(encoding="utf-8")

    # idempotent: replace an existing section rather than appending a second
    if START in page:
        a = page.index(START)
        b = page.index(END) + len(END) + 1
        page = page[:a] + section + page[b:]
    else:
        anchor = "  </main>\n"
        if anchor not in page:
            raise SystemExit("closing </main> not found")
        page = page.replace(anchor, section + anchor, 1)

    if 'href="#software"' not in page:
        nav_end = "    </nav>\n"
        if nav_end not in page:
            raise SystemExit("sidebar nav not found")
        page = page.replace(nav_end, NAV_LINK + nav_end, 1)

    PAGE.write_text(page, encoding="utf-8")

    css_path = ROOT / "wiki-prototype" / "styles.css"
    css = css_path.read_text(encoding="utf-8")
    if "/* ---------- software section ---------- */" not in css:
        css_path.write_text(css.rstrip() + "\n" + CSS, encoding="utf-8")
        print("  appended software styles to wiki-prototype/styles.css")

    print("placed the software section into %s" % PAGE.relative_to(ROOT))
    print("  page now %d lines" % len(page.splitlines()))
    print("  nav entries: %d" % page.count('class="nav-link'))


if __name__ == "__main__":
    build()
