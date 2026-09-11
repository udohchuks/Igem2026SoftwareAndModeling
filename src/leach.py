"""Part I — Bioleaching. Three vessels in series.

Source: "Bioleaching Models [Sequential]", in
`docs/source/sequential_2026-08-12/`.

    Stage 1  culture vessel      grow cells, harvest and purify TetH
    Stage 2  conversion vessel   purified TetH + tetrathionate broth
    Stage 3  leach vessel        thiosulfate liquor + crushed board

Only Stages 2 and 3 have differential equations. Stage 1 is algebraic: the
culture settles in about 55 minutes, far faster than anything downstream, so
only the level it reaches is used.

Units: umol/L, minutes, umol for solid inventories, m and m^2 for geometry.
The source table gives n_Au as "mol (or umol)" while R_Au is in umol/min, and
dn_Au/dt = -R_Au. Only umol makes those consistent. ISSUES.md item 4.

State vectors:
    Stage 2   STATES_STAGE2   [S4O6, S2O3]
    Stage 3   STATES_STAGE3   [Vmax, S4O6, S2O3, n_Au, Au_complex,
                               n_Cu, Cu_I, Cu_II, alkalinity]

WHAT THE THREE VESSELS CHANGE
-----------------------------
  1. Stage 2 has no cells, so the enzyme is a fixed input, not a state.
     k_syn, k_deg and mu leave the vessel with the cells.
  2. Stage 2 has no copper, so every loss term vanishes. What is left is a
     closed two-state system that conserves sulfur and has an exact solution.
  3. Stage 3 has no enzyme unless one is deliberately carried over, so
     thiosulfate has no source. It is a budget, charged once and spent.

Point 2 is the payoff. With copper absent the whole broth charge converts and
banks: 94.4 mM of thiosulfate, against the 0.1 M the gold literature calls
optimal.

`Vmax` in Stage 3 is a constant, not a state that builds. It is zero unless
`carry_enzyme` is set, in which case it is k_cat times the enzyme carried over.
There are no cells in the leach vessel, so there is nothing to synthesise or
dilute it. `Vmax = k_cat * [TetH]` keeps ISSUES.md item 13's lumping: those two
constants only ever appear multiplied, so no measurement can separate them.

THE ONE-POT MODEL IS RETIRED
----------------------------
Part I had a second design in which everything ran in one vessel from t = 0.
It was retired on 2026-08-12 and this module no longer implements it. Its
write-up and MATLAB file stay unchanged in `docs/source/sequential_2026-08-12/`
so the record survives. See docs/source/sequential_2026-08-12/README.md.

Every rate constant here comes from params/leach.yaml with a source attached.
Nothing is invented in this file. ISSUES.md item 36 is the audit that cleared
the model before adoption.
"""

import numpy as np
from scipy.integrate import solve_ivp

#: Stage 2. Two states, and their sum never changes.
STATES_STAGE2 = ["S4O6", "S2O3"]

#: Stage 3. Eight chemical states, then the four the extensions add.
STATES = ["Vmax", "S4O6", "S2O3", "n_Au", "Au_complex", "n_Cu", "Cu_I", "Cu_II"]

#: Appended 2026-08-19, all inert unless their switch is on.
#:   S3O6      trithionate, made by the alkaline decomposition of S4O6
#:   O2_diss   dissolved oxygen, when the air pump supplies it
#:   titrant   cumulative net BASE the dosing pump must deliver, umol/L,
#:             negative meaning acid
#:   S_removed cumulative sulfur ATOMS that have left the dissolved
#:             polythionate pool, umol/L. Without it the sulfur audit cannot
#:             close, because thiosulfate drawn into Au(S2O3)2(3-) and
#:             [Cu(S2O3)2](3-) simply disappears from the tracked states, and
#:             the copper draw is 2 or 4 per atom depending on the route, so
#:             it cannot be recovered from the states afterwards.
#: They are appended, never inserted, so `y[:8]` and `STATES_STAGE3[:8]` keep
#: meaning what they meant. A shorter state vector is padded on entry, so the
#: nine-element form still runs.
STATES_STAGE3 = STATES + ["alkalinity", "S3O6", "O2_diss", "titrant",
                          "S_removed"]

AVOGADRO = 6.02214076e23        # molecules/mol, exact by definition


def vmax_from_expression(teth_per_cell, cells_per_L, k_cat):
    """Vmax = k_cat * [TetH]. The route for an engineered host.

    This is the correct route when the organism does not live on tetrathionate
    and TetH is there because it was put there. Count the enzyme molecules the
    expression cascade produces per cell, multiply by cells per litre, convert
    to umol/L, multiply by the turnover number.

        Vmax = k_cat * teth_per_cell * cells_per_L / N_A * 1e6

    Returns umol L^-1 min^-1, with k_cat in min^-1.

    The dimer ambiguity in ISSUES.md item 15 cancels here. If teth_per_cell
    counts monomers, use k_cat = 110 min^-1 per subunit. If it counts dimers,
    use 220 min^-1. Both give the same Vmax, because dimers = monomers/2.

    Used to size Stage 1 and Stage 2. Nothing in Stage 3 calls it.
    """
    enzyme_umol_per_L = teth_per_cell * cells_per_L / AVOGADRO * 1e6
    return k_cat * enzyme_umol_per_L


def exposed_gold_area(m_Au, rho_Au, t_film):
    """Section 4 — a_Au = m_Au / (rho_Au * t_film).

    Gold on a PCB is a plated film. It thins at roughly constant face area
    until exhausted, so the area is a constant while gold remains.
    """
    return m_Au / (rho_Au * t_film)


def exposed_copper_area(a_Cu0, n_Cu, n_Cu0):
    """Section 5 — a_Cu(t) = a_Cu(0) * (n_Cu/n_Cu0)^(2/3).

    Copper is bulk metal and genuinely erodes inward, so area falls as the
    two-thirds power of the fraction remaining.
    """
    frac = max(n_Cu / n_Cu0, 0.0)
    return a_Cu0 * frac ** (2.0 / 3.0)


