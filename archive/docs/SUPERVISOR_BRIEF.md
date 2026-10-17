# Progress brief

**Tier 2, record.** Correspondence, dated. It says what was true on the day it
was written and is not updated afterwards. `AGENTS.md` section 11.

**iGEM 2026 · 12 August 2026**

For software and modelling, each member was working on a separate phase of the
process. That is now done, and this week we are reviewing all the models and
putting them together. We have also finished a software tool that reads the UV
spectrometry output from the NanoDrop One and converts it into the
concentration of metal ions in the sample, including gold. The wet lab will
test it this week. Alongside this we are simulating the proteins under
different conditions, to understand how their behaviour varies.

We will begin putting our work on the wiki this week, and we are now thinking
about how to present it so that it stands out.

## This week's main piece of work

The leaching model has been rebuilt as a three stage process and merged into
the combined model. Instead of running everything in one vessel, the bacteria
are grown and the enzyme is harvested and purified first, the enzyme then
converts the feedstock into the leaching agent in a second vessel, and only
then is the crushed circuit board added in a third. This matters because
published work says our enzyme does not fold into a working form inside the
bacteria and has to be refolded outside them. The three vessel route is the
first version of the process that could work at all.

Before merging it we rebuilt the model independently and checked it against the
results it reports. Fourteen of fourteen numbers matched, and three mass
balances that the original does not test also close. Five rate constants that
had been missing since the start now have sourced values, so the leaching model
runs end to end for the first time.

## The most useful thing we found

The model says the process is decided by a reaction nobody had been watching.
Copper comes off the board in a form that is harmless. Dissolved oxygen then
converts it into the form that destroys the leaching agent, and that single
route accounts for 98 per cent of the losses. The oxygen supply is therefore
both what drives the leaching and what poisons it, and there is a best level in
between.

Turning the aeration down from the level we had assumed, to roughly a sixth of
it, takes predicted gold recovery from 38 per cent to 61 per cent. It costs
nothing and needs no new equipment. We would like the wet lab to run the leach
at two oxygen levels, because it is the cheapest high value experiment we have.

The exact figure is not reliable yet. Two of the rate constants behind it come
from a different chemistry, one that contains ammonia, and ours does not. What
does survive every value we tested is that a best oxygen level exists and that
our assumed level is well above it.

## What we need from outside the modelling team

1. The gold plating thickness on the actual boards, from the supplier. This is
   one question and it moves predicted recovery by a factor of five.
2. Two rate constants measured in our own liquor, without ammonia.
3. Whether the wet lab can accept three vessels. The cost is about nine litres
   of culture for every litre of the second vessel, and probably more once
   purification losses are counted.

## One problem we created

The leaching model now hands the capture model a gold concentration higher than
the capture model can use, and every improvement to the leaching makes that
worse, because the two are the same number.

**Correction, 15 August.** We first said the fix was to stop the leach early.
A closer audit says that is not enough. The gap is a scale mismatch of about
two thousand fold, not a concentration a stopping rule can tune — it takes
about ninety four grams of dry cells per gram of board. Stopping the leach
early is still worth doing on throughput grounds, but it does not close this
gap. Either the number of binding sites per cell rises by a large factor, or
the leach output is diluted heavily, or both. `ISSUES.md` item 43.

## Since this brief, 15–16 August

We reviewed the elution step, which is where gold is stripped back off the
cells. Two things came out of it.

The rate equation we had been using was correct but unnamed, which made it look
invented. It is a standard model published in 1898 and used for sorption work
ever since. Naming it and citing it costs nothing and removes an easy line of
attack.

The more useful finding is that a second, equally standard rate law fits this
kind of system better in most of the published gold work. Both laws predict the
same final recovery — the ceiling is a property of the chemistry and neither law
changes it — but they disagree by about four times on how long the wash must
run. We have implemented both and left the original as the default, because
every number we have published used it and switching quietly would make those
numbers impossible to reproduce.

**What we would like from the wet lab.** One elution time course, six samples,
at fifteen minutes through six hours. The final sample tells us the ceiling and
therefore whether the eluent is the right one. The shape of the curve tells us
which rate law is real and therefore how long the wash needs to be. It closes
two open questions at once and is the cheapest experiment on our list.
`ISSUES.md` items 28 and 47.

## Since 16 August

Three things happened, and two of them correct numbers given earlier in this
brief. The earlier text is left as it was written, so this section is the
correction rather than a rewrite.

**The plasmid turned out to be high copy.** The wet lab confirmed a pUC type
backbone. That is fifteen times more copies per cell than we had assumed, and
it moves every number that depends on how much protein a cell can display. The
binding sites per cell go from about two thousand seven hundred to about
twenty three thousand.

**So the scale mismatch above is wrong, and it is better than we said.** This
brief says two thousand fold, and about ninety four grams of dry cells per gram
of board. The corrected figures are **about sixty fold, and about eleven grams
per gram of board**. The shape of the problem has not changed. Eleven grams of
engineered cells per gram of circuit board is still not something that stopping
the leach early can fix, and the recommendation in the section above stands.

**The elution default has changed, so the note above is out of date.** That
section says we implemented the second rate law and left the original as the
default. We switched the default to the second law on 16 August, because it
fits better on twelve of twelve published systems and both of the thiourea
papers we rely on report it. Every number we have published since that date
uses it, and the original law is still in the code for comparison. The
experiment we asked for is unchanged and still the cheapest on our list.

**One new finding worth a sentence.** The reduction step does not fail because
it is slow. It fails because it starts late: the vessel spends about thirteen
hours building the gold particles that catalyse the reaction before anything
much happens. Adding a small amount of preformed gold at the start removes that
delay, and it cuts the concentration step we need beforehand from about ten
fold to about four fold. Four fold is ordinary equipment. Ten fold is not.

**What we would like from the wet lab, added to the earlier request.** One
reduction run with and without a one percent gold seed. It measures the seed
we need and constrains the rate constant at the same time. `ISSUES.md` items
61 and 64.
