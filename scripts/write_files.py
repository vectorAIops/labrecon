"""
write_files.py — Run this from your repo root (labrecon/) to create the scraper/ directory.
Usage: python write_files.py
"""
from pathlib import Path

# Create directories
Path("scraper/providers").mkdir(parents=True, exist_ok=True)
Path("scraper/utils").mkdir(parents=True, exist_ok=True)
Path("scraper/debug").mkdir(parents=True, exist_ok=True)

# ============================================================
# __init__.py files (empty)
# ============================================================
Path("scraper/__init__.py").write_text("")
Path("scraper/providers/__init__.py").write_text("")
Path("scraper/utils/__init__.py").write_text("")

# ============================================================
# scraper/tests_catalog.py
# ============================================================
Path("scraper/tests_catalog.py").write_text('''\
TESTS = [
    {
        "id": "cbc",
        "name": "Complete Blood Count",
        "alt_names": ["CBC", "CBC with Differential", "CBC w/ Diff",
                      "Complete Blood Count with Differential"],
        "notes": None,
    },
    {
        "id": "cmp",
        "name": "Comprehensive Metabolic Panel",
        "alt_names": ["CMP", "Complete Metabolic Panel", "Chemistry Panel",
                      "14-Panel Chemistry"],
        "notes": None,
    },
    {
        "id": "lipid",
        "name": "Lipid Panel",
        "alt_names": ["Lipid Panel", "Cholesterol Panel", "Lipid Profile"],
        "notes": None,
    },
    {
        "id": "a1c",
        "name": "Hemoglobin A1c",
        "alt_names": ["HbA1c", "A1c", "Glycosylated Hemoglobin",
                      "Hemoglobin A1C", "Glycated Hemoglobin"],
        "notes": None,
    },
    {
        "id": "crp",
        "name": "C-Reactive Protein",
        "alt_names": ["CRP", "hsCRP", "High-Sensitivity CRP", "hs-CRP",
                      "C-Reactive Protein High Sensitivity"],
        "notes": "Prefer hsCRP over standard CRP. Flag which variant was matched.",
    },
    {
        "id": "insulin",
        "name": "Insulin, Fasting",
        "alt_names": ["Insulin", "Fasting Insulin", "Serum Insulin"],
        "notes": "Must be the fasting version.",
    },
    {
        "id": "lpa",
        "name": "Lipoprotein(a)",
        "alt_names": ["Lp(a)", "Lipoprotein a", "Lipoprotein-a"],
        "notes": "Units vary (mg/dL vs nmol/L). Record and flag unit.",
    },
    {
        "id": "apob",
        "name": "Apolipoprotein B",
        "alt_names": ["ApoB", "Apo B", "Apolipoprotein B-100"],
        "notes": None,
    },
    {
        "id": "tsh",
        "name": "Thyroid Stimulating Hormone",
        "alt_names": ["TSH", "Thyroid Stimulating Hormone", "Thyrotropin"],
        "notes": None,
    },
    {
        "id": "ft4",
        "name": "Free Thyroxine",
        "alt_names": ["Free T4", "FT4", "Free Thyroxine", "Thyroxine Free"],
        "notes": None,
    },
    {
        "id": "vitd",
        "name": "Vitamin D, 25-Hydroxyvitamin D",
        "alt_names": ["Vitamin D", "25-OH Vitamin D", "25-Hydroxyvitamin D",
                      "Vitamin D 25-Hydroxy", "Calcidiol"],
        "notes": "Prefer total D. Flag if only D2/D3 split is available.",
    },
    {
        "id": "b12",
        "name": "Vitamin B12",
        "alt_names": ["B12", "Vitamin B12", "Cobalamin", "Cyanocobalamin"],
        "notes": None,
    },
    {
        "id": "ferritin",
        "name": "Ferritin",
        "alt_names": ["Ferritin", "Serum Ferritin"],
        "notes": None,
    },
    {
        "id": "iron",
        "name": "Iron and Total Iron Binding Capacity",
        "alt_names": ["Iron Panel", "Iron and TIBC", "Iron Binding Capacity",
                      "Iron Studies", "Iron with TIBC"],
        "notes": None,
    },
    {
        "id": "total-test",
        "name": "Testosterone, Total",
        "alt_names": ["Total Testosterone", "Testosterone Total",
                      "Testosterone Serum"],
        "notes": "Flag LC-MS/MS vs immunoassay if visible.",
    },
    {
        "id": "free-test",
        "name": "Testosterone, Free",
        "alt_names": ["Free Testosterone", "Testosterone Free and Total",
                      "Free T"],
        "notes": "Flag calculated vs direct measurement.",
    },
    {
        "id": "estradiol",
        "name": "Estradiol",
        "alt_names": ["Estradiol", "Estradiol Sensitive", "E2",
                      "Estradiol LC/MS"],
        "notes": "Prefer sensitive/LC-MS assay. Flag assay type.",
    },
    {
        "id": "shbg",
        "name": "Sex Hormone Binding Globulin",
        "alt_names": ["SHBG", "Sex Hormone Binding Globulin",
                      "Sex Hormone-Binding Globulin"],
        "notes": None,
    },
    {
        "id": "psa",
        "name": "Prostate-Specific Antigen, Total",
        "alt_names": ["PSA", "PSA Total", "Prostate Specific Antigen",
                      "PSA Serum"],
        "notes": "Total PSA only. Flag if Free PSA ratio is bundled.",
    },
]
''')

