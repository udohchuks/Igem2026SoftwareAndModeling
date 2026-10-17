# Sources found while building this model

**Tier 2, record.** 41 papers, `S1` to `S41`, cited from every other document
and citing none of them. `AGENTS.md` section 11.

Papers located by literature search during the model walkthrough, with the
number each one supplies and where that number is used. This file is for
sources **found by us**, not the reference lists already inside the three
source documents.

Rule: a source is listed here only if it supplies a number, a bound, or a
structural fact that the model uses. A paper that is merely relevant does not
go here.

---

## Part I — Bioleaching

### The enzyme block, `k_syn` and `k_cat`

Searched 2026-08-10 for a measured enzyme synthesis rate per cell. **No direct
measurement exists**, and none is expected: synthesis rate per cell is a
modelling construct, not a quantity anyone assays. The two papers below reach
it indirectly.

**S1. Kanao T., et al. (2023).**
✅ **Independently verified 2026-08-10** against the PMC full text: 2.2 ± 0.37
and 2.5 ± 0.18 U mg⁻¹ both confirmed, as is the homodimer of 50 kDa subunits
(Table 1, "50 × 2"), and the 1.95 Å crystal structure describing Af-Tth as a
homodimer.

"Recombinant expression using the tetrathionate hydrolase promoter in
*Acidithiobacillus ferrooxidans*."
*Journal of Bioscience and Bioengineering.*
https://consensus.app/papers/details/ae6a84efbdd9539cb3a2d45e26a0b7f0/

- **Supplies:** specific activity of purified Af-Tth, **2.2 ± 0.37 U mg⁻¹**
  from recombinant *A. ferrooxidans*, and **2.5 ± 0.18 U mg⁻¹** for the same
  enzyme acid-refolded from *E. coli* inclusion bodies.
- **Also supplies:** `tetH` expression ratios by qRT-PCR, S⁰/Fe²⁺ = 68 ± 21
  and S₄O₆²⁻/Fe²⁺ = 181 ± 5. Useful if induction is ever modelled.
- **Used in:** `ISSUES.md` item 14, as the denominator of the TetH mass
  fraction.

**S2. Protze J., Müller F.-H., Lauber K., Naß B., et al. (2011).**
"An extracellular tetrathionate hydrolase from the thermoacidophilic archaeon
*Acidianus ambivalens* with an activity optimum at pH 1."
*Frontiers in Microbiology*, 39 citations.
https://consensus.app/papers/details/b2ffb8dd3ef65a23949a05f0d1087f12/

- **Supplies:** TTH activity in cell-free extract of tetrathionate-grown
  cells, **≈0.28 U mg⁻¹ total protein**. Also: 92% of activity is
  pseudo-periplasmic, enrichment to purity from that fraction is only
  2.1-fold, subunit mass 54 kDa, doubling time 9 h, final density up to
  8×10⁸ cells/mL.
- **Used in:** `ISSUES.md` item 14, as the numerator of the TetH mass
  fraction.
- **⚠️ Caveat:** this is an archaeon, not *Acidithiobacillus*. Combining S1
  and S2 assumes the two homologues have comparable turnover. It is a proxy,
  not a measurement.

**S3. Kanao T. (2024).** "Tetrathionate hydrolase from the acidophilic
microorganisms." *Frontiers in Microbiology*, 5 citations.
https://consensus.app/papers/details/b9118905e2495425bb7a03237b76b092/

- **Supplies:** review-level confirmation that Af-Tth is a dimer of ~50 kDa
  subunits, is periplasmic or outer-membrane, and is highly expressed on
  tetrathionate but not on iron.
- **Used in:** the 100 kDa molar mass in the `ISSUES.md` item 14 derivation.
- **Note:** this is reference **[1]** of the Part I source document. Listed
  again here because the walkthrough drew a specific number from it.

**S4. Yu Y., Liu X., Wang H., Li X., Lin J. (2014).**
"Construction and characterization of *tetH* overexpression and knockout
strains of *Acidithiobacillus ferrooxidans*." *Journal of Bacteriology*,
40 citations.
https://consensus.app/papers/details/53358a8638f3573888ffba6f3d66582f/

- **Supplies:** the structural fact that tetrathionate hydrolysis is mediated
  **only** by TetH. The knockout cannot grow on tetrathionate at all.
- **Why it matters:** this justifies Part I modelling hydrolysis as a single
  enzymatic term with no parallel route. Without it, the single
  Michaelis-Menten term is an assumption.
- **Also supplies:** the overexpression strain raises both tetrathionate
  utilisation rate and TetH activity, so `k_syn` is engineerable upward.

### The enzyme block, `Vmax` — RETIRED ROUTE, kept on the record

⚠️ **S5 no longer supplies `Vmax`.** The team confirmed *E. coli* throughout on
2026-08-11, and Eccleston's growth yield and maintenance coefficient are
*A. ferrooxidans* numbers that do not transfer. See `ISSUES.md` item 30. The
entry below is unchanged and is kept because the derivation is on the record.

**S5. Eccleston M., Kelly D. P. (1978).**
"Oxidation kinetics and chemostat growth kinetics of *Thiobacillus
ferrooxidans* on tetrathionate and thiosulfate."
*Journal of Bacteriology* **134**:718–727. 69 citations.
✅ **Independently verified 2026-08-10** against the primary record: growth
yield 12.2 and maintenance coefficient 1.01 both confirmed.
https://consensus.app/papers/details/e9b7fb7cedd350618966b8023cb23730/

- **Supplies three numbers**, all measured, that together give `Vmax` with no
  enzyme assay required:
  - specific growth rate on 10 mM tetrathionate, pH 2.5: **0.092 h⁻¹**
  - true growth yield, chemostat, tetrathionate-limited: **12.2 g dry weight
    per mol tetrathionate**
  - maintenance coefficient: **1.01 mmol tetrathionate g⁻¹ h⁻¹**
- **Also supplies:** apparent `K_m` for tetrathionate oxidation, 0.13 to
  8.33 mM, pH dependent. Compare Part I's transcribed range of 50–2400
  µmol/L, that is 0.05–2.4 mM. The two overlap.
- **Derived:** growth demand + maintenance = 8.55 mmol g⁻¹ h⁻¹, which is
  **142.5 µmol per gram dry weight per minute**. At 0.1 g/L this gives
  `Vmax` = 14.3 µmol L⁻¹ min⁻¹.
- **Was used in:** `params/leach.yaml :: enzyme_capacity`, now under
  `retired_A_ferrooxidans_route`. `src/leach.py :: specific_tetrathionate_demand`
  is kept but is not the operating route.
- **⚠️ Caveat 1, organism and setting.** *Thiobacillus ferrooxidans* is the
  former name of *Acidithiobacillus ferrooxidans*, so the organism is right.
  The measurement is from 1978 and from a chemostat, not a leaching reactor.
- **⚠️ Caveat 2, and it is the important one.** These numbers describe what
  cells **do** consume while growing at 0.092 h⁻¹. The model's `Vmax` is what
  they **can** consume at top speed. A growing culture is not necessarily
  working flat out, so **14.3 µmol L⁻¹ min⁻¹ should be read as a lower bound**,
  not a central estimate. The true capacity is at or above it.
  Two consequences: gold dissolution predicted from this `Vmax` is
  conservative, and the upper end of the stated range matters more than the
  lower end.
- **Cross-check:** the independent route through S1 and S2 gives 28 µmol L⁻¹
  min⁻¹ at 0.28 g/L, against 39.9 by this route. Two unrelated methods agree
  to within 30%.

---

## Part II / Part III — GolB selectivity and what capture actually is

Searched 2026-08-10 to answer one question: does GolB bind gold uniquely, with
no competition? **The answer is no, and the reason is not the one expected.**

**S6. Checa S., Soncini F. C., et al. (2007).** "Bacterial sensing of and
resistance to gold salts." *Molecular Microbiology*, 129 citations.
https://consensus.app/papers/details/7e569b5eaa095eec8cc84bb88b0ca9f1/

- **Supplies:** the discovery of GolS, a MerR-family regulator "highly
  selective for Au ions", with selectivity traced to a metal-binding motif.
- **⚠️ Note carefully:** this is about **GolS**, the transcriptional
  *regulator*, not GolB, the binding *protein*. They are different molecules.

**S7. Checa S., Soncini F. C. (2011).** "Bacterial gold sensing and
resistance." *BioMetals*, 32 citations.
https://consensus.app/papers/details/49867f1103fa5d2d84d670d098c98038/

- **Supplies:** the mechanism of selectivity. A single dithiolate coordination
  is tuned to **lower** affinity for Cu(I) while maintaining or raising
  affinity for Au(I). "GolS not only privileges the binding of Au(I) over
  Cu(I) or Ag(I)..."
- **Supplies also:** gold ions "enter into the cells by non-specific intake".
- **⚠️ Again GolS, not GolB.**

**S8. Ibáñez M. M., Checa S. K., Soncini F. C. (2013).** "Dissecting the metal
selectivity of MerR monovalent metal ion sensors in Salmonella."
*Journal of Bacteriology*, 22 citations.
https://consensus.app/papers/details/ab60717bbd305aea9c7a3fd29c9f6d49/

- **Supplies:** GolS shows **higher activation by Au than by Ag or Cu**, and
  the residues responsible are at positions 113 and 118. CueR, by contrast,
  "responds similarly to Au, Ag, or Cu".
- **Supplies the important qualifier:** selectivity is *higher activation by*,
  not *exclusive binding of*. Ag and Cu still activate GolS, just less.

**S9. Tolbatov I., Re N., Coletti C., Marrone A. (2019).** "An insight on the
gold(I) affinity of golB protein via multilevel computational approaches."
*Inorganic Chemistry*, 18 citations.
https://consensus.app/papers/details/310edd919d3155b8ac0080632c1cd4f6/

- **The only GolB-specific selectivity evidence found.** Concludes the
  protein environment favours a thiol-thiolate protonation state, "thus
  **probably** enhancing the binding selectivity for Au(I) compared to other
  cations."
- **⚠️ This is a computational study and the claim is hedged.** No measured
  competitive binding constant for GolB against Cu(I) or Ag(I) was found in
  this search.
- **Also supplies:** GolB switches between sequestration and release states by
  changing the Cys10–Cys13 distance. Relevant to elution.

**S10. Wei W., et al. (2015).** "Structural insights and the surprisingly low
mechanical stability of the Au–S bond in the gold-specific protein GolB."
*JACS*, 51 citations.
https://consensus.app/papers/details/bca1082312b857d2a0f1bd1d56fa7a2e/

- **Supplies:** apo-GolB and Au(I)-GolB crystal structures. Au–S rupture force
  **165 pN**, against ~1,000 pN for Au–S on a gold surface, and an
  unusually long Au–S bond.
- **Why it matters:** the protein–gold bond is **six times weaker** than the
  gold–gold-surface bond. Favourable for elution, unfavourable for holding on
  during washing. Neither Part II nor Part III uses this number.
- This is already reference [GolB structure] in the Part II document.

**S11. Chen S., et al. (2020).** "Interfacial properties of
mercaptopropyl-functionalised silica gel and its adsorption performance in the
recovery of gold(I) thiosulfate complex." *Chemical Engineering Journal*,
71 citations.
https://consensus.app/papers/details/2efb43997cd0558e91b4cdbc6d687d92/

- **This paper answers the mechanism question the biology papers do not.**
  A thiol-functionalised surface captures gold from a thiosulfate leachate by
  **ion exchange between the thiol groups and Au(S₂O₃)₂³⁻**, with charge
  transfer from the ligand to gold(I).
- **So capture is a ligand-exchange competition**, thiol versus thiosulfate,
  not simple binding of a free ion.
- **Independent confirmation of Part III's elution chemistry:** the loaded
  material is eluted with **thiourea plus HCl**, exactly the mechanism
  Part III §3 specifies.
- **Supplies:** thiosulfate concentration is listed among the variables that
  affect adsorption. That dependence appears nowhere in Part II or Part III.

**S12. Chen Y., et al. (2019).** "Grafting of organic sulfur-containing
functional groups on activated carbon for gold(I) adsorption from thiosulfate
solution." *Hydrometallurgy*, 56 citations.
https://consensus.app/papers/details/a2da90f101075589b54f490197ed127b/

- **Direct confirmation of the capture mechanism.** "The adsorption of
  [Au(S₂O₃)₂]³⁻ onto S-AC involved a **gold(I) thiolate and disulfide
  interchange mechanism**", proved by XPS, FT-IR, BET and SEM.
- **Supplies the operating window:** the thiol adsorbent "worked well at a pH
  of about 9.0 and thiosulfate concentration of about **0.1 mol/L**".
- **Why that matters:** 0.1 mol/L is 100,000 µmol/L, which is what our own
  Part I leach produces. Thiol capture from a full-strength thiosulfate
  leachate is therefore demonstrated, not speculative.
- **⚠️ But at pH 9**, and the leach runs acidic. See `ISSUES.md` item 23.
- **Note the word "disulfide".** Capture is not purely ligand exchange; a
  thiol/disulfide redox interchange is part of it.

**S13. Fotoohi B., Mercier L. (2015).** "Some insights into the chemistry of
gold adsorption by thiol and amine functionalized mesoporous silica in
simulated thiosulfate system." *Hydrometallurgy*, 49 citations.
https://consensus.app/papers/details/8c280523464c5af8806316bd6103915d/

