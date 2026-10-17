# CLAUDE.md

**Tier 3, synthesis.** Machine-specific notes only.

**Read [AGENTS.md](AGENTS.md) first. It is the operating manual for this
repository and it applies to you.** Rules belong there, not here, so the two
cannot drift apart.

---

## The rules that matter most

1. **Do not look in `archive/`** unless the user names a file in it. It holds
   everything the current wiki does not use. `AGENTS.md` section 0.
2. **Never edit `docs/source/`.** Log an error in `docs/ISSUES.md` and leave
   it standing in the text, even when the fix is one character.
3. **Never edit `docs/WIKI_BIORECOVERY_DRAFT.md`.** Propose wording and wait.

---

## This machine

- Windows 11. The shell is PowerShell; a Bash tool is also available. Each
  takes its own syntax. In PowerShell, `bash` starts WSL, not Git Bash; Git
  Bash is `C:\Program Files\Git\bin\bash.exe`.
- Python is on `PATH`. `jupyter` is **not** installed.
- Console output is cp1252. Non-ASCII characters in `print()` render as `?`.
  Keep code output ASCII; keep the Unicode in the Markdown documents.

---

## Before you start editing

1. Read `docs/ISSUES.md` for any item you are about to touch.
2. Read `AGENTS.md` section 4, the standing decisions. **Do not relitigate
   them.**
3. Read `AGENTS.md` section 5, the naming rules, if you are adding a symbol.

## Before you report done

Run the three checks in `AGENTS.md` section 8, then grep for the symbol you
changed. Report the real output.

## Scope

Finish the whole item. If part of it is blocked, finish everything else and
say what you left out and why. Do not spawn subagents unless asked.
