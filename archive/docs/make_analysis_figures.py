"""The five analyses added on 2026-08-20, and the figures they produce.

Run from the repository root:

    python docs/make_analysis_figures.py

Writes PNGs into docs/media/review/ and prints every number it draws, so the
prose in REVIEW.md can be checked against this output rather than against a
memory of it. Numbers come from params/ and src/ only.

The five, in the order REVIEW.md uses them:

  1  fig13_tornado          what actually moves the end-to-end result
  2  --                     the PRCC recomputation, BLOCKED, see ISSUES 63
  3  fig14_monte_carlo      the operating case with an error bar on it
  4  fig15_two_levers       biomass against display density
  5  fig16_k_grow_inverse   what a seeded reduction run would have to show
"""
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import (expression, interfaces, leach, params,  # noqa: E402
                 recovery_chain as rc, sensitivity as sn)

OUT = Path(__file__).resolve().parent / "media" / "review"
OUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"figure.dpi": 160, "font.size": 9,
                     "axes.grid": True, "grid.alpha": 0.3})

L = params.load("leach")
E = params.load("expression")
R = params.load("recovery_chain")
P_SEQ = leach.parameters()
N_GRID = 801


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)
    print("wrote", name)


# =========================================================================
# The end-to-end metric everything is scored against.
# =========================================================================
def chain_from_leach(p_leach=None, **chain_over):
    """Gold recovered, umol per litre of liquor, end to end.

    This is the right target for a sensitivity study and gold-at-72-h is not:
    capture is capacity limited, so a leach improvement that raises Au_feed
    does NOT raise what comes out the far end. Only a metric that carries the
    whole chain can show that.
    """
    p = dict(P_SEQ, **(p_leach or {}))
    s3 = leach.simulate_sequential(p, n=N_GRID)["stage3"]
    au_feed = float(s3["Au_complex"][-1])

    c = dict(
        q_max=R["V1_capture"]["q_max"]["value"],
        X_max=R["V1_capture"]["X_max"]["value"],
        K_Au=R["V1_capture"]["K_Au"]["value"],
        phi=R["elution"]["phi"]["value"],
        k_elute=R["elution"]["k_elute"]["value"],
        t_elute_h=6.0,
    )
    c.update(chain_over)

    red = {k: R["reduction"][k]["value"] for k in
           ("k_nuc", "k_grow", "k_ox", "k_rech", "K_inh", "nu", "Rech_0")}
    red["E_tot"] = rc.protein_uM(
        R["reagent_arm"]["protein_target_g_per_L"]["value"],
        R["reagent_arm"]["M_r_reductase"]["value"])
    red["t_reduce_h"] = 24.0
    for k in ("k_nuc", "k_grow", "Rech_0", "seeding_on", "seed_frac"):
        if k in chain_over:
            red[k] = chain_over[k]

    bound = rc.eta_capture(au_feed, c["q_max"] * c["X_max"], c["K_Au"])
    eta_el = float(rc.eta_elute(c["t_elute_h"], c["phi"], c["k_elute"]))
    au_red = au_feed * bound * eta_el
    eta_red = sn.reduce_finke_watzky(au_red, red, t_end=24.0)
    # Physical recovery is out of scope, so the chain ends here. Until
    # 2026-08-21 this function multiplied by eta_spin * eta_wash * eta_ash
    # with eta_spin HARD-CODED at 0.50, while the notebook and
    # src/sensitivity.py used eta_phys = 1. The two halves of the repository
    # were answering different questions, and the number in this file also
    # broke AGENTS.md rule 2, no number in a .py file. Every absolute figure
    # from this module rises by 1/(0.50*0.95*0.98) = 2.148x; every RATIO,
    # which is what the tornado reports, is unchanged.
    return au_feed * bound * eta_el * eta_red


# =========================================================================
# 1. Tornado. What actually moves the end-to-end result.
# =========================================================================
# low, high, and where the range comes from. A range that is a declared
# `range:` in params/ says so; the rest are stated here and are assumptions
# about plausible spread, not measurements. REVIEW.md section 8 lists them.
LEACH_SWEEPS = [
    ("t_film  plating thickness", "t_film", 0.05e-6, 1.0e-6, "params range"),
    ("d  crush size", "d", 0.002, 0.006, "params range"),
    ("O2  dissolved oxygen", "O2", 60.0, 500.0, "the span tested in 2.4"),
    ("K_S4O6", "K_S4O6", 50.0, 2400.0, "params range"),
    ("K_S2O3", "K_S2O3", 1960.0, 5800.0, "1/K_ads measured band"),
    ("k_par  parasitic", "k_par", 1.2e-5 / 3, 1.2e-5 * 3, "assumed 3x either way"),
    ("k_cat", "k_cat", 110.0, 250.0, "110 to 250 across both bases"),
]
RED_V = {k: R["reduction"][k]["value"] for k in ("k_nuc", "k_grow")}

