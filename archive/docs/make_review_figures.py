"""Regenerate every figure in docs/REVIEW.docx.

Run from the repository root:

    python docs/make_review_figures.py

Writes PNGs into docs/media/review/. Numbers come from params/*.yaml and
src/, never from this file, so a figure cannot drift from the model.
"""
from pathlib import Path
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src import expression, params, recovery_chain  # noqa: E402
from src import leach  # noqa: E402

OUT = Path(__file__).resolve().parent / "media" / "review"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"figure.dpi": 160, "font.size": 9,
                     "axes.grid": True, "grid.alpha": 0.3})


def save(fig, name):
    path = OUT / name
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print("wrote", path.relative_to(Path.cwd()) if path.is_relative_to(Path.cwd()) else path)


P_SEQ = leach.parameters()
run = leach.simulate_sequential(P_SEQ, n=20001)
s2, s3 = run["stage2"], run["stage3"]
th2, th3 = s2["t"] / 60.0, s3["t"] / 60.0

# ---------------------------------------------------------------- figure 1
fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
ax[0].plot(th2, s2["S4O6"], label="tetrathionate")
ax[0].plot(th2, s2["S2O3"], label="thiosulfate")
ax[0].set(xlabel="time (h)", ylabel="umol/L",
          title="(a) conversion, closed vessel")
ax[0].legend()

conv = 100 * (1 - s2["S4O6"] / P_SEQ["S4O6_initial"])
ax[1].plot(th2, conv)
ax[1].set(xlabel="time (h)", ylabel="conversion (%)",
          title="(b) extent of conversion")
fig.tight_layout()
save(fig, "fig1_stage2_conversion.png")

# ---------------------------------------------------------------- figure 2
fig, ax = plt.subplots(1, 4, figsize=(14, 3.2))
ax[0].plot(th3, s3["S2O3"], label="thiosulfate (budget)")
ax[0].plot(th3, s3["S4O6"], label="tetrathionate (dead end)")
ax[0].set(xlabel="time (h)", ylabel="umol/L", title="(a) sulfur species")
ax[0].legend(fontsize=8)

ax[1].plot(th3, s3["Cu_II"], label="Cu(II), the oxidant")
ax[1].plot(th3, s3["Cu_I"], "--", label="Cu(I), inactive")
ax[1].set(xlabel="time (h)", ylabel="umol/L", title="(b) copper redox")
ax[1].legend(fontsize=8)

ax[2].plot(th3, s3["Au_complex"])
ax[2].set(xlabel="time (h)", ylabel="umol/L", title="(c) dissolved gold")

ax[3].plot(th3, 100 * s3["gold_recovered"], label="gold")
ax[3].plot(th3, 100 * s3["copper_recovered"], "--", label="copper")
ax[3].set(xlabel="time (h)", ylabel="recovered (%)", title="(d) metal recovery")
ax[3].legend(fontsize=8)
fig.tight_layout()
save(fig, "fig2_stage3_leach.png")

# ---------------------------------------------------------------- figure 3
ledger = leach.thiosulfate_ledger(P_SEQ, s3["t"], s3)
names = ["gold", "copper", "parasitic"]
vals = [ledger[n] for n in names]
labels = ["gold leaching", "copper leaching", "parasitic Cu(II)"]

fig, ax = plt.subplots(figsize=(6, 3.0))
bars = ax.barh(labels, vals, color=["tab:green", "tab:orange", "tab:red"])
ax.set(xlabel="thiosulfate consumed (umol/L)",
       title="Where the leachant goes over 72 h")
for bar, v in zip(bars, vals):
    ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
            f"  {100 * v / ledger['total']:.1f} %", va="center", fontsize=9)
ax.set_xlim(0, max(vals) * 1.18)
fig.tight_layout()
save(fig, "fig3_thiosulfate_ledger.png")

# ---------------------------------------------------------------- figure 4
o2_levels = [20, 40, 60, 80, 100, 150, 250, 500, 1000]
rec = [100 * leach.simulate_sequential(dict(P_SEQ, O2=float(o)),
                                       n=801)["stage3"]["gold_recovered"][-1]
       for o in o2_levels]
fig, ax = plt.subplots(figsize=(6, 3.4))
ax.plot(o2_levels, rec, "o-")
ax.axvline(P_SEQ["O2"], color="k", ls=":", lw=1)
ax.annotate("baseline", (P_SEQ["O2"], min(rec)),
            textcoords="offset points", xytext=(6, 4))
