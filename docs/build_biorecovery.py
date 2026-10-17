"""Build docs/BIORECOVERY.docx from docs/WIKI_BIORECOVERY_DRAFT.md.

Run from the repository root:

    python docs/build_biorecovery.py

Pass --figures to regenerate the PNGs first.

The draft is the document. This script changes no wording: it converts the
draft's markdown conventions into the ones Word needs, and nothing else.

  * the indented display blocks become Word equations, using the LaTeX in
    docs/biorecovery_equations.py, keyed by the block exactly as the draft
    writes it;
  * <details> sections become ordinary third-level headings, because Word has
    no collapsible section;
  * links into other repository documents become plain text, because those
    files do not travel with the .docx;
  * the sources the draft cites are collected into a References section,
    copied from docs/SOURCES.md.

The look comes from docs/reference_biorecovery.docx, the team's bioleaching
summary, so the two documents carry the same headings, tables and fonts.
Equations and figures are centred afterwards, which pandoc cannot be told to do.

Requires pandoc on PATH.
"""
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parents[0]
sys.path.insert(0, str(DOCS))
from biorecovery_equations import EQUATIONS


def run(*cmd, cwd=None):
    print("$", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True, cwd=cwd or ROOT)


if "--figures" in sys.argv:
    run(sys.executable, DOCS / "make_biorecovery_figures.py")

text = (DOCS / "WIKI_BIORECOVERY_DRAFT.md").read_text(encoding="utf-8")

# Nothing is silently dropped: pandoc omits a figure whose file is absent.
missing = [p for p in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
           if not (DOCS / p).exists()]
if missing:
    sys.exit("missing figures: " + ", ".join(missing) + "\n"
             "run: python docs/build_biorecovery.py --figures")

# The alt text repeats the caption that follows the figure, and Word would
# print both. The caption under the image is the one the draft wrote.
text = re.sub(r"!\[[^\]]*\]\(", "![](", text)

# --- the tier banner -----------------------------------------------------
# It goes in as an HTML comment: docs/check_docs.py looks for it, and pandoc
# drops raw HTML from a .docx, so the reader never sees it. The draft's own
# Tier 3 marker is the line it replaces, so the built file cannot claim to be
# the hand-written one.
SOURCE_BANNER = ("<!-- **Tier 3, synthesis.** Repository marker; do not copy "
                 "this comment to the wiki. -->")
BANNER = ("<!-- **Tier 4, generated.** Written by docs/build_biorecovery.py "
          "from WIKI_BIORECOVERY_DRAFT.md. Do not hand-edit: every run "
          "overwrites it. -->")
if SOURCE_BANNER not in text:
    sys.exit("the draft's Tier 3 marker was not found; "
             "docs/build_biorecovery.py expects it in the opening lines")
text = text.replace(SOURCE_BANNER, BANNER, 1)

# --- collapsible sections become headings --------------------------------
text = re.sub(r"<details>\n<summary>(.+?)</summary>\n", r"### \1\n", text)
text = text.replace("\n</details>\n", "\n")

# --- display blocks become equations -------------------------------------
def equation(match):
    block = "\n".join(line[4:] for line in match.group(0).rstrip("\n").split("\n"))
    if block not in EQUATIONS:
        sys.exit("docs/biorecovery_equations.py has no entry for:\n" + block)
    latex = EQUATIONS[block]
    if latex is None:
        # Not mathematics. Carried through as its own lines, breaks kept.
        return "\n".join(line.strip() for line in block.split("\n")) + "\n"
    return "$$" + latex + "$$\n"


text = re.sub(r"(?:^ {4}\S.*\n(?:^ {4}.*\n)*)", equation, text, flags=re.M)
remaining = [b for b in EQUATIONS if b in text]
if remaining:
    sys.exit("display blocks left unconverted: %d" % len(remaining))

# --- citations -----------------------------------------------------------
# Every source the draft cites, in the order it first cites them.
cited = []
for label, target in re.findall(r"\[([^\]]+)\]\((SOURCES\.md)\)", text):
    for piece in re.findall(r"S(\d+)(?:\s*[–-]\s*S?(\d+))?", label):
        low = int(piece[0])
        high = int(piece[1]) if piece[1] else low
        for n in range(low, high + 1):
            if n not in cited:
                cited.append(n)

sources = (DOCS / "SOURCES.md").read_text(encoding="utf-8")
entries = {}
for match in re.finditer(r"^\*\*S(\d+)\.(.*?)(?=\n\n)", sources, re.S | re.M):
    entries[int(match.group(1))] = match.group(0)


def plain(entry):
    """One citation paragraph: links flattened, emphasis dropped."""
    entry = re.sub(r"\[([^\]]+)\]\(([^)]+)\)",
                   lambda m: m.group(1) if m.group(2).endswith(".pdf")
                   else "%s: %s" % (m.group(1), m.group(2)), entry)
    entry = entry.replace("**", "").replace("*", "")
    return " ".join(entry.split())


references = ["", "## References", ""]
for n in cited:
    if n not in entries:
        sys.exit("docs/SOURCES.md has no entry for S%d" % n)
    references.append(plain(entries[n]))
    references.append("")
text = text.rstrip("\n") + "\n" + "\n".join(references)

# A citation keeps its brackets and loses its link, the way the team's
# bioleaching summary writes them. Every other link into a repository document
# becomes plain text, because those files do not travel with the .docx.
text = re.sub(r"\[([^\]]+)\]\(SOURCES\.md\)", r"\\[\1\\]", text)
text = re.sub(r"\[([^\]]+)\]\((?!http)[^)]*\.md(?:#[^)]*)?\)", r"\1", text)

built = DOCS / "_BIORECOVERY_build.md"
built.write_text(text, encoding="utf-8")

run("pandoc", built.name, "-o", "BIORECOVERY.docx", "--resource-path=.",
    "--reference-doc=reference_biorecovery.docx", cwd=DOCS)

# --- centre the equations and the figures --------------------------------
# Pandoc has no option for this, and the team's bioleaching summary centres
# both, so it is done on the finished package.
CENTRE = '<w:jc w:val="center"/>'
docx = DOCS / "BIORECOVERY.docx"
with zipfile.ZipFile(docx) as z:
    items = {name: z.read(name) for name in z.namelist()}
document = items["word/document.xml"].decode("utf-8")


def centre(match):
    para = match.group(0)
    if "<m:oMath" not in para and "<w:drawing>" not in para:
        return para
    if CENTRE in para:
        return para
    if "<w:pPr>" in para:
        return para.replace("<w:pPr>", "<w:pPr>" + CENTRE, 1)
    return para.replace(">", "><w:pPr>" + CENTRE + "</w:pPr>", 1)


document, centred = re.subn(r"<w:p\b[^>]*>.*?</w:p>", centre, document,
                            flags=re.S)

# Pandoc invents its own table style. The reference document already has one,
# and using it is what makes these tables look like the bioleaching summary's.
document = re.sub(r'<w:tblStyle w:val="Table"\s*/>',
                  '<w:tblStyle w:val="TableGrid"/>', document)
items["word/document.xml"] = document.encode("utf-8")
with zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED) as z:
    for name, data in items.items():
        z.writestr(name, data)

print("\nwrote docs/BIORECOVERY.docx")
print("   %d sources cited, %d display blocks converted"
      % (len(cited), len(EQUATIONS)))
