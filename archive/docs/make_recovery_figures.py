"""Generate the audited recovery figures and numerical summary from YAML.

Run python docs/make_recovery_figures.py. Generated images are scenarios,
not experimental measurements. ISSUES 84-88.
"""
from pathlib import Path
import sys
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import params, recovery_audit as audit, recovery_chain as rc, sensitivity as sn

OUT = Path(__file__).resolve().parent / "media" / "recovery"
OUT.mkdir(parents=True, exist_ok=True)
P = audit.operating_parameters()
R = params.load("recovery_chain")
BASE = audit.stage_amounts(P)
N = P["grid_points"]
plt.rcParams.update({"figure.dpi": 160, "font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False})

def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)

# Capture: both the amount and the fraction, with a recomputed display joint.
sites = P["q_max"] * P["X_max"]
feed = np.geomspace(P["K_Au"] / N, P["Au_feed"] * N, N)
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].loglog(feed, rc.capture_equilibrium(feed, sites, P["K_Au"]), color="#126c80")
axes[0].axhline(sites, linestyle="--", color="#aa6730", label="site inventory")
axes[0].plot(P["Au_feed"], BASE["bound_uM"], "o", color="black")
axes[0].set(xlabel="Feed gold (uM)", ylabel="Bound gold (uM)", title="Capacity under the display model")
axes[0].legend()
axes[1].semilogx(feed, rc.eta_capture(feed, sites, P["K_Au"]), color="#126c80")
axes[1].plot(P["Au_feed"], BASE["eta_capture"], "o", color="black")
axes[1].set(xlabel="Feed gold (uM)", ylabel="Captured fraction", title="Dilution changes fraction, not site count")
save(fig, "figR1_capture_regimes.png")

# Elution: first-order working model and its literature-derived rate range.
t = np.linspace(0, P["t_elute_h"] + P["t_elute_h"], N)
fig, ax = plt.subplots(figsize=(7, 4))
for k in R["elution"]["k_elute"]["range"]:
    ax.plot(t, rc.eta_elute(t, P["phi"], k), linestyle=":", color="#777777",
            label="First-order scenario k = %.2g /h" % k)
ax.plot(t, rc.eta_elute(t, P["phi"], P["k_elute"]), color="#126c80",
        label="First-order reference")
ax.axhline(1-P["phi"], color="black", linestyle=":", label="assumed elutable fraction")
ax.set(xlabel="Elution time (h)", ylabel="Eluted fraction of captured gold",
       title="First-order acid-thiourea elution")
ax.legend(fontsize=8)
save(fig, "figR4_elution.png")

# Full rectangular range. The colour is simulated conversion, not probability.
kn = np.geomspace(*R["reduction"]["k_nuc"]["range"], num=N)
kg = np.geomspace(*R["reduction"]["k_grow"]["range"], num=N)
z = np.array([[sn.reduce_finke_watzky(BASE["eluate_uM"], dict(P, k_nuc=a, k_grow=b))
               for a in kn] for b in kg])
fig, ax = plt.subplots(figsize=(7, 4.5))
mesh = ax.pcolormesh(kn, kg, z, shading="auto", vmin=0, vmax=1, cmap="viridis")
ax.set(xscale="log", yscale="log", xlabel="Effective nucleation constant (1/h)",
       ylabel="Effective growth constant (1/uM/h)", title="Reduction uncertainty at the delivered gold")
ax.plot(P["k_nuc"], P["k_grow"], "*", color="white", markeredgecolor="black", markersize=12, label="reference proxy")
ax.legend(fontsize=8)
fig.colorbar(mesh, ax=ax, label="Fraction converted after %.0f h" % P["t_reduce_h"])
save(fig, "figR5_reduction_threshold.png")

# Stages track amounts per original litre. No concentration or mixing credit.
fig, ax = plt.subplots(figsize=(7, 4))
labels = ["Fed", "Captured", "Eluted", "Metal: reference"]
amounts = [BASE[k] for k in ("feed_uM", "bound_uM", "eluate_uM", "metal_umol_per_initial_L")]
ax.bar(labels, amounts, color=["#555555", "#126c80", "#348f9e", "#aa6730"])
ax.set(yscale="log", ylabel="Gold (umol per initial litre, log scale)", title="Conditional stage balance; collection excluded")
for label, amount in zip(labels, amounts):
    ax.annotate("%.4g" % amount, (label, amount), xytext=(0, 5), textcoords="offset points", ha="center")
save(fig, "figR8_stage_balance.png")

summary = {"basis": "Equal stage volumes; fixed protein target; no collection model; scenario not validation",
           "q_max_umol_per_g": P["q_max"], "site_inventory_uM": sites,
           "reference": BASE, "kinetic_scenarios": audit.reduction_scenario_range(P),
           "grid_conversion_min": float(z.min()), "grid_conversion_max": float(z.max()),
           "grid_shape": list(z.shape)}
(OUT / "audit_results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps(summary, indent=2))
