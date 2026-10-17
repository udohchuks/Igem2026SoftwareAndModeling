"""Assets for the leaching figure, each drawn on its own and composable.

Every asset is a function returning a dict with its own width, height, body
markup and CSS. The body is written in LOCAL coordinates with the origin at
the asset's top-left, so the composer can place it anywhere with a single
translate and nothing inside an asset needs to know where it ended up.

Run this module to inspect one asset by itself:

    python docs/leach_assets.py vessel
    python docs/leach_assets.py --all

which writes standalone SVGs under docs/media/wiki/concepts/_assets/.
Those files are scratch and are not referenced by the wiki.

The figure these assets build carries one argument and no more:

    A small pathway dissolves gold. Oxygen also regenerates Cu(II). The
    repeating Cu(I)/Cu(II) cycle converts much more thiosulfate into
    tetrathionate. Thiosulfate is exhausted, and gold dissolution stops.

Reactions quoted in the figure come from the source document
"Bioleaching_Models_v5", paragraphs 147 and 165-166, matching
docs/EQUATIONS.md lines 123-150 and docs/MASTER.md lines 570-575.

There is exactly one bar in the figure and it is the timeline. The size of
the thiosulfate budget is told by the liquor emptying and the tetrathionate
node filling, never by a meter.
"""
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "media" / "wiki" / "concepts"
SCRATCH = OUT / "_assets"

# ---------------------------------------------------------------- constants

T = 12.0                       # master clock, seconds, shared by every asset

BG = "#faf8f3"                 # warm off-white
INK = "#26221d"
MUTED = "#7b756c"
FAINT = "#a9a296"
HAIR = "#e3ddd2"
ARROW = "#c7c0b4"

TEAL = "#2d8f94"               # thiosulfate
GOLD = "#b3821f"               # gold
CU1 = "#cc8d63"                # copper(I), light terracotta
CU2 = "#9c4a2f"                # copper(II), dark rust
PURPLE = "#8a70a6"             # tetrathionate
BLUE = "#4a86b8"               # oxygen
BOARD = "#39433a"              # PCB substrate
COPPER = "#8d5738"             # copper metal on the board
LIQUID = "#e7f0f2"
GLASS = "#ffffff"

SERIF = "Iowan Old Style,Georgia,'Times New Roman',serif"
SANS = "Inter,'Segoe UI',system-ui,sans-serif"


# ---------------------------------------------------------------- helpers


def pc(t):
    """Seconds on the master clock as a keyframe percentage."""
    return max(0.0, min(100.0, t / T * 100.0))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size, fill=INK, anchor="start", weight=400, ls="0",
         family=SANS, cls=None):
    return ('<text x="%s" y="%s" font-family="%s" font-size="%s"'
            ' font-weight="%s" letter-spacing="%s" text-anchor="%s"'
            ' style="fill:%s"%s>%s</text>'
            % (x, y, family, size, weight, ls, anchor, fill,
               ' class="%s"' % cls if cls else "", esc(s)))


def fade(name, spans, hold=0.0):
    """Keyframes that hold opacity 1 across the given [t0, t1] windows."""
    stops, f = [(0.0, hold)], 0.2
    for t0, t1 in spans:
        stops += [(pc(t0), hold), (pc(t0 + f), 1.0),
                  (pc(t1 - f), 1.0), (pc(t1), hold)]
    stops.append((100.0, hold))
    body = "".join("%.2f%%{opacity:%.2f}" % s for s in stops)
    return ("@keyframes %s{%s}.%s{opacity:%.2f;"
            "animation:%s %.1fs linear infinite}"
            % (name, body, name, hold, name, T))


def ramp(name, steps, prop="opacity", unit=""):
    """Keyframes stepping one property through (time, value) pairs."""
    body = "".join("%.2f%%{%s:%s%s}" % (pc(t), prop, v, unit)
                   for t, v in steps)
    return "@keyframes %s{%s}" % (name, body)


# ================================================================= assets
#
# Each returns dict(w, h, body, css). Anchors are extra named points the
# composer needs, given in the asset's own local coordinates.


