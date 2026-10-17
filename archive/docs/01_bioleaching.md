# Bioleaching Modelling --- Process Overview

Bacteria express tetrathionate hydrolase (TetH), which breaks
tetrathionate down into thiosulfate. The thiosulfate then leaches gold
(and, unavoidably, copper) from crushed PCB particles. The chain of
models is:

- Enzyme production rate

- Tetrathionate consumption rate

- Thiosulfate production rate (with Cu(II) coupling)

- Gold leaching rate --- Model A (oxygen only) and Model B (oxygen +
  Cu(II))

- Copper leaching rate and the Cu(I)/Cu(II) balance

- pH change (to be built)

## Enzyme Production

Bacteria produce tetrathionate hydrolase (TetH), which hydrolyses
tetrathionate to thiosulfate.^\[1\]^

**Reaction**

bacteria → TetH enzyme (E)

**Model**

Enzyme concentration is governed by three processes --- production
(proportional to biomass), first-order degradation, and dilution as the
cells grow ^\[3\]^:

$$\frac{d\lbrack E\rbrack}{dt} = \ k_{syn} \cdot X\ \  - \ \ (k_{\deg} + \mu) \cdot E$$

At steady state, \[E\]ₛₛ = k_syn·X / (k_deg + μ), reached over a
characteristic time of 1/(k_deg+μ) ^\[3\]^. Under the fixed-biomass
assumption (no growth), μ = 0.

**Parameters**

  ------------- ---------------------------- --------------- ------------
   **Symbol**           **Meaning**             **Unit**      **Value /
                                                               source**

      \[E\]      Active TetH concentration      µmol L⁻¹        state
                                                               variable

        t                   Time                   min           ---

        X          Biomass concentration        cell L⁻¹       input /
                                                               measured

      k_syn      Enzyme synthesis rate per     µmol cell⁻¹    calibrate
                            cell                  min⁻¹      

      k_deg       Enzyme degradation rate         min⁻¹       ≈1.1×10⁻³
                                                                \[4\]

        Μ           Growth-dilution rate          min⁻¹        0 if no
                      (=ln2/t_double)                        growth \[3\]
  ------------- ---------------------------- --------------- ------------

## Tetrathionate Consumption

**Reactions**

TetH hydrolyses tetrathionate via a disulfane-monosulfonic-acid (DSMSA)
intermediate ^\[1\]^:

S₄O₆²⁻ + H₂O → HS₂SO₃⁻ + HSO₄⁻

HS₂SO₃⁻ → S₂O₃²⁻ + S⁰ + H⁺

Lumped into a single overall reaction:

S₄O₆²⁻ + H₂O → S₂O₃²⁻ + S⁰ + SO₄²⁻ + 2H⁺

Copper(II) leached from the PCB re-oxidises thiosulfate back to
tetrathionate, so a regeneration term is required ^\[6\]\[7\]^:

2Cu(II) + 2S₂O₃²⁻ → 2Cu(I) + S₄O₆²⁻

**Model**

Consumption follows irreversible Michaelis--Menten kinetics ^\[5\]^; the
parasitic reaction above adds tetrathionate back:

$$\frac{d\left\lbrack S_{4}O_{6}^{2 -} \right\rbrack}{dt} = \ F_{in} - \frac{k_{cat} \cdot E \cdot \left\lbrack S_{4}O_{6}^{2 -} \right\rbrack}{K_{m} + \ \left\lbrack S_{4}O_{6}^{2 -} \right\rbrack} + \ k₁ \cdot \lbrack Cu(II)\rbrack \cdot \lbrack S₂O₃²⁻\rbrack$$

**Parameters**

  ------------- ---------------------------- --------------- ------------
   **Symbol**           **Meaning**             **Unit**      **Value /
                                                               source**

   \[S₄O₆²⁻\]   Tetrathionate concentration     µmol L⁻¹        state
                                                               variable

      F_in        Tetrathionate feed rate    µmol L⁻¹ min⁻¹   operating
                                                                choice

      k_cat       Turnover number of TetH         min⁻¹       unmeasured
                                                                 ---
                                                              calibrate
                                                                \[1\]

       K_m           Michaelis constant         µmol L⁻¹       50--2400
                                                                \[2\]

        E        Active TetH concentration      µmol L⁻¹     from Section
                                                                  1

       k₁                Parasitic           L µmol⁻¹ min⁻¹  calibrate (↑
                  Cu(II)--thiosulfate rate                     w/o NH₃)
                          constant                            \[6\]\[7\]

   \[Cu(II)\]     Copper(II) concentration      µmol L⁻¹     from Section
                                                                  5
  ------------- ---------------------------- --------------- ------------

