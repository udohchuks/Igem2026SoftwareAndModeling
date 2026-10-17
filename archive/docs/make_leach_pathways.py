"""Build the leaching competing-pathways figure, desktop and mobile.

A timed run on a 15 s clock. Thiosulfate markers leave the vessel. One
reaches gold. Nine meet Cu(II) and leave as tetrathionate. When the last
marker is spent the routes grey out and nothing moves until the clock
resets.

The topology follows the balanced reactions in docs/MASTER.md and the
balances in docs/EQUATIONS.md:

    4 Cu(0) + O2 + 8 S2O3(2-) + 2 H2O ->  4 [Cu(S2O3)2](3-) + 4 OH(-)   O2 route
    Cu(0) + Cu(2+) + 4 S2O3(2-)       ->  2 [Cu(S2O3)2](3-)   comproportionating
    4 Cu(I) + O2 + 2 H2O              ->  4 Cu(II) + 4 OH(-)   re-oxidation, v4
    2 Cu(II) + 2 S2O3(2-)             ->  2 Cu(I) + S4O6(2-)   parasitic, v3

Copper is not fed in. It comes off the board as Cu(0) and dissolves as Cu(I)
on both routes, so v_4 is the only source of Cu(II) anywhere in the model
(MASTER.md, "The copper loop, which decides the whole stage"). Cu(II) is a
reactant of the parasitic step and not its product: it is consumed there and
returned as Cu(I), so it is drawn entering and leaving the thiosulfate arrow
rather than sitting on it. The share of the thiosulfate each
sink takes is MASTER.md's table: gold 0.06 %, copper metal 1.7 %,
parasitic 98.2 %; the figure states that lopsidedness in words rather than
in numbers. Fragment dissolution tracks the 28.5 % gold recovery at 72 h,
so two fragments of seven go.

Writes both files under docs/media/wiki/concepts/.
"""
from pathlib import Path

T = 15.0                      # master clock, seconds
RESET = 14.3                  # everything restores between here and T
STOP = 12.6                   # last marker has landed; the process halts

GOLD, COPPER, TEAL, VIOLET = "#b98524", "#9a6040", "#2d9297", "#8d73a8"
DEAD = "#d5d5d1"

# emit time, route, transit seconds. One gold against nine parasitic; the
# true ratio is about one in sixteen hundred, so the shares are labelled.
TOKENS = ([(1.0, "gold", 2.0)]
          + [(1.0 + 0.9 * i, "waste", 3.4) for i in range(1, 10)])

GOLD_ARRIVAL = TOKENS[0][0] + TOKENS[0][2]
WASTE_ARRIVALS = [e + d for e, r, d in TOKENS if r == "waste"]

# seven fragments, two dissolve: 28.6 %, against the model's 28.5 % at 72 h
DISSOLVED = {1: 4.2, 4: 8.4}
N_FRAGMENTS = 7

# The figure states the process, not the shares. The model's split is steeply
# lopsided, so the two routes carry the weight visually and in words instead.
SHARE_GOLD = "a trace of the leachant"
SHARE_WASTE = "nearly all of the leachant"
FOOTER = ("Ammonia-free run. Oxygen dissolves the gold. Cu(II) takes almost all of the "
          "thiosulfate and oxygen keeps rebuilding it, so the leachant runs out first.")
FOOTER_MOBILE = "Ammonia-free. Cu(II) takes almost all the thiosulfate."


def pc(t):
    """Seconds on the master clock as a keyframe percentage."""
    return "%.3f%%" % (max(0.0, min(t, T)) / T * 100.0)


def fragment(cx, cy, s=1.0):
    pts = [(cx - 11 * s, cy - 5 * s), (cx + 1 * s, cy - 8 * s), (cx + 11 * s, cy - 3 * s),
           (cx + 8 * s, cy + 7 * s), (cx - 4 * s, cy + 8 * s), (cx - 11 * s, cy + 3 * s)]
    return " ".join("%.1f,%.1f" % p for p in pts)


