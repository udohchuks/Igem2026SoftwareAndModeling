# Appendix A — every parameter in the model

**Tier 4, generated. Do not hand-edit this file.** It is rewritten from
`params/*.yaml` by `docs/make_review_tables.py` every time
`docs/build_review.py` runs, and any edit made here is discarded without
warning. `AGENTS.md` section 11.

Each row is read from the file the code loads, so no value here can differ
from the one the model used to produce the figures above.

**Read the status column first.** Anything marked *assumed*, *unmeasured*,
*fitted* or *placeholder* is a number we chose rather than found. Every one
of those appears in section 8, where we ask you to confirm it. A parameter
with no value stays `null` and the model raises an error rather than
substituting a guess.

Where the source column says *Stage 1*, *Stage 2* or *Stage 3*, that is the
source document's own numbering for the culture, conversion and leach
vessels, quoted unchanged.

## A.1 Bioleaching — all three vessels

Source file: `params/leach.yaml`

| Parameter | Block | Value | Unit | Status | Source or basis |
|---|---|---|---|---|---|
| S2O3_initial | broth | 72100 | umol/L | derived from the recipe | docs/source/sequential_2026-08-12/, Stage 2 feed composition |
| S4O6_initial | broth | 23200 | umol/L | derived from the recipe | docs/source/sequential_2026-08-12/, Stage 2 feed composition |
| d | copper | 0.006 | m | operating choice | docs/source/sequential_2026-08-12/, operating choice |
| k_Cu_Cu | copper | 200 | umol.m^-2.min^-1 | **assumed equal to `k_Cu_O2`** | docs/source/sequential_2026-08-12/, assumed equal to k_Cu_O2 |
| k_Cu_O2 | copper | 200 | umol.m^-2.min^-1 | sourced | [13] Salinas-Rodriguez 2022 |
| k_ox_Cu | copper | 0.0001 | L.umol^-1.min^-1 | sourced by proxy | [7] Breuer & Jeffrey 2003 |
| rho_Cu | copper | 8960 | kg.m^-3 | sourced | — |
| Vmax | enzyme_capacity | 80.36 | umol.L^-1.min^-1 | derived from the display model | params/expression.yaml + tetrathionate.k_cat [S1] |
| biomass | enzyme_capacity | 4 | g dry weight/L | operating choice | Chosen 2026-08-11 to reach Vmax = 14.3, the capacity the retired route claimed at 0.1 g/L. A normal aerobic E. |
| cells_per_g | enzyme_capacity | 2.36e+12 | cells/g dry weight | sourced | params/conversions.yaml :: cells_per_g_dry_weight [S30] |
| k_Vmax | enzyme_capacity | **null — model refuses to run** | umol.cell^-1.min^-1 | derived at use | — |
| localisation | enzyme_capacity | surface_displayed | — | design choice | TetH must meet tetrathionate in the bulk liquid, so P_s is used, not the cytoplasmic pool P_c = 1454. Native T |
| organism | enzyme_capacity | Escherichia coli | — | team decision | Confirmed 2026-08-11. Same organism in Parts I, II and III. |
| route | enzyme_capacity | expression | — | team decision | Vmax = k_cat * [TetH]. Computed by src/leach.py :: vmax_from_expression(teth_per_cell, cells_per_L, k_cat). |
| teth_per_cell | enzyme_capacity | 23301 | molecules/cell | derived from the display model | params/expression.yaml; src/expression.py :: simulate |
| X | enzyme_production | **null — model refuses to run** | cell/L | measured input | — |
| k_deg | enzyme_production | 0.0011 | min^-1 | sourced | [4] Maurizi 1992 |
| k_syn | enzyme_production | **null — model refuses to run** | umol.cell^-1.min^-1 | **needs calibration** | — |
| mu | enzyme_production | 0.02 | min^-1 | adopted from the display model | params/expression.yaml :: mu |
| M_Au | feed_basis | 0.19697 | kg/mol | sourced | IUPAC standard atomic weight |
| M_Cu | feed_basis | 0.06355 | kg/mol | sourced | IUPAC standard atomic weight |
| m_Au | feed_basis | 2e-05 | kg | sourced | docs/source/sequential_2026-08-12/, typical PCB assay |
| m_Cu | feed_basis | 0.03 | kg | sourced | docs/source/sequential_2026-08-12/, typical PCB assay |
| pcb_loading | feed_basis | 100 | g/L | operating choice | docs/source/sequential_2026-08-12/ |
| K_CuII | gold_leaching | 50000 | umol/L | sourced | [12] Maharaj 2024 |
| K_O2 | gold_leaching | 50 | umol/L | sourced | [10] Sitando 2018 |
| K_S2O3 | gold_leaching | 3376 | umol/L | sourced | [18] Senanayake 2005, J. Colloid Interface Sci. 286, 253 |
| k_Au_Cu | gold_leaching | 21 | umol.m^-2.min^-1 | sourced | [11] Aylmore & Muir 2001; [12] Maharaj 2024 |
| k_Au_O2 | gold_leaching | 11.4 | umol.m^-2.min^-1 | sourced | [9] Zhang & Nicol 2003; [10] Sitando 2018 |
| rho_Au | gold_leaching | 19300 | kg.m^-3 | sourced | — |
| t_film | gold_leaching | 5e-07 | m | **assumed by us** | team assumption; range from docs/source/sequential_2026-08-12/ |
| G_T | ligand | **null — model refuses to run** | umol/L | operating choice | Held null because the dose is not chosen. The published glycine- thiosulfate work uses about 0.27 M, i.e. 2.7e |
| eps_gly | ligand | **null — model refuses to run** | dimensionless | **unmeasured** | HELD NULL DELIBERATELY. This one number sets the entire size of the glycine benefit and NOBODY HAS MEASURED IT |
| gly_on | ligand | False | — | operating choice | team decision 2026-08-19 |
| logB1_CuGly | ligand | 8.62 | dimensionless | sourced | IUPAC stability constant compilations |
| logB2_CuGly | ligand | 15.64 | dimensionless | sourced | IUPAC stability constant compilations |
| pKa2_gly | ligand | 9.78 | dimensionless | sourced | standard, 25 C |
| exhaustion_smoothing_fraction | numerics | 0.0001 | dimensionless | numerical_choice | docs/source/sequential_2026-08-12/, smooth_step |
| C_star | oxygen | 259 | umol/L | sourced | APHA Standard Methods DO tables |
| O2 | oxygen | 500 | umol/L | operating choice | docs/source/sequential_2026-08-12/ |
| O2_dynamic | oxygen | False | — | operating choice | docs/source/Bioleaching_Models_v5.docx, Intervention 1 |
| O2_initial | oxygen | 259 | umol/L | operating choice | docs/source/Bioleaching_Models_v5.docx, Intervention 1 |
| kLa | oxygen | 1.68 | min^-1 | derived_from_correlation | [Van't Riet 1979]; equipment values in v5 Intervention 1 |
| beta | pH_balance | 1e+05 | umol/L per pH unit | **needs calibration** | About a 0.1 M carbonate buffer. Lower it and the pH swing grows. |
| form | pH_balance | alkalinity | — | team decision | Adopted 2026-08-12. Tracking free [H+] fails here by construction: net base production is about 1e5 umol/L ove |
| pH0 | pH_balance | 7 | dimensionless | operating choice | docs/source/sequential_2026-08-12/, Stage 3 |
| pH_control | pH_balance | False | — | operating choice | team equipment, 2026-08-19 |
| pH_on | pH_balance | False | — | operating choice | docs/source/sequential_2026-08-12/, Stage 3 |
| pH_set | pH_balance | **null — model refuses to run** | dimensionless | operating choice | HELD NULL because the set point is not chosen. Choosing it is the call, and the model raises rather than pick  |
| K_S2O3 | reproduction_2026_08_12 | 3900 | umol/L | retired_reproduction_only | [18] Senanayake 2005 |
| k_Au_Cu | reproduction_2026_08_12 | 1500 | umol.m^-2.min^-1 | retired_reproduction_only | [11] Aylmore & Muir 2001; [12] Maharaj 2024 |
| k_par | reproduction_2026_08_12 | 1e-05 | L.umol^-1.min^-1 | retired_reproduction_only | [6] Byerley 1973; [7] Breuer & Jeffrey 2003 |
| eps_gly_band | scenarios.glycine | [0.0024, 0.0116, 0.0421] | — | calibrated_against_a_published_consequence | calibrated 2026-08-19 against the 5.2 -> 2.2 g/L observable |
| E_stage2 | sequential | 0.043 | umol/L | design choice | docs/source/sequential_2026-08-12/, Stage 2 |
| E_stage3 | sequential | 0.043 | umol/L | design choice | docs/source/sequential_2026-08-12/, Stage 3 |
| carry_enzyme | sequential | False | — | operating choice | docs/source/sequential_2026-08-12/, compare_carryover |
| enzyme_half_life_stage2 | sequential | **null — model refuses to run** | min | missing | NOT MODELLED. Stage 2 holds the enzyme concentration constant for 4320 minutes. k_deg was dropped along with t |
| purification_yield | sequential | **null — model refuses to run** | dimensionless | missing | NOT MODELLED ANYWHERE. Stage 1 assumes every enzyme molecule in the culture reaches the conversion vessel. Rea |
| t_stage2 | sequential | 4320 | min | operating choice | docs/source/sequential_2026-08-12/ |
| t_stage3 | sequential | 4320 | min | operating choice | docs/source/sequential_2026-08-12/ |
| K_S4O6 | tetrathionate | 300 | umol/L | chosen_from_sourced_range | [2] Kanao 2007, range; docs/source/sequential_2026-08-12/, choice |
| alkaline_decay_on | tetrathionate | False | — | operating choice | team decision 2026-08-19 |
| k_alk | tetrathionate | 16.8 | L.mol^-1.min^-1 | sourced_secondary | secondary only; primary sources not yet obtained |
| k_cat | tetrathionate | 220 | min^-1 | sourced | [S1] Kanao et al. 2023, J. Biosci. Bioeng. |
| k_cat_per_subunit | tetrathionate | 125 | min^-1 | sourced | [S1] Kanao et al. 2023; docs/source/sequential_2026-08-12/ |
| k_par | tetrathionate | 1.2e-05 | L.umol^-1.min^-1 | sourced by proxy | [6] Byerley 1973; [7] Breuer & Jeffrey 2003 |
| k_tri | tetrathionate | **null — model refuses to run** | min^-1 | **unmeasured** | HELD NULL DELIBERATELY, so that using it raises rather than guessing. The reported measurements are at 70 to 8 |
| nu_OH_S4 | tetrathionate | 1.5 | dimensionless | stoichiometric | balanced equation |
| nu_S2_S4 | tetrathionate | 1.25 | dimensionless | stoichiometric | balanced equation |
| nu_S3_S4 | tetrathionate | 0.5 | dimensionless | stoichiometric | balanced equation |
| trithionate_hydrolysis_on | tetrathionate | False | — | operating choice | team decision 2026-08-19 |
| V_R | thiosulfate | 1 | L | operating choice | docs/source/sequential_2026-08-12/, both write-ups |
| Y | thiosulfate | 1 | dimensionless | sourced | [1] |

## A.2 GolB surface display

Source file: `params/expression.yaml`

| Parameter | Block | Value | Unit | Status | Source or basis |
|---|---|---|---|---|---|
| K_Au | — | 10 | uM | **placeholder** | Placeholder -- no clean experimental K_Au; source or fit |
| N | — | 300 | copies/cell | sourced_from_an_inconsistent_literature | pJUMP24-1A(sfGFP), OriV #4 pRO1600/ColE1, high copy per Addgene #126971; band from NEB pUC19 datasheet and the autodisplay literature |
| P_s_max | — | 1e+05 | sites/cell | sourced | Autodisplay reaches >10^5 molecules/cell (Jose & Meyer) |
| alpha | — | 0.5 | mRNA.min^-1.copy^-1 | sourced | Typical E. coli promoter output (BioNumbers) |
| beta | — | 4 | protein.min^-1.mRNA^-1 | sourced | Typical E. coli translation efficiency (BioNumbers) |
| delta_c | — | 0.005 | min^-1 | **assumed** | approx 0 for a stable protein |
| delta_m | — | 0.2 | min^-1 | sourced | E. coli mRNA half-life approx 2-5 min (t_half approx 3.5 min) |
| delta_s | — | 0.005 | min^-1 | **assumed** | Assumed dilution-dominated |
| f | — | 0.5 | dimensionless | **fitted** | Folding/accessibility; fitted parameter |
| k_sec | — | 0.1 | min^-1 | **fitted** | Set by the display scaffold; fitted parameter |
| mu | — | 0.02 | min^-1 | sourced | Doubling time approx 35 min (mu = ln2 / t_double) |

## A.3 Recovery chain

Source file: `params/recovery_chain.yaml`

| Parameter | Block | Value | Unit | Status | Source or basis |
|---|---|---|---|---|---|
| A_tox | V1_capture | 250 | uM | LB regime; two sources agree on ~30 uM onset | SOURCED 2026-08-24. Munoz-Villagran et al. 2020, Biol Res 53:26, doi:10.1186/s40659-020-00292-5: MIC of Au(III) for aerobic E. coli in LB at 37 C is 250 uM. SOURCES.md S54. |
| Au_feed | V1_capture | **null — model refuses to run** | uM | supplied_by_part_I | params/leach.yaml |
| K_Au | V1_capture | 0.7 | uM | literature proxy from a purified GolB-based sensor; not measured in thiosulfate leachate | S78 |
| X0 | V1_capture | 0.05 | g/L | standard E. coli | — |
| X_max | V1_capture | 5 | g/L | design choice | Sezonov, Joseleau-Petit & D'Ari 2007, J Bacteriol 189(23):8746-8749, for the LB ceiling of OD600 7; Ukkonen et al. 2011, Microb Cell Fact 10:107, for the measured shake-flask dry cell weights of 8.1, 10.3 and 19.7-21.1 g/L. SOURCES.md S40 and S41 |
| k_dam | V1_capture | 1 | h^-1 | scale-setting; k_dam/A_tox non-identifiable --- only the ratio is determined | NOT MEASURABLE SEPARATELY. No published rate exists for gold damage accrual in E. coli. 1.0 h^-1 is a scale for D, which is dimensionless and defined only up to this constant; what carries the biology is the ratio k_dam/A_tox, and A_tox is sourced above. SOURCES.md S54, S55. |
| k_maint | V1_capture | 0.005 | h^-1 | standard E. coli | Renamed from m on 2026-08-11. The was/now table in docs/EQUATIONS.md announced this rename on 2026-08-10 but i |
| k_on | V1_capture | 1 | uM^-1.h^-1 | sourced 2026-08-24; the equilibrium still depends only on K_Au | Tsuruta 2004, J Gen Appl Microbiol 50(4):221-228, doi:10.2323/jgam.50.221, Fig. 5: gold(III) biosorption onto resting Pseudomonas maltophilia fitted as Q = Qe[1 - exp(-(i*t + j))] with i = 0.0201 /min, j = 2.78 and Qe = 329 umol/g dry cells, at 50.5 uM Au and 0.15 g/L cells. Their loading leaves 1.15 uM free at equilibrium, and the relaxation rate of this model's binding equation, k_on*(Au + S0 - 2*Ceq) + k_off, then gives k_on = 1.05 uM^-1 h^-1. SOURCES.md S57. |
| k_rep0 | V1_capture | 0.1 | h^-1 | an order of magnitude slower than the nearest measured analogue | SOURCED 2026-08-24 against an analogue, not against gold. LaVoie & Summers 2018, BMC Genomics 19:52, doi:10.1186/s12864-017-4413-z: E. coli recovering from a sublethal soft-metal thiol insult shows 10-30 min of growth stasis and is back at its pre-exposure growth rate by 60 min. SOURCES.md S56. |
| lambda_D | V1_capture | **null — model refuses to run** | uM^-1.h^-1 | **unmeasured** | ISSUES 73 and 88. The source formula is dimensionally invalid; do not infer a replacement. |
| mu | V1_capture | 1.2 | h^-1 | adopted from the display model | Part II runs its expression cascade at mu = 0.02 min^-1 = 1.2 /h, doubling time 34.7 min. Growth dilution is 8 |
| q_max | V1_capture | 0.0913 | uM/(g/L) | adopted from the display model | CHANGED 2026-08-19 from 0.0108 with Part II's copy number, N = 20 -> 300. THIS VALUE IS NOT INDEPENDENT. It is |
| w | V1_capture | 1 | dimensionless | insensitive (PRCC -0.02) | — |
| whole_cell_capacity | V1_capture | **null — model refuses to run** | umol/g dry cells | unmeasured_in_project_matrix | ISSUES 91; requires a whole-cell isotherm and phase accounting |
| TU | elution | 0.1 | M | adopted_literature_operating_condition | S60 |
| elution_solid_liquid_ratio | elution | 1 | g sorbent/L | adopted_literature_operating_condition | S60 |
| elution_temperature | elution | 50 | degC | adopted_literature_operating_condition | S60 |
| k_elute | elution | 0.22 | h^-1 | literature-derived lower-bound proxy; not measured on GolB | S60 |
| kinetic_model | elution | PFO | dimensionless | provisional_literature_proxy | S60 |
| n_TU | elution | **null — model refuses to run** | dimensionless | **unmeasured** | Added 2026-08-11 by the audit. The equation was in EQUATIONS.md with no parameter behind it. It cannot be fill |
| phi | elution | 0.03 | dimensionless | 97% endpoint in the same acid-thiourea study used for k_elute | S60 |
| sulfuric_acid | elution | 0.1 | M | adopted_literature_operating_condition | S60 |
| M_r_reductase | reagent_arm | 70000 | g/mol | **assumed** | Used to turn g/L into uM. Replace when the construct is fixed. |
| N | reagent_arm | **null — model refuses to run** | copies/cell | not_separately_identifiable | RETIRED 2026-08-20 into alpha_N_beta above, for the same reason as alpha. THE VECTOR IS STILL WORTH RECORDING: |
| OD_induce | reagent_arm | 0.9 | OD600 | from_source_recipe | S35 |
| X_0 | reagent_arm | 0.02 | g dry weight/L | **assumed** | A 1:100 inoculation from a saturated overnight. Sets only how long the lag to induction is, not the plateau. |
| X_cap | reagent_arm | 2 | g dry weight/L | design choice | Sezonov, Joseleau-Petit & D'Ari 2007, J Bacteriol 189(23):8746-8749, doi:10.1128/jb.01368-07, for the LB ceiling of OD600 7; Ukkonen et al. 2011, Microb Cell Fact 10:107, doi:10.1186/1475-2859-10-107, for the measured shake-flask dry cell weights of 8.1, 10.3 and 19.7-21.1 g/L |
| alpha | reagent_arm | **null — model refuses to run** | mRNA/min per plasmid copy | not_separately_identifiable | RETIRED 2026-08-20 into alpha_N_beta above. It is not measurable separately from N and beta by anything this m |
| alpha_N_beta | reagent_arm | 500 | protein.min^-2.cell^-1 | sourced by proxy | Lumping follows Raue et al. 2009, Bioinformatics 25(15):1923-1929, on structural non-identifiability. Component anchors: T7 elongation about 5x E. coli RNA polymerase, and Studier & Moffatt 1986 for the 50 % of total cell protein ceiling; copy number from Sathiamoorthy & Shin 2012, PLoS ONE 7(10) e47259, 51 +/- 8 for the pBR322-derived pGEX-6p-1 |
| beta | reagent_arm | **null — model refuses to run** | protein/min per mRNA | not_separately_identifiable | RETIRED 2026-08-20 into alpha_N_beta above. It was never given a value of its own; GolB's 4.0 stood in, and it |
| burden | reagent_arm | 0.3 | dimensionless | sourced_from_the_burden_literature | 33 % growth-rate fall under IPTG-induced expression (metabolic-burden maintenance-coefficient literature); <45 % across hundreds of BioBricks, Nature Communications 2024 burden survey |
| concentration_factor | reagent_arm | **null — model refuses to run** | dimensionless | **unmeasured** | The mixing table in ISSUES.md item 48 shows why this matters: a lysate only 1.05x above target needs a 20:1 vo |
| delta_c | reagent_arm | 0.005 | min^-1 | sourced_from_the_turnover_literature | Global protein-turnover quantification in E. coli, Nature Communications 2024: degradation practically zero for most of the proteome in exponential growth; rapidly degrading component 2-7 % at about 1 h half-life |
| g_dw_per_OD600 | reagent_arm | 0.4 | g dry weight/L per OD600 unit | sourced_from_an_inconsistent_literature | BioNumbers E. coli cell-dry-weight per OD600 entries, about 0.36 g/L commonly cited, 0.3 to 0.5 usual range, strain and instrument dependent |
| lysis_yield | reagent_arm | 0.7 | dimensionless | sourced_from_the_lysis_literature | Ultrasonication of E. coli: about 30 % of recombinant protein remains with cell debris after one 15-min treatment, about 90 % global recovery after two, Biotechnology Techniques ultrasonication protocol literature |
| protein_target_g_per_L | reagent_arm | 0.2 | g/L | design choice | Was hard-coded in model.ipynb and tests/test_sensitivity.py until 2026-08-16. It sets E_tot and therefore the  |
| t_harvest_source_h | reagent_arm | 4 | h after induction | from_source_recipe | S35 |
| Rech_0 | reagent_arm.robust_design | 50 | uM | design_recommendation | IT IS NOT A NEW CHEMICAL. S35's own protocol is built on it: "The reaction was activated by adding 100 uL sodi |
| concentration_factor | reagent_arm.robust_design | 30 | dimensionless | design_recommendation | RAISED 2026-08-21 from 10 when the k_grow floor was anchored on a purified Au(III) reductase and fell sixty-fo |
| seed_frac | reagent_arm.robust_design | 0.5 | dimensionless | design_recommendation | Half of a previous batch, recycled. THE SEED IS NOT CONSUMED and it is not a reagent to buy: it is product hel |
| t_reduce_h | reagent_arm.robust_design | 96 | h | design_recommendation | NOT OPTIONAL. Nothing tested clears the worst corner in 24 h at any concentration. Time is the cheapest of the |
| worst_case_eta_reduce | reagent_arm.robust_design | 0.98 | dimensionless | derived | — |
| eta_ash | recovery | **null — model refuses to run** | dimensionless | out_of_scope | OUT OF SCOPE 2026-08-21, with the rest of physical recovery. |
| eta_phys | recovery | 1 | dimensionless | out_of_scope | Team decision 2026-08-16, confirmed permanent 2026-08-21. This is not an estimate of a recovery efficiency. It |
| eta_spin | recovery | **null — model refuses to run** | dimensionless | out_of_scope | OUT OF SCOPE 2026-08-21. A source was added earlier the same day and has been removed with it: sourcing a para |
| eta_wash | recovery | **null — model refuses to run** | dimensionless | out_of_scope | OUT OF SCOPE 2026-08-21, with the rest of physical recovery. |
| K_inh | reduction | 500 | uM | unmeasured proxy; sensitivity is scenario-dependent | — |
| Rech_0 | reduction | 50 | uM | design choice | Reagent and identity from S35; the 50 uM quantity is this project's own design choice, adopted 2026-08-21. S35's own 4.6 uM is in superseded. |
| k_grow | reduction | 0.082 | uM^-1.h^-1 | sourced by proxy | Mechanism from Watzky & Finke 1997, kept after the 2019 challenge and the 2020 Response. Band top from the ascorbate-PVP gold fit; see the note. SOURCES.md S51 and S52 |
| k_nuc | reduction | 0.96 | h^-1 | sourced by proxy | Mechanism from Watzky & Finke 1997, kept after the 2019 challenge and the 2020 Response. Value anchored on two gold systems, scaled for reductant; see the note. SOURCES.md S51 and S52 |
| k_ox | reduction | 0.02 | h^-1 | unsourced; measurable (air vs N2) | — |
| k_rech | reduction | 0.1 | uM^-1.h^-1 | unmeasured proxy; sensitivity is scenario-dependent | UNIT CORRECTED 2026-08-24. It read h^-1, which does not balance. The code uses v_rech = k_rech*E_ox*Rech, and  |
| mediator_0 | reduction | 0.1 | uM | in the source recipe, absent from every equation in this model | S35 |
| nu | reduction | 0.5 | mol reductase per mol Au | stoichiometric; 0.5 for Au(I), 1.5 for Au(III) | S63 |
| nu_rech | reduction | 1 | mol donor per mol protein recharged | stoichiometric_assumption | ISSUES 90; two-electron bookkeeping, not measured recharge yield |
| seed_frac | reduction | **null — model refuses to run** | dimensionless | **unmeasured** | The band is what the model was explored over, NOT a measurement. At a 4x concentration and 24 h it spans 92% t |
| seeding_on | reduction | False | — | switch | Finke-Watzky is autocatalytic, so the vessel spends its first hours building the catalyst it needs. t_ind = 1/ |

## A.4 Constants used at the handovers

Source file: `params/conversions.yaml`

| Parameter | Block | Value | Unit | Status | Source or basis |
|---|---|---|---|---|---|
| N_A | — | 6.02e+23 | mol^-1 | exact | SI definition |
| cells_per_g_dry_weight | — | 2.36e+12 | cells/g | sourced | [S30] Dennis & Bremer via BioNumbers; interpolated at our own mu |
| minutes_per_hour | — | 60 | min/h | exact | — |

**144 parameters in total. 30 of them are assumed, fitted, unmeasured, or awaiting a value.** Those are the ones worth your time.