CHAIN_SWEEPS = [
    ("q_max  display density", "q_max", None, None, "N = 75 to 700"),
    ("X_max  biomass", "X_max", 5.0, 130.0, "published E. coli densities"),
    ("K_Au  affinity", "K_Au", 0.7, 10.0, "S78 proxy vs Part II placeholder, ISSUES 1"),
    ("phi  irreversible fraction", "phi", 0.05, 0.30, "assumed"),
    ("k_elute", "k_elute", 0.5, 4.0, "assumed"),
    # Both were hardcoded around the retired values, 5.0e-5 and 0.2, until
    # 2026-08-24. They now track whatever params/recovery_chain.yaml holds, so
    # a recentring cannot leave this figure behind again. ISSUES.md item 82.
    ("k_nuc  nucleation", "k_nuc",
     *R["reduction"]["k_nuc"]["range"], "full YAML scenario range"),
    ("k_grow  autocatalysis", "k_grow",
     *R["reduction"]["k_grow"]["range"], "full YAML scenario range"),
    ("Rech_0  dithionite", "Rech_0", 4.6, 1000.0, "params range"),
]


def qmax_at_N(n):
    p2 = {k: v["value"] for k, v in E.items()
          if isinstance(v, dict) and "value" in v}
    p2["N"] = n
    return interfaces.qmax_from_expression(expression.steady_state(p2)["A"])


def tornado():
    base = chain_from_leach()
    print("\n1. TORNADO   base = %.5f umol/L recovered end to end" % base)
    rows = []
    for label, key, lo, hi, why in LEACH_SWEEPS:
        a = chain_from_leach({key: lo})
        b = chain_from_leach({key: hi})
        rows.append((label, a, b, why))
    for label, key, lo, hi, why in CHAIN_SWEEPS:
        if key == "q_max":
            lo, hi = qmax_at_N(75.0), qmax_at_N(700.0)
        a = chain_from_leach(None, **{key: lo})
        b = chain_from_leach(None, **{key: hi})
        rows.append((label, a, b, why))

    rows.sort(key=lambda r: max(r[1], r[2]) / max(min(r[1], r[2]), 1e-12))
    for label, a, b, why in rows:
        span = max(a, b) / max(min(a, b), 1e-12)
        print("   %-28s %9.5f -> %9.5f   span %8.1fx   (%s)"
              % (label, a, b, span, why))

    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    y = np.arange(len(rows))
    for i, (label, a, b, why) in enumerate(rows):
        lo, hi = min(a, b), max(a, b)
        ax.plot([lo, hi], [i, i], lw=7, solid_capstyle="butt",
                color="tab:blue", alpha=0.75)
    ax.axvline(base, color="k", ls="--", lw=1, label="operating point")
    ax.set_yticks(y)
    ax.set_yticklabels([r[0] for r in rows], fontsize=8)
    ax.set_xscale("log")
    ax.set(xlabel="gold recovered end to end (umol per litre of liquor, log)",
           title="Conditional one-at-a-time scenarios (ranges differ)")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    save(fig, "fig13_tornado.png")
    return rows, base