# Thiosulfate Production

Thiosulfate is produced as a stoichiometric multiple (Y) of
tetrathionate consumed.

$$d\frac{\left\lbrack S_{2}O_{3}^{2 -} \right\rbrack}{dt} = \frac{k_{cat} \cdot E \cdot \left\lbrack S_{4}O_{6}^{2 -} \right\rbrack}{K_{m} + \ \left\lbrack S_{4}O_{6}^{2 -} \right\rbrack}\ \lbrack production\ only\rbrack$$

Adding the parasitic loss to Cu(II) (2 thiosulfate consumed per reaction
extent) and the loss to gold leaching gives the full balance:

$\frac{d\left\lbrack S_{2}O_{3}^{2 -} \right\rbrack}{dt}$
$\  = \frac{k_{cat} \cdot E \cdot \left\lbrack S_{4}O_{6}^{2 -} \right\rbrack}{K_{m} + \left\lbrack S_{4}O_{6}^{2 -} \right\rbrack} - 2 \cdot k_{1} \cdot \left\lbrack Cu(II) \right\rbrack \cdot \left\lbrack S_{2}O_{3}^{2 -} \right\rbrack - \left( \frac{2}{V} \right) \cdot R_{Au} - \left( \frac{1}{V} \right) \cdot R_{Cu}$

where R_Au is the gold-leaching rate (µmol min⁻¹) and R_Cu is the
copper-leaching rate (µmol min⁻¹) from Sections 4 and 5. Each gold atom
consumes 2 thiosulfate, and, depending on the oxidant, each copper atom
consumes 2 or 4 thiosulfate. The 1/V converts the surface rate to a
concentration rate.

**Parameters**

  ------------- ---------------------------- ----------------- ------------
   **Symbol**           **Meaning**              **Unit**       **Value /
                                                                 source**

   \[S₂O₃²⁻\]    Thiosulfate concentration       µmol L⁻¹         state
                                                                 variable

        Y        Stoichiometric yield (S₂O₃         ---          1 \[1\]
                         per S₄O₆)            (dimensionless)  

        V              Reactor volume                L          operating
                                                                  choice

      R_Au           Gold leaching rate         µmol min⁻¹     from Section
                                                                    4

      R_Cu          Copper leaching rate        µmol min⁻¹     From Section
                                                                    5
  ------------- ---------------------------- ----------------- ------------

# Gold Leaching

**Reactions**

Metallic gold is oxidised and complexed by thiosulfate. The oxidation
and complexation happen in a single surface step (free Au⁺ does not
persist in solution) ^\[8\]^:

Au⁰ + 2S₂O₃²⁻ → Au(S₂O₃)₂³⁻ + e⁻ (anodic half-reaction)

With oxygen as the terminal oxidant, the overall reaction is:

4Au⁰ + 8S₂O₃²⁻ + O₂ + 2H₂O → 4Au(S₂O₃)₂³⁻ + 4OH⁻

Because copper is leached from the PCB, a second, faster pathway exists
in which Cu(II) is the oxidant ^\[11\]\[12\]^:

Au⁰ + 2S₂O₃²⁻ + Cu(II) → Au(S₂O₃)₂³⁻ + Cu(I)

**Gold Surface-Area Equation**

Gold on a PCB is a thin plated film, not a bulk particle, so it
dissolves by thinning at roughly constant face area until it is
exhausted (it does not shrink inward). The exposed area is fixed by the
gold mass and plating thickness, independent of how finely the board is
crushed:

$$A_{Au}\  = \frac{m_{Au}}{\rho_{Au}\  \cdot \ t_{film}}$$

$A_{Au}\ (t)\  \approx \ A_{Au}(0)\ \$while gold remains, → 0 once
exhausted

Derivation: a film of area A and thickness t has volume A·t = m/ρ, so A
= m/(ρ·t).

### Model A --- Oxygen only (conservative)

Starting from simple mass action, gold leaching depends on oxygen
(oxidant) and thiosulfate (ligand). Because gold sits on the particle
surface, the rate scales with a time-dependent gold area --- a
shrinking-surface variant of the shrinking-core model

Since the surface has a finite number of reaction sites, each reactant
enters through a saturating (Langmuir) term ^\[8\]\[10\]^. Tracking
solid gold in mol and dissolved gold as a concentration:

