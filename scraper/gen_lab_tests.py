"""
Generate app/data/labTests.ts from scraped prices + catalog data.
Run from repo root: py scraper/gen_lab_tests.py > app/data/labTests.ts
"""
import sys, ast, json
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")

# ── Load source files ─────────────────────────────────────────────────────────

def _load(path, varname):
    with open(path, encoding="utf-8") as f:
        src = f.read()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            tgt = getattr(node, "targets", None) or [getattr(node, "target", None)]
            if tgt and isinstance(tgt[0], ast.Name) and tgt[0].id == varname:
                val = getattr(node, "value", None)
                if val:
                    return ast.literal_eval(val)
    raise KeyError(varname)

PROVIDER_NAMES   = _load("scraper/provider_mappings.py",    "PROVIDER_NAMES")
EXISTING_MATCHES = _load("scraper/goodlabs-catalog-data.py","EXISTING_MATCHES")
NEW_IND          = _load("scraper/goodlabs-catalog-data.py","NEW_INDIVIDUAL_TESTS")
BUNDLES_GL       = _load("scraper/goodlabs-catalog-data.py","BUNDLES")
TESTS_CAT        = _load("scraper/tests_catalog.py",        "TESTS")
# alt_names keyed by id
ALT_NAMES = {t["id"]: t.get("alt_names", []) for t in TESTS_CAT}

# ── GoodLabs prices ───────────────────────────────────────────────────────────
GL_PRICES = {}
for tid, d in EXISTING_MATCHES.items(): GL_PRICES[tid] = d["price"]
for tid, d in NEW_IND.items():          GL_PRICES[tid] = d["price"]
for tid, d in BUNDLES_GL.items():       GL_PRICES[tid] = d["price"]

# ── Quest prices (from 2026-03-12 scrape) ────────────────────────────────────
QUEST_PRICES = {
    "Complete Blood Count (CBC) Test":                  29.00,
    "Comprehensive Metabolic Panel (CMP) Test":         44.10,
    "Cholesterol (Lipid) Panel":                        53.10,
    "Hemoglobin A1c Test":                              35.10,
    "hsCRP Test for Inflammation Marker":               65.00,
    "Lipoprotein(a)/Lp(a) Test":                        40.50,
    "Testosterone Test":                                69.00,
    "Thyroid TSH Function Test":                        49.00,
    "Vitamin D Test":                                   67.50,
    "Vitamin B12 Test":                                 44.10,
    "Iron, TIBC & Ferritin Panel":                      53.10,
    "Prostate Screening (PSA)":                         69.00,
    "AMH Marker Test":                                 135.00,
    "Autoimmune Screening Test (ANA with Reflex)":     112.00,
    "Copper Test":                                      52.00,
    "Cortisol Stress Hormone Test":                     89.00,
    "Hepatitis C Test With Confirmation":               62.00,
    "Homocysteine Test":                                75.00,
    "Iodine Test":                                      52.00,
    "Lead Test":                                        52.00,
    "Leptin (Weight Regulation) Test":                  69.00,
    "Magnesium Test":                                   35.10,
    "Progesterone Test":                                89.00,
    "Syphilis Test With Confirmation":                  52.00,
    "Gout (Uric Acid) Test":                            42.00,
    "Urinalysis / Urinary Tract Infection (UTI) Test":  40.00,
    "Vitamin A Test":                                   44.10,
    "Zinc Test":                                        53.10,
    "Blood Type Test":                                  40.00,
    "Celiac (Gluten) Disease Panel":                   112.00,
    "Chlamydia & Gonorrhea Test":                      105.00,
    "HIV 1 & 2 Test with Confirmation":                 85.00,
    "Prothrombin Time with INR Test":                   42.00,
}

# ── LabCorp prices + URLs (from 2026-03-12 scrape) ───────────────────────────
LC_BASE = "https://www.ondemand.labcorp.com"
LABCORP_DATA = {
    "Complete Blood Count (CBC) Test":                    {"price":  29, "path": "/content/labcorp-ondemand/us/en/lab-tests/complete-blood-count"},
    "Comprehensive Metabolic Panel (CMP)":                {"price":  49, "path": "/content/labcorp-ondemand/us/en/lab-tests/comprehensive-metabolic-panel"},
    "Cholesterol and Lipid Panel Test":                   {"price":  59, "path": "/content/labcorp-ondemand/us/en/lab-tests/cholesterol-test-lipid-panel"},
    "Diabetes Risk (HbA1c) Test":                         {"price":  39, "path": "/content/labcorp-ondemand/us/en/lab-tests/diabetes-risk-hbA1c-test"},
    "Inflammation (hs-CRP) Test":                         {"price":  59, "path": "/content/labcorp-ondemand/us/en/lab-tests/inflammation-hs-crp-test"},
    "Lipoprotein(a) Test":                                {"price":  49, "path": "/content/labcorp-ondemand/us/en/lab-tests/lipoprotein-a-test"},
    "Apolipoprotein B (ApoB) Test":                       {"price":  69, "path": "/content/labcorp-ondemand/us/en/lab-tests/apob-test"},
    "Thyroid Stimulating Hormone (TSH) Test":             {"price":  49, "path": "/content/labcorp-ondemand/us/en/lab-tests/thyroid-stimulating-hormone-tsh-test"},
    "Vitamin D Test":                                     {"price":  99, "path": "/content/labcorp-ondemand/us/en/lab-tests/vitamin-d-test"},
    "Vitamin B12 Test":                                   {"price":  49, "path": "/content/labcorp-ondemand/us/en/lab-tests/vitamin-b12-test"},
    "Ferritin Test":                                      {"price":  59, "path": "/content/labcorp-ondemand/us/en/lab-tests/ferritin-test"},
    "Total Testosterone Test":                            {"price":  69, "path": "/content/labcorp-ondemand/us/en/lab-tests/total-testosterone-blood-test"},
    "Estradiol (E2) Test":                                {"price":  79, "path": "/content/labcorp-ondemand/us/en/lab-tests/estradiol-test"},
    "PSA Prostate Cancer Screening Test":                 {"price":  69, "path": "/content/labcorp-ondemand/us/en/lab-tests/psa-prostate-cancer-screening-test"},
    "Amylase Test":                                       {"price":  39, "path": "/content/labcorp-ondemand/us/en/lab-tests/amylase-test"},
    "Women's Fertility AMH Test":                         {"price": 139, "path": "/content/labcorp-ondemand/us/en/lab-tests/amh-blood-test"},
    "Copper Test":                                        {"price":  59, "path": "/content/labcorp-ondemand/us/en/lab-tests/copper-test"},
    "Cortisol Test":                                      {"price":  89, "path": "/content/labcorp-ondemand/us/en/lab-tests/cortisol-test"},
    "DHEA-S Test":                                        {"price":  69, "path": "/content/labcorp-ondemand/us/en/lab-tests/dheas-blood-test"},
    "Follicle-Stimulating Hormone (FSH) Test":            {"price":  59, "path": "/content/labcorp-ondemand/us/en/lab-tests/follicle-stimulating-hormone-test"},
    "GGT Test":                                           {"price":  59, "path": "/content/labcorp-ondemand/us/en/lab-tests/ggt-test"},
    "Fasting Glucose Test":                               {"price":  39, "path": "/content/labcorp-ondemand/us/en/lab-tests/fasting-glucose-test"},
    "Hepatitis C Test":                                   {"price":  69, "path": "/content/labcorp-ondemand/us/en/lab-tests/hepatitis-c-test"},
    "Homocysteine Test":                                  {"price":  79, "path": "/content/labcorp-ondemand/us/en/lab-tests/homocysteine-test"},
    "Iodine Test":                                        {"price":  69, "path": "/content/labcorp-ondemand/us/en/lab-tests/iodine-test"},
    "Lead Test":                                          {"price":  59, "path": "/content/labcorp-ondemand/us/en/lab-tests/lead-test"},
    "Leptin Test":                                        {"price":  79, "path": "/content/labcorp-ondemand/us/en/lab-tests/leptin-test"},
    "Luteinizing Hormone (LH) Test":                      {"price":  49, "path": "/content/labcorp-ondemand/us/en/lab-tests/luteinizing-hormone-lh-test"},
    "Lipase Test":                                        {"price":  39, "path": "/content/labcorp-ondemand/us/en/lab-tests/lipase-test"},
    "Albumin to Creatinine Ratio (ACR) Test":             {"price":  79, "path": "/content/labcorp-ondemand/us/en/lab-tests/albumin-creatinine-ratio-acr-test"},
    "NMR LipoProfile\u00ae Test":                         {"price": 119, "path": "/content/labcorp-ondemand/us/en/lab-tests/nmr-lipoprofile-test"},
    "Progesterone Test":                                  {"price":  59, "path": "/content/labcorp-ondemand/us/en/lab-tests/progesterone-test"},
    "Prolactin Test":                                     {"price":  79, "path": "/content/labcorp-ondemand/us/en/lab-tests/prolactin-blood-test"},
    "Syphilis Test":                                      {"price":  59, "path": "/content/labcorp-ondemand/us/en/lab-tests/syphilis-rpr-test"},
    "Selenium Test":                                      {"price": 109, "path": "/content/labcorp-ondemand/us/en/lab-tests/selenium-test"},
    "Free T3 Test":                                       {"price":  89, "path": "/content/labcorp-ondemand/us/en/lab-tests/free-t3-test"},
    "Thyroid Peroxidase (TPO) Antibody Test":             {"price":  69, "path": "/content/labcorp-ondemand/us/en/lab-tests/thyroid-peroxidase-tpo-antibody-test"},
    "Uric Acid Test":                                     {"price":  49, "path": "/content/labcorp-ondemand/us/en/lab-tests/uric-acid-test"},
    "Urine Analysis Test":                                {"price":  49, "path": "/content/labcorp-ondemand/us/en/lab-tests/urine-analysis"},
    "Vitamin A Test":                                     {"price":  59, "path": "/content/labcorp-ondemand/us/en/lab-tests/vitamin-a-test"},
    "Zinc Test":                                          {"price":  69, "path": "/content/labcorp-ondemand/us/en/lab-tests/zinc-test"},
    "Blood Type Test":                                    {"price":  39, "path": "/content/labcorp-ondemand/us/en/lab-tests/blood-type-test"},
    "Anemia Test":                                        {"price": 189, "path": "/content/labcorp-ondemand/us/en/lab-tests/anemia-test"},
    "Celiac Disease Antibody Test":                       {"price": 119, "path": "/content/labcorp-ondemand/us/en/lab-tests/celiac-disease-antibody-test"},
    "Chlamydia, Gonorrhea, Trichomoniasis Test":          {"price": 189, "path": "/content/labcorp-ondemand/us/en/lab-tests/sti-test-chlamydia-gonorrhea-trichomoniasis"},
    "HIV Test":                                           {"price":  99, "path": "/content/labcorp-ondemand/us/en/lab-tests/hiv-test"},
}

