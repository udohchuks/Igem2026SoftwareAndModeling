"""Enforce the documentation standard in AGENTS.md section 11.

Run from the repository root:

    python docs/check_docs.py

Four checks. The first three fail the run; the fourth is advisory.

1. Every markdown link that points at a path resolves.
2. Every Tier 3 and Tier 4 file declares its tier in its opening lines.
3. No Tier 4 file has been hand-edited since it was last generated, judged by
   whether regenerating changes it.
4. No Tier 3 file quotes a retired parameter value as though it were current.

Check 3 is skipped unless --regen is passed, because it runs pandoc.
Check 4 is the one that would have caught ISSUES.md item 62.

Tier 1 files are deliberately exempt from check 2. They may not be edited at
all, so they cannot carry a marker; their tier is declared in STRUCTURE.md and
in AGENTS.md section 11 instead.

archive/ is not checked. A link from a live file to a file that moved there on
2026-10-16 still resolves, because archive/ keeps each file's old path. The
record files, ISSUES.md above all, cite those files and may not be rewritten.
"""
import io
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# --- the tiers, from AGENTS.md section 11 ---------------------------------
# Tier 1 is docs/source/, which SKIP_DIRS already excludes.
TIER1 = set()
TIER2 = {"docs/ISSUES.md", "docs/SOURCES.md"}
TIER3 = {
    "README.md", "STRUCTURE.md", "AGENTS.md", "CLAUDE.md",
    "docs/EQUATIONS.md", "docs/WIKI_MODEL_UPDATE.md",
    "docs/WIKI_BIORECOVERY_DRAFT.md", "docs/CAPTURE_DESIGN.md",
    "docs/WIKI_EQUATIONS.md",
}
TIER4 = {"docs/_BIORECOVERY_build.md"}

SKIP_DIRS = (".git", "__pycache__", ".pytest_cache", ".claude", "docs/source",
             "archive")
ARCHIVE = ROOT / "archive"

# A markdown link inside a fenced code block is not a link. Chemical formulae
# such as [Cu(S2O3)2](3-) look exactly like one, which is why fences are
# stripped before the link check rather than special-cased afterwards.
FENCE = re.compile(r"```.*?```", re.S)
LINK = re.compile(r"\[([^\]]{1,80})\]\(([^)\s]+)\)")
# Bold in prose, or first thing in an opening HTML comment. WIKI_MODEL_UPDATE.md
# uses the comment form and is supplied content, so the check bends, not it.
TIER_LINE = re.compile(r"(?:\*\*|<!--\s*)Tier ([1-4])[ ,.]", re.I)


def markdown_files():
    out = []
    for d, _, fs in os.walk(ROOT):
        rel = str(Path(d).relative_to(ROOT)).replace(os.sep, "/")
        if any(x in rel for x in SKIP_DIRS):
            continue
        for f in fs:
            if f.endswith(".md"):
                p = (Path(d) / f).relative_to(ROOT)
                out.append(str(p).replace(os.sep, "/"))
    return sorted(out)


def ascii_only(text):
    """The console here is cp1252; non-ASCII prints as a crash, not a glyph."""
    return text.encode("ascii", "replace").decode("ascii")


def check_links(files):
    bad = []
    for f in files:
        text = io.open(ROOT / f, encoding="utf-8", errors="replace").read()
        body = FENCE.sub("", text)
        base = (ROOT / f).parent
        for m in LINK.finditer(body):
            target = m.group(2)
            if target.startswith(("http", "mailto", "#")):
                continue
            path = (base / target.split("#")[0]).resolve()
            if path.exists():
                continue
            try:
                archived = ARCHIVE / path.relative_to(ROOT.resolve())
            except ValueError:
                archived = None
            if archived is None or not archived.exists():
                bad.append((f, m.group(1)[:40], target))
    return bad


def check_tiers(files):
    bad = []
    for f in files:
        if f in TIER1:
            continue
        expected = (3 if f in TIER3 else 4 if f in TIER4
                    else 2 if f in TIER2 else None)
        if expected is None:
            bad.append((f, "not listed in any tier in check_docs.py"))
            continue
        head = io.open(ROOT / f, encoding="utf-8",
                       errors="replace").read(2000)
        m = TIER_LINE.search(head)
        if not m:
            bad.append((f, "no tier declared in the first 2000 characters"))
        elif int(m.group(1)) != expected:
            bad.append((f, "declares tier %s, expected %d"
                        % (m.group(1), expected)))
    return bad


# --- check 4 -------------------------------------------------------------
# Words that mark a number as deliberately historical. A retired value on a
# line carrying one of these is a record, not a stale claim.
HISTORICAL = (
    # stems, not whole words: "supersed" catches superseded and superseding,
    # "retire" catches retired and retiring, "chang" catches changed and
    # changes. Whole words missed three real decision-log rows on the first
    # run of this check.
    "supersed", "retire", "was ", "were ", "before", "until", "historical",
    "previously", "no longer", "used to", "item ", "issues", "old ", "earlier",
    "~~", "moved", "chang", "prior", "n = 20",
    # every decision-log row is dated, and a dated row is by definition a
    # record of what a value used to be.
    "2026-08-",
)


