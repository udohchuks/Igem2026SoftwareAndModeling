"""Build the two approved Stage 2 wiki figures from the live leach model.

The public captions carry interpretation and evidence status. The SVGs contain
only axes, traces and operating markers so they remain visually quiet.
"""

from pathlib import Path
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src import leach


OUT = Path(__file__).parent / "media" / "wiki" / "plots"
GOLD = "#b98524"
TEAL = "#2d9297"
VIOLET = "#8d73a8"
GRID = "#e7e7e2"
INK = "#343431"
MUTED = "#74746e"


def document_ammonia_run(*, oxygen=500.0, n=1201):
    """Run the supplied document's ammoniacal, fixed-oxygen Stage 3 case."""
    _, summary = leach.run_scenario(
        "ammonia",
        n=n,
        O2_dynamic=False,
        alkaline_decay_on=False,
        pH_control=False,
        O2=float(oxygen),
    )
    return summary["traj"]


def finish(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#cfcfca")
    ax.tick_params(colors=MUTED, labelsize=10, length=3)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def productive_window():
    traj = document_ammonia_run()
    hours = traj["t"] / 60.0
    recovery = 100.0 * traj["gold_recovered"]
    thiosulfate = np.maximum(traj["S2O3"], 0.0) / 1000.0

    fig, axes = plt.subplots(2, 1, figsize=(10.8, 7.0), sharex=True)
    fig.patch.set_facecolor("#fbfbfa")
    for ax in axes:
        ax.set_facecolor("#fbfbfa")
        ax.axvline(24, color="#aaa9a3", linewidth=1.1, linestyle=(0, (4, 4)))
        finish(ax)

    axes[0].plot(hours, recovery, color=GOLD, linewidth=3)
    axes[0].set_ylabel("Gold recovered (%)", color=INK, labelpad=12)
    axes[0].set_ylim(0, max(50, np.ceil(recovery.max() / 10) * 10))

    axes[1].plot(hours, thiosulfate, color=TEAL, linewidth=3)
    axes[1].fill_between(hours, thiosulfate, color=TEAL, alpha=0.08)
    axes[1].set_ylabel("Thiosulfate (mM)", color=INK, labelpad=12)
    axes[1].set_xlabel("Time in the leaching vessel (hours)", color=INK, labelpad=12)
    axes[1].set_xlim(0, 72)
    axes[1].set_ylim(bottom=0)

    fig.subplots_adjust(left=0.12, right=0.98, top=0.97, bottom=0.12, hspace=0.18)
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / "dissolving-gold-productive-window.svg", format="svg",
                facecolor=fig.get_facecolor())
    plt.close(fig)


def oxygen_strategy():
    oxygen = np.linspace(25.0, 500.0, 30)
    at_24h = []
    at_72h = []
    for value in oxygen:
        traj = document_ammonia_run(oxygen=value, n=501)
        i24 = int(np.argmin(np.abs(traj["t"] - 1440.0)))
        at_24h.append(100.0 * traj["gold_recovered"][i24])
        at_72h.append(100.0 * traj["gold_recovered"][-1])

    fig, ax = plt.subplots(figsize=(10.8, 5.6))
    fig.patch.set_facecolor("#fbfbfa")
    ax.set_facecolor("#fbfbfa")
    ax.plot(oxygen, at_24h, color=GOLD, linewidth=3, label="After 24 hours")
    ax.plot(oxygen, at_72h, color=VIOLET, linewidth=3, label="After 72 hours")
    ax.axvline(259, color="#aaa9a3", linewidth=1.1, linestyle=(0, (4, 4)))
    finish(ax)
    ax.set_xlim(25, 500)
    ax.set_ylim(bottom=0)
    ax.set_xlabel("Held dissolved oxygen (µmol L⁻¹)", color=INK, labelpad=12)
    ax.set_ylabel("Gold recovered (%)", color=INK, labelpad=12)
    ax.legend(frameon=False, loc="upper right", labelcolor=INK, fontsize=10)
    fig.subplots_adjust(left=0.11, right=0.98, top=0.96, bottom=0.17)
    fig.savefig(OUT / "dissolving-gold-oxygen-strategy.svg", format="svg",
                facecolor=fig.get_facecolor())
    plt.close(fig)


if __name__ == "__main__":
    productive_window()
    oxygen_strategy()
    print("Stage 2 wiki figures rebuilt")