# ── Descriptions (plain, medical) keyed by test ID ───────────────────────────
DESCS = {
  # Original 19 — preserved from labTests.ts
  "cbc":       ("Counts and measures your red blood cells, white blood cells, and platelets. One of the most routinely ordered panels in medicine.",
                "Complete cellular evaluation of peripheral blood. Screens for anemia, infection, inflammation, polycythemia, and platelet disorders."),
  "cmp":       ("A 14-marker snapshot of your metabolic health — blood sugar, kidney function, liver enzymes, and electrolytes.",
                "14-panel metabolic assessment covering renal function, hepatic enzymes, glucose metabolism, and fluid/electrolyte balance."),
  "lipid":     ("Measures cholesterol and triglycerides. Standard for assessing cardiovascular health.",
                "Quantification of serum lipid fractions. Primary screen for dyslipidemia and cardiovascular risk."),
  "a1c":       ("Shows your average blood sugar over the past 2–3 months. A better picture than a single glucose reading.",
                "Percentage of glycated hemoglobin. Standard marker for screening and monitoring glycemic control in prediabetes and diabetes."),
  "crp":       ("Measures inflammation in the body. Used for tracking inflammatory status and cardiovascular risk assessment.",
                "Acute-phase reactant synthesized by the liver in response to cytokine signaling. High-sensitivity CRP (hsCRP) is used in cardiovascular risk stratification."),
  "insulin":   ("Measures insulin levels. Best done fasting. Useful for tracking insulin resistance.",
                "Fasting serum insulin quantification. Used to calculate HOMA-IR and evaluate pancreatic beta-cell function."),
  "lpa":       ("Measures a specific atherogenic lipoprotein particle linked to heart disease. Levels are largely genetic and not significantly changed by diet.",
                "Quantification of lipoprotein(a), an LDL-like particle with Apo(a). An independent, largely genetically determined cardiovascular risk factor."),
  "apob":      ("Counts the total number of atherogenic lipoprotein particles. Many consider it a more accurate cardiovascular risk marker than LDL cholesterol alone.",
                "Measures total apolipoprotein B, present on all atherogenic lipoproteins (LDL, IDL, VLDL, Lp(a)). Reflects total particle burden; increasingly used in cardiovascular risk stratification."),
  "tsh":       ("Checks how well your thyroid is functioning. Usually the first thyroid test ordered.",
                "Third-generation immunometric assay for thyroid-stimulating hormone. Primary screen for hypothyroidism and hyperthyroidism."),
  "ft4":       ("Measures the active thyroid hormone circulating freely in the blood. Often ordered alongside TSH.",
                "Immunoassay for unbound thyroxine (T4). Used with TSH to differentiate primary from secondary thyroid dysfunction and guide levothyroxine dosing."),
  "vitd":      ("Checks your vitamin D status. One of the most common nutrient deficiencies in adults.",
                "Measures serum 25-hydroxyvitamin D, the primary circulating form and standard clinical marker for vitamin D sufficiency."),
  "b12":       ("Measures B12, important for nerve function, energy production, and red blood cell formation.",
                "Serum cobalamin quantification. Used to evaluate B12 deficiency, macrocytic anemia, and peripheral neuropathy."),
  "ferritin":  ("Measures your iron storage levels. The most sensitive early indicator of iron deficiency.",
                "Acute-phase protein reflecting total body iron stores. Decreased in iron-deficiency anemia; elevated in hemochromatosis and inflammatory states."),
  "iron":      ("Full picture of iron metabolism — how much iron is in your blood and how much your body could absorb.",
                "Quantifies serum iron, total and unsaturated iron binding capacity, and transferrin saturation. Differentiates iron-deficiency anemia from anemia of chronic disease."),
  "total-test":("Measures total testosterone. Standard for TRT monitoring, general hormonal health, and baseline checks.",
                "Immunoassay or LC-MS/MS quantification of total serum testosterone. Primary marker for hypogonadism screening and TRT monitoring."),
  "free-test": ("Measures the testosterone not bound to proteins — the portion that's biologically active.",
                "Calculated or direct measurement of unbound testosterone. More sensitive than total testosterone alone in individuals with altered SHBG levels."),
  "estradiol": ("Measures estrogen (E2). Used by people on TRT or HRT to monitor levels and track hormonal status.",
                "Quantitative estradiol measurement. LC-MS/MS preferred over immunoassay for men and low-level monitoring. Used in TRT/HRT management and fertility evaluation."),
  "shbg":      ("Measures a protein that binds to sex hormones, affecting how much free testosterone and estrogen are available in the body.",
                "Quantification of sex hormone binding globulin. Used alongside total testosterone to estimate free testosterone and assess androgen bioavailability."),
  "psa":       ("Screens for prostate health in men. Typically recommended starting at age 40–50 depending on risk factors.",
                "Total PSA immunoassay. Primary prostate cancer screening marker; also used for post-treatment monitoring and risk stratification."),
  # New individual tests
  "acth":           ("Measures adrenocorticotropic hormone, which signals the adrenals to produce cortisol. Used to evaluate adrenal and pituitary function.",
                     "Plasma ACTH quantification. Used in differential diagnosis of Cushing's syndrome, Addison's disease, and secondary adrenal insufficiency."),
  "aluminum":       ("Screens for aluminum accumulation in blood. Relevant for patients on dialysis or with occupational exposures.",
                     "Whole blood aluminum by ICP-MS. Elevated in dialysis encephalopathy, industrial exposure, and prolonged antacid use."),
  "amylase":        ("Measures the digestive enzyme amylase. Used to evaluate pancreatic and salivary gland function.",
                     "Serum amylase activity. Elevated in acute pancreatitis, salivary gland disorders, and intestinal ischemia."),
  "ana":            ("Screens for antinuclear antibodies — a marker associated with autoimmune diseases like lupus and Sjögren's syndrome.",
                     "IFA-based ANA screen with reflex to titer and pattern. Primary screen for systemic autoimmune diseases including SLE, Sjögren's, and mixed connective tissue disease."),
  "androstenedione":("Measures a precursor sex hormone produced by the adrenals and gonads. Used in evaluation of androgen excess disorders.",
                     "Androstenedione quantification, an adrenal and gonadal androgen precursor. Elevated in congenital adrenal hyperplasia, PCOS, and adrenal tumors."),
  "amh":            ("Measures anti-Müllerian hormone — a marker of ovarian reserve in women and testicular function in men.",
                     "AMH is produced by ovarian granulosa follicles; declining levels reflect diminishing ovarian reserve. Also elevated in PCOS. In men, assesses Sertoli cell function."),
  "arsenic":        ("Checks for arsenic in the blood. Used for occupational screening and suspected toxic exposure.",
                     "Whole blood arsenic measurement by ICP-MS. Differentiates inorganic (toxic) from organic (dietary seafood-derived) arsenic."),
  "c-peptide":      ("Measures C-peptide, a byproduct of insulin production, to assess how much insulin your pancreas is making.",
                     "C-peptide is co-secreted with insulin in equimolar amounts. Distinguishes type 1 from type 2 diabetes and evaluates residual beta-cell function."),
  "ceruloplasmin":  ("Measures the main copper-carrying protein in blood. Used to evaluate copper metabolism disorders.",
                     "Serum ceruloplasmin quantification. Low in Wilson's disease; elevated in inflammatory states. Part of copper metabolism workup with serum copper."),
  "coq10":          ("Measures Coenzyme Q10 (ubiquinol), an antioxidant essential for cellular energy production. May be depleted by statins.",
                     "Total CoQ10 plasma quantification. Mitochondrial electron transport chain component; may be reduced by statin therapy. Used in mitochondrial dysfunction evaluation."),
  "copper":         ("Measures copper levels in blood. Used to screen for Wilson's disease and assess copper status.",
                     "Serum/plasma copper quantification. Elevated in inflammatory states; paradoxically low in Wilson's disease due to defective ceruloplasmin binding."),
  "cortisol":       ("Measures cortisol, the primary stress hormone produced by the adrenal glands. Time-of-day dependent.",
                     "Serum cortisol immunoassay. Used to evaluate adrenal function, Cushing's syndrome, and adrenal insufficiency. Results are diurnally dependent — morning draw standard."),
  "cortisol-lcms":  ("LC/MS cortisol assay — more accurate at low levels than standard immunoassay.",
                     "LC/MS cortisol quantification provides superior analytical specificity by eliminating immunoassay cross-reactivity with cortisol metabolites and exogenous steroids."),
  "ck":             ("Measures creatine kinase, an enzyme released when muscle is damaged. Used to detect muscle injury or myopathy.",
                     "Total CK serum activity. Elevated in rhabdomyolysis, myocardial infarction, inflammatory myopathies, and statin-induced myopathy."),
  "crp-standard":   ("Standard C-reactive protein — detects acute inflammation. Not sensitive enough for cardiovascular risk stratification (use hsCRP for that).",
                     "Standard CRP immunoassay detecting acute-phase elevation >10 mg/L. Not suitable for cardiovascular risk stratification; use hsCRP for that purpose."),
  "cystatin-c":     ("Measures cystatin C, a kidney function marker less affected by muscle mass than creatinine — more accurate in some populations.",
                     "Cystatin C is freely filtered by the glomerulus and not secreted. Independent of muscle mass, sex, and diet — a more accurate eGFR estimate in sarcopenic or obese patients."),
  "dhea-s":         ("Measures DHEA-sulfate, the main adrenal androgen. Used to evaluate adrenal function and androgen levels.",
                     "DHEA-S is the most abundant circulating adrenal androgen and the most stable (long half-life). Elevated in CAH and adrenal tumors; used in PCOS and adrenal workup."),
  "dht":            ("Measures dihydrotestosterone, the most potent androgen. Relevant for hair loss, BPH, and advanced hormone monitoring.",
                     "DHT is the primary androgenic driver of benign prostatic hyperplasia and androgenetic alopecia. Elevated in 5α-reductase excess; relevant in TRT and finasteride monitoring."),
  "estradiol-lcms": ("Sensitive LC/MS estradiol assay — more accurate at low levels. Preferred for men, postmenopausal women, and precision hormone tracking.",
                     "Sensitive LC/MS estradiol provides greater analytical precision at sub-20 pg/mL than immunoassay. Preferred in male TRT monitoring, postmenopausal assessment, and low-estrogen states."),
  "estrogens-total":("Measures total estrogen concentration in blood. Less specific than testing individual estrogens separately.",
                     "Total estrogens immunoassay reflecting combined E1, E2, and E3 levels. Less specific than fractionated LC/MS panel; useful as a broad estrogenic activity screen."),
  "estrone":        ("Measures estrone (E1), the primary estrogen after menopause. Useful in HRT monitoring.",
                     "Estrone is the dominant estrogen post-menopause, produced via peripheral aromatization of androstenedione. Used in HRT monitoring and perimenopausal evaluation."),
  "fibrinogen":     ("Measures fibrinogen, a blood-clotting protein that also indicates inflammation. Used in coagulation and cardiovascular workups.",
                     "Plasma fibrinogen quantification. Elevated in inflammatory states; independent cardiovascular risk factor. Part of coagulation cascade and inflammatory panel evaluation."),
  "folate-rbc":     ("Measures folate stored inside red blood cells — a better indicator of long-term folate status than serum folate.",
                     "RBC folate reflects tissue folate stores over the preceding ~3 months. More stable than serum folate; relevant for megaloblastic anemia workup and methylation assessment."),
  "folate-serum":   ("Measures folate in the blood. Important for methylation, DNA synthesis, and neural tube health.",
                     "Serum folate measures recent dietary intake. Used in B9 deficiency evaluation and megaloblastic anemia workup; pairs with RBC folate and B12 for complete picture."),
  "fructosamine":   ("Measures average blood sugar over the past 2–3 weeks. Useful when A1c is unreliable due to red blood cell abnormalities.",
                     "Fructosamine reflects mean glycemia over ~2–3 weeks. Useful in hemolytic anemia, hemoglobinopathies, or other conditions affecting HbA1c reliability."),
  "fsh":            ("Measures follicle-stimulating hormone. Used to evaluate fertility, menopause status, and reproductive health.",
                     "FSH drives follicle development in women and spermatogenesis in men. Elevated FSH indicates primary ovarian insufficiency or primary hypogonadism."),
  "gastrin":        ("Measures gastrin, a hormone that stimulates stomach acid. Used to evaluate ulcers and gastrin-secreting tumors (Zollinger-Ellison syndrome).",
                     "Serum gastrin quantification. Markedly elevated in Zollinger-Ellison syndrome. Also elevated with chronic PPI use, atrophic gastritis, and H. pylori infection."),
  "ggt":            ("Measures GGT, a liver enzyme particularly sensitive to alcohol use and liver/bile duct disease.",
                     "Gamma-glutamyl transferase is elevated in hepatobiliary disease, chronic alcohol use, and drug-induced liver injury. More sensitive than ALT for alcohol-related liver disease."),
  "glucose":        ("Measures blood glucose (blood sugar). Standard test for diabetes screening and metabolic health.",
                     "Fasting serum glucose quantification. Primary screen for diabetes, prediabetes, and hypoglycemia. Results must be interpreted in the context of fasting status."),
  "gh":             ("Measures growth hormone. Used to evaluate pituitary function, growth disorders, and GH therapy.",
                     "GH is pulsatilely secreted by anterior pituitary somatotrophs. Single random measurements are rarely diagnostic; stimulus/suppression tests are preferred for acromegaly and deficiency."),
  "hemoglobin":     ("Measures hemoglobin, the oxygen-carrying protein in red blood cells. Used to screen for anemia.",
                     "Hemoglobin quantification; a component of CBC but available standalone. Used in rapid anemia screening and point-of-care settings."),
  "hep-c":          ("Tests for hepatitis C antibodies, indicating past or current HCV infection.",
                     "Hepatitis C antibody immunoassay. Reactive results require confirmatory HCV RNA testing to distinguish active from resolved infection."),
  "homocysteine":   ("Measures homocysteine, an amino acid linked to cardiovascular risk and B vitamin deficiency.",
                     "Elevated homocysteine is associated with increased cardiovascular and thrombotic risk. May indicate B6, B12, or folate deficiency or MTHFR variant."),
  "iga":            ("Measures immunoglobulin A (IgA). Used in IgA deficiency evaluation and as part of celiac disease workup.",
                     "IgA serum quantification. IgA deficiency (total IgA <7 mg/dL) causes false-negative IgA-based celiac antibody tests and increases susceptibility to mucosal infections."),
  "inhibin-b":      ("Measures inhibin B, a hormone from the gonads that reflects testicular or ovarian function.",
                     "Inhibin B is produced by Sertoli cells in men and granulosa cells in women. Low in primary gonadal failure and diminished ovarian reserve; used in male fertility evaluation."),
  "igf1":           ("Measures IGF-1, a liver hormone that reflects growth hormone activity. More stable than GH for routine testing.",
                     "IGF-1 LC/MS quantification. Stable 24-hour surrogate of GH secretion status. Used in acromegaly diagnosis, GH deficiency evaluation, and longevity monitoring."),
  "il1b":           ("Measures interleukin-1 beta, a key pro-inflammatory cytokine elevated in inflammatory and autoimmune conditions.",
                     "IL-1β is a master mediator of innate immunity. Elevated in inflammatory arthritis, autoinflammatory syndromes, and metabolic inflammation associated with obesity."),
  "il6":            ("Measures interleukin-6, a cytokine involved in both acute inflammation and chronic immune regulation.",
                     "IL-6 is a pleiotropic cytokine elevated in infection, autoimmune disease, and metabolic syndrome. Relevant in cytokine storm monitoring and tocilizumab response assessment."),
  "iodine-urine":   ("Measures iodine in urine. Reflects recent dietary iodine intake rather than true body stores.",
                     "Spot urine iodine measures recent iodine intake. Day-to-day variability limits individual diagnostic utility; better suited for population-level surveillance than clinical diagnosis."),
  "iodine-serum":   ("Measures iodine in blood. Used when thyroid-related iodine excess or deficiency is suspected.",
                     "Serum iodine measurement. Elevated in iodine toxicity from contrast agents or amiodarone; used in thyroid function workup when iodine imbalance is clinically suspected."),
  "ldl-direct":     ("Directly measures LDL cholesterol without calculation. More accurate when triglycerides are elevated.",
                     "Direct LDL measurement by homogeneous assay. Preferred over the Friedewald equation when triglycerides exceed 400 mg/dL or in non-fasting specimens."),
  "lead":           ("Tests for lead in the blood. Used for occupational screening and to assess heavy metal exposure.",
                     "Venous blood lead quantification by ICP-MS. CDC threshold for elevated BLL is 3.5 µg/dL in children; OSHA medical removal threshold for workers is 50 µg/dL."),
  "leptin":         ("Measures leptin, a hormone secreted by fat cells that regulates hunger and energy balance.",
                     "Leptin is an adipokine reflecting fat mass and energy stores. Deficiency causes severe obesity; elevated in leptin resistance. Used in hypothalamic amenorrhea evaluation."),
  "lh":             ("Measures luteinizing hormone. Used to assess fertility, ovulation timing, and pituitary function.",
                     "LH drives testosterone production in men and triggers ovulation in women. Elevated in primary hypogonadism; suppressed in hypothalamic hypogonadism and exogenous androgen use."),
  "lipase":         ("Measures lipase, a pancreatic enzyme. Elevated levels indicate pancreatitis or pancreatic injury.",
                     "Serum lipase quantification. More pancreas-specific than amylase. Elevated in acute pancreatitis, remaining elevated longer than amylase."),
  "lp-pla2":        ("Measures Lp-PLA2 activity — a vascular inflammation marker linked to plaque instability and stroke risk.",
                     "Lp-PLA2 is produced by macrophages within atherosclerotic plaques. Elevated activity reflects vascular inflammation and is independently associated with cardiovascular events."),
  "magnesium-rbc":  ("Measures magnesium inside red blood cells — a better indicator of tissue magnesium than serum levels.",
                     "RBC magnesium reflects intracellular stores more accurately than serum magnesium, which is tightly regulated and often normal even with cellular depletion."),
  "mercury":        ("Tests for mercury in blood. Used to detect methylmercury exposure from fish or occupational sources.",
                     "Whole blood mercury by ICP-MS. Elevated in fish-heavy diets (methylmercury) or occupational/industrial exposure. Speciation testing differentiates organic from inorganic mercury."),
  "methylmalonic":  ("Measures methylmalonic acid, which rises when B12 is functionally deficient. More sensitive than serum B12 alone.",
                     "MMA accumulates when B12-dependent methylmalonyl-CoA mutase is impaired. More sensitive marker of functional B12 deficiency than serum B12 level alone."),
  "methylmalonic-s":("Serum methylmalonic acid assay — same clinical utility as the standard test with a different specimen.",
                     "Serum MMA quantification. Analytically equivalent to plasma MMA; ordered when serum is the available specimen type."),
  "molybdenum":     ("Measures molybdenum, an essential trace mineral required by several enzymes.",
                     "Molybdenum serum measurement. Required cofactor for xanthine oxidase, aldehyde oxidase, and sulfite oxidase. Deficiency is rare; assessed in parenteral nutrition patients."),
  "mthfr":          ("Genetic test for MTHFR variants (C677T and A1298C) that affect folate metabolism and homocysteine levels.",
                     "MTHFR C677T and A1298C genotyping. Variants reduce methylenetetrahydrofolate reductase activity, impairing one-carbon metabolism and potentially elevating homocysteine."),
  "nt-probnp":      ("Measures NT-proBNP, a biomarker released by the heart under stress. Used to detect and monitor heart failure.",
                     "NT-proBNP is a cardiac stretch marker elevated in heart failure, pulmonary hypertension, and renal failure. Used for HF diagnosis, severity stratification, and treatment response."),
  "oxldl":          ("Measures oxidized LDL, a more atherogenic and inflammatory form of LDL associated with plaque formation.",
                     "OxLDL is formed by free radical oxidation of LDL particles. More atherogenic than native LDL; promotes foam cell formation and is independently associated with cardiovascular events."),
  "pregnenolone":   ("Measures pregnenolone, the master precursor steroid produced from cholesterol. Used in adrenal function and steroidogenesis workup.",
                     "Pregnenolone is the primary precursor for all steroid hormones. LC/MS assay provides specificity over immunoassay. Used in adrenal insufficiency and steroidogenesis pathway evaluation."),
  "progesterone":   ("Measures progesterone. Used for cycle tracking, confirming ovulation, and fertility/HRT monitoring.",
                     "Progesterone quantification. Peaks at mid-luteal phase; used to confirm ovulation. Essential for assisted reproduction, pregnancy monitoring, and HRT management."),
  "progesterone-lcms":("LC/MS progesterone — more accurate at low levels. Useful for male hormone tracking or follicular phase monitoring.",
                     "LC/MS progesterone provides greater specificity at low concentrations than immunoassay. Preferred in males, the follicular phase, and precision HRT assessment."),
  "prolactin":      ("Measures prolactin. Elevated levels can suppress sex hormones and cause fertility issues.",
                     "Prolactin is secreted by pituitary lactotrophs. Hyperprolactinemia suppresses GnRH and sex hormone production; causes of elevation include prolactinoma, medications, and hypothyroidism."),
  "pth":            ("Measures parathyroid hormone, which regulates calcium and phosphorus. Used to evaluate bone and mineral metabolism.",
                     "Intact PTH quantification. PTH is the primary regulator of calcium homeostasis via bone resorption, renal calcium reabsorption, and vitamin D activation."),
  "rbc-copper":     ("Measures copper inside red blood cells. Reflects long-term copper status more reliably than serum copper.",
                     "RBC copper reflects intracellular copper stores accumulated over the lifespan of red blood cells (~120 days), providing a longer-term view than serum copper."),
  "reverse-t3":     ("Measures reverse T3, an inactive form of thyroid hormone. Elevated levels may impair active T3 activity.",
                     "Reverse T3 is produced by deiodination of T4 to a biologically inactive form. Elevated rT3 may reflect impaired T4-to-T3 conversion in illness, stress, or selenium deficiency."),
  "rf":             ("Screens for rheumatoid factor, an autoantibody associated with rheumatoid arthritis.",
                     "RF is an autoantibody against the Fc region of IgG. Present in ~80% of RA patients; also elevated in other autoimmune conditions, chronic infections, and healthy elderly."),
  "rpr":            ("Tests for syphilis using the RPR method — a standard syphilis screening test.",
                     "RPR is a non-treponemal syphilis screening assay detecting cardiolipin antibodies. Reactive results require confirmation with treponemal tests (FTA-ABS or TPPA)."),
  "esr":            ("Measures how fast red blood cells settle — a general, nonspecific marker of inflammation.",
                     "ESR (Westergren method) is a nonspecific inflammatory marker elevated in infection, autoimmune disease, malignancy, and anemia. Slower to rise and fall than CRP."),
  "selenium":       ("Measures selenium, an essential antioxidant mineral important for thyroid hormone conversion and immune health.",
                     "Serum selenium quantification. Selenium is a cofactor for glutathione peroxidase and iodothyronine deiodinases; deficiency impairs T4-to-T3 conversion and immune function."),
  "serum-amyloid-a":("Measures serum amyloid A, a highly sensitive acute-phase protein that rises sharply during inflammation.",
                     "SAA is an acute-phase reactant with a dynamic range exceeding 1000-fold. More sensitive than CRP in some inflammatory conditions; chronic elevation predicts secondary amyloidosis risk."),
  "t3-reverse-lcms":("LC/MS assay for reverse T3. Eliminates cross-reactivity with T4 and metabolites seen in immunoassay.",
                     "LC/MS-based reverse T3 provides superior analytical specificity over immunoassay by eliminating cross-reactivity with T4, T3, and other iodothyronines."),
  "t3-total":       ("Measures total T3 (triiodothyronine), the active thyroid hormone including both bound and free forms.",
                     "Total T3 quantification. Elevated in hyperthyroidism and T3 toxicosis; affected by thyroid-binding protein changes. Less useful than free T3 when protein abnormalities are present."),
  "t3-uptake":      ("Measures T3 uptake (THBR) — an indirect estimate of thyroid-binding protein capacity.",
                     "T3 resin uptake measures available binding sites on thyroid-binding proteins. Used to calculate the Free Thyroxine Index (FTI) when direct free T4 is unavailable."),
  "t4-total":       ("Measures total T4 (thyroxine), including protein-bound and free T4.",
                     "Total T4 reflects overall thyroxine production and protein binding capacity. Affected by changes in TBG (pregnancy, OCP use, liver disease, nephrotic syndrome)."),
  "t3-free":        ("Measures free T3, the biologically active unbound fraction of triiodothyronine.",
                     "Free T3 reflects metabolically active thyroid hormone. Elevated in hyperthyroidism and T3 toxicosis; may remain elevated after TSH normalizes during treatment."),
  "tg-antibody":    ("Screens for antibodies against thyroglobulin — a marker of autoimmune thyroid disease.",
                     "Anti-thyroglobulin antibodies are present in Hashimoto's thyroiditis and Graves' disease. They interfere with thyroglobulin measurements used for thyroid cancer surveillance post-thyroidectomy."),
  "tpo":            ("Tests for thyroid peroxidase antibodies — the most common marker of autoimmune thyroid disease (Hashimoto's).",
                     "TPO antibodies are present in >90% of Hashimoto's and ~75% of Graves' disease. Elevated TPO Ab predicts progression to overt hypothyroidism in subclinical hypothyroidism."),
  "transferrin":    ("Measures transferrin, the main iron-transport protein. Used in iron deficiency and iron overload evaluation.",
                     "Transferrin is the primary iron transport protein. Elevated in iron deficiency; decreased in inflammatory states, protein malnutrition, and liver disease."),
  "uric-acid":      ("Measures uric acid. Elevated levels can cause gout and are linked to kidney and cardiovascular risk.",
                     "Serum urate quantification. Hyperuricemia precipitates monosodium urate crystals in gout. Associated with hypertension, metabolic syndrome, and chronic kidney disease."),
  "urinalysis":     ("Examines urine for signs of kidney disease, infection, diabetes, and other conditions.",
                     "Dipstick and/or microscopic urinalysis. Screens for proteinuria, hematuria, glucosuria, ketonuria, nitrites, leukocyte esterase, and urinary casts."),
  "vita":           ("Measures vitamin A (retinol). Used to assess for deficiency or toxicity.",
                     "Serum retinol quantification. Deficiency causes night blindness and increased infection susceptibility; toxicity (hypervitaminosis A) can cause hepatotoxicity and teratogenicity."),
  "vitb1":          ("Measures thiamine (vitamin B1). Deficiency causes neurological disorders including Wernicke encephalopathy.",
                     "Whole blood thiamine as thiamine pyrophosphate (TPP). Deficiency impairs pyruvate dehydrogenase; causes Wernicke-Korsakoff syndrome, cardiomyopathy, and peripheral neuropathy."),
  "vitb2":          ("Measures riboflavin (vitamin B2). Important for energy metabolism and the activation of other B vitamins.",
                     "Riboflavin quantification. FAD/FMN-dependent enzyme cofactor in the electron transport chain; required for activation of B6 and folate. Deficiency causes stomatitis and seborrheic dermatitis."),
  "vitb6":          ("Measures vitamin B6 (pyridoxal-5-phosphate). Essential for amino acid metabolism and neurotransmitter synthesis.",
                     "Plasma PLP (pyridoxal-5-phosphate) quantification. Cofactor for >100 enzymatic reactions; deficiency causes peripheral neuropathy, sideroblastic anemia, and elevated homocysteine."),
  "zinc-rbc":       ("Measures zinc inside red blood cells — more sensitive to zinc deficiency than serum zinc.",
                     "RBC zinc reflects intracellular stores and is less affected by acute-phase responses than serum zinc. More sensitive marker of chronic zinc depletion."),
  "zinc-serum":     ("Measures zinc in blood. Used to assess zinc deficiency or overload.",
                     "Serum zinc quantification. Subject to diurnal variation and acute-phase response suppression. Used to screen for zinc deficiency in malabsorption, vegetarian diets, and chronic illness."),
  # Bundles
  "abo-rh":              ("Determines your ABO blood type and Rh factor (positive or negative).",
                          "ABO grouping and Rh typing by agglutination. Essential for pre-transfusion compatibility and prenatal Rh incompatibility evaluation."),
  "aldo-renin":          ("Measures aldosterone and plasma renin activity together — the gold standard screen for primary aldosteronism.",
                          "Aldosterone/plasma renin activity ratio is the primary screen for primary aldosteronism (Conn's syndrome), the most common cause of secondary hypertension."),
  "albumin-urine":       ("Tests for albumin in urine — an early, sensitive marker of kidney damage from diabetes or hypertension.",
                          "Urine albumin-to-creatinine ratio (ACR) is the preferred method for detecting early diabetic nephropathy and hypertensive nephropathy."),
  "anemia-panel":        ("Comprehensive panel evaluating the main causes of anemia — iron, B12, folate, and red cell indices.",
                          "Multi-analyte anemia workup differentiating nutritional (iron, B12, folate) from hemolytic and normochromic anemias using CBC, ferritin, iron/TIBC, B12, and folate."),
  "celiac":              ("Tests for antibodies associated with celiac disease, triggered by gluten ingestion.",
                          "Celiac disease antibody panel including tTG IgA, deamidated gliadin IgG, and total IgA to detect IgA deficiency that would cause false-negative tTG IgA results."),
  "ct-ng":               ("Tests for chlamydia and gonorrhea (the most common bacterial STIs) — and often trichomoniasis.",
                          "NAAT-based detection of Chlamydia trachomatis and Neisseria gonorrhoeae. Highly sensitive and specific; recommended first-line STI testing per CDC guidelines."),
  "comp-mens":           ("GoodLabs comprehensive men's health panel.",
                          "GoodLabs bundled comprehensive panel for men. See GoodLabs website for current included analytes."),
  "comp-womens":         ("GoodLabs comprehensive women's health panel.",
                          "GoodLabs bundled comprehensive panel for women. See GoodLabs website for current included analytes."),
  "dht-free":            ("Measures free dihydrotestosterone by equilibrium dialysis — the most accurate DHT method.",
                          "Free DHT by equilibrium dialysis/LC/MS. Equilibrium dialysis is the reference method for free hormone measurement; relevant in 5α-reductase activity evaluation."),
  "estrogens-frac":      ("Fractionated estrogen panel measuring E1, E2, and E3 separately using precise LC/MS.",
                          "Fractionated estrogens (estrone E1, estradiol E2, estriol E3) by LC/MS. Provides comprehensive estrogenic profile; used in HRT monitoring and menopausal assessment."),
  "fsh-lh":              ("Measures FSH and LH together — the paired gonadotropins for fertility and hormonal evaluation.",
                          "FSH and LH quantification in a single draw. Evaluates hypothalamic-pituitary-gonadal axis; used in fertility workup, menopause assessment, and hypogonadism diagnosis."),
  "full-monty":          ("GoodLabs comprehensive health panel covering a broad range of biomarkers.",
                          "GoodLabs 'Full Monty' bundle. Multi-system comprehensive assessment. See GoodLabs website for current included analytes."),
  "gtt":                 ("Two-hour oral glucose tolerance test — the diagnostic standard for gestational diabetes and prediabetes.",
                          "75g oral glucose load with 2-hour glucose per WHO protocol. Diagnostic for gestational diabetes mellitus, prediabetes, and impaired glucose tolerance."),
  "heart-health":        ("GoodLabs cardiovascular health panel.",
                          "GoodLabs Heart Health bundle. See GoodLabs website for current included analytes."),
  "heavy-metals":        ("Panel testing for multiple heavy metals (arsenic, lead, mercury, cadmium) in a single draw.",
                          "Multi-element heavy metals panel by ICP-MS. Screens for toxic metal accumulation from environmental, occupational, or dietary sources."),
  "hb-frac":             ("Tests for hemoglobin variants (sickle cell, thalassemia) using HPLC fractionation.",
                          "Hemoglobinopathy fractionation by HPLC identifies and quantifies hemoglobin variants (HbA, HbA2, HbF, HbS, HbC, etc.) for sickle cell and thalassemia diagnosis."),
  "hiv":                 ("Tests for HIV using the fourth-generation antigen/antibody assay — the most sensitive available.",
                          "Fourth-generation HIV combo assay detects p24 antigen and HIV-1/2 antibodies, reducing the window period to 18–45 days post-exposure. Reactive results require confirmatory testing."),
  "iron-tibc":           ("Tests iron and total iron binding capacity (TIBC) together — without ferritin.",
                          "Iron and TIBC panel quantifying serum iron, TIBC, and transferrin saturation. Does not include ferritin; see the 'iron' ID for the full panel including ferritin."),
  "mens-hormone":        ("GoodLabs men's hormone panel.",
                          "GoodLabs Men's Hormone bundle. See GoodLabs website for current included analytes."),
  "metabolic-health":    ("GoodLabs metabolic health panel.",
                          "GoodLabs Metabolic Health bundle. See GoodLabs website for current included analytes."),
  "nmr-lipo":            ("Measures lipoprotein particle number and size by NMR — more detail than a standard cholesterol panel.",
                          "NMR LipoProfile measures LDL particle number (LDL-P), HDL-P, and particle size. LDL-P is a more accurate cardiovascular risk predictor than LDL-C in some populations."),
  "nutrient-panel":      ("GoodLabs nutrient panel.",
                          "GoodLabs Nutrient bundle. See GoodLabs website for current included analytes."),
  "omegacheck":          ("Measures omega-3 fatty acids in red blood cells (the Omega-3 Index). Target >8% is associated with lower cardiovascular risk.",
                          "OmegaCheck measures EPA and DHA as a percentage of total RBC fatty acids (Omega-3 Index). Levels >8% are associated with reduced sudden cardiac death risk."),
  "ogtt":                ("Extended glucose and insulin tolerance test with 4 blood draws over 2 hours.",
                          "Four-specimen OGTT with insulin measurements assesses insulin secretion dynamics, insulin resistance, and glucose tolerance. Used in functional and advanced metabolic workup."),
  "prolactin-total":     ("Measures total prolactin including all molecular forms — used to rule out macroprolactinemia.",
                          "Total and monomeric prolactin fractionation distinguishes true hyperprolactinemia from macroprolactinemia (biologically inactive large complexes), which can cause spuriously elevated total prolactin."),
  "psa-free":            ("Total PSA with free-to-total ratio — helps distinguish benign prostate changes from cancer in the PSA gray zone.",
                          "PSA total with free percentage. Free/total PSA <10–15% in the 4–10 ng/mL gray zone is associated with higher prostate cancer probability and guides biopsy decisions."),
  "pt-inr":              ("Measures prothrombin time and INR — standard for evaluating blood clotting and monitoring warfarin.",
                          "PT with INR evaluates the extrinsic coagulation pathway. INR standardizes PT ratios for warfarin monitoring and coagulopathy severity assessment."),
  "reticulocyte":        ("Counts immature red blood cells (reticulocytes) to assess bone marrow activity.",
                          "Reticulocyte count reflects erythropoietic activity. Elevated in hemolytic anemia and blood loss; low in aplastic anemia and nutritional deficiencies with impaired erythropoiesis."),
  "std-screening":       ("GoodLabs STD screening bundle.",
                          "GoodLabs STD Screening bundle. See GoodLabs website for current included tests."),
  "test-free-total":     ("Measures free and total testosterone together by LC/MS.",
                          "Combined free and total testosterone by mass spectrometry. Provides both total testosterone and directly measured free fraction for comprehensive androgen assessment."),
  "test-free-bio-total": ("Free, bioavailable, and total testosterone — the most complete testosterone panel available.",
                          "Free, bioavailable, and total testosterone by equilibrium dialysis and LC/MS. Most complete picture of androgenic status, accounting for both albumin-bound and free fractions."),
  "test-calc-shbg":      ("Measures total testosterone, SHBG, and albumin to calculate free testosterone.",
                          "Total testosterone, SHBG, and albumin to calculate free testosterone via the Vermeulen equation. Cost-effective alternative to direct free testosterone measurement."),
  "ttg":                 ("Tests for tissue transglutaminase antibodies (IgA and IgG) — the most sensitive celiac antibody test.",
                          "tTG IgA has >95% sensitivity for celiac disease; tTG IgG covers IgA-deficient patients. Together they form the cornerstone of celiac serological evaluation."),
  "thyroid-panel":       ("GoodLabs thyroid panel.",
                          "GoodLabs Thyroid bundle. See GoodLabs website for current included analytes."),
  "womens-hormone":      ("GoodLabs women's hormone panel.",
                          "GoodLabs Women's Hormone bundle. See GoodLabs website for current included analytes."),
  "body-builder":        ("GoodLabs performance and athlete-focused panel.",
                          "GoodLabs Body Builder Panel. See GoodLabs website for current included analytes."),
}

