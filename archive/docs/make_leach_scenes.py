"""Build the ten-scene leaching animation, desktop 16:9 and mobile portrait.

The figure walks one ammonia-free leach from a full thiosulfate charge to
exhaustion, one reaction at a time. Every scene carries three things at once:
a large headline saying what is happening, animated species showing what
changes, and a large outcome label saying why it matters.

Every balanced reaction below is quoted from the source document
"Bioleaching_Models_v5", paragraphs 147-166, and matches docs/EQUATIONS.md
lines 123-150 and docs/MASTER.md lines 570-575 word for word:

    4 Au(0) + 8 S2O3(2-) + O2 + 2 H2O ->  4 Au(S2O3)2(3-) + 4 OH(-)   gold, O2
    Au(0) + 2 S2O3(2-) + Cu(II)       ->  Au(S2O3)2(3-) + Cu(I)       gold, Cu(II)
    4 Cu(0) + O2 + 8 S2O3(2-) + 2 H2O ->  4 [Cu(S2O3)2](3-) + 4 OH(-) copper, O2
    Cu(0) + Cu(2+) + 4 S2O3(2-)       ->  2 [Cu(S2O3)2](3-)           comproportionating
    4 Cu(I) + O2 + 2 H2O              ->  4 Cu(II) + 4 OH(-)          re-oxidation, v4
    2 Cu(II) + 2 S2O3(2-)             ->  2 Cu(I) + S4O6(2-)          parasitic, v3

Three facts fix the quantities drawn here.

1. Copper is never fed in. It comes off the board as Cu(0) and dissolves as
   Cu(I) on both routes, so v4 is the only source of Cu(II) in the model
   (EQUATIONS.md line 208). Cu(II) is a reactant of the parasitic step, not a
   product: it is spent there and handed back as Cu(I).
2. Re-oxidation consumes no thiosulfate, so the gauge does not move in the
   Cu(II) scene. Only gold, copper metal and the parasitic step draw on it
   (EQUATIONS.md line 180).
3. The budget splits gold 0.06 %, copper metal 1.7 %, parasitic 98.2 %
   (MASTER.md lines 745-750). The lower strip draws that split to true scale.
   The draining gauge above it exaggerates the first two steps so they are
   visible at all, and the strip is what carries the real proportion.

Gold reaches 28.5 % at 72 h (MASTER.md line 742), so the gold film ends the
run at 0.715 of its starting width and the dissolved-gold readout ends at
0.285. Cu(II) keeps climbing after the thiosulfate is gone, which is what the
model does.

Oxygen is supplied by an air pump (v5 paragraph 443). The pump is drawn above
the vessel with a pipe entering the top, which is the team's arrangement; no
source document fixes the entry point either way.

The animation degrades cleanly. Without scripting the ten scenes cycle on a
CSS clock, so the file still teaches inside an <img>. With scripting, which
needs an <object> or inline embed, the reader gets play, pause, step and an
equation toggle. Reduced motion freezes all movement and keeps every label.

Writes both files under docs/media/wiki/concepts/.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent / "media" / "wiki" / "concepts"

# ---------------------------------------------------------------- palette

INK = "#252523"
MUTED = "#73736e"
RULE = "#e6e6e0"
PAPER = "#fbfbfa"
PANEL = "#f3f3ef"
DEAD = "#d5d5d1"

GOLD = "#b98524"
CU1 = "#c08a63"          # copper(I), the reduced form
CU2 = "#8a3f2a"          # copper(II), the oxidant
COPPER = "#9a6040"       # copper metal on the board
TEAL = "#2d9297"         # thiosulfate
VIOLET = "#8d73a8"       # tetrathionate
OXY = "#3f7fb5"          # oxygen
BOARD = "#4e5a4a"        # PCB substrate

FADE = 0.35              # scene crossfade, per cent of the master clock

# ---------------------------------------------------------------- scenes
#
# gauge  fraction of the thiosulfate charge still in the vessel
# au/cu2/tet  readout fractions, 0 to 1
# goldw/cuw   what is left of the gold film and the copper bulk on a fragment
# pop         how many particles of each species are in the liquid

SCENES = [
    dict(
        key="start", stage="START", pump=False, tint=None,
        headline="THE LEACHING VESSEL STARTS WITH A FINITE THIOSULFATE SUPPLY",
        category="STARTING CHEMISTRY", cat_colour=TEAL,
        equation=None,
        note="The charge is fixed. Nothing in this vessel makes more of it.",
        outcomes=[
            ("THIOSULFATE LIQUOR FILLS THE VESSEL", TEAL),
            ("CRUSHED PCB: THIN GOLD OVER BULK COPPER", COPPER),
            ("NOTHING HAS DISSOLVED YET", MUTED),
        ],
        dur=4.5, gauge=1.00,
        au=(0.00, "NONE YET"), cu2=(0.00, "NONE YET"), tet=(0.00, "NONE YET"),
        goldw=1.00, cuw=1.00,
        pop=dict(thio=34, o2=0, au=0, cu1=0, cu2=0, tet=0),
    ),
    dict(
        key="gold-o2", stage="GOLD", pump=True, tint=GOLD,
        headline="DESIRED REACTION: OXYGEN HELPS DISSOLVE GOLD",
        category="DESIRED REACTION", cat_colour=GOLD,
        equation="4Au⁰ + 8S₂O₃²⁻ + O₂ + 2H₂O "
                 "→ 4Au(S₂O₃)₂³⁻ + 4OH⁻",
        outcomes=[
            ("GOLD LEAVES THE PCB AND REMAINS DISSOLVED", GOLD),
            ("TWO THIOSULFATES ARE SPENT PER GOLD ATOM", TEAL),
            ("THIS IS THE ONLY REACTION WE WANT", MUTED),
        ],
        dur=6.5, gauge=0.99,
        au=(0.10, "INCREASING"), cu2=(0.00, "NONE YET"), tet=(0.00, "NONE YET"),
        goldw=0.95, cuw=1.00,
        pop=dict(thio=26, o2=6, au=3, cu1=0, cu2=0, tet=0),
    ),
    dict(
        key="copper-o2", stage="COPPER", pump=True, tint=COPPER,
        headline="COMPETING METAL REACTION: COPPER ALSO CONSUMES THIOSULFATE",
        category="COMPETING METAL REACTION", cat_colour=COPPER,
        equation="4Cu⁰ + O₂ + 8S₂O₃²⁻ + 2H₂O "
                 "→ 4[Cu(S₂O₃)₂]³⁻ + 4OH⁻",
        outcomes=[
            ("COPPER ENTERS THE LIQUID AS Cu(I)", CU1),
            ("MORE THIOSULFATE IS CONSUMED", TEAL),
            ("THERE IS FAR MORE COPPER THAN GOLD ON THE BOARD", MUTED),
        ],
        dur=6.5, gauge=0.94,
        au=(0.10, "HOLDING"), cu2=(0.00, "NONE YET"), tet=(0.00, "NONE YET"),
        goldw=0.95, cuw=0.90,
        pop=dict(thio=22, o2=6, au=3, cu1=6, cu2=0, tet=0),
    ),
    dict(
        key="reoxidation", stage="Cu(II)", pump=True, tint=OXY,
        headline="OXYGEN RE-OXIDISES Cu(I) TO Cu(II)",
        category="RE-OXIDATION BY THE PUMP", cat_colour=OXY,
        equation="4Cu(I) + O₂ + 2H₂O → 4Cu(II) + 4OH⁻",
        outcomes=[
            ("THE OXYGEN SUPPLY CONTINUOUSLY REBUILDS Cu(II)", OXY),
            ("NO THIOSULFATE IS SPENT HERE", TEAL),
            ("THIS IS WHY Cu(II) NEVER RUNS OUT", MUTED),
        ],
        dur=6.0, gauge=0.94,
        au=(0.10, "HOLDING"), cu2=(0.45, "RISING"), tet=(0.00, "NONE YET"),
        goldw=0.95, cuw=0.90,
        pop=dict(thio=22, o2=8, au=3, cu1=2, cu2=6, tet=0),
    ),
    dict(
        key="gold-cu", stage="Cu(II) PATHS", pump=False, tint=GOLD,
        headline="PRODUCTIVE Cu(II) PATH: Cu(II) ACCEPTS ELECTRONS FROM GOLD",
        category="PRODUCTIVE Cu(II) PATH", cat_colour=GOLD,
        equation="Au⁰ + 2S₂O₃²⁻ + Cu(II) "
                 "→ Au(S₂O₃)₂³⁻ + Cu(I)",
        outcomes=[
            ("ANOTHER GOLD ATOM ENTERS SOLUTION", GOLD),
            ("Cu(II) RETURNS TO Cu(I)", CU1),
            ("WEAK WITHOUT AMMONIA: A SLIVER OF THE GOLD COMES THIS WAY", MUTED),
        ],
        dur=6.0, gauge=0.93,
        au=(0.16, "INCREASING"), cu2=(0.35, "SPENT, RETURNED"),
        tet=(0.00, "NONE YET"),
        goldw=0.90, cuw=0.90,
        pop=dict(thio=20, o2=4, au=5, cu1=4, cu2=4, tet=0),
    ),
    dict(
        key="comproportionation", stage="Cu(II) PATHS", pump=False, tint=COPPER,
        headline="Cu(II) CAN ALSO REACT WITH METALLIC COPPER",
        category="COMPROPORTIONATING ROUTE", cat_colour=COPPER,
        equation="Cu⁰ + Cu²⁺ + 4S₂O₃²⁻ "
                 "→ 2[Cu(S₂O₃)₂]³⁻",
        outcomes=[
            ("MORE Cu(I) IS FORMED", CU1),
            ("FOUR THIOSULFATES ARE USED PER REACTION", TEAL),
            ("TWICE THE COST OF THE OXYGEN ROUTE", MUTED),
        ],
        dur=6.0, gauge=0.90,
        au=(0.16, "HOLDING"), cu2=(0.22, "FALLING"), tet=(0.00, "NONE YET"),
        goldw=0.90, cuw=0.82,
        pop=dict(thio=17, o2=4, au=5, cu1=7, cu2=2, tet=0),
    ),
    dict(
        key="parasitic", stage="PARASITIC", pump=False, tint=VIOLET,
        headline="PARASITIC REACTION: Cu(II) DESTROYS THE LEACHANT",
        category="PARASITIC REACTION", cat_colour=VIOLET,
        equation="2Cu(II) + 2S₂O₃²⁻ "
                 "→ 2Cu(I) + S₄O₆²⁻",
        outcomes=[
            ("THIOSULFATE BECOMES TETRATHIONATE", VIOLET),
            ("NO GOLD IS DISSOLVED", MUTED),
            ("Cu(II) RETURNS TO Cu(I)", CU1),
        ],
        dur=8.0, gauge=0.62,
        au=(0.16, "HOLDING"), cu2=(0.30, "SPENT, RETURNED"),
        tet=(0.35, "ACCUMULATING"),
        goldw=0.90, cuw=0.82,
        pop=dict(thio=11, o2=4, au=5, cu1=8, cu2=3, tet=4),
    ),
    dict(
        key="loop", stage="PARASITIC", pump=True, tint=VIOLET, loop=True,
        headline="COPPER IS RECYCLED — THIOSULFATE IS NOT",
        category="THE COPPER LOOP", cat_colour=CU2,
        equation="4Cu(I) + O₂ + 2H₂O → 4Cu(II) + 4OH⁻"
                 "  "
                 "2Cu(II) + 2S₂O₃²⁻ "
                 "→ 2Cu(I) + S₄O₆²⁻",
        outcomes=[
            ("THE SAME COPPER GOES ROUND FOR EVER", CU2),
            ("OXYGEN REBUILDS Cu(II) EVERY TURN", OXY),
            ("THE LEACHANT NEVER COMES BACK", TEAL),
        ],
        dur=10.0, gauge=0.30,
        au=(0.20, "BARELY MOVING"), cu2=(0.40, "CYCLING"),
        tet=(0.62, "ACCUMULATING"),
        goldw=0.85, cuw=0.75,
        pop=dict(thio=7, o2=8, au=6, cu1=8, cu2=4, tet=7),
    ),
    dict(
        key="compete", stage="COMPETITION", pump=True, tint=None,
        headline="PRODUCTIVE AND PARASITIC REACTIONS NOW COMPETE",
        category="BOTH PATHWAYS RUNNING", cat_colour=INK,
        equation="DESIRED  Au⁰ → Au(S₂O₃)₂³⁻"
                 "  "
                 "COMPETING  S₂O₃²⁻ → S₄O₆²⁻",
        outcomes=[
            ("OXYGEN HELPS GOLD DISSOLUTION", GOLD),
            ("OXYGEN ALSO REGENERATES Cu(II)", OXY),
            ("TETRATHIONATE APPEARS FAR FASTER THAN DISSOLVED GOLD", VIOLET),
        ],
        dur=7.5, gauge=0.12,
        au=(0.26, "CREEPING UP"), cu2=(0.55, "RISING"),
        tet=(0.82, "RISING FAST"),
        goldw=0.78, cuw=0.68,
        pop=dict(thio=4, o2=8, au=7, cu1=8, cu2=6, tet=9),
    ),
    dict(
        key="exhaustion", stage="EXHAUSTION", pump=True, tint=None, halt=True,
        headline="THE LEACH STOPS WHEN THIOSULFATE RUNS OUT",
        category="EXHAUSTION", cat_colour=MUTED,
        equation=None,
        note="Oxygen still enters. Copper still cycles. Neither can leach"
             " gold without thiosulfate.",
        outcomes=[
            ("WITHOUT THIOSULFATE, NO MORE GOLD CAN DISSOLVE", GOLD),
            ("THE LEACHANT IS EXHAUSTED BEFORE THE GOLD IS RECOVERED", TEAL),
            ("OXYGEN, COPPER AND TETRATHIONATE ALL REMAIN", MUTED),
        ],
        dur=8.5, gauge=0.00,
        au=(0.285, "STOPPED"), cu2=(0.70, "STILL RISING"),
        tet=(1.00, "AT ITS MAXIMUM"),
        goldw=0.715, cuw=0.62,
        pop=dict(thio=0, o2=8, au=8, cu1=8, cu2=8, tet=11),
    ),
]

STAGES = ["START", "GOLD", "COPPER", "Cu(II)", "Cu(II) PATHS",
          "PARASITIC", "COMPETITION", "EXHAUSTION"]

# true split of the charge, MASTER.md lines 745-750
SINKS = [("GOLD", 0.0006, GOLD, "a trace"),
         ("COPPER METAL", 0.017, COPPER, "a small share"),
         ("PARASITIC Cu(II) REACTION", 0.982, VIOLET, "nearly all of it")]

TOTAL = sum(s["dur"] for s in SCENES)

# ---------------------------------------------------------------- layouts


def desktop():
    return dict(
        name="", w=1600, h=900,
        head_x=56, head_y=74, head_size=38, head_wrap=64,
        rule_y=100,
        pump=(252, 120, 356, 76), pump_size=17,
        pipe_x=430, pipe_w=20, pipe_top=196,
        vessel=(210, 262, 440, 386),
        grid=(234, 312, 626, 566), frag_y=586, frag_h=46, frag_n=5,
        panel_x=700, panel_w=856,
        cat_y=196, cat_size=23,
        eq_y=222, eq_h=78, eq_size=25, eq_wrap=70,
        out_y=356, out_lh=28, out_gap=14, out_size=22, out_wrap=62,
        ind_y=508, ind_dy=52, ind_size=19,
        ind_bar_x=1040, ind_bar_w=280, ind_word_x=1556,
        loop=(1356, 336, 96), loop_panel=0.62,
        gauge=(56, 684, 1488, 30), gauge_lab_y=674, gauge_size=19,
        strip_y=744, strip_h=18, strip_lab_y=736, strip_size=14,
        strip_left="GOLD AND COPPER METAL: A SLIVER BETWEEN THEM",
        strip_right="PARASITIC Cu(II) REACTION: NEARLY ALL OF IT",
        stage_y=822, stage_size=14, stage_names=True,
        tick_y=834, tick_h=6,
        ctl=(56, 854, 32), ctl_size=15,
        species_size=17,
    )


def mobile():
    return dict(
        name="-mobile", w=430, h=960,
        head_x=24, head_y=34, head_size=19, head_wrap=32,
        rule_y=None,
        pump=(132, 96, 166, 38), pump_size=10,
        pipe_x=215, pipe_w=12, pipe_top=134,
        vessel=(24, 164, 382, 240),
        grid=(38, 188, 392, 332), frag_y=352, frag_h=30, frag_n=4,
        panel_x=24, panel_w=382,
        cat_y=434, cat_size=13,
        eq_y=446, eq_h=54, eq_size=14, eq_wrap=34,
        out_y=546, out_lh=15, out_gap=9, out_size=12, out_wrap=44,
        ind_y=690, ind_dy=30, ind_size=12,
        ind_bar_x=186, ind_bar_w=104, ind_word_x=406,
        loop=None, loop_panel=1.0,
        gauge=(24, 794, 382, 18), gauge_lab_y=786, gauge_size=12,
        strip_y=838, strip_h=12, strip_lab_y=830, strip_size=9,
        strip_left="GOLD + COPPER: A SLIVER",
        strip_right="PARASITIC: NEARLY ALL",
        stage_y=894, stage_size=12, stage_names=False,
        tick_y=902, tick_h=5,
        ctl=(24, 918, 28), ctl_size=11,
        species_size=11,
    )


# ---------------------------------------------------------------- helpers


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def wrap(text, width):
    """Break a headline on spaces, never mid-word."""
    lines, line = [], ""
    for word in text.split(" "):
        trial = (line + " " + word).strip()
        if len(trial) > width and line:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    return lines


def split_eq(text, width):
    """Break an equation after an arrow or a wide space, never inside a term."""
    if len(text) <= width:
        return [text]
    for mark in ("  ", " → "):
        if mark in text:
            head, _, tail = text.partition(mark)
            if mark.strip():
                return [head + " →", tail]
            return [head, tail]
    return wrap(text, width)


def pool(lay):
    """Deterministic particle sites, one spatial band per species.

    Bands keep each species together so a single large label can name it,
    and the site of a given particle never moves between scenes, so the
    liquid reads as one evolving population rather than a reshuffle.
    """
    x0, y0, x1, y1 = lay["grid"]
    cols, rows = 13, 7
    cw, ch = (x1 - x0) / cols, (y1 - y0) / rows

    def site(c, r):
        # a fixed woven offset, so the grid never looks like a grid
        jx = ((c * 7 + r * 3) % 5 - 2) * cw * 0.16
        jy = ((c * 5 + r * 11) % 5 - 2) * ch * 0.16
        return (round(x0 + (c + 0.5) * cw + jx, 1),
                round(y0 + (r + 0.5) * ch + jy, 1))

    bands = {
        "o2": [(c, 0) for c in range(13)],
        "cu1": [(c, r) for r in (2, 3, 4) for c in (0, 1, 2)],
        "cu2": [(c, r) for r in (2, 3, 4) for c in (5, 6, 7)],
        "au": [(c, r) for r in (2, 3, 4) for c in (10, 11, 12)],
        "tet": [(c, r) for r in (5, 6) for c in (8, 9, 10, 11, 12)],
    }
    taken = {cell for cells in bands.values() for cell in cells}
    rest = [(c, r) for r in range(rows) for c in range(cols)
            if (c, r) not in taken]
    # Thiosulfate is the solvent, so it has to read as filling the whole
    # liquid at every population. Walking the free cells with a stride
    # coprime to their count spreads any prefix of the list over the field
    # instead of filling it row by row, and it stays reproducible.
    stride = 17 if len(rest) % 17 else 19
    bands["thio"] = [rest[(i * stride) % len(rest)] for i in range(len(rest))]
    return {k: [site(c, r) for c, r in v] for k, v in bands.items()}


def stops_for(index):
    """Opacity keyframe stops that hold scene `index` visible in its window."""
    start = sum(s["dur"] for s in SCENES[:index])
    a = start / TOTAL * 100.0
    b = (start + SCENES[index]["dur"]) / TOTAL * 100.0
    out = []
    if a <= 0.01:
        out.append((0.0, 1))
    else:
        out += [(0.0, 0), (max(a - FADE, 0.01), 0), (a + FADE, 1)]
    out.append((max(b - FADE, a + FADE + 0.01), 1))
    if b + FADE >= 99.99:
        out.append((100.0, 1))
    else:
        out += [(min(b + FADE, 100.0), 0), (100.0, 0)]
    return out


# ---------------------------------------------------------------- styles


def css(lay):
    a = []
    add = a.append
    add("svg{font-family:Inter,'Segoe UI',system-ui,sans-serif;"
        "background:%s}" % PAPER)
    add("text{fill:%s}" % INK)
    add(".mut{fill:%s}" % MUTED)

    # --- scene cycling, the no-script path -------------------------------
    for i, sc in enumerate(SCENES):
        frames = " ".join("%.3f%%{opacity:%d}" % (p, v) for p, v in stops_for(i))
        add("@keyframes kf%d{%s}" % (i, frames))
        add(".sc%d{opacity:0;animation:kf%d %.1fs linear infinite}"
            % (i, i, TOTAL))

    # --- scene switching, the scripted path ------------------------------
    # No transition on the scene swap. A CSS transition cannot advance
    # while the document is throttled or hidden, and a stuck transition
    # pins opacity at the old value, so the figure would freeze between
    # two scenes. Straight from the cascade, the swap is always correct.
    add("svg.js .scene{animation:none;opacity:0}")
    for i in range(len(SCENES)):
        add('svg.js[data-scene="%d"] .sc%d{opacity:1}' % (i, i))

    # --- motion ----------------------------------------------------------
    add("@keyframes drop{0%{transform:translateY(-76px);opacity:0}"
        "12%{opacity:1}88%{opacity:1}"
        "100%{transform:translateY(4px);opacity:0}}")
    add(".drop{animation:drop 1.7s linear infinite}")
    add("@keyframes breathe{0%,100%{transform:scale(1)}"
        "50%{transform:scale(1.16)}}")
    add(".breathe{transform-box:fill-box;transform-origin:center;"
        "animation:breathe 2.2s ease-in-out infinite}")
    add("@keyframes pulse{0%,100%{opacity:.30}50%{opacity:.75}}")
    add(".pulse{animation:pulse 1.7s ease-in-out infinite}")
    add("@keyframes orbit{0%{offset-distance:0%}100%{offset-distance:100%}}")
    add(".orbit{animation:orbit 4.2s linear infinite}")
    add("@keyframes bar{from{transform:scaleX(0)}to{transform:scaleX(1)}}")
    add(".grow{transform-box:fill-box;transform-origin:left center;"
        "animation:bar .7s ease-out both}")

    # --- controls --------------------------------------------------------
    add(".ctl{cursor:pointer}")
    add(".ctl rect{fill:#fff;stroke:%s}" % RULE)
    add(".ctl:hover rect{fill:%s}" % PANEL)
    add(".ctl text{fill:%s;font-weight:600;letter-spacing:.06em}" % INK)
    add(".ctlbar{display:none}")
    add("svg.js .ctlbar{display:block}")
    add("svg.noeq .eqbox{display:none}")
    add("svg.paused *{animation-play-state:paused!important}")

    # --- reduced motion: freeze, keep every label ------------------------
    add("@media(prefers-reduced-motion:reduce){"
        ".scene{animation:none}.sc0{opacity:1}"
        ".drop,.breathe,.pulse,.orbit,.grow{animation:none}"
        ".pulse{opacity:.55}.grow{transform:scaleX(1)}}")
    return "".join(a)


# ---------------------------------------------------------------- pieces


def species(x, y, kind, r):
    """One dissolved particle. Tetrathionate is drawn as a joined pair."""
    if kind == "thio":
        return ('<circle cx="%s" cy="%s" r="%.1f" fill="%s" opacity=".92"/>'
                % (x, y, r, TEAL))
    if kind == "o2":
        return ('<circle cx="%s" cy="%s" r="%.1f" fill="none" stroke="%s"'
                ' stroke-width="2.4"/>' % (x, y, r * 0.92, OXY))
    if kind == "au":
        return ('<circle cx="%s" cy="%s" r="%.1f" fill="%s"/>'
                '<circle cx="%s" cy="%s" r="%.1f" fill="none" stroke="%s"'
                ' stroke-width="1.6" opacity=".55"/>'
                % (x, y, r * 0.72, GOLD, x, y, r * 1.22, TEAL))
    if kind == "cu1":
        return ('<circle cx="%s" cy="%s" r="%.1f" fill="%s"/>'
                % (x, y, r, CU1))
    if kind == "cu2":
        return ('<circle cx="%s" cy="%s" r="%.1f" fill="%s"/>'
                '<circle cx="%s" cy="%s" r="%.1f" fill="none" stroke="%s"'
                ' stroke-width="1.5"/>'
                % (x, y, r * 0.82, CU2, x, y, r * 1.3, CU2))
    # tetrathionate: two thiosulfates welded together
    return ('<g><circle cx="%.1f" cy="%s" r="%.1f" fill="%s"/>'
            '<circle cx="%.1f" cy="%s" r="%.1f" fill="%s"/></g>'
            % (x - r * 0.52, y, r * 0.96, VIOLET,
               x + r * 0.52, y, r * 0.96, VIOLET))


def fragment(x, y, w, h, goldw, cuw, dead):
    """One crushed board piece: thin gold film over bulk copper."""
    sh = max(h * cuw, h * 0.42)
    top = y + h - sh
    body = DEAD if dead else BOARD
    cu = DEAD if dead else COPPER
    au = DEAD if dead else GOLD
    out = ['<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3"'
           ' fill="%s"/>' % (x, top, w, sh, body)]
    # the copper bulk, most of the piece
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2"'
               ' fill="%s" opacity=".85"/>'
               % (x + w * 0.10, top + sh * 0.34, w * 0.80, sh * 0.50, cu))
    # the gold film, a thin plated strip that only ever thins
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="1.5"'
               ' fill="%s"/>'
               % (x + w * 0.10, top + sh * 0.13, w * 0.80 * goldw,
                  max(sh * 0.14, 3.0), au))
    return "".join(out)


def bar(x, y, w, h, frac, colour, back=RULE, grow=False):
    cls = ' class="grow"' if grow else ""
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%.1f" fill="%s"/>'
            '<rect%s x="%s" y="%s" width="%.1f" height="%s" rx="%.1f"'
            ' fill="%s"/>'
            % (x, y, w, h, h / 2, back,
               cls, x, y, max(w * frac, 0.0), h, h / 2, colour))


def label(x, y, text, size, colour=INK, anchor="start", weight=600, ls=".07em"):
    return ('<text x="%s" y="%s" font-size="%s" font-weight="%s"'
            ' letter-spacing="%s" text-anchor="%s" style="fill:%s">%s</text>'
            % (x, y, size, weight, ls, anchor, colour, esc(text)))


def chip(x, y, text, size, colour):
    """A label with a paper backing, so it stays readable over particles."""
    w = len(text) * size * 0.62 + 14
    return ('<g><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3"'
            ' fill="%s" opacity=".88"/>%s</g>'
            % (x - 7, y - size * 0.92, w, size * 1.3, PAPER,
               label(x, y, text, size, colour, ls=".09em")))


# ---------------------------------------------------------------- panels


def loop_diagram(lay):
    """The copper cycle: the same atom round and round, the leachant spent."""
    cx, cy, r = lay["loop"]
    s = lay["cat_size"]
    # The travelling atom sits in a group already translated to the centre and
    # its offset-path is written about the origin. A renderer without
    # offset-path support then parks it at the centre of the loop rather than
    # in the top-left corner of the canvas.
    path = "M0 %d A%d %d 0 1 1 -0.1 %d" % (-r, r, r, -r)
    out = ['<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s"'
           ' stroke-width="3" stroke-dasharray="7 6"/>' % (cx, cy, r, CU2)]
    out.append('<g transform="translate(%d,%d)">'
               '<g class="orbit" style="offset-path:path(\'%s\')">'
               '<circle r="%.1f" fill="%s"/></g></g>'
               % (cx, cy, path, s * 0.5, CU2))
    out.append(label(cx, cy - r - 12, "Cu(II)", s, CU2, "middle"))
    out.append(label(cx, cy + r + s + 6, "Cu(I)", s, CU1, "middle"))
    out.append(label(cx - r - 12, cy + 4, "+ O₂", s * 0.86, OXY, "end"))
    out.append(label(cx + r + 12, cy - 6, "+ S₂O₃²⁻",
                     s * 0.86, TEAL))
    out.append(label(cx + r + 12, cy + s * 0.95,
                     "→ S₄O₆²⁻",
                     s * 0.86, VIOLET))
    return "".join(out)


def panel(lay, sc):
    """Category, equation, outcome labels and the three readouts.

    The loop scene puts the copper cycle in the right half and narrows
    everything else to the left half, so nothing is ever drawn over the text.
    """
    px, pw = lay["panel_x"], lay["panel_w"]
    loop = bool(sc.get("loop")) and lay["loop"] is not None
    text_w = pw * lay["loop_panel"] if loop else pw
    wrap_at = int(lay["out_wrap"] * lay["loop_panel"]) if loop else lay["out_wrap"]

    out = [label(px, lay["cat_y"], sc["category"], lay["cat_size"],
                 sc["cat_colour"], ls=".14em")]
    if loop:
        out.append(loop_diagram(lay))

    if sc["equation"]:
        lines = split_eq(sc["equation"], int(lay["eq_wrap"] * (
            lay["loop_panel"] if loop else 1.0)))
        h = lay["eq_h"]
        if len(lines) > 1:
            h += lay["eq_size"] * 1.25 * (len(lines) - 1)
        out.append('<g class="eqbox">')
        out.append('<rect x="%s" y="%s" width="%.1f" height="%.1f" rx="4"'
                   ' fill="%s"/>' % (px, lay["eq_y"], text_w, h, PANEL))
        out.append('<rect x="%s" y="%s" width="5" height="%.1f" rx="2.5"'
                   ' fill="%s"/>'
                   % (px, lay["eq_y"], h, sc["tint"] or RULE))
        for i, ln in enumerate(lines):
            out.append(label(px + 20,
                             lay["eq_y"] + lay["eq_size"] * (1.7 + 1.25 * i),
                             ln, lay["eq_size"], INK, weight=500, ls=".01em"))
        out.append("</g>")
    elif sc.get("note"):
        size = lay["eq_size"] * 0.88
        for i, ln in enumerate(wrap(sc["note"], lay["eq_wrap"])):
            out.append(label(px + 4, lay["eq_y"] + size * (1.7 + 1.3 * i),
                             ln, size, MUTED, weight=500, ls=".05em"))

    y = lay["out_y"]
    for txt, colour in sc["outcomes"]:
        lines = wrap(txt, wrap_at)
        out.append('<circle cx="%s" cy="%.1f" r="%.1f" fill="%s"/>'
                   % (px + 6, y - lay["out_size"] * 0.32,
                      lay["out_size"] * 0.26, colour))
        for ln in lines:
            out.append(label(px + 22, y, ln, lay["out_size"],
                             MUTED if colour is MUTED else INK,
                             weight=600, ls=".03em"))
            y += lay["out_lh"]
        y += lay["out_gap"]

    rows = [("DISSOLVED GOLD", sc["au"], GOLD),
            ("Cu(II) IN SOLUTION", sc["cu2"], CU2),
            ("TETRATHIONATE", sc["tet"], VIOLET)]
    for i, (name, (frac, word), colour) in enumerate(rows):
        y = lay["ind_y"] + i * lay["ind_dy"]
        s = lay["ind_size"]
        out.append(label(px, y, name, s, MUTED, weight=600, ls=".1em"))
        out.append(bar(lay["ind_bar_x"], y - s * 0.78, lay["ind_bar_w"],
                       s * 0.95, frac, colour, grow=True))
        # right-aligned, so a long readout word can never run off the edge
        out.append(label(lay["ind_word_x"], y, word, s * 0.92, colour,
                         "end", weight=700, ls=".06em"))
    return "".join(out)


def vessel_contents(lay, sc, sites):
    """The liquid: particles, species labels, and the board fragments.

    Nothing greys out at exhaustion. Every species that is still in the
    vessel when the leach halts really is still there, and the gold left on
    the board is the whole point of the last scene, so it keeps its colour.
    """
    vx, vy, vw, vh = lay["vessel"]
    r = lay["species_size"] * 0.42
    dead = False
    out = []

    # oxygen falling down the pipe, only while the pump runs
    if sc["pump"] and not dead:
        for i in range(4):
            out.append('<circle class="drop" cx="%s" cy="%s" r="%.1f"'
                       ' fill="none" stroke="%s" stroke-width="2.4"'
                       ' style="animation-delay:%.2fs"/>'
                       % (lay["pipe_x"], vy + 14, r * 0.9, OXY, i * 0.42))

    order = ["thio", "o2", "cu1", "cu2", "au", "tet"]
    for kind in order:
        n = sc["pop"].get(kind, 0)
        for j, (x, y) in enumerate(sites[kind][:n]):
            g = species(x, y, kind, r)
            if not dead and kind in ("o2", "cu2"):
                g = '<g class="breathe" style="animation-delay:%.2fs">%s</g>' \
                    % (j * 0.27, g)
            out.append(g)

    # the board, thinning as the run goes on
    n = lay["frag_n"]
    span = vw - 56
    fw = span / (n + (n - 1) * 0.28)
    for i in range(n):
        fx = vx + 28 + i * fw * 1.28
        out.append(fragment(fx, lay["frag_y"], fw, lay["frag_h"],
                            sc["goldw"], sc["cuw"], dead))

    # one large label per species band, added only when the species is present
    gx0, gy0, gx1, gy1 = lay["grid"]
    s = lay["species_size"]
    bandtop = gy0 + (gy1 - gy0) * 2 / 7
    names = [
        ("thio", gx0, gy0 - 6, "THIOSULFATE", TEAL, "start"),
        ("o2", gx1, gy0 - 6, "OXYGEN", OXY, "end"),
        ("cu1", gx0, bandtop - 5, "Cu(I)", CU1, "start"),
        ("cu2", (gx0 + gx1) / 2, bandtop - 5, "Cu(II)", CU2, "middle"),
        ("au", gx1, bandtop - 5, "DISSOLVED GOLD", GOLD, "end"),
        ("tet", gx1, gy0 + (gy1 - gy0) * 5 / 7 - 5, "TETRATHIONATE",
         VIOLET, "end"),
    ]
    for kind, x, y, text, colour, anchor in names:
        if sc["pop"].get(kind, 0) <= 0:
            continue
        w = len(text) * s * 0.62 + 14
        bx = x - 7 if anchor == "start" else (
            x - w + 7 if anchor == "end" else x - w / 2)
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3"'
                   ' fill="%s" opacity=".86"/>'
                   % (bx, y - s * 0.92, w, s * 1.3, PAPER))
        out.append(label(x, y, text, s, DEAD if dead else colour, anchor,
                         ls=".09em"))

    # At the halt the caption changes rather than moving, which is the one
    # place the figure can say the run ended with gold still unrecovered.
    if sc.get("halt"):
        caption, ccol = "GOLD STILL ON THE BOARD", GOLD
    else:
        caption, ccol = "CRUSHED PCB — THIN GOLD OVER BULK COPPER", MUTED
    out.append(label(vx + vw / 2, lay["frag_y"] - 10, caption,
                     s * 0.88, ccol, "middle", weight=700, ls=".09em"))
    return "".join(out)


def gauge_block(lay, sc):
    """Thiosulfate remaining, and where the charge actually went."""
    gx, gy, gw, gh = lay["gauge"]
    s = lay["gauge_size"]
    out = [label(gx, lay["gauge_lab_y"], "THIOSULFATE AVAILABLE", s, MUTED,
                 weight=700, ls=".14em")]
    frac = sc["gauge"]
    out.append('<rect x="%s" y="%s" width="%s" height="%s" rx="%.1f"'
               ' fill="%s"/>' % (gx, gy, gw, gh, gh / 2, RULE))
    if frac > 0:
        out.append('<rect x="%s" y="%s" width="%.1f" height="%s" rx="%.1f"'
                   ' fill="%s"/>' % (gx, gy, gw * frac, gh, gh / 2, TEAL))
    else:
        out.append(label(gx + 16, gy + gh * 0.74, "EMPTY — THE LEACH HAS"
                         " STOPPED", s * 0.82, MUTED, weight=700, ls=".18em"))

    # The honest split, drawn to scale. Gold is a hairline because it is one:
    # 0.06 % of the charge against 98.2 % for the parasitic reaction.
    sy, sh = lay["strip_y"], lay["strip_h"]
    out.append(label(gx, lay["strip_lab_y"], "WHERE THE CHARGE GOES",
                     lay["strip_size"], MUTED, weight=700, ls=".14em"))
    cur = gx
    for name, share, colour, word in SINKS:
        w = gw * share
        out.append('<rect x="%.2f" y="%s" width="%.2f" height="%s"'
                   ' fill="%s"/>' % (cur, sy, max(w, 2.0), sh, colour))
        cur += w
    cy = sy + sh + lay["strip_size"] * 1.6
    out.append(label(gx, cy, lay["strip_left"], lay["strip_size"], COPPER,
                     weight=700, ls=".08em"))
    out.append(label(gx + gw, cy, lay["strip_right"], lay["strip_size"],
                     VIOLET, "end", weight=700, ls=".08em"))
    return "".join(out)


def progress(lay, index):
    """Named stages, then a tick per scene, so position is never in doubt."""
    gx, _, gw, _ = lay["gauge"]
    s = lay["stage_size"]
    out = []
    active = SCENES[index]["stage"]
    if lay["stage_names"]:
        step = gw / len(STAGES)
        for i, name in enumerate(STAGES):
            on = name == active
            out.append(label(gx + step * (i + 0.5), lay["stage_y"], name, s,
                             INK if on else "#a8a8a2", "middle",
                             weight=700 if on else 600, ls=".1em"))
    else:
        # Eight stage names will not fit across a phone, so the narrow layout
        # names only the stage the reader is in and lets the ticks do the rest.
        out.append(label(gx + gw / 2, lay["stage_y"], active, s, INK,
                         "middle", weight=700, ls=".12em"))
    n = len(SCENES)
    tw = gw / n
    for i in range(n):
        done = i <= index
        out.append('<rect x="%.1f" y="%s" width="%.1f" height="%s" rx="%.1f"'
                   ' fill="%s"/>'
                   % (gx + i * tw + 2, lay["tick_y"], tw - 4, lay["tick_h"],
                      lay["tick_h"] / 2, INK if done else RULE))
    return "".join(out)


def controls(lay):
    """Only ever shown when scripting is available to drive them."""
    x, y, h = lay["ctl"]
    s = lay["ctl_size"]
    items = [("bPrev", "PREVIOUS", 118), ("bPlay", "PAUSE", 96),
             ("bNext", "NEXT", 86), ("bReset", "RESTART", 108),
             ("bEq", "EQUATIONS", 124)]
    if lay["w"] < 600:
        items = [("bPrev", "PREV", 66), ("bPlay", "PAUSE", 70),
                 ("bNext", "NEXT", 64), ("bReset", "RESET", 68),
                 ("bEq", "EQN", 56)]
    out = ['<g class="ctlbar">']
    cur = x
    for ident, text, w in items:
        out.append('<g class="ctl" id="%s" role="button" tabindex="0">'
                   '<rect x="%.1f" y="%s" width="%s" height="%s" rx="4"/>'
                   '<text x="%.1f" y="%.1f" font-size="%s" text-anchor="middle"'
                   '>%s</text></g>'
                   % (ident, cur, y, w, h, cur + w / 2, y + h * 0.66, s, text))
        cur += w + 10
    out.append("</g>")
    return "".join(out)


# ---------------------------------------------------------------- script

SCRIPT = """
(function(){
  var svg=document.documentElement, n=%d, dur=%s, i=0, playing=true, t=null;
  var reduce=window.matchMedia&&
    window.matchMedia('(prefers-reduced-motion:reduce)').matches;
  svg.classList.add('js');
  function show(k){
    i=(k+n)%%n; svg.setAttribute('data-scene',i);
    var b=svg.getElementById('bPlay');
    if(b)b.querySelector('text').textContent=playing?'PAUSE':'PLAY';
    arm();
  }
  function arm(){
    if(t)clearTimeout(t); t=null;
    if(playing&&!reduce)t=setTimeout(function(){show(i+1);},dur[i]*1000);
  }
  function setPlay(p){
    playing=p; svg.classList.toggle('paused',!p);
    var b=svg.getElementById('bPlay');
    if(b)b.querySelector('text').textContent=p?'PAUSE':'PLAY';
    arm();
  }
  function on(id,fn){
    var e=svg.getElementById(id); if(!e)return;
    e.addEventListener('click',fn);
    e.addEventListener('keydown',function(ev){
      if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();fn();}
    });
  }
  on('bPrev',function(){setPlay(false);show(i-1);});
  on('bNext',function(){setPlay(false);show(i+1);});
  on('bPlay',function(){setPlay(!playing);});
  on('bReset',function(){setPlay(true);show(0);});
  on('bEq',function(){svg.classList.toggle('noeq');});
  if(reduce)playing=false;
  show(0);
})();
"""


# ---------------------------------------------------------------- render


def render(lay):
    w, h = lay["w"], lay["h"]
    sites = pool(lay)
    a = []
    add = a.append
    # Sized in per cent, not pixels, so the file fills whatever box the page
    # gives it. The viewBox still carries the intrinsic ratio, so an <img>
    # embed lays out correctly too.
    add('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"'
        ' width="100%%" height="100%%" preserveAspectRatio="xMidYMid meet"'
        ' data-scene="0" role="img" aria-label="%s">' % (w, h, esc(ALT)))
    add("<style>%s</style>" % css(lay))
    add('<rect width="%d" height="%d" fill="%s"/>' % (w, h, PAPER))

    # ---- fixed furniture: the vessel and the pump never move -------------
    vx, vy, vw, vh = lay["vessel"]
    px_, py_, pw_, ph_ = lay["pump"]
    add('<rect x="%s" y="%s" width="%s" height="%s" rx="4" fill="#fff"'
        ' stroke="%s" stroke-width="2"/>' % (px_, py_, pw_, ph_, RULE))
    add(label(px_ + pw_ / 2, py_ + ph_ * 0.42, "CONTROLLED", lay["pump_size"],
              MUTED, "middle", weight=700, ls=".16em"))
    add(label(px_ + pw_ / 2, py_ + ph_ * 0.82, "OXYGEN SUPPLY",
              lay["pump_size"], OXY, "middle", weight=700, ls=".16em"))
    add('<rect x="%.1f" y="%s" width="%s" height="%.1f" fill="%s"'
        ' opacity=".22"/>'
        % (lay["pipe_x"] - lay["pipe_w"] / 2, lay["pipe_top"], lay["pipe_w"],
           vy - lay["pipe_top"] + 4, OXY))
    add('<rect x="%s" y="%s" width="%s" height="%s" rx="8" fill="#fff"'
        ' stroke="%s" stroke-width="2"/>' % (vx, vy, vw, vh, RULE))
    add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="5"'
        ' fill="#eef5f5"/>'
        % (vx + 6, vy + 22, vw - 12, vh - 28))
    if lay["rule_y"]:
        add('<rect x="%s" y="%s" width="%s" height="1" fill="%s"/>'
            % (lay["head_x"], lay["rule_y"], w - 2 * lay["head_x"], RULE))

    # ---- one group per scene, everything that changes lives inside -------
    for i, sc in enumerate(SCENES):
        add('<g class="scene sc%d">' % i)
        if sc["tint"]:
            top = lay["cat_y"] - lay["cat_size"] * 1.8
            bottom = (lay["out_y"]
                      + len(sc["outcomes"]) * (lay["out_lh"] + lay["out_gap"]))
            add('<rect x="%s" y="%.1f" width="%s" height="%.1f" rx="6"'
                ' fill="%s" opacity=".05"/>'
                % (lay["panel_x"] - 14, top, lay["panel_w"] + 28,
                   bottom - top, sc["tint"]))
        if sc["pump"]:
            add('<rect class="pulse" x="%s" y="%s" width="%s" height="%s"'
                ' rx="4" fill="%s"/>' % (px_, py_, pw_, ph_, OXY))
        for j, line in enumerate(wrap(sc["headline"], lay["head_wrap"])):
            add(label(lay["head_x"],
                      lay["head_y"] + j * lay["head_size"] * 1.12,
                      line, lay["head_size"], INK, weight=700, ls=".012em"))
        add(vessel_contents(lay, sc, sites))
        add(panel(lay, sc))
        add(gauge_block(lay, sc))
        add(progress(lay, i))
        add("</g>")

    add(controls(lay))
    add('<script type="text/javascript"><![CDATA[%s]]></script>'
        % (SCRIPT % (len(SCENES), [s["dur"] for s in SCENES])))
    add("</svg>")
    return "".join(a)


ALT = ("A ten-scene animation of one ammonia-free leaching run. An air pump "
       "above the vessel feeds oxygen down a pipe into the liquid. Oxygen "
       "dissolves gold from the board and also dissolves copper, which enters "
       "as copper(I). Oxygen re-oxidises that to copper(II), which can help "
       "dissolve gold but mostly converts thiosulfate into tetrathionate. "
       "Copper cycles round for ever, thiosulfate does not, and the run stops "
       "when the thiosulfate is gone with most of the gold still on the board.")


def main():
    for lay in (desktop(), mobile()):
        path = OUT / ("leaching-scenes%s.svg" % lay["name"])
        path.write_text(render(lay), encoding="utf-8")
        print("wrote %s  %d bytes" % (path.name, path.stat().st_size))
    print("clock %.1f s over %d scenes" % (TOTAL, len(SCENES)))


if __name__ == "__main__":
    main()