def initial_copper_area(m_Cu, rho_Cu, d):
    """Section 5 — a_Cu(0) = 6*m_Cu / (rho_Cu * d)."""
    return 6.0 * m_Cu / (rho_Cu * d)


def saturating_fraction(x, K):
    """How close a reactant is to fully occupying the sites it competes for.

    Returns x/(K+x), a number between 0 and 1. At x = K it is exactly 0.5, so
    K is the concentration at which the reaction runs at half its top speed.
    Doubling x beyond that point buys less and less. Negative x is clamped to
    zero, which matters because Part I's Cu(II) pool can go negative
    (ISSUES.md item 5).

    This one shape is used for the Michaelis-Menten enzyme step and for every
    Langmuir surface term in sections 4 and 5.
    """
    x = max(x, 0.0)
    return x / (K + x)


def free_cu_fraction(pH, p):
    """Fraction of dissolved Cu(II) that is free Cu(2+), given glycine.

    Returns (alpha_free, gly_minus_molar).

    Free Cu(2+) is the species that attacks thiosulfate. Glycine holds the
    rest as copper glycinate. Only the deprotonated form Gly- chelates, so the
    pH sets how much ligand is actually available:

        [Gly-]     = G_T * Ka2/(Ka2 + [H+])
        alpha_free = 1 / (1 + beta1 [Gly-] + beta2 [Gly-]^2)

    Concentrations here are mol/L, because the stability constants are.
    G_T arrives in umol/L like everything else and is converted.

    WHY THIS IS THE AMMONIA-FREE FIX. Ammonia does the same job and has better
    published constants, but ammonia above pH 9.25 is mostly free NH3, and
    sparging air through an alkaline ammoniacal liquor is the standard way to
    strip ammonia out of water. The air pump would remove the ligand. Glycine
    is non-volatile, so pH and airflow stay independent knobs. ISSUES.md 54.
    """
    G_T = p["G_T"]
    if G_T <= 0.0:
        return 1.0, 0.0
    H = 10.0 ** (-pH)
    Ka2 = 10.0 ** (-p["pKa2_gly"])
    gly_minus = G_T * 1e-6 * Ka2 / (Ka2 + H)
    b1 = 10.0 ** p["logB1_CuGly"]
    b2 = 10.0 ** p["logB2_CuGly"]
    return 1.0 / (1.0 + b1 * gly_minus + b2 * gly_minus ** 2), gly_minus


def reactive_cu_II(Cu_II, p):
    """Cu(II) available to attack thiosulfate, after glycine takes its share.

        Cu(II)_reactive = Cu(II) * [alpha_free + eps_gly (1 - alpha_free)]

    eps_gly is the reactivity of copper glycinate toward thiosulfate RELATIVE
    to free Cu(2+). It is UNMEASURED and held null in params/leach.yaml, so
    this raises KeyError rather than guessing. That is AGENTS.md rule 4, and
    it matters here more than anywhere else in Part I: this one number sets
    the entire size of the glycine benefit.

    Modelling glycine as a perfect switch, eps_gly = 0, gives 100 % gold at
    every dose, which contradicts the published claim that consumption is
    REDUCED, not eliminated. The eps term is what stops that.

    NOT APPLIED TO THE GOLD RATE, deliberately. Electrochemical work reports
    the Cu(II)-glycine complexes are themselves the catalysts for anodic gold
    dissolution, so the gold term keeps the full Cu(II) pool while the
    parasitic term does not. That asymmetry is the entire mechanism. If it
    turns out to be wrong, glycine does nothing and this model says so.
    """
    if not p.get("gly_on"):
        return Cu_II
    alpha_free, _ = free_cu_fraction(p["pH_set"], p)
    eps = p["eps_gly"]
    return Cu_II * (alpha_free + eps * (1.0 - alpha_free))


def smooth_step(x, width):
    """A soft on-off switch: about 0 when x is 0, about 1 when x >> width.

    Used at metal exhaustion. Section 4 makes the exposed gold area a step
    function, constant while gold remains and zero once it is gone. A hard
    step makes a stiff solver take vanishingly small steps around the
    discontinuity. Replacing it with x/(width + x) rounds the corner without
    moving anything that matters: at ten times the width the switch is already
    at 0.91, and `width` is a ten-thousandth of the starting inventory.

    Part I's author introduced this. It is a numerical device, not chemistry.
    """
    if x <= 0.0:
        return 0.0
    return x / (width + x)


def _exhaustion_switch(p, amount, initial):
    """1 while a solid remains, 0 once it is gone, smoothed if asked.

    Returns a hard 0-or-1 switch unless the parameter set carries
    `exhaustion_smoothing`, in which case the corner is rounded. `parameters`
    turns smoothing on. A set that omits the key keeps the hard switch, which
    is what the write-up prints and what an exact limit check wants.
    """
    fraction = p.get("exhaustion_smoothing")
    if fraction is None:
        return 1.0 if amount > 0.0 else 0.0
    return smooth_step(amount, fraction * initial)