$$R_{Au}\  = \ k_{Au},O_{2} \cdot \ A_{Au}(t) \cdot \frac{\left\lbrack O_{2} \right\rbrack}{K_{O_{2}} + \left\lbrack O_{2} \right\rbrack}\  \cdot \frac{\left\lbrack S_{2}O_{3}^{2 -} \right\rbrack}{K_{S} + \left\lbrack S_{2}O_{3}^{2 -} \right\rbrack}$$

$$\frac{dn_{Au}}{dt} = \  - \ R_{Au}$$

$$\frac{d\left\lbrack Au\left( S_{2}O_{3} \right)_{2}^{3 -} \right\rbrack}{dt} = + \frac{R_{Au}}{V}$$

### Model B --- Oxygen + Copper(II) (realistic)

Cu(II) provides a parallel oxidant pathway. Parallel pathways add
(either oxidant alone can dissolve gold), while area, thiosulfate, and
passivation multiply everything (all are required regardless of
oxidant). Oxygen enters only its own term --- Cu(II) does not need O₂ at
the gold surface ^\[15\]^:

$$R_{Au}\  = \ A_{Au}(t) \cdot \frac{\left\lbrack S_{2}O_{3}^{2 -} \right\rbrack}{K_{S} + \left\lbrack S_{2}O_{3}^{2 -} \right\rbrack}\ \  \cdot \ \{ k_{Au,O_{2}} \cdot \frac{\left\lbrack O_{2} \right\rbrack}{K_{O_{2}} + \left\lbrack O_{2} \right\rbrack}\  + \ k_{Au,Cu} \cdot \frac{\left\lbrack Cu(II) \right\rbrack}{K_{Cu} + \left\lbrack Cu(II) \right\rbrack}\ \}$$

$$\frac{dn_{Au}}{dt}\  = \  - R_{Au}$$

$$\ \ \ \ \ \ \ \ d\frac{\left\lbrack AuO_{3}^{3 -} \right\rbrack}{dt}\  = \  + \frac{R_{Au}}{V}$$

**Parameters**

  ----------------- ---------------------------- --------------- --------------
     **Symbol**             **Meaning**             **Unit**       **Value /
                                                                    Source**

        n_Au            Solid gold remaining      mol (or µmol)  state variable

   \[Au(S₂O₃)₂³⁻\]     Dissolved gold complex       µmol L⁻¹     state variable
                             (product)                           

        A_Au            Exposed gold area =            m²        from geometry
                         m_Au/(ρ_Au·t_film)                      

        ρ_Au                Gold density             kg m⁻³          19300

       t_film          Gold plating thickness           M        0.05--1 ×10⁻⁶
                                                                  (board spec)

       k_Au,O₂      Gold rate constant, O₂ route µmol m⁻² min⁻¹  ≈11 (1.9×10⁻⁷
                                                                  mol m⁻²s⁻¹)
                                                                  \[9\]\[10\]

       k_Au,Cu       Gold rate constant, Cu(II)  µmol m⁻² min⁻¹   ≈10³× larger
                               route                              \[11\]\[12\]

        K_O₂             O₂ half-saturation         µmol L⁻¹       calibrate
                                                                     (\~50)

         K_S        Thiosulfate half-saturation     µmol L⁻¹       calibrate
                                                                   (\~5×10⁴)

        K_Cu           Cu(II) half-saturation       µmol L⁻¹       Calibrate
  ----------------- ---------------------------- --------------- --------------

## Copper Leaching and the Cu(I)/Cu(II) Balance

**Reactions**

Metallic copper dissolves as Cu(I)--thiosulfate. Two oxidant pathways
exist ^\[13\]\[7\]^:

With oxygen as oxidant:

4Cu⁰ + O₂ + 8S₂O₃²⁻ + 2H₂O → 4\[Cu(S₂O₃)₂\]³⁻ + 4OH⁻

With Cu(II) as oxidant (comproportionating one Cu(II) plus one Cu⁰ gives
two Cu(I)):

Cu⁰ + Cu²⁺ → 2Cu⁺

Cu⁺ + 2S₂O₃²⁻ → \[Cu(S₂O₃)₂\]³⁻

Cu⁰ + Cu²⁺ + 4S₂O₃²⁻ → 2\[Cu(S₂O₃)₂\]³⁻

Cu(I) is re-oxidised to Cu(II) by oxygen, and Cu(II) is reduced back to
Cu(I) by thiosulfate and by gold leaching ^\[7\]\[15\]^:

4Cu(I) + O₂ + 2H₂O → 4Cu(II) + 4OH⁻

2Cu(II) + 2S₂O₃²⁻ → 2Cu(I) + S₄O₆²⁻

Au⁰ + 2S₂O₃²⁻ + Cu(II) → Au(S₂O₃)₂³⁻ + Cu(I)

**Copper Surface-Area Equation**

Copper is bulk metal (traces, planes, inner layers), so its particles
genuinely erode inward --- a true shrinking-particle geometry

The initial area follows the surface-to-volume ratio 6/d for crushed
particles of size d; as copper is consumed, the area falls as the
two-thirds power of the fraction remaining (area ∝ r², volume ∝ r³)
^\[14\]^:

$$A_{Cu}(0) = \ 6 \cdot \frac{m_{Cu}}{(\rho_{Cu}\  \cdot \ d)}$$

$$A_{Cu}(t)\  = \ A_{Cu}(0)\  \cdot \ \left( \frac{n_{Cu}}{n_{Cu}(0)} \right)^{\frac{2}{3}}$$

**Rates**

Copper leaching, oxygen route (v₁A) and combined-oxidant route (v₁B);
gold-leaching Cu(I) return (v₂); parasitic tetrathionate regeneration
(v₃); Cu(I) re-oxidation by oxygen (v₄):

$$v_{1A}\  = \ {2k}_{Cu,O_{2}} \cdot A_{Cu}(t) \cdot \frac{\left\lbrack O_{2} \right\rbrack}{K_{O_{2}} + \left\lbrack O_{2} \right\rbrack} \cdot \frac{\left\lbrack S_{2}O_{3}^{2 -} \right\rbrack}{K_{S} + \left\lbrack S_{2}O_{3}^{2 -} \right\rbrack}\ $$

$$v_{1B}\  = \ A_{Cu}(t) \cdot \frac{\left\lbrack S_{2}O_{3}^{2 -} \right\rbrack}{K_{S} + \left\lbrack S_{2}O_{3}^{2 -} \right\rbrack} \cdot \{\ {2k}_{Cu,O_{2}} \cdot \frac{\left\lbrack O_{2} \right\rbrack}{K_{O_{2}} + \left\lbrack O_{2} \right\rbrack}\  + \ {4k}_{Cu,\ \ Cu^{2 +}} \cdot \frac{\left\lbrack Cu(II) \right\rbrack}{K_{Cu} + \left\lbrack Cu(II) \right\rbrack}\ \}\ $$

$$v₂\  = \ R_{Au}\ \ (gold - leaching\ rate,\ Section\ 4)$$

$$v₃\  = \ k₃ \cdot \lbrack Cu(II)\rbrack \cdot \lbrack S₂O₃²⁻\rbrack$$

$$v₄\  = \ k₄ \cdot \lbrack O₂\rbrack \cdot \lbrack Cu(I)\rbrack$$

**Cu(I) model**

Cu(I) is produced by copper leaching, by gold leaching, and by the
parasitic reaction, and is consumed by oxygen re-oxidation. Reading
coefficients off the balanced reactions (comproportionating gives 2
Cu(I) per extent; parasitic gives 2 Cu(I) per extent; O₂ re-oxidation
consumes 4 Cu(I) per extent):

$$\frac{d\left\lbrack Cu(I) \right\rbrack}{dt}\  = \ \left( \frac{1}{V} \right) \cdot 2 \cdot v₁B\  + \ \left( \frac{1}{V} \right) \cdot v₂\  + \ 2 \cdot v₃\  - \ 4 \cdot v₄$$

**Cu(II) model**

Cu(II) is produced only by oxygen re-oxidation of Cu(I), and consumed by
the comproportionating leach, the parasitic reaction, and gold leaching:

$$d\frac{\left\lbrack Cu(II) \right\rbrack}{dt}\  = \ 4 \cdot v₄\  - \ \left( \frac{1}{V} \right) \cdot v₁B\  - \ \left( \frac{1}{V} \right) \cdot v₂\  - \ 2 \cdot v₃$$

