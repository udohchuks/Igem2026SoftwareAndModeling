"""Generate the biorecovery wiki figures from params/capture_design.yaml.

Run from the repository root:

    python docs/make_biorecovery_figures.py

Writes five PNGs and results.json into docs/media/biorecovery/. It writes
nowhere else. The figures under docs/media/recovery/ and
docs/media/recovery_model/ were built from q_max = 0.0913 umol/g in
params/recovery_chain.yaml; these are built from q_Au = 4.62 umol/g in
params/capture_design.yaml, so the two sets do not agree and are not mixed.

Every number printed here comes from a parameter file or from src/. Console
output is ASCII: the console on the build machine is cp1252.
"""
from pathlib import Path
import json
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import (capture_kinetics, competition, params, recovery_audit,
                 recovery_chain as rc, reduction)

OUT = Path(__file__).resolve().parent / "media" / "biorecovery"
GOLD, COPPER, MARK = "#087e8b", "#bd5932", "#4a4a4a"

design = params.load("capture_design")
figures = params.load("biorecovery_figures")
scenario = params.values(figures["scenario"])
display = params.values(figures["display"])
monolayer = params.values(design["comb_monolayer_assumption"])
proxies = params.values(design["binding_proxies"])
literature = params.values(design["literature"])
volumes = params.values(params.load("recovery_process")["volumes"])
operating = recovery_audit.operating_parameters()

q_Au = literature["wei2012_loading"]
rho_X = monolayer["attached_dry_biomass_density"]
K_Au = operating["K_Au"]
K_Cu = proxies["derived_K_Cu_competition_scenario"]
k_on_Au = params.values(params.load("recovery_chain")["V1_capture"])["k_on"]

area_m2 = scenario["downstream_wetted_area_m2"]
biomass_g = rho_X*area_m2
capture_volume_L = volumes["capture_volume_L"]
Au_feed = operating["Au_feed"]
S_total = q_Au*biomass_g/capture_volume_L
points = int(display["grid_points"])

plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "legend.frameon": False,
                     "figure.autolayout": True})


def save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=display["figure_dpi"], bbox_inches="tight")
    plt.close(fig)
    print("wrote docs/media/biorecovery/" + name)


# --- 1. capture over time ------------------------------------------------
track = capture_kinetics.simulate(Au_feed, S_total, k_on_Au, K_Au,
                                  scenario["capture_duration_h"], points)
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot(track["t_h"], track["Au"], color=COPPER, label="Dissolved gold")
ax.plot(track["t_h"], track["Au_GolB"], color=GOLD, label="Gold on the comb")
ax.set(xlabel="Time (h)", ylabel="Concentration (µM)",
       xlim=(0, scenario["capture_duration_h"]), ylim=(0, None))
ax.legend()
save(fig, "fig1_capture_time.png")

# --- 2. capacity against comb area ---------------------------------------
areas = np.linspace(0.0, display["area_maximum_m2"], points)
sites = q_Au*rho_X*areas/capture_volume_L
captured = np.array([competition.capture_equilibrium(
    Au_feed, 0.0, s, K_Au, K_Cu)["bound_Au"] for s in sites])
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot(areas, captured*capture_volume_L, color=GOLD, label="Gold captured")
ax.axhline(Au_feed*capture_volume_L, color=MARK, linestyle=":",
           label="Dissolved gold available")
ax.set(xlabel="Wetted comb area (m$^2$)", ylabel="Gold at equilibrium (µmol)",
       xlim=(0, display["area_maximum_m2"]), ylim=(0, None))
ax.legend()
save(fig, "fig2_capacity_area.png")

# --- 3. equilibrium capture against effective competing copper -----------
copper = np.linspace(0.0, scenario["copper_stress_uM"], points)
fraction = np.array([competition.capture_equilibrium(
    Au_feed, c, S_total, K_Au, K_Cu)["captured_Au_fraction"] for c in copper])