def derivatives(t, y, p, model="B", stoichiometry="balanced",
                return_rates=False, o2=None):
    """The Stage 3 chemistry: how fast each tracked quantity is changing.

    Given the clock time `t` and the current amounts `y`, returns the rate of
    change of each of the eight chemical quantities, in the order given by
    STATES. `stage3_derivatives` wraps this and appends alkalinity.

    model="A" uses the oxygen-only gold rate of section 4 Model A.
    model="B" adds the Cu(II) oxidant pathway of section 4 Model B, and uses
    the combined-oxidant copper rate v1B of section 5.

    stoichiometry="source"    reproduces the write-up exactly as printed.
    stoichiometry="balanced"  applies each balanced reaction's coefficients
                              once, per pathway. Default. See ISSUES.md 18.

    Why the switch exists
    ---------------------
    The write-up prints three rates that each lump two chemical pathways
    together, then applies one stoichiometric coefficient to the lumped total.
    The two pathways do not share coefficients, so a single number cannot be
    right for both. Concretely:

      v1   copper dissolving   O2 route needs 2 S2O3 per Cu and yields 1 Cu(I)
                               Cu(II) route needs 4 S2O3 per Cu, yields 2 Cu(I),
                               and consumes 1 Cu(II)
      R_Au gold dissolving     O2 route consumes no copper at all
                               Cu(II) route consumes 1 Cu(II) per Au

    "source" keeps the printed lumping. "balanced" splits each rate into its
    two pathways and charges each one its own coefficients, read off the
    balanced reactions in sections 4 and 5. The sequential write-up still
    prints the lumped form while its own MATLAB uses the split form, which is
    ISSUES.md item 37, so both are kept here.

    Local names R_Au, v1 to v4 and v_hyd follow the write-up so the code can be
    read beside section 3.2.
    """
    Vmax, S4O6, S2O3, n_Au, Au_cplx, n_Cu, Cu_I, Cu_II = y
    V_R = p["V_R"]
    balanced = stoichiometry == "balanced"
    if stoichiometry not in ("balanced", "source"):
        raise ValueError("stoichiometry must be 'balanced' or 'source'")

    # --- enzyme capacity, if any -----------------------------------------
    # There are no cells in the leach vessel, so nothing synthesises Vmax and
    # nothing dilutes it. It is whatever was carried over, held constant, and
    # zero by default. Vmax = k_cat*[TetH]; ISSUES.md item 13.
    dVmax = 0.0

    # --- shared saturating factors ---------------------------------------
    # `o2` overrides the imposed constant when Stage 3 carries oxygen as a
    # state. Passing it rather than copying the parameter dict on every right-
    # hand side call keeps the solver cheap. None means "use the constant".
    O2 = p["O2"] if o2 is None else o2
    f_S = saturating_fraction(S2O3, p["K_S2O3"])
    f_O2 = saturating_fraction(O2, p["K_O2"])
    f_Cu = saturating_fraction(Cu_II, p["K_CuII"])

    # --- 4. gold, split by oxidant ---------------------------------------
    # 4Au + 8S2O3 + O2 + 2H2O -> 4Au(S2O3)2 + 4OH     no copper involved
    # Au  + 2S2O3 + Cu(II)    ->  Au(S2O3)2 + Cu(I)   1 Cu(II) per Au
    a_Au = (exposed_gold_area(p["m_Au"], p["rho_Au"], p["t_film"])
            * _exhaustion_switch(p, n_Au, p.get("n_Au0", n_Au)))
    R_Au_O2 = p["k_Au_O2"] * a_Au * f_O2 * f_S
    R_Au_Cu = p["k_Au_Cu"] * a_Au * f_Cu * f_S if model != "A" else 0.0
    R_Au = R_Au_O2 + R_Au_Cu

    # --- 5. copper, split by oxidant -------------------------------------
    # 4Cu + O2 + 8S2O3 + 2H2O -> 4[Cu(S2O3)2] + 4OH   2 S2O3, 1 Cu(I) per Cu
    # Cu  + Cu(II) + 4S2O3    -> 2[Cu(S2O3)2]         4 S2O3, 2 Cu(I),
    #                                                 1 Cu(II) consumed per Cu
    a_Cu = (exposed_copper_area(p["a_Cu0"], n_Cu, p["n_Cu0"])
            * _exhaustion_switch(p, n_Cu, p["n_Cu0"]))
    if balanced:
        v1_O2 = p["k_Cu_O2"] * a_Cu * f_O2 * f_S
        v1_Cu = p["k_Cu_Cu"] * a_Cu * f_Cu * f_S if model != "A" else 0.0
        v1 = v1_O2 + v1_Cu                       # copper metal dissolved
        s2o3_draw_Cu = 2.0 * v1_O2 + 4.0 * v1_Cu  # thiosulfate it consumes
        cu_I_from_leach = 1.0 * v1_O2 + 2.0 * v1_Cu
        cu_II_used_by_leach = 1.0 * v1_Cu
        cu_I_from_gold = R_Au_Cu
        cu_II_used_by_gold = R_Au_Cu
    else:
        # Part I as written: coefficients folded into v1, then reused as if
        # v1 were a copper rate. R_Au likewise drains Cu(II) on both routes.
        if model == "A":
            v1 = 2.0 * p["k_Cu_O2"] * a_Cu * f_O2 * f_S
        else:
            v1 = a_Cu * f_S * (2.0 * p["k_Cu_O2"] * f_O2
                               + 4.0 * p["k_Cu_Cu"] * f_Cu)
        s2o3_draw_Cu = v1
        cu_I_from_leach = 2.0 * v1
        cu_II_used_by_leach = v1
        cu_I_from_gold = R_Au
        cu_II_used_by_gold = R_Au
        # Exposed for the proton balance, which needs the oxygen route alone.
        v1_O2 = p["k_Cu_O2"] * a_Cu * f_O2 * f_S

    # One reaction, one constant. Source table called it k1 here and k3
    # in section 5; they are the same event. ISSUES.md item 16.
    #
    # `reactive_cu_II` is the identity unless glycine is switched on. With it
    # on, only the free Cu(2+) fraction plus a small eps_gly share of the
    # glycinate attacks thiosulfate. f_Cu above is deliberately NOT reduced,
    # because copper glycinate still oxidises gold. ISSUES.md item 54.
    v3 = p["k_par"] * reactive_cu_II(Cu_II, p) * S2O3
    v4 = p["k_ox_Cu"] * O2 * Cu_I

    # --- 2. tetrathionate ------------------------------------------------
    # No feed term. The broth is charged once, in Stage 2, and never fed.
    # Without carried-over enzyme v_hyd is zero and this is a DEAD END: the
    # parasitic reaction makes tetrathionate and nothing converts it back.
    v_hyd = Vmax * saturating_fraction(S4O6, p["K_S4O6"])
    dS4O6 = -v_hyd + v3

    # --- 3. thiosulfate --------------------------------------------------
    # Y is the stoichiometric yield, thiosulfate produced per tetrathionate
    # hydrolysed. Section 3's parameter table gives Y = 1 but the equation
    # printed beside it omits Y. It is carried here so that changing the table
    # changes the answer instead of being silently ignored. ISSUES.md item 6.
    dS2O3 = (p["Y"] * v_hyd - 2.0 * v3
             - (2.0 / V_R) * R_Au - (1.0 / V_R) * s2o3_draw_Cu)

    # --- solid and dissolved inventories ---------------------------------
    dn_Au = -R_Au
    dAu_cplx = R_Au / V_R
    dn_Cu = -v1
    dCu_I = (cu_I_from_leach + cu_I_from_gold) / V_R + 2.0 * v3 - 4.0 * v4
    dCu_II = 4.0 * v4 - (cu_II_used_by_leach + cu_II_used_by_gold) / V_R - 2.0 * v3

    dy = [dVmax, dS4O6, dS2O3, dn_Au, dAu_cplx, dn_Cu, dCu_I, dCu_II]
    if not return_rates:
        return dy
    return dy, {
        "R_Au": R_Au, "R_Au_O2": R_Au_O2, "R_Au_Cu": R_Au_Cu,
        "R_Cu": v1, "R_Cu_O2": v1_O2,
        "v_hyd": v_hyd, "v_par": v3, "v_ox_Cu": v4,
        "a_Au": a_Au, "a_Cu": a_Cu,
        "f_S": f_S, "f_O2": f_O2, "f_Cu": f_Cu,
        "s2o3_draw_Cu": s2o3_draw_Cu, "O2": O2,
    }


