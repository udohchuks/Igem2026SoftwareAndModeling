"""Compose the leaching figure from the assets in docs/leach_assets.py.

This module owns only three things: where each asset sits, the routes
between them, and the few labels that belong to no single asset.

    python docs/leach_assets.py --all     inspect the parts
    python docs/make_leach_figure.py      build the whole

One argument, and nothing else earns space:

    A small pathway dissolves gold. Oxygen also regenerates Cu(II). The
    repeating Cu(I)/Cu(II) cycle converts much more thiosulfate into
    tetrathionate. Thiosulfate is exhausted, and gold dissolution stops.

An earlier build put thirty-one text runs and nine stroke weights on this
canvas and read as clutter. The budget here is deliberate and tight:

  * five composition labels plus the assets' own names, and no sentence
    that only restates the label above it;
  * three stroke weights, 1.5 for containers, 3 for the small pathway and
    10 for the dominant one, so weight alone says which matters;
  * four routes, each a single shallow curve. Three leave the vessel from
    one wall and one leaves the junction. Nothing wanders across the page.

Three constraints the geometry answers for:

1. Copper is never fed in. It leaves the board as Cu(0) and dissolves as
   Cu(I), and v4 is the only source of Cu(II) in the model
   (EQUATIONS.md line 208), so the entry arrow runs into Cu(I).
2. Cu(II) is a reactant of the parasitic step, not a product. The route to
   tetrathionate lands on the junction that sits ON the Cu(II) to Cu(I)
   arc, so tetrathionate cannot be reached without going through the
   copper. No arrow runs from the vessel to tetrathionate.
3. There is one bar and it is the timeline. The size of the loss is told
   by the liquor emptying and the tetrathionate disc filling.

Writes docs/media/wiki/concepts/leaching-budget.svg.
"""
from pathlib import Path

import leach_assets as A
from leach_assets import (BG, INK, MUTED, ARROW, TEAL, GOLD, PURPLE, BLUE,
                          CU1, T, pc, text, esc)

W, H = 1600, 900
OUT = Path(__file__).resolve().parent / "media" / "wiki" / "concepts"

THIN, HEAVY = 3, 10
TINT_GOLD, TINT_CU, TINT_PUR = "#cbb383", "#d9b49a", "#d5cbe3"

PLACE = dict(
    title=(70, 56),
    vessel=(70, 280),
    cycle=(560, 450),
    gold=(1300, 352),           # discs are placed by their centre
    tet=(1310, 620),
    timeline=(70, 840),
)

CYC = PLACE["cycle"]
_CYCLE = A.asset_cycle()
_JX, _JY = _CYCLE["anchors"]["junction"]
RING = _CYCLE["anchors"]["ring"]
JUNCTION = (CYC[0] + _JX, CYC[1] + _JY)


def on_ring(dx, dy, clear=2.0):
    """A point on the junction ring, in the given direction.

    The two purple routes meet the ring by construction. Writing their
    endpoints by hand left the arrowhead floating thirteen pixels clear of
    the node it was meant to arrive at, which is what made the junction
    read as a bead on a string rather than a reaction site.
    """
    n = (dx * dx + dy * dy) ** 0.5
    r = RING + clear
    return (round(JUNCTION[0] + r * dx / n, 1),
            round(JUNCTION[1] + r * dy / n, 1))


def land(centre, r, toward, clear=4.0):
    """A point just outside a disc, on the line from its centre to `toward`.

    Route ends are computed against the thing they point at. Hand-written
    ones drifted: the tetrathionate head finished 29 px short of its disc
    and the copper head finished 1 px inside Cu(I), where the disc drew
    over it.
    """
    dx, dy = toward[0] - centre[0], toward[1] - centre[1]
    n = (dx * dx + dy * dy) ** 0.5
    d = r + clear
    return (round(centre[0] + d * dx / n, 1),
            round(centre[1] + d * dy / n, 1))