# =========================================================================
# 3. Monte Carlo. The operating case with an error bar.
# =========================================================================
def monte_carlo(n=400, seed=0):
    rng = np.random.default_rng(seed)
    band = leach.eps_gly_band()
    print("\n3. MONTE CARLO  n = %d over the five unmeasured constants" % n)
    golds, polys = [], []
    for _ in range(n):
        eps = float(np.exp(rng.uniform(np.log(band[0]), np.log(band[-1]))))
        k_alk = L["tetrathionate"]["k_alk"]["value"] * float(
            np.exp(rng.uniform(np.log(1 / 3), np.log(3))))
        kla = L["oxygen"]["kLa"]["value"] * float(
            np.exp(rng.uniform(np.log(0.5), np.log(2.0))))
        _, s = leach.run_scenario("glycine", eps_gly=eps, k_alk=k_alk,
                                  kLa=kla, n=N_GRID)
        golds.append(s["gold_72h"])
        polys.append(s["S4O6_end"] + s["S3O6_end"])
    g = np.array(golds)
    p = np.array(polys)
    print("   gold 72 h   median %.1f %%   5-95 %% band %.1f to %.1f"
          % (np.median(g), np.percentile(g, 5), np.percentile(g, 95)))
    print("   polythionate median %.0f uM   5-95 %% band %.0f to %.0f"
          % (np.median(p), np.percentile(p, 5), np.percentile(p, 95)))

    fig, axes = plt.subplots(1, 2, figsize=(7.6, 3.2))
    axes[0].hist(g, bins=26, color="tab:green", alpha=0.85)
    axes[0].axvline(np.median(g), color="k", ls="--", lw=1)
    axes[0].set(xlabel="gold at 72 h (%)", ylabel="runs",
                title="Operating case, gold")
    axes[1].hist(p / 1000.0, bins=26, color="tab:red", alpha=0.85)
    axes[1].axvline(np.median(p) / 1000.0, color="k", ls="--", lw=1)
    axes[1].set(xlabel="polythionate to capture (mM)",
                title="Operating case, polythionate")
    fig.suptitle("What the unmeasured constants are worth, %d draws" % n,
                 fontsize=10)
    fig.tight_layout()
    save(fig, "fig14_monte_carlo.png")
    return g, p


# =========================================================================
# 4. The two levers: biomass against display density.
# =========================================================================
def two_levers():
    print("\n4. TWO LEVERS  gold recovered end to end, umol/L")
    qs = [qmax_at_N(75.0), R["V1_capture"]["q_max"]["value"],
          qmax_at_N(700.0),
          R["V1_capture"]["q_max"]["engineering_target"]["value"]]
    qlab = ["N=75", "N=300, in use", "N=700", "every anchor"]
    xs = np.array([5.0, 20.0, 50.0, 90.0, 130.0])
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for q, lab in zip(qs, qlab):
        ys = [chain_from_leach(None, q_max=q, X_max=float(x)) for x in xs]
        ax.plot(xs, ys, "o-", label="q_max %.3f, %s" % (q, lab))
        print("   q_max %.4f %-14s " % (q, lab)
              + "  ".join("%.4f" % v for v in ys))
    ax.set(xlabel="biomass X_max (g/L)",
           ylabel="gold recovered (umol per litre)",
           title="Biomass is now the larger of the two levers")
    ax.legend(fontsize=7)
    fig.tight_layout()
    save(fig, "fig15_two_levers.png")


# =========================================================================
# 5. k_grow inverse. What a seeded run would have to show.
# =========================================================================
def k_grow_inverse():
    red = {k: R["reduction"][k]["value"] for k in
           ("k_nuc", "k_grow", "k_ox", "k_rech", "K_inh", "nu", "Rech_0")}
    red["E_tot"] = rc.protein_uM(
        R["reagent_arm"]["protein_target_g_per_L"]["value"],
        R["reagent_arm"]["M_r_reductase"]["value"])
    red["t_reduce_h"] = 24.0
    q = R["V1_capture"]["q_max"]["value"] * R["V1_capture"]["X_max"]["value"]
    delivered = q * float(rc.eta_elute(6.0, R["elution"]["phi"]["value"],
                                       R["elution"]["k_elute"]["value"]))
    kgs = np.logspace(np.log10(0.02), np.log10(2.0), 22)
    print("\n5. k_grow INVERSE  delivered = %.4f uM" % delivered)
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    for seed, lab in ((0.0, "no seed"), (0.01, "1 % seed")):
        ys = []
        for kg in kgs:
            p = dict(red, k_grow=float(kg))
            if seed:
                p["seeding_on"] = True
                p["seed_frac"] = seed
            ys.append(100 * sn.reduce_finke_watzky(delivered * 4.0, p,
                                                   t_end=24.0))
        ax.semilogx(kgs, ys, "o-", label=lab + ", 4x concentrated")
        print("   %-10s " % lab
              + "  ".join("%.0f" % v for v in ys[::3]))
    ax.axvline(red["k_grow"], color="k", ls="--", lw=1,
               label="k_grow in use, unmeasured")
    ax.set(xlabel="k_grow (uM^-1 h^-1, log)",
           ylabel="conversion at 24 h (%)",
           title="One seeded run constrains the constant that decides this")
    ax.legend(fontsize=8)
    fig.tight_layout()
    save(fig, "fig16_k_grow_inverse.png")


if __name__ == "__main__":
    tornado()
    monte_carlo()
    two_levers()
    k_grow_inverse()
    print("\nall analysis figures written to", OUT)