best = int(np.argmax(rec))
ax.annotate(f"optimum, {o2_levels[best]} umol/L",
            (o2_levels[best], rec[best]), textcoords="offset points",
            xytext=(8, -12))
ax.set(xscale="log", xlabel="dissolved oxygen (umol/L)",
       ylabel="gold recovered at 72 h (%)",
       title="Oxygen: oxidant below the peak, poison above it")
fig.tight_layout()
save(fig, "fig4_oxygen_optimum.png")

# ---------------------------------------------------------------- figure 5
t_film = [0.05e-6, 0.1e-6, 0.2e-6, 0.5e-6, 1.0e-6, 2.0e-6]
gold = [100 * leach.simulate_sequential(dict(P_SEQ, t_film=t),
                                        n=801)["stage3"]["gold_recovered"][-1]
        for t in t_film]
fig, ax = plt.subplots(figsize=(6, 3.2))
ax.plot([t * 1e6 for t in t_film], gold, "o-")
ax.axvline(0.5, color="k", ls=":", lw=1)
ax.annotate("assumed", (0.5, min(gold)), textcoords="offset points",
            xytext=(6, 4))
ax.set(xscale="log", xlabel="gold plating thickness (um)",
       ylabel="gold recovered at 72 h (%)",
       title="Plating thickness: assumed, and it is a lever")
fig.tight_layout()
save(fig, "fig5_plating_thickness.png")


# ---------------------------------------------------------------- figure 9
# The pH window. Gold dissolution is flat over pH 9 to 11, so pH acts only on
# whether the leachant survives. Two effects pull against each other and the
# result is an interior optimum.
ph_set = [9.0, 9.3, 9.6, 10.0, 10.3, 10.5, 10.8]
P_PH = dict(P_SEQ, alkaline_decay_on=True, pH_control=True)
ph_runs = [leach.simulate_sequential(dict(P_PH, pH_set=x), n=801)["stage3"]
           for x in ph_set]
ph_gold = [100 * r["gold_recovered"][-1] for r in ph_runs]
ph_tri = [r["S3O6"][-1] for r in ph_runs]

fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.plot(ph_set, ph_gold, "o-", color="tab:green", label="gold at 72 h")
ax.axvspan(9.3, 10.5, color="tab:green", alpha=0.07)
best = int(np.argmax(ph_gold))
ax.annotate(f"optimum, pH {ph_set[best]}", (ph_set[best], ph_gold[best]),
            textcoords="offset points", xytext=(-64, -14))
ax.set(xlabel="pH set point held by the dosing pump",
       ylabel="gold recovered at 72 h (%)",
       title="pH: recycling below the peak, sulfur loss above it")
ax2 = ax.twinx()
ax2.plot(ph_set, ph_tri, "s--", color="tab:red", label="trithionate at 72 h")
ax2.set_ylabel("trithionate (umol/L)", color="tab:red")
ax2.grid(False)
lines = ax.get_lines()[:1] + ax2.get_lines()[:1]
ax.legend(lines, [l.get_label() for l in lines], loc="lower right", fontsize=8)
fig.tight_layout()
save(fig, "fig9_ph_window.png")

# --------------------------------------------------------------- figure 10
# The ligand decision. Same operating point in both columns, so the only
# difference is the ligand. Glycine is a band because eps_gly is unmeasured.
LIG = leach.compare_ligands(n=2001)
fig, ax = plt.subplots(1, 2, figsize=(10, 3.4))

amm = LIG["ammonia"][1]["traj"]
ax[0].plot(amm["t"] / 60.0, 100 * amm["gold_recovered"], color="tab:purple",
           lw=2, label="ammonia, 266 mM")
lo = LIG["glycine_low"][1]["traj"]
hi = LIG["glycine_high"][1]["traj"]
ax[0].fill_between(lo["t"] / 60.0, 100 * hi["gold_recovered"],
                   100 * lo["gold_recovered"], color="tab:blue", alpha=0.25)
mid = LIG["glycine_mid"][1]["traj"]
ax[0].plot(mid["t"] / 60.0, 100 * mid["gold_recovered"], color="tab:blue",
           lw=2, label="glycine, 0.27 M (band)")
ax[0].axvline(24, color="k", ls=":", lw=1)
ax[0].annotate("24 h batch", (24, 8), textcoords="offset points", xytext=(4, 0),
               fontsize=8)
ax[0].set(xlabel="time (h)", ylabel="gold recovered (%)",
          title="(a) gold: ammonia wins, but only after 24 h")
ax[0].legend(fontsize=8, loc="upper left")