**Parameters**

  ------------- ---------------------------- --------------- ------------
   **Symbol**           **Meaning**             **Unit**      **Value /
                                                               source**

    \[Cu(I)\]     Copper(I) concentration       µmol L⁻¹        state
                    (cannot leach gold)                        variable

   \[Cu(II)\]     Copper(II) concentration      µmol L⁻¹        state
                       (gold oxidant)                          variable

      n_Cu         Solid copper remaining          mol          state
                                                               variable

      A_Cu         Exposed copper area =           m²            from
                  6m_Cu/(ρ_Cu·d)·(n/n₀)\^⅔                     geometry

      ρ_Cu             Copper density            kg m⁻³          8960

        d          Crushed particle size            m         2--6×10⁻³
                                                             (your feed)

     k_Cu,O₂      Copper rate constant, O₂   µmol m⁻² min⁻¹   calibrate
                           route                               (Ea≈25.8
                                                               kJ/mol)
                                                                \[13\]

     k_Cu,Cu    Copper rate constant, Cu(II) µmol m⁻² min⁻¹   calibrate
                           route                             

       k₃       Parasitic (Cu(II)+S₂O₃) rate L µmol⁻¹ min⁻¹      ≈ k₁
                          constant                            \[6\]\[7\]

       k₄         Cu(I) re-oxidation rate    L µmol⁻¹ min⁻¹   calibrate
                          constant                           
  ------------- ---------------------------- --------------- ------------

# References

**\[1\]** Y. Kanao et al., \"Tetrathionate hydrolase from the
acidophilic microorganisms,\" Front. Microbiol., vol. 15, 1338669, 2024.

**\[2\]** Y. Kanao, K. Kamimura, and T. Sugio, \"Purification of a
tetrathionate hydrolase from Acidithiobacillus ferrooxidans,\" J.
Biotechnol., vol. 132, pp. 16--22, 2007.

**\[3\]** U. Alon, An Introduction to Systems Biology, 2nd ed. Boca
Raton, FL: CRC Press, 2019.

**\[4\]** M. R. Maurizi, \"Proteases and protein degradation in
Escherichia coli,\" Experientia, vol. 48, pp. 178--201, 1992.

**\[5\]** G. E. Briggs and J. B. S. Haldane, \"A note on the kinetics of
enzyme action,\" Biochem. J., vol. 19, pp. 338--339, 1925.

**\[6\]** J. J. Byerley, S. A. Fouda, and G. L. Rempel, \"Kinetics and
mechanism of the oxidation of thiosulphate ions by copper(II) ions in
aqueous ammonia solution,\" J. Chem. Soc. Dalton Trans., pp. 889--893,
1973.

**\[7\]** P. L. Breuer and M. I. Jeffrey, \"The reduction of copper(II)
and the oxidation of thiosulfate and oxysulfur anions in gold leaching
solutions,\" Hydrometallurgy, vol. 70, pp. 163--173, 2003.

**\[8\]** G. Senanayake, \"Analysis of reaction kinetics, speciation and
mechanism of gold leaching and thiosulfate oxidation by ammoniacal
copper(II) solutions,\" Hydrometallurgy, vol. 75, pp. 55--75, 2004.

**\[9\]** S. Zhang and M. J. Nicol, \"An electrochemical study of the
dissolution of gold in thiosulfate solutions Part I: Alkaline
solutions,\" J. Appl. Electrochem., vol. 33, pp. 767--775, 2003.

**\[10\]** O. Sitando et al., \"A review of factors affecting gold
leaching in non-ammoniacal thiosulfate solutions,\" Hydrometallurgy,
vol. 178, pp. 151--175, 2018.

**\[11\]** M. G. Aylmore and D. M. Muir, \"Thiosulfate leaching of gold
--- a review,\" Miner. Eng., vol. 14, no. 2, pp. 135--174, 2001.

**\[12\]** D. Maharaj, T. Moyo, and J. Petersen, \"Ammonium thiosulfate
leaching of gold from electronic printed circuit boards --- effect of
solution copper concentration,\" J. S. Afr. Inst. Min. Metall., vol.
124, no. 12, pp. 711--718, 2024.

**\[13\]** E. Salinas-Rodríguez et al., \"Leaching of copper contained
in waste printed circuit boards using the thiosulfate--oxygen system: a
kinetic approach,\" Materials, vol. 15, no. 7, 2354, 2022.

**\[14\]** O. Levenspiel, Chemical Reaction Engineering, 3rd ed. New
York, NY: Wiley, 1999.

**\[15\]** P. L. Breuer and M. I. Jeffrey, \"The effect of ionic
strength and buffer choice on the decomposition of tetrathionate; and
the role of copper(II) as oxidant in gold thiosulfate leaching,\"
Hydrometallurgy, vol. 65, pp. 145--157, 2002.
