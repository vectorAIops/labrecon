/**
 * LabRecon Reference Data
 *
 * Canonical test catalog and provider list.
 * Pricing values are estimated placeholder data.
 * Replace with scraped values once the live data pipeline is built.
 *
 * Structure is designed to support future provider normalization,
 * test name matching across sources, and scraper configuration.
 */

// ── Types ─────────────────────────────────────────────────────────────────

export type Provider = {
  /** Internal key — matches keys in LabTest.pricing */
  id: string;
  /** Display name shown in the UI */
  label: string;
  /** Consumer-facing ordering URL — verify before scraping */
  consumerUrl: string;
  /** Whether live pricing data is available for UI display */
  active: boolean;
  /** Names this provider uses internally — for scrape result matching */
  alternateLabels: string[];
  /** Scrape target URL — fill in when implementing the scraper */
  scrapeUrl?: string;
};

export type LabTest = {
  /** Stable internal ID — used in slugs and as a pricing map key */
  id: string;
  /** Normalized canonical name for cross-provider matching */
  canonicalName: string;
  /** UI display name */
  displayName: string;
  /** Category for grouping in the comparison table */
  category: string;
  /** Names other providers use for this test — for scraper normalization */
  alternateNames: string[];
  /** Individual analytes / biomarkers included in the panel */
  biomarkers: string[];
  /** Plain English — describes what it measures, no medical claims */
  plainDescription: string;
  /** Technical/clinical description for informed users */
  medicalDescription: string;
  /** Estimated cash-pay pricing by provider ID. undefined = not yet scraped */
  pricing: Partial<Record<string, number>>;
  /** Ordering or scraping notes — clarifications for future implementation */
  notes?: string;
};

// ── Providers ─────────────────────────────────────────────────────────────
// active: true  → live pricing shown in the comparison UI
// active: false → placeholder reference for future scraping

export const providers: Provider[] = [
  {
    id: "quest",
    label: "Quest",
    consumerUrl: "https://www.questhealth.com", // verify before scraping
    active: true,
    alternateLabels: ["Quest Health", "Quest Diagnostics", "QuestDirect"],
  },
  {
    id: "labcorp",
    label: "LabCorp",
    consumerUrl: "https://www.labcorpondemand.com", // verify before scraping
    active: true,
    alternateLabels: ["Labcorp OnDemand", "Labcorp", "Laboratory Corporation"],
  },
  {
    id: "goodlabs",
    label: "GoodLabs",
    consumerUrl: "", // fill in when confirmed
    active: true,
    alternateLabels: ["GoodLabs"],
  },
  {
    id: "walkinlab",
    label: "Walk-In Lab",
    consumerUrl: "https://www.walkinlab.com", // verify before scraping
    active: false,
    alternateLabels: ["Walk-In Lab", "WalkInLab"],
  },
  {
    id: "requestatest",
    label: "Request A Test",
    consumerUrl: "https://www.requestatest.com", // verify before scraping
    active: false,
    alternateLabels: ["Request A Test", "RequestATest"],
  },
  {
    id: "healthlabs",
    label: "HealthLabs",
    consumerUrl: "https://www.healthlabs.com", // verify before scraping
    active: false,
    alternateLabels: ["HealthLabs.com", "HealthLabs"],
  },
  {
    id: "privatemd",
    label: "Private MD Labs",
    consumerUrl: "https://www.privatemdlabs.com", // verify before scraping
    active: false,
    alternateLabels: ["Private MD Labs", "PrivateMDLabs", "PrivateMD"],
  },
];

/** Providers currently shown in the comparison table UI */
export const activeProviders = providers.filter((p) => p.active);

// ── Test Catalog ──────────────────────────────────────────────────────────
// Add new tests here. Pricing is placeholder until scraping is live.
// Keep alternateNames accurate — these are used to match test names
// across provider websites during scraping.