def gold_recovered_fraction(traj, n_Au0):
    """Fraction of the plated gold that has entered solution."""
    return 1.0 - traj["n_Au"] / n_Au0


# ===========================================================================
# THE THREE VESSELS
# ===========================================================================


def parameters():
    """Build the flat parameter dict for a run, from params/leach.yaml.

    Every number comes from the YAML file. Nothing is defaulted here. A
    parameter still held at null in the YAML is simply absent from the result,
    so using it raises KeyError rather than silently becoming None. That is
    AGENTS.md rule 4.

    `k_cat` is the per-50-kDa-subunit value, because `E_stage2` is a
    concentration of subunits. Pairing it with the per-dimer 220 would
    double-count the dimer.

    The derived geometry, a_Cu0, n_Au0 and n_Cu0, is computed here so that
    changing a mass or a crush size in the YAML moves the areas and the
    inventories with it.
    """
    from . import params as _params

    doc = _params.load("leach")
    p = {}
    for block in ("tetrathionate", "thiosulfate", "gold_leaching", "copper",
                  "feed_basis", "oxygen", "pH_balance", "ligand"):
        p.update(_params.values(doc[block]))
    p.update(_params.values(doc["broth"]))
    p.update(_params.values(doc["sequential"]))

    # Stage 1 only: the culture steady state. Never used by Stage 2 or 3.
    enzyme = _params.values(doc["enzyme_production"])
    p["k_deg"] = enzyme["k_deg"]
    p["mu"] = enzyme["mu"]
    p["X"] = doc["enzyme_capacity"]["teth_per_cell"]["value"]

    p["k_cat"] = p.pop("k_cat_per_subunit")
    p["exhaustion_smoothing"] = _params.values(
        doc["numerics"])["exhaustion_smoothing_fraction"]

    return refresh(p)


def source_2026_08_12_overrides():
    """The three constants that reproduce the 2026-08-12 write-up.

    k_Au_Cu, k_par and K_S2O3 all changed on 2026-08-19, when the team chose
    glycine over ammonia. The write-up in `docs/source/sequential_2026-08-12/`
    still prints the ammoniacal numbers and is never edited, so this returns
    the values that reproduce it:

        p = dict(leach.parameters(), **leach.source_2026_08_12_overrides())

    Use it to reproduce a figure, never to make a prediction. It describes an
    ammoniacal reactor, and this project is not building one: ammonia is
    volatile and the air pump would strip it out. ISSUES.md item 54.
    """
    from . import params as _params

    return _params.values(_params.load("leach")["reproduction_2026_08_12"])


def refresh(p):
    """Recompute everything that follows from the primitive parameters.

    The areas and the starting inventories are not independent numbers. They
    follow from the metal masses, the densities, the film thickness and the
    crush size. Anything that changes one of those five must call this, or the
    run will use a new rate law against the old geometry.

    THIS IS A TRAP THAT HAS ALREADY CAUGHT TWO PEOPLE. Sweeping `d` without
    refreshing gives an identical answer for every crush size, because a_Cu0
    never moves. Part I's author guarded against it by calling his refresh
    inside his sweep. `simulate_sequential` and `simulate_stage3` call this on
    entry, so `dict(p, d=2e-3)` is safe.
    """
    p = dict(p)
    p["a_Cu0"] = initial_copper_area(p["m_Cu"], p["rho_Cu"], p["d"])
    p["a_Au0"] = exposed_gold_area(p["m_Au"], p["rho_Au"], p["t_film"])
    p["n_Au0"] = p["m_Au"] / p["M_Au"] * 1e6      # umol
    p["n_Cu0"] = p["m_Cu"] / p["M_Cu"] * 1e6      # umol
    return p


# --- Stage 1. The culture vessel. Algebraic, not an ODE. -------------------


def stage1_enzyme_steady_state(k_syn, X, k_deg, mu):
    """How much TetH a litre of culture holds once it has settled.

        [E] = k_syn * X / (k_deg + mu)          umol/L

    The culture reaches this in about 1/(k_deg + mu) minutes, roughly 55, which
    is far faster than anything downstream. So the approach is never simulated;
    only the level it reaches is used.

    Note which losses are in the denominator. Growth dilution mu is about 16
    times k_deg here, so enzyme is lost overwhelmingly by cell division, not by
    proteolysis. Engineering a protease-resistant enzyme would buy very little.
    Slowing growth or raising expression would buy a great deal.
    """
    return k_syn * X / (k_deg + mu)


