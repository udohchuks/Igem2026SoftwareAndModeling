"""Two-metal competition: the limits, the balances and the non-adoption."""

import numpy as np
import pytest

from src import capture_design, competition, params, recovery_chain

# The 72 h handoff: 29 uM gold and 818 uM total copper from src.leach, against
# 4.62 umol/g x 5 g dry cells in 1 L. ISSUES.md item 92.
AU_FEED, CU_FEED, SITES = 29.0, 818.0, 23.1
K_AU = params.values(params.load("recovery_chain")["V1_capture"])["K_Au"]


def test_no_copper_reduces_to_the_one_metal_quadratic():
    r = competition.capture_equilibrium(AU_FEED, 0.0, SITES, K_AU, K_Cu=1.0)
    one = float(recovery_chain.capture_equilibrium(AU_FEED, SITES, K_AU))
    assert r["bound_Au"] == pytest.approx(one, rel=1e-9)
    assert r["bound_Cu"] == 0.0


def test_infinite_selectivity_reproduces_the_capacity_scenario():
    scenario = capture_design.capacity_scenario(AU_FEED, 1.0, K_AU, 4.62, 5.0)
    r = competition.capture_equilibrium(AU_FEED, CU_FEED, SITES, K_AU,
                                        K_Cu=K_AU*1e18)
    assert r["captured_Au_fraction"] == pytest.approx(
        scenario["captured_fraction"], rel=1e-6)


def test_both_mass_balances_close():
    r = competition.capture_equilibrium(AU_FEED, CU_FEED, SITES, K_AU, 10.0)
    assert r["free_Au"] + r["bound_Au"] == pytest.approx(AU_FEED, rel=1e-9)
    assert r["free_Cu"] + r["bound_Cu"] == pytest.approx(CU_FEED, rel=1e-9)


def test_occupancies_share_one_denominator_and_cannot_exceed_the_sites():
    r = competition.capture_equilibrium(AU_FEED, CU_FEED, SITES, K_AU, 10.0)
    assert r["theta_Au"] + r["theta_Cu"] <= 1.0
    assert r["bound_Au"] + r["bound_Cu"] <= SITES * (1.0 + 1e-12)


def test_gold_capture_rises_with_selectivity():
    rows = competition.selectivity_sweep(AU_FEED, CU_FEED, SITES, K_AU,
                                         [1.0, 10.0, 100.0, 1e4, 1e6])
    captured = [row["captured_Au_fraction"] for row in rows]
    assert all(np.diff(captured) > 0.0)


def test_separation_factor_is_the_swept_ratio():
    # An analytic property of the extended Langmuir, and the reason the sweep
    # is reported in alpha: the selectivity IS the constant ratio.
    for alpha in (3.0, 28.2, 1e3):
        r = competition.capture_equilibrium(AU_FEED, CU_FEED, SITES, K_AU,
                                            alpha*K_AU)
        assert competition.separation_factor(r) == pytest.approx(alpha, rel=1e-6)


def test_the_tie_point_is_the_feed_ratio():
    assert competition.critical_selectivity(AU_FEED, CU_FEED) == pytest.approx(
        CU_FEED/AU_FEED)


def test_module_adopts_no_copper_constant():
    # K_Cu is an argument everywhere and a stored value nowhere. If a default
    # appears, this test is the place the decision gets relitigated.
    import inspect
    for name in ("capture_equilibrium", "occupancy"):
        sig = inspect.signature(getattr(competition, name))
        assert sig.parameters["K_Cu"].default is inspect.Parameter.empty


def test_GolS_surrogate_is_retired_and_its_record_kept():
    """ISSUES 93: alpha = 52 was a GolS transcriptional response, not a GolB
    binding constant. Retired 2026-10-17 when S76's own GolB constants were
    read. The value stays in a superseded block; loading it must not return a
    number, so nothing can quietly go on using it.
    """
    block = params.load("capture_design")["binding_proxies"]
    entry = block["checa2007_gols_selectivity_alpha"]
    assert entry["value"] is None
    assert entry["superseded"]["value"] == 52.0
    assert "ISSUES 93" in entry["superseded"]["reason"]
    assert "checa2007_gols_selectivity_alpha" not in params.values(block)


def test_GolB_measured_constants_are_recorded_with_their_caveat():
    """ISSUES 93: S76 measured both constants on GolB itself. Stage 3 uses
    them directly (author's decision, 2026-10-17), so the thiosulfate-corrected
    band is retired. The constants and the bare-ion caveat must stay on record.
    """
    block = params.load("capture_design")["binding_proxies"]
    proxies = params.values(block)
    kd_au = proxies["wei2012_golb_Kd_Au"]
    kd_cu = proxies["wei2012_golb_Kd_Cu"]
    assert kd_au == pytest.approx(3.02e-37)
    assert kd_cu == pytest.approx(1.61e-17)
    assert proxies["wei2012_golb_selectivity_alpha"] == pytest.approx(
        kd_cu/kd_au, rel=2e-3)
    assert "bare-ion" in block["wei2012_golb_Kd_Au"]["conditions"]
    assert "conditional_selectivity_band" not in proxies


def test_rejects_impossible_inputs():
    with pytest.raises(ValueError):
        competition.capture_equilibrium(-1.0, CU_FEED, SITES, K_AU, 1.0)
    with pytest.raises(ValueError):
        competition.occupancy(1.0, 1.0, 0.0, 1.0)
    with pytest.raises(ValueError):
        competition.selectivity_sweep(AU_FEED, CU_FEED, SITES, K_AU, [-1.0])
