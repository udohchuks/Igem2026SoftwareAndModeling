"""LaTeX for every display block in docs/WIKI_BIORECOVERY_DRAFT.md.

Generated once and then maintained by hand. The key is the block exactly as the
draft writes it, so docs/build_biorecovery.py fails loudly when the draft gains,
loses or reworks a block rather than silently dropping it from the document.

A value of None means the block is not mathematics and is carried into the
document as plain text.
"""

EQUATIONS = {
    'Au(S₂O₃)₂³⁻ + GolB-(SH)₂ ⇌ Au-GolB + released thiosulfate':
        r"""\mathrm{Au(S_2O_3)_2^{3-}} + \mathrm{GolB\text{-}(SH)_2} \rightleftharpoons \mathrm{Au\text{-}GolB} + \text{released thiosulfate}""",
    'Cu_effective + GolB-(SH)₂ ⇌ Cu-GolB':
        r"""\mathrm{Cu_{effective}} + \mathrm{GolB\text{-}(SH)_2} \rightleftharpoons \mathrm{Cu\text{-}GolB}""",
    'm_X = ρ_X A_wet':
        r"""m_X = \rho_X A_{wet}""",
    'Q_Au,comb = q_Au m_X':
        r"""Q_{Au,comb} = q_{Au} m_X""",
    '[S_total] = Q_Au,comb / V_capture':
        r"""[S_{total}] = \frac{Q_{Au,comb}}{V_{capture}}""",
    '4.62 µmol/g × 0.212 g/m² = 0.979 µmol Au/m²':
        r"""4.62\ \mathrm{\mu mol/g} \times 0.212\ \mathrm{g/m^2} = 0.979\ \mathrm{\mu mol\ Au/m^2}""",
    'r_Au = k_on,Au[Au][S_free] − k_off,Au[Au-GolB]':
        r"""r_{Au} = k_{on,Au}[\mathrm{Au}][S_{free}] - k_{off,Au}[\mathrm{Au\text{-}GolB}]""",
    'd[Au]/dt = −r_Au':
        r"""\frac{d[\mathrm{Au}]}{dt} = -r_{Au}""",
    'd[Au-GolB]/dt = r_Au':
        r"""\frac{d[\mathrm{Au\text{-}GolB}]}{dt} = r_{Au}""",
    'r_Cu = k_on,Cu[Cu_effective][S_free] − k_off,Cu[Cu-GolB]':
        r"""r_{Cu} = k_{on,Cu}[\mathrm{Cu_{effective}}][S_{free}] - k_{off,Cu}[\mathrm{Cu\text{-}GolB}]""",
    'd[Cu_effective]/dt = −r_Cu':
        r"""\frac{d[\mathrm{Cu_{effective}}]}{dt} = -r_{Cu}""",
    'd[Cu-GolB]/dt = r_Cu':
        r"""\frac{d[\mathrm{Cu\text{-}GolB}]}{dt} = r_{Cu}""",
    '[S_free] = [S_total] − [Au-GolB] − [Cu-GolB]':
        r"""[S_{free}] = [S_{total}] - [\mathrm{Au\text{-}GolB}] - [\mathrm{Cu\text{-}GolB}]""",
    '[Au-GolB]₀ = 0':
        r"""[\mathrm{Au\text{-}GolB}]_0 = 0""",
    '[Cu-GolB]₀ = 0':
        r"""[\mathrm{Cu\text{-}GolB}]_0 = 0""",
    'k_off,Au = K_Au k_on,Au = 0.7 h⁻¹':
        r"""k_{off,Au} = K_{Au} k_{on,Au} = 0.7\ \mathrm{h^{-1}}""",
    '[Au-GolB]_eq =\n    [S_total] × ([Au]_eq/K_Au)\n    / (1 + [Au]_eq/K_Au + [Cu_effective]_eq/K_Cu)':
        r"""[\mathrm{Au\text{-}GolB}]_{eq} = \frac{[S_{total}] \times ([\mathrm{Au}]_{eq}/K_{Au})}{1 + [\mathrm{Au}]_{eq}/K_{Au} + [\mathrm{Cu_{effective}}]_{eq}/K_{Cu}}""",
    '[Cu-GolB]_eq =\n    [S_total] × ([Cu_effective]_eq/K_Cu)\n    / (1 + [Au]_eq/K_Au + [Cu_effective]_eq/K_Cu)':
        r"""[\mathrm{Cu\text{-}GolB}]_{eq} = \frac{[S_{total}] \times ([\mathrm{Cu_{effective}}]_{eq}/K_{Cu})}{1 + [\mathrm{Au}]_{eq}/K_{Au} + [\mathrm{Cu_{effective}}]_{eq}/K_{Cu}}""",
    '[Au]₀ = [Au]_eq + [Au-GolB]_eq':
        r"""[\mathrm{Au}]_0 = [\mathrm{Au}]_{eq} + [\mathrm{Au\text{-}GolB}]_{eq}""",
    '[Cu_effective]₀ = [Cu_effective]_eq + [Cu-GolB]_eq':
        r"""[\mathrm{Cu_{effective}}]_0 = [\mathrm{Cu_{effective}}]_{eq} + [\mathrm{Cu\text{-}GolB}]_{eq}""",
    'K_Au = k_off,Au/k_on,Au':
        r"""K_{Au} = k_{off,Au}/k_{on,Au}""",
    'K_Cu = k_off,Cu/k_on,Cu':
        r"""K_{Cu} = k_{off,Cu}/k_{on,Cu}""",
    'α = K_Cu/K_Au = 52':
        r"""\alpha = K_{Cu}/K_{Au} = 52""",
    'K_Cu = 52 × 0.7 µM = 36.4 µM':
        r"""K_{Cu} = 52 \times 0.7\ \mathrm{\mu M} = 36.4\ \mathrm{\mu M}""",
    'dm_X/dt = μ_att m_X(1 − m_X/m_X,max)':
        r"""\frac{dm_X}{dt} = \mu_{att} m_X\left(1 - \frac{m_X}{m_{X,max}}\right)""",
    'm_X(t) = m_X,max\n         / [1 + ((m_X,max − m_X,0)/m_X,0)e^(−μ_att t)]':
        r"""m_X(t) = \frac{m_{X,max}}{1 + \frac{m_{X,max} - m_{X,0}}{m_{X,0}} e^{-\mu_{att} t}}""",
    'm_X,max = ρ_X A_wet':
        r"""m_{X,max} = \rho_X A_{wet}""",
    'A_wet = 5 g / 0.212 g/m² = 23.6 m²':
        r"""A_{wet} = 5\ \mathrm{g} / 0.212\ \mathrm{g/m^2} = 23.6\ \mathrm{m^2}""",
    'Q_Au,comb = 4.62 µmol/g × 5 g = 23.1 µmol':
        r"""Q_{Au,comb} = 4.62\ \mathrm{\mu mol/g} \times 5\ \mathrm{g} = 23.1\ \mathrm{\mu mol}""",
    'n_Au,bound = V_capture[Au-GolB]_pre-elution':
        r"""n_{Au,bound} = V_{capture}[\mathrm{Au\text{-}GolB}]_{pre\text{-}elution}""",
    'n_Au,eluted = η_Au,elute n_Au,bound':
        r"""n_{Au,eluted} = \eta_{Au,elute} n_{Au,bound}""",
    'V_reduction = V_elution + V_reductase':
        r"""V_{reduction} = V_{elution} + V_{reductase}""",
    '[Au(I)-TU]₀ = n_Au,eluted/V_reduction':
        r"""[\mathrm{Au(I)\text{-}TU}]_0 = \frac{n_{Au,eluted}}{V_{reduction}}""",
    'Au-GolB + 2TU → [Au(TU)₂]⁺ + GolB':
        r"""\mathrm{Au\text{-}GolB} + 2\,\mathrm{TU} \rightarrow [\mathrm{Au(TU)_2}]^{+} + \mathrm{GolB}""",
    '[Au-GolB]_elutable,0 = (1 − f_Au,res)[Au-GolB]₀':
        r"""[\mathrm{Au\text{-}GolB}]_{elutable,0} = (1 - f_{Au,res})[\mathrm{Au\text{-}GolB}]_0""",
    'd[Au-GolB]_elutable/dt = −k_elute[Au-GolB]_elutable':
        r"""\frac{d[\mathrm{Au\text{-}GolB}]_{elutable}}{dt} = -k_{elute}[\mathrm{Au\text{-}GolB}]_{elutable}""",
    '[Au-GolB]_elutable(t) =\n    (1 − f_Au,res)[Au-GolB]₀e^(−k_elute t)':
        r"""[\mathrm{Au\text{-}GolB}]_{elutable}(t) = (1 - f_{Au,res})[\mathrm{Au\text{-}GolB}]_0 e^{-k_{elute} t}""",
    '[Au-GolB]_remaining(t) =\n    f_Au,res[Au-GolB]₀ + [Au-GolB]_elutable(t)':
        r"""[\mathrm{Au\text{-}GolB}]_{remaining}(t) = f_{Au,res}[\mathrm{Au\text{-}GolB}]_0 + [\mathrm{Au\text{-}GolB}]_{elutable}(t)""",
    'η_Au,elute(t) =\n    (1 − f_Au,res)(1 − e^(−k_elute t))':
        r"""\eta_{Au,elute}(t) = (1 - f_{Au,res})(1 - e^{-k_{elute} t})""",
    'k_elute = −ln(1 − 0.90/0.97)/12 h = 0.22 h⁻¹':
        r"""k_{elute} = -\ln(1 - 0.90/0.97)/12\ \mathrm{h} = 0.22\ \mathrm{h^{-1}}""",
    'g_R = μ_R(1 − X_R/X_R,max)':
        r"""g_R = \mu_R\left(1 - \frac{X_R}{X_{R,max}}\right)""",
    'dX_R/dt = g_R X_R':
        r"""\frac{dX_R}{dt} = g_R X_R""",
    'dm*_R/dt = G_R I − (δ_m,R + g_R)m*_R':
        r"""\frac{dm^{*}_{R}}{dt} = G_R I - (\delta_{m,R} + g_R)m^{*}_{R}""",
    'dp_R/dt = m*_R − (δ_p,R + g_R)p_R':
        r"""\frac{dp_R}{dt} = m^{*}_{R} - (\delta_{p,R} + g_R)p_R""",
    'R_lysate(t) =\n    p_R(t) X_R(t) n_cells/g y_lysis F_conc × 10⁶/N_A':
        r"""R_{lysate}(t) = p_R(t) X_R(t) n_{cells/g} y_{lysis} F_{conc} \times 10^{6}/N_A""",
    '[R_total]₀ = R_lysate(t_harvest)V_reductase/V_reduction':
        r"""[R_{total}]_0 = R_{lysate}(t_{harvest})V_{reductase}/V_{reduction}""",
    '[Au(TU)₂]⁺ + e⁻ → Au(0) + 2TU':
        r"""[\mathrm{Au(TU)_2}]^{+} + e^{-} \rightarrow \mathrm{Au(0)} + 2\,\mathrm{TU}""",
    'r_Au,reduce =\n    (k_nucleation + k_growth[Au(0)])\n    × [Au(I)-TU] × ([R_red]/[R_total])':
        r"""r_{Au,reduce} = (k_{nucleation} + k_{growth}[\mathrm{Au(0)}]) \times [\mathrm{Au(I)\text{-}TU}] \times \frac{[R_{red}]}{[R_{total}]}""",
    'd[Au(I)-TU]/dt = −r_Au,reduce':
        r"""\frac{d[\mathrm{Au(I)\text{-}TU}]}{dt} = -r_{Au,reduce}""",
    'd[Au(0)]/dt = r_Au,reduce':
        r"""\frac{d[\mathrm{Au(0)}]}{dt} = r_{Au,reduce}""",
    'η_Au,reduce(t) =\n    ([Au(0)]_t − [Au(0)]₀)/[Au(I)-TU]₀':
        r"""\eta_{Au,reduce}(t) = \frac{[\mathrm{Au(0)}]_t - [\mathrm{Au(0)}]_0}{[\mathrm{Au(I)\text{-}TU}]_0}""",
    '[R_ox] = [R_total] − [R_red]':
        r"""[R_{ox}] = [R_{total}] - [R_{red}]""",
    'r_recharge =\n    k_recharge[R_ox][D]\n    / (1 + [Au(I)-TU]/K_Au,inhibition)':
        r"""r_{recharge} = \frac{k_{recharge}[R_{ox}][D]}{1 + [\mathrm{Au(I)\text{-}TU}]/K_{Au,inhibition}}""",
    'd[R_red]/dt =\n    −ν_R,Au r_Au,reduce + r_recharge − k_ox[R_red]':
        r"""\frac{d[R_{red}]}{dt} = -\nu_{R,Au} r_{Au,reduce} + r_{recharge} - k_{ox}[R_{red}]""",
    'd[D]/dt = −ν_D,R r_recharge':
        r"""\frac{d[D]}{dt} = -\nu_{D,R} r_{recharge}""",
    'PCB gold\n  → dissolved gold after leaching\n  → gold captured on the comb\n  → gold released into the eluate\n  → gold converted to recovered Au(0)':
        None,
    'n_Au,leached = η_Au,leach n_Au,PCB':
        r"""n_{Au,leached} = \eta_{Au,leach} n_{Au,PCB}""",
    'n_Au,captured = η_Au,capture n_Au,leached':
        r"""n_{Au,captured} = \eta_{Au,capture} n_{Au,leached}""",
    'n_Au,eluted = η_Au,elute n_Au,captured':
        r"""n_{Au,eluted} = \eta_{Au,elute} n_{Au,captured}""",
    'n_Au,recovered = η_Au,reduce n_Au,eluted':
        r"""n_{Au,recovered} = \eta_{Au,reduce} n_{Au,eluted}""",
    'η_Au,biorecovery = n_Au,recovered/n_Au,leached':
        r"""\eta_{Au,biorecovery} = n_{Au,recovered}/n_{Au,leached}""",
    'η_Au,PCB-to-metal = η_Au,leach η_Au,biorecovery':
        r"""\eta_{Au,PCB\text{-}to\text{-}metal} = \eta_{Au,leach} \eta_{Au,biorecovery}""",
    't_preparation = max(t_leach, t_comb-growth, t_reductase-growth)':
        r"""t_{preparation} = \max(t_{leach},\ t_{comb\text{-}growth},\ t_{reductase\text{-}growth})""",
    't_total = t_preparation + t_capture + t_wash + t_elution + t_reduction':
        r"""t_{total} = t_{preparation} + t_{capture} + t_{wash} + t_{elution} + t_{reduction}""",
}