def culture_volume_ratio(target_enzyme, culture_enzyme):
    """Litres of culture needed to charge one litre of the conversion vessel.

    Purification concentrates the enzyme, so the conversion vessel can hold
    more than a culture ever does. The price is volume of culture grown.

    THIS IS A FLOOR, NOT AN ESTIMATE. It assumes every enzyme molecule in the
    culture reaches the conversion vessel. Real extraction and purification
    recover perhaps a third to two thirds. There is no yield term anywhere in
    Part I. See ISSUES.md item 39.
    """
    return target_enzyme / culture_enzyme


# --- Stage 2. The conversion vessel. Closed, and it conserves sulfur. ------


def stage2_derivatives(t, y, p):
    """Tetrathionate to thiosulfate, with nothing else in the vessel.

    States are [S4O6, S2O3], both umol/L.

    There are no cells, so the enzyme is a constant and k_syn, k_deg and mu do
    not appear. There is no copper, so the parasitic reaction cannot happen.
    There is no metal, so nothing draws thiosulfate down. Every loss term is
    gone, and what is left is one Michaelis-Menten step running forwards:

        dS4O6/dt = -Vmax * S4O6/(K_S4O6 + S4O6)
        dS2O3/dt = +Y * Vmax * S4O6/(K_S4O6 + S4O6)        Vmax = k_cat * E

    Because Y = 1, the sum S4O6 + S2O3 never changes. That is a free
    correctness check on any solver, and it is pinned by a test.
    """
    S4O6, _S2O3 = y
    v_hyd = p["k_cat"] * p["E_stage2"] * saturating_fraction(S4O6, p["K_S4O6"])
    return [-v_hyd, p["Y"] * v_hyd]


def simulate_stage2(p, t_end=None, n=2001):
    """Run the conversion vessel. Returns (t, dict of state arrays)."""
    if t_end is None:
        t_end = p["t_stage2"]
    y0 = [p["S4O6_initial"], p["S2O3_initial"]]
    t_eval = np.linspace(0.0, t_end, n)
    sol = solve_ivp(stage2_derivatives, (0.0, t_end), y0, args=(p,),
                    t_eval=t_eval, rtol=1e-10, atol=1e-12, method="LSODA")
    return sol.t, dict(zip(STATES_STAGE2, sol.y))


def stage2_time_to_reach(p, S4O6_target):
    """Minutes to bring tetrathionate down to a chosen level. Exact, no solver.

    A closed Michaelis-Menten step integrates in closed form:

        K_S4O6 * ln(S0/S) + (S0 - S) = Vmax * t

    Use it to cross-check the solver, or to size the vessel without running it.
    The reaction is close to zero order for most of a run: tetrathionate starts
    at 23,200 umol/L against K_S4O6 = 300, so the saturating factor is 0.987 at
    the start and the enzyme works flat out until substrate is nearly gone.
    That is why the curve is almost a straight line and not an exponential.
    """
    S0 = p["S4O6_initial"]
    v_max = p["k_cat"] * p["E_stage2"]
    return (p["K_S4O6"] * np.log(S0 / S4O6_target) + (S0 - S4O6_target)) / v_max


# --- Stage 3. The leach vessel. A fixed budget, spent. --------------------


