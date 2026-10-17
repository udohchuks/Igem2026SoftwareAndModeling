---
name: igem-2026-software-direction
description: The iGEM 2026 software idea is a world-model virtual cell for E. coli with trainable meta-queries, not wet lab tooling and not a simulator wrapper.
metadata:
  type: project
---

As of 2026-09-18, the software-track idea is a **world model of an E. coli
cell** driven by trainable query tokens. The user's two reference papers:

- **arXiv 2606.05979v1**, "World-Language-Action Model for Unified World
  Modeling, Language Reasoning, and Action Synthesis" (Yang, Liu, Kou et al.).
  AR Transformer backbone, 64 learnable **meta-queries** appended to context,
  a diffusion World Expert (SANA-600M) and a flow-matching Action Expert
  (390M). Loss `L_act + 0.1*L_wm + 0.005*L_lang`. The World Expert is
  discardable at inference because the meta-queries pass its influence through
  shared parameters (116 ms to 40 ms).
- **GenBio AI, "A World Model of the Virtual Cell"**, Eric Xing and Le Song,
  3 May 2026. A position paper, no experiments. Defines the virtual cell as
  `p(x'|x,a,e)` with encoder E onto a cellular manifold M, action-conditioned
  transition core F, and cross-modal decoder D. Calls for a "Virtual Cell
  Arena" benchmark that does not yet exist.

**Why:** The user rejected two framings explicitly. Wet lab tooling is
saturated. A chat interface over an existing solver is a wrapper and is not
what they want. "Meta query" means trainable query tokens, not a query
language.

**How to apply:** Pitch at the level of action-conditioned generative
dynamics: manifold, transition operator, decoder, action synthesis. The
existing gold-biorecovery repo model is a candidate verifier and trajectory
generator, never the product.