# ============================================================
# scraper/utils/matching.py
# ============================================================
Path("scraper/utils/matching.py").write_text('''\
"""Fuzzy test name matching for LabRecon.io scraper."""

import re
from difflib import SequenceMatcher


def find_match(scraped_name: str, catalog: list[dict]) -> tuple[str | None, str]:
    """
    Find the best match for a scraped test name in the catalog.

    Returns (test_id, match_type) where match_type is
    "exact", "alt_exact", "fuzzy", or "none".
    """
    normalized = re.sub(r"\\s+", " ", scraped_name.strip()).lower()

    # 1. Exact match on canonical name
    for test in catalog:
        if test["name"].lower().strip() == normalized:
            return test["id"], "exact"

    # 2. Exact match on any alt_name
    for test in catalog:
        for alt_name in test["alt_names"]:
            if alt_name.lower().strip() == normalized:
                return test["id"], "alt_exact"

    # 3. Fuzzy match — threshold >= 0.82
    best_match: str | None = None
    best_score = 0.0
    for test in catalog:
        for name in [test["name"]] + test["alt_names"]:
            score = SequenceMatcher(None, normalized, name.lower().strip()).ratio()
            if score >= 0.82 and score > best_score:
                best_score = score
                best_match = test["id"]

    if best_match:
        return best_match, "fuzzy"

    return None, "none"
''')

# ============================================================
# scraper/utils/pricing.py
# ============================================================
Path("scraper/utils/pricing.py").write_text('''\
"""Price string parsing for LabRecon.io scraper."""

import re


def parse_price(raw: str) -> tuple[float | None, list[str]]:
    """
    Parse a raw price string into a float.

    Returns (price_float, flags) where flags is a list of warning strings.
    """
    flags: list[str] = []
    cleaned = re.sub(r"[\\s$,]", "", raw).strip()

    # Handle price ranges like "29.99-39.99" or "29.99\\u201339.99"
    if "\\u2013" in cleaned or "-" in cleaned:
        sep = "\\u2013" if "\\u2013" in cleaned else "-"
        parts = cleaned.split(sep)
        if len(parts) == 2:
            try:
                lower = float(parts[0])
                flags.append(f"Price range detected: {raw}, using lower bound")
                return round(lower, 2), flags
            except ValueError:
                pass

    # Single price
    try:
        price = float(cleaned)
        return round(price, 2), flags
    except ValueError:
        flags.append(f"Could not parse price: {raw}")
        return None, flags
''')

# ============================================================
# scraper/main.py
# ============================================================
Path("scraper/main.py").write_text('''\
"""Entry point for LabRecon.io scraper."""

import asyncio
import json
import argparse
from datetime import datetime, timezone

from scraper.providers.quest import scrape_quest
from scraper.providers.labcorp import scrape_labcorp
from scraper.tests_catalog import TESTS

PROVIDERS = {
    "quest": scrape_quest,
    "labcorp": scrape_labcorp,
}


async def main(headed: bool = False) -> None:
    results: dict[str, dict[str, float | None]] = {t["id"]: {} for t in TESTS}
    all_flags: list[str] = []
    not_found: list[str] = []

    for provider_id, scrape_fn in PROVIDERS.items():
        prices, flags = await scrape_fn(headed=headed)
        all_flags.extend(flags)
        for test in TESTS:
            tid = test["id"]
            price = prices.get(tid)
            results[tid][provider_id] = price
            if price is None:
                not_found.append(f"{tid}@{provider_id}")

    output = {
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "results": results,
        "flags": all_flags,
        "not_found": not_found,
    }

    with open("scraped_pricing.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Done. {len(not_found)} tests not found. See scraped_pricing.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LabRecon.io price scraper")
    parser.add_argument("--headed", action="store_true",
                        help="Run browsers in headed mode for debugging")
    args = parser.parse_args()
    asyncio.run(main(headed=args.headed))
''')

