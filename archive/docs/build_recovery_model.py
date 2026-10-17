"""Build the technical recovery report with live parameter and result tables.

Use --figures to regenerate all accompanying plots. Generated files must not
be hand-edited. Scientific values come from the shared parameter loader.
"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT))
from src import params, recovery_audit, recovery_process

if "--figures" in sys.argv:
    subprocess.run([sys.executable, str(DOCS / "make_recovery_model_figures.py")],
                   cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(DOCS / "make_capture_design_figures.py")],
                   cwd=ROOT, check=True)
p = recovery_audit.operating_parameters()
r = params.load("recovery_chain")
base = recovery_process.run()
slow = recovery_process.run(nucleation_rate_per_h=r["reduction"]["k_nuc"]["range"][0],
                            growth_rate_per_uM_h=r["reduction"]["k_grow"]["range"][0])
rows = [("Feed gold", "feed_gold_amount_umol"),
        ("Captured gold", "bound_gold_amount_umol"),
        ("Eluted gold", "eluted_gold_amount_umol"),
        ("New metal after the reduction batch", "new_metal_amount_umol")]
results = "| Quantity | Reference | Slow kinetic scenario |\n|---|---:|---:|\n"
for label, key in rows:
    results += f"| {label} | {base[key]:.6g} µmol | {slow[key]:.6g} µmol |\n"
results += f"| New metal / original feed | {base['metal_fraction_of_feed']:.6%} | {slow['metal_fraction_of_feed']:.6%} |\n"

specs = [
    ("Feed gold concentration", "Au_feed", "µmol/L", "Reporting scenario; recovery_audit.yaml"),
    ("Single-occupancy binding capacity", "q_max", "µmol/g", "Derived expression joint; ISSUES 62"),
    ("Reference biomass concentration", "X_max", "g/L", "Operating assumption"),
    ("Gold dissociation constant", "K_Au", "µmol/L", "GolB-based literature proxy; S78, ISSUES 1"),
    ("Nonelutable fraction", "phi", "fraction", "Transferred assumption; ISSUES 28"),
    ("First-order elution rate", "k_elute", "h⁻¹", "Acid-thiourea lower-bound proxy; S60"),
    ("Elution time", "t_elute_h", "h", "Reporting time"),
    ("Effective nucleation rate", "k_nuc", "h⁻¹", "Cross-system proxy; S74, ISSUES 84"),
    ("Effective autocatalytic growth rate", "k_grow", "L µmol⁻¹ h⁻¹", "Cross-system proxy; ISSUES 84"),
    ("Protein oxidation rate", "k_ox", "h⁻¹", "Unmeasured assumption"),
    ("Protein recharge rate", "k_rech", "L µmol⁻¹ h⁻¹", "Unmeasured assumption"),
    ("Gold inhibition constant", "K_inh", "µmol/L", "Unmeasured assumption"),
    ("Initial recharge donor", "Rech_0", "µmol/L", "Design choice; S35 gives reagent identity"),
    ("Final redox-protein concentration", "E_tot", "µmol/L", "Target dose, not measured supply"),
    ("Protein equivalents per gold", "nu", "mol/mol", "Proposed two-electron mechanism; S63"),
    ("Donor per protein recharge", "nu_rech", "mol/mol", "Assumed coupling; ISSUES 90"),
    ("Reduction duration", "t_reduce_h", "h", "Design choice")]
table = "| Clear name (existing symbol) | Reference value | Evidence |\n|---|---:|---|\n"
for label, key, unit, evidence in specs:
    table += f"| {label} (`{key}`) | {p[key]:.6g} {unit} | {evidence} |\n"
for key, label, unit in (("k_nuc", "Nucleation scenario range", "h⁻¹"),
                         ("k_grow", "Growth scenario range", "L µmol⁻¹ h⁻¹")):
    low, high = r["reduction"][key]["range"]
    table += f"| {label} | {low:g}–{high:g} {unit} | Declared scenarios; not a confidence interval |\n"
text = (DOCS / "RECOVERY_MODEL.md").read_text(encoding="utf-8")
text = text.replace("{{RESULTS_TABLE}}", results).replace("{{PARAMETER_TABLE}}", table)
text = text.replace("**Tier 3, synthesis.**", "**Tier 4, generated.** Do not hand-edit. Built by build_recovery_model.py.")
missing = [x for x in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", text)
           if not (DOCS / x).exists()]
if missing:
    raise FileNotFoundError("Missing figures; run with --figures: " + str(missing))
built = DOCS / "_RECOVERY_MODEL_build.md"
built.write_text(text, encoding="utf-8")
subprocess.run(["pandoc", built.name, "-o", "RECOVERY_MODEL.docx", "--resource-path=."],
               cwd=DOCS, check=True)
# Formatting only, using the standard library so the report builder shares
# the model's environment without requiring a second document dependency.
from zipfile import ZipFile, ZIP_DEFLATED
path = DOCS / "RECOVERY_MODEL.docx"
with ZipFile(path) as archive:
    contents = {name: archive.read(name) for name in archive.namelist()}
styles = contents["word/styles.xml"].decode("utf-8")
normal = re.search(r'<w:style\b[^>]*w:styleId="Normal"[^>]*>.*?</w:style>', styles, re.S)
if normal:
    block = normal.group()
    block = re.sub(r'<w:rPr>.*?</w:rPr>', '', block, flags=re.S)
    block = block.replace('</w:style>', '<w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>'
                          '<w:sz w:val="21"/></w:rPr></w:style>')
    styles = styles[:normal.start()] + block + styles[normal.end():]
contents["word/styles.xml"] = styles.encode("utf-8")
with ZipFile(path, "w", ZIP_DEFLATED) as archive:
    for name, content in contents.items():
        archive.writestr(name, content)
print("Wrote docs/RECOVERY_MODEL.docx and live numerical tables")
