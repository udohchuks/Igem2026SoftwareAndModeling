"""Remove the painted checkerboard from the concept illustrations.

The generator drew a checkerboard instead of writing an alpha channel, so the
files arrive as RGB with the pattern baked into the pixels. This finds the
grey checker tones, keeps only the run of them that touches the image border,
and turns that region into real transparency. Grey inside the subject is
enclosed, so it is never reached and never removed.

Run from the repository root:
    python docs/media/wiki/concepts/strip_checkerboard.py
"""

import glob
import os

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
WEB_PX = 840          # 2x the 420 px the overview SVG draws them at
SAT_TOL = 22          # max channel spread still counted as neutral grey
TONE_TOL = 26         # how far from a checker tone still counts


def checker_tones(rgb):
    """The two dominant neutral greys along the border."""
    border = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
    spread = border.max(axis=1).astype(int) - border.min(axis=1).astype(int)
    grey = border[spread <= SAT_TOL].mean(axis=1)
    if grey.size == 0:
        return []
    hist, edges = np.histogram(grey, bins=64, range=(0, 255))
    centres = (edges[:-1] + edges[1:]) / 2
    top = centres[np.argsort(hist)[::-1][:2]]
    return sorted(float(t) for t in top)


def strip(path):
    im = Image.open(path).convert("RGB")
    rgb = np.asarray(im).astype(np.int16)

    tones = checker_tones(rgb)
    if not tones:
        return None

    spread = rgb.max(axis=2) - rgb.min(axis=2)
    value = rgb.mean(axis=2)
    neutral = spread <= SAT_TOL
    # One band spanning both checker tones, not two windows around them. The
    # squares meet in anti-aliased mid-greys that a two-window test misses,
    # and those leftovers read as a faint grid over the page.
    lo = min(tones) - TONE_TOL
    hi = max(tones) + TONE_TOL
    candidate = neutral & (value >= lo) & (value <= hi)

    # keep only the connected region that reaches the border
    labels, n = ndimage.label(candidate)
    if n == 0:
        return None
    edge_ids = set(labels[0]) | set(labels[-1]) | set(labels[:, 0]) | set(labels[:, -1])
    edge_ids.discard(0)
    background = np.isin(labels, list(edge_ids))

    alpha = np.where(background, 0, 255).astype(np.uint8)
    # close single-pixel holes the checker left inside the subject outline
    alpha = np.asarray(
        Image.fromarray(alpha).filter(ImageFilter.MaxFilter(3))
        .filter(ImageFilter.MinFilter(3))
    )

    out = np.dstack([np.asarray(im), alpha])
    full = Image.fromarray(out, "RGBA")

    stem = os.path.basename(path).replace("-approved.png", "")
    full_path = os.path.join(HERE, stem + "-alpha.png")
    full.save(full_path, optimize=True)

    web = full.resize((WEB_PX, WEB_PX), Image.LANCZOS)
    web_path = os.path.join(HERE, stem + "-web.png")
    web.save(web_path, optimize=True)

    removed = 100.0 * background.mean()
    return stem, tones, removed, full_path, web_path


if __name__ == "__main__":
    for src in sorted(glob.glob(os.path.join(HERE, "*-approved.png"))):
        result = strip(src)
        if result is None:
            print("no checker found:", os.path.basename(src))
            continue
        stem, tones, removed, full_path, web_path = result
        print("%-34s tones %s  background %5.1f%%  web %6.0f kB"
              % (stem,
                 " ".join("%.0f" % t for t in tones),
                 removed,
                 os.path.getsize(web_path) / 1024))
