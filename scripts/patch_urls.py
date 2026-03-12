"""
patch_urls.py — Run from repo root to update provider URLs and add GoodLabs.
Usage: python patch_urls.py
"""
from pathlib import Path

# ============================================================
# Update scraper/providers/quest.py — fix catalog URL
# ============================================================
quest = Path("scraper/providers/quest.py").read_text()
quest = quest.replace(
    "https://www.questhealth.com/lab-tests",
    "https://www.questhealth.com/shop-tests"
)
Path("scraper/providers/quest.py").write_text(quest)
print("Updated quest.py URL")

# ============================================================
# Update scraper/providers/labcorp.py — fix catalog URL
# ============================================================
labcorp = Path("scraper/providers/labcorp.py").read_text()
labcorp = labcorp.replace(
    "https://www.labcorpondemand.com/tests",
    "https://www.ondemand.labcorp.com/products"
)
Path("scraper/providers/labcorp.py").write_text(labcorp)
print("Updated labcorp.py URL")

# ============================================================
# Create scraper/providers/goodlabs.py
# ============================================================
Path("scraper/providers/goodlabs.py").write_text('''\
"""GoodLabs scraper for LabRecon.io."""

import asyncio
import json
import random
from pathlib import Path

from playwright.async_api import async_playwright

from scraper.tests_catalog import TESTS
from scraper.utils.matching import find_match
from scraper.utils.pricing import parse_price

# ---- CSS Selectors (update these when site changes) ----
SEARCH_INPUT_SELECTOR = "input[type=\'search\']"   # SELECTOR: verify against goodlabs.com DOM
TEST_CARD_SELECTOR = ".test-card"                   # SELECTOR: verify
TEST_NAME_SELECTOR = ".test-card h3"                # SELECTOR: verify
PRICE_SELECTOR = ".test-card .price"                # SELECTOR: verify

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]


async def scrape_goodlabs(headed: bool = False) -> tuple[dict[str, float | None], list[str]]:
    """Scrape GoodLabs prices. Returns (prices_dict, flags_list)."""
    prices: dict[str, float | None] = {}
    flags: list[str] = []
    debug_dir = Path("scraper/debug")
    debug_dir.mkdir(parents=True, exist_ok=True)

    async def handle_error(page, msg: str) -> None:
        try:
            await page.screenshot(path=str(debug_dir / "goodlabs_error.png"))
        except Exception:
            pass
        flags.append("goodlabs: scraping error \\u2014 see debug/goodlabs_error.png")
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
                                f"goodlabs: fuzzy match \\"{name}\\" -> {test_id}"
                            )
                    else:
                        flags.append(f"goodlabs: no match for \\"{name}\\"")
        except Exception as e:
            await handle_error(page, f"goodlabs: error searching \\"{test_name}\\": {e}")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=not headed)
            context = await browser.new_context(user_agent=random.choice(UA_LIST))
            page = await context.new_page()
            await page.set_viewport_size({"width": 1280, "height": 900})

            try:
                await page.goto("https://goodlabs.com/tests",
                                wait_until="networkidle", timeout=30_000)
                await asyncio.sleep(1.5)

                for test in TESTS:
                    await fetch_test_prices(page, test["name"])
            except Exception as e:
                await handle_error(page, f"goodlabs: navigation error: {e}")
            finally:
                await browser.close()
    except Exception as e:
        flags.append(f"goodlabs: playwright launch failed: {e}")
        print(f"goodlabs: playwright launch failed: {e}")

    return prices, flags


if __name__ == "__main__":
    result_prices, result_flags = asyncio.run(scrape_goodlabs(headed=True))
    print(json.dumps({"prices": result_prices, "flags": result_flags}, indent=2))
''')
print("Created goodlabs.py")

# ============================================================
# Update scraper/main.py — add GoodLabs provider
# ============================================================
Path("scraper/main.py").write_text('''\
"""Entry point for LabRecon.io scraper."""

import asyncio
import json
import argparse
from datetime import datetime, timezone

from scraper.providers.quest import scrape_quest
from scraper.providers.labcorp import scrape_labcorp
from scraper.providers.goodlabs import scrape_goodlabs
from scraper.tests_catalog import TESTS

PROVIDERS = {
    "quest": scrape_quest,
    "labcorp": scrape_labcorp,
    "goodlabs": scrape_goodlabs,
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
print("Updated main.py with GoodLabs")

print("\\nDone. All URLs updated, GoodLabs provider added.")
print("Next: bring to Claude Code for review, then verify CSS selectors.")