baseline, stress = 100.0*fraction[0], 100.0*fraction[-1]
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot(copper, 100.0*fraction, color=GOLD)
ax.plot([0.0], [baseline], "o", color=COPPER, label="Working process baseline")
ax.plot([scenario["copper_stress_uM"]], [stress], "s", color=MARK,
        label="Stress test")
ax.set(xlabel="Effective competing copper (µM)",
       ylabel="Gold captured at equilibrium (%)",
       xlim=(0, scenario["copper_stress_uM"]), ylim=(0, 100))
ax.legend()
save(fig, "fig3_copper_competition.png")

# --- 4. elution -----------------------------------------------------------
t_elute = np.linspace(0.0, scenario["elution_duration_h"], points)
released = 100.0*np.array([float(rc.eta_elute(t, operating["phi"],
                                              operating["k_elute"]))
                           for t in t_elute])
eta_elute_reference = float(rc.eta_elute(operating["t_elute_h"],
                                         operating["phi"],
                                         operating["k_elute"]))
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot(t_elute, released, color=GOLD, label="Released into the eluate")
ax.plot(t_elute, 100.0 - released, color=COPPER, label="Remaining on the comb")
ax.plot([operating["t_elute_h"]], [100.0*eta_elute_reference], "o", color=MARK)
ax.set(xlabel="Time (h)", ylabel="Post-wash comb gold (%)",
       xlim=(0, scenario["elution_duration_h"]), ylim=(0, 100))
ax.legend()
save(fig, "fig4_elution.png")

# --- 5. reduction ---------------------------------------------------------
eta_capture = fraction[0]
eluate_uM = Au_feed*eta_capture*eta_elute_reference
trajectory = reduction.simulate(eluate_uM, operating,
                                t_end=operating["t_reduce_h"])
t_reduce = trajectory["t_h"] if "t_h" in trajectory else trajectory["t"]
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot(t_reduce, 100.0*trajectory["Au_aq"]/eluate_uM, color=COPPER,
        label="Dissolved gold(I)-thiourea")
ax.plot(t_reduce, 100.0*trajectory["Au_s"]/eluate_uM, color=GOLD,
        label="Metallic gold")
ax.set(xlabel="Time (h)", ylabel="Reduction-vessel gold (%)",
       xlim=(0, operating["t_reduce_h"]), ylim=(0, 100))
ax.legend()
save(fig, "fig5_reduction.png")

# --- the ledger -----------------------------------------------------------
eta_reduce = float(trajectory["eta_reduce"])
stress_fraction = float(fraction[-1])
results = dict(
    basis=("Production-scale downstream wetted-area design input and "
           "dissolved-gold feed; capture from params/capture_design.yaml, "
           "not params/recovery_chain.yaml"),
    q_Au_umol_per_g=q_Au, rho_X_g_per_m2=rho_X,
    downstream_wetted_area_m2=area_m2, derived_dry_biomass_g=biomass_g,
    comb_capacity_umol=q_Au*biomass_g, site_inventory_uM=S_total,
    K_Au_uM=K_Au, K_Cu_uM=K_Cu, k_on_Au_per_uM_h=k_on_Au,
    feed_uM=Au_feed,
    eta_capture=eta_capture, eta_capture_stress=stress_fraction,
    eta_elute=eta_elute_reference, eta_reduce=eta_reduce,
    eta_total=eta_capture*eta_elute_reference*eta_reduce,
    eta_total_stress=stress_fraction*eta_elute_reference*eta_reduce,
    eluate_uM=eluate_uM,
    gold_balance_residual_uM=track["gold_balance_residual_uM"])
(OUT / "results.json").write_text(json.dumps(results, indent=2) + "\n",
                                  encoding="utf-8")
print("wrote docs/media/biorecovery/results.json")
for key in ("eta_capture", "eta_capture_stress", "eta_elute", "eta_reduce",
            "eta_total", "eta_total_stress"):
    print("   %-20s %6.2f %%" % (key, 100.0*results[key]))