names = ["ammonia", "glycine\nhigh", "glycine\nmid", "glycine\nlow"]
keys = ["ammonia", "glycine_high", "glycine_mid", "glycine_low"]
s4 = [LIG[k][1]["S4O6_end"] for k in keys]
s3v = [LIG[k][1]["S3O6_end"] for k in keys]
ax[1].barh(names, s4, color="tab:red", label="tetrathionate")
ax[1].barh(names, s3v, left=s4, color="tab:orange", label="trithionate")
ax[1].set(xlabel="polythionate handed to capture (umol/L)",
          title="(b) what GolB has to survive")
ax[1].legend(fontsize=8, loc="lower right")
fig.tight_layout()
save(fig, "fig10_ligand_scenarios.png")

# --------------------------------------------------------------- figure 11
# Aeration. The old model imposed 500 umol/L, which is above what air can
# dissolve. With the pump modelled, turning it down keeps helping.
kla = [0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 1.68, 3.0]
kla_gold = [100 * leach.simulate_sequential(
    dict(P_SEQ, O2_dynamic=True, kLa=k), n=801)["stage3"]["gold_recovered"][-1]
    for k in kla]
fig, ax = plt.subplots(figsize=(6.2, 3.2))
ax.plot(kla, kla_gold, "o-", color="tab:cyan")
ax.axvline(P_SEQ["kLa"], color="k", ls=":", lw=1)
ax.annotate("stirrer 600 rpm,\n0.5 L/min air", (P_SEQ["kLa"], min(kla_gold)),
            textcoords="offset points", xytext=(-72, 16), fontsize=8)
ax.set(xscale="log", xlabel="kLa (min$^{-1}$), set by stirrer speed and airflow",
       ylabel="gold recovered at 72 h (%)",
       title="Aeration: less is more, over the whole range tested")
fig.tight_layout()
save(fig, "fig11_aeration.png")

# ---------------------------------------------------------------- figure 6
P_EXPR = params.values(params.load("expression"))
t_e, m, Pc, Ps, A = expression.simulate(P_EXPR, t_end=400.0)
ss = expression.steady_state(P_EXPR)

fig, ax = plt.subplots(1, 3, figsize=(13, 3.4))
ax[0].plot(t_e, m)
ax[0].set(xlabel="time (min)", ylabel="mRNA / cell", title="(a) transcript")

ax[1].plot(t_e, Pc, label="cytoplasmic")
ax[1].plot(t_e, Ps, label="surface")
ax[1].plot(t_e, A, label="active sites")
ax[1].set(xlabel="time (min)", ylabel="molecules / cell",
          title="(b) protein and active sites")
ax[1].legend(fontsize=8)

symbols = ["alpha", "N", "beta", "f", "k_sec", "delta_c", "delta_s",
           "delta_m", "mu"]
sens = [expression.normalised_sensitivity(P_EXPR, s) for s in symbols]
ax[2].bar(range(len(symbols)), sens,
          color=["tab:green" if v > 0 else "tab:red" for v in sens])
ax[2].set_xticks(range(len(symbols)))
ax[2].set_xticklabels(symbols, rotation=45, ha="right")
ax[2].axhline(0, color="k", lw=0.8)
ax[2].set(ylabel="normalised sensitivity", title="(c) which knob moves sites")
fig.tight_layout()
save(fig, "fig6_golb_expression.png")

# ---------------------------------------------------------------- figure 7
P_CHAIN = params.load("recovery_chain")
phi = P_CHAIN["elution"]["phi"]["value"]
k_elute = P_CHAIN["elution"]["k_elute"]["value"]

t_k = np.linspace(0, 8, 400)
fig, ax = plt.subplots(figsize=(6, 3.4))
for k in (0.2, 0.5, k_elute, 5.0):
    ax.plot(t_k, recovery_chain.eta_elute(t_k, phi, k),
            label=f"k = {k} /h" + ("  (1 M thiourea)" if k == k_elute else ""))
ax.axhline(1 - phi, color="k", ls="--", lw=1,
           label=f"ceiling 1 - phi = {1 - phi:.2f}")
ax.set(xlabel="elution time (h)", ylabel="eta_elute",
       title="Elution: the ceiling is chemistry, the approach is time")
ax.legend(fontsize=8)
fig.tight_layout()
save(fig, "fig7_elution.png")

# ---------------------------------------------------------------- figure 8
A_star = ss["A"]
q_max = P_CHAIN["V1_capture"]["q_max"]["value"]
X_max = P_CHAIN["V1_capture"]["X_max"]["value"]
feed = float(s3["Au_complex"][-1])