def asset_title(width=760):
    """The upper-left title block: eyebrow, serif line, hairline rule."""
    b = [text(0, 20, "INSIDE THE LEACHING VESSEL", 15, MUTED,
              weight=700, ls=".22em"),
         text(0, 72, "Thiosulfate is a finite reaction budget", 46, INK,
              family=SERIF, ls="-.005em"),
         '<rect x="0" y="100" width="%d" height="1" fill="%s"/>'
         % (width, HAIR)]
    return dict(w=width, h=104, body="".join(b), css="", anchors={})


def asset_vessel(w=400, h=372):
    """The vessel, and everything that happens inside it.

    The oxygen enters here rather than from a labelled pump: a metered
    supply from above is the team's arrangement, and a box with a caption
    was one more thing on the canvas without being one more idea.

    The board is deliberately small. It is crushed feed, and drawing it
    large made it compete with the chemistry for attention while saying
    nothing extra. What it has to show is one proportion: a hairline of
    plated gold over a body of bulk copper.

    The liquor empties over the run. That is the whole budget argument,
    and it is why the figure needs no meter.
    """
    lip, pad = 34, 12
    lx, ly = pad, lip
    lw, lh = w - pad * 2, h - lip - pad
    b, css = [], []

    b.append('<rect x="0" y="0" width="%d" height="%d" rx="18" fill="%s"'
             ' stroke="%s" stroke-width="1.5"/>' % (w, h, GLASS, HAIR))
    b.append('<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="%s"/>'
             % (lx, ly, lw, lh, LIQUID))

    # ---- oxygen, entering from above and dispersing -----------------------
    # Drawn diatomic, the same grammar the figure uses for tetrathionate:
    # a species is one disc, a pair welded together is two.
    css.append("@keyframes o2in{0%%{transform:translateY(-%dpx);opacity:0}"
               "16%%{opacity:.95}72%%{opacity:.95}"
               "100%%{transform:translateY(%dpx);opacity:0}}" % (lip + 14, lh * 0.46))
    css.append(".o2{animation:o2in 4.2s cubic-bezier(.4,0,.6,1) infinite}")
    for i, ox in enumerate((0.26, 0.54, 0.78)):
        x = lx + lw * ox
        b.append('<g class="o2" style="animation-delay:%.1fs">'
                 '<circle cx="%.1f" cy="%d" r="7" fill="none" stroke="%s"'
                 ' stroke-width="3"/>'
                 '<circle cx="%.1f" cy="%d" r="7" fill="none" stroke="%s"'
                 ' stroke-width="3"/></g>'
                 % (i * 1.4, x - 5, ly + 16, BLUE, x + 5, ly + 16, BLUE))
    b.append(text(lx + lw - 8, ly + 26, "O₂", 19, BLUE, "end",
                  weight=700))

    # ---- the board: small, scattered, no two alike ------------------------
    floor = ly + lh - 16
    pieces = [(52, 30, -4, 0), (44, 34, 3, 9), (58, 25, -1, -2),
              (38, 31, 6, 5), (50, 27, -2, 12)]
    gaps = [12, 26, 9, 30]
    x = lx + 20
    for i, (fw, fh, tilt, lift) in enumerate(pieces):
        fy = floor - fh - lift
        c = [(i * 3) % 5 + 2, (i * 5) % 4 + 2, (i * 7) % 6 + 2]
        quad = ("M%.1f 0 L%.1f 1 L%.1f %.1f L%.1f %.1f Z"
                % (c[0], fw - c[1], fw, fh, c[2] * 0.5, fh))
        b.append('<g transform="translate(%.1f,%.1f) rotate(%d,%.1f,%.1f)">'
                 % (x, fy, tilt, fw / 2, fh / 2))
        b.append('<clipPath id="pcb%d"><path d="%s"/></clipPath>' % (i, quad))
        b.append('<path d="%s" fill="%s"/>' % (quad, BOARD))
        b.append('<g clip-path="url(#pcb%d)">' % i)
        b.append('<rect x="2" y="%.1f" width="%.1f" height="%.1f"'
                 ' fill="%s"/>' % (fh * 0.36, fw - 4, fh * 0.58, COPPER))
        b.append('<rect x="2" y="%.1f" width="%.1f" height="4" fill="%s"/>'
                 % (fh * 0.19, fw - 4, GOLD))
        b.append("</g></g>")
        x += fw + (gaps[i] if i < len(gaps) else 16)

    # ---- thiosulfate, spent in the order the run spends it ----------------
    sites = [(58, 76), (146, 60), (232, 84), (312, 64),
             (40, 130), (122, 112), (206, 138), (292, 118), (348, 98),
             (72, 186), (160, 166), (248, 192), (324, 160), (46, 218)]
    spend = [3.1, 3.1, 5.2, 5.2, 7.2, 7.4, 7.6, 7.8, 9.2, 9.4, 9.6,
             10.1, 10.3, 10.5]
    for i, ((sx, sy), gone) in enumerate(zip(sites, spend)):
        css.append("@keyframes gone%d{0%%{opacity:.9}%.2f%%{opacity:.9}"
                   "%.2f%%{opacity:0}100%%{opacity:0}}"
                   % (i, pc(gone), pc(gone + 0.4)))
        css.append(".g%d{animation:gone%d %.1fs linear infinite}" % (i, i, T))
        b.append('<g class="s2o3" style="animation-delay:-%.1fs">'
                 '<circle class="g%d" cx="%d" cy="%d" r="8" fill="%s"/></g>'
                 % ((i % 5) * 1.2, i, lx + sx, ly + sy, TEAL))
    css.append("@keyframes bob{0%,100%{transform:translate(0,0)}"
               "50%{transform:translate(2px,-4px)}}")
    css.append(".s2o3{animation:bob 6s ease-in-out infinite}")

    b.append(text(lx + 10, ly + 26, "S₂O₃²⁻", 19,
                  TEAL, weight=600))
    return dict(w=w, h=h, body="".join(b), css="".join(css), anchors={})


