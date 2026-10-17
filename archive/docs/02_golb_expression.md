**Modeling Surface Site Density for GolB-Based Gold Biosorption**

# 1. Purpose and scope

Our project recovers gold from electronic waste in two stages:
bioleaching mobilizes gold from the waste into a leachate, and
biosorption then captures the dissolved gold using engineered bacteria.
For biosorption we display the gold-binding protein GolB on the cell
surface, so that gold ions in the leachate bind directly to accessible
protein rather than having to enter the cell. The quantity that
determines how much gold a single cell can capture is the surface site
density --- the number of active, gold-accessible GolB molecules on the
outer membrane.

This model predicts that surface site density from first principles,
tracing the gene-expression cascade that produces it: transcription of
the GolB gene into mRNA, translation into cytoplasmic protein, export
and anchoring of that protein at the surface, and finally the fraction
of surface protein that is correctly folded and able to bind gold.
Because our team works from published data rather than our own
measurements, every parameter is a literature-grounded estimate, and the
two parameters that cannot be read directly from the literature are
treated as explicitly fitted values.

# 2. Model structure

We represent the system as four connected pools, expressed as molecules
per cell. Each pool is fed by the process upstream of it and drained by
degradation and by dilution as the cell grows and divides:

mRNA *m* → cytoplasmic protein *P*~c~ → surface-displayed protein *P*~s~
→ active sites *A*

Dilution appears because a growing cell continually doubles its volume;
even a perfectly stable protein is diluted at the growth rate. For
fast-turnover species such as mRNA this term is small, but for stable
proteins it is often the dominant loss.

# 3. Governing equations

The cascade is written as a system of ordinary differential equations.
Transcription produces mRNA at a rate set by promoter strength and copy
number, and mRNA is lost to degradation and dilution:

d*m*/d*t* = *α*·*N* − (*δ*~m~ + *μ*)·*m*

Translation converts each mRNA into protein; the cytoplasmic pool is
drained by export to the surface, by degradation, and by dilution:

d*P*~c~/d*t* = *β*·*m* − (*k_sec* + *δ*~c~ + *μ*)·*P*~c~

Export anchors protein at the surface. Because the membrane holds a
finite number of anchors, the arrival term saturates as the surface
fills toward its capacity:

d*P*~s~/d*t* = *k_sec*·*P*~c~·(1 − *P*~s~/*P*~s,max~) − (*δ*~s~ +
*μ*)·*P*~s~

Finally, only a fraction of the displayed protein is correctly folded
and gold-accessible, so the number of active binding sites is:

*A* = *f*·*P*~s~

# 4. Parameters

The table below lists every parameter, the value used in the simulation,
and its basis in the literature. The central-dogma constants are
standard order-of-magnitude values for Escherichia coli. The surface
capacity comes from characterized autodisplay systems. Two parameters
--- the display rate k_sec and the functional fraction f --- depend on
the specific construct and are treated as fitted; the gold dissociation
constant K_d is a placeholder because no clean experimental value for
GolB has been reported.

  ------------------------------------------------------------------------------------------------
  **Symbol**   **Meaning**             **Value**   **Units**              **Basis / source**
  ------------ ----------------------- ----------- ---------------------- ------------------------
  α            Transcription rate per  0.5         mRNA·min⁻¹·copy⁻¹      Typical E. coli promoter
               plasmid copy (promoter                                     output (BioNumbers)
               strength)                                                  

  N            Plasmid copy number     20          copies/cell            Medium-copy backbone,
                                                                          pBR322-like (≈15--20)

  δₘ           mRNA degradation rate   0.20        min⁻¹                  E. coli mRNA half-life
                                                                          ≈2--5 min (t½≈3.5 min)

  β            Translation rate per    4.0         protein·min⁻¹·mRNA⁻¹   Typical E. coli
               mRNA (RBS strength)                                        translation efficiency
                                                                          (BioNumbers)

  k_sec        Export /                0.10        min⁻¹                  Set by the display
               surface-display rate                                       scaffold; fitted
               constant                                                   parameter

  δ_c          Cytoplasmic protein     0.005       min⁻¹                  ≈0 for a stable protein
               degradation                                                

  δ_s          Surface protein loss    0.005       min⁻¹                  Assumed
                                                                          dilution-dominated

  μ            Growth (dilution) rate  0.02        min⁻¹                  Doubling time ≈35 min (μ
                                                                          = ln2 / t_double)

  f            Fraction folded +       0.5         --                     Folding/accessibility;
               gold-accessible                                            fitted parameter

  P_s,max      Maximum surface anchor  1×10⁵       sites/cell             Autodisplay reaches
               sites                                                      \>10⁵ molecules/cell
                                                                          (Jose & Meyer)

  K_d          GolB--Au(I)             10          µM                     Placeholder -- no clean
               dissociation constant                                      experimental K_d; source
                                                                          or fit
  ------------------------------------------------------------------------------------------------

# 5. Steady-state site density

Setting the time derivatives to zero and substituting down the cascade
gives closed-form steady-state values (in the non-saturating limit,
valid whenever site density stays well below capacity, which holds
here):

*m*~\*~ = *αN* / (*δ*~m~ + *μ*)

*P*~c\*~ = *βm*~\*~ / (*k_sec* + *δ*~c~ + *μ*)

*P*~s\*~ = *k_secP*~c\*~ / (*δ*~s~ + *μ*)

Combining these yields a single expression for the quantity we care
about:

*A*~\*~ = *f·α·N·β·k_sec* / \[(*δ*~m~ + *μ*)(*k_sec* + *δ*~c~ +
*μ*)(*δ*~s~ + *μ*)\]

This makes the design logic explicit: site density scales linearly with
promoter strength, copy number, and translation strength, while the
secretion rate partitions protein between the cytoplasm and the surface.
With the parameters above, the model gives roughly 45 mRNA, 1,460
cytoplasmic protein, 5,500 surface protein, and about 2,900 active sites
per cell.

# 6. Coupling to gold uptake

The active-site count feeds a Langmuir adsorption isotherm that predicts
how much gold a cell binds at a given leachate concentration *C*.
Because GolB binds Au(I) through a single Cys-X-X-Cys motif, each site
captures one gold ion, so the maximum uptake equals the site count *A*:

*q*(*C*) = *A*·*C* / (*K*~d~ + *C*)

This is the bridge between the expression model and the actual
objective: whatever raises the active-site count raises the recovery
ceiling proportionally.

# 7. Simulation results

Figure 1 shows the model run to steady state and two analyses derived
from it.

![](media/image1.jpg){width="6.5in"
height="4.770833333333333in"}

*Figure 1. (a) Transcript dynamics; (b) protein and active-site
dynamics; (c) steady-state site density versus display rate; (d)
normalized parameter sensitivity of the steady-state site density.*

**Panel (a) --- Transcript dynamics.** mRNA reaches steady state (about
45 copies per cell) within roughly 20--30 minutes. This is fast because
mRNA turns over quickly; a species equilibrates on the timescale of a
few of its own half-lives, and mRNA half-life is only a few minutes.

**Panel (b) --- Protein and active sites.** The cytoplasmic pool
(≈1,460), the surface pool (≈5,500), and the active sites (≈2,900, being
half the surface pool) rise much more slowly, taking around 150--200
minutes to plateau. The slowness comes from the protein loss being
dominated by dilution, which is far slower than mRNA turnover. Notably
the surface pool exceeds the cytoplasmic pool: export continuously
drains the cytoplasm, whereas the surface pool is lost only to slow
dilution, so displayed protein accumulates.

**Panel (c) --- Sensitivity to display rate.** Steady-state site density
is plotted against the export rate k_sec on a logarithmic axis, giving
an S-shaped curve. When export is slow, protein remains trapped in the
cytoplasm and few sites form. As export speeds up, more protein reaches
the surface, but above roughly 1 min⁻¹ the curve flattens near 3,600
sites because transcription and translation, not export, now set the
ceiling. The marked point is the operating value used (0.1 min⁻¹). The
practical message is that simply making secretion faster yields
diminishing returns.

**Panel (d) --- Which parameter moves site density.** Each bar is a
normalized sensitivity: the fractional change in steady-state site
density per fractional change in that parameter. Promoter strength (α),
copy number (N), translation strength (β), and functional fraction (f)
all sit near +1, meaning a 1% increase in any of them gives about a 1%
increase in sites --- these are the highest-leverage engineering
handles. The export rate k_sec is only about +0.2 (sublinear, because it
appears in both the numerator and a denominator), confirming the
diminishing returns seen in panel (c). Growth rate (μ) is the strongest
negative influence because it appears in all three loss terms, and mRNA
degradation (δₘ) is also strongly negative; cytoplasmic and surface
degradation matter little at these values.

Figure 2 translates site density into predicted gold capture.

![](media/image2.png){width="5.416666666666667in"
height="4.145833333333333in"}

*Figure 2. Langmuir uptake curves for three engineered site densities
(base, 2×, and 5×), showing gold ions bound per cell as a function of
leachate Au(I) concentration.*

Each curve rises with leachate gold concentration and plateaus at its
own site density --- the plateau is simply the number of sites, since
each binds one ion. The three curves correspond to the base design
(≈2,900 sites) and to two- and five-fold improvements. Half-saturation
occurs at a concentration equal to *K*~d~ (10 µM here), and above
roughly 100 µM every design is near saturation. The key takeaway is that
at any fixed leachate concentration, gold captured scales directly with
engineered site density, so the expression-level improvements identified
in Figure 1 carry straight through to recovery capacity.

# 8. Assumptions and limitations

The model is deterministic and describes an average cell, so it does not
capture cell-to-cell variability. Expression is treated as constant and
constitutive; induction timing, resource competition, and the growth
burden of heavy membrane-protein overexpression are not included. The
drain on the cytoplasmic pool is kept first-order so that a closed-form
steady state exists, with saturation applied only to surface arrival;
this is accurate while site density stays well below capacity, which is
the case here (thousands of sites against a ceiling of 10⁵). Finally,
the parameters are literature order-of-magnitude estimates rather than
measurements of our exact construct, and the gold dissociation constant
in particular is a placeholder that should be sourced from a biosorption
isotherm or fitted.

# 9. Literature basis

**Surface-display capacity.** Jose J, Meyer TF. Autodisplay: efficient
bacterial surface display of recombinant proteins. Applied Microbiology
and Biotechnology (2006) --- reports more than 10⁵ recombinant molecules
displayed per cell via the AIDA-I autotransporter.

**GolB structure and gold binding.** Structural Insights and the
Surprisingly Low Mechanical Stability of the Au--S Bond in the
Gold-Specific Protein GolB. Journal of the American Chemical Society
(2015) --- apo- and Au(I)-bound GolB crystal structures and the
Cys-X-X-Cys binding motif. Tolbatov I, Re N, Coletti C, Marrone A. An
Insight on the Gold(I) Affinity of golB Protein via Multilevel
Computational Approaches (2019).

**Gold sensing and the gol system.** Bacterial gold sensing and
resistance. BioMetals (2011) --- GolS/GolB selectivity for Au(I). GolS
controls the response to gold by hierarchical induction of
Salmonella-specific genes. Molecular Microbiology (2007) --- GolB as a
small cytoplasmic gold-binding protein.

**Prior GolB display precedent.** iGEM Registry part BBa_K1701000 ---
GolB displayed on the E. coli surface for selective enrichment of gold
ions from mixed-metal media (parts.igem.org).

**Central-dogma parameters.** BioNumbers database
(bionumbers.hms.harvard.edu) for E. coli mRNA half-lives, translation
rates, and growth rates.