def stage3_derivatives(t, y, p, model="B", stoichiometry="balanced"):
    """The leach, with thiosulfate as a budget rather than a flow.

    States are STATES_STAGE3: the eight of `derivatives`, plus alkalinity.

    Two things follow from there being no cells in the vessel:

      - Thiosulfate has no production term unless enzyme was carried over.
      - Tetrathionate made by the parasitic reaction is a dead end. Nothing
        converts it back.

    ALKALINITY, NOT FREE PROTONS. The ninth state is net hydroxide added, in
    umol/L, and pH follows from it as pH0 + alkalinity/beta. Tracking free
    [H+] instead does not work here and the failure is not subtle: the run
    makes on the order of 1e5 umol/L of net base, while the free proton pool at
    pH 7 is 0.1 umol/L. The pool goes negative and pH diverges. Alkalinity is
    the standard way round this. See ISSUES.md item 37.

    The four terms in the balance are read off reactions already written:

        4 Cu(I) + O2 + 2H2O -> 4 Cu(II) + 4 OH        +4 per re-oxidation
        gold,   O2 route                              +1 per gold atom
        copper, O2 route                              +1 per copper atom
        S4O6 + H2O -> S2O3 + S + SO4 + 2H+            -2 per hydrolysis

    THREE EXTENSIONS, ADDED 2026-08-19, ALL OFF BY DEFAULT
    ------------------------------------------------------
    Each is a switch in params/leach.yaml. With all three off this function
    returns exactly what it returned before, which is why every figure already
    reported still reproduces.

      tetrathionate.alkaline_decay_on
          4 S4O6(2-) + 6 OH- -> 5 S2O3(2-) + 2 S3O6(2-) + 3 H2O
          Tetrathionate stops being a dead end and hands most of its sulfur
          back. This is the only reason pH changes any rate in the model, so
          without it the dosing pump is unmodellable. It is also the largest
          single term in Part I and rests on the least certain constant; read
          k_alk's note before switching it on.

      oxygen.O2_dynamic
          dO2/dt = kLa (C* - O2) - OUR, with the pump on one side and the
          three oxygen-consuming reactions on the other.

      pH_balance.pH_control
          pH is held at pH_set by the dosing pump, so alkalinity stops moving
          and the model reports TITRANT DEMAND instead: the net base the pump
          must deliver, in umol/L, negative meaning acid. That is the quantity
          the equipment produces and a reagent budget needs.

    OXYGEN PER RE-OXIDATION IS 1.0 v4, NOT 0.25 v4. v5's Intervention 1 writes
    0.25, because v5 defines v4 per Cu(I). Here v4 = k_ox_Cu [O2] [Cu(I)] and
    the existing code already charges 4 Cu(I) and 4 OH- per v4, so v4 is the
    per-O2 extent and one O2 goes with it. Using 0.25 here would under-count
    the pump duty fourfold while the alkalinity balance beside it counted 4.
    """
    n = len(y)
    dy8, r = derivatives(t, y[:8], p, model=model, stoichiometry=stoichiometry,
                         return_rates=True,
                         o2=y[10] if n > 10 and p.get("O2_dynamic") else None)
    dy8 = list(dy8)
    V_R = p["V_R"]

    # --- the proton balance, as chemistry produces it ---------------------
    alk_chem = (4.0 * r["v_ox_Cu"]
                + r["R_Au_O2"] / V_R
                + r["R_Cu_O2"] / V_R
                - 2.0 * r["v_hyd"])

    # --- tetrathionate decomposition in alkali ----------------------------
    # 4 S4O6 + 6 OH- -> 5 S2O3 + 2 S3O6 + 3 H2O, first order in each.
    # Sulfur closes exactly: 4 = 2 x nu_S2_S4 + 3 x nu_S3_S4 = 2.5 + 1.5.
    d_S3O6 = 0.0
    if p.get("alkaline_decay_on"):
        oh_molar = 10.0 ** (p["pH_set"] - 14.0)
        v_alk = p["k_alk"] * oh_molar * max(y[1], 0.0)
        dy8[1] -= v_alk                          # S4O6 destroyed
        dy8[2] += p["nu_S2_S4"] * v_alk          # S2O3 returned
        d_S3O6 = p["nu_S3_S4"] * v_alk           # S3O6 made, and stays
        alk_chem -= p["nu_OH_S4"] * v_alk        # hydroxide consumed

    # --- trithionate hydrolysis, if anyone ever measures it ---------------
    # S3O6(2-) + H2O -> S2O3(2-) + SO4(2-) + 2 H+, first order, not OH-
    # dependent. Sulfur closes as 3 = 2 + 1, with the sulfate leaving the
    # tracked pools and going to S_removed.
    #
    # k_tri is null in params/leach.yaml because the reported measurements are
    # at 70 to 85 C and there is no 25 C value, so switching this on raises.
    # It is wired up anyway: before 2026-08-19 k_tri was declared and read by
    # no code, so obtaining the value and setting it would have changed
    # nothing at all. A parameter that is silently ignored is worse than one
    # that raises. Model audit, 2026-08-19.
    v_tri = 0.0
    if p.get("trithionate_hydrolysis_on"):
        v_tri = p["k_tri"] * max(y[9], 0.0) if n > 9 else 0.0
        d_S3O6 -= v_tri
        dy8[2] += v_tri              # one thiosulfate back per trithionate
        alk_chem -= 2.0 * v_tri      # and two protons, so the pump pays

    # --- oxygen, when the air pump supplies it ----------------------------
    # 4 Au + O2, 4 Cu + O2, 4 Cu(I) + O2. The first two are per metal atom,
    # so a quarter each; the third is already per O2. See the docstring.
    d_O2 = 0.0
    if p.get("O2_dynamic"):
        our = (0.25 * r["R_Au_O2"] / V_R
               + 0.25 * r["R_Cu_O2"] / V_R
               + 1.0 * r["v_ox_Cu"])
        d_O2 = p["kLa"] * (p["C_star"] - r["O2"]) - our

    # --- pH: held by the pump, integrated, or ignored ---------------------
    if p.get("pH_control"):
        d_alk = 0.0                # the pump holds it, so it does not move
        d_titrant = -alk_chem      # and delivers whatever chemistry does not
    elif p.get("pH_on"):
        d_alk = alk_chem
        d_titrant = 0.0
    else:
        d_alk = 0.0
        d_titrant = 0.0

    # --- sulfur that leaves the dissolved polythionate pool ---------------
    # Two thiosulfate per gold and 2 or 4 per copper, each carrying 2 sulfur
    # atoms, plus the two of every four that hydrolysis sends to S(0) and
    # SO4(2-). Accumulating it is what lets sulfur_audit close exactly.
    d_S_removed = (2.0 * (2.0 * r["R_Au"] + r["s2o3_draw_Cu"]) / V_R
                   + 2.0 * r["v_hyd"]
                   + 1.0 * v_tri)     # the sulfate leg of the hydrolysis

    extra = [d_alk, d_S3O6, d_O2, d_titrant, d_S_removed]
    return dy8 + extra[:max(n - 8, 0)]


def ph_from_alkalinity(alkalinity, pH0, beta):
    """Convert net hydroxide added into a pH, on a linear buffer.

    beta is a lumped buffer capacity in umol/L per pH unit. It is a
    calibration target, not a measurement: raise it for a buffered medium,
    lower it for an unbuffered one and the swing grows.
    """
    return pH0 + np.asarray(alkalinity) / beta


def simulate_stage3(p, S4O6_charge, S2O3_charge, t_end=None, n=2001,
                    model="B", stoichiometry="balanced", y0=None):
    """Run the leach vessel on a charge of liquor. Returns (t, states).

    No terminal event is attached. The smoothed exhaustion switch that
    `parameters` turns on removes the discontinuity that would otherwise make
    one necessary, so the run goes to t_end and the arrays are always length n.

    `y0` overrides the whole starting state, in STATES_STAGE3 order. It exists
    so that a check can start the vessel somewhere the process never would, for
    instance with copper already in solution, and is not used by a normal run.
    """
    if t_end is None:
        t_end = p["t_stage3"]
    q = refresh(p)
    if y0 is None:
        vmax0 = q["k_cat"] * q["E_stage3"] if q.get("carry_enzyme") else 0.0
        o2_0 = q["O2_initial"] if q.get("O2_dynamic") else 0.0
        y0 = [vmax0, S4O6_charge, S2O3_charge, q["n_Au0"], 0.0, q["n_Cu0"],
              0.0, 0.0, 0.0, 0.0, o2_0, 0.0, 0.0]
    else:
        # A caller that hands over the pre-2026-08-19 nine-element form gets
        # the appended states zeroed, which is exactly their inert value.
        y0 = list(y0) + [0.0] * (len(STATES_STAGE3) - len(y0))
    t_eval = np.linspace(0.0, t_end, n)
    sol = solve_ivp(stage3_derivatives, (0.0, t_end), y0,
                    args=(q, model, stoichiometry), t_eval=t_eval,
                    rtol=1e-9, atol=1e-11, method="LSODA")
    return sol.t, dict(zip(STATES_STAGE3, sol.y))


