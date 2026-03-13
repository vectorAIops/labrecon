# GoodLabs Complete Catalog — March 12, 2026
# Source: app.hellogoodlabs.com/book-tests (manual capture)
# Excludes "Donation" variants (free with blood donation, no listed price)
# Excludes "All the tests in Superpower" bundle ($130) — meta-bundle

# ============================================================
# SECTION 1: Matches to existing 19 test IDs
# Update provider_mappings.py "goodlabs" values with these
# ============================================================

EXISTING_MATCHES = {
    "cbc":        {"name": "Complete Blood Count (CBC) with Differential/Platelet", "price": 3},
    "cmp":        {"name": "Comprehensive Metabolic Panel (CMP)", "price": 5},
    "lipid":      {"name": "Lipid Panel", "price": 8},
    "a1c":        {"name": "Hemoglobin A1c (HbA1c)", "price": 4},
    "crp":        {"name": "High-Sensitivity C-Reactive Protein (hs-CRP)", "price": 6},
    "insulin":    {"name": "Insulin", "price": 4},
    "lpa":        {"name": "Lp(a)", "price": 16},
    "apob":       {"name": "Apolipoprotein B", "price": 8},
    "tsh":        {"name": "Thyroid Stimulating Hormone (TSH)", "price": 5},
    "ft4":        {"name": "Thyroxine, Free (Free T4)", "price": 6},
    "vitd":       {"name": "Vitamin D, 25-Hydroxy", "price": 11},
    "b12":        {"name": "Vitamin B12 (Cobalamin)", "price": 10},
    "ferritin":   {"name": "Ferritin", "price": 9},
    "iron":       {"name": "Iron, TIBC and Ferritin Panel", "price": 15},
    "total-test": {"name": "Testosterone, Total, MS", "price": 11},
    "free-test":  {"name": "Testosterone, Free and Total, MS", "price": 15},
    "estradiol":  {"name": "Estradiol", "price": 7},
    "shbg":       {"name": "Sex Hormone Binding Globulin (SHBG)", "price": 8},
    "psa":        {"name": "PSA Total (Reflex To Free)", "price": 5},
}

# ============================================================
# SECTION 2: New individual tests to add to tests_catalog.py
# These are NOT bundles (bundle=No in source data)
# ============================================================

