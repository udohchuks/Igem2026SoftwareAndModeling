# CLAUDE.md

**Tier 3, synthesis.** Machine-specific notes only.

**Read [AGENTS.md](AGENTS.md) first. It is the operating manual for this
repository and it applies to you.** This file adds only what is specific to
Claude Code on this machine. What each document is for, and what may be done to
it, is `AGENTS.md` section 11.

Do not duplicate guidance here. If a rule belongs to the project, it goes in
`AGENTS.md`, so the two cannot drift apart.

---

## The one rule that matters most

**Never edit a source document.** `docs/source/`, `docs/00_*`, `docs/01_*`,
`docs/02_*` and `docs/MODEL.md` are verbatim transcriptions. When you find an
error in one, record it in `docs/ISSUES.md` and **leave the error standing in
the text**. Only the document's author corrects it.

This holds even when the error is obvious, even when fixing it would take one
character, and even when a test would pass afterwards.

---

## This machine

- Windows 11. The shell is PowerShell; a Bash tool is also available. Each
  takes its own syntax.
- Python is on `PATH`. `jupyter` is **not** installed, so do not reach for
  `nbconvert --execute`. Use the notebook check in `AGENTS.md` §7, which
  executes the cells directly.
- Console output is cp1252. Non-ASCII characters in `print()` render as `?`.
  Keep code output ASCII; keep the Unicode in the Markdown documents.

---

## Before you start editing

Read, in this order:

1. `docs/ISSUES.md`, the Open table and any item you are about to touch.
2. `AGENTS.md` §4, the standing decisions. **Do not relitigate them.**
3. `AGENTS.md` §5, the naming rules, if you are adding a symbol.

---

## Before you report done

Run all four checks in `AGENTS.md` §7: tests, YAML, notebook, then grep for
the symbol you changed. Report the real output. If one fails, say which and
paste it.

---

## Scope

Finish the whole item. If part of it is blocked, finish everything else and
say plainly what you left out and why.

Do not start the deferred items, temperature and the V1 to V2 vessel transfer.
The team set them aside on 2026-08-11.

Do not spawn subagents unless asked.

---

## The biorecovery wiki draft

Added 2026-09-19.

`docs/WIKI_BIORECOVERY_DRAFT.md` is ahead of the rest of the repository.
Treat it as the current statement of the biorecovery model, and treat a
disagreement with any other file as the other file being stale.

**The conflict to expect.** The draft uses `q_Au = 4.62 µmol/g` and reports
`73.10%` capture, from `params/capture_design.yaml`. Every PNG under
`docs/media/recovery/` and `docs/media/recovery_model/` was built from
`q_max = 0.0913 µmol/g` in `params/recovery_chain.yaml`, and reports `1.54%`.

Work to these five rules:

1. Do not reuse an existing figure for this document. Generate new figures
   from `params/capture_design.yaml`.
2. Write new figures to `docs/media/biorecovery/`. Do not write into
   `docs/media/recovery/` or `docs/media/recovery_model/`, and do not
   regenerate them.
3. Add figure calls and captions to the draft. Add no prose and change no
   number in it. An error found in the draft goes to `docs/ISSUES.md`.
4. Build the document with `docs/build_biorecovery.py`, on the
   `docs/build_recovery.py` pattern: page break before each `#`, Tier 4
   banner, pandoc, and abort when a referenced figure file is absent.
5. The draft's time-dependent capture model is not in `src/` yet.
   `src/competition.py` gives equilibrium only. Add the kinetics as a module
   with a test, not as loose code inside a figure script.