# ── Display names, canonical names, categories, biomarkers ───────────────────
# Existing 19 — preserved from labTests.ts
EXISTING_META = {
  "cbc":        {"canon":"Complete Blood Count","display":"Complete Blood Count (CBC)","cat":"General",
    "bio":["WBC (White Blood Cells)","RBC (Red Blood Cells)","Hemoglobin","Hematocrit","MCV","MCH","MCHC","Platelets","Neutrophils","Lymphocytes","Monocytes","Eosinophils","Basophils"],
    "notes":None},
  "cmp":        {"canon":"Comprehensive Metabolic Panel","display":"Comprehensive Metabolic Panel (CMP)","cat":"General",
    "bio":["Glucose","BUN (Blood Urea Nitrogen)","Creatinine","eGFR","Sodium","Potassium","CO2 (Bicarbonate)","Chloride","Calcium","Total Protein","Albumin","Total Bilirubin","ALT (Alanine Aminotransferase)","AST (Aspartate Aminotransferase)","ALP (Alkaline Phosphatase)"],
    "notes":None},
  "lipid":      {"canon":"Lipid Panel","display":"Lipid Panel","cat":"Cardio / Metabolic",
    "bio":["Total Cholesterol","LDL Cholesterol","HDL Cholesterol","Triglycerides","VLDL Cholesterol"],"notes":None},
  "a1c":        {"canon":"Hemoglobin A1c","display":"Hemoglobin A1c","cat":"Cardio / Metabolic",
    "bio":["Hemoglobin A1c (%)","Estimated Average Glucose (eAG)"],"notes":None},
  "crp":        {"canon":"C-Reactive Protein","display":"C-Reactive Protein (CRP)","cat":"Cardio / Metabolic",
    "bio":["C-Reactive Protein (mg/L)"],
    "notes":"hsCRP preferred for cardiovascular risk; standard CRP for acute inflammation. Confirm assay type when scraping — these are often listed as separate SKUs."},
  "insulin":    {"canon":"Insulin, Fasting","display":"Insulin (Fasting)","cat":"Cardio / Metabolic",
    "bio":["Serum Insulin (uIU/mL)"],"notes":"Must be fasting. Some providers bundle with glucose for HOMA-IR."},
  "lpa":        {"canon":"Lipoprotein(a)","display":"Lipoprotein(a)","cat":"Cardio / Metabolic",
    "bio":["Lipoprotein(a) (mg/dL or nmol/L)"],
    "notes":"Units vary by lab — mg/dL vs nmol/L. Results are not interchangeable. Normalize units during scraping."},
  "apob":       {"canon":"Apolipoprotein B","display":"Apolipoprotein B (ApoB)","cat":"Cardio / Metabolic",
    "bio":["Apolipoprotein B (mg/dL)"],"notes":None},
  "tsh":        {"canon":"Thyroid Stimulating Hormone","display":"TSH","cat":"Thyroid",
    "bio":["TSH (mIU/L)"],"notes":None},
  "ft4":        {"canon":"Free Thyroxine","display":"Free T4","cat":"Thyroid",
    "bio":["Free T4 (ng/dL)"],"notes":None},
  "vitd":       {"canon":"Vitamin D, 25-Hydroxyvitamin D","display":"Vitamin D, 25-OH","cat":"Vitamins",
    "bio":["25-Hydroxyvitamin D, Total (ng/mL)"],
    "notes":"Some labs report D2 and D3 separately. Confirm total vs. fractionated reporting when scraping."},
  "b12":        {"canon":"Vitamin B12","display":"Vitamin B12","cat":"Vitamins",
    "bio":["Vitamin B12 / Cobalamin (pg/mL)"],"notes":None},
  "ferritin":   {"canon":"Ferritin","display":"Ferritin","cat":"Iron",
    "bio":["Serum Ferritin (ng/mL)"],"notes":None},
  "iron":       {"canon":"Iron and Total Iron Binding Capacity","display":"Iron / TIBC Panel","cat":"Iron",
    "bio":["Serum Iron (mcg/dL)","TIBC — Total Iron Binding Capacity (mcg/dL)","UIBC — Unsaturated Iron Binding Capacity","Transferrin Saturation (%)"],"notes":None},
  "total-test": {"canon":"Testosterone, Total","display":"Testosterone, Total","cat":"Hormones",
    "bio":["Total Testosterone (ng/dL)"],"notes":"LC-MS/MS is more accurate at low levels. Confirm assay method when scraping."},
  "free-test":  {"canon":"Testosterone, Free","display":"Testosterone, Free","cat":"Hormones",
    "bio":["Free Testosterone (pg/mL)","Total Testosterone (ng/dL)"],
    "notes":"Calculated free T uses albumin and SHBG; equilibrium dialysis is the gold standard. Clarify method when scraping."},
  "estradiol":  {"canon":"Estradiol","display":"Estradiol (Sensitive)","cat":"Hormones",
    "bio":["Estradiol / E2 (pg/mL)"],
    "notes":"Sensitive LC-MS/MS preferred for men and low-level female monitoring. Immunoassay is inaccurate at low concentrations. Flag assay type when scraping."},
  "shbg":       {"canon":"Sex Hormone Binding Globulin","display":"SHBG","cat":"Hormones",
    "bio":["SHBG (nmol/L)"],"notes":None},
  "psa":        {"canon":"Prostate-Specific Antigen, Total","display":"PSA","cat":"Men's Health",
    "bio":["PSA, Total (ng/mL)"],
    "notes":"Free PSA ratio can improve specificity. Some providers list PSA + Free PSA as a bundle — note both when scraping."},
}