def keyframes(waste_step, bar_width):
    kf = []
    for i, (emit, _route, dur) in enumerate(TOKENS):
        end = emit + dur
        kf.append("@keyframes mv%d{0%%,%s{offset-distance:0%%}%s,100%%{offset-distance:100%%}}"
                  % (i, pc(emit), pc(end)))
        kf.append("@keyframes fd%d{0%%,%s{opacity:0}%s,%s{opacity:1}%s,100%%{opacity:0}}"
                  % (i, pc(emit), pc(emit + 0.12), pc(end - 0.12), pc(end)))
        kf.append("@keyframes st%d{0%%,%s{opacity:1}%s,%s{opacity:.10}100%%{opacity:1}}"
                  % (i, pc(emit - 0.10), pc(emit + 0.20), pc(RESET)))
    for i, gone in DISSOLVED.items():
        kf.append("@keyframes fr%d{0%%,%s{opacity:1}%s,%s{opacity:0}100%%{opacity:1}}"
                  % (i, pc(gone - 0.25), pc(gone + 0.25), pc(RESET)))
    # the single grain of gold, and the tetrathionate meter
    kf.append("@keyframes grain{0%%,%s{opacity:0;transform:scale(.4)}%s,%s"
              "{opacity:1;transform:scale(1)}100%%{opacity:0;transform:scale(.4)}}"
              % (pc(GOLD_ARRIVAL), pc(GOLD_ARRIVAL + 0.3), pc(RESET)))
    frames = ["0%%,%s{transform:translateY(0)}" % pc(WASTE_ARRIVALS[0] - 0.20)]
    for n, t in enumerate(WASTE_ARRIVALS, start=1):
        nxt = WASTE_ARRIVALS[n] - 0.20 if n < len(WASTE_ARRIVALS) else RESET
        frames.append("%s,%s{transform:translateY(%.2fpx)}" % (pc(t), pc(nxt), -waste_step * n))
    frames.append("100%{transform:translateY(0)}")
    kf.append("@keyframes mWaste{%s}" % "".join(frames))

    kf.append("@keyframes halt{0%%,%s{opacity:0}%s,%s{opacity:1}100%%{opacity:0}}"
              % (pc(STOP), pc(STOP + 0.25), pc(RESET)))
    for tag, col in (("g", GOLD), ("c", COPPER), ("v", VIOLET)):
        kf.append("@keyframes dim%s{0%%,%s{stroke:%s}%s,%s{stroke:%s}100%%{stroke:%s}}"
                  % (tag, pc(STOP), col, pc(STOP + 0.25), pc(RESET), DEAD, col))
        kf.append("@keyframes fil%s{0%%,%s{fill:%s}%s,%s{fill:%s}100%%{fill:%s}}"
                  % (tag, pc(STOP), col, pc(STOP + 0.25), pc(RESET), DEAD, col))
    kf.append("@keyframes vessel{0%%,%s{opacity:1}%s,%s{opacity:.5}100%%{opacity:1}}"
              % (pc(STOP), pc(STOP + 0.25), pc(RESET)))
    kf.append("@keyframes sweep{0%{transform:scaleX(0)}100%{transform:scaleX(1)}}")
    kf.append("@keyframes head{0%%{transform:translateX(0)}100%%{transform:translateX(%dpx)}}"
              % bar_width)
    kf.append("@keyframes barcol{0%%,%s{fill:%s}%s,100%%{fill:#c6c6c2}}"
              % (pc(STOP), TEAL, pc(STOP + 0.25)))
    return "".join(kf)