- **Supplies the stoichiometry:** thiol-bearing silica shows monolayer
  behaviour "approaching an ultimate **metal:ligand = 1:1** capacity".
- **Supplies two levers:** capacity rises at alkaline pH (~10.5) and at higher
  solution oxidation potential (Eh ~300 mV).
- **A warning about the alternative chemistry:** amine groups gave capacities
  beyond monolayer chemisorption, and gold was often not detectable by XPS.
  The authors propose partial electrochemical reduction to metallic gold
  nanoparticles during contact. If that happens on our cells it would be
  reduction occurring at the capture step, which no part of the model allows.

**S14. Green T. A., Roy S. (2006).** "Speciation analysis of Au(I)
electroplating baths containing sulfite and thiosulfate."
*Journal of The Electrochemical Society*, 47 citations.
https://consensus.app/papers/details/2b17559cb2445d78a151249eae50f056/

- **Supplies:** "The thiosulfate complex Au(S₂O₃)₂³⁻ is only dominant under
  **acidic** conditions." At neutral or basic pH, mixed complexes dominate
  when sulfite is present.
- **Why it matters:** the species entering capture depends on the pH the
  leachate is at when it gets there.

### pH: the regime conflict inside Part I

**S15. Rouchalová D., et al. (2020).** "Bioleaching of iron, copper, lead, and
zinc from the sludge mining sediment at different particle sizes, pH, and pulp
density using *Acidithiobacillus ferrooxidans*." *Minerals*, 58 citations.
https://consensus.app/papers/details/e645985517a15fbaae90168329b01600/

- **Supplies the organism's operating pH:** experiments run at **pH 1.6–2.0**,
  with the highest dissolution rates at **pH 1.8**.
- Confirms Eccleston's pH 2.5 growth optimum sits at the top of the usable
  range, not the middle.

**S16. Redrovan A. S., et al. (2025).** "Gold leaching from an auriferous ore
by alkaline thiosulfate–glycine–copper solution." *Metals*, 8 citations.
https://consensus.app/papers/details/56176b08e5bf5482b3bf8a2dfe1cb8ab/

- **Supplies the chemistry's operating pH:** thiosulfate gold leaching
  optimised over **pH 9.3–10.5**, best at pH 9.3, giving 89.3% gold in 6 h.
- Also reports ammoniacal thiosulfate at 58% in 6 h, and notes "the
  limitations of thiosulfate degradation in ammoniacal systems".

**S17. Lee S., et al. (2024).** "Exploring non-ammoniacal thiosulfate gold
leaching and limited gold recovery from a refractory gold ore oxidized in
alkaline pressure conditions." *Journal of Sustainable Metallurgy*.
https://consensus.app/papers/details/060e81afb09f535e972c770f42b61814/

- **Supplies:** a second independent non-ammoniacal thiosulfate system, again
  alkaline, optimum 0.14 M thiosulfate with 0.78 mM cupric ion at 50 °C.
- Confirms 0.1–0.15 M thiosulfate as the standard working concentration,
  matching what Part I's model produces.

### `X_max`: how dense can the capture culture actually be?

Searched 2026-08-10 after the `q_max` adoption made `X_max` the remaining
lever. **The earlier claim in this repository that "50 g/L is a thick paste"
and that the biomass route was closed was wrong.**

**S18. Ganjave S. D., et al. (2021).** "High cell density cultivation of
*E. coli* in shake flasks for the production of recombinant proteins."
*Biotechnology Reports*, 39 citations.
https://consensus.app/papers/details/b85507dd0b4050d68e8440da638e5e48/

- **Supplies:** **20.7 g dry cell weight per litre in shake flasks**, using a
  syringe-pump fed-batch of glycerol and yeast extract over 24 h.
- **Why it matters:** this is the density reachable without a bioreactor,
  which is the realistic ceiling for an iGEM team.

**S19. Korz D. J., Rinas U., Hellmuth K., Sanders E. A., Deckwer W.-D. (1995).**
"Simple fed-batch technique for high cell density cultivation of *Escherichia
coli*." *Journal of Biotechnology*, 451 citations.
https://consensus.app/papers/details/2023a9785ef35238a82ec2b9bb39364a/

- **Supplies:** **128 g/L DCW on glucose and 148 g/L on glycerol**, by
  carbon-limited exponential feeding held below the growth rate that causes
  acetate formation.
- This is the standard reference for what *E. coli* density is achievable at
  all. It is 26–30× Part III's assumed `X_max` = 5 g/L.

**S20. Kumar S. R., et al. (2026).** "High cell density fermentation strategy
for high-level soluble expression of a GLP-1 analogue in *Escherichia coli*."
*Fermentation*.
https://consensus.app/papers/details/43920cde759f55d19f2e5c69edbffbda/

- **Supplies:** **88.9 g/L DCW** in a modern optimised fed-batch, with soluble
  recombinant protein expressed at the same time.
- **Why that last point matters:** it shows high density and heterologous
  expression are compatible, which is the combination this project needs.

**S23. Shiloach J., Fass R. (2005).** "Growing *E. coli* to high cell density
— a historical perspective on method development."
*Biotechnology Advances*, 479 citations.
https://consensus.app/papers/details/c9bf974b354f51aca1e19461e49bc474/

- **Supplies the record:** batch, fed-batch and dialysis techniques together
  "made it possible to grow *E. coli* to cell densities of up to **190 g/l
  (dry weight)**, while avoiding media precipitation and preventing acetate
  accumulation".
- **This is the ceiling to quote.** It is a review of the whole field, not a
  single result.

**S21. Agarwal A., et al. (2020).** "A review on valorization of biomass in
heavy metal removal from wastewater." *Journal of Water Process Engineering*,
153 citations.
https://consensus.app/papers/details/a685390a17355cfdb04c6240f42c816c/

- **Supplies the alternative architecture:** fixed-bed columns of immobilised
  biomass, with desorption "mostly carried out via acidic eluent", matching
  Part III's elution step.
- **Supplies the key structural point:** biosorbents in these studies are
  routinely **non-viable**. Dead or immobilised biomass still binds metal.

**S22. Meringer A., et al. (2021).** "Removal of copper and/or zinc ions from
synthetic solutions by immobilized, non-viable bacterial biomass."
*Journal of Biotechnology*, 17 citations.
https://consensus.app/papers/details/81b6ab2a835750fcadb09f01cbc6a0c0/

- **Supplies:** a non-viable *Pseudomonas putida* biosorbent in agar beads,
  reused over **ten adsorption/desorption cycles** without losing capacity.
- **Supplies a warning relevant to issue 22:** in mixed-metal solutions,
  capacity for each metal fell by about half, and "in 10:1-ratio solutions,
  the metal in greater proportion was better adsorbed". Our leachate is
  copper-rich and gold-poor.

### The eluent, which is not yet finalised

**S24. Niu H., et al. (2024).** "Gold recovery from chloride leach solution of
TCCA using D301 anion exchange resin and elution with thiourea."
*Hydrometallurgy*, 12 citations.
https://consensus.app/papers/details/6063a66567b35047b327b152ab1b5979/

- **Supplies the best documented eluent formulation:** among several tested,
  **0.4 mol/L thiourea + 0.8 mol/L HCl** achieved **95.7 ± 0.3% desorption in
  80 minutes**. That is `φ` ≈ 0.043, against the 0.13 currently in the model.
- **Note the composition.** It beats 1 M thiourea alone while using *less*
  thiourea, because the acid is part of the eluent rather than a separate
  step. Acid and thiourea together, not either alone.
- **Also supplies:** regeneration held up over three cycles, 91.2% efficiency,
  adsorption still 95.3%.

**S25. Sasaki K., et al. (2024).** "Complete gold extraction and recovery from
double refractory gold ores by thiourea after bio-oxidation."
*Hydrometallurgy*, 11 citations.
https://consensus.app/papers/details/ca29cab05df05ee49cd148f5076867b4/

- **Supplies:** thiourea under strongly acidic conditions reached ~100% gold
  extraction in 12 h with no re-adsorption, after a bio-oxidation step.
- **Supplies a warning:** iron-bearing sulfides cause **thiourea
  decomposition**. Bio-oxidation was needed first to remove them. Our leachate
  is a sulfur system carrying copper, so thiourea stability in it is an open
  question.
- Confirms the eluted species is `Au(CS(NH₂)₂)₂⁺`, a **cation**, in contrast to
  the anionic `Au(S₂O₃)₂³⁻` that enters capture. The charge reverses across
  the elution step.

**S26. Ray D., et al. (2022).** "Thiourea leaching: an update on a sustainable
approach for gold recovery from e-waste." *Journal of Sustainable Metallurgy*,
67 citations.
https://consensus.app/papers/details/0c18227c97d352258b9f192d055bd07a/

- **Supplies context:** a review of thiourea for gold from e-waste
  specifically, including hybrid bioleaching systems. The closest published
  analogue to this project's architecture.
- **No number is taken from it**; listed because it is the right entry point
  for the eluent decision.

### The elution rate law itself

Added 2026-08-15. Section 6.2 of `REVIEW.md` derived its rate equation from
scratch without naming it. Both candidates are standard models; S34 is the one
the model adopted on 2026-08-16.

**S33. Lagergren S. (1898).** "Zur Theorie der sogenannten Adsorption gelöster
Stoffe." *Kungliga Svenska Vetenskapsakademiens Handlingar* 24(4), 1–39.

- **Supplies the superseded law.** The pseudo-first-order (PFO) law,
  `dq/dt = k₁(q_e − q)`, applied backwards with `q_e = φC_0`. It was the model
  until 2026-08-16 and is kept as `recovery_chain.eta_elute_pfo`.
- **Supplies no number.** `k_elute` = 2.0 h⁻¹ is still unsourced.
- **Supplies a warning, via the secondary literature:** PFO is widely reported
  to fit only the first 20–30 minutes of a chemisorption time course. Our wash
  runs 3–6 h.

**S34. Ho Y. S., McKay G. (1999).** "Pseudo-second order model for sorption
processes." *Process Biochemistry* 34(5), 451–465.
doi:10.1016/S0032-9592(98)00112-5

- **Supplies the rate law the model uses**, `dq/dt = k₂(q_e − q)²`,
  implemented as `recovery_chain.eta_elute`. Adopted 2026-08-16.
- **Supplies the reason to take it seriously:** of 12 sorption systems already
  published as first order, PSO gave the higher correlation coefficient in
  **all 12**. The gold work behind S24 and S25 reports PSO as well.
- **Supplies the size of the disagreement:** identical `(1 − φ)` ceiling,
  but 95 % of it costs `3/k` under PFO and `19/k` under PSO. About 4× the
  contact time.
- **Supplies no number for this project.** `k_elute` = 2.0 h⁻¹ remains
  unsourced and provisional, because the eluent is unchosen. ISSUES.md items
  28 and 47; one time course fills both.

### The reducing protein, and the reaction it was demonstrated in

Added 2026-08-16. Until this date the repository modelled a reduction step
whose protein had no citation and whose reactions were never written down.

**S35. Erasmus M., Idris O. A., Adetunji A. I., Cason E. D. (2024).**
"Biogenic synthesis and characterization of gold nanoparticles using
transformed mesophilic *Escherichia coli* BL21 and thermophilic *Thermus
thermophilus* HB27." *Biologia* 79:2605-2619.
doi:10.1007/s11756-024-01733-2

- **Supplies the protein.** ABC transporter, peptide-binding protein from
  *Thermus scotoductus* SA-01, a reductase-like protein already known to
  reduce U(VI), Fe(III), Cr and Au. Runs at **~70 kDa** on SDS-PAGE, which is
  the `M_r_reductase` = 70000 the model uses to turn g/L into uM.
- **Supplies the expression host and route**, which item 48 needs: *E. coli*
  BL21(DE3), pET-22b(+) without a His-tag or pET-28b(+) with an N-terminal
  His-tag, grown to OD600 0.8-1.0, induced with **1 mM IPTG**, harvested after
  **4 h**.
- **Supplies the reaction, which is item 49.** 1 mL total: purified protein,
  HAuCl4 as **Au(III)**, **methyl viologen** as electron shuttle, **sodium
  dithionite** as the electron source, phosphate buffer pH 7.4, 24 h.
  Optimum quoted at 0.5-2 mM HAuCl4; nanoparticles read at 520-560 nm.
- **Supplies `Rech_0` and the mediator concentration, read 2026-08-17.** 100 uL
  of 46 uM dithionite and 100 uL of 1 uM methyl viologen into 1000 uL, so
  **4.6 uM** and **0.1 uM** final. The dithionite *activates* the reaction. It
  is added to purified protein, so `Rech` is a dosed reagent and **not** lysate
  carryover, which this repository assumed until that date. Item 51.
- **⚠️ Its own electron ledger does not close, which caps what may be quoted
  from it.** 4.6 uM of dithionite at 2 e- supplies 9.2 uM of electrons against
  1500-30000 uM demanded by 0.5-10 mM Au(III) at 3 e-: **0.6% down to 0.03%**.
  Consistently, the paper reports colour and TEM and never a conversion or a
  yield. No efficiency in this source corroborates our `eta_reduce`. Item 51.
