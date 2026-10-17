---
title: "Source-document issues by wiki stage"
date: "2026-09-10"
---

# Source-document issues

**Tier 3, synthesis.** This lists only problems within the supplied model
document. An unambiguous value or stated assumption is not an issue merely
because another repository route differs. Full evidence is in
[ISSUES.md](ISSUES.md).

## Making the leachant

| Document issue | What is needed |
|---|---|
| Two active-TetH yields give different culture volumes. [Item 58](ISSUES.md#58-v5s-stage-1-enzyme-yield-contradicts-v5s-own-derivation) | Measure active TetH recovered per litre of culture. |
| An active fraction of 0.5 is assumed, but the cited TetH requires acid refolding. [Item 32](ISSUES.md#32--blocking--teth-cannot-fold-into-an-active-form-in-ecoli-at-neutral-ph) | Define the refolding procedure and measure activity after refolding. |
| Extraction and purification are treated as 100% efficient. [Item 40](ISSUES.md#40-nothing-accounts-for-purification-losses-or-enzyme-decay-in-the-vessel) | Measure recovery yield and retained activity. |
| The reasoning gives 2.2 U mg^-1, while the calculation uses 2.5 U mg^-1. [Item 57](ISSUES.md#57-v5s-k_cat-reasoning-says-22-umg-and-its-arithmetic-uses-25) | Confirm the intended specific activity. |
| The sulfur check counts molecules rather than sulfur atoms. [Item 56](ISSUES.md#56-v5s-sulfur-conservation-check-counts-molecules-not-sulfur-atoms) | Track elemental sulfur and sulfate in the balance. |
| Enzyme decay and sulfur-species degradation are excluded. [Items 38 and 40](ISSUES.md#38-stage-2-needs-ph-3-for-the-enzyme-and-thiosulfate-is-unstable-there) | Measure TetH lifetime and thiosulfate loss under Stage 2 conditions. |
| Stage 2 assumes optimal conditions but gives no pH, temperature or agitation inputs. | Define the operating window and measure TetH activity across it. |
| The transfer to PCB leaching has no conditioning or transfer-recovery parameters. | Define outgoing pH and temperature, adjustment requirements and transfer yield. |

## Dissolving the gold

| Document issue | What is needed |
|---|---|
| The Model B product balance writes `AuO3^3-` instead of the gold-thiosulfate complex. [Item 7](ISSUES.md#7-part-i-4-model-b-labels-the-dissolved-gold-product-two-different-ways) | Correct the species label to `Au(S2O3)2^3-`. |
| Passivation is named as a rate factor, but no passivation term appears in the equation. [Item 45](ISSUES.md#45-part-i-names-passivation-in-its-prose-and-has-no-passivation-term) | Add a measured passivation term or state that it is excluded. |
| The pump-limited oxygen balance charges `v4/4`, while the copper balances define `v4` as one complete oxygen reaction. | Use `v4` in the oxygen balance and recompute the pump-limited result. |
| Operating conditions are called optimised, but pH, temperature and agitation are not specified. | State the selected operating conditions. |
| The ammonia explanation says it prevents “thiosulfate leaching”; the intended effect is slower thiosulfate depletion. | Correct the wording. |