NEW_INDIVIDUAL_TESTS = {
    "acth":             {"name": "ACTH, Plasma", "price": 18},
    "aluminum":         {"name": "Aluminum, Blood", "price": 145},
    "amylase":          {"name": "Amylase", "price": 4},
    "ana":              {"name": "ANA Screen, IFA, with Reflex to Titer and Pattern", "price": 6},
    "androstenedione":  {"name": "Androstenedione", "price": 17},
    "amh":              {"name": "Anti-Mullerian Hormone (AMH)", "price": 28},
    "arsenic":          {"name": "Arsenic, Blood", "price": 19},
    "c-peptide":        {"name": "C-Peptide", "price": 18},
    "ceruloplasmin":    {"name": "Ceruloplasmin", "price": 13},
    "coq10":            {"name": "Coenzyme Q10, Total", "price": 66},
    "copper":           {"name": "Copper, Serum or Plasma", "price": 27},
    "cortisol":         {"name": "Cortisol", "price": 8},
    "cortisol-lcms":    {"name": "Cortisol, Total, LC/MS", "price": 14},
    "ck":               {"name": "Creatine Kinase (CK), Total", "price": 6},
    "crp-standard":     {"name": "CRP", "price": 5},
    "cystatin-c":       {"name": "Cystatin C", "price": 18},
    "dhea-s":           {"name": "DHEA-Sulfate", "price": 8},
    "dht":              {"name": "Dihydrotestosterone (DHT)", "price": 35},
    "estradiol-lcms":   {"name": "Estradiol, Sensitive, LC/MS", "price": 36},
    "estrogens-total":  {"name": "Estrogens, Total, Immunoassay", "price": 23},
    "estrone":          {"name": "Estrone", "price": 30},
    "fibrinogen":       {"name": "Fibrinogen", "price": 10},
    "folate-rbc":       {"name": "Folate, RBC", "price": 15},
    "folate-serum":     {"name": "Folate, Serum", "price": 6},
    "fructosamine":     {"name": "Fructosamine", "price": 11},
    "fsh":              {"name": "FSH", "price": 5},
    "gastrin":          {"name": "Gastrin", "price": 23},
    "ggt":              {"name": "GGT", "price": 5},
    "glucose":          {"name": "Glucose", "price": 8},
    "gh":               {"name": "Growth Hormone (GH)", "price": 34},
    "hemoglobin":       {"name": "Hemoglobin (Hb)", "price": 1},
    "hep-c":            {"name": "Hepatitis C Antibody", "price": 13},
    "homocysteine":     {"name": "Homocysteine", "price": 13},
    "iga":              {"name": "Immunoglobulin A (IgA) - Serum", "price": 15},
    "inhibin-b":        {"name": "Inhibin B", "price": 291},
    "igf1":             {"name": "Insulin-Like Growth Factor I (IGF-1) LC/MS", "price": 27},
    "il1b":             {"name": "Interleukin-1 Beta (IL-1β)", "price": 322},
    "il6":              {"name": "Interleukin-6 (IL-6)", "price": 119},
    "iodine-urine":     {"name": "Iodine, Random Urine", "price": 45},
    "iodine-serum":     {"name": "Iodine, Serum/Plasma", "price": 53},
    "ldl-direct":       {"name": "LDL Cholesterol (Direct)", "price": 3},
    "lead":             {"name": "Lead (Venous)", "price": 11},
    "leptin":           {"name": "Leptin", "price": 23},
    "lh":               {"name": "LH", "price": 5},
    "lipase":           {"name": "Lipase", "price": 5},
    "lp-pla2":          {"name": "Lp-PLA2 Activity", "price": 36},
    "magnesium-rbc":    {"name": "Magnesium, RBC", "price": 13},
    "mercury":          {"name": "Mercury, Blood", "price": 21},
    "methylmalonic":    {"name": "Methylmalonic Acid", "price": 36},
    "methylmalonic-s":  {"name": "Methylmalonic Acid, Serum", "price": 37},
    "molybdenum":       {"name": "Molybdenum, Serum or Plasma", "price": 105},
    "mthfr":            {"name": "MTHFR Genetic Test", "price": 128},
    "nt-probnp":        {"name": "NT-proBNP", "price": 134},
    "oxldl":            {"name": "OxLDL", "price": 42},
    "pregnenolone":     {"name": "Pregnenolone, MS", "price": 38},
    "progesterone":     {"name": "Progesterone", "price": 9},
    "progesterone-lcms":{"name": "Progesterone, LC/MS", "price": 16},
    "prolactin":        {"name": "Prolactin", "price": 9},
    "pth":              {"name": "PTH, Intact without Calcium", "price": 41},
    "rbc-copper":       {"name": "RBC Copper", "price": 30},
    "reverse-t3":       {"name": "Reverse T3 Serum/Plasma", "price": 32},
    "rf":               {"name": "Rheumatoid Factor", "price": 7},
    "rpr":              {"name": "RPR (Rapid Plasma Reagin) - Syphilis Screening", "price": 7},
    "esr":              {"name": "Sedimentation Rate-Westergren (ESR)", "price": 6},
    "selenium":         {"name": "Selenium, Serum or Plasma", "price": 12},
    "serum-amyloid-a":  {"name": "Serum Amyloid A", "price": 302},
    "t3-reverse-lcms":  {"name": "T3 Reverse, LC/MS/MS", "price": 27},
    "t3-total":         {"name": "T3 Total", "price": 8},
    "t3-uptake":        {"name": "T3 Uptake", "price": 5},
    "t4-total":         {"name": "T4 (Thyroxine), Total", "price": 4},
    "t3-free":          {"name": "Triiodothyronine (T3), Free", "price": 10},
    "tg-antibody":      {"name": "Thyroglobulin Antibody", "price": 5},
    "tpo":              {"name": "Thyroid Peroxidase Antibody (TPO)", "price": 5},
    "transferrin":      {"name": "Transferrin", "price": 11},
    "uric-acid":        {"name": "Uric Acid", "price": 4},
    "urinalysis":       {"name": "Urinalysis", "price": 4},
    "vita":             {"name": "Vitamin A, Serum or Plasma", "price": 30},
    "vitb1":            {"name": "Vitamin B1 (Thiamine), Whole Blood", "price": 25},
    "vitb2":            {"name": "Vitamin B2 (Riboflavin)", "price": 59},
    "vitb6":            {"name": "Vitamin B6, Plasma", "price": 38},
    "zinc-rbc":         {"name": "Zinc, RBC", "price": 17},
    "zinc-serum":       {"name": "Zinc, Serum or Plasma", "price": 11},
}

