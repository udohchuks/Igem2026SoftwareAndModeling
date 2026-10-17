"""Build the leaching-budget figure: one canvas, one argument, a 12 s loop.

The argument, and the only thing this figure sets out to carry:

    A small pathway dissolves gold. Oxygen also regenerates Cu(II). The
    repeating Cu(I)/Cu(II) cycle converts much more thiosulfate into
    tetrathionate. Thiosulfate is exhausted, and gold dissolution stops.

This is deliberately not a complete account of the model. Three of the
model's balanced reactions are left out, and the four that are shown are
quoted verbatim from the source document "Bioleaching_Models_v5",
paragraphs 147 and 165-166, which match docs/EQUATIONS.md lines 123-150 and
docs/MASTER.md lines 570-575:

    4 Au(0) + 8 S2O3(2-) + O2 + 2 H2O ->  4 Au(S2O3)2(3-) + 4 OH(-)   gold
    Au(0) + 2 S2O3(2-) + Cu(II)       ->  Au(S2O3)2(3-) + Cu(I)       gold
    4 Cu(I) + O2 + 2 H2O              ->  4 Cu(II) + 4 OH(-)          v4
    2 Cu(II) + 2 S2O3(2-)             ->  2 Cu(I) + S4O6(2-)          v3

Both gold oxidants are shown, because the rate law adds them in parallel
(EQUATIONS.md lines 133-137). Cu(II) is therefore not purely parasitic: it
dissolves gold as well. The parasitic step alone dissolves none, and the
tetrathionate caption says only that.

Three things the geometry is answerable for.

1. Copper is never fed in. It leaves the board as Cu(0) and dissolves as
   Cu(I), and v4 is the only source of Cu(II) anywhere in the model
   (EQUATIONS.md line 208). So the copper-entry arrow runs from the board
   into Cu(I), never into Cu(II).
2. Cu(II) is a reactant of the parasitic step, not a product. The route to
   tetrathionate therefore passes through a reaction point beside Cu(II)
   and the copper returns to Cu(I); no arrow runs from the vessel straight
   to tetrathionate.
3. Re-oxidation consumes no thiosulfate (EQUATIONS.md line 180), so the
   budget bar does not move on the Cu(I) to Cu(II) leg.

The budget bar shows relative dominance and states no percentage. The
model's split is gold 0.06 %, copper metal 1.7 %, parasitic 98.2 %
(MASTER.md lines 745-750), but those hold for one scenario only, so the
figure argues the shape of the split and not its value. All three sinks are
drawn: copper metal is the second-largest one and leaving it out made the
bar read as though gold and tetrathionate were the only two.

Tetrathionate is drawn as a dead end. That is the default model: the
alkaline route that returns it to thiosulfate is off unless enabled
(EQUATIONS.md lines 196-207).

Degrades in three directions: the loop is pure CSS and runs inside an
<img>; the script only adds tab-visibility pausing and click-to-restart;
and prefers-reduced-motion renders the final, exhausted state as a still.

Writes docs/media/wiki/concepts/leaching-budget.svg.
"""
from pathlib import Path

OUT = Path(__file__).resolve().parent / "media" / "wiki" / "concepts"

W, H = 1600, 900
T = 12.0                       # master clock, seconds

# ---------------------------------------------------------------- palette

BG = "#faf8f3"                 # warm off-white
INK = "#26221d"
MUTED = "#7b756c"
FAINT = "#a9a296"
HAIR = "#e3ddd2"
ARROW = "#c7c0b4"              # soft neutral grey

TEAL = "#2d8f94"               # thiosulfate
GOLD = "#b3821f"               # gold
CU1 = "#cc8d63"                # copper(I), light terracotta
CU2 = "#9c4a2f"                # copper(II), dark rust
PURPLE = "#8a70a6"             # tetrathionate
BLUE = "#4a86b8"               # oxygen
BOARD = "#3f4a3d"              # PCB substrate
LIQUID = "#e9f2f3"

SERIF = "Iowan Old Style,Georgia,'Times New Roman',serif"
SANS = "Inter,'Segoe UI',system-ui,sans-serif"

# ---------------------------------------------------------------- geometry

