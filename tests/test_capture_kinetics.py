"""Time-dependent capture: the balances, the long-time limit and the copper rule."""

import numpy as np
import pytest

from src import capture_kinetics, competition, params

# The same reference contact as tests/test_competition.py: 29 uM gold against
# 4.62 umol/g x 5 g dry cells in 1 L, with 818 uM copper in the stress test.
AU_FEED, CU_FEED, SITES = 29.0, 818.0, 23.1
K_AU = params.values(params.load("recovery_chain")["V1_capture"])["K_Au"]
K_ON_AU = params.values(params.load("recovery_chain")["V1_capture"])["k_on"]
K_CU = params.values(params.load("capture_design")["binding_proxies"])[
    "derived_K_Cu_competition_scenario"]


def test_k_off_is_the_affinity_times_the_on_rate():
    assert capture_kinetics.k_off(K_AU, K_ON_AU) == pytest.approx(
        K_AU*K_ON_AU, rel=1e-12)


def test_gold_balance_closes_along_the_whole_trajectory():
    r = capture_kinetics.simulate(AU_FEED, SITES, K_ON_AU, K_AU, 24.0, 200)
    assert r["gold_balance_residual_uM"] < 1e-9
    assert r["Au"][0] == pytest.approx(AU_FEED, rel=1e-12)
    assert r["Au_GolB"][0] == 0.0


def test_dissolved_gold_falls_and_captured_gold_rises():
    r = capture_kinetics.simulate(AU_FEED, SITES, K_ON_AU, K_AU, 24.0, 200)
    # The plateau is flat to solver tolerance, so the monotonicity bound is
    # the solver's absolute tolerance and not zero.
    assert np.all(np.diff(r["Au"]) <= 1e-9)
    assert np.all(np.diff(r["Au_GolB"]) >= -1e-9)


def test_long_time_limit_is_the_equilibrium_module():
    r = capture_kinetics.simulate(AU_FEED, SITES, K_ON_AU, K_AU, 24.0, 200)
    equilibrium = competition.capture_equilibrium(AU_FEED, 0.0, SITES,
                                                  K_AU, K_CU)
    assert float(r["Au_GolB"][-1]) == pytest.approx(equilibrium["bound_Au"],
                                                    rel=1e-6)


def test_two_metals_share_one_site_inventory():
    r = capture_kinetics.simulate(AU_FEED, SITES, K_ON_AU, K_AU, 24.0, 200,
                                  Cu_0=CU_FEED, k_on_Cu=K_ON_AU, K_Cu=K_CU)
    assert np.all(r["Au_GolB"] + r["Cu_GolB"] <= SITES*(1.0 + 1e-9))
    equilibrium = competition.capture_equilibrium(AU_FEED, CU_FEED, SITES,
                                                  K_AU, K_CU)
    assert float(r["Au_GolB"][-1]) == pytest.approx(equilibrium["bound_Au"],
                                                    rel=1e-4)


def test_copper_capture_lowers_gold_capture():
    gold_only = capture_kinetics.simulate(AU_FEED, SITES, K_ON_AU, K_AU,
                                          24.0, 200)
    with_copper = capture_kinetics.simulate(AU_FEED, SITES, K_ON_AU, K_AU,
                                            24.0, 200, Cu_0=CU_FEED,
                                            k_on_Cu=K_ON_AU, K_Cu=K_CU)
    assert with_copper["Au_GolB"][-1] < gold_only["Au_GolB"][-1]


def test_a_copper_feed_without_copper_rate_constants_is_refused():
    with pytest.raises(ValueError, match="k_on_Cu"):
        capture_kinetics.simulate(AU_FEED, SITES, K_ON_AU, K_AU, 24.0, 200,
                                  Cu_0=CU_FEED)


@pytest.mark.parametrize("bad", [
    dict(Au_0=-1.0), dict(S_total=-1.0), dict(k_on_Au=0.0),
    dict(K_Au=0.0), dict(t_end=0.0), dict(points=1),
])
def test_unphysical_inputs_are_refused(bad):
    call = dict(Au_0=AU_FEED, S_total=SITES, k_on_Au=K_ON_AU, K_Au=K_AU,
                t_end=24.0, points=200)
    call.update(bad)
    with pytest.raises(ValueError):
        capture_kinetics.simulate(**call)