def stylesheet(waste_step, bar_width, fonts):
    S = []
    S.append('.eyebrow{font:700 %dpx Inter,Segoe UI,sans-serif;letter-spacing:.09em;'
             'text-transform:uppercase;fill:#74746f}' % fonts["eyebrow"])
    S.append('.heading{font:500 %dpx Georgia,serif;fill:#252523}' % fonts["heading"])
    S.append('.label{font:700 %dpx Inter,Segoe UI,sans-serif;fill:#252523}' % fonts["label"])
    S.append('.copy{font:400 %dpx Inter,Segoe UI,sans-serif;fill:#74746f}' % fonts["copy"])
    S.append('.tiny{font:400 %dpx Inter,Segoe UI,sans-serif;fill:#8b8b85}' % fonts["tiny"])
    S.append('.route{fill:none;stroke-linecap:round}')
    S.append('.an,.ar{animation-duration:%gs;animation-iteration-count:infinite;'
             'animation-timing-function:linear}' % T)
    S.append('.tk{offset-rotate:0deg}')
    for i in range(len(TOKENS)):
        S.append('.tk%d{animation-name:mv%d,fd%d}.sk%d{animation-name:st%d}'
                 % (i, i, i, i, i))
    for i in DISSOLVED:
        S.append('.fr%d{animation-name:fr%d}' % (i, i))
    S.append('.grain{opacity:0;transform-box:fill-box;transform-origin:center;'
             'animation-name:grain}')
    S.append('.meterW{transform-box:fill-box;animation-name:mWaste}')
    S.append('.rg{animation-name:dimg}.rc{animation-name:dimc}.rv{animation-name:dimv}')
    S.append('.filg{animation-name:filg}.filc{animation-name:filc}.filv{animation-name:filv}')
    S.append('.halt{opacity:0;animation-name:halt}')
    S.append('.vessel{animation-name:vessel}')
    S.append('.sweep{transform-box:fill-box;transform-origin:left center;'
             'animation-name:sweep,barcol}')
    S.append('.head{animation-name:head}')
    S.append(keyframes(waste_step, bar_width))
    # a still that reads as the finished run, for readers who ask for less motion
    S.append('@media(prefers-reduced-motion:reduce){'
             '.an,.ar{animation:none}'
             '.tk{display:none}'
             '.grain{opacity:1;transform:scale(1)}'
             '.meterW{transform:translateY(-%.2fpx)}'
             '.fr1,.fr4{opacity:0}'
             '.halt{opacity:1}'
             '.stock{opacity:.10}'
             '.route{stroke:%s}.ar{fill:%s}'
             '.vessel{opacity:.5}'
             '.sweep{transform:scaleX(1);fill:#c6c6c2}'
             '.head{transform:translateX(%dpx)}'
             '}' % (waste_step * len(WASTE_ARRIVALS), DEAD, DEAD, bar_width))
    return "".join(S)


def head(w, h, waste_c, waste_r, waste_step, bar_width, fonts):
    A = []
    A.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" '
             'aria-labelledby="ttl dsc">' % (w, h))
    A.append('<title id="ttl">Thiosulfate is a finite reaction budget</title>')
    A.append('<desc id="dsc">A timed run. Thiosulfate markers leave a vessel of crushed '
             'circuit-board fragments. Oxygen oxidises the gold, and the marker leaves as the '
             'gold thiosulfate complex; only a trace of the leachant takes that route. Nearly '
             'all of it meets copper two, which converts it to tetrathionate and is itself '
             'rebuilt from copper one by oxygen, so the loop keeps spending the budget. Two '
             'fragments of seven dissolve. When the last marker is spent the routes grey out '
             'and the run halts with gold still on the remaining fragments. A bar along the '
             'bottom tracks the cycle and its restart.</desc>')
    A.append('<defs>')
    A.append('<linearGradient id="liquor" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#e6f4f4"/>'
             '<stop offset="1" stop-color="#bfe1e1"/></linearGradient>')
    A.append('<clipPath id="clipWaste"><circle cx="%d" cy="%d" r="%d"/></clipPath>'
             % (waste_c[0], waste_c[1], waste_r - 2))
    for tag, key, col in (("Gold", "g", GOLD), ("Copper", "c", COPPER), ("Violet", "v", VIOLET)):
        # userSpaceOnUse keeps the head one size on a 2 px dash and a 7 px route alike
        A.append('<marker id="a%s" markerUnits="userSpaceOnUse" markerWidth="11" '
                 'markerHeight="11" refX="9.5" refY="5.5" orient="auto">'
                 '<path class="ar fil%s" d="M0 0L11 5.5L0 11Z" fill="%s"/></marker>'
                 % (tag, key, col))
    A.append('<style>%s</style></defs>' % stylesheet(waste_step, bar_width, fonts))
    A.append('<rect width="%d" height="%d" fill="#fbfbfa"/>' % (w, h))
    return A