def retired_values():
    """Every superseded numeric value in params/, with its current value."""
    import yaml

    def walk(node, path=()):
        out = []
        if isinstance(node, dict):
            cur = node.get("value", None)
            for k, v in node.items():
                if not isinstance(v, dict):
                    continue
                if "superseded" in k or "retired" in k:
                    rv = v.get("value", None)
                    # A value retired from something already retired is two
                    # decisions back. Searching for it only produces noise:
                    # K_S2O3's grandparent 50000 matched the anchor ceiling
                    # in five unrelated places.
                    nested = sum(1 for p in path
                                 if "superseded" in p or "retired" in p)
                    if (isinstance(rv, (int, float))
                            and not isinstance(rv, bool) and nested == 0):
                        out.append((".".join(path + (k,)), rv, cur))
                out += walk(v, path + (k,))
        return out

    found = []
    for f in ("leach", "expression", "recovery_chain", "conversions"):
        d = yaml.safe_load(io.open(ROOT / "params" / (f + ".yaml"),
                                   encoding="utf-8"))
        found += walk(d)
    return found


def literals(value):
    """How a number like 0.0108 might plausibly be written in prose."""
    out = set()
    if isinstance(value, float) and value == int(value) and abs(value) < 1e6:
        value = int(value)
    text = repr(value)
    if len(text) >= 4 and not text.startswith("0.0000"):
        out.add(text)
    if isinstance(value, int) and 1000 <= abs(value) < 10 ** 9:
        out.add("{:,}".format(value))
    return out


def check_stale(files):
    """Retired parameter values quoted in a Tier 3 file without a marker.

    This is the check that would have caught ISSUES.md item 62: q_max moved
    and four documents went on quoting the old value as current. It is
    ADVISORY. A retired number can legitimately appear in a sentence this
    cannot parse, so it reports rather than fails.
    """
    hits = []
    targets = [f for f in files if f in TIER3]
    for name, rv, cur in retired_values():
        if rv == cur:
            continue
        for lit in literals(rv):
            # Bounded, so that 3,900 does not match inside 63,900 : 1.
            pattern = re.compile(r"(?<![\d.,])" + re.escape(lit)
                                 + r"(?![\d,]*\d)")
            for f in targets:
                for n, line in enumerate(
                        io.open(ROOT / f, encoding="utf-8",
                                errors="replace"), 1):
                    if not pattern.search(line):
                        continue
                    low = line.lower()
                    if any(w in low for w in HISTORICAL):
                        continue
                    hits.append((f, n, lit, name, cur))
    return hits


def main():
    files = markdown_files()
    failures = 0

    bad = check_links(files)
    print("1. links")
    # A Tier 1 file may not be edited, so a bad link inside one is reported
    # and never counted as a failure. Both current cases are chemical formulae
    # outside a code fence, which markdown reads as a link and we cannot fix.
    fixable = [b for b in bad if b[0] not in TIER1]
    for f, label, target in bad:
        tag = "BROKEN " if f not in TIER1 else "tier 1,"
        print("   %s %-28s [%s] -> %s"
              % (tag, f, ascii_only(label), ascii_only(target)))
    print("   %d broken and fixable, %d in Tier 1 and left alone, "
          "across %d files" % (len(fixable), len(bad) - len(fixable),
                               len(files)))
    failures += len(fixable)

    print("2. tier declarations")
    bad = check_tiers(files)
    for f, why in bad:
        print("   %-30s %s" % (f, why))
    print("   %d missing or wrong" % len(bad))
    failures += len(bad)

    print("3. generated files match their generator")
    if "--regen" not in sys.argv:
        print("   skipped; pass --regen to run docs/build_biorecovery.py first")
    else:
        before = {f: (ROOT / f).read_bytes() for f in TIER4
                  if (ROOT / f).exists()}
        if not before:
            print("   no Tier 4 files on disk to compare")
            failures += 1
        # subprocess, not os.system: a quoted Windows path with a space in it
        # fails silently under os.system and the check then reports a false
        # pass. It did exactly that the first time this ran.
        builders = ("build_biorecovery.py",)
        runs = [subprocess.run([sys.executable, str(ROOT / "docs" / name)],
                               cwd=ROOT, capture_output=True, text=True)
                for name in builders]
        broken = [(name, r) for name, r in zip(builders, runs)
                  if r.returncode != 0]
        for name, r in broken:
            print("   %s failed, exit %d" % (name, r.returncode))
            print("   " + ascii_only(r.stderr.strip()[-400:]))
        failures += len(broken)
        if not broken:
            drift = [f for f, b in before.items()
                     if (ROOT / f).read_bytes() != b]
            for f in drift:
                print("   HAND-EDITED  %s changed when regenerated" % f)
            print("   %d of %d Tier 4 files drifted"
                  % (len(drift), len(before)))
            failures += len(drift)

    print("4. retired parameter values quoted as current (advisory)")
    hits = check_stale(files)
    for f, n, lit, name, cur in hits:
        print("   %s:%d quotes %s; %s is now %s"
              % (f, n, lit, name.split(".superseded")[0], cur))
    print("   %d to look at" % len(hits))

    print()
    print("FAIL: %d problems" % failures if failures else "ok")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
