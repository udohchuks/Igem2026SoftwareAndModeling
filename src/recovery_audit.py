"""Reproducible conditional recovery scenarios for the September review.

Model parameters are read from YAML. The feed is the RECOVERY report case,
not a claimed validated leach output. No experimental data are invented.
"""
from . import expression, interfaces, params, recovery_chain as rc, sensitivity


def operating_parameters():
    r = params.load("recovery_chain")
    p = params.values(r["V1_capture"])
    p.update(params.values(r["elution"]))
    p.update(params.values(r["reduction"]))
    p.update(params.values(params.load("recovery_audit")["operating"]))
    e = params.values(params.load("expression"))
    p["q_max"] = interfaces.qmax_from_expression(expression.steady_state(e)["A"])
    arm = params.values(r["reagent_arm"])
    p["E_tot"] = rc.protein_uM(arm["protein_target_g_per_L"], arm["M_r_reductase"])
    return p


def stage_amounts(p=None):
    """Amounts per initial litre for equal-volume, lossless stage transfers."""
    p = operating_parameters() if p is None else p
    out = sensitivity.chain_eta_total(p)
    out["feed_uM"] = p["Au_feed"]
    out["bound_uM"] = p["Au_feed"] * out["eta_capture"]
    out["eluate_uM"] = out["bound_uM"] * out["eta_elute"]
    out["metal_umol_per_initial_L"] = p["Au_feed"] * out["eta_total"]
    return out


def reduction_scenario_range(p=None):
    """Full declared kinetic range, not a confidence interval or global bound."""
    p = operating_parameters() if p is None else p
    r = params.load("recovery_chain")["reduction"]
    au = stage_amounts(p)["eluate_uM"]
    return {name: sensitivity.reduce_finke_watzky(
        au, dict(p, k_nuc=r["k_nuc"]["range"][idx],
                 k_grow=r["k_grow"]["range"][idx]))
        for name, idx in (("slow_corner", 0), ("fast_corner", -1))}