def _node(r, fill, ring, label, lsize, lcolour, ringw=2.5, sub=None):
    """A species or product disc, drawn about its own centre."""
    b = ['<circle cx="0" cy="0" r="%d" fill="%s"/>' % (r, fill),
         '<circle cx="0" cy="0" r="%d" fill="none" stroke="%s"'
         ' stroke-width="%s"/>' % (r, ring, ringw)]
    if label:
        b.append(text(0, lsize * 0.35, label, lsize, lcolour, "middle",
                      weight=600))
    if sub:
        b.append(sub)
    return b


def asset_gold_node(r=64):
    """Dissolved gold. The disc gains gold as the desired reaction fires."""
    b = _node(r, "#f5e9cd", "#e0cb99", "", 0, GOLD)
    b.append('<circle class="auFill" cx="0" cy="0" r="%d" fill="%s"/>'
             % (int(r * 0.34), GOLD))
    # The disc gains gold in two steps: once at the desired reaction, and a
    # little more over the later repeats, then it stops for good.
    css = ("@keyframes auGrow{0%%,%.2f%%{transform:scale(.42)}"
           "%.2f%%,%.2f%%{transform:scale(.80)}"
           "%.2f%%,100%%{transform:scale(.92)}}"
           ".auFill{transform-box:fill-box;transform-origin:center;"
           "animation:auGrow %.1fs ease-out infinite}"
           % (pc(2.6), pc(3.6), pc(9.0), pc(10.0), T))
    return dict(w=r * 2, h=r * 2, origin=(r, r), body="".join(b), css=css,
                anchors={})


def asset_cu1(r=52):
    """Copper(I). A light disc with dark type.

    Cu(I) and Cu(II) are told apart by value as well as by hue, so the
    oxidation state never rests on colour alone.
    """
    b = _node(r, "#f7e3d6", CU1, "Cu(I)", 24, "#7d4320")
    return dict(w=r * 2, h=r * 2, origin=(r, r), body="".join(b), css="",
                anchors={})