# --- The three of them, end to end. ---------------------------------------


def simulate_sequential(p, model="B", stoichiometry="balanced", n=2001):
    """Run all three vessels in order. Returns one dict.

    Stage 1 is solved algebraically. Stage 2's end point becomes Stage 3's
    charge, which is the only thing that crosses between the vessels.

    Keys returned:
        stage1   enzyme per litre of culture, and the culture volume ratio
        stage2   t, S4O6, S2O3
        stage3   t, the nine states, pH, and the recovery fractions
        charge   what went from Stage 2 into Stage 3
    """
    p = refresh(p)
    t2, s2 = simulate_stage2(p, n=n)
    S4O6_charge = float(s2["S4O6"][-1])
    S2O3_charge = float(s2["S2O3"][-1])

    t3, s3 = simulate_stage3(p, S4O6_charge, S2O3_charge, n=n, model=model,
                             stoichiometry=stoichiometry)
    if p.get("pH_control"):
        # The pump holds it. Reporting the alkalinity-derived pH here would
        # be reporting the set point back as if it were a result.
        s3["pH"] = np.full_like(s3["alkalinity"], float(p["pH_set"]))
    else:
        s3["pH"] = ph_from_alkalinity(s3["alkalinity"], p["pH0"], p["beta"])
    s3["gold_recovered"] = gold_recovered_fraction(s3, p["n_Au0"])
    s3["copper_recovered"] = 1.0 - s3["n_Cu"] / p["n_Cu0"]

    stage1 = {}
    if p.get("k_syn") is not None:
        e_culture = stage1_enzyme_steady_state(
            p["k_syn"], p["X"], p["k_deg"], p["mu"])
        stage1 = {
            "enzyme_per_L_culture": e_culture,
            "culture_L_per_L_vessel": culture_volume_ratio(
                p["E_stage2"], e_culture),
        }

    return {
        "stage1": stage1,
        "stage2": {"t": t2, **s2},
        "stage3": {"t": t3, **s3},
        "charge": {"S4O6": S4O6_charge, "S2O3": S2O3_charge},
    }


def sulfur_audit(traj):
    """Total sulfur ATOMS per litre along a trajectory. Must be flat.

    Counting molecules instead of atoms is the trap this exists to catch, and
    v5 fell into it: it checks [S4O6] + [S2O3] = constant and calls that
    sulfur conservation. That sum is conserved because the Stage-2 reaction is
    one-in one-out, but sulfur is not: 4 x 23200 + 2 x 72100 = 237,000 atoms
    in and 4 x 941 + 2 x 94359 = 192,482 out. The missing 44,518 leave as the
    S(0) and SO4(2-) that the same reaction produces and nothing tracks. The
    check passes on the wrong quantity, so it cannot catch a real error.

    Atom counts: S4O6 carries 4, S2O3 carries 2, S3O6 carries 3.
    Trithionate carrying 3 and not 6 is the first error this function caught.

    The second was subtler and is why S_removed exists. Summing only the three
    dissolved polythionates leaves a 3 % drift, because thiosulfate drawn into
    Au(S2O3)2(3-) and [Cu(S2O3)2](3-) leaves the tracked states and is gone.
    It cannot be reconstructed afterwards either: copper takes 2 thiosulfate
    on the oxygen route and 4 on the Cu(II) route, so the draw depends on the
    path and not on the end state. Accumulating it as it happens is the only
    way to make the audit exact, and an audit that is not exact catches
    nothing.
    """
    total = (4.0 * np.asarray(traj["S4O6"])
             + 2.0 * np.asarray(traj["S2O3"])
             + 3.0 * np.asarray(traj["S3O6"])
             + np.asarray(traj["S_removed"]))
    return total


def titrant_demand(traj):
    """Net base the dosing pump must deliver over the run, umol/L.

    Positive means base. Negative means acid, which is the usual sign here:
    the parasitic reaction is a net acid source once the alkaline route is
    consuming hydroxide. Only meaningful with pH_balance.pH_control on;
    otherwise it is zero because there is no pump.
    """
    return float(np.asarray(traj["titrant"])[-1])


