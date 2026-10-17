"""Generate technical recovery scenarios and their numerical ledger, ISSUES 90.

Outputs in media/recovery_model are generated; never edit them by hand.
Run from the repository root: python docs/make_recovery_model_figures.py.
"""
from pathlib import Path
import json
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import params, recovery_audit as audit, recovery_chain as rc, reduction

OUT = Path(__file__).resolve().parent / "media" / "recovery_model"
OUT.mkdir(parents=True, exist_ok=True)
P = audit.operating_parameters()
R = params.load("recovery_chain")
C = params.values(params.load("recovery_model_figures")["figures"])
BASE = audit.stage_amounts(P)
A = BASE["eluate_uM"]
SLOW = dict(P, k_nuc=R["reduction"]["k_nuc"]["range"][0],
            k_grow=R["reduction"]["k_grow"]["range"][0])
TRAJ = {name: reduction.simulate(A, p) for name, p in (("Reference proxy", P), ("Slow corner", SLOW))}
TEAL, ORANGE, GRAY = "#087e8b", "#bd5932", "#8b959d"
plt.rcParams.update({"font.size": 12, "axes.titlesize": 12, "axes.labelsize": 12,
                     "xtick.labelsize": 11, "ytick.labelsize": 11, "figure.dpi": 170,
                     "axes.spines.top": False, "axes.spines.right": False})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)


def endpoint(p, **kwargs):
    return reduction.simulate(A, p, times=[p["t_reduce_h"]], **kwargs)["eta_reduce"]


# Amounts are per starting feed volume; concentrations coincide only under
# the explicitly retained equal-volume, lossless-transfer assumption.
fig, axes = plt.subplots(1, 2, figsize=(8, 4.5))
lost_capture = BASE["feed_uM"]-BASE["bound_uM"]
lost_elution = BASE["bound_uM"]-A
remaining = A-BASE["metal_umol_per_initial_L"]
ledger = {"Uncaptured": lost_capture, "Retained after wash": lost_elution,
          "Dissolved after reduction": remaining,
          "New metal": BASE["metal_umol_per_initial_L"]}
axes[0].bar(["Initial feed", "Uncaptured"], [BASE["feed_uM"], lost_capture], color=[GRAY, ORANGE])
axes[0].set(ylabel="Gold amount (µmol per initial L)", title="Most feed is uncaptured")
for pos, value in enumerate([BASE["feed_uM"], lost_capture]):
    axes[0].annotate(f"{value:.3g}", (pos, value), xytext=(0, 4), textcoords="offset points", ha="center")
axes[0].margins(y=.15)
values = [BASE["bound_uM"], A, BASE["metal_umol_per_initial_L"]]
axes[1].bar(["Captured", "Eluted", "New metal"], values, color=[TEAL, "#58a5ae", "#274c64"])
for pos, value in enumerate(values):
    axes[1].annotate(f"{value:.4f}", (pos, value), xytext=(0, 4), textcoords="offset points", ha="center")
axes[1].set(ylabel="Gold amount (µmol per initial L)", title="Zoom into the captured stream")
axes[1].margins(y=.55)
axes[1].text(.02, .97, "Amounts: µmol per initial L\n"
             f"Retained after wash: {lost_elution:.4f}\n"
             f"Dissolved at end: {remaining:.4f}", transform=axes[1].transAxes, va="top", fontsize=10)
fig.suptitle("Reference scenario: gold ledger before physical collection", y=1.03, fontsize=13)
save(fig, "fig1_gold_ledger.png")

fig = plt.figure(figsize=(8, 6.5))
layout = fig.add_gridspec(2, 2)
axes = [fig.add_subplot(layout[0, 0]), fig.add_subplot(layout[0, 1]),
        fig.add_subplot(layout[1, :])]
for ax, (name, tr) in zip(axes[:2], TRAJ.items()):
    ax.plot(tr["t_h"], tr["Au_aq"], color=TEAL, label="Dissolved gold")
    mask = tr["metal_new"] > 0 if name == "Slow corner" else np.ones_like(tr["t_h"], dtype=bool)
    ax.plot(tr["t_h"][mask], tr["metal_new"][mask], color=ORANGE, label="New metal")
    if name == "Slow corner":
        ax.set_yscale("log")
    ax.set(xlabel="Reduction time (h)", ylabel="Gold concentration (µM)",
           title=f"{name}\nConversion at end: {tr['eta_reduce']:.3%}")
    ax.legend(fontsize=10)
for name, tr in TRAJ.items():
    style = "-" if name == "Reference proxy" else "--"
    axes[2].plot(tr["t_h"], tr["oxidation_loss"], style, color=ORANGE, label=f"Oxidation: {name}")
    axes[2].plot(tr["t_h"], P["nu"]*tr["metal_new"], style, color=TEAL, label=f"Gold demand: {name}")
axes[2].set(xlabel="Reduction time (h)", ylabel="Reduced-protein\nequivalents (µM)", title="Where reducing power is spent")
axes[2].legend(fontsize=10, loc="upper left")
save(fig, "fig2_reduction_trajectories.png")