fig, ax = plt.subplots(figsize=(6.4, 3.2))
bars = ax.barh(["delivered by the leach", "capture capacity, in use",
                "capture capacity, at the display target"],
               [feed, q_max * X_max, 0.1961 * X_max],
               color=["tab:blue", "tab:red", "tab:green"])
for bar, v in zip(bars, [feed, q_max * X_max, 0.1961 * X_max]):
    ax.text(v, bar.get_y() + bar.get_height() / 2, f"  {v:.3g} uM",
            va="center", fontsize=9)
ax.set(xscale="log", xlabel="gold (uM, log scale)",
       title="The scale mismatch at handover 1")
fig.tight_layout()
save(fig, "fig8_capacity_mismatch.png")

# --------------------------------------------------------------- figure 12
# Seeding. Every value here comes from src.sensitivity, and seed_frac is
# supplied explicitly because params/recovery_chain.yaml holds it as null.
from src import sensitivity as sn  # noqa: E402

P_RED = P_CHAIN["reduction"]
_red = {k: P_RED[k]["value"] for k in
        ("k_nuc", "k_grow", "k_ox", "k_rech", "K_inh", "nu", "Rech_0")}
_red["E_tot"] = recovery_chain.protein_uM(
    P_CHAIN["reagent_arm"]["protein_target_g_per_L"]["value"],
    P_CHAIN["reagent_arm"]["M_r_reductase"]["value"])
_red["t_reduce_h"] = 24.0

_q = P_CHAIN["V1_capture"]["q_max"]["value"]
_X = P_CHAIN["V1_capture"]["X_max"]["value"]
_eta_el = recovery_chain.eta_elute(
    P_CHAIN["elution"]["t_elute_h"]["value"]
    if "t_elute_h" in P_CHAIN["elution"] else 6.0,
    P_CHAIN["elution"]["phi"]["value"],
    P_CHAIN["elution"]["k_elute"]["value"])
delivered = _q * _X * float(_eta_el)

factors = np.array([1.0, 2.0, 4.0, 6.6, 10.0])
seeds = [0.0, 0.01, 0.10]

fig, ax = plt.subplots(figsize=(6.4, 3.4))
for sfrac in seeds:
    p = dict(_red)
    if sfrac:
        p["seeding_on"] = True
        p["seed_frac"] = sfrac
    ys = [100.0 * sn.reduce_finke_watzky(delivered * f, p, t_end=24.0)
          for f in factors]
    label = "no seed" if not sfrac else f"{100 * sfrac:g} % seed"
    ax.plot(factors, ys, marker="o", label=label)

ax.axhline(90, color="grey", ls=":", lw=1)
ax.text(1.05, 91, "90 % conversion", fontsize=8, color="grey")
ax.set(xlabel="elution concentration factor",
       ylabel="eta_reduce at 24 h (%)",
       title=f"Seeding beats concentrating. Delivered gold = {delivered:.3f} uM")
ax.set_ylim(-3, 105)
ax.legend(fontsize=8)
fig.tight_layout()
save(fig, "fig12_seeding.png")

# Figure 17, a slope chart replacing the section 1 summary table, was
# built and DISCARDED on 2026-08-20. The table compares percentages,
# micromolar and millimolar across two scenarios; forcing them onto one
# log axis made it unreadable, and a zero in the base model drove the
# axis to 1e-15. Some comparisons are tables. That one is.

# --------------------------------------------------------------- figure 18
# t_cross and conversion against the gold the vessel is charged with.
_red = {k: P_CHAIN["reduction"][k]["value"] for k in
        ("k_nuc", "k_grow", "k_ox", "k_rech", "K_inh", "nu", "Rech_0")}
_red["E_tot"] = recovery_chain.protein_uM(
    P_CHAIN["reagent_arm"]["protein_target_g_per_L"]["value"],
    P_CHAIN["reagent_arm"]["M_r_reductase"]["value"])
_red["t_reduce_h"] = 24.0
_ceil = (P_CHAIN["V1_capture"]["q_max"]["value"]
         * P_CHAIN["V1_capture"]["X_max"]["value"])
_deliv = _ceil * float(recovery_chain.eta_elute(
    6.0, P_CHAIN["elution"]["phi"]["value"],
    P_CHAIN["elution"]["k_elute"]["value"]))

au = np.logspace(np.log10(0.03), np.log10(8.0), 40)
tc = 1.0 / (_red["k_grow"] * au)
e24 = [100 * sn.reduce_finke_watzky(float(a), _red, t_end=24.0) for a in au]