VESSEL = (150, 316, 410, 372)          # x, y, w, h
PUMP = (400, 196, 180, 56)
PIPE_X, PIPE_W, PIPE_TOP = 490, 16, 252

GOLD_NODE = (1330, 314, 62)            # cx, cy, r
TET_NODE = (1370, 618, 64)
# The loop is wide so the two labels it carries clear its arcs. Cu(I) sits
# left and Cu(II) right, matching the direction of the two arrows.
CU1_NODE = (760, 630, 46)
CU2_NODE = (1090, 630, 46)
REACT = (1190, 560)                    # parasitic reaction point, beside Cu(II)

# The bar's name sits on its left rather than above it, which keeps the band
# under the copper loop free for that loop's own labels.
BAR = (380, 800, 1150, 24)
ALLOC_Y, ALLOC_H = 838, 12
ALLOC_GOLD = 0.04                      # a visibly small share; no number claimed
ALLOC_CU = 0.11                        # copper metal: larger than gold, still small
SAY_Y = 212                            # upper-centre line, the one big message

# Routes. Each is a run of cubic segments written as flat point lists:
# [start, c1, c2, p1, c3, c4, p2, ...]. Emitted twice, once absolute for the
# drawn stroke and once shifted to the origin for the travelling token, so a
# renderer without offset-path parks the token at the route start rather than
# in the corner of the canvas.
ROUTES = {
    "gold": [(566, 356), (760, 312), (1010, 292), (1268, 310)],
    "cuin": [(492, 690), (556, 744), (656, 714), (714, 664)],
    # thiosulfate reaches tetrathionate only by way of the reaction point
    # beside Cu(II); it is never drawn going there directly
    "feed": [(566, 534), (750, 456), (980, 440), (1120, 486),
             (1154, 506), (1176, 534), (1190, 560)],
    "tet": [(1190, 560), (1236, 578), (1264, 592), (1292, 600)],
    "ox": [(760, 676), (820, 718), (1030, 718), (1090, 676)],     # Cu(I)->Cu(II)
    "par": [(1090, 584), (1030, 542), (820, 542), (760, 584)],    # Cu(II)->Cu(I)
    # the pump's second job, kept outside the vessel and clear of every label
    "o2cu": [(566, 252), (604, 320), (592, 480), (600, 600),
             (612, 656), (690, 684), (752, 678)],
}


def pathd(pts, dx=0.0, dy=0.0):
    d = "M%.1f %.1f" % (pts[0][0] - dx, pts[0][1] - dy)
    for i in range(1, len(pts), 3):
        a, b, c = pts[i], pts[i + 1], pts[i + 2]
        d += "C%.1f %.1f %.1f %.1f %.1f %.1f" % (
            a[0] - dx, a[1] - dy, b[0] - dx, b[1] - dy, c[0] - dx, c[1] - dy)
    return d


def pc(t):
    """Seconds on the master clock as a keyframe percentage."""
    return max(0.0, min(100.0, t / T * 100.0))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------- text


def text(x, y, s, size, fill=INK, anchor="start", weight=400, ls="0",
         family=SANS, cls=None, extra=""):
    return ('<text x="%s" y="%s" font-family="%s" font-size="%s"'
            ' font-weight="%s" letter-spacing="%s" text-anchor="%s"'
            ' style="fill:%s"%s%s>%s</text>'
            % (x, y, family, size, weight, ls, anchor, fill,
               ' class="%s"' % cls if cls else "", extra, esc(s)))


# ---------------------------------------------------------------- styles