- **Supplies a control worth having.** Boiled protein does not reduce gold, so
  the activity belongs to the folded protein and is not a buffer artefact.
- **Supplies pH and temperature ranges.** Nanoparticles formed at every pH
  tested, optimum **5.5-9.0** for the mesophilic host at 30 C. That brackets
  our pH 7.4 comfortably and is one of the few places in this project where a
  requirement is not in conflict.
- **⚠️ Does not supply what the model most needs.** No protein yield per litre
  of culture, no lysis recovery, and no experiment on Au(I) or on thiourea
  complexes. Items 48 and 49.
- **Recipe re-read from the PDF, 2026-08-21**, and it confirms every number
  this repository took from it. Verbatim: *"An aliquot of 100 µL of the
  purified protein was reacted with 100 µL gold (III) solution (HAuCl₄;
  0–10 mM), 100 µl methyl viologen (1 µM), 100 µL phosphate buffer (50 mM;
  pH 7.4), and 500 µL double distilled water. The reaction was activated by
  adding 100 µL sodium dithionite (46 µM) dissolved in sodium hydrogen
  carbonate (100 µM)."* Total 1000 µL, so **4.6 µM dithionite and 0.1 µM
  methyl viologen final**, exactly as `reduction.Rech_0` and
  `reduction.mediator_0` carry them.
- **SODIUM DITHIONITE IS NOT OPTIONAL IN THE SOURCE PROTOCOL.** The paper's
  own word is *activated*. Any question of whether to use it is settled by the
  method itself; only the quantity is open.
- **⚠️ An internal tension worth recording.** The concentration and pH series
  for the mesophilic host were run **at 30 °C**, yet the temperature results
  state that *"Nanoparticle formation in mesophilic host proteins was observed
  to begin at 55 °C, with optimum formation at 65 °C."* If formation begins at
  55 °C, the 30 °C series should show little. **Left standing; not resolved
  here.** Temperature is deferred (item 29), so nothing in this repository
  models it, and the reduction stage is silent about temperature altogether.

**S36. Protein-mediated gold reduction is stepwise.** Reviewed in the
gold-nanoparticle biosynthesis literature: Au(III) is reduced to Au(I) and
further to Au(0) by hydroxyl, amine, carboxyl, phospho or sulfhydryl groups of
proteins, which then stabilise the particle.
https://www.dovepress.com/a-review-on-the-synthesis-and-functionalization-of-gold-nanoparticles--peer-reviewed-fulltext-article-IJN

- **Supplies the argument that defuses half of item 49.** Au(I) is not a
  different reaction from the demonstrated one; it is the intermediate inside
  it. Every Au(III) demonstration already contains an Au(I) reduction step.

**S37. Erasmus M., et al. (2014).** "Gold nanoparticle synthesis using the
thermophilic bacterium *Thermus scotoductus* SA-01 and the purification and
characterization of its unusual gold reducing protein." *Gold Bulletin* /
*Discover Metals*. doi:10.1007/s13404-014-0147-8

- **Supplies the mechanism:** a **cysteine-disulfide bridge electron shuttle**
  is proposed for Au(III) reduction. This is the basis of `nu` = 0.5, two
  electrons per disulfide.
- **Supplies independent support for the rate model:** the protein also acts
  as **nucleation seed sites** that initiate and direct particle synthesis.
  That is the `k_nuc` term in Finke-Watzky, and it is the only outside support
  that term has.
- **Supplies context:** this is protein promiscuity. A transporter protein
  doing redox work it did not evolve for.

**S38. The di(thiourea)gold(I) complex as a nanoparticle precursor.**
[Au{S=C(NH2)2}2][SO3Me], *Zeitschrift fur Naturforschung B*, 2019.
doi:10.1515/znb-2019-0213. With the thiourea-leaching potential-pH literature,
*Hydrometallurgy*, for the couple.

- **Supplies the reassurance:** Au(I)-thiourea is itself a documented precursor
  for preparing gold nanoparticles, so the species we deliver is reducible.
- **Supplies the warning:** the Au(CS(NH2)2)2+ / Au couple sits near
  **+0.38 V**, against about +1.00 V for AuCl4- / Au. Our gold is roughly
  **0.6 V less oxidising** than the gold the protein was demonstrated on.
- **Used in:** ISSUES.md item 49.

**S39. Watzky M. A., Finke R. G. (1997).** "Transition Metal Nanocluster
Formation Kinetic and Mechanistic Studies. A New Mechanism When Hydrogen Is the
Reductant: Slow, Continuous Nucleation and Fast Autocatalytic Surface Growth."
*Journal of the American Chemical Society* 119(43):10382-10400.

- **Supplies the reduction rate law.** Two elementary steps, `A -> B` slow
  continuous nucleation and `A + B -> 2B` autocatalytic surface growth, giving
  `-d[A]/dt = (k1 + k2[B])[A]`. That is the reduction rate `v` in
  `src/sensitivity.py` exactly, carrying only the donor factor `E_red/E_tot`,
  which equals 1 in the excess limit the source assumes.
- **Supplies the shape.** An induction period followed by a rapid sigmoidal
  fall in precursor, which is the prediction section 6.3 asks the wet lab to
  test first. Classical LaMer theory does not produce it.
- **Robust.** The mechanism survived a published "disproof" and a rebuttal in
  *Chemistry of Materials*, and it is applied well outside nanoparticles,
  including to amyloid fibril formation.
- **⚠️ Does not supply the min().** Finke-Watzky describes particle formation
  alone. Coupling it to an electron-supply branch by taking the minimum is this
  repository's own choice, and it is the classical rate-determining-step
  approximation rather than a standard kinetic form. Justified here only
  because the two branches differ by about 57,000x and never cross. ISSUES.md
  item 27 and REVIEW.md section 6.3.

**S40. Amirjani A., Haghshenas D. F. (2018).** "Modified Finke-Watzky
mechanisms for the two-step nucleation and growth of silver nanoparticles."
*Nanotechnology* 29(50):505602.

- **Supplies the precedent for making the rate law explicit rather than
  assumed.** The authors drop the usual simplifying assumptions, `[A]0 >> [A]`
  and `k2[A] >> k1`, and treat nucleation as reversible, on the grounds that
  the linearised F-W form did not describe their data.
- **Used in:** ISSUES.md item 50, as the justification for carrying the
  electron donor explicitly instead of assuming excess. Our reason is
  different from theirs, but the principle is the same: do not assume a
  condition that fails across the operating range.
- **No number is taken from it.** Their system is silver with borohydride.

**S41. Finke R. G. and co-workers, the three- and four-step extensions.**
"Nanocluster nucleation, growth, and then agglomeration kinetic and mechanistic
studies: a more general, four-step mechanism involving double autocatalysis,"
*Chemistry of Materials*, 2005, and the supported-nanoparticle four-step study,
2014.

- **Supplies what we deliberately do not model.** Beyond the two steps, the
  lineage adds bimolecular agglomeration `B + B -> C` and autocatalytic
  agglomeration `B + C -> 1.5C`. **Those steps are what set the particle size
  distribution.**
- **Why it is listed anyway:** section 6.4 was descoped on 2026-08-16, so
  particle size no longer enters `eta_total`. If physical recovery is brought
  back into scope, this is the route to *predicting* particle size rather than
  treating it as an unmeasured input. ISSUES.md items 50 and the section 8
  row on particle size.

---

## Added 2026-08-11 by the source audit

Found by reading the full texts of the papers already cited. All four were
retrieved through PubMed.