def vessel(A, x, y, w, h, frags, stock, fs, dot_r, cap_y, halt_y, fonts):
    A.append('<g class="an vessel">')
    A.append('<rect x="%d" y="%d" width="%d" height="%d" rx="18" fill="url(#liquor)" '
             'stroke="#9fc9c9"/>' % (x, y, w, h))
    A.append('<path d="M%d %dQ%d %d %d %d" fill="none" stroke="#8dbfbf" stroke-width="1.5"/>'
             % (x, y + 34, x + w // 2, y + 44, x + w, y + 34))
    A.append('</g>')
    A.append('<text x="%d" y="%d" class="label" style="fill:#1f6f73">'
             'S&#8322;O&#8323;&#178;&#8315;</text>' % (x + 16, y + 26))
    for i, (cx, cy) in enumerate(stock):
        A.append('<circle class="stock an sk%d" cx="%d" cy="%d" r="%s" fill="%s" '
                 'stroke="#eef7f6" stroke-width="1.2"/>' % (i, cx, cy, dot_r, TEAL))
    for i, (cx, cy) in enumerate(frags):
        cls = ' class="an fr%d"' % i if i in DISSOLVED else ''
        A.append('<g%s>' % cls)
        A.append('<polygon points="%s" fill="#2f5a44"/>' % fragment(cx, cy, fs))
        A.append('<circle cx="%.1f" cy="%d" r="%.1f" fill="#d5ae47"/>'
                 % (cx + fs, cy, 2.8 * fs))
        if i not in DISSOLVED:
            A.append('<circle class="an halt" cx="%.1f" cy="%d" r="%.1f" fill="none" '
                     'stroke="%s" stroke-width="1.5"/>' % (cx + fs, cy, 7.0 * fs, GOLD))
        A.append('</g>')
    A.append('<text x="%d" y="%d" text-anchor="middle" class="copy">'
             'Crushed PCB fragments</text>' % (x + w // 2, cap_y))
    A.append('<text x="%d" y="%d" text-anchor="middle" class="tiny an halt" '
             'style="fill:#8a6b28">Gold still on the board</text>'
             % (x + w // 2, halt_y))


def outcome_waste(A, c, r, step, n):
    cx, cy = c
    A.append('<circle cx="%d" cy="%d" r="%d" fill="#f7f3fa" stroke="#cfbddb" stroke-width="2"/>'
             % (cx, cy, r))
    A.append('<g clip-path="url(#clipWaste)"><rect class="an meterW" x="%d" y="%d" width="%d" '
             'height="%d" fill="#c8b4d8" opacity=".9"/></g>'
             % (cx - r, cy + r, 2 * r, 2 * r + step * n + 6))
    A.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="#cfbddb" stroke-width="2"/>'
             % (cx, cy, r))


def scrubber(A, x, y, width, tiny_y, caption_y, caption,
             right_label="Thiosulfate exhausted &#183; run halts", right_anchor=False):
    A.append('<rect x="%d" y="%d" width="%d" height="6" rx="3" fill="#ececea"/>'
             % (x, y, width))
    A.append('<rect class="an sweep" x="%d" y="%d" width="%d" height="6" rx="3" fill="%s"/>'
             % (x, y, width, TEAL))
    tick = x + width * STOP / T
    A.append('<path d="M%.1f %dV%d" stroke="#c6c6c2"/>' % (tick, y - 6, y + 12))
    A.append('<circle class="an head" cx="%d" cy="%d" r="5" fill="#fbfbfa" stroke="#8b8b85" '
             'stroke-width="1.6"/>' % (x, y + 3))
    A.append('<text x="%d" y="%d" class="tiny">Leaching</text>' % (x, tiny_y))
    if right_anchor:
        A.append('<text x="%d" y="%d" text-anchor="end" class="tiny">%s</text>'
                 % (x + width, tiny_y, right_label))
    else:
        A.append('<text x="%.1f" y="%d" class="tiny">%s</text>' % (tick + 6, tiny_y, right_label))
    A.append('<text x="%d" y="%d" class="copy">%s</text>' % (x, caption_y, caption))


def tokens(A, gold_path, waste_path, r):
    for i, (_e, route, _d) in enumerate(TOKENS):
        d = gold_path if route == "gold" else waste_path
        A.append('<circle class="tk tk%d an" r="%s" fill="%s" stroke="#fbfbfa" '
                 'stroke-width="1.4" style="offset-path:path(\'%s\')"/>' % (i, r, TEAL, d))


# ------------------------------------------------------------------ desktop
def desktop():
    waste_c, waste_r = (760, 340), 40
    waste_step = (2 * waste_r - 4) * 0.98 / len(WASTE_ARRIVALS)
    fonts = dict(eyebrow=11, heading=21, label=13, copy=12, tiny=11)
    A = head(900, 620, waste_c, waste_r, waste_step, 836, fonts)

    A.append('<text x="32" y="38" class="eyebrow">Inside the leaching vessel</text>')
    A.append('<text x="32" y="69" class="heading">Thiosulfate is a finite reaction budget</text>')
    A.append('<path d="M32 90H868" stroke="#e7e7e3"/>')

    A.append('<text x="42" y="112" class="eyebrow">Thiosulfate '
             '&#183; controlled air</text>')
    frags = [(70, 178), (120, 170), (175, 180), (225, 172),
             (95, 222), (150, 226), (210, 222)]
    stock = [(52, 202), (98, 196), (148, 200), (198, 200), (240, 196),
             (62, 250), (112, 252), (162, 252), (212, 250), (242, 230)]
    vessel(A, 40, 118, 210, 150, frags, stock, 0.78, "4", 292, 310, fonts)

    # the desired route: oxygen is the oxidant in the ammonia-free run
    A.append('<text x="330" y="128" class="eyebrow" style="fill:#94691e">Desired reaction</text>')
    A.append('<path d="M250 168C330 142 440 134 556 148" class="route an rg" stroke="%s" '
             'stroke-width="3" marker-end="url(#aGold)"/>' % GOLD)
    A.append('<text x="322" y="190" class="tiny">O&#8322; oxidises the gold</text>')
    A.append('<circle cx="604" cy="158" r="42" fill="#fdf8ea" stroke="#e3cd91" stroke-width="2"/>')
    A.append('<circle class="grain an" cx="604" cy="158" r="13" fill="#d5ae47"/>')
    A.append('<text x="656" y="150" class="label">Dissolved gold</text>')
    A.append('<text x="656" y="168" class="copy">Au(S&#8322;O&#8323;)&#8322;&#179;&#8315;</text>')
    A.append('<text x="656" y="186" class="tiny" style="fill:#8a6b28">%s</text>' % SHARE_GOLD)

    # the competing route: thiosulfate goes straight to tetrathionate
    A.append('<path d="M250 240C360 280 460 316 700 336" class="route an rv" stroke="%s" '
             'stroke-width="7" marker-end="url(#aViolet)"/>' % VIOLET)
    A.append('<text x="470" y="284" class="eyebrow" style="fill:#755a8a">Competing reaction</text>')
    A.append('<text x="470" y="300" class="tiny" style="fill:#755a8a">%s</text>' % SHARE_WASTE)
    outcome_waste(A, waste_c, waste_r, waste_step, len(WASTE_ARRIVALS))
    A.append('<text x="760" y="345" text-anchor="middle" class="label" '
             'style="fill:#3f2f4f">S&#8324;O&#8326;&#178;&#8315;</text>')
    A.append('<text x="760" y="400" text-anchor="middle" class="copy">tetrathionate</text>')

    # copper comes off the board as Cu(0) and dissolves as Cu(I)
    A.append('<path d="M250 264C312 324 372 398 436 430" class="route an rc" stroke="%s" '
             'stroke-width="2.5" marker-end="url(#aCopper)"/>' % COPPER)
    A.append('<text x="430" y="478" text-anchor="end" class="tiny">Cu&#8304; off the board, '
             'dissolving as Cu(I)</text>')
    for cx, txt in ((470, "Cu(I)"), (620, "Cu(II)")):
        A.append('<circle cx="%d" cy="440" r="28" fill="#f4e8e0" stroke="#d3aa91" '
                 'stroke-width="2"/>' % cx)
        A.append('<text x="%d" y="445" text-anchor="middle" class="label" '
                 'style="fill:#8a5738">%s</text>' % (cx, txt))

    # Cu(II) is spent at the thiosulfate arrow and handed back as Cu(I)
    A.append('<path d="M620 412C606 376 592 346 570 334C548 346 500 400 480 424" '
             'class="route an rc" stroke="%s" stroke-width="2.5" '
             'marker-end="url(#aCopper)"/>' % COPPER)
    A.append('<path d="M478 468C520 496 570 496 612 468" class="route an rc" stroke="%s" '
             'stroke-width="2.5" marker-end="url(#aCopper)"/>' % COPPER)
    A.append('<text x="545" y="524" text-anchor="middle" class="copy">'
             'O&#8322; re-oxidises Cu(I), the only source of Cu(II)</text>')

    tokens(A, "M250 168C330 142 440 134 562 150",
           "M250 240C360 280 460 316 706 336", "6")

    scrubber(A, 32, 552, 836, 580, 602, FOOTER)
    A.append('</svg>')
    return "\n".join(A)


# ------------------------------------------------------------------- mobile
def mobile():
    waste_c, waste_r = (316, 596), 36
    waste_step = (2 * waste_r - 4) * 0.98 / len(WASTE_ARRIVALS)
    fonts = dict(eyebrow=10, heading=18, label=12, copy=11, tiny=10)
    A = head(420, 760, waste_c, waste_r, waste_step, 372, fonts)

    A.append('<text x="24" y="30" class="eyebrow">Inside the leaching vessel</text>')
    A.append('<text x="24" y="56" class="heading">Thiosulfate is a finite budget</text>')
    A.append('<path d="M24 70H396" stroke="#e7e7e3"/>')

    A.append('<text x="110" y="86" class="eyebrow">Thiosulfate &#183; air</text>')
    frags = [(140, 152), (185, 144), (235, 154), (275, 146),
             (160, 194), (215, 198), (265, 192)]
    stock = [(122, 176), (168, 172), (208, 176), (252, 170), (292, 176),
             (128, 206), (186, 214), (240, 214), (292, 204), (296, 148)]
    vessel(A, 110, 96, 200, 128, frags, stock, 0.70, "3.6", 244, 260, fonts)

    A.append('<text x="24" y="292" class="eyebrow" style="fill:#94691e">Desired</text>')
    A.append('<path d="M110 190C76 214 66 244 70 278" class="route an rg" stroke="%s" '
             'stroke-width="2.5" marker-end="url(#aGold)"/>' % GOLD)
    A.append('<circle cx="76" cy="330" r="34" fill="#fdf8ea" stroke="#e3cd91" stroke-width="2"/>')
    A.append('<circle class="grain an" cx="76" cy="330" r="11" fill="#d5ae47"/>')
    A.append('<text x="76" y="384" text-anchor="middle" class="label">Dissolved gold</text>')
    A.append('<text x="76" y="399" text-anchor="middle" class="copy">'
             'Au(S&#8322;O&#8323;)&#8322;&#179;&#8315;</text>')
    A.append('<text x="76" y="414" text-anchor="middle" class="tiny" '
             'style="fill:#8a6b28">%s</text>' % SHARE_GOLD)
    A.append('<text x="76" y="429" text-anchor="middle" class="tiny">'
             'O&#8322; oxidises the gold</text>')

    # thiosulfate runs straight to tetrathionate down the right
    A.append('<path d="M290 224C332 300 342 420 324 552" class="route an rv" stroke="%s" '
             'stroke-width="6" marker-end="url(#aViolet)"/>' % VIOLET)
    A.append('<text x="24" y="470" class="eyebrow" style="fill:#755a8a">Competing</text>')
    A.append('<text x="24" y="486" class="tiny" style="fill:#755a8a">%s</text>' % SHARE_WASTE)
    outcome_waste(A, waste_c, waste_r, waste_step, len(WASTE_ARRIVALS))
    A.append('<text x="316" y="601" text-anchor="middle" class="label" '
             'style="fill:#3f2f4f">S&#8324;O&#8326;&#178;&#8315;</text>')
    A.append('<text x="316" y="652" text-anchor="middle" class="copy">tetrathionate</text>')

    # the copper pair, fed by the board's own copper
    for cy, txt in ((450, "Cu(II)"), (560, "Cu(I)")):
        A.append('<circle cx="180" cy="%d" r="26" fill="#f4e8e0" stroke="#d3aa91" '
                 'stroke-width="2"/>' % cy)
        A.append('<text x="180" y="%d" text-anchor="middle" class="label" '
                 'style="fill:#8a5738">%s</text>' % (cy + 4, txt))
    A.append('<path d="M206 438C258 412 304 388 328 372C316 402 262 494 208 540" '
             'class="route an rc" stroke="%s" stroke-width="2.5" '
             'marker-end="url(#aCopper)"/>' % COPPER)
    A.append('<path d="M154 546C114 520 114 480 152 458" class="route an rc" stroke="%s" '
             'stroke-width="2.5" marker-end="url(#aCopper)"/>' % COPPER)
    A.append('<text x="150" y="608" text-anchor="middle" class="tiny">'
             'Cu(I) comes off the board</text>')
    A.append('<text x="150" y="623" text-anchor="middle" class="tiny">'
             'O&#8322; makes every Cu(II)</text>')

    tokens(A, "M110 190C76 214 66 244 72 286",
           "M290 224C332 300 342 420 326 556", "5")

    scrubber(A, 24, 690, 372, 716, 738, FOOTER_MOBILE,
             right_label="Exhausted &#183; halts", right_anchor=True)
    A.append('</svg>')
    return "\n".join(A)


base = Path("docs/media/wiki/concepts")
for name, svg in (("leaching-competing-pathways-v2.svg", desktop()),
                  ("leaching-competing-pathways-v2-mobile.svg", mobile())):
    out = base / name
    out.write_text(svg, encoding="utf-8")
    print("wrote", out, out.stat().st_size, "bytes")