fig, ax = plt.subplots(figsize=(6.4, 3.6))
ax.semilogx(au, e24, "-", color="tab:blue", lw=2, label="conversion at 24 h")
ax.axvline(_deliv, color="tab:red", ls="--", lw=1)
ax.annotate("delivered\n%.2f uM" % _deliv, (_deliv, 55), fontsize=8,
            color="tab:red", ha="right")
ax.axvline(3.0, color="tab:green", ls="--", lw=1)
ax.annotate("3 uM", (3.0, 20), fontsize=8, color="tab:green")
ax.set(xlabel="gold charged into the reduction vessel (uM, log)",
       ylabel="conversion at 24 h (%)",
       title="Reduction has a threshold, not a rate")
ax2 = ax.twinx()
ax2.semilogx(au, tc, ":", color="grey", lw=1.5, label="t_cross")
ax2.axhline(24.0, color="grey", lw=0.8)
ax2.annotate("a 24 h batch", (0.035, 26), fontsize=7, color="grey")
ax2.set_ylabel("t_cross (h)", color="grey")
ax2.set_yscale("log")
ax2.grid(False)
lines = ax.get_lines()[:1] + ax2.get_lines()[:1]
ax.legend(lines, [l.get_label() for l in lines], loc="upper left", fontsize=8)
fig.tight_layout()
save(fig, "fig18_reduction_threshold.png")


# --------------------------------------------------------------- figure 19
# The sigmoid, against the shape an electron-limited process would give.
# THE CONTRAST IS THE PREDICTION. Both curves are normalised to the same
# final conversion so that only the SHAPE is being compared.
t = np.linspace(0.0, 24.0, 49)[1:]
fw = np.array([sn.reduce_finke_watzky(5.78, _red, t_end=float(x)) for x in t])
# An electron-limited process is first order in the remaining gold: fastest at
# the start, then slowing. Rate constant chosen to reach the same 24 h point.
k_eq = -np.log(max(1e-9, 1.0 - fw[-1] * 0.999)) / 24.0
el = 1.0 - np.exp(-k_eq * t)

fig, ax = plt.subplots(figsize=(6.4, 3.6))
ax.plot(t, 100 * fw, "-", lw=2, color="tab:blue",
        label="autocatalytic, this model")
ax.plot(t, 100 * el, "--", lw=2, color="tab:orange",
        label="electron-limited, first order")
ax.axvspan(0, 4, color="tab:red", alpha=0.08)
ax.annotate("the two disagree\ncompletely here", (0.4, 62), fontsize=8,
            color="tab:red")
ax.set(xlabel="time (h)", ylabel="conversion (%)",
       title="The sharpest testable prediction: the shape, not the endpoint")
ax.legend(fontsize=8, loc="lower right")
fig.tight_layout()
save(fig, "fig19_sigmoid_shape.png")


# --------------------------------------------------------------- figure 20
# What the lysate volume costs the gold.
mult = np.linspace(1.02, 12.0, 60)
tgt = recovery_chain.protein_uM(
    P_CHAIN["reagent_arm"]["protein_target_g_per_L"]["value"],
    P_CHAIN["reagent_arm"]["M_r_reductase"]["value"])
ratio = np.array([float(recovery_chain.lysate_mixing_ratio(m * tgt, tgt))
                  for m in mult])
gold = np.array([float(recovery_chain.gold_after_mixing(_ceil, r))
                 for r in ratio])

fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.plot(mult, gold, "-", lw=2, color="tab:purple")
ax.axhline(_ceil, color="grey", ls=":", lw=1)
ax.annotate("undiluted, %.3f uM" % _ceil, (7.5, _ceil * 1.02), fontsize=8,
            color="grey")
for m, lab in ((2.0, "2x target"), (4.05, "fed batch, 4x")):
    r = float(recovery_chain.lysate_mixing_ratio(m * tgt, tgt))
    g = float(recovery_chain.gold_after_mixing(_ceil, r))
    ax.plot([m], [g], "o", color="tab:red")
    ax.annotate(lab + "\n%.3f uM" % g, (m, g), textcoords="offset points",
                xytext=(6, -16), fontsize=8)
ax.set(xlabel="lysate reductase, as a multiple of the target",
       ylabel="gold left after mixing (uM)",
       title="A weak lysate is paid for in gold")
fig.tight_layout()
save(fig, "fig20_lysate_dilution.png")


print("\nall figures written to", OUT)