def asset_cu2(r=52):
    """Copper(II). A solid rust disc with light type.

    It brightens each time oxygen rebuilds it, which is the beat the whole
    figure turns on: the copper comes back, the thiosulfate does not.
    """
    b = ['<circle class="cu2Glow" cx="0" cy="0" r="%d" fill="%s"'
         ' opacity="0"/>' % (r + 11, CU2),
         '<circle cx="0" cy="0" r="%d" fill="%s"/>' % (r, CU2),
         text(0, 8, "Cu(II)", 24, "#fdf4f0", "middle", weight=600)]
    css = ("@keyframes cu2Pulse{0%%,%.2f%%{opacity:0}%.2f%%{opacity:.28}"
           "%.2f%%{opacity:0}%.2f%%{opacity:.28}%.2f%%{opacity:0}"
           "100%%{opacity:0}}"
           ".cu2Glow{animation:cu2Pulse %.1fs ease-out infinite}"
           % (pc(5.0), pc(5.6), pc(6.6), pc(9.3), pc(10.2), T))
    return dict(w=(r + 11) * 2, h=(r + 11) * 2, origin=(r + 11, r + 11),
                body="".join(b), css=css, anchors={})


def asset_tet(r=66):
    """Tetrathionate. The disc fills as the leachant is spent.

    This is what replaces a budget meter: the thiosulfate leaves the vessel
    and arrives here, and the reader reads the size of the loss off the
    thing the loss turned into.
    """
    b = _node(r, "#ece4f3", "#c9b8de", "", 0, PURPLE)
    b.append('<circle class="tetFill" cx="0" cy="0" r="%d" fill="%s"'
             ' opacity=".85"/>' % (r, PURPLE))
    b.append(text(0, 9, "S₄O₆²⁻", 25, "#4e3a66",
                  "middle", weight=600))
    css = ("@keyframes tetGrow{0%%,%.2f%%{transform:scale(.10)}"
           "%.2f%%,%.2f%%{transform:scale(.44)}"
           "%.2f%%,%.2f%%{transform:scale(.72)}"
           "%.2f%%,100%%{transform:scale(.94)}}"
           ".tetFill{transform-box:fill-box;transform-origin:center;"
           "animation:tetGrow %.1fs ease-out infinite}"
           % (pc(7.0), pc(8.0), pc(9.2), pc(9.9), pc(10.1), pc(10.7), T))
    return dict(w=r * 2, h=r * 2, origin=(r, r), body="".join(b), css=css,
                anchors={})