# Category mapping for new tests
CATS = {
  "acth":"Hormones","aluminum":"Heavy Metals","amylase":"Digestive",
  "ana":"Autoimmune","androstenedione":"Hormones","amh":"Hormones",
  "arsenic":"Heavy Metals","c-peptide":"Cardio / Metabolic","ceruloplasmin":"Minerals",
  "coq10":"Vitamins","copper":"Minerals","cortisol":"Hormones",
  "cortisol-lcms":"Hormones","ck":"Cardio / Metabolic","crp-standard":"Inflammation",
  "cystatin-c":"Kidney","dhea-s":"Hormones","dht":"Hormones",
  "estradiol-lcms":"Hormones","estrogens-total":"Hormones","estrone":"Hormones",
  "fibrinogen":"Inflammation","folate-rbc":"Vitamins","folate-serum":"Vitamins",
  "fructosamine":"Cardio / Metabolic","fsh":"Hormones","gastrin":"Digestive",
  "ggt":"Liver","glucose":"Cardio / Metabolic","gh":"Hormones",
  "hemoglobin":"General","hep-c":"Infectious Disease","homocysteine":"Cardio / Metabolic",
  "iga":"Immune","inhibin-b":"Hormones","igf1":"Hormones",
  "il1b":"Inflammation","il6":"Inflammation","iodine-urine":"Thyroid",
  "iodine-serum":"Thyroid","ldl-direct":"Cardio / Metabolic","lead":"Heavy Metals",
  "leptin":"Hormones","lh":"Hormones","lipase":"Digestive",
  "lp-pla2":"Cardio / Metabolic","magnesium-rbc":"Minerals","mercury":"Heavy Metals",
  "methylmalonic":"Vitamins","methylmalonic-s":"Vitamins","molybdenum":"Minerals",
  "mthfr":"Genetics","nt-probnp":"Cardio / Metabolic","oxldl":"Cardio / Metabolic",
  "pregnenolone":"Hormones","progesterone":"Hormones","progesterone-lcms":"Hormones",
  "prolactin":"Hormones","pth":"Bone / Mineral","rbc-copper":"Minerals",
  "reverse-t3":"Thyroid","rf":"Autoimmune","rpr":"Infectious Disease",
  "esr":"Inflammation","selenium":"Minerals","serum-amyloid-a":"Inflammation",
  "t3-reverse-lcms":"Thyroid","t3-total":"Thyroid","t3-uptake":"Thyroid",
  "t4-total":"Thyroid","t3-free":"Thyroid","tg-antibody":"Thyroid",
  "tpo":"Thyroid","transferrin":"Iron","uric-acid":"Cardio / Metabolic",
  "urinalysis":"General","vita":"Vitamins","vitb1":"Vitamins",
  "vitb2":"Vitamins","vitb6":"Vitamins","zinc-rbc":"Minerals","zinc-serum":"Minerals",
  # bundles
  "abo-rh":"General","aldo-renin":"Cardio / Metabolic","albumin-urine":"Kidney",
  "anemia-panel":"Bundle Panels","celiac":"Bundle Panels","ct-ng":"Bundle Panels",
  "comp-mens":"Bundle Panels","comp-womens":"Bundle Panels","dht-free":"Bundle Panels",
  "estrogens-frac":"Bundle Panels","fsh-lh":"Bundle Panels","full-monty":"Bundle Panels",
  "gtt":"Bundle Panels","heart-health":"Bundle Panels","heavy-metals":"Bundle Panels",
  "hb-frac":"Bundle Panels","hiv":"Bundle Panels","iron-tibc":"Iron",
  "mens-hormone":"Bundle Panels","metabolic-health":"Bundle Panels","nmr-lipo":"Cardio / Metabolic",
  "nutrient-panel":"Bundle Panels","omegacheck":"Bundle Panels","ogtt":"Bundle Panels",
  "prolactin-total":"Hormones","psa-free":"Men's Health","pt-inr":"Bundle Panels",
  "reticulocyte":"General","std-screening":"Bundle Panels","test-free-total":"Hormones",
  "test-free-bio-total":"Hormones","test-calc-shbg":"Hormones","ttg":"Bundle Panels",
  "thyroid-panel":"Bundle Panels","womens-hormone":"Bundle Panels","body-builder":"Bundle Panels",
}