GOLD_AT, TET_AT = PLACE["gold"], PLACE["tet"]
GOLD_R, TET_R, CU_R = 62, 62, 52
CU1_AT = (CYC[0] + _CYCLE["anchors"]["cu1"][0],
          CYC[1] + _CYCLE["anchors"]["cu1"][1])


FEED_END = on_ring(-0.60, -0.80)        # thiosulfate arrives from upper left
TET_START = on_ring(0.87, -0.49)        # tetrathionate leaves to upper right

# Four routes, each one shallow curve. Three leave the vessel's right wall
# at three heights, which reads as a fan rather than as scribble. The two
# purple ones begin and end ON the junction ring, never near it.
ROUTES = {
    "gold": [(474, 352), (700, 302), (980, 312),
             land(GOLD_AT, GOLD_R, (980, 312))],
    "feed": [(474, 428), (614, 436), (716, 470), FEED_END],
    "cuin": [(474, 578), (512, 594), (538, 602),
             land(CU1_AT, CU_R, (538, 602))],
    "tetout": [TET_START, (866, 496), (1084, 482),
               land(TET_AT, TET_R, (1084, 482))],
    "o2arc": [(770, 680), (770, 698), (770, 716), (770, 732)],
}

TRAVELS = [
    ("tkAu", "gold", 2.4, 4.0),
    ("tkCuIn", "cuin", 4.4, 5.2),
    ("tkO2", "o2arc", 4.8, 5.6),
    ("tkFeedA", "feed", 6.3, 7.2),
    ("tkFeedB", "feed", 6.6, 7.5),
    ("tkTetA", "tetout", 7.6, 8.5),
    ("tkFeedC", "feed", 9.0, 9.7),
    ("tkTetB", "tetout", 9.8, 10.3),
    ("tkFeedD", "feed", 9.8, 10.3),
    ("tkTetC", "tetout", 10.4, 10.9),
]


def pathd(pts, dx=0.0, dy=0.0):
    d = "M%.1f %.1f" % (pts[0][0] - dx, pts[0][1] - dy)
    for i in range(1, len(pts), 3):
        a, b, c = pts[i], pts[i + 1], pts[i + 2]
        d += "C%.1f %.1f %.1f %.1f %.1f %.1f" % (
            a[0] - dx, a[1] - dy, b[0] - dx, b[1] - dy, c[0] - dx, c[1] - dy)
    return d


def marker(ident, colour, size=16):
    return ('<marker id="%s" viewBox="0 0 12 12" refX="9.4" refY="6"'
            ' markerWidth="%d" markerHeight="%d" markerUnits="userSpaceOnUse"'
            ' orient="auto"><path d="M1 1L11 6L1 11Z" fill="%s"/></marker>'
            % (ident, size, size, colour))


def route(key, colour, width, mark):
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%s"'
            ' marker-end="url(#%s)"/>'
            % (pathd(ROUTES[key]), colour, width, mark))


def travel(name, key, t0, t1):
    """One token riding one route between two moments on the master clock."""
    f = 0.18
    frac = f / max(t1 - t0, 0.01)
    stops = [(0.0, 0, 0.0)]
    if t0 > 0.02:
        stops.append((pc(t0), 0, 0.0))
    stops += [(pc(t0 + f), 1, 100.0 * frac),
              (pc(t1 - f), 1, 100.0 * (1 - frac)),
              (pc(t1), 0, 100.0), (100.0, 0, 100.0)]
    frames = "".join("%.2f%%{opacity:%d;offset-distance:%.1f%%}" % s
                     for s in stops)
    p0 = ROUTES[key][0]
    return ("@keyframes %s{%s}.%s{offset-path:path('%s');offset-rotate:0deg;"
            "animation:%s %.1fs cubic-bezier(.45,0,.55,1) infinite}"
            % (name, frames, name, pathd(ROUTES[key], *p0), name, T))


def token(key, cls, body):
    """Place a travelling token at its route start.

    The wrapper carries the translate and the path is written about the
    origin, so a renderer without offset-path rests the token at the start
    of its route instead of in the corner of the canvas.
    """
    x, y = ROUTES[key][0]
    return ('<g transform="translate(%.1f,%.1f)"><g class="tok %s">%s</g>'
            '</g>' % (x, y, cls, body))