# ============================================================
# SECTION 3: Bundle tests (bundle=Yes in source data)
# Add to catalog separately — these contain multiple biomarkers
# ============================================================

BUNDLES = {
    "abo-rh":               {"name": "ABO Group and Rh Type", "price": 12},
    "aldo-renin":           {"name": "Aldosterone/Plasma Renin Activity Ratio", "price": 74},
    "albumin-urine":        {"name": "Albumin, Random Urine with Creatinine", "price": 12},
    "anemia-panel":         {"name": "Anemia", "price": 60},
    "celiac":               {"name": "Celiac Disease Antibody Evaluation", "price": 32},
    "ct-ng":                {"name": "Chlamydia/Neisseria gonorrhoeae", "price": 30},
    "comp-mens":            {"name": "Comprehensive Men's", "price": 200},
    "comp-womens":          {"name": "Comprehensive Women's", "price": 200},
    "dht-free":             {"name": "Dihydrotestosterone (DHT), Free, LC/MS/Dialysis", "price": 241},
    "estrogens-frac":       {"name": "Estrogens, Fractionated, LC/MS", "price": 263},
    "fsh-lh":               {"name": "FSH and LH", "price": 9},
    "full-monty":           {"name": "Full Monty", "price": 180},
    "gtt":                  {"name": "Glucose Tolerance Test (GTT), Two Hour Oral (WHO Protocol)", "price": 12},
    "heart-health":         {"name": "Heart Health", "price": 60},
    "heavy-metals":         {"name": "Heavy Metals", "price": 50},
    "hb-frac":              {"name": "Hemoglobinopathy Fractionation Cascade", "price": 25},
    "hiv":                  {"name": "HIV-1/2 Antigen and Antibodies, Fourth Generation, with Reflexes", "price": 24},
    "iron-tibc":            {"name": "Iron and TIBC", "price": 7},
    "mens-hormone":         {"name": "Men's Hormone", "price": 60},
    "metabolic-health":     {"name": "Metabolic Health", "price": 60},
    "nmr-lipo":             {"name": "NMR LipoProfile", "price": 38},
    "nutrient-panel":       {"name": "Nutrient", "price": 60},
    "omegacheck":           {"name": "OmegaCheck", "price": 42},
    "ogtt":                 {"name": "Oral Glucose + Insulin Tolerance Test over 2 hours (4 Specimens) (OGTT)", "price": 40},
    "prolactin-total":      {"name": "Prolactin, Total and Monomeric", "price": 505},
    "psa-free":             {"name": "PSA Total+% Free", "price": 12},
    "pt-inr":               {"name": "PT w/INR", "price": 7},
    "reticulocyte":         {"name": "Reticulocyte Count", "price": 9},
    "std-screening":        {"name": "STD Screening", "price": 73},
    "test-free-total":      {"name": "Testosterone, Free and Total, MS", "price": 15},
    "test-free-bio-total":  {"name": "Testosterone, Free, Bioavailable and Total, MS", "price": 22},
    "test-calc-shbg":       {"name": "Testosterone, Free (Calculated) and Total, SHBG, Albumin", "price": 40},
    "ttg":                  {"name": "Tissue Transglutaminase (tTG) Antibodies (IgA, IgG)", "price": 51},
    "thyroid-panel":        {"name": "Thyroid", "price": 60},
    "womens-hormone":       {"name": "Women's Hormone", "price": 60},
    "body-builder":         {"name": "Body Builder Panel", "price": 225},
}

# ============================================================
# NOTES
# ============================================================
# - "Donation" variants are free with blood donation — not priced. 
#   Consider adding a "free with donation" flag on the site later.
# - GoodLabs has two CRP tests: standard "CRP" ($5) and "hs-CRP" ($6).
#   Mapped hs-CRP to existing crp ID. Standard CRP added as crp-standard.
# - GoodLabs has two reverse T3 tests and two methylmalonic acid tests
#   (different assay methods). Both included.
# - "Iron and TIBC" ($7) is a smaller bundle than "Iron, TIBC and Ferritin Panel" ($15).
#   Mapped the full panel to existing iron ID. Smaller bundle in BUNDLES section.
# - "Testosterone, Free and Total, MS" appears in both existing matches 
#   (as free-test) and bundles. The bundle entry is a duplicate reference.
# - Superpower bundle ($130) excluded — it's a meta-bundle of other bundles.
