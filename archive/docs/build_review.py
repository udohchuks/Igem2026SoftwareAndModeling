"""Build docs/REVIEW.docx from docs/REVIEW.md.

Run from the repository root:

    python docs/build_review.py

Regenerates the figures, regenerates the parameter appendix, splices the
appendix into the document, and calls pandoc. Requires pandoc on PATH.
"""
from pathlib import Path
import subprocess
import sys

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parents[0]
PLACEHOLDER = "!INCLUDE_PARAMETERS!"
TOC_PLACEHOLDER = "!INCLUDE_TOC!"


def build_toc(markdown):
    """A literal contents list, built from the headings themselves.

    pandoc's --toc emits a Word FIELD, which renders as an empty box until the
    reader refreshes it, and most readers never do. This writes the contents
    out as ordinary text instead, so it is correct the moment the file opens
    and correct in the .md as well.
    """
    lines, out = markdown.split(chr(10)), ["## Contents", ""]
    fence = False
    for ln in lines:
        if ln.startswith("```"):
            fence = not fence
        if fence or not ln.startswith("#"):
            continue
        level = len(ln) - len(ln.lstrip("#"))
        if level > 2:
            continue
        title = ln.lstrip("#").strip()
        if title.startswith("Contents") or "!INCLUDE" in title:
            continue
        out.append(("- " if level == 1 else "    - ") + title)
    out.append("")
    return chr(10).join(out)


def run(*cmd, cwd=None):
    print("$", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True, cwd=cwd or ROOT)


run(sys.executable, DOCS / "make_review_figures.py")
run(sys.executable, DOCS / "make_review_tables.py")

review = (DOCS / "REVIEW.md").read_text(encoding="utf-8")
appendix = (DOCS / "_review_parameters.md").read_text(encoding="utf-8")
if PLACEHOLDER not in review:
    sys.exit(f"{PLACEHOLDER} not found in REVIEW.md")

text = review.replace(PLACEHOLDER, appendix)
if TOC_PLACEHOLDER not in text:
    sys.exit(f"{TOC_PLACEHOLDER} not found in REVIEW.md")
# built from the spliced text, so Appendix A's headings are included
text = text.replace(TOC_PLACEHOLDER, build_toc(text))

# Start every top-level section on a fresh page. Pandoc passes a raw openxml
# block straight through to the .docx.
PAGE_BREAK = ('```{=openxml}\n'
              '<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n'
              '```\n\n')
out, first = [], True
for line in text.split("\n"):
    if line.startswith("# ") and not first:
        out.append(PAGE_BREAK.rstrip("\n"))
    if line.startswith("# "):
        first = False
    out.append(line)
text = "\n".join(out)

# The tier banner goes in as an HTML comment, after the YAML frontmatter so
# pandoc still reads the metadata, and invisible in the .docx. docs/check_docs.py
# looks for it; a reader of the .docx never sees it. AGENTS.md section 11.
BANNER = ("<!-- **Tier 4, generated.** Written by docs/build_review.py from "
          "REVIEW.md plus _review_parameters.md. Do not hand-edit: every run "
          "overwrites it. -->")
if text.startswith("---"):
    end = text.index(chr(10) + "---", 3) + len(chr(10) + "---")
    end = text.index(chr(10), end) + 1
    text = text[:end] + chr(10) + BANNER + chr(10) + text[end:]
else:
    text = BANNER + chr(10) * 2 + text

built = DOCS / "_REVIEW_build.md"
built.write_text(text, encoding="utf-8")

# No --toc: the contents are spliced in above as real text, because a Word
# TOC field shows an empty box until the reader refreshes it.
run("pandoc", built.name, "-o", "REVIEW.docx", "--resource-path=.", cwd=DOCS)

print("\nwrote docs/REVIEW.docx")