def phase(name, t0, t1, fade=0.25):
    stops = [(0.0, 0)]
    if t0 > 0.02:
        stops.append((pc(t0), 0))
    stops += [(pc(t0 + fade), 1), (pc(t1 - fade), 1)]
    if t1 < T - 0.02:
        stops += [(pc(t1), 0), (100.0, 0)]
    else:
        stops.append((100.0, 1))
    return ("@keyframes %s{%s}.%s{opacity:0;animation:%s %.1fs linear"
            " infinite}"
            % (name, "".join("%.2f%%{opacity:%d}" % s for s in stops),
               name, name, T))


TITLE = "Thiosulfate is a finite reaction budget"
DESC = ("Inside the leaching vessel, thiosulfate is a fixed charge. Oxygen "
        "enters from above and helps thiosulfate dissolve gold from crushed "
        "circuit board, which carries far more copper than gold, and that "
        "pathway takes only a small share of the charge. Copper leaves the "
        "board as copper(I). The same oxygen re-oxidises it to copper(II), "
        "which converts thiosulfate into tetrathionate at a junction on the "
        "copper cycle and returns to copper(I). The copper comes back on "
        "every turn and the thiosulfate does not, so the leachant is "
        "exhausted while gold is still on the board.")

SCRIPT = """
(function(){
  var svg=document.documentElement;
  function sync(){ svg.classList.toggle('paused', document.hidden); }
  document.addEventListener('visibilitychange', sync); sync();
  svg.addEventListener('click', function(){
    var all = svg.getAnimations ? svg.getAnimations({subtree:true}) : [];
    for (var i=0;i<all.length;i++){ all[i].currentTime = 0; }
  });
})();
"""


