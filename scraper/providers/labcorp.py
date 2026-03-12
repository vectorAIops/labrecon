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
SEARCH_INPUT_SELECTOR = "input[type='search']"   # SELECTOR: verify against labcorpondemand.com DOM
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
        flags.append("labcorp: scraping error \u2014 see debug/labcorp_error.png")
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
                            f"labcorp: \"{name}\" shows \"Starting at\" price"
                        )

                    # Flag "Add to Cart" prices and skip
                    if "add to cart" in price_text.lower():
                        flags.append(
                            f"labcorp: \"{name}\" requires add-to-cart for price, skipped"
                        )
                        continue

                    test_id, match_type = find_match(name, TESTS)
                    if test_id:
                        price, price_flags = parse_price(price_text)
                        prices[test_id] = price
                        flags.extend(price_flags)
                        if match_type == "fuzzy":
                            flags.append(
                                f"labcorp: fuzzy match \"{name}\" -> {test_id}"
                            )
                    else:
                        flags.append(f"labcorp: no match for \"{name}\"")
        except Exception as e:
            await handle_error(page, f"labcorp: error searching \"{test_name}\": {e}")

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=not headed)
            context = await browser.new_context(user_agent=random.choice(UA_LIST))
            page = await context.new_page()
            await page.set_viewport_size({"width": 1280, "height": 900})

            try:
                await page.goto("https://www.ondemand.labcorp.com/products",
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