def thiosulfate_ledger(p, t, traj, model="B", stoichiometry="balanced"):
    """Where the thiosulfate charge went. Returns umol/L down each sink.

    This is the single most useful diagnostic in Part I, because the answer is
    not the one anybody expects. Gold takes about 0.08 % of the charge. Copper
    metal takes about 1.8 %. The parasitic reaction with Cu(II) takes the other
    98 %. The leachant is not consumed by leaching.

    The three sinks are integrated along a finished trajectory, so they close
    against the thiosulfate actually lost to better than one part in 1e7.

    THERE IS A FOURTH TERM WHEN THE ALKALINE ROUTE IS OPEN, and it is a
    SOURCE, not a sink. Tetrathionate decomposing in alkali gives back 1.25
    thiosulfate per tetrathionate, so the charge is no longer spent once and
    only once. Without that term the ledger does not close and the closure
    check below is what says so, rather than the numbers quietly drifting.

    This also corrects a claim worth stating plainly. The headline "the
    parasitic reaction destroys 98 % of the charge" counts the GROSS draw. Any
    thiosulfate the alkaline route hands back can be destroyed again, so the
    gross figure double-counts. `net_destroyed` is the number that answers
    "how much leachant did the process actually consume".
    """
    n = len(t)
    y = np.array([traj[s] for s in STATES_STAGE3[:8]])
    # Recomputing the rates must use the oxygen the run actually had. Passing
    # None here would silently fall back to the imposed constant, which is not
    # what the trajectory was integrated with once the air pump is on. That
    # error is invisible in the sink numbers themselves and shows up only in
    # the closure check below, which is the whole reason the check exists.
    o2_traj = (np.asarray(traj["O2_diss"]) if p.get("O2_dynamic") else None)
    rates = [derivatives(t[i], y[:, i], p, model=model,
                         stoichiometry=stoichiometry, return_rates=True,
                         o2=None if o2_traj is None else float(o2_traj[i]))[1]
             for i in range(n)]
    to_gold = np.trapezoid([2.0 * r["R_Au"] / p["V_R"] for r in rates], t)
    to_copper = np.trapezoid([r["s2o3_draw_Cu"] / p["V_R"] for r in rates], t)
    to_parasitic = np.trapezoid([2.0 * r["v_par"] for r in rates], t)

    returned = 0.0
    if p.get("alkaline_decay_on"):
        oh_molar = 10.0 ** (p["pH_set"] - 14.0)
        v_alk = p["k_alk"] * oh_molar * np.clip(np.asarray(traj["S4O6"]), 0, None)
        returned = float(np.trapezoid(p["nu_S2_S4"] * v_alk, t))

    total = to_gold + to_copper + to_parasitic - returned
    return {
        "gold": to_gold,
        "copper": to_copper,
        "parasitic": to_parasitic,
        "returned": returned,
        "gross_destroyed": to_parasitic,
        "net_destroyed": to_parasitic - returned,
        "total": total,
        "actually_lost": float(traj["S2O3"][0] - traj["S2O3"][-1]),
    }


# ===========================================================================
# THE TWO LIGAND SCENARIOS
# ===========================================================================


def scenario(name, eps_gly=None, **over):
    """Parameters for one named ligand scenario. See params/leach.yaml.

    v5 runs Stage 3 twice, with ammonia and with no ligand at all. "No ligand"
    is not a choice anybody proposed; copper destroys 98 % of the charge and
    the run fails. The decision in front of the team is WHICH ligand, so the
    second column here is glycine.

    Both start from the same operating point, so every difference between them
    is the ligand. `over` is applied last, for a sweep.

    The glycine scenario needs `eps_gly`, which is unmeasured and null in the
    parameter file. Pass one value from `eps_gly_band`, or use
    `compare_ligands`, which runs the whole band. Omitting it raises, which is
    the intended behaviour: there is no single right value to fall back on.
    """
    from . import params as _params

    doc = _params.load("leach")["scenarios"]
    if name not in doc or name == "meta":
        raise KeyError("no scenario %r; have %r" % (name, scenario_names()))

    p = dict(parameters())
    p.update(doc["meta"]["operating_point"]["values"])
    p.update(doc[name]["overrides"])
    if eps_gly is not None:
        p["eps_gly"] = eps_gly
    p.update(over)
    return refresh(p)


def scenario_names():
    """The scenarios defined in params/leach.yaml, in file order."""
    from . import params as _params

    return [k for k in _params.load("leach")["scenarios"] if k != "meta"]


def eps_gly_band():
    """The calibrated low / mid / high values of eps_gly.

    NOT a measurement. eps_gly is unmeasured; what is published is its
    consequence, thiosulfate consumption falling from 5.2 to 2.2 g/L. These
    three come from calibrating against that observable under different
    operating conditions, and they span 17x. Gold was never used, so every
    gold number the band produces is a prediction rather than a fit.
    """
    from . import params as _params

    return list(_params.load("leach")["scenarios"]["glycine"]
                ["eps_gly_band"]["value"])


def run_scenario(name, eps_gly=None, n=2001, **over):
    """Run one scenario end to end. Returns (parameters, stage-3 summary).

    The summary carries what v5's two Stage-3 sections print: gold at 24 and
    72 hours, the Cu(II) peak, what is handed downstream, and the thiosulfate
    ledger, plus the two things v5 has no column for, titrant demand and the
    trithionate that the alkaline return leg creates.
    """
    p = scenario(name, eps_gly=eps_gly, **over)
    r = simulate_sequential(p, n=n)
    s3 = r["stage3"]
    t = s3["t"]
    i24 = int(np.argmin(abs(t - 1440.0)))
    ledger = thiosulfate_ledger(p, t, s3)
    atoms = sulfur_audit(s3)
    return p, {
        "gold_24h": 100.0 * s3["gold_recovered"][i24],
        "gold_72h": 100.0 * s3["gold_recovered"][-1],
        "Cu_II_peak": float(s3["Cu_II"].max()),
        "S2O3_end": float(s3["S2O3"][-1]),
        "S4O6_end": float(s3["S4O6"][-1]),
        "S3O6_end": float(s3["S3O6"][-1]),
        "Au_feed_24h": float(s3["Au_complex"][i24]),
        "titrant": titrant_demand(s3),
        "ledger": ledger,
        "sulfur_drift": float(abs(atoms - atoms[0]).max() / atoms[0]),
        "traj": s3,
    }


def compare_ligands(n=2001):
    """Ammonia against glycine at one operating point. Returns a dict of runs.

    Keys are "ammonia", then "glycine_low", "glycine_mid", "glycine_high" for
    the three calibrated values of eps_gly. Glycine is reported as a band and
    never as a point, because the constant that sets its size is unmeasured.

    THE COMPARISON HANDICAPS GLYCINE THREE TIMES OVER, and the handicaps are
    listed in the parameter file next to the scenarios. Ammonia is assumed not
    to be stripped by the air pump, though it would be; ammonia keeps its own
    measured constants while glycine's decisive one is unmeasured; and
    k_ox_Cu is ammoniacal in both columns because no ammonia-free value
    exists, which understates the Cu(II) that glycine has to suppress.
    """
    out = {"ammonia": run_scenario("ammonia", n=n)}
    lo, mid, hi = eps_gly_band()
    for label, eps in (("glycine_low", lo), ("glycine_mid", mid),
                       ("glycine_high", hi)):
        out[label] = run_scenario("glycine", eps_gly=eps, n=n)
    return out
