"""
Provider-specific test name mappings for LabRecon scrapers.

Keys are internal test IDs from tests_catalog.py.
Values are dicts keyed by provider ID ("quest", "labcorp", "goodlabs").

Use exact string matching against the live page name when scraping.
Set to None when:
  - the provider doesn't offer the test as a standalone product
  - the name hasn't been verified against the live site yet

Quest names verified 2026-03-12 against questhealth.com/shop-tests (165 cards).
LabCorp names verified 2026-03-12 against ondemand.labcorp.com/products (119 cards).
GoodLabs names verified 2026-03-12 against app.hellogoodlabs.com/book-tests.
"""

PROVIDER_NAMES: dict[str, dict[str, str | None]] = {

    # ── Original 19 tests ────────────────────────────────────────────

    "cbc": {
        "quest":    "Complete Blood Count (CBC) Test",
        "labcorp":  "Complete Blood Count (CBC) Test",
        "goodlabs": "Complete Blood Count (CBC) with Differential/Platelet",
    },
    "cmp": {
        "quest":    "Comprehensive Metabolic Panel (CMP) Test",
        "labcorp":  "Comprehensive Metabolic Panel (CMP)",
        "goodlabs": "Comprehensive Metabolic Panel (CMP)",
    },
    "lipid": {
        "quest":    "Cholesterol (Lipid) Panel",
        "labcorp":  "Cholesterol and Lipid Panel Test",
        "goodlabs": "Lipid Panel",
    },
    "a1c": {
        "quest":    "Hemoglobin A1c Test",
        "labcorp":  "Diabetes Risk (HbA1c) Test",
        "goodlabs": "Hemoglobin A1c (HbA1c)",
    },
    "crp": {
        "quest":    "hsCRP Test for Inflammation Marker",
        "labcorp":  "Inflammation (hs-CRP) Test",
        "goodlabs": "High-Sensitivity C-Reactive Protein (hs-CRP)",
    },
    "insulin": {
        # Quest: only bundles — "Insulin Resistance Test Panel" ($84.15)
        # LabCorp: "Insulin Resistance Test" ($89) is likely a bundle
        # GoodLabs: standalone available
        "quest":    None,
        "labcorp":  None,
        "goodlabs": "Insulin",
    },
    "lpa": {
        "quest":    "Lipoprotein(a)/Lp(a) Test",
        "labcorp":  "Lipoprotein(a) Test",
        "goodlabs": "Lp(a)",
    },
    "apob": {
        # Quest: only "Advanced Heart Health Test Panel (with ApoB)" ($172) — bundle
        "quest":    None,
        "labcorp":  "Apolipoprotein B (ApoB) Test",
        "goodlabs": "Apolipoprotein B",
    },
    "tsh": {
        "quest":    "Thyroid TSH Function Test",
        "labcorp":  "Thyroid Stimulating Hormone (TSH) Test",
        "goodlabs": "Thyroid Stimulating Hormone (TSH)",
    },
    "ft4": {
        # Quest: no standalone; LabCorp: no standalone
        # GoodLabs: standalone available
        "quest":    None,
        "labcorp":  None,
        "goodlabs": "Thyroxine, Free (Free T4)",
    },
    "vitd": {
        "quest":    "Vitamin D Test",
        "labcorp":  "Vitamin D Test",
        "goodlabs": "Vitamin D, 25-Hydroxy",
    },
    "b12": {
        "quest":    "Vitamin B12 Test",
        "labcorp":  "Vitamin B12 Test",
        "goodlabs": "Vitamin B12 (Cobalamin)",
    },
    "ferritin": {
        # Quest: no standalone — bundled into "Iron, TIBC & Ferritin Panel"
        "quest":    None,
        "labcorp":  "Ferritin Test",
        "goodlabs": "Ferritin",
    },
    "iron": {
        # Quest: bundles iron + TIBC + ferritin — flag in output
        # LabCorp: no standalone — closest is "Anemia Test" ($189) bundle
        "quest":    "Iron, TIBC & Ferritin Panel",
        "labcorp":  None,
        "goodlabs": "Iron, TIBC and Ferritin Panel",
    },
    "total-test": {
        "quest":    "Testosterone Test",
        "labcorp":  "Total Testosterone Test",
        "goodlabs": "Testosterone, Total, MS",
    },
    "free-test": {
        # Quest: no standalone; LabCorp: "Comprehensive Testosterone Test" ($159) is a bundle
        "quest":    None,
        "labcorp":  None,
        "goodlabs": "Testosterone, Free and Total, MS",
    },
    "estradiol": {
        # Quest: not visible as standalone
        "quest":    None,
        "labcorp":  "Estradiol (E2) Test",
        "goodlabs": "Estradiol",
    },
    "shbg": {
        # Quest: not found; LabCorp: not found
        "quest":    None,
        "labcorp":  None,
        "goodlabs": "Sex Hormone Binding Globulin (SHBG)",
    },
    "psa": {
        "quest":    "Prostate Screening (PSA)",
        "labcorp":  "PSA Prostate Cancer Screening Test",
        "goodlabs": "PSA Total (Reflex To Free)",
    },

    # ── GoodLabs individual tests — Quest/LabCorp pending scraper runs ─

    "acth":             {"quest": None, "labcorp": None, "goodlabs": "ACTH, Plasma"},
    "aluminum":         {"quest": None, "labcorp": None, "goodlabs": "Aluminum, Blood"},
    "amylase":          {"quest": None, "labcorp": None, "goodlabs": "Amylase"},
    "ana":              {"quest": None, "labcorp": None, "goodlabs": "ANA Screen, IFA, with Reflex to Titer and Pattern"},
    "androstenedione":  {"quest": None, "labcorp": None, "goodlabs": "Androstenedione"},
    "amh":              {"quest": None, "labcorp": None, "goodlabs": "Anti-Mullerian Hormone (AMH)"},
    "arsenic":          {"quest": None, "labcorp": None, "goodlabs": "Arsenic, Blood"},
    "c-peptide":        {"quest": None, "labcorp": None, "goodlabs": "C-Peptide"},
    "ceruloplasmin":    {"quest": None, "labcorp": None, "goodlabs": "Ceruloplasmin"},
    "coq10":            {"quest": None, "labcorp": None, "goodlabs": "Coenzyme Q10, Total"},
    "copper":           {"quest": None, "labcorp": None, "goodlabs": "Copper, Serum or Plasma"},
    "cortisol":         {"quest": None, "labcorp": None, "goodlabs": "Cortisol"},
    "cortisol-lcms":    {"quest": None, "labcorp": None, "goodlabs": "Cortisol, Total, LC/MS"},
    "ck":               {"quest": None, "labcorp": None, "goodlabs": "Creatine Kinase (CK), Total"},
    "crp-standard":     {"quest": None, "labcorp": None, "goodlabs": "CRP"},
    "cystatin-c":       {"quest": None, "labcorp": None, "goodlabs": "Cystatin C"},
    "dhea-s":           {"quest": None, "labcorp": None, "goodlabs": "DHEA-Sulfate"},
    "dht":              {"quest": None, "labcorp": None, "goodlabs": "Dihydrotestosterone (DHT)"},
    "estradiol-lcms":   {"quest": None, "labcorp": None, "goodlabs": "Estradiol, Sensitive, LC/MS"},
    "estrogens-total":  {"quest": None, "labcorp": None, "goodlabs": "Estrogens, Total, Immunoassay"},
    "estrone":          {"quest": None, "labcorp": None, "goodlabs": "Estrone"},
    "fibrinogen":       {"quest": None, "labcorp": None, "goodlabs": "Fibrinogen"},
    "folate-rbc":       {"quest": None, "labcorp": None, "goodlabs": "Folate, RBC"},
    "folate-serum":     {"quest": None, "labcorp": None, "goodlabs": "Folate, Serum"},
    "fructosamine":     {"quest": None, "labcorp": None, "goodlabs": "Fructosamine"},
    "fsh":              {"quest": None, "labcorp": None, "goodlabs": "FSH"},
    "gastrin":          {"quest": None, "labcorp": None, "goodlabs": "Gastrin"},
    "ggt":              {"quest": None, "labcorp": None, "goodlabs": "GGT"},
    "glucose":          {"quest": None, "labcorp": None, "goodlabs": "Glucose"},
    "gh":               {"quest": None, "labcorp": None, "goodlabs": "Growth Hormone (GH)"},
    "hemoglobin":       {"quest": None, "labcorp": None, "goodlabs": "Hemoglobin (Hb)"},
    "hep-c":            {"quest": None, "labcorp": None, "goodlabs": "Hepatitis C Antibody"},
    "homocysteine":     {"quest": None, "labcorp": None, "goodlabs": "Homocysteine"},
    "iga":              {"quest": None, "labcorp": None, "goodlabs": "Immunoglobulin A (IgA) - Serum"},
    "inhibin-b":        {"quest": None, "labcorp": None, "goodlabs": "Inhibin B"},
    "igf1":             {"quest": None, "labcorp": None, "goodlabs": "Insulin-Like Growth Factor I (IGF-1) LC/MS"},
    "il1b":             {"quest": None, "labcorp": None, "goodlabs": "Interleukin-1 Beta (IL-1\u03b2)"},
    "il6":              {"quest": None, "labcorp": None, "goodlabs": "Interleukin-6 (IL-6)"},
    "iodine-urine":     {"quest": None, "labcorp": None, "goodlabs": "Iodine, Random Urine"},
    "iodine-serum":     {"quest": None, "labcorp": None, "goodlabs": "Iodine, Serum/Plasma"},
    "ldl-direct":       {"quest": None, "labcorp": None, "goodlabs": "LDL Cholesterol (Direct)"},
    "lead":             {"quest": None, "labcorp": None, "goodlabs": "Lead (Venous)"},
    "leptin":           {"quest": None, "labcorp": None, "goodlabs": "Leptin"},
    "lh":               {"quest": None, "labcorp": None, "goodlabs": "LH"},
    "lipase":           {"quest": None, "labcorp": None, "goodlabs": "Lipase"},
    "lp-pla2":          {"quest": None, "labcorp": None, "goodlabs": "Lp-PLA2 Activity"},
    "magnesium-rbc":    {"quest": None, "labcorp": None, "goodlabs": "Magnesium, RBC"},
    "mercury":          {"quest": None, "labcorp": None, "goodlabs": "Mercury, Blood"},
    "methylmalonic":    {"quest": None, "labcorp": None, "goodlabs": "Methylmalonic Acid"},
    "methylmalonic-s":  {"quest": None, "labcorp": None, "goodlabs": "Methylmalonic Acid, Serum"},
    "molybdenum":       {"quest": None, "labcorp": None, "goodlabs": "Molybdenum, Serum or Plasma"},
    "mthfr":            {"quest": None, "labcorp": None, "goodlabs": "MTHFR Genetic Test"},
    "nt-probnp":        {"quest": None, "labcorp": None, "goodlabs": "NT-proBNP"},
    "oxldl":            {"quest": None, "labcorp": None, "goodlabs": "OxLDL"},
    "pregnenolone":     {"quest": None, "labcorp": None, "goodlabs": "Pregnenolone, MS"},
    "progesterone":     {"quest": None, "labcorp": None, "goodlabs": "Progesterone"},
    "progesterone-lcms":{"quest": None, "labcorp": None, "goodlabs": "Progesterone, LC/MS"},
    "prolactin":        {"quest": None, "labcorp": None, "goodlabs": "Prolactin"},
    "pth":              {"quest": None, "labcorp": None, "goodlabs": "PTH, Intact without Calcium"},
    "rbc-copper":       {"quest": None, "labcorp": None, "goodlabs": "RBC Copper"},
    "reverse-t3":       {"quest": None, "labcorp": None, "goodlabs": "Reverse T3 Serum/Plasma"},
    "rf":               {"quest": None, "labcorp": None, "goodlabs": "Rheumatoid Factor"},
    "rpr":              {"quest": None, "labcorp": None, "goodlabs": "RPR (Rapid Plasma Reagin) - Syphilis Screening"},
    "esr":              {"quest": None, "labcorp": None, "goodlabs": "Sedimentation Rate-Westergren (ESR)"},
    "selenium":         {"quest": None, "labcorp": None, "goodlabs": "Selenium, Serum or Plasma"},
    "serum-amyloid-a":  {"quest": None, "labcorp": None, "goodlabs": "Serum Amyloid A"},
    "t3-reverse-lcms":  {"quest": None, "labcorp": None, "goodlabs": "T3 Reverse, LC/MS/MS"},
    "t3-total":         {"quest": None, "labcorp": None, "goodlabs": "T3 Total"},
    "t3-uptake":        {"quest": None, "labcorp": None, "goodlabs": "T3 Uptake"},
    "t4-total":         {"quest": None, "labcorp": None, "goodlabs": "T4 (Thyroxine), Total"},
    "t3-free":          {"quest": None, "labcorp": None, "goodlabs": "Triiodothyronine (T3), Free"},
    "tg-antibody":      {"quest": None, "labcorp": None, "goodlabs": "Thyroglobulin Antibody"},
    "tpo":              {"quest": None, "labcorp": None, "goodlabs": "Thyroid Peroxidase Antibody (TPO)"},
    "transferrin":      {"quest": None, "labcorp": None, "goodlabs": "Transferrin"},
    "uric-acid":        {"quest": None, "labcorp": None, "goodlabs": "Uric Acid"},
    "urinalysis":       {"quest": None, "labcorp": None, "goodlabs": "Urinalysis"},
    "vita":             {"quest": None, "labcorp": None, "goodlabs": "Vitamin A, Serum or Plasma"},
    "vitb1":            {"quest": None, "labcorp": None, "goodlabs": "Vitamin B1 (Thiamine), Whole Blood"},
    "vitb2":            {"quest": None, "labcorp": None, "goodlabs": "Vitamin B2 (Riboflavin)"},
    "vitb6":            {"quest": None, "labcorp": None, "goodlabs": "Vitamin B6, Plasma"},
    "zinc-rbc":         {"quest": None, "labcorp": None, "goodlabs": "Zinc, RBC"},
    "zinc-serum":       {"quest": None, "labcorp": None, "goodlabs": "Zinc, Serum or Plasma"},

    # ── GoodLabs bundle tests — Quest/LabCorp pending scraper runs ────

    "abo-rh":              {"quest": None, "labcorp": None, "goodlabs": "ABO Group and Rh Type"},
    "aldo-renin":          {"quest": None, "labcorp": None, "goodlabs": "Aldosterone/Plasma Renin Activity Ratio"},
    "albumin-urine":       {"quest": None, "labcorp": None, "goodlabs": "Albumin, Random Urine with Creatinine"},
    "anemia-panel":        {"quest": None, "labcorp": None, "goodlabs": "Anemia"},
    "celiac":              {"quest": None, "labcorp": None, "goodlabs": "Celiac Disease Antibody Evaluation"},
    "ct-ng":               {"quest": None, "labcorp": None, "goodlabs": "Chlamydia/Neisseria gonorrhoeae"},
    "comp-mens":           {"quest": None, "labcorp": None, "goodlabs": "Comprehensive Men's"},
    "comp-womens":         {"quest": None, "labcorp": None, "goodlabs": "Comprehensive Women's"},
    "dht-free":            {"quest": None, "labcorp": None, "goodlabs": "Dihydrotestosterone (DHT), Free, LC/MS/Dialysis"},
    "estrogens-frac":      {"quest": None, "labcorp": None, "goodlabs": "Estrogens, Fractionated, LC/MS"},
    "fsh-lh":              {"quest": None, "labcorp": None, "goodlabs": "FSH and LH"},
    "full-monty":          {"quest": None, "labcorp": None, "goodlabs": "Full Monty"},
    "gtt":                 {"quest": None, "labcorp": None, "goodlabs": "Glucose Tolerance Test (GTT), Two Hour Oral (WHO Protocol)"},
    "heart-health":        {"quest": None, "labcorp": None, "goodlabs": "Heart Health"},
    "heavy-metals":        {"quest": None, "labcorp": None, "goodlabs": "Heavy Metals"},
    "hb-frac":             {"quest": None, "labcorp": None, "goodlabs": "Hemoglobinopathy Fractionation Cascade"},
    "hiv":                 {"quest": None, "labcorp": None, "goodlabs": "HIV-1/2 Antigen and Antibodies, Fourth Generation, with Reflexes"},
    "iron-tibc":           {"quest": None, "labcorp": None, "goodlabs": "Iron and TIBC"},
    "mens-hormone":        {"quest": None, "labcorp": None, "goodlabs": "Men's Hormone"},
    "metabolic-health":    {"quest": None, "labcorp": None, "goodlabs": "Metabolic Health"},
    "nmr-lipo":            {"quest": None, "labcorp": None, "goodlabs": "NMR LipoProfile"},
    "nutrient-panel":      {"quest": None, "labcorp": None, "goodlabs": "Nutrient"},
    "omegacheck":          {"quest": None, "labcorp": None, "goodlabs": "OmegaCheck"},
    "ogtt":                {"quest": None, "labcorp": None, "goodlabs": "Oral Glucose + Insulin Tolerance Test over 2 hours (4 Specimens) (OGTT)"},
    "prolactin-total":     {"quest": None, "labcorp": None, "goodlabs": "Prolactin, Total and Monomeric"},
    "psa-free":            {"quest": None, "labcorp": None, "goodlabs": "PSA Total+% Free"},
    "pt-inr":              {"quest": None, "labcorp": None, "goodlabs": "PT w/INR"},
    "reticulocyte":        {"quest": None, "labcorp": None, "goodlabs": "Reticulocyte Count"},
    "std-screening":       {"quest": None, "labcorp": None, "goodlabs": "STD Screening"},
    "test-free-total":     {"quest": None, "labcorp": None, "goodlabs": "Testosterone, Free and Total, MS"},
    "test-free-bio-total": {"quest": None, "labcorp": None, "goodlabs": "Testosterone, Free, Bioavailable and Total, MS"},
    "test-calc-shbg":      {"quest": None, "labcorp": None, "goodlabs": "Testosterone, Free (Calculated) and Total, SHBG, Albumin"},
    "ttg":                 {"quest": None, "labcorp": None, "goodlabs": "Tissue Transglutaminase (tTG) Antibodies (IgA, IgG)"},
    "thyroid-panel":       {"quest": None, "labcorp": None, "goodlabs": "Thyroid"},
    "womens-hormone":      {"quest": None, "labcorp": None, "goodlabs": "Women's Hormone"},
    "body-builder":        {"quest": None, "labcorp": None, "goodlabs": "Body Builder Panel"},
}