def render():
    parts, css, defs = [], [], []
    add = parts.append
    assets = {k: getattr(A, "asset_" + {"gold": "gold_node"}.get(k, k))()
              for k in PLACE}

    for ident, colour in (("mGrey", ARROW), ("mGold", GOLD),
                          ("mPurple", PURPLE), ("mCu", CU1)):
        defs.append(marker(ident, colour))
    for a in assets.values():
        if a.get("defs"):
            defs.append(a["defs"])
        if a.get("css"):
            css.append(a["css"])

    css.append(phase("phPar", 6.2, 10.8))
    css.append(phase("phEnd", 10.6, 12.0))
    css.append(phase("phHold", 10.4, 12.0))
    css.append("@keyframes wane{0%%,%.2f%%{opacity:1}%.2f%%,100%%"
               "{opacity:.20}}.wane{animation:wane %.1fs linear infinite}"
               % (pc(8.8), pc(10.4), T))
    css.append(".tok{opacity:0}")
    css.append(".paused *,.paused{animation-play-state:paused!important}")
    for name, key, t0, t1 in TRAVELS:
        css.append(travel(name, key, t0, t1))
    css.append("@media(prefers-reduced-motion:reduce){"
               "*{animation:none!important}"
               ".tok,.o2{opacity:0}"
               ".phPar,.phEnd,.phHold{opacity:1}.wane{opacity:.20}"
               ".g0,.g1,.g2,.g3,.g4,.g5,.g6,.g7,.g8,.g9,.g10,.g11,.g12,"
               ".g13{opacity:0}"
               ".tetFill{transform:scale(.94)}.auFill{transform:scale(.92)}"
               ".arcPar{opacity:1}}")

    add('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d"'
        ' width="100%%" height="100%%" preserveAspectRatio="xMidYMid meet"'
        ' role="img" aria-labelledby="figTitle figDesc">' % (W, H))
    add('<title id="figTitle">%s</title>' % esc(TITLE))
    add('<desc id="figDesc">%s</desc>' % esc(DESC))
    add("<defs>%s</defs>" % "".join(defs))
    add("<style>%s</style>" % "".join(css))
    add('<rect width="%d" height="%d" fill="%s"/>' % (W, H, BG))

    def put(key):
        a = assets[key]
        x, y = PLACE[key]
        return ('<g id="%s" transform="translate(%d,%d)">%s</g>'
                % (key, x, y, a["body"]))

    add(put("title"))

    # ---- routes, under the assets so nothing is ever crossed out --------
    add('<g id="routes">')
    add('<g class="wane">%s</g>'
        % route("gold", TINT_GOLD, THIN, "mGold"))
    add(route("cuin", TINT_CU, THIN, "mCu"))
    add(route("feed", TINT_PUR, HEAVY, "mPurple"))
    add(route("tetout", TINT_PUR, HEAVY, "mPurple"))
    add('<g class="phPar">')
    add(route("feed", PURPLE, HEAVY, "mPurple"))
    add(route("tetout", PURPLE, HEAVY, "mPurple"))
    add("</g></g>")

    add(put("vessel"))
    add(put("cycle"))
    add(put("gold"))
    add(put("tet"))

    # ---- the whole composition text budget: five runs -------------------
    add('<g id="labels">')
    add(text(850, 272, "Oxygen dissolves a little gold", 20, MUTED,
             "middle"))
    add(text(1300, 442, "DISSOLVED GOLD", 22, INK, "middle", weight=700,
             ls=".06em"))
    add(text(700, 404, "Cu(II) destroys most of the thiosulfate", 20, MUTED,
             "middle"))
    # the ring had no name, so a reader could only guess what it was. This
    # says what the site does, in the fewest characters that can say it.
    add(text(JUNCTION[0], JUNCTION[1] + 38,
             "S₂O₃²⁻ → S₄O₆"
             "²⁻", 18, PURPLE, "middle", weight=700))
    add(text(1310, 710, "TETRATHIONATE", 22, INK, "middle", weight=700,
             ls=".06em"))
    add(text(770, 786, "Copper comes back. Thiosulfate does not.", 21,
             "#9c4a2f", "middle", weight=700, ls=".03em"))
    add("</g>")

    add('<g id="conclusion" class="phEnd">')
    add(text(1010, 212, "THE LEACHANT RUNS OUT FIRST", 30, INK, "middle",
             weight=700, ls=".08em"))
    add("</g>")

    # ---- travelling species ---------------------------------------------
    add('<g id="carriers">')
    add(token("gold", "tkAu",
              '<circle r="10" fill="%s"/><circle r="16" fill="none"'
              ' stroke="%s" stroke-width="3"/>' % (GOLD, TEAL)))
    add(token("cuin", "tkCuIn", '<circle r="9" fill="%s"/>' % CU1))
    add(token("o2arc", "tkO2",
              '<circle cx="-5" r="6.5" fill="none" stroke="%s"'
              ' stroke-width="3"/><circle cx="5" r="6.5" fill="none"'
              ' stroke="%s" stroke-width="3"/>' % (BLUE, BLUE)))
    for cls, dy in (("tkFeedA", -10), ("tkFeedB", 10), ("tkFeedC", -10),
                    ("tkFeedD", 10)):
        add(token("feed", cls,
                  '<circle cy="%d" r="8" fill="%s"/>' % (dy, TEAL)))
    for cls in ("tkTetA", "tkTetB", "tkTetC"):
        # tetrathionate is two thiosulfates welded together, and is drawn so
        add(token("tetout", cls,
                  '<circle cx="-7" r="8.5" fill="%s"/>'
                  '<circle cx="7" r="8.5" fill="%s"/>' % (PURPLE, PURPLE)))
    add("</g>")

    add(put("timeline"))
    add('<script type="text/javascript"><![CDATA[%s]]></script>' % SCRIPT)
    add("</svg>")
    return "".join(parts)


def main():
    p = OUT / "leaching-budget.svg"
    p.write_text(render(), encoding="utf-8")
    print("wrote %s  %d bytes" % (p.name, p.stat().st_size))


if __name__ == "__main__":
    main()