# ── Helpers ───────────────────────────────────────────────────────────────────
QUEST_BASE   = "https://www.questhealth.com/shop-tests"
GL_BASE      = "https://app.hellogoodlabs.com/book-tests"
LAST_VERIFIED = "2026-03-12"

def price_val(v):
    if v is None:
        return "null"
    return str(v)

def ts_str(s):
    if s is None:
        return "null"
    return json.dumps(s)

def ts_arr(lst):
    if not lst:
        return "[]"
    items = ",\n      ".join(json.dumps(x) for x in lst)
    return f"[\n      {items},\n    ]"

def render_test(tid, is_bundle=False):
    names = PROVIDER_NAMES[tid]
    qname = names.get("quest")
    lname = names.get("labcorp")
    gname = names.get("goodlabs")

    # Prices
    qprice = QUEST_PRICES.get(qname) if qname else None
    ldata  = LABCORP_DATA.get(lname) if lname else None
    lprice = ldata["price"] if ldata else None
    gprice = GL_PRICES.get(tid)

    # Order URLs
    quest_url  = QUEST_BASE if qprice is not None else None
    lc_url     = (LC_BASE + ldata["path"]) if ldata else None
    gl_url     = GL_BASE if gprice is not None else None

    # Meta
    if tid in EXISTING_META:
        m = EXISTING_META[tid]
        canon   = m["canon"]
        display = m["display"]
        cat     = m["cat"]
        bio     = m["bio"]
        notes   = m["notes"]
    else:
        from_gl = {**NEW_IND, **BUNDLES_GL}.get(tid, {})
        gl_name = from_gl.get("name", tid)
        canon   = gl_name
        display = gl_name
        cat     = CATS.get(tid, "General")
        bio     = []
        notes   = None

    alts  = ALT_NAMES.get(tid, [])
    plain, medical = DESCS.get(tid, ("", ""))

    # Build pricing block
    plines = []
    plines.append(f"quest: {price_val(qprice)}")
    plines.append(f"labcorp: {price_val(lprice)}")
    plines.append(f"goodlabs: {price_val(gprice)}")
    pricing_str = ",\n      ".join(plines)

    # Build orderUrls block
    url_parts = []
    if quest_url:  url_parts.append(f"quest: {json.dumps(quest_url)}")
    if lc_url:     url_parts.append(f"labcorp: {json.dumps(lc_url)}")
    if gl_url:     url_parts.append(f"goodlabs: {json.dumps(gl_url)}")
    order_urls = "{ " + ", ".join(url_parts) + " }" if url_parts else "{}"

    bio_str = ts_arr(bio)
    alt_str = ts_arr(alts)

    lines = [f"  {{"]
    lines.append(f"    id: {json.dumps(tid)},")
    lines.append(f"    canonicalName: {json.dumps(canon)},")
    lines.append(f"    displayName: {json.dumps(display)},")
    lines.append(f"    category: {json.dumps(cat)},")
    lines.append(f"    alternateNames: {alt_str},")
    lines.append(f"    biomarkers: {bio_str},")
    lines.append(f"    plainDescription: {json.dumps(plain)},")
    lines.append(f"    medicalDescription: {json.dumps(medical)},")
    lines.append(f"    pricing: {{ {pricing_str} }},")
    lines.append(f"    orderUrls: {order_urls},")
    lines.append(f"    lastVerified: {json.dumps(LAST_VERIFIED)},")
    if is_bundle:
        lines.append(f"    bundle: true,")
    if notes:
        lines.append(f"    notes: {json.dumps(notes)},")
    lines.append(f"  }},")
    return "\n".join(lines)