def css():
    a = []
    add = a.append
    add("svg{background:%s}" % BG)

    # ---- oxygen falling down the pipe, slow controlled pulses -----------
    add("@keyframes drip{0%{transform:translateY(-58px);opacity:0}"
        "18%{opacity:.9}78%{opacity:.9}"
        "100%{transform:translateY(6px);opacity:0}}")
    add(".drip{animation:drip 2.4s cubic-bezier(.4,0,.5,1) infinite}")

    # ---- ambient drift for the thiosulfate in the liquor ----------------
    add("@keyframes drift{0%,100%{transform:translate(0,0)}"
        "33%{transform:translate(3px,-4px)}"
        "66%{transform:translate(-3px,3px)}}")
    add(".drift{transform-box:fill-box;transform-origin:center;"
        "animation:drift 7s ease-in-out infinite}")

    add("@keyframes breathe{0%,100%{transform:scale(1)}"
        "50%{transform:scale(1.14)}}")
    add(".breathe{transform-box:fill-box;transform-origin:center;"
        "animation:breathe 2.6s ease-in-out infinite}")

    # ---- the budget, stepping down as each sink draws on it -------------
    steps = [(0.0, 1.00), (2.6, 1.00), (3.4, 0.97), (4.6, 0.97),
             (5.4, 0.90), (6.4, 0.90), (8.6, 0.62), (9.2, 0.62),
             (9.8, 0.40), (10.4, 0.16), (10.9, 0.02), (12.0, 0.02)]
    add("@keyframes budget{%s}" % "".join(
        "%.2f%%{transform:scaleX(%.3f)}" % (pc(t), v) for t, v in steps))
    add(".budget{transform-box:fill-box;transform-origin:left center;"
        "animation:budget %.1fs linear infinite}" % T)

    # ---- phase visibility ------------------------------------------------
    # Each label, equation and glow is on the master clock, so the whole
    # composition stays in step without any scripting.
    def phase(name, t0, t1, fade=0.22, peak=1.0):
        s = [(0.0, 0)]
        if t0 > 0.02:
            s.append((pc(t0), 0))
        s += [(pc(t0 + fade), peak), (pc(t1 - fade), peak)]
        if t1 < T - 0.02:
            s += [(pc(t1), 0), (100.0, 0)]
        else:
            s.append((100.0, peak))
        add("@keyframes %s{%s}" % (name, "".join(
            "%.2f%%{opacity:%.2f}" % (p, v) for p, v in s)))
        add(".%s{opacity:0;animation:%s %.1fs linear infinite}"
            % (name, name, T))

    phase("phGold", 2.0, 4.3)
    phase("phOx", 4.5, 6.2)
    phase("phPar", 6.1, 10.5)
    phase("phCycle", 6.4, 10.5)
    phase("phEnd", 10.6, 12.0)
    phase("phGoldGlow", 2.1, 4.1, peak=0.95)
    phase("phOxGlow", 4.8, 6.1, peak=0.95)
    phase("phParGlow", 6.4, 10.4, peak=0.95)

    # the desired route slows and fades as the leachant thins out
    add("@keyframes wane{0%%,%.2f%%{opacity:1}%.2f%%{opacity:.28}"
        "100%%{opacity:.28}}" % (pc(9.0), pc(10.6)))
    add(".wane{animation:wane %.1fs linear infinite}" % T)

    # gold still on the board once the run halts
    add("@keyframes hold{0%%,%.2f%%{opacity:0}%.2f%%{opacity:1}"
        "100%%{opacity:1}}" % (pc(10.4), pc(10.9)))
    add(".hold{opacity:0;animation:hold %.1fs linear infinite}" % T)

    add(".paused *,.paused{animation-play-state:paused!important}")

    # ---- reduced motion: the exhausted state, held still ----------------
    # The still is the end of the run, so it carries the conclusion and not
    # the mechanism line: the two share one line of the canvas and must
    # never both be on.
    add("@media(prefers-reduced-motion:reduce){"
        "*{animation:none!important}"
        ".budget{transform:scaleX(.02)}"
        ".tok,.drip,.phGold,.phOx,.phGoldGlow,.phOxGlow,.phCycle"
        "{opacity:0}"
        ".phPar,.phParGlow{opacity:1}"
        ".phEnd,.hold{opacity:1}"
        ".wane{opacity:.28}}")
    return "".join(a)