def asset_cycle():
    """The Cu(I)/Cu(II) cycle: the heaviest object on the canvas.

    It owns both nodes and both arcs, so nothing can drift out of
    alignment, and it owns the junction where thiosulfate is destroyed.

    Two decisions the chemistry forces. The lower arc is Cu(I) to Cu(II)
    and is driven by oxygen, which is why it is blue. The upper arc is
    Cu(II) back to Cu(I), which is the step that eats thiosulfate, so the
    junction sits on that arc and not beside it: the reader cannot reach
    tetrathionate without passing through the copper.

    The arcs are drawn heavy because this pathway is the dominant one.
    An earlier version drew it as thin as the desired pathway and the
    figure argued the opposite of what the model says.
    """
    cy = 170
    c1, c2 = (52, cy), (368, cy)
    jx, jy = 210, 86       # seed only; recomputed from the arc below
    w, h = 440, 336
    RING = 14                                   # junction ring radius
    b, css, defs = [], [], []

    for ident, colour in (("arcBlue", BLUE), ("arcPurple", PURPLE)):
        defs.append('<marker id="%s" viewBox="0 0 12 12" refX="9.4"'
                    ' refY="6" markerWidth="15" markerHeight="15"'
                    ' markerUnits="userSpaceOnUse" orient="auto">'
                    '<path d="M1 1L11 6L1 11Z" fill="%s"/></marker>'
                    % (ident, colour))

    # the arc ends sit ON the discs, at 45 degrees, so the arrowheads touch
    # what they point at instead of stopping short of it
    off = 37                                    # 52 * cos(45 degrees)
    # Arrow ends are computed, never guessed. A tail tucks INSIDE its disc
    # so the disc hides the join; a head stops just OUTSIDE the other disc
    # so the arrowhead is whole and visibly aimed at what it points to. A
    # 10 px stroke ending exactly on a rim at 45 degrees leaves a notch,
    # which is what the earlier version did at all four ends.
    TAIL, HEAD = 44.0, 60.0                     # radii, disc is 52
    k = 0.7071                                  # 45 degrees

    def on(centre, r, sx, sy):
        return (centre[0] + r * k * sx, centre[1] + r * k * sy)

    dn_a, dn_b = on(c1, TAIL, 1, 1), on(c2, HEAD, -1, 1)
    up_a, up_b = on(c2, TAIL, -1, -1), on(c1, HEAD, 1, -1)
    dn_c1, dn_c2 = (150, cy + 126), (270, cy + 126)
    up_c1, up_c2 = (270, jy - 4), (150, jy - 4)

    def bez(p0, p1, p2, p3, t):
        m = 1 - t
        return tuple(m ** 3 * p0[i] + 3 * m * m * t * p1[i]
                     + 3 * m * t * t * p2[i] + t ** 3 * p3[i]
                     for i in (0, 1))

    # the junction is placed ON the parasitic arc by evaluating it, so the
    # ring can never drift off the curve it is supposed to sit on
    jx, jy = bez(up_a, up_c1, up_c2, up_b, 0.5)

    up = "M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f" % (
        up_a + up_c1 + up_c2 + up_b)
    dn = "M%.1f %.1f C%.1f %.1f %.1f %.1f %.1f %.1f" % (
        dn_a + dn_c1 + dn_c2 + dn_b)

    # lower arc: oxygen doing the re-oxidising, Cu(I) to Cu(II)
    b.append('<path d="%s" fill="none" stroke="%s" stroke-width="10"'
             ' stroke-linecap="round" marker-end="url(#arcBlue)"/>'
             % (dn, "#9fc0d8"))
    b.append('<path class="arcOx" d="%s" fill="none" stroke="%s"'
             ' stroke-width="10" stroke-linecap="round"/>' % (dn, BLUE))
    # upper arc: the parasitic return that spends the leachant
    b.append('<path d="%s" fill="none" stroke="%s" stroke-width="10"'
             ' stroke-linecap="round" marker-end="url(#arcPurple)"/>'
             % (up, "#c3b2d6"))
    b.append('<path class="arcPar" d="%s" fill="none" stroke="%s"'
             ' stroke-width="10" stroke-linecap="round"/>' % (up, PURPLE))

    a1, a2 = asset_cu1(), asset_cu2()
    b.append('<g transform="translate(%d,%d)">%s</g>' % (c1[0], c1[1],
                                                         a1["body"]))
    b.append('<g transform="translate(%d,%d)">%s</g>' % (c2[0], c2[1],
                                                         a2["body"]))
    css += [a1["css"], a2["css"]]

    # the junction: where thiosulfate is spent and tetrathionate is made
    b.append('<circle class="jGlow" cx="%.1f" cy="%.1f" r="%d" fill="%s"'
             ' opacity="0"/>' % (jx, jy, RING + 12, PURPLE))
    # Hollow, not filled. A filled ring masked the arc and read as a bead
    # threaded on a string; leaving it open lets the copper arc run visibly
    # straight through, which is the point: the copper passes through this
    # reaction, the thiosulfate does not come out the other side.
    b.append('<circle cx="%.1f" cy="%.1f" r="%d" fill="none" stroke="%s"'
             ' stroke-width="4"/>' % (jx, jy, RING, PURPLE))

    # No caption here. The cycle is explained once, by the composition,
    # and repeating it on the asset was two of the thirty-one text runs
    # that made the figure read as clutter.
    css.append("@keyframes arcOxOn{0%%,%.2f%%{opacity:0}%.2f%%,%.2f%%"
               "{opacity:1}%.2f%%{opacity:0}%.2f%%,%.2f%%{opacity:1}"
               "%.2f%%,100%%{opacity:0}}"
               ".arcOx{opacity:0;animation:arcOxOn %.1fs linear infinite}"
               % (pc(4.6), pc(5.0), pc(6.2), pc(6.6), pc(9.0), pc(9.6),
                  pc(10.1), T))
    css.append("@keyframes arcParOn{0%%,%.2f%%{opacity:0}%.2f%%,%.2f%%"
               "{opacity:1}%.2f%%,100%%{opacity:0}}"
               ".arcPar{opacity:0;animation:arcParOn %.1fs linear infinite}"
               % (pc(6.4), pc(6.9), pc(10.4), pc(10.9), T))
    css.append("@keyframes jOn{0%%,%.2f%%{opacity:0}%.2f%%{opacity:.30}"
               "%.2f%%{opacity:0}100%%{opacity:0}}"
               ".jGlow{animation:jOn %.1fs ease-out infinite}"
               % (pc(6.8), pc(7.4), pc(10.6), T))

    return dict(w=w, h=h, body="".join(b), css="".join(css),
                defs="".join(defs),
                anchors=dict(cu1=c1, cu2=c2, junction=(jx, jy),
                             ring=RING))