kn = np.geomspace(*R["reduction"]["k_nuc"]["range"], num=C["grid_points"])
kg = np.geomspace(*R["reduction"]["k_grow"]["range"], num=C["grid_points"])
grid = np.array([[endpoint(dict(P, k_nuc=nuc, k_grow=grow)) for nuc in kn] for grow in kg])
fig, ax = plt.subplots(figsize=(7.5, 4.8))
mesh = ax.pcolormesh(kn, kg, grid, shading="auto", vmin=0, vmax=1, cmap="viridis")
ax.plot(P["k_nuc"], P["k_grow"], "*", color="white", markeredgecolor="black", markersize=13, label="Reference proxy")
ax.set(xscale="log", yscale="log", xlabel="Effective nucleation constant (h⁻¹)",
       ylabel="Effective growth constant (µM⁻¹ h⁻¹)",
       title=f"Full declared kinetic ranges at {A:.3f} µM initial gold\nScenario map; not a confidence interval")
ax.legend(fontsize=10)
fig.colorbar(mesh, ax=ax, label=f"New-metal fraction after {P['t_reduce_h']:g} h")
save(fig, "fig3_kinetic_range.png")

ratios = np.geomspace(C["minimum_dose_ratio"], C["maximum_dose_ratio"], C["dose_points"])
doses = ratios*P["E_tot"]
dose_results = {}
fig, axes = plt.subplots(1, 2, figsize=(8, 4.3))
for ax, (name, p) in zip(axes, (("Reference proxy", P), ("Slow corner", SLOW))):
    curves = {}
    for mode, label, colour in (("fixed_effective", "Fixed effective kinetics", TEAL),
                                ("linear_reference", "Linear dose hypothesis", ORANGE)):
        curves[mode] = np.array([endpoint(dict(p, E_tot=dose), protein_scaling=mode,
                                          E_ref=P["E_tot"]) for dose in doses])
        ax.semilogx(ratios, curves[mode], color=colour, label=label)
    ax.axvline(1, color=GRAY, linestyle=":")
    ax.set(xlabel="Protein dose / reference dose", ylabel=f"New-metal fraction at {P['t_reduce_h']:g} h",
           title=name)
    ax.legend(fontsize=10)
    dose_results[name] = {key: value.tolist() for key, value in curves.items()}
fig.suptitle(f"Protein dose hypotheses; fixed reference = {P['E_tot']:.3g} µM", y=1.02, fontsize=13)
save(fig, "fig4_protein_dose.png")

t = np.linspace(0, P["t_elute_h"]*C["elution_duration_multiplier"],
                params.values(params.load("reduction_solver")["solver"])["points"])
eta = rc.eta_elute(t, P["phi"], P["k_elute"])
# Analytic derivative of the implemented cumulative elution fraction.
marginal = ((1-P["phi"])*P["k_elute"]
            * np.exp(-P["k_elute"]*t))
fig, axes = plt.subplots(1, 2, figsize=(8, 4))
axes[0].plot(t, eta, color=TEAL)
axes[0].axhline(1-P["phi"], linestyle="--", color=GRAY, label="Assumed elutable fraction")
axes[0].legend(fontsize=10)
axes[0].set(ylabel="Fraction of captured gold eluted", title="Cumulative elution")
axes[1].plot(t, marginal, color=ORANGE)
axes[1].set(ylabel="Additional fraction per hour (h⁻¹)", title="Diminishing gain from washing")
for ax in axes:
    ax.axvline(P["t_elute_h"], color=GRAY, linestyle=":", label="Reference elution time")
    ax.set_xlabel("Elution time (h)")
save(fig, "fig5_elution_tradeoff.png")

summary = {"scope": "Conditional model ending at new metal; equal-volume lossless stage transfers. Not measured uncertainty.",
           "reference": BASE, "protein_reference_uM": P["E_tot"],
           "fate_umol_per_initial_L": ledger,
           "slow_corner": {"k_nuc_per_h": SLOW["k_nuc"], "k_grow_per_uM_h": SLOW["k_grow"],
                           "eta_reduce": TRAJ["Slow corner"]["eta_reduce"],
                           "metal_umol_per_initial_L": A*TRAJ["Slow corner"]["eta_reduce"]},
           "trajectories": {name: {"eta_reduce": tr["eta_reduce"], "donor_ceiling": tr["donor_ceiling"],
                                    "oxidation_loss_uM_protein_equivalents": float(tr["oxidation_loss"][-1]),
                                    "dithionite_consumed_uM": float(P["Rech_0"]-tr["Rech"][-1]),
                                    "maximum_gold_balance_residual_uM": float(np.max(np.abs(tr["gold_residual"]))),
                                    "maximum_electron_balance_residual_uM": float(np.max(np.abs(tr["electron_residual"]))) }
                            for name, tr in TRAJ.items()},
           "kinetic_grid": {"shape": list(grid.shape), "min": float(grid.min()), "max": float(grid.max()),
                            "k_nuc_per_h": kn.tolist(), "k_grow_per_uM_h": kg.tolist(), "conversion": grid.tolist()},
           "dose_ratios": ratios.tolist(), "dose_uM": doses.tolist(), "dose_results": dose_results,
           "elution": {"duration_h": t.tolist(), "fraction": eta.tolist(), "marginal_fraction_per_h": marginal.tolist()}}
(OUT / "results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps({"reference": BASE, "slow_corner": summary["slow_corner"],
                  "trajectories": summary["trajectories"], "grid_min": float(grid.min()),
                  "grid_max": float(grid.max())}, indent=2))