**S27. Kanao T., Matsumoto C., Shiraga K., Yoshida K., Takada J., Kamimura K.
(2010).** "Recombinant tetrathionate hydrolase from *Acidithiobacillus
ferrooxidans* requires exposure to acidic conditions for proper folding."
*FEMS Microbiology Letters* **309**(1):43–47.
[DOI](https://doi.org/10.1111/j.1574-6968.2010.02019.x) — PMID 20546308
✅ **verified against the PubMed record 2026-08-11.**

- **The finding that changes Part I.** "The heterologous expression of
  *Af-tth* in *Escherichia coli* resulted in the formation of **inclusion
  bodies of the protein in an inactive form**." Activity was recovered only
  after solubilising in 6 M guanidine hydrochloride and refolding at **pH 4.0**
  for 14 h at 4 °C.
- **"*Af*-Tth required exposure to an acidic environment during protein folding
  for activation."** Not incidental: the authors tie it to the enzyme's outer
  membrane location in an acidophile.
- **Also supplies a competing specific activity: 21.0 ± 9.4 U mg⁻¹**, which is
  **8 to 10× the 2.2 and 2.5 U mg⁻¹ of [S1]**, from the same group and the same
  protein. See `ISSUES.md` item 34.
- **Used in:** `ISSUES.md` items 32 and 34.

**S28. Kanao T., et al. (2013).** "Crystallization and preliminary X-ray
diffraction analysis of tetrathionate hydrolase from *Acidithiobacillus
ferrooxidans*." *Acta Cryst. F* **69**:692–694.
[DOI](https://doi.org/10.1107/S1744309113013419) — PMID 23722856
✅ **verified 2026-08-11.**

- **Independent replication of S27:** "expressed as inclusion bodies in
  recombinant *E. coli*. Recombinant *Af*-Tth was activated by refolding under
  acidic conditions."
- Third paper by the same group reporting the same outcome.

**S29. Jose J., Meyer T. F. (2007).** "The autodisplay story, from discovery to
biotechnical and biomedical applications." *Microbiol. Mol. Biol. Rev.*
**71**(4):600–619. [DOI](https://doi.org/10.1128/MMBR.00011-07) — PMC2168652.
With **Jose J. (2005)**, *Appl. Microbiol. Biotechnol.* **69**:607–614,
[DOI](https://doi.org/10.1007/s00253-005-0227-z).
✅ **verified 2026-08-11.**

- **Supplies `P_s,max`**, which had no entry in this file despite anchoring the
  whole engineering target. "Autodisplay facilitates the export of **more than
  100,000 recombinant molecules per single cell**", and the 2005 review says
  "**more than 10⁵** recombinant molecules per single cell".
- **⚠️ Read the words "more than".** `P_s,max` = 1×10⁵ is a **demonstrated
  floor, not a hard ceiling.** `ISSUES.md` item 2's open sub-question is
  answered, and the answer weakens the framing: the 0.2964 engineering target
  is a design anchor, not a physical limit.
- **Also supplies:** autodisplay permits oligomerisation of subunits on the
  surface, which matters because TetH is a homodimer.
- **Used in:** `params/expression.yaml :: P_s_max`; `ISSUES.md` items 2 and 26.

**S30. Dennis P. P., Bremer H., via BioNumbers.** *E. coli* dry mass per cell
against growth rate.
https://book.bionumbers.org/how-big-is-an-e-coli-cell-and-what-is-its-mass/
✅ **verified 2026-08-11.**

- **Supplies:** dry mass per cell is **148 fg at a 100 min doubling time and
  865 fg at 24 min**, "over a 5-fold difference depending upon the growth
  rate". Faster growth means larger cells.
- **Why it matters:** `params/conversions.yaml` uses 0.28 pg = 280 fg, which
  sits near the slow end. The model runs the culture at `μ` = 1.2 h⁻¹, a
  **35 min** doubling time, where the interpolated mass is about 415 fg.
- **Used in:** `ISSUES.md` item 33.

---

## Added 2026-08-12 with Part I's two finished models

Part I's author supplied a reference list with both write-ups. Two entries are
new to this file and both carry numbers the model now uses.

**S31. Senanayake G. (2005).** "A surface adsorption/reaction mechanism for
gold oxidation by copper(II) in ammoniacal thiosulfate solutions."
*J. Colloid Interface Sci.* **286**, 253–257.

- **Supplies:** the thiosulfate adsorption constant `K_ads` = **172–510 M⁻¹**,
  whose reciprocal is the half-saturation `K_S2O3` = **1960–5800 µmol/L**.
  Part I uses the midpoint, 3900.
- **Why it matters:** this replaced a placeholder of 5.0×10⁴ that this
  repository had carried with `status: calibrate` and no source. The
  placeholder sat 8.6× above the top of the measured band, and the correction
  moves gold recovered at 72 h from 22.6% to 38.4%.
- **Used in:** `params/leach.yaml :: gold_leaching.K_S2O3`; `ISSUES.md` item 42.

**S32. Kanao T., et al. (2010).** "Recombinant tetrathionate hydrolase from
*Acidithiobacillus ferrooxidans* requires exposure to acidic conditions for
proper folding." *FEMS Microbiol. Lett.* **309**(1), 43–47.

- **Supplies:** recombinant TetH expressed in *E. coli* forms inactive
  inclusion bodies, and activity is recovered only by refolding at acidic pH.
- **Why it matters:** this is the paper behind the blocking item 32, and Part I
  cites it in his sequential write-up as reference [19]. It is also the
  strongest argument *for* the three-vessel design: harvesting, extracting and
  refolding the enzyme outside the cell is the published procedure, and the
  sequential process does exactly that.
- **Used in:** `ISSUES.md` items 32 and 36.

**S40. Sezonov G., Joseleau-Petit D., D'Ari R. (2007).** "*Escherichia coli*
physiology in Luria-Bertani broth." *J. Bacteriol.* **189**(23), 8746–8749.
doi:10.1128/jb.01368-07

- **Supplies:** LB supports growth to an OD600 of about 7, and growth stops for
  want of a usable carbon source — LB's carbon is catabolisable amino acids,
  not sugar. Steady-state growth has already ceased by OD600 0.3.
- **Why it matters:** it puts a ceiling under the low end of `X_cap`, which had
  been `status: assumed` with `source: null`. The adopted 2.0 g/L is OD600 5,
  below this ceiling, so the value is conservative rather than invented.
- **Used in:** `params/recovery_chain.yaml :: reagent_arm.X_cap`; `ISSUES.md`
  item 67.

**S41. Ukkonen K., Vasala A., Ojamo H., Neubauer P. (2011).** "High-yield
production of biologically active recombinant protein in shake flask culture by
combination of enzyme-based glucose delivery and increased oxygen transfer."
*Microb. Cell Fact.* **10**, 107. doi:10.1186/1475-2859-10-107

- **Supplies:** measured shake-flask dry cell weights — 8.1 g/L at OD600 30 in
  Terrific Broth and ZYM-5052, 10.3 g/L at OD600 38 in EnBase in an Erlenmeyer,
  and 19.7–21.1 g/L at OD600 73–78 in EnBase in an Ultra Yield flask.
- **Why it matters:** `X_cap` scales the reagent-arm yield linearly and with no
  unknown in it, so this band is the cheapest lever on the shortfall of item
  52. Terrific Broth alone takes it from 18.5× to 4.6×.
- **⚠️ What it does not supply.** The host is *E. coli* RB791 with pQE30, a T5
  promoter — not BL21(DE3) with pET. **The biomass transfers; the expression
  system does not.** Nothing about T7 promoter strength may be taken from it.
- **Used in:** `params/recovery_chain.yaml :: reagent_arm.X_cap`; `ISSUES.md`
  item 67.

**S42. Sathiamoorthy S., Shin J. A. (2012).** "Boundaries of the origin of
replication: creation of a pET-28a-derived vector with p15A copy control
allowing compatible coexistence with pET vectors." *PLoS ONE* **7**(10),
e47259. doi:10.1371/journal.pone.0047259

- **Supplies the reductase copy number.** qPCR in one pair of hands:
  **51 ± 8** copies per cell for pGEX-6p-1, which is pBR322-derived and
  rom-intact like pET-24(+), and 18 ± 4 for a p15A derivative. Also confirms
  that pET vectors carry the full pBR322 replicon, RNAI, RNAII and Rom.
- **Why it matters:** `reagent_arm.N` was 40 for part of 2026-08-20, a
  mid-range reading of a wide literature. This is a **measurement of the
  nearest relative**, and it moved the value to 50.
- **⚠️ It is not this strain.** No copy number has been measured for the
  reductase construct. The band stays 15–60.
- **Used in:** `params/recovery_chain.yaml :: reagent_arm.N`; `ISSUES.md`
  item 67.

**S43. Studier F. W., Moffatt B. A. (1986), and the T7 kinetics literature.**
"Use of bacteriophage T7 RNA polymerase to direct selective high-level
expression of cloned genes." *J. Mol. Biol.* **189**(1), 113–130.

- **Supplies the two anchors on `alpha`.** T7 RNA polymerase elongates at
  about **230 nt s⁻¹** at 37 °C, roughly **five times** *E. coli* RNA
  polymerase — the proxy value. And a T7 target protein can exceed **50 % of
  total cell protein**, which fixes the top of the band.
- **⚠️ Neither anchor is `alpha`.** `alpha` is a transcript *initiation* rate
  per plasmid copy. The 5× is an *elongation* ratio, a different quantity, and
  no in-vivo initiation rate for T7 exists in the literature — in the cell the
  limit is T7 RNAP abundance, not the enzyme's speed. This is the loosest
  number in the reagent arm and it is labelled `sourced_by_proxy` for that
  reason.
- **Used in:** `params/recovery_chain.yaml :: reagent_arm.alpha`; `ISSUES.md`
  item 67.

**S44. Raue A., Kreutz C., Maiwald T., Bachmann J., Schilling M., Klingmüller
U., Timmer J. (2009).** "Structural and practical identifiability analysis of
partially observed dynamical models by exploiting the profile likelihood."
*Bioinformatics* **25**(15), 1923–1929. doi:10.1093/bioinformatics/btp358

- **Supplies the treatment, not a number.** Parameters that enter a model only
  in a fixed combination are **structurally non-identifiable**: no amount of
  data separates them. The prescribed response is model reduction — lump the
  group and estimate the lump.
- **Why it matters:** `α`, `N` and `β` enter the reagent-arm cascade only as
  their product. They were carried as three parameters with three bands, which
  spread a single number over about 160×. They are now one parameter,
  `alpha_N_beta`, with one anchored band.
- **Used in:** `params/recovery_chain.yaml :: reagent_arm.alpha_N_beta`;
  `src/reductase.py :: lumped_group, cascade_from_lumped`; `ISSUES.md` item 67.

**S45. Kelly J. R., Rubin A. J., Davis J. H., et al., Endy D. (2009).**
"Measuring the activity of BioBrick promoters using an in vivo reference
standard." *J. Biol. Eng.* **3**, 4. doi:10.1186/1754-1611-3-4

- **Supplies the reason no absolute `α` exists.** Promoter activity is reported
  in **Relative Promoter Units**, against the reference promoter BBa_J23101,
  because relative measurement cuts between-lab variation by about half. The
  field stopped publishing absolute transcription rates.
- **⚠️ Not yet used.** If the wet lab characterises the reductase promoter it
  will report RPU, and this repository has no conversion at that interface.
  Recorded so the gap is visible. `ISSUES.md` item 67.

**S46. BioNumbers, *E. coli* dry weight per OD600.** BNID 109835, 109837,
109838, 100008.

- **Supplies:** about **0.36 g L⁻¹ per OD600** as the commonly cited default,
  0.3–0.5 as the usual range. Strain and instrument dependent; every entry says
  to calibrate your own curve.
- **Used in:** `reagent_arm.g_dw_per_OD600`, which was `assumed` with no source.

**S47. Metabolic-burden literature.** Including the BioBrick burden survey,
*Nat. Commun.* **15** (2024), and the maintenance-coefficient studies of
IPTG-induced recombinant expression.

- **Supplies:** a **33 % fall in maximum specific growth rate** under
  IPTG-induced expression, and **no BioBrick above 45 %** across hundreds
  measured. Band 0.10–0.45.
- **Why it matters:** `burden` was `null` while the tests passed 0.3 by hand
  since 2026-08-16. The hand-passed value was right and had nothing behind it.
- **Used in:** `reagent_arm.burden`; `ISSUES.md` items 52 and 67.

**S48. Global protein turnover in *E. coli*.** *Nat. Commun.* (2024),
"Global protein turnover quantification in *Escherichia coli* reveals
cytoplasmic recycling under nitrogen limitation."

- **Supplies:** the active degradation constant is **practically zero for the
  great majority of the proteome** during exponential growth, with a rapidly
  degrading component of 2–7 % at about a **1 h half-life**. Band 0 to
  0.0116 min⁻¹.
- **Why it matters:** `delta_c` = 0.005 is GolB's value, a 139 min half-life.
  It sits inside the band but **the low end is the more likely one**, so the
  value is conservative. At `delta_c` = 0 the plateau rises about 25 %.
- **Used in:** `reagent_arm.delta_c`.

**S49. Ultrasonication of *E. coli*.** Ultrasonication protocol literature for
bacterial disruption and fusion-protein recovery.

- **Supplies:** about **30 % of recombinant protein stays with cell debris**
  after one 15-min sonication, and about **90 % global recovery** after two
  consecutive treatments. Band 0.50–0.90.
- **Used in:** `reagent_arm.lysis_yield`, which was `null`.

**S50. Centrifugal recovery of colloidal gold.** Including shape separation of
gold nanorods by centrifugation, *PNAS* **106** (2009).

- **Supplies the physics, not a value.** The sedimentation coefficient goes as
  the **square of particle diameter**, so recovery climbs steeply with size and
  ultrasmall particles stay in the supernatant. About **50 % for 10 nm gold**.
- **⚠️ `eta_spin` stays `null` deliberately.** The model does not predict
  particle size, so choosing a value would be a guess about a quantity this
  repository has no equation for.
- **Used in:** `recovery.eta_spin`.

**S51. Finke–Watzky kinetics: the mechanism, the challenge, and the reply.**
Watzky & Finke 1997, *J. Am. Chem. Soc.*; Finke's explicit lag-and-growth-time
formulas, *J. Phys. Chem. C* (2017); Whitehead, Özkar & Finke, "Particle Size
Is a Primary Determinant for Sigmoidal Kinetics… A 'Disproof' of the F–W
Mechanism," *Chem. Mater.* (2019); and the published **Response**,
*Chem. Mater.* (2020), doi:10.1021/acs.chemmater.0c00780.

- **Supplies the decision to keep F–W.** The mechanism was challenged in print
  and the challenge was answered in print. It remains the standard model for
  sigmoidal nanoparticle formation, and the biogenic gold literature describes
  the same picture — reduction to Au(0), cluster formation, then autocatalytic
  growth.
- **The field's own extension is an addition, not a replacement.**
  Mechanism-Enabled Population Balance Modelling adds a third step
  (A + C → 1.5 C) to the F–W two. **Its purpose is particle size
  distribution**, which this repository does not need: physical recovery went
  out of scope on 2026-08-21, and conversion is the deliverable.
- **⚠️ Supplies no value for `k_nuc` or `k_grow`.** Searched 2026-08-21. F–W
  constants are published for many systems and **none for protein-mediated
  gold reduction**; the literature states they are system-dependent and fitted
  per curve. These two remain the joint #1 driver and remain uncalibrated.
- **⚠️ A warning about switching models.** Fitting the same data with the
  classic KJMA/Avrami model "affords radically different rate constants for
  equivalent reaction conditions". A rate constant is meaningful only beside
  the mechanism it was fitted with, so no `k_grow` may be borrowed across
  model families.
- **Used in:** `reduction.k_nuc`, `reduction.k_grow`; `ISSUES.md` item 67.

**S52. Fitted Finke–Watzky constants for gold.** Two systems, neither of them
protein-mediated:

1. **Cinnamon-extract reduction of Au(III).** *Molecules* **29**, 1426 (2024).
   Watzky–Finke fit at 0.01 M Au(III), 18 g L⁻¹ extract, 20–60 °C:
   **k₁ = 0.0056 min⁻¹ at 40 °C**, band 0.0004–0.0124 min⁻¹ across the range;
   k₂ = 0.165 (a.u.)⁻¹ min⁻¹. Activation energies **E₁ = 70.6 kJ mol⁻¹**,
   E₂ = 19.6 kJ mol⁻¹.
2. **Ascorbate–PVP reduction of HAuCl₄**, refitted in "Gold Nanoparticle
   Formation Kinetics and Mechanism: A Critical Analysis of the 'Redox
   Crystallization' Mechanism," *ACS Omega* (2018).
   **k₁ = 2.19 × 10⁻⁵ s⁻¹, k₂ = 0.234 s⁻¹ for a normalised [A]₀ = 1.00.**

- **What transfers, and how.** `k_nuc`: 0.0056 min⁻¹ at 40 °C corrected to
  25 °C on E₁ gives **0.0858 h⁻¹**, and the ascorbate fit gives **0.0788 h⁻¹**
  — two independent chemistries agreeing at about 0.08 h⁻¹. `k₁` is
  pseudo-first-order and absorbs reductant concentration; those systems carry
  **millimolar** reductant against about **9.2 µM of electrons** here, so
  scaling by ~1000 gives 8.6 × 10⁻⁵ h⁻¹, within a factor of two of the
  5 × 10⁻⁵ already in use. **That agreement is why the value survives.**
- **`k_grow`: k₂ × [A]₀ = 842 h⁻¹ at full precursor.** Converting needs the
  precursor concentration, which the paper does not give; at the 0.4 mM
  typical of such preparations it is **2.1 µM⁻¹ h⁻¹**. ⚠️ **The 0.4 mM is our
  assumption and the answer is linear in it.**
- **⚠️ The value in use is about ten times slower**, and that decides the
  stage: 0.3 % conversion at 24 h against 99.9 %. 0.2 is kept because these
  are chemical reductants at millimolar loading and ours is a protein at
  micromolar — adopting a borrowed constant would rewrite section 6.3 on
  somebody else's chemistry.
- **⚠️ k₂ in source 1 is in arbitrary absorbance units** and cannot be
  converted at all. Only source 2 anchors `k_grow`.
- **Used in:** `reduction.k_nuc`, `reduction.k_grow`; `ISSUES.md` item 67.

**S53. Wang, Yan, Ye, Chen et al. (2022).** "Identification and
Characterization of a Au(III) Reductase from *Erwinia* sp. IMH." *JACS Au*
**2**(6), 1435–1442. doi:10.1021/jacsau.2c00170

- **The closest published analogue to this project's reduction step.** A
  purified, cytoplasmic **Au(III) reductase**, GolR, reducing Au(III) to gold
  nanoparticles *in vitro*.
- **Supplies the floor of the `k_grow` band.** "About 67 % Au(III) was reduced
  in 2 h" at **2 mM Au(III), 1 mM GolR, 1 mM NADH, 30 °C, pH 7.0**. Fitting
  that endpoint through this repository's own reduction model gives
  **k_grow = 3.2 × 10⁻³ µM⁻¹ h⁻¹**; a plain Finke–Watzky fit gives
  0.9 × 10⁻³ to 3.7 × 10⁻³ depending on the `k_nuc` assumed.
- **A purified enzyme is about sixty times slower than the value this
  repository carries**, and about six hundred times slower than ascorbate
  (S52). That is the expected direction: a small molecule in large excess
  against a protein handing over electrons one at a time.
- **Its electron ledger closes**, which is why the unusual "1 mM GolR" can be
  taken at face value: 67 % of 2 mM Au(III) at 3 e⁻ is 4 mM of electrons, and
  1 mM NADH plus 1 mM GolR at 2 e⁻ each is exactly 4 mM. Re-running the same
  conditions at 1 µM protein caps conversion at 4 %.
- **⚠️ Three limits, all of them real.** It is ONE endpoint, not a time course,
  so `k_nuc` and `k_grow` cannot be separated from it. It was measured at 2 mM
  gold and is applied here at 0.37 µM — five thousandfold lower, which is
  exactly the extrapolation the 2019 particle-size critique warns about (S51).
  And it is a different protein from ours.
- **Used in:** `reduction.k_grow`; `ISSUES.md` item 67.

**S54. Munoz-Villagran, Contreras, Cornejo et al. (2020).** "Understanding gold
toxicity in aerobically-grown *Escherichia coli*." *Biological Research*
**53**, 26. doi:10.1186/s40659-020-00292-5

- **The only gold-toxicity dose-response measured in our own organism.**
  Aerobic *E. coli* in LB at 37 C, exposed to HAuCl4.
- **Supplies `V1_capture.A_tox` = 250 uM**, the reported MIC in that regime.
- **And supplies the onset, which is a different number.** 7.8-15.6 uM has
  "negligible effects on cell growth"; 31.2-125 uM extends the lag phase
  without stopping growth. So damage begins about eightfold below the MIC.
- **The mechanism is the one our binding chemistry uses.** Au3+ decreases
  intracellular thiol levels and raises superoxide, superoxide dismutase and
  catalase: it is a soft metal attacking thiols, and GolB binds gold through a
  Cys-X-X-Cys motif.
- **Limits.** It is Au(III) from chloride; we deliver Au(I) thiosulfate, and
  no MIC has been published for that species. LB was the only medium tested.
- **Used in:** `V1_capture.A_tox`, `V1_capture.k_dam`.

**S55. Wiesemann, Bütof, Herzberg et al. (2017).** "Synergistic Toxicity of
Copper and Gold Compounds in *Cupriavidus metallidurans*." *Applied and
Environmental Microbiology* **83**(23), e01679-17. doi:10.1128/AEM.01679-17

- **The second, independent anchor for the onset.** Au(III) IC50 in strain
  CH34 is **18.7-25.8 uM** in liquid culture.
- **Two organisms, two assays, the same order of magnitude**, which is why the
  onset is carried as about 20-30 uM rather than as one figure.
- **It also reports the copper interaction**, MIC(Au) falling linearly with
  Cu(II). Our leach hands about 820 uM of copper to capture, and no term in
  this model represents that.
- **Limits.** *C. metallidurans* is a metal-resistant organism, not *E. coli*,
  and IC50 is not MIC.
- **Used in:** `V1_capture.A_tox`, `V1_capture.k_dam`.

**S56. LaVoie & Summers (2018).** "Transcriptional responses of *Escherichia
coli* during recovery from inorganic or organic mercury exposure." *BMC
Genomics* **19**, 52. doi:10.1186/s12864-017-4413-z

- **The nearest measured repair timescale**, for the nearest measured insult:
  a soft metal that attacks thiols, in our own organism.
- **Cells recover in about an hour.** Growth stasis lasts 10-30 min after a
  sublethal dose; by 60 min a PMA-exposed culture is back at its pre-exposure
  growth rate with 1.5 % of genes still differentially expressed, while
  HgCl2-exposed cells are slower.
- **This makes `V1_capture.k_rep0` = 0.1 h⁻¹ an order of magnitude slow.** A
  one-hour recovery is about 1 h⁻¹. The parameter is not changed here, because
  `k_dam` and `k_rep0` are not separately identifiable and nothing in the code
  integrates the damage equation.
- **Limits.** Mercury is not gold, and transcriptional recovery is not the
  same observable as a repaired binding site.
- **Used in:** `V1_capture.k_rep0`.

**S57. Tsuruta (2004).** "Biosorption and recycling of gold using various
microorganisms." *Journal of General and Applied Microbiology* **50**(4),
221-228. doi:10.2323/jgam.50.221

- **The only published time course of gold biosorption onto Gram-negative
  bacteria that this project has found.** Resting *Pseudomonas maltophilia*,
  15 mg dry cells in 100 mL, 50.5 uM HAuCl4, pH 3.0, room temperature.
- **It supplies `V1_capture.k_on`.** The paper fits a time-dependent Langmuir
  form, Q = Qe[1 - exp(-(i*t + j))], with **i = 0.0201 min^-1, j = 2.78,
  Qe = 329 umol/g dry cells**. Their own loading gives 49.35 uM bound out of
  50.5 uM fed, so 1.15 uM free at equilibrium. Relaxation toward equilibrium
  in the binding equation of this model runs at k_on*(Au + S0 - 2*Ceq) + k_off,
  which for those numbers is k_on * 1.15 uM. Setting that equal to
  i = 1.206 h^-1 gives **k_on = 1.05 uM^-1 h^-1**, against the 1.0 this
  repository had been carrying unsourced. The placeholder was right.
- **The fit also says the uptake is biphasic.** j = 2.78 means 93.8 % of the
  equilibrium load is already bound at t = 0, i.e. within the mixing time; the
  50-minute time constant describes only the last 6 %.
- **It reports a capacity 3,600x above this model's.** Qe = 329 umol/g at
  50.5 uM and a Langmuir maximum of 992 umol/g, against `q_max` = 0.0913
  umol/g here. `ISSUES.md` item 69.
- **Limits.** Au(III) chloride at pH 3, not Au(I) thiosulfate at pH 9-10;
  wild-type cells, so the uptake is the cell wall's own and not a displayed
  protein's; and at pH 3 part of what is measured as sorption is reduction to
  metal on the wall.
- **Used in:** `V1_capture.k_on`; `ISSUES.md` item 69.

**S58. Tafakori, Zadmard, Tabandeh, Amoozegar & Ahmadian (2017).**
"Equilibrium isotherm, kinetic modeling, optimization, and characterization
studies of cadmium adsorption by surface-engineered *Escherichia coli*."
*Iranian Biomedical Journal* **21**(6), 380-391.
doi:10.18869/acadpub.ibj.21.6.380

- **The closest published system to ours in construction**: *E. coli*
  displaying a metal-binding protein through Lpp'-OmpA, the same display
  strategy class as the GolB construct, with a measured adsorption time
  course.
- **Pseudo-second order fits, R^2 = 0.99 against 0.75 for first order**, with
  k2 = 0.005 g mg^-1 min^-1 and qe = 15.2 mg/g at 1 g/L of cells and 20 mg/L
  of Cd(II). The PSO half-time 1/(k2*qe) is **13 min** and the paper reports
  **equilibrium at 40 min**.
- **It corroborates the timescale from a different direction.** A displayed
  binding protein on *E. coli* reaches equilibrium in tens of minutes, which
  is what this model predicts at the sourced k_on.
- **Limits.** Cadmium, not gold, and a metallothionein rather than GolB.
- **Used in:** the capture time course, `docs/RECOVERY.md` 2.3.

### The elution ceiling and rate

Added 2026-08-24. `phi` and `k_elute` had `source: null` since the parameter
file was written. `phi` is now traced to its origin; `k_elute` is bracketed by
three published desorption endpoints. ISSUES.md item 28.

**S59. Han Y.-L., Gao P.-J., Cheng C.-L., Wu P.-Y., Chang J.-S. (2019).**
"Recovery of gold from industrial wastewater by immobilized gold-binding
proteins on porous silica carriers grafted with amino group."
*Biochemical Engineering Journal* **152**, 107388.
doi:10.1016/j.bej.2019.107388

- **This is where `phi` = 0.13 comes from.** The paper tested several
  desorption agents and reports that **1 M thiourea was the best, stripping
  87 % of the gold off the loaded protein biosorbent**. That is the sentence
  carried, without a citation, in `docs/MODEL.md` §7 as *"87% desorption,
  protein biosorbent + 1 M thiourea"*. 1 - 0.87 = 0.13.
- **It is the closest analogue this project has for the ceiling**, because the
  sorbent is a **protein**, not a resin or a functionalised polymer. The gold
  is held by a polypeptide and the thiourea has to displace it from one.
- **Companion paper, same proteins:** Han Y.-L., Wu J.-H., Cheng C.-L.,
  Nagarajan D., Lee C.-R., Li Y.-H., Lo Y.-C., Chang J.-S. (2017), "Recovery
  of gold from industrial wastewater by extracellular proteins obtained from a
  thermophilic bacterium *Tepidimonas fonticaldi* AT-A2." *Bioresource
  Technology* **239**, 160-170. doi:10.1016/j.biortech.2017.05.038. Maximum
  capacity 9.7 mg Au per mg protein at pH 5 and 50 °C; 71 % removal from a
  real wastewater at 15 mg/L of gold.
- **Limits.** Au(III) from electroplating wastewater, not Au(I) thiosulfate.
  The protein is immobilised on amino-grafted silica, not displayed on a live
  cell. And the 87 % is a **batch endpoint with no time course**, so it fixes
  the ceiling and says nothing about `k_elute`.
- **Used in:** `elution.phi`; `docs/RECOVERY.md` 3.2.
- ⚠️ **The 87 % is from the publisher's page text, not the full text**, which
  is paywalled; the abstract does not carry it. Confirm before publication.

**S60. Son J., Hong Y., Han G., Nguyen T. S., Yavuz C. T., Han J.-I. (2019).**
"Gold recovery using porphyrin-based polymer from electronic wastes: gold
desorption and adsorbent regeneration." *Science of the Total Environment*
**704**, 135405. doi:10.1016/j.scitotenv.2019.135405

- **Supplies the slow end of the `k_elute` band.** Acid thiourea on the
  COP-180 porphyrin polymer released **more than 90 % of the gold after 12 h**
  and reached **97 %** overall; above **94 %** after five regenerations.
- **It is the only one of the three that yields a rate at all**, because it
  reports a ceiling (97 %) and an intermediate point (> 90 % at 12 h) that are
  **different numbers**. The share of the ceiling reached at 12 h is
  0.90/0.97 = 0.928, and `kt/(1+kt)` = 0.928 gives `k_elute` = **1.1 h⁻¹**.
  That is itself a floor, because the reported point is "more than 90 %".
- **CORRECTED 2026-08-24.** This entry first read the 90 % against a ceiling
  of 1.0 and gave 0.75 h⁻¹, which double-counted `phi`.
- **Also supplies a ceiling**, `phi` = 0.03, and the reagent warning that
  matters most: the formamidine disulfide route was used specifically to stop
  **thiourea being consumed**, which [S25] also flags.
- **Used in:** `elution.k_elute` band; `docs/RECOVERY.md` 3.4.

> **Rate-law update, 2026-09-18.** Under the provisional first-order model,
> the same S60 observations give
> `k_elute = -ln(1 - 0.90/0.97)/12 = 0.219 h^-1`, rounded to `0.22 h^-1`.
> Because the reported 12 h release is greater than 90%, this is a lower
> bound. It is a polymer-derived proxy, not a GolB measurement.

> **Full-text operating condition verified 2026-09-18.** S60 used 0.1 M
> thiourea in 0.1 M sulfuric acid at 50 °C and a solid/liquid ratio of 1 g/L
> for its subsequent desorption experiments. The 97% endpoint occurred at the
> lowest reported gold loading. These conditions now define the internally
> consistent working elution scenario; they remain transferred from COP-180,
> not measured on GolB.

**S61. Camoglu A. Y., Duran C., Ozdes D., Nalcaoglu A., Bektas K. I.,
Belduz A. O. (2025).** "Efficient extraction and determination of Au(III) ions
from acid mine drainage and water samples using silica gel immobilized with
*Brevibacillus borstelensis*." *Analytical Methods* **17**(3), 539-551.
doi:10.1039/d4ay01950d

- **Supplies the fast end of the band, on bacterial biomass.** Whole bacteria
  on silica gel, quantitative gold recovery, with an optimised **elution time
  of 60 min** using 0.1 % w/v thiourea in 0.5 M HNO₃.
- **It gives a bound, not a rate.** A quantitative elution at the optimised
  contact time is a plateau: it says the ceiling was reached **within 60 min**
  and nothing about how the curve got there. Reading it as 95 % of the ceiling
  would give 19 h⁻¹, but 99 % would give 74, so the number follows the
  convention chosen and not the data. Take the bound: `k_elute` >> 1 h⁻¹ in
  that system.
- **Note how little thiourea it needs.** 0.1 % w/v is about 13 mM, against the
  1 M in [S59]. The acid is doing the work, which is the same lesson [S24]
  teaches at 0.4 M thiourea plus 0.8 M HCl.
- **Limits.** Au(III) at pH 3, an analytical column rather than a vessel, and
  the cells are not engineered.
- **Used in:** `elution.k_elute` band; `docs/RECOVERY.md` 3.4.

**Where the model's `k_elute` = 2.0 h⁻¹ sits, restated 2026-08-24.** One
anchor gives a rate: [S60], at **1.1 h⁻¹ or faster**. The other two are
plateau readings — [S24] reached its ceiling within 80 min and [S61] within
60 min — so they bound `k_elute` well above 1 h⁻¹ without fixing it. The value
in use is consistent with all three and is within a factor of two of the only
derived one.

**Why an endpoint cannot be converted twice.** A reported desorption
percentage is either the ceiling or a point below it, and the same number
cannot serve as both. [S24]'s 95.7 % is used here as a **ceiling**,
`phi` = 0.043; reading it also as "95 % of the ceiling at 80 min" would count
`phi` twice and give a rate that is an artefact. The 14.3 h⁻¹ this file
carried until 2026-08-24 was exactly that artefact and is withdrawn.

**And rate constants of this kind do not transfer between systems** [S62].
`k_elute` = `k_2 C_elut(0)` scales with the loading it was measured at, so a
constant borrowed from a resin at a different loading is an order-of-magnitude
guide and no more.

Nothing here is a measurement on **this** sorbent, so `k_elute` stays
provisional; one desorption time course on GolB cells replaces all three
anchors at once. ISSUES.md items 28 and 47.

**S62. Bullen J. C., Saleesongsom S., Gallagher K., Weiss D. J. (2021).**
"A revised pseudo-second-order kinetic model for adsorption, sensitive to
changes in adsorbate and adsorbent concentrations." *Langmuir* **37**(10),
3189-3201. doi:10.1021/acs.langmuir.1c00142

- **Supplies the warning that limits every anchor above.** Across 103 kinetic
  experiments from 47 sources, the PSO rate constant `k_2` is shown to depend
  on the adsorbate and adsorbent concentrations of the experiment, so
  comparing `k_2` between published studies "can lead to erroneous
  conclusions".
- **It is the reason this model reports one constant, not two.**
  `k_elute` = `k_2 C_elut(0)` already carries the loading inside it, which is
  the conditionality the paper describes. It also means the anchors above are
  order-of-magnitude only.
- **Used in:** the `k_elute` band; `docs/RECOVERY.md` 3.3; ISSUES.md item 28.

### The reduction step, audited 2026-08-24

`nu`, `k_ox`, `k_rech` and `K_inh` all carried `source: null`. One of them now
has a source, one is shown to be mislabelled, and the transferability of
`k_nuc` and `k_grow` is now bounded by a citation rather than by assertion.

**S63. Erasmus M., Cason E. D., van Marwijk J., Botes E., Gericke M.,
van Heerden E. (2014).** "Gold nanoparticle synthesis using the thermophilic
bacterium *Thermus scotoductus* SA-01 and the purification and
characterization of its unusual gold reducing protein."
*Gold Bulletin* **47**, 245-253. doi:10.1007/s13404-014-0147-8

- **This is the origin of the protein [S35] uses**, purified to homogeneity
  and identified by N-terminal sequencing as an **ABC transporter,
  peptide-binding protein**.
- **It supplies `nu` = 0.5.** The paper proposes that the protein reduces
  Au(III) "through an electron shuttle mechanism involving a **cysteine
  disulphide bridge**". One disulfide carries two electrons, so one protein
  serves two Au(I), which is `nu` = 0.5 protein per gold. For Au(III) at three
  electrons the same arithmetic gives 1.5.
- **Carry the qualification with the number.** The paper writes *speculated*.
  No crystal structure, no redox titration, and no electron count is reported.
  `nu` is therefore a mechanism-based estimate, not a measurement, and the
  whole electron budget in the electron budget of the reduction model rests on it.
- **Same protein, different metal:** Cason et al. (2012), *Chemosphere*
  86(6):572-577, showed the same ABC transporter reduces U(VI), which is where
  the "reductase-like" description comes from. It is protein promiscuity, not
  a dedicated reductase.
- **Used in:** `reduction.nu`; `docs/RECOVERY.md` 4.1.

**S64. Ferreira D. L., Pereira C. F. J., Vivas M. G. (2023).** "Unveiling
step-by-step the bottom-up kinetics and growth mechanism of laser-induced
colloidal gold nanoparticles." *Journal of Physical Chemistry C* **127**(37),
18533-18546. doi:10.1021/acs.jpcc.3c04676

- **Supports the choice of rate law.** Gold nanoparticle formation is analysed
  with the Finke-Watzky model, slow continuous nucleation plus fast
  autocatalytic surface growth, and the model reproduces the measured size and
  concentration traces.
- **Supplies the limit on borrowing its constants**, which is the reason it is
  filed here: the paper finds that **the initial precursor concentration
  controls the fitted nucleation and growth constants**. Our anchors [S52] are
  millimolar-precursor fits and this vessel runs at micromolar, so `k_nuc` and
  `k_grow` cannot be carried across as numbers, only as orders of magnitude.
  This is the same defect [S62] describes for pseudo-second-order constants.
- **Used in:** `docs/RECOVERY.md` 4.4. The robust design it argued for was retired on
  2026-08-24, `ISSUES.md` item 82.

**S65. Dithionite: two electrons, and a warning.**

1. **Nkole I. U., Idris S. O., Abdulkadir I., Onu A. D. (2022).**
   "Application of the Piszkiewicz model on the electron transfer reaction of
   dithionite ion and bis-(2-pyridinealdoximato)dioxomolybdate(IV) complex."
   *Scientific Reports* **12**, 22125. doi:10.1038/s41598-022-24096-7
   **Supplies the stoichiometry the budget uses:** a 2:1 acceptor-to-dithionite
   ratio, so one `S2O4^2-` delivers **two electrons**. That is the factor of 2
   on `Rech_0` in the ceiling inequality.
2. **Martini M. A., et al. (2021).** "The nonphysiological reductant sodium
   dithionite and [FeFe] hydrogenase: influence on the enzyme mechanism."
   *Journal of the American Chemical Society* 143(43):18159-18171.
   **Supplies a caution against the 50 uM recommendation.** Dithionite's
   oxidation product, sulfite, binds at the active site and shifts its
   potential, producing states the authors call dithionite-inhibited. The
   effect is documented for a hydrogenase and not for this protein, but the
   design retired on 2026-08-24 asked for **11x** [S35]'s dithionite, so inhibition is a real
   risk and it is not in any equation here.

**S66. Streszewski B., Jaworski W., Paclawski K., Csapo E., Dekany I.,
Fitzner K. (2012).** "Gold nanoparticles formation in the aqueous system of
gold(III) chloride complex ions and hydrazine sulfate - kinetic studies."
*Colloids and Surfaces A* **397**, 63-72. doi:10.1016/j.colsurfa.2012.01.031

- **A modified Finke-Watzky fit on a gold system that separates Au(III) to
  Au(I) from the autocatalytic reduction of Au(I) to metal** - the step this
  project runs, since elution delivers Au(I). Reported constants:
  `k1` = 1.188 M^-1 s^-1, `k3` = 3.87e-2 M^-1 s^-1, `k4` = 7.53e5 M^-2 s^-1.
- **The mapping to `k_grow` was chased and could not be closed.** The full text
  is paywalled and the Szeged repository copy is archive-maintainer-only. From
  the abstract and the authors' summary: the particles catalyse the reduction
  of **both** Au(III) and Au(I), so there are two autocatalytic constants, and
  **each elementary step transfers one electron**.
- **The favoured reading is `k4`**, third order, which is the shape an
  autocatalytic step takes with the reductant written explicitly. Folding in a
  hydrazine concentration gives 0.027 to 2.7 uM^-1 h^-1 across 1e-5 to 1e-3 M,
  which brackets the 0.2 in use. On that reading the band needs no change.
- **The alternative reading is `k3`**, second order, which converts to
  1.4e-4 uM^-1 h^-1 and would put the band floor **23x too high**. It fits the
  Au(III)-on-particle step better than ours.
- **Used in:** nothing. It is the open question in ISSUES.md item 71.

**S67. Bentea L., Watzky M. A., Finke R. G. (2017).** "Sigmoidal nucleation and
growth curves across nature fit by the Finke-Watzky model of slow continuous
nucleation and autocatalytic growth: explicit formulas for the lag and growth
times plus other key insights." *Journal of Physical Chemistry C* **121**(9),
5302-5312. doi:10.1021/acs.jpcc.6b12021

- **Supplies the closed form this project should have been using**, from the
  model's own authors. Integrating `dB/dt = (k1 + k2*B)*(A0 - B)` gives
  `B(t) = A0 - (k1/k2 + A0)/(1 + (k1/(k2*A0))*exp((k1 + k2*A0)*t))`, so the
  sigmoid has one time constant, `1/(k1 + k2*A0)`, and reaches its midpoint at
  `ln(k2*A0/k1)` multiples of it.
- **It converts `t_cross` from a rule of thumb into a criterion.**
  `docs/RECOVERY.md` 4.3 observed empirically that a vessel needs "roughly ten"
  induction times. The logarithm is that ten: it runs 7.3 to 10.7 across the
  concentrations this project uses.
- **Checked against the code, 2026-08-24.** The closed form and
  `src/sensitivity.py :: reduce_finke_watzky` agree within 1 percentage point
  at 0.367, 1.5, 3.0 and 11.0 uM at both 24 h and 96 h, which is an
  independent check on the five-state implementation, the donor factor
  included.
- **Used in:** `docs/RECOVERY.md` 4.3.

**S68. Sullivan A. M., Kohl P. A. (1995).** "The autocatalytic deposition of
gold in nonalkaline, gold thiosulfate electroless bath." *Journal of The
Electrochemical Society* **142**(7), 2250-2255. doi:10.1149/1.2044282

- **The closest industrial analogue to this project's reduction step.**
  Ascorbate autocatalytically reduces **gold(I) thiosulfate** - the same
  oxidation state and the same ligand this chain carries - at about
  **1 um/h** of deposition.
- **Supplies a warning that applies directly to us:** the rate falls as
  **thiosulfate accumulates** and as the reductant depletes, and their fix is
  periodic peroxide to destroy the excess thiosulfate. Our eluate arrives from
  a thiosulfate leach, so free thiosulfate is present and its effect is in no
  equation here. Related to `ISSUES.md` item 44.
- **It also shows the reaction runs at all in this chemistry**, which no
  protein study does: [S35] used Au(III) chloride.
- **Used in:** `docs/RECOVERY.md` 4.5, as a limit.

**S69. Autocatalytic growth is surface-specific.** Two studies that bound how
far any single `k_grow` can be trusted.

1. **Yang T.-H., et al. (2017).** "Autocatalytic surface reduction and its role
   in controlling seed-mediated growth of colloidal metal nanocrystals."
   *PNAS* 114(52):13619-13624. **The activation energy of autocatalytic
   surface reduction depends on the facet and on whether the seed is twinned**,
   so a seeded vessel's growth constant is a property of the seed, not only of
   the chemistry. This project's design recycles 50% of a batch as seed, so the
   seed's surface is a design variable that the model does not carry.
2. **Kirner F., et al. (2020).** "Additive-controlled synthesis of monodisperse
   single crystalline gold nanoparticles." *Journal of Materials Chemistry C*
   8:10844-10851. Seed-mediated gold growth fitted with the **Finke-Watzky**
   two-step model, and the fitted constants shift with bromide and ascorbate.
   A third independent confirmation that the rate law is the right one and the
   constants are conditional.

- **Used in:** `docs/RECOVERY.md` 4.4; `ISSUES.md` item 71.

**S70. Cheng Y., Prusoff W. H. (1973).** "Relationship between the inhibition
constant (K1) and the concentration of inhibitor which causes 50 per cent
inhibition (I50) of an enzymatic reaction." *Biochemical Pharmacology*
**22**(23), 3099-3108. doi:10.1016/0006-2952(73)90196-2

- **Supplies the standard form of the factor in `v_rech`.** Competitive
  inhibition enters a rate law as `1 + [I]/K_i`, which is exactly the
  denominator `docs/source/model.md` writes and `docs/RECOVERY.md` 4.2 now
  derives in four steps.
- **And the condition under which it may be dropped:** the factor is within a
  few per cent of 1 while the inhibitor sits far below `K_i`. Here gold is 45x
  below `K_inh`, so the term is inert. ISSUES.md item 74.
- **Note what it is not.** The paper is about converting IC50 to `K_i`; no
  number is taken from it. It is cited for the algebraic form only.
- **Used in:** `docs/RECOVERY.md` 4.2.

**S71. How redox enzymes and dithionite are actually modelled.** Three papers
that between them verify the structure of `v_rech` and find one thing wrong
with it.

1. **Trimmer E. E., et al. (2001).** "Methylenetetrahydrofolate reductase from
   *Escherichia coli*: elucidation of the kinetic mechanism by steady-state and
   rapid-reaction studies." *Biochemistry* 40(20):6216-6226.
   **Confirms the structure.** A flavoprotein oxidoreductase is analysed as two
   separate half-reactions with their own rate constants -- reductive and
   oxidative -- and the two are then shown to account for overall turnover by a
   ping-pong Bi-Bi mechanism. That is exactly the shape of this model: `E_red`
   spent by gold, `E_ox` recharged by donor. **Two half-reactions in mass
   action is the standard treatment, not an invention.**

2. **Yousafzai F. K., Eady R. R. (2002).** "Dithionite reduction kinetics of
   the dissimilatory copper-containing nitrite reductase of *Alcaligenes
   xylosoxidans*." *Journal of Biological Chemistry* 277(38):34067-34073.
   **Confirms second-order mass action for the recharge, and supplies a
   magnitude:** `k` = 3.06 x 10^6 M^-1 s^-1 for dithionite reducing the type-1
   copper centre. In this model's units that is **1.1 x 10^4 uM^-1 h^-1**,
   against `k_rech` = 0.1 in use -- **110,000x slower**. Whatever else is
   uncertain, this model does not overstate the recharge.
   **And it supplies the correction below:** "in all cases the SO2 radical
   rather than S2O4^2- was the effective reductant".

3. **Lambeth D. O., Palmer G. (1973).** "The kinetics and mechanism of
   reduction of electron transfer proteins and other compounds of biological
   interest by dithionite." *Journal of Biological Chemistry* **248**(17),
   6095-6103. doi:10.1016/s0021-9258(19)43514-x
   **The classical result: dithionite reduces proteins through the SO2 radical**,
   `S2O4^2- <=> 2 SO2^.-`, so the observed rate goes as the **square root** of
   the dithionite concentration, not linearly with it.

**What that means for `v_rech` = `k_rech*E_ox*Rech/(1 + Au/K_inh)`.** The
`Rech` should strictly be `sqrt(Rech)`. Tested 2026-08-24 with the exponent set
to 0.5 and the constant rescaled to match at `t` = 0: conversion moves by at
most **0.001 of a point** at 0.367, 3, 11, 60, 120 and 200 uM. The order does
not matter here because recharging is five orders of magnitude faster than the
demand; only the electron *count* binds. ISSUES.md item 76.

- **Used in:** `docs/RECOVERY.md` 4.2; ISSUES.md items 74 and 76.

---

## Still needed

Numbers the walkthrough has identified as missing, with no source found yet.
Three rows cleared on 2026-08-12 are kept, struck through, so the record of
what was missing survives.

| Needed for | Quantity | Status |
|---|---|---|
| `ISSUES.md` item 14 | total protein per cell for the leaching organism | **assumed 1.0×10⁻¹³ g/cell**, no source. No longer on the critical path: the `Vmax` route via [S5] avoids it entirely. |
| `params/leach.yaml` | biomass in g dry weight per litre for our own culture | set to 4.0 g/L as an operating choice on 2026-08-11; measure by OD600 or dry weight |
| `ISSUES.md` item 2 | whether `P_s,max` = 1×10⁵ anchors/cell is a hard ceiling | open |
| **`ISSUES.md` item 19** | **gold plating thickness `t_film`, area-weighted over the real feed** | **assumed 0.5 µm on 2026-08-12. No supplier exists for mixed e-waste, so this will not come from a datasheet. Measure it: weigh the gold and the plated area on a feed sample, or fit it to a leach run. Decides a factor of 5.2 in recovery.** |
| **`ISSUES.md` item 41** | **`k_ox,Cu` and `k_par` measured in ammonia-free liquor** | **open. Both are borrowed from ammoniacal systems, where ammonia deliberately stabilises Cu(II). Together they decide 98% of the leachant budget.** |
| **`ISSUES.md` item 38** | **thiosulfate decomposition rate at pH 3–5, and TetH activity at pH 5–6** | **open. Decides whether Stage 2 can run at all.** |
| **`ISSUES.md` item 40** | **purification recovery for TetH** | **open. Sets the true culture volume, currently understated.** |
| ~~Part I §2~~ | ~~`K_m` single value; document gives the range 50–2400 µmol/L~~ | ✅ **300 µmol/L chosen 2026-08-12. Item 17 closed.** |
| ~~Part I §4~~ | ~~`k_Au,Cu`; given only as "≈10³× larger" than `k_Au,O2`~~ | ✅ **1500 µmol m⁻² min⁻¹ supplied 2026-08-12. Item 8 closed. Note the true ratio is 132×, not 10³×.** |
| ~~Part I §5~~ | ~~`k_Cu,O2`; given only as an activation energy, 25.8 kJ/mol~~ | ✅ **200 µmol m⁻² min⁻¹ supplied 2026-08-12. Item 8 closed.** |

---

## Verification status

| Source | Number or fact used | Verified against |
|---|---|---|
| S1 | 2.2 ± 0.37 U mg⁻¹, 50 kDa × 2 | ✅ PMC full text, 2026-08-10 |
| S2 | 0.28 U mg⁻¹ crude extract | ⚠️ abstract only; different organism |
| S3 | dimer, periplasmic | ✅ PMC full text read in the 2026-08-11 audit |
| S4 | TetH is the sole hydrolysis route | ⚠️ abstract only |
| S5 | 0.092 h⁻¹, 12.2 g/mol, 1.01 mmol g⁻¹ h⁻¹ | ✅ two independent lookups |
| S6 | GolS is Au-selective | ⚠️ abstract only |
| S7 | dithiolate tuning lowers Cu(I) affinity | ⚠️ abstract only |
| S8 | GolS activated more by Au than Ag or Cu | ⚠️ abstract only |
| S9 | GolB Au(I) selectivity "probably" | ⚠️ computational, hedged |
| S10 | Au–S rupture 165 pN | ⚠️ abstract only |
| S11 | thiol/Au(S₂O₃)₂³⁻ ion exchange | ⚠️ abstract only |
| S12 | thiolate + disulfide interchange; 0.1 M S₂O₃, pH 9 | ⚠️ abstract only |
| S13 | metal:ligand 1:1; alkaline and high Eh favour uptake | ⚠️ abstract only |
| S14 | Au(S₂O₃)₂³⁻ dominant only in acid | ⚠️ abstract only |
| S15 | *A. ferrooxidans* pH 1.6–2.0, best 1.8 | ⚠️ abstract only |
| S16 | thiosulfate gold leach pH 9.3–10.5 | ⚠️ abstract only |
| S17 | non-ammoniacal thiosulfate, 0.14 M, alkaline | ⚠️ abstract only |
| S18 | 20.7 g/L DCW in shake flasks | ⚠️ abstract only |
| S19 | 128 and 148 g/L DCW | ✅ confirmed by two independent lookups |
| S20 | 88.9 g/L DCW with soluble expression | ⚠️ abstract only |
| S21 | biosorption columns use non-viable biomass | ⚠️ abstract only |
| S22 | ten reuse cycles; mixed metals halve capacity | ⚠️ abstract only |
| S23 | 190 g/L is the field record | ✅ confirmed by two independent lookups |
| S24 | 0.4 M thiourea + 0.8 M HCl → 95.7% desorption | ⚠️ abstract only |
| S25 | thiourea + acid ≈100%; iron sulfides degrade thiourea | ⚠️ abstract only |
| S26 | review, thiourea for gold from e-waste | context only, no number taken |
| S27 | inclusion bodies in *E. coli*; acid refolding required; 21.0 U mg⁻¹ | ✅ PubMed record, 2026-08-11 |
| S28 | inclusion bodies, acid refolding, replicated | ✅ PubMed record, 2026-08-11 |
| S29 | >10⁵ displayed molecules per cell | ✅ PMC full text, 2026-08-11 |
| S30 | 148 fg at 100 min, 865 fg at 24 min doubling | ✅ full text, 2026-08-11 |
| S3 | **also**: TetH optimum pH 3.0, optimum 60 °C, 50 kDa × 2 | ✅ PMC full text, 2026-08-11 |
| S59 | 87% desorption, protein biosorbent + 1 M thiourea -> phi = 0.13 | publisher page text only; abstract does not carry it |
| S60 | >90% gold released in 12 h, 97% overall, acid thiourea | PubMed record, 2026-08-24 |
| S61 | elution time 60 min, thiourea in HNO3, bacteria on silica | PubMed record, 2026-08-24 |
| S62 | PSO k_2 depends on experimental concentrations | ✅ abstract, 2026-08-24 |
| S63 | disulfide shuttle proposed for the gold reductase -> nu = 0.5 | ⚠️ abstract; the paper says "speculated" |
| S64 | FW constants for gold depend on precursor concentration | ✅ abstract, 2026-08-24 |
| S65 | one dithionite = 2 electrons; sulfite inhibits enzymes | ✅ abstract, 2026-08-24 |
| S66 | modified FW on Au(I) -> Au(0); k4 reading fits our band, k3 reading would not | ⚠️ abstract + author summary; full text paywalled |
| S67 | FW closed form; lag = ln(k2A/k1) time constants. Checked against our code | ✅ abstract + independent re-derivation |
| S68 | ascorbate reduces Au(I) THIOSULFATE autocatalytically, ~1 um/h | ⚠️ abstract only |
| S69 | autocatalytic growth constant depends on seed facet and twinning | ⚠️ abstracts only |
| S70 | competitive inhibition enters as 1 + [I]/K_i, and when to drop it | ✅ abstract, 2026-08-24 |
| S71 | two half-reactions is standard; dithionite acts as SO2 radical, so rate goes as sqrt | ✅ abstracts, 2026-08-24 |
| S72 | the primary curves behind the k_grow ceiling; biogenic gold nucleates heterogeneously; crystallisation is rate-determining | ⚠️ abstract only, paywalled |
| S73 | two dead ends recorded: no fitted constants, and dye-degradation constants that are not gold reduction | ✅ abstracts, 2026-08-24 |
| S74 | MEASURED kcat and K_M for an enzyme reducing gold; K_M is 50-290 uM, far above this vessel, so the rate is first order | ✅ full text, 2026-08-24 |

**How to read this column.** ✅ means the number was checked against the
publisher's full text or confirmed by a second independent lookup. ⚠️ means it
comes from the abstract only. Abstract-sourced numbers are usable for a first
pass and should be confirmed against the full text before anything is
published.

**S72. Zhou Y., Wang H., Lin W., Lin L., Gao Y., Yang F., Du M., Fang W.,
Huang J., Sun D., Li Q. (2013).** "Quantitative nucleation and growth kinetics
of gold nanoparticles via model-assisted dynamic spectroscopic approach."
*Journal of Colloid and Interface Science* **407**, 8–16.
doi:[10.1016/j.jcis.2013.06.027](https://doi.org/10.1016/j.jcis.2013.06.027).
Retrieved from PubMed, PMID 23871600, on 2026-08-24.

- **This is the primary data behind the `k_grow` ceiling.** The ascorbate–PVP
  numbers in [S52](SOURCES.md) are not an independent fit: Watzky and Finke
  digitised **this paper's** published curves and refitted them. The chain for
  the ceiling is therefore this measurement, refitted twice.
- **⚠️ It does not close the gap that matters.** The abstract names no
  concentration of HAuCl₄ or ascorbate, and the refit reports its constants for
  a normalised `[A]₀` = 1.00. **The 0.4 mM used to convert `k₂` into
  µM⁻¹ h⁻¹ remains this project's assumption**, and `k_grow`'s ceiling is
  linear in it. Full text is paywalled at Elsevier.
- **It measured a biogenic route as well as a chemical one**, and the two
  differ in a way this project should note: the biogenic approach, a foliar
  aqueous extract, **"involved heterogeneous nucleation"** where the chemical
  approach did not. Nucleation on an existing surface is what seeding supplies,
  which is an independent argument for the seed of `ISSUES.md` item 64.
- **And it puts the rate-determining step where this model puts it.** The
  authors conclude that of the two aspects of particle formation, the redox
  chemistry and the crystallisation, **the crystallisation is rate-determining**.
  This model reaches the same place by a different route: `E_red/E_tot` stays
  at 0.996, so the electron supply never limits the rate and the particle terms
  do, `ISSUES.md` item 74.
- **Used in:** `reduction.k_grow`; `ISSUES.md` items 71 and 79.

**S73. Two searches that returned nothing usable, recorded so they are not
repeated.** 2026-08-24.

1. **Pestovsky Y. S., Srichana T. (2022).** "Formation of Aggregate-Free Gold
   Nanoparticles in the Cyclodextrin–Tetrachloroaurate System Follows
   Finke–Watzky Kinetics." *Nanomaterials* **12**(4), 583.
   doi:[10.3390/nano12040583](https://doi.org/10.3390/nano12040583).
   The title promises what this project needs. **The paper reports no fitted
   `k₁` or `k₂`**; it demonstrates the three-stage sigmoidal shape and then
   states the growth is multistage and not the plain two-step form. No value
   transfers.
2. **Gholami-Shabani M. et al. (2015).** "Enzymatic synthesis of gold
   nanoparticles using sulfite reductase purified from *Escherichia coli*."
   *Process Biochemistry* **50**(7), 1076–1085.
   A purified enzyme making gold, which is this project's chemistry. **Its
   rate constants are for the wrong reaction:** 4.5 × 10⁻³ s⁻¹ and
   1.7 × 10⁻³ s⁻¹ describe the finished nanoparticles **catalysing dye
   degradation**, congo red and methyl orange, not the enzyme reducing gold.
   Quoting them for `k_nuc` or `k_grow` would be a category error.

- **The standing conclusion is unchanged.** No published Finke–Watzky fit for
  protein-mediated gold reduction has been found in two searches, 2026-08-21
  and 2026-08-24. [S53](SOURCES.md), the GolR endpoint refit, remains the only
  enzyme anchor.
- **Used in:** `ISSUES.md` item 79.


**S74. Ng W. L., Chan K. W. K. et al. (2024).** "Engineering a Metal Reductase
for the Bioremediation of Anthropogenic Electronic Wastes: From Hg(II) to
Au(III) and Ag(I) Enzymatic Reduction." *JACS Au* **4**(7), 2529–2539.
doi:[10.1021/jacsau.4c00297](https://doi.org/10.1021/jacsau.4c00297).
Retrieved as full text from PubMed Central, PMC11200239 / PMID 38938813, on
2026-08-24.

- **This is the first source found that gives MEASURED kinetic constants for an
  enzyme reducing gold.** MerA and an engineered variant, assayed by NADPH
  oxidation at 340 nm and fitted to Michaelis–Menten:

| Enzyme | `k_cat` | `K_M` | `k_cat/K_M` |
|---|---|---|---|
| WT MerA, *P. aeruginosa* | 0.027 s⁻¹ = **97 h⁻¹** | **290 µM** | 91 M⁻¹s⁻¹ = **0.335 µM⁻¹h⁻¹** |
| G415I variant | 0.068 s⁻¹ = **245 h⁻¹** | **50 µM** | 1360 M⁻¹s⁻¹ = **4.90 µM⁻¹h⁻¹** |

  Conditions: 100 mM KH₂PO₄ pH 7.6, 0.02 mM enzyme, 0.4 mM NADPH,
  0.01–1 mM metal, 25 °C. The internal arithmetic closes: `k_cat`/`K_M` for the
  variant is 15× the wild type, which is the improvement the abstract claims.

- **`K_M` is the number that matters most.** 50–290 µM against a vessel running
  at 0.367–11 µM means this enzyme is **far below saturation** here, so the
  rate law collapses to first order in gold, `v = (k_cat/K_M)·E·Au`, and the
  time to 95 % is `ln(20)/((k_cat/K_M)·E_tot)` — **independent of the gold
  charged**. There is no concentration threshold in this description.
- **The assay is one this team can run.** NADPH oxidation at 340 nm,
  ε = 6220 M⁻¹cm⁻¹, initial velocities against a metal series, nonlinear fit.
  A plate reader and an afternoon replace a constant that has resisted two
  literature searches.
- **⚠️ Four limits.** It is a different enzyme from this project's; it is
  Au(III) where elution delivers Au(I) thiourea; the assay measures **electron
  transfer**, not particle formation, so it bounds the redox half only; and the
  gold ions were the substrate at 10–1000 µM, above this vessel's range.
- **Used in:** `ISSUES.md` item 80.


---

## How to cite these in the wiki

Full journal citations are given above. The Consensus links are for locating
the paper quickly; replace them with DOIs before anything is published.


## Recovery audit sources, 2026-09-06

**S75. Haiss W., Thanh N. T. K., Aveyard J., Fernig D. G. (2007).**
Determination of size and concentration of gold nanoparticles from UV-vis
spectra. *Analytical Chemistry* 79, 4215–4221.
[DOI](https://doi.org/10.1021/ac0702084).
[PubMed abstract checked](https://pubmed.ncbi.nlm.nih.gov/17458937/).
Optical response depends on particle size and wavelength. Supports requiring
calibration and particle characterization before an optical trace represents
metal concentration. Does not validate a single-wavelength kinetic fit here.

**Audit access note.** S35's publisher full text and S62's publisher abstract
were checked on 2026-09-06. S35 studies Au(III) and reports optical and particle
characterization; it does not validate the present Au(I)-thiourea process.
The PMC copy of S74 returned a browser check and the publisher returned HTTP
403 in this review. Its detailed table was not independently reverified in
this pass; its earlier entry remains a record, and its transfer remains a proxy.

**Judging reference, not a parameter source.** The official
[2026 special awards criteria](https://competition.igem.org/judging/special-prizes)
and [medal criteria](https://competition.igem.org/judging/medals) were checked
on 2026-09-06. These govern presentation of evidence, not scientific validation.


**S76. Wei W., Zhu T., Wang Y., Yang H., Hao Z., Chen P. R., Zhao J. (2012).**
Engineering a gold-specific regulon for cell-based visual detection and recovery
of gold. *Chemical Science* 3, 1780–1784.
[DOI](https://doi.org/10.1039/C2SC01119K).
[Archived primary manuscript](source/capture_investigation/wei_2012_golb.pdf).
[Official supplementary methods](https://www.rsc.org/suppdata/sc/c2/c2sc01119k/c2sc01119k.pdf).

Checked 2026-09-07. The image of printed page1783 (PDF page5) confirms the
reported loading is **4.62 µmol/g cells**, not mmol/g. Supplementary methods
use lyophilised dry weight. This is a whole-cell endpoint during growth with
Au(III) chloride, not a fitted Langmuir maximum. Surface particles and
mixed-metal recovery are reported. Neither kinetic parameters nor a capacity
for this project's Au(I)-thiosulfate mixture are supplied.

This supersedes the completeness claim above S9: experimental surface-GolB
capture/selectivity evidence exists. It still does not give a competitive
binding constant in the project matrix. ISSUES 91 records the consequence for
interpreting the expression-derived site count.

> **Update 2026-10-17. The full text was read, and it does supply GolB's own
> metal constants.** Table 1 and the surrounding text report, for purified
> GolB: `K_d(Au(I)) = 3.02e-37 M` from the Au(I)-S absorption at 250 nm with a
> competitive cyanide titration, and `K_d(Cu(I)) = 1.61e-17 M` by a published
> protocol. The ratio is a gold preference of **5.3e19**, measured on GolB
> itself, against the 52 taken from the GolS reporter in S79.
>
> **These are bare-ion thermodynamic constants.** They carry no competing
> ligand, so neither may be used as the apparent `K` of the capture model,
> where thiosulfate holds both metals. The usable quantity is the ratio, and
> even that is an upper bound: thiosulfate binds Au(I) far more strongly than
> Cu(I), which lowers the conditional selectivity. ISSUES 93.
>
> Three further findings from the same read:
> - **1:1 binding, confirmed.** ESI-MS gave apo-GolB at 7002.5 Da and the
>   complex at 7199.5 Da, one gold per protein, and a Job plot agreed. This
>   supports the one-gold-per-site assumption in `docs/CAPTURE_DESIGN.md`.
> - **The 4.62 µmol/g loading was measured at 50 µM Au(III)**, overnight in
>   LB. That is close to this project's 37-44 µM feed, so the loading
>   transfers on concentration grounds, though not on matrix.
> - **Recovery was by papain, not thiourea.** 12 h at 30 °C with 10 mg/L
>   papain released about **89 %** of the adsorbed gold, and the cells survived
>   three adsorb-release cycles with an unchanged growth curve. This is a
>   different elution route from the project's acid thiourea, and a direct
>   measurement of comb reuse.


**S77. iGEM 2015, Registry Part `BBa_K1701000`.** GolB displayed on the
*Bacillus subtilis* surface through TasA (biofilm) and CotC (spore) anchors.
[Registry page](https://parts.igem.org/Part:BBa_K1701000).

Checked 2026-09-07. Reported gold loadings: **5.2 µmol/g cells** for the
TasA-displayed construct under Pveg, **3.5 µmol/g** under Ptas, and
**4.4 µmol/g** for the CotC spore construct under Pveg. The page states these
are 26-fold, 18-fold and 22-fold above the matching un-displayed controls.

- **Why it is here.** It is a second, independent whole-cell loading for
  displayed GolB. It agrees with S76's 4.62 µmol/g within 13 %, and both
  sit about 50x above this repository's expression-derived `q_max` of 0.0913.
  Two independent measurements agreeing against one derivation is the reason
  ISSUES 92 was opened.
- **⚠️ VERIFICATION CAVEAT. The page was not read directly.** `parts.igem.org`
  returned HTTP 403 to the fetcher and the current `registry.igem.org` renders
  empty to it. The figures above come from the search index, consistent across
  two independent queries on 2026-09-07. **A human must open the page and
  confirm the numbers before any of them is used for anything but a scenario.**
  This is the same class of caveat as S59's paywalled body text.
- **Limits.** *B. subtilis*, not *E. coli*; TasA and CotC anchors, not this
  project's; an iGEM Registry entry, not a peer-reviewed paper; and no
  gold species, pH or isotherm is given, so it is a single endpoint and not a
  fitted saturation capacity.
- **Used in:** `params/capture_design.yaml`
  `literature.igem2015_bba_k1701000_loading`; ISSUES 92.


**S78. Nazir R., Mohsin M., Siddiqi T. O. (2022).** "Real time optical
detection of gold in living cells through genetically-encoded probe."
*RSC Advances* **12**, 23193-23203.
doi:[10.1039/D2RA02574D](https://doi.org/10.1039/D2RA02574D).
[Open full text](https://pubs.rsc.org/en/content/articlehtml/2022/ra/d2ra02574d).

Checked against the publisher full text on 2026-09-18. The authors inserted
the *Salmonella* GolB recognition domain between ECFP and Venus, purified the
fusion protein, titrated gold in 20 mM MOPS, and fitted the one-site saturation
equation `S = [L]/(K_d + [L])`. Table 1 reports `K_d = 0.7 µM` for wild-type
GolSeN and `0.2-1.15 µM` for the three variants. The article body drops the
micro symbol in one sentence, but the table header, concentration range and
abstract confirm micromolar units.

- **Why it is adopted.** `0.7 µM` is the closest published value with the same
  mathematical meaning as this model's apparent `K_Au`: it uses GolB and comes
  from a fitted saturation curve over nanomolar-to-micromolar gold.
- **Limits.** The construct is soluble ECFP-GolB-Venus, not surface-displayed
  GolB. The ligand is HAuCl4 in MOPS, not Au(I)-thiosulfate in leachate.
  Therefore it is a literature proxy, not a project-matrix measurement.
- **Used in:** `params/recovery_chain.yaml :: V1_capture.K_Au`;
  `params/capture_design.yaml :: binding_proxies.nazir2022_golsen_wt_K_Au`;
  ISSUES 1 and 22.


**S79. Checa S. K., Espariz M., Audero M. E. P., Botta P. E., Spinelli S. V.,
Soncini F. C. (2007).** "Bacterial sensing of and resistance to gold salts."
*Molecular Microbiology* **63**, 1307-1318.
doi:[10.1111/j.1365-2958.2007.05590.x](https://doi.org/10.1111/j.1365-2958.2007.05590.x).
[Publisher full text](https://onlinelibrary.wiley.com/doi/10.1111/j.1365-2958.2007.05590.x).

Checked against the publisher full text on 2026-09-18. In matched whole-cell
reporter experiments, GolS had apparent half-maximal responses of `0.2 µM` for
gold and `10.4 µM` for copper, a 52-fold gold preference.

- **Why it is used.** It is a matched Au/Cu experiment in cells and supplies a
  conservative working selectivity ratio while no comparable GolB experiment
  exists.
- **Limit.** GolS is the transcriptional regulator, not the GolB capture
  protein. Its `K_app,50` values are response constants, not GolB dissociation
  constants. `alpha = 52` and the derived `K_Cu = 36.4 µM` are therefore a
  labelled competition scenario only.
- **Used in:** `params/capture_design.yaml ::
  binding_proxies.checa2007_gols_selectivity_alpha`; WIKI_BIORECOVERY_DRAFT;
  ISSUES 22.

**S80. Kay K. L., Zhou L., Tenori L., Bradley J. M., Singleton C., Kihlken
M. A., Ciofi-Baffoni S., Le Brun N. E. (2017).** "Kinetic analysis of copper
transfer from a chaperone to its target protein mediated by complex
formation." *Chemical Communications* **53**(8), 1397-1400.
doi:[10.1039/c6cc08966f](https://doi.org/10.1039/c6cc08966f).

Metadata checked 2026-09-19 against PubMed PMID 28078344; the publisher page
refused the request, so the full text is NOT verified. Cu(I) transfer from the
Atx1-type chaperone CopZ of *Bacillus subtilis* to its target CopAab proceeds
at about `267 s⁻¹` at 25 °C, so copper handling by a Cys-X-X-Cys protein is
complete in milliseconds.

- **Why it is used.** It sets the timescale on which effective copper reaches
  its equilibrium share. Seconds against a capture contact of hours is what
  allows copper to be shown at equilibrium and left off the time graph.
- **Limit.** This is chaperone-to-target transfer between purified proteins,
  not capture of copper from a leachate onto displayed GolB. It supplies a
  timescale, not a `k_on,Cu` or a `k_off,Cu`, and no Cu-GolB rate constant has
  been measured.
- **Used in:** `WIKI_BIORECOVERY_DRAFT`, the capture graphs section and
  capture assumptions 7 and 8.
