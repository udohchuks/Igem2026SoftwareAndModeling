"""Export model trajectories for the dashboard prototype.

Reads the leach model, runs every ligand scenario at the operating point in
params/leach.yaml, and writes runs.json plus runs.js beside this file.

This is a build script for a prototype, not part of the model. It adds no
number of its own: every value below comes from src/ or params/.
Regenerate with:  python dashboard-prototype/export_runs.py
"""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import leach, params  # noqa: E402

STRIDE = 8          # keep every 8th solver point, so the file stays small
SERIES = ["pH", "titrant", "O2_diss", "Au_complex", "gold_recovered",
          "Cu_II", "S2O3", "S4O6"]
SERIES_S2 = ["S4O6", "S2O3"]


def thin(a):
    a = np.asarray(a, dtype=float)
    keep = a[::STRIDE]
    if keep[-1] != a[-1]:
        keep = np.append(keep, a[-1])
    return [round(float(v), 6) for v in keep]


def one(label, name, eps_gly=None):
    p, r = leach.run_scenario(name, eps_gly=eps_gly, n=2001)
    tr = r["traj"]
    # Stage 2 shares the operating point but has no proton balance, so it
    # carries no titrant series. The console says so rather than inventing one.
    seq = leach.simulate_sequential(p, n=2001)
    s2 = seq["stage2"]
    return label, {
        "stage2": {
            "t_min": thin(s2["t"]),
            "series": {k: thin(s2[k]) for k in SERIES_S2},
            "t_end_min": float(s2["t"][-1]),
            "S4O6_start": round(float(s2["S4O6"][0]), 1),
            "S4O6_end": round(float(s2["S4O6"][-1]), 1),
            "S2O3_start": round(float(s2["S2O3"][0]), 1),
            "S2O3_end": round(float(s2["S2O3"][-1]), 1),
            "conversion_pct": round(
                100.0 * (1.0 - float(s2["S4O6"][-1]) / float(s2["S4O6"][0])), 2),
        },
        "label": label,
        "scenario": name,
        "eps_gly": eps_gly,
        "t_min": thin(tr["t"]),
        "series": {k: thin(tr[k]) for k in SERIES},
        "summary": {
            "gold_24h_pct": round(r["gold_24h"], 3),
            "gold_72h_pct": round(r["gold_72h"], 3),
            "titrant_umol_per_L": round(r["titrant"], 1),
            "Au_feed_24h_uM": round(r["Au_feed_24h"], 4),
            "Cu_II_peak_uM": round(r["Cu_II_peak"], 3),
            "S2O3_end_uM": round(r["S2O3_end"], 1),
        },
        "operating_point": {
            "pH_set": float(p["pH_set"]),
            "pH_control": bool(p["pH_control"]),
            "kLa": float(p["kLa"]),
            "C_star": float(p["C_star"]),
            "t_end_min": float(tr["t"][-1]),
        },
    }


def load_yaml(name):
    """A prototype file beside this script. Not params/, not an authority."""
    import yaml
    here = Path(__file__).resolve().parent
    return yaml.safe_load((here / name).read_text(encoding="utf-8"))


def main():
    lo, mid, hi = leach.eps_gly_band()
    stage_ph = load_yaml("stage_ph.yaml")
    sensors = load_yaml("sensors.yaml")
    runs = dict([
        one("Glycine, mid", "glycine", mid),
        one("Glycine, low", "glycine", lo),
        one("Glycine, high", "glycine", hi),
        one("Ammonia, reference only", "ammonia"),
    ])

    out = {
        "generated_by": "dashboard-prototype/export_runs.py",
        "source": "src/leach.py run_scenario, params/leach.yaml",
        "pH_window": {"floor": 9.3, "ceiling": 10.5,
                      "recommended": [10.0, 10.3]},
        "eps_gly_band": [lo, mid, hi],
        "stage_ph": stage_ph,
        "sensors": sensors,
        "runs": runs,
        "default_run": "Glycine, mid",
    }

    here = Path(__file__).resolve().parent
    dest = here / "runs.json"
    dest.write_text(json.dumps(out, indent=1), encoding="utf-8")

    # Same payload as a script, because the dashboard page loads it with a
    # <script> tag rather than fetch().
    js = here / "runs.js"
    payload = json.dumps(out, separators=(",", ":"))
    js.write_text("window.RUNS = " + payload + ";" + chr(10), encoding="utf-8")

    print("wrote %s  %.1f kB  %d runs"
          % (dest.name, dest.stat().st_size / 1024.0, len(runs)))
    print("wrote %s  %.1f kB" % (js.name, js.stat().st_size / 1024.0))
    for k, v in runs.items():
        s = v["summary"]
        print("  %-26s gold72 %6.2f %%   titrant %10.1f umol/L   stage2 %5.2f %%"
              % (k, s["gold_72h_pct"], s["titrant_umol_per_L"],
                 v["stage2"]["conversion_pct"]))
    live = [c["key"] for c in sensors["channels"] if c["feed"] != "none"]
    nofeed = [c["key"] for c in sensors["channels"] if c["feed"] == "none"]
    print("  channels live   : %s" % ", ".join(live))
    print("  channels no feed: %s" % ", ".join(nofeed))
    print("  not measurable  : %s" % ", ".join(
        n["key"] for n in sensors["not_measurable"]))
    runnable = [s["key"] for s in stage_ph["stages"] if s["runnable"]]
    blocked = [s["key"] for s in stage_ph["stages"] if not s["runnable"]]
    print("  stages runnable: %s" % ", ".join(runnable))
    print("  stages blocked : %s" % ", ".join(blocked))


if __name__ == "__main__":
    main()