# ── Emit TypeScript ───────────────────────────────────────────────────────────
print('''\
/**
 * LabRecon Reference Data
 *
 * Canonical test catalog and provider list.
 * Pricing is live scraped data — Quest and LabCorp verified 2026-03-12.
 * GoodLabs prices verified 2026-03-12 via manual capture (goodlabs-catalog-data.py).
 *
 * pricing values:
 *   number  = confirmed price in USD
 *   null    = provider confirmed to not offer this test as a standalone
 *   omitted = not yet scraped (legacy; all entries now explicit)
 *
 * orderUrls:
 *   Quest — no per-product deep links available from tile scrape; base catalog URL used.
 *   LabCorp — individual product page URLs scraped 2026-03-12.
 *   GoodLabs — base booking URL used (no per-product URLs captured).
 */

// ── Types ─────────────────────────────────────────────────────────────────

export type Provider = {
  id: string;
  label: string;
  consumerUrl: string;
  active: boolean;
  alternateLabels: string[];
  scrapeUrl?: string;
};

export type LabTest = {
  /** Stable internal ID */
  id: string;
  /** Normalized canonical name for cross-provider matching */
  canonicalName: string;
  /** UI display name */
  displayName: string;
  /** Category for grouping in the comparison table */
  category: string;
  /** Provider-specific alternate names — used for scraper normalization */
  alternateNames: string[];
  /** Individual analytes / biomarkers included */
  biomarkers: string[];
  /** Plain English description — no medical claims */
  plainDescription: string;
  /** Technical/clinical description for informed users */
  medicalDescription: string;
  /**
   * Cash-pay pricing by provider ID.
   * null  = provider does not offer this test as a standalone product.
   * UI should display "Not available" when value is null.
   */
  pricing: Partial<Record<string, number | null>>;
  /** Direct order page URLs by provider ID */
  orderUrls?: Partial<Record<string, string>>;
  /** ISO date string of last price verification */
  lastVerified: string;
  /** True if this entry represents a multi-biomarker bundle panel */
  bundle?: boolean;
  /** Ordering or scraping notes */
  notes?: string;
};

// ── Providers ─────────────────────────────────────────────────────────────

export const providers: Provider[] = [
  {
    id: "quest",
    label: "Quest",
    consumerUrl: "https://www.questhealth.com/shop-tests",
    active: true,
    alternateLabels: ["Quest Health", "Quest Diagnostics", "QuestDirect"],
  },
  {
    id: "labcorp",
    label: "LabCorp",
    consumerUrl: "https://www.ondemand.labcorp.com/products",
    active: true,
    alternateLabels: ["Labcorp OnDemand", "Labcorp", "Laboratory Corporation"],
  },
  {
    id: "goodlabs",
    label: "GoodLabs",
    consumerUrl: "https://app.hellogoodlabs.com/book-tests",
    active: true,
    alternateLabels: ["GoodLabs"],
  },
  {
    id: "walkinlab",
    label: "Walk-In Lab",
    consumerUrl: "https://www.walkinlab.com",
    active: false,
    alternateLabels: ["Walk-In Lab", "WalkInLab"],
  },
  {
    id: "requestatest",
    label: "Request A Test",
    consumerUrl: "https://www.requestatest.com",
    active: false,
    alternateLabels: ["Request A Test", "RequestATest"],
  },
  {
    id: "healthlabs",
    label: "HealthLabs",
    consumerUrl: "https://www.healthlabs.com",
    active: false,
    alternateLabels: ["HealthLabs.com", "HealthLabs"],
  },
  {
    id: "privatemd",
    label: "Private MD Labs",
    consumerUrl: "https://www.privatemdlabs.com",
    active: false,
    alternateLabels: ["Private MD Labs", "PrivateMDLabs", "PrivateMD"],
  },
];

/** Providers currently shown in the comparison table UI */
export const activeProviders = providers.filter((p) => p.active);

// ── Test Catalog ──────────────────────────────────────────────────────────
// pricing: null = not available as standalone at this provider
// orderUrls: Quest uses base catalog URL (no individual product deep links from tile scrape)
''')