def travel(name, route, t0, t1, ease="cubic-bezier(.45,0,.55,1)"):
    """A token riding one route between two moments on the master clock."""
    f = 0.16
    s = [(0.0, 0, 0.0)]
    if t0 > 0.02:
        s.append((pc(t0), 0, 0.0))
    s += [(pc(t0 + f), 1, 100.0 * f / (t1 - t0)),
          (pc(t1 - f), 1, 100.0 * (1 - f / (t1 - t0))),
          (pc(t1), 0, 100.0), (100.0, 0, 100.0)]
    frames = "".join("%.2f%%{opacity:%d;offset-distance:%.1f%%}" % k for k in s)
    rule = ("@keyframes %s{%s}"
            ".%s{offset-path:path('%s');offset-rotate:0deg;"
            "animation:%s %.1fs %s infinite}"
            % (name, frames, name,
               pathd(ROUTES[route], *ROUTES[route][0]), name, T, ease))
    return rule


def token_at(route, cls, body):
    """Wrap a travelling token at its route start.

    offset-path composes with the transform, so the group's translate puts
    the origin-relative path in the right place. Without offset-path support
    the token simply rests at the start of its route.
    """
    x, y = ROUTES[route][0]
    return '<g transform="translate(%.1f,%.1f)"><g class="tok %s">%s</g></g>' \
        % (x, y, cls, body)


# ---------------------------------------------------------------- pieces


def arrowhead(ident, colour, size=13):
    return ('<marker id="%s" viewBox="0 0 12 12" refX="9.6" refY="6"'
            ' markerWidth="%d" markerHeight="%d" markerUnits="userSpaceOnUse"'
            ' orient="auto"><path d="M1 1L11 6L1 11Z" fill="%s"/></marker>'
            % (ident, size, size, colour))


def route(route_key, stroke, width, marker, cls="", dash=None):
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%s"'
            ' stroke-linecap="round" marker-end="url(#%s)"%s%s/>'
            % (pathd(ROUTES[route_key]), stroke, width, marker,
               ' class="%s"' % cls if cls else "",
               ' stroke-dasharray="%s"' % dash if dash else ""))


def node(cx, cy, r, fill, ring, label, lsize, lcolour, cls=""):
    return ('<g%s><circle cx="%d" cy="%d" r="%d" fill="%s"/>'
            '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s"'
            ' stroke-width="2"/>%s</g>'
            % (' class="%s"' % cls if cls else "", cx, cy, r, fill,
               cx, cy, r, ring,
               text(cx, cy + lsize * 0.35, label, lsize, lcolour, "middle",
                    weight=600)))


def fragment(x, y, w, h, gold_frac, gold_cls=""):
    """One crushed board piece: a thick copper body under a hairline of gold."""
    out = ['<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3"'
           ' fill="%s"/>' % (x, y, w, h, BOARD)]
    # the copper bulk, most of the piece by area
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2"'
               ' fill="#9a6040"/>'
               % (x + w * 0.08, y + h * 0.30, w * 0.84, h * 0.56))
    # the gold plating, a hairline by comparison
    out.append('<rect%s x="%.1f" y="%.1f" width="%.1f" height="4" rx="2"'
               ' fill="%s"/>'
               % (' class="%s"' % gold_cls if gold_cls else "",
                  x + w * 0.08, y + h * 0.14, w * 0.84 * gold_frac, GOLD))
    return "".join(out)


# ---------------------------------------------------------------- render