def asset_timeline(w=1460):
    """The only bar in the figure, and it measures time, not quantity.

    Every other number the figure carries is told by an asset changing:
    the liquor empties, the tetrathionate disc fills. This bar exists so a
    reader can tell where they are in the loop and when it starts again.
    """
    b, css = [], []
    marks = [(3.1, "GOLD"), (5.2, "COPPER"), (7.4, "THE COPPER CYCLE"),
             (10.6, "LEACHANT SPENT")]
    b.append('<rect x="0" y="0" width="%d" height="2" rx="1" fill="%s"/>'
             % (w, HAIR))
    b.append('<rect class="tlFill" x="0" y="-1" width="%d" height="4" rx="2"'
             ' fill="%s"/>' % (w, TEAL))
    for t, name in marks:
        x = w * t / T
        b.append('<rect x="%.1f" y="4" width="1.5" height="9" fill="%s"/>'
                 % (x, HAIR))
        b.append(text(x, 30, name, 13, FAINT, "middle", weight=700,
                      ls=".14em"))
    b.append('<circle class="tlHead" cx="0" cy="1" r="6" fill="%s"/>'
             % TEAL)
    css.append("@keyframes tlSweep{from{transform:scaleX(0)}"
               "to{transform:scaleX(1)}}"
               ".tlFill{transform-box:fill-box;transform-origin:left center;"
               "animation:tlSweep %.1fs linear infinite}" % T)
    css.append("@keyframes tlRun{from{transform:translateX(0)}"
               "to{transform:translateX(%dpx)}}"
               ".tlHead{animation:tlRun %.1fs linear infinite}" % (w, T))
    return dict(w=w, h=36, body="".join(b), css="".join(css), anchors={})


# ---------------------------------------------------------------- harness

ASSETS = {
    "timeline": asset_timeline,
    "title": asset_title,
    "vessel": asset_vessel,
    "gold": asset_gold_node,
    "cu1": asset_cu1,
    "cu2": asset_cu2,
    "tet": asset_tet,
    "cycle": asset_cycle,
}


def standalone(name):
    """Wrap one asset in its own SVG so it can be looked at by itself.

    `origin` says where the asset's own (0,0) sits inside its box, so discs
    drawn about their centre land in the same frame as boxes drawn from
    their top-left.
    """
    a = ASSETS[name]()
    pad = 40
    ox, oy = a.get("origin", (0, 0))
    w, h = a["w"] + pad * 2, a["h"] + pad * 2
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"'
            ' width="%d" height="%d">'
            '<defs>%s</defs><style>%s</style>'
            '<rect width="%d" height="%d" fill="%s"/>'
            '<g transform="translate(%.1f,%.1f)">%s</g></svg>'
            % (w, h, w, h, a.get("defs", ""), a["css"], w, h, BG,
               pad + ox, pad + oy, a["body"]))


def main(argv):
    SCRATCH.mkdir(parents=True, exist_ok=True)
    names = sorted(ASSETS) if (not argv or argv[0] == "--all") else argv
    for n in names:
        if n not in ASSETS:
            print("no such asset: %s" % n)
            continue
        p = SCRATCH / ("_%s.svg" % n)
        p.write_text(standalone(n), encoding="utf-8")
        a = ASSETS[n]()
        print("%-12s %4d x %4d   %s" % (n, a["w"], a["h"], p.name))


if __name__ == "__main__":
    main(sys.argv[1:])