# ============================================================
# scraper/providers/quest.py
# ============================================================
Path("scraper/providers/quest.py").write_text('''\
"""Quest Health scraper for LabRecon.io."""

import asyncio
import json
import random
from pathlib import Path

from playwright.async_api import async_playwright

from scraper.tests_catalog import TESTS
from scraper.utils.matching import find_match
from scraper.utils.pricing import parse_price

# ---- CSS Selectors (update these when site changes) ----
SEARCH_INPUT_SELECTOR = "input[type=\'search\']"   # SELECTOR: verify against questhealth.com DOM
TEST_CARD_SELECTOR = ".test-card"                   # SELECTOR: verify
TEST_NAME_SELECTOR = ".test-card h3"                # SELECTOR: verify
PRICE_SELECTOR = ".test-card .price"                # SELECTOR: verify

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]


async def scrape_quest(headed: bool = False) -> tuple[dict[str, float | None], list[str]]:
    """Scrape Quest Health prices. Returns (prices_dict, flags_list)."""
    prices: dict[str, float | None] = {}
    flags: list[str] = []
    debug_dir = Path("scraper/debug")
    debug_dir.mkdir(parents=True, exist_ok=True)

    async def handle_error(page, msg: str) -> None:
        try:
            await page.screenshot(path=str(debug_dir / "quest_error.png"))
        except Exception:
            pass
        flags.append("quest: scraping error \\u2014 see debug/quest_error.png")
        print(msg)

    async def fetch_test_prices(page, test_name: str) -> None:
        try:
            await page.fill(SEARCH_INPUT_SELECTOR, test_name)
            await page.wait_for_selector(TEST_CARD_SELECTOR, state="visible",
                                         timeout=10_000)
            await asyncio.sleep(1.5)

            cards = await page.query_selector_all(TEST_CARD_SELECTOR)
            for card in cards:
                name_el = await card.query_selector(TEST_NAME_SELECTOR)
                price_el = await card.query_selector(PRICE_SELECTOR)

                if name_el and price_el:
                    name = (await name_el.text_content() or "").strip()
                    price_text = (await price_el.text_content() or "").strip()
                    test_id, match_type = find_match(name, TESTS)
                    if test_id:
                        price, price_flags = parse_price(price_text)
                        prices[test_id] = price
                        flags.extend(price_flags)
                        if match_type == "fuzzy":
                            flags.append(
                                f"quest: fuzzy match \\"{name}\\" -> {test_id}"
                            )
                    else:
                        flags.append(f"quest: no match for \\"{name}\\"")
        except Exception as e:
            await handle_error(page, f"quest: error searching \\"{test_name}\\": {e}")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=not headed)
            context = await browser.new_context(user_agent=random.choice(UA_LIST))
            page = await context.new_page()
            await page.set_viewport_size({"width": 1280, "height": 900})

            try:
                await page.goto("https://www.questhealth.com/lab-tests",
                                wait_until="networkidle", timeout=30_000)
                await asyncio.sleep(1.5)

                for test in TESTS:
                    await fetch_test_prices(page, test["name"])
            except Exception as e:
                await handle_error(page, f"quest: navigation error: {e}")
            finally:
                await browser.close()
    except Exception as e:
        flags.append(f"quest: playwright launch failed: {e}")
        print(f"quest: playwright launch failed: {e}")

    return prices, flags


if __name__ == "__main__":
    result_prices, result_flags = asyncio.run(scrape_quest(headed=True))
    print(json.dumps({"prices": result_prices, "flags": result_flags}, indent=2))
''')