def render():
    vx, vy, vw, vh = VESSEL
    px, py, pw, ph = PUMP
    gx, gy, gr = GOLD_NODE
    tx, ty, tr = TET_NODE
    c1x, c1y, c1r = CU1_NODE
    c2x, c2y, c2r = CU2_NODE
    rx, ry = REACT
    bx, by, bw, bh = BAR

    a = []
    add = a.append
    add('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"'
        ' width="100%%" height="100%%" preserveAspectRatio="xMidYMid meet"'
        ' role="img" aria-labelledby="figTitle figDesc">' % (W, H))
    add('<title id="figTitle">%s</title>' % esc(TITLE))
    add('<desc id="figDesc">%s</desc>' % esc(DESC))

    add("<defs>")
    for ident, colour in (("aGrey", ARROW), ("aGold", GOLD), ("aCu", CU1),
                          ("aPur", PURPLE), ("aBlue", BLUE)):
        add(arrowhead(ident, colour))
    add("</defs>")
    add("<style>%s</style>" % css())
    for name, rt, t0, t1 in TRAVELS:
        add("<style>%s</style>" % travel(name, rt, t0, t1))
    # painted, not a CSS background: a root background only paints in a
    # browser, and the file is also read by static renderers
    add('<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG))

    # ---------------------------------------------------------- title ----
    add('<g id="title">')
    add(text(70, 74, "INSIDE THE LEACHING VESSEL", 15, MUTED,
             weight=700, ls=".22em"))
    add(text(70, 126, TITLE, 46, INK, family=SERIF, weight=400, ls="-.005em"))
    add('<rect x="70" y="154" width="470" height="1" fill="%s"/>' % HAIR)
    add("</g>")

    # ------------------------------------------------ oxygen supply ------
    add('<g id="oxygen-supply">')
    add('<rect x="%d" y="%d" width="%d" height="%d" rx="7" fill="#fff"'
        ' stroke="%s" stroke-width="1.5"/>' % (px, py, pw, ph, HAIR))
    add(text(px + pw / 2, py + ph * 0.62, "CONTROLLED OXYGEN", 17, BLUE,
             "middle", weight=700, ls=".1em"))
    add('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" opacity=".18"'
        ' rx="3"/>' % (PIPE_X - PIPE_W / 2, PIPE_TOP, PIPE_W,
                       vy - PIPE_TOP + 6, BLUE))
    for i in range(3):
        add('<circle class="drip" cx="%d" cy="%d" r="6" fill="none"'
            ' stroke="%s" stroke-width="2.4"'
            ' style="animation-delay:%.2fs"/>'
            % (PIPE_X, vy + 16, BLUE, i * 0.8))
    add("</g>")

    # the pump's second job, drawn as a quiet dotted line to the copper leg
    add('<path id="oxygen-to-copper" d="%s" fill="none" stroke="%s"'
        ' stroke-width="2" stroke-dasharray="2 9" stroke-linecap="round"'
        ' opacity=".38"/>' % (pathd(ROUTES["o2cu"]), BLUE))

    # ----------------------------------------------------- vessel --------
    add('<g id="vessel">')
    add(text(vx, 302, "THIOSULFATE · CONTROLLED OXYGEN", 18, MUTED,
             weight=700, ls=".12em"))
    add('<rect x="%d" y="%d" width="%d" height="%d" rx="16" fill="#fff"'
        ' stroke="%s" stroke-width="1.5"/>' % (vx, vy, vw, vh, HAIR))
    add('<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="%s"/>'
        % (vx + 8, vy + 30, vw - 16, vh - 38, LIQUID))

    # thiosulfate in the liquor, spaced to stay calm rather than crowded
    sites = [(214, 382), (298, 366), (380, 392), (462, 372), (524, 404),
             (196, 448), (270, 432), (352, 454), (436, 438), (508, 466),
             (232, 512), (316, 498), (404, 520), (486, 504)]
    for i, (sx, sy) in enumerate(sites):
        add('<circle class="drift" cx="%d" cy="%d" r="8" fill="%s"'
            ' opacity=".85" style="animation-delay:%.2fs"/>'
            % (sx, sy, TEAL, (i % 5) * 1.3))
    add(text(vx + 18, 356, "S₂O₃²⁻", 17, TEAL,
             weight=600))

    # dissolved oxygen, a few only
    for i, (sx, sy) in enumerate([(466, 344), (418, 336), (500, 372)]):
        add('<circle class="breathe" cx="%d" cy="%d" r="7" fill="none"'
            ' stroke="%s" stroke-width="2.2" style="animation-delay:%.1fs"/>'
            % (sx, sy, BLUE, i * 0.7))

    # the board: four pieces, thick copper under a hairline of gold
    for i in range(4):
        fx = vx + 30 + i * 92
        add(fragment(fx, 596, 74, 52, 1.0 if i != 1 else 0.62,
                     gold_cls="wane" if i == 1 else ""))
    add("</g>")
    add(text(vx + vw / 2, 712, "Crushed PCB fragments", 19, MUTED, "middle"))
    add(text(vx + vw / 2, 740, "Gold remains on the board", 19, GOLD,
             "middle", weight=600, cls="hold"))

    # the atom that leaves, highlighted just before it goes
    add('<circle class="phGold" cx="322" cy="602" r="9" fill="%s"/>' % GOLD)

    # ----------------------------------------------- desired pathway -----
    # Labels stack clear of the arrow: name above it, then the arrow, then
    # the plain-language line, then the equation that only appears in phase.
    add('<g id="desired-pathway">')
    add(route("gold", ARROW, 2.6, "aGrey", cls="wane"))
    add(route("gold", GOLD, 3.4, "aGold", cls="phGoldGlow"))
    add(text(800, 272, "DESIRED REACTION", 27, INK, "middle", weight=700,
             ls=".1em"))
    add(text(800, 348, "Oxygen and copper(II) both dissolve gold", 20, MUTED,
             "middle"))
    add(text(800, 372, "4Au⁰ + 8S₂O₃²⁻ + O₂ "
             "+ 2H₂O → 4Au(S₂O₃)₂³⁻ "
             "+ 4OH⁻", 18, FAINT, "middle", cls="phGold"))
    add(text(800, 396, "Au⁰ + 2S₂O₃²⁻ + Cu(II) → "
             "Au(S₂O₃)₂³⁻ + Cu(I)", 18, FAINT, "middle", cls="phGold"))
    add("</g>")

    add('<g id="dissolved-gold">')
    add(node(gx, gy, gr, "#f3e6c8", "#e0cb99", "", 0, GOLD))
    add('<circle cx="%d" cy="%d" r="20" fill="%s"/>' % (gx, gy, GOLD))
    add(text(gx, 414, "DISSOLVED GOLD", 24, INK, "middle", weight=700,
             ls=".06em"))
    add(text(gx, 444, "Au(S₂O₃)₂³⁻", 21, GOLD,
             "middle", weight=600))
    add(text(gx, 472, "Small share of the thiosulfate budget", 17, FAINT,
             "middle"))
    add("</g>")

    # ------------------------------------------------ copper entry -------
    add('<g id="copper-entry">')
    add(route("cuin", ARROW, 2.4, "aGrey"))
    add(text(500, 782, "Copper leaves the PCB as Cu(I)", 19, MUTED))
    add("</g>")

    # ------------------------------------------------- copper cycle ------
    # Cu(I) is a light fill with dark type, Cu(II) a solid rust fill with
    # light type. The two read apart by value as well as by hue, so the
    # oxidation state never depends on colour alone.
    add('<g id="copper-cycle">')
    add(route("ox", "#93a8bb", 3.2, "aBlue"))
    add(route("ox", BLUE, 4.4, "aBlue", cls="phOxGlow"))
    add(route("par", "#b9a4cd", 3.6, "aPur"))
    add(route("par", PURPLE, 6.0, "aPur", cls="phParGlow"))
    add(node(c1x, c1y, c1r, "#f7e3d6", CU1, "Cu(I)", 23, "#8a4a22"))
    add(node(c2x, c2y, c2r, CU2, CU2, "Cu(II)", 23, "#fdf6f2"))
    add(text(925, 714, "THE COPPER CYCLE REPEATS", 24, PURPLE, "middle",
             weight=700, ls=".08em"))
    add(text(925, 742, "OXYGEN RE-OXIDISES Cu(I) TO Cu(II)", 20, INK,
             "middle", weight=700, ls=".06em"))
    add(text(925, 772, "4Cu(I) + O₂ + 2H₂O → 4Cu(II) "
             "+ 4OH⁻", 18, FAINT, "middle", cls="phOx"))
    add("</g>")

    # The mechanism and the conclusion share the upper-centre line. They
    # never overlap in time, and the space is the calmest on the canvas.
    add('<g id="mechanism-statement" class="phCycle">')
    add(text(920, SAY_Y, "COPPER IS REGENERATED · THIOSULFATE IS "
             "CONSUMED", 26, CU2, "middle", weight=700, ls=".07em"))
    add("</g>")

    # ---------------------------------------------- competing pathway ----
    # The feed carries no arrowhead: it does not arrive anywhere on its own.
    # It ends at the reaction point, and only what leaves there is drawn
    # arriving at tetrathionate.
    add('<g id="competing-pathway">')
    add('<path d="%s" fill="none" stroke="%s" stroke-width="6.5"'
        ' stroke-linecap="round"/>' % (pathd(ROUTES["feed"]), ARROW))
    add('<path class="phParGlow" d="%s" fill="none" stroke="%s"'
        ' stroke-width="6.5" stroke-linecap="round"/>'
        % (pathd(ROUTES["feed"]), PURPLE))
    add(route("tet", ARROW, 6.5, "aGrey"))
    add(route("tet", PURPLE, 6.5, "aPur", cls="phParGlow"))
    add('<circle cx="%d" cy="%d" r="8" fill="%s" class="phParGlow"/>'
        % (rx, ry, PURPLE))
    add(text(880, 476, "COMPETING REACTION", 27, INK, "middle", weight=700,
             ls=".1em"))
    add(text(925, 530, "2Cu(II) + 2S₂O₃²⁻ → "
             "2Cu(I) + S₄O₆²⁻", 18, FAINT, "middle",
             cls="phPar"))
    add("</g>")

    add('<g id="tetrathionate">')
    add(node(tx, ty, tr, "#e6ddef", "#c9b8de",
             "S₄O₆²⁻", 24, "#5f4a78"))
    add(text(tx, 712, "TETRATHIONATE", 24, INK, "middle", weight=700,
             ls=".06em"))
    add(text(tx, 740, "Thiosulfate becomes tetrathionate", 18, MUTED,
             "middle"))
    add(text(tx, 768, "No gold is dissolved in this step", 18, PURPLE,
             "middle", weight=600))
    add("</g>")

    # -------------------------------------------------- travelling -------
    add('<g id="carriers">')
    add(token_at("gold", "tkGold",
                 '<circle r="11" fill="%s"/>'
                 '<circle r="17" fill="none" stroke="%s" stroke-width="2"'
                 ' opacity=".7"/>' % (GOLD, TEAL)))
    add(token_at("cuin", "tkCuIn", '<circle r="9" fill="%s"/>' % CU1))
    add(token_at("o2cu", "tkO2", '<circle r="7" fill="none" stroke="%s"'
                 ' stroke-width="2.4"/>' % BLUE))
    for n, cls in ((1, "tkOx1"), (2, "tkOx2"), (3, "tkOx3")):
        add(token_at("ox", cls, '<circle r="9" fill="%s"/>' % CU1))
    for n, cls in ((1, "tkPar1"), (2, "tkPar2"), (3, "tkPar3")):
        add(token_at("par", cls, '<circle r="9" fill="%s"/>' % CU2))
    for cls, dy in (("tkFeed1", -9), ("tkFeed2", 9)):
        add(token_at("feed", cls,
                     '<circle cy="%d" r="8" fill="%s"/>' % (dy, TEAL)))
    for cls in ("tkFeed3", "tkFeed4"):
        add(token_at("feed", cls, '<circle r="8" fill="%s"/>' % TEAL))
    for cls in ("tkTet1", "tkTet2", "tkTet3"):
        # tetrathionate is two thiosulfates welded together, and is drawn so
        add(token_at("tet", cls,
                     '<circle cx="-7" r="8.5" fill="%s"/>'
                     '<circle cx="7" r="8.5" fill="%s"/>' % (PURPLE, PURPLE)))
    add("</g>")

    # -------------------------------------------------- budget bar -------
    add('<g id="budget">')
    add(text(70, by + bh * 0.72, "THIOSULFATE AVAILABLE", 17, MUTED,
             weight=700, ls=".16em"))
    add('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="%s"/>'
        % (bx, by, bw, bh, bh // 2, "#ece7dd"))
    add('<rect class="budget" x="%d" y="%d" width="%d" height="%d" rx="%d"'
        ' fill="%s"/>' % (bx, by, bw, bh, bh // 2, TEAL))
    # the allocation, shown as shape and not as a number
    add('<rect x="%d" y="%d" width="%.1f" height="%d" rx="2" fill="%s"/>'
        % (bx, ALLOC_Y, bw * ALLOC_GOLD, ALLOC_H, GOLD))
    add('<rect x="%.1f" y="%d" width="%.1f" height="%d" rx="2" fill="%s"/>'
        % (bx + bw * ALLOC_GOLD + 4, ALLOC_Y, bw * ALLOC_CU - 4,
           ALLOC_H, CU1))
    add('<rect x="%.1f" y="%d" width="%.1f" height="%d" rx="2" fill="%s"/>'
        % (bx + bw * (ALLOC_GOLD + ALLOC_CU) + 4, ALLOC_Y,
           bw * (1 - ALLOC_GOLD - ALLOC_CU) - 4, ALLOC_H, PURPLE))
    add(text(bx, ALLOC_Y + ALLOC_H + 22, "TO GOLD", 15, GOLD,
             weight=700, ls=".12em"))
    add(text(bx + 118, ALLOC_Y + ALLOC_H + 22,
             "TO COPPER METAL", 15, "#a9683f",
             weight=700, ls=".12em"))
    add(text(bx + bw, ALLOC_Y + ALLOC_H + 22, "DIVERTED TO TETRATHIONATE",
             15, PURPLE, "end", weight=700, ls=".12em"))
    add("</g>")

    add('<g id="closing" class="phEnd">')
    add(text(920, SAY_Y, "THE LEACHANT RUNS OUT FIRST", 30, INK, "middle",
             weight=700, ls=".08em"))
    add("</g>")

    add('<script type="text/javascript"><![CDATA[%s]]></script>' % SCRIPT)
    add("</svg>")
    return "".join(a)


TITLE = "Thiosulfate is a finite reaction budget"
DESC = ("Inside the leaching vessel, thiosulfate is a fixed charge. Oxygen "
        "from a controlled supply above the vessel helps thiosulfate dissolve "
        "gold from crushed circuit board, which carries far more copper than "
        "gold, and copper(II) dissolves gold as well. Copper leaves the board "
        "as copper(I); oxygen re-oxidises it to copper(II), which converts "
        "thiosulfate into tetrathionate and returns to copper(I). The budget "
        "bar splits the thiosulfate three ways: a small share to dissolved "
        "gold, a larger one to dissolved copper, and the rest to "
        "tetrathionate. The copper is regenerated on every turn and the "
        "thiosulfate is not, so the leachant runs out while gold is still on "
        "the board.")

# name, route, start and end on the 12 s clock
TRAVELS = [
    ("tkGold", "gold", 2.4, 4.2),
    ("tkCuIn", "cuin", 4.2, 5.4),
    ("tkO2", "o2cu", 4.6, 5.6),
    ("tkOx1", "ox", 5.4, 6.4),
    ("tkFeed1", "feed", 6.2, 7.6),
    ("tkFeed2", "feed", 6.4, 7.8),
    ("tkPar1", "par", 7.6, 8.6),
    ("tkTet1", "tet", 7.8, 8.8),
    ("tkOx2", "ox", 8.6, 9.4),
    ("tkFeed3", "feed", 9.0, 9.8),
    ("tkPar2", "par", 9.6, 10.1),
    ("tkTet2", "tet", 9.7, 10.3),
    ("tkOx3", "ox", 9.9, 10.3),
    ("tkFeed4", "feed", 9.8, 10.4),
    ("tkPar3", "par", 10.1, 10.5),
    ("tkTet3", "tet", 10.2, 10.6),
]

SCRIPT = """
(function(){
  var svg=document.documentElement;
  // Stop the clock while the tab is in the background, and let a click
  // start the loop over. Nothing else here needs scripting.
  function sync(){ svg.classList.toggle('paused', document.hidden); }
  document.addEventListener('visibilitychange', sync); sync();
  svg.addEventListener('click', function(){
    var all = svg.getAnimations ? svg.getAnimations({subtree:true}) : [];
    for (var i=0;i<all.length;i++){ all[i].currentTime=0; }
  });
})();
"""


def main():
    path = OUT / "leaching-budget.svg"
    path.write_text(render(), encoding="utf-8")
    print("wrote %s  %d bytes" % (path.name, path.stat().st_size))
    print("clock %.1f s, %d travelling tokens" % (T, len(TRAVELS)))


if __name__ == "__main__":
    main()