# Determine ordering: original 19, then individual new, then bundles
ORIG_19 = list(EXISTING_META.keys())
BUNDLE_IDS = set(BUNDLES_GL.keys())
IND_IDS = [tid for tid in PROVIDER_NAMES if tid not in ORIG_19 and tid not in BUNDLE_IDS]

# Group individual tests by category for section headers
from collections import defaultdict
ind_by_cat = defaultdict(list)
for tid in IND_IDS:
    ind_by_cat[CATS.get(tid,"General")].append(tid)

print("export const labTests: LabTest[] = [")

# Original 19
print("  // ── Original 19 ──────────────────────────────────────────────────────")
for tid in ORIG_19:
    print(render_test(tid))

# New individual tests by category
CAT_ORDER = [
    "General","Cardio / Metabolic","Thyroid","Vitamins","Iron","Hormones",
    "Men's Health","Minerals","Heavy Metals","Autoimmune","Inflammation",
    "Kidney","Liver","Digestive","Infectious Disease","Immune",
    "Bone / Mineral","Genetics",
]
seen = set(ORIG_19)
for cat in CAT_ORDER:
    tids = [t for t in ind_by_cat.get(cat,[]) if t not in seen]
    if not tids: continue
    label = cat.upper()
    print(f"\n  // ── {label} ─────────────────────────────────────────────────────────")
    for tid in tids:
        print(render_test(tid))
        seen.add(tid)
# any uncategorized
leftover = [t for t in IND_IDS if t not in seen]
if leftover:
    print("\n  // ── OTHER ───────────────────────────────────────────────────────────")
    for tid in leftover:
        print(render_test(tid))

# Bundles
print("\n  // ── BUNDLE PANELS ───────────────────────────────────────────────────")
for tid in BUNDLES_GL:
    if tid in PROVIDER_NAMES:
        print(render_test(tid, is_bundle=True))

print("];")