export const labTests: LabTest[] = [
  // ── General ──────────────────────────────────────────────────────────
  {
    id: "cbc",
    canonicalName: "Complete Blood Count",
    displayName: "Complete Blood Count (CBC)",
    category: "General",
    alternateNames: [
      "CBC",
      "CBC with Differential",
      "CBC w/ Diff",
      "Complete Blood Count with Differential",
    ],
    biomarkers: [
      "WBC (White Blood Cells)",
      "RBC (Red Blood Cells)",
      "Hemoglobin",
      "Hematocrit",
      "MCV",
      "MCH",
      "MCHC",
      "Platelets",
      "Neutrophils",
      "Lymphocytes",
      "Monocytes",
      "Eosinophils",
      "Basophils",
    ],
    plainDescription:
      "Counts and measures your red blood cells, white blood cells, and platelets. One of the most routinely ordered panels in medicine.",
    medicalDescription:
      "Complete cellular evaluation of peripheral blood. Screens for anemia, infection, inflammation, polycythemia, and platelet disorders.",
    pricing: { quest: 39, labcorp: 35, goodlabs: 28 },
  },
  {
    id: "cmp",
    canonicalName: "Comprehensive Metabolic Panel",
    displayName: "Comprehensive Metabolic Panel (CMP)",
    category: "General",
    alternateNames: [
      "CMP",
      "Complete Metabolic Panel",
      "Chemistry Panel",
      "14-Panel Chemistry",
    ],
    biomarkers: [
      "Glucose",
      "BUN (Blood Urea Nitrogen)",
      "Creatinine",
      "eGFR",
      "Sodium",
      "Potassium",
      "CO2 (Bicarbonate)",
      "Chloride",
      "Calcium",
      "Total Protein",
      "Albumin",
      "Total Bilirubin",
      "ALT (Alanine Aminotransferase)",
      "AST (Aspartate Aminotransferase)",
      "ALP (Alkaline Phosphatase)",
    ],
    plainDescription:
      "A 14-marker snapshot of your metabolic health — blood sugar, kidney function, liver enzymes, and electrolytes.",
    medicalDescription:
      "14-panel metabolic assessment covering renal function, hepatic enzymes, glucose metabolism, and fluid/electrolyte balance.",
    pricing: { quest: 49, labcorp: 42, goodlabs: 31 },
  },

  // ── Cardio / Metabolic ────────────────────────────────────────────────
  {
    id: "lipid",
    canonicalName: "Lipid Panel",
    displayName: "Lipid Panel",
    category: "Cardio / Metabolic",
    alternateNames: ["Lipid Panel", "Cholesterol Panel", "Lipid Profile"],
    biomarkers: [
      "Total Cholesterol",
      "LDL Cholesterol",
      "HDL Cholesterol",
      "Triglycerides",
      "VLDL Cholesterol",
    ],
    plainDescription:
      "Measures cholesterol and triglycerides. Standard for assessing cardiovascular health.",
    medicalDescription:
      "Quantification of serum lipid fractions. Primary screen for dyslipidemia and cardiovascular risk.",
    pricing: { quest: 42, labcorp: 39, goodlabs: 26 },
  },
  {
    id: "a1c",
    canonicalName: "Hemoglobin A1c",
    displayName: "Hemoglobin A1c",
    category: "Cardio / Metabolic",
    alternateNames: [
      "HbA1c",
      "A1c",
      "Glycosylated Hemoglobin",
      "Glycated Hemoglobin",
      "Hemoglobin A1C",
    ],
    biomarkers: ["Hemoglobin A1c (%)", "Estimated Average Glucose (eAG)"],
    plainDescription:
      "Shows your average blood sugar over the past 2–3 months. A better picture than a single glucose reading.",
    medicalDescription:
      "Percentage of glycated hemoglobin. Standard marker for screening and monitoring glycemic control in prediabetes and diabetes.",
    pricing: { quest: 34, labcorp: 31, goodlabs: 24 },
  },
  {
    id: "crp",
    canonicalName: "C-Reactive Protein",
    displayName: "C-Reactive Protein (CRP)",
    category: "Cardio / Metabolic",
    alternateNames: [
      "CRP",
      "hsCRP",
      "High-Sensitivity CRP",
      "hs-CRP",
      "C-Reactive Protein, High Sensitivity",
    ],
    biomarkers: ["C-Reactive Protein (mg/L)"],
    plainDescription:
      "Measures inflammation in the body. Used for tracking inflammatory status and cardiovascular risk assessment.",
    medicalDescription:
      "Acute-phase reactant synthesized by the liver in response to cytokine signaling. High-sensitivity CRP (hsCRP) is used in cardiovascular risk stratification.",
    pricing: { quest: 29, labcorp: 27, goodlabs: 19 },
    notes:
      "hsCRP preferred for cardiovascular risk; standard CRP for acute inflammation. Confirm assay type when scraping — these are often listed as separate SKUs.",
  },
  {
    id: "insulin",
    canonicalName: "Insulin, Fasting",
    displayName: "Insulin (Fasting)",
    category: "Cardio / Metabolic",
    alternateNames: ["Insulin", "Fasting Insulin", "Serum Insulin"],
    biomarkers: ["Serum Insulin (uIU/mL)"],
    plainDescription:
      "Measures insulin levels. Best done fasting. Useful for tracking insulin resistance.",
    medicalDescription:
      "Fasting serum insulin quantification. Used to calculate HOMA-IR and evaluate pancreatic beta-cell function.",
    pricing: { quest: 35, labcorp: 32, goodlabs: 24 },
    notes: "Must be fasting. Some providers bundle with glucose for HOMA-IR.",
  },
  {
    id: "lpa",
    canonicalName: "Lipoprotein(a)",
    displayName: "Lipoprotein(a)",
    category: "Cardio / Metabolic",
    alternateNames: ["Lp(a)", "Lipoprotein a", "Lipoprotein-a", "Lp(a) Particle"],
    biomarkers: ["Lipoprotein(a) (mg/dL or nmol/L)"],
    plainDescription:
      "Measures a specific atherogenic lipoprotein particle linked to heart disease. Levels are largely genetic and not significantly changed by diet.",
    medicalDescription:
      "Quantification of lipoprotein(a), an LDL-like particle with Apo(a). An independent, largely genetically determined cardiovascular risk factor.",
    pricing: { quest: 55, labcorp: 51, goodlabs: 38 },
    notes:
      "Units vary by lab — mg/dL vs nmol/L. Results are not interchangeable. Normalize units during scraping.",
  },
  {
    id: "apob",
    canonicalName: "Apolipoprotein B",
    displayName: "Apolipoprotein B (ApoB)",
    category: "Cardio / Metabolic",
    alternateNames: ["ApoB", "Apo B", "Apolipoprotein B-100"],
    biomarkers: ["Apolipoprotein B (mg/dL)"],
    plainDescription:
      "Counts the total number of atherogenic lipoprotein particles. Many consider it a more accurate cardiovascular risk marker than LDL cholesterol alone.",
    medicalDescription:
      "Measures total apolipoprotein B, present on all atherogenic lipoproteins (LDL, IDL, VLDL, Lp(a)). Reflects total particle burden; increasingly used in cardiovascular risk stratification.",
    pricing: { quest: 39, labcorp: 36, goodlabs: 27 },
  },

  // ── Thyroid ───────────────────────────────────────────────────────────
  {
    id: "tsh",
    canonicalName: "Thyroid Stimulating Hormone",
    displayName: "TSH",
    category: "Thyroid",
    alternateNames: ["TSH", "Thyroid Stimulating Hormone", "Thyrotropin"],
    biomarkers: ["TSH (mIU/L)"],
    plainDescription:
      "Checks how well your thyroid is functioning. Usually the first thyroid test ordered.",
    medicalDescription:
      "Third-generation immunometric assay for thyroid-stimulating hormone. Primary screen for hypothyroidism and hyperthyroidism.",
    pricing: { quest: 44, labcorp: 41, goodlabs: 29 },
  },
  {
    id: "ft4",
    canonicalName: "Free Thyroxine",
    displayName: "Free T4",
    category: "Thyroid",
    alternateNames: [
      "Free T4",
      "FT4",
      "Free Thyroxine",
      "Thyroxine, Free",
      "T4 Free",
    ],
    biomarkers: ["Free T4 (ng/dL)"],
    plainDescription:
      "Measures the active thyroid hormone circulating freely in the blood. Often ordered alongside TSH.",
    medicalDescription:
      "Immunoassay for unbound thyroxine (T4). Used with TSH to differentiate primary from secondary thyroid dysfunction and guide levothyroxine dosing.",
    pricing: { quest: 47, labcorp: 44, goodlabs: 30 },
  },

  // ── Vitamins ──────────────────────────────────────────────────────────
  {
    id: "vitd",
    canonicalName: "Vitamin D, 25-Hydroxyvitamin D",
    displayName: "Vitamin D, 25-OH",
    category: "Vitamins",
    alternateNames: [
      "Vitamin D",
      "25-OH Vitamin D",
      "25-Hydroxyvitamin D",
      "Vitamin D, 25-Hydroxy",
      "Calcidiol",
    ],
    biomarkers: ["25-Hydroxyvitamin D, Total (ng/mL)"],
    plainDescription:
      "Checks your vitamin D status. One of the most common nutrient deficiencies in adults.",
    medicalDescription:
      "Measures serum 25-hydroxyvitamin D, the primary circulating form and standard clinical marker for vitamin D sufficiency.",
    pricing: { quest: 69, labcorp: 61, goodlabs: 45 },
    notes:
      "Some labs report D2 and D3 separately. Confirm total vs. fractionated reporting when scraping.",
  },
  {
    id: "b12",
    canonicalName: "Vitamin B12",
    displayName: "Vitamin B12",
    category: "Vitamins",
    alternateNames: ["B12", "Vitamin B12", "Cobalamin", "Cyanocobalamin"],
    biomarkers: ["Vitamin B12 / Cobalamin (pg/mL)"],
    plainDescription:
      "Measures B12, important for nerve function, energy production, and red blood cell formation.",
    medicalDescription:
      "Serum cobalamin quantification. Used to evaluate B12 deficiency, macrocytic anemia, and peripheral neuropathy.",
    pricing: { quest: 54, labcorp: 49, goodlabs: 34 },
  },

  // ── Iron ──────────────────────────────────────────────────────────────
  {
    id: "ferritin",
    canonicalName: "Ferritin",
    displayName: "Ferritin",
    category: "Iron",
    alternateNames: ["Ferritin", "Serum Ferritin"],
    biomarkers: ["Serum Ferritin (ng/mL)"],
    plainDescription:
      "Measures your iron storage levels. The most sensitive early indicator of iron deficiency.",
    medicalDescription:
      "Acute-phase protein reflecting total body iron stores. Decreased in iron-deficiency anemia; elevated in hemochromatosis and inflammatory states.",
    pricing: { quest: 46, labcorp: 43, goodlabs: 33 },
  },
  {
    id: "iron",
    canonicalName: "Iron and Total Iron Binding Capacity",
    displayName: "Iron / TIBC Panel",
    category: "Iron",
    alternateNames: [
      "Iron Panel",
      "Iron and TIBC",
      "Iron Binding Capacity",
      "Iron Studies",
      "Iron with TIBC",
    ],
    biomarkers: [
      "Serum Iron (mcg/dL)",
      "TIBC — Total Iron Binding Capacity (mcg/dL)",
      "UIBC — Unsaturated Iron Binding Capacity",
      "Transferrin Saturation (%)",
    ],
    plainDescription:
      "Full picture of iron metabolism — how much iron is in your blood and how much your body could absorb.",
    medicalDescription:
      "Quantifies serum iron, total and unsaturated iron binding capacity, and transferrin saturation. Differentiates iron-deficiency anemia from anemia of chronic disease.",
    pricing: { quest: 62, labcorp: 57, goodlabs: 39 },
  },

  // ── Hormones ──────────────────────────────────────────────────────────
  {
    id: "total-test",
    canonicalName: "Testosterone, Total",
    displayName: "Testosterone, Total",
    category: "Hormones",
    alternateNames: [
      "Total Testosterone",
      "Testosterone Total",
      "Testosterone, Serum",
    ],
    biomarkers: ["Total Testosterone (ng/dL)"],
    plainDescription:
      "Measures total testosterone. Standard for TRT monitoring, general hormonal health, and baseline checks.",
    medicalDescription:
      "Immunoassay or LC-MS/MS quantification of total serum testosterone. Primary marker for hypogonadism screening and TRT monitoring.",
    pricing: { quest: 69, labcorp: 61, goodlabs: 45 },
    notes:
      "LC-MS/MS is more accurate at low levels. Confirm assay method when scraping.",
  },
  {
    id: "free-test",
    canonicalName: "Testosterone, Free",
    displayName: "Testosterone, Free",
    category: "Hormones",
    alternateNames: [
      "Free Testosterone",
      "Testosterone, Free and Total",
      "Free T",
    ],
    biomarkers: ["Free Testosterone (pg/mL)", "Total Testosterone (ng/dL)"],
    plainDescription:
      "Measures the testosterone not bound to proteins — the portion that's biologically active.",
    medicalDescription:
      "Calculated or direct measurement of unbound testosterone. More sensitive than total testosterone alone in individuals with altered SHBG levels.",
    pricing: { quest: 79, labcorp: 72, goodlabs: 51 },
    notes:
      "Calculated free T uses albumin and SHBG; equilibrium dialysis is the gold standard. Clarify method when scraping.",
  },
  {
    id: "estradiol",
    canonicalName: "Estradiol",
    displayName: "Estradiol (Sensitive)",
    category: "Hormones",
    alternateNames: [
      "Estradiol",
      "Estradiol Sensitive",
      "E2",
      "Estradiol, Sensitive",
      "Estradiol LC/MS",
    ],
    biomarkers: ["Estradiol / E2 (pg/mL)"],
    plainDescription:
      "Measures estrogen (E2). Used by people on TRT or HRT to monitor levels and track hormonal status.",
    medicalDescription:
      "Quantitative estradiol measurement. LC-MS/MS preferred over immunoassay for men and low-level monitoring. Used in TRT/HRT management and fertility evaluation.",
    pricing: { quest: 58, labcorp: 53, goodlabs: 38 },
    notes:
      "Sensitive LC-MS/MS preferred for men and low-level female monitoring. Immunoassay is inaccurate at low concentrations. Flag assay type when scraping.",
  },
  {
    id: "shbg",
    canonicalName: "Sex Hormone Binding Globulin",
    displayName: "SHBG",
    category: "Hormones",
    alternateNames: [
      "SHBG",
      "Sex Hormone Binding Globulin",
      "Sex Hormone-Binding Globulin",
    ],
    biomarkers: ["SHBG (nmol/L)"],
    plainDescription:
      "Measures a protein that binds to sex hormones, affecting how much free testosterone and estrogen are available in the body.",
    medicalDescription:
      "Quantification of sex hormone binding globulin. Used alongside total testosterone to estimate free testosterone and assess androgen bioavailability.",
    pricing: { quest: 67, labcorp: 61, goodlabs: 44 },
  },

  // ── Men's Health ──────────────────────────────────────────────────────
  {
    id: "psa",
    canonicalName: "Prostate-Specific Antigen, Total",
    displayName: "PSA",
    category: "Men's Health",
    alternateNames: [
      "PSA",
      "PSA Total",
      "Prostate Specific Antigen",
      "PSA, Serum",
    ],
    biomarkers: ["PSA, Total (ng/mL)"],
    plainDescription:
      "Screens for prostate health in men. Typically recommended starting at age 40–50 depending on risk factors.",
    medicalDescription:
      "Total PSA immunoassay. Primary prostate cancer screening marker; also used for post-treatment monitoring and risk stratification.",
    pricing: { quest: 41, labcorp: 38, goodlabs: 27 },
    notes:
      "Free PSA ratio can improve specificity. Some providers list PSA + Free PSA as a bundle — note both when scraping.",
  },
];