# ============================================================
# scraper/providers/labcorp.py
# ============================================================
Path("scraper/providers/labcorp.py").write_text('''\
"""LabCorp OnDemand scraper for LabRecon.io."""

import asyncio
import json
import random
from pathlib import Path

from playwright.async_api import async_playwright

from scraper.tests_catalog import TESTS
from scraper.utils.matching import find_match
from scraper.utils.pricing import parse_price

# ---- CSS Selectors (update these when site changes) ----
SEARCH_INPUT_SELECTOR = "input[type=\'search\']"   # SELECTOR: verify against labcorpondemand.com DOM
CATEGORY_SELECTOR = ".category"                     # SELECTOR: verify
TEST_CARD_SELECTOR = ".test-card"                   # SELECTOR: verify
TEST_NAME_SELECTOR = ".test-card h3"                # SELECTOR: verify
PRICE_SELECTOR = ".test-card .price"                # SELECTOR: verify

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]


async def scrape_labcorp(headed: bool = False) -> tuple[dict[str, float | None], list[str]]:
    """Scrape LabCorp OnDemand prices. Returns (prices_dict, flags_list)."""
    prices: dict[str, float | None] = {}
    flags: list[str] = []
    debug_dir = Path("scraper/debug")
    debug_dir.mkdir(parents=True, exist_ok=True)

    async def handle_error(page, msg: str) -> None:
        try:
            await page.screenshot(path=str(debug_dir / "labcorp_error.png"))
        except Exception:
            pass
        flags.append("labcorp: scraping error \\u2014 see debug/labcorp_error.png")
        print(msg)

    async def fetch_test_prices(page, test_name: str) -> None:
        try:
            await page.fill(SEARCH_INPUT_SELECTOR, test_name)
            await page.wait_for_selector(TEST_CARD_SELECTOR, state="visible",
                                         timeout=10_000)
            await asyncio.sleep(1.5)

            cards = await page.query_selector_all(TEST_CARD_SELECTOR)
            for card in cards:
                name_el = await card.query_selector(TEST_NAME_SELECTOR)
                price_el = await card.query_selector(PRICE_SELECTOR)

                if name_el and price_el:
                    name = (await name_el.text_content() or "").strip()
                    price_text = (await price_el.text_content() or "").strip()

                    # Flag "Starting at" prices
                    if "starting at" in price_text.lower():
                        flags.append(
                            f"labcorp: \\"{name}\\" shows \\"Starting at\\" price"
                        )

                    # Flag "Add to Cart" prices and skip
                    if "add to cart" in price_text.lower():
                        flags.append(
                            f"labcorp: \\"{name}\\" requires add-to-cart for price, skipped"
                        )
                        continue

                    test_id, match_type = find_match(name, TESTS)
                    if test_id:
                        price, price_flags = parse_price(price_text)
                        prices[test_id] = price
                        flags.extend(price_flags)
                        if match_type == "fuzzy":
                            flags.append(
                                f"labcorp: fuzzy match \\"{name}\\" -> {test_id}"
                            )
                    else:
                        flags.append(f"labcorp: no match for \\"{name}\\"")
        except Exception as e:
            await handle_error(page, f"labcorp: error searching \\"{test_name}\\": {e}")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=not headed)
            context = await browser.new_context(user_agent=random.choice(UA_LIST))
            page = await context.new_page()
            await page.set_viewport_size({"width": 1280, "height": 900})

            try:
                await page.goto("https://www.labcorpondemand.com/tests",
                                wait_until="networkidle", timeout=30_000)
                await asyncio.sleep(1.5)

                # Try category-based navigation first
                categories = await page.query_selector_all(CATEGORY_SELECTOR)
                if categories:
                    for category in categories:
                        await category.click()
                        await asyncio.sleep(1.5)
                        for test in TESTS:
                            await fetch_test_prices(page, test["name"])
                else:
                    # Fall back to search-based approach
                    for test in TESTS:
                        await fetch_test_prices(page, test["name"])
            except Exception as e:
                await handle_error(page, f"labcorp: navigation error: {e}")
            finally:
                await browser.close()
    except Exception as e:
        flags.append(f"labcorp: playwright launch failed: {e}")
        print(f"labcorp: playwright launch failed: {e}")

    return prices, flags


if __name__ == "__main__":
    result_prices, result_flags = asyncio.run(scrape_labcorp(headed=True))
    print(json.dumps({"prices": result_prices, "flags": result_flags}, indent=2))
''')

# ============================================================
# scraper/README.md
# ============================================================
Path("scraper/README.md").write_text("""\
# LabRecon.io Scraper

Scrapes self-pay cash pricing for lab tests from Quest Health and LabCorp OnDemand.

## Install

```sh
pip install playwright beautifulsoup4 requests
playwright install chromium
```

## Usage

```sh
# Run all providers
python -m scraper.main [--headed]

# Run a single provider
python -m scraper.providers.quest
python -m scraper.providers.labcorp
```

## Output

Results are written to `scraped_pricing.json` in the repo root.

## When selectors break

Every CSS selector in the provider files is a placeholder marked with
`# SELECTOR: verify`. These target the live site DOM and **will** need
updating when the sites redesign.

To fix broken selectors:

1. Open the provider's site in Chrome.
2. Right-click the test name or price element -> **Inspect**.
3. Identify a stable CSS selector (prefer `data-*` attributes, IDs, or
   ARIA roles over class names).
4. Update the corresponding `*_SELECTOR` variable at the top of the
   provider file.
5. Test with `python -m scraper.providers.<name>` in `--headed` mode.
""")

print("All files written to scraper/")
print("Next: verify CSS selectors, then run with: python -m scraper.main --headed")
