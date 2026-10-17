"""Build docs/RECOVERY.docx from docs/RECOVERY.md.

Run from the repository root:

    python docs/build_recovery.py

Adds a page break before each top-level section, then calls pandoc. It changes
no text: RECOVERY.md is hand-written and is the document. Pass --figures to
regenerate the PNGs first.

RECOVERY.md states the same numbers as docs/REVIEW.md sections 6 and 8, in
fewer words. It is not sliced from it, so when a value moves in params/*.yaml
both documents need the edit; docs/check_docs.py flags a retired value quoted
as current in either.

Requires pandoc on PATH.
"""
from pathlib import Path
import re
import subprocess
import sys

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parents[0]
def run(*cmd, cwd=None):
    print("$", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True, cwd=cwd or ROOT)


if "--figures" in sys.argv:
    run(sys.executable, DOCS / "make_recovery_figures.py")

text = (DOCS / "RECOVERY.md").read_text(encoding="utf-8")

# Nothing is silently dropped: pandoc omits a figure whose file is absent.
missing = [p for p in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
           if not (DOCS / p).exists()]
if missing:
    sys.exit("missing figures: " + ", ".join(missing) + "\n"
             "run: python docs/build_recovery.py --figures")

# Start every top-level section on a fresh page. Pandoc passes a raw openxml
# block straight through to the .docx.
PAGE_BREAK = ('```{=openxml}\n'
              '<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n'
              '```\n')
out, first = [], True
for line in text.split("\n"):
    if line.startswith("# ") and not first:
        out.append(PAGE_BREAK)
    if line.startswith("# "):
        first = False
    out.append(line)
text = "\n".join(out)

# The tier banner goes in as an HTML comment: docs/check_docs.py looks for it,
# and pandoc drops raw HTML from a .docx, so the reader never sees it.
BANNER = ("<!-- **Tier 4, generated.** Written by docs/build_recovery.py from "
          "RECOVERY.md. Do not hand-edit: every run overwrites it. -->")
end = text.index("\n---", 3) + len("\n---")
end = text.index("\n", end) + 1
text = text[:end] + "\n" + BANNER + "\n" + text[end:]

built = DOCS / "_RECOVERY_build.md"
built.write_text(text, encoding="utf-8")

run("pandoc", built.name, "-o", "RECOVERY.docx", "--resource-path=.", cwd=DOCS)
print("\nwrote docs/RECOVERY.docx")
