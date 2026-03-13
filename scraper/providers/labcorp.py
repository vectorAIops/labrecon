"""LabCorp OnDemand scraper for LabRecon.io."""

import asyncio
import json
from pathlib import Path

from playwright.async_api import async_playwright

from scraper.provider_mappings import PROVIDER_NAMES
from scraper.utils.pricing import parse_price

# Reverse lookup: exact LabCorp name -> internal test ID
# Built at import time — only populated once labcorp mappings are confirmed.
_LABCORP_EXACT: dict[str, str] = {
    v["labcorp"]: tid
    for tid, v in PROVIDER_NAMES.items()
    if v.get("labcorp") is not None
}

# ---- CSS Selectors (verified 2026-03-12 against ondemand.labcorp.com DOM) ----
TEST_CARD_SELECTOR = "a.productcollection__item"
CARD_DATA_SELECTOR = ".productlist__item-actions"  # holds data-name and data-price
LOAD_MORE_SELECTOR = "button[class*='more']"

# Firefox UA — matches quest.py browser context setup
FIREFOX_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"


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
        flags.append("labcorp: scraping error - see debug/labcorp_error.png")
        print(msg)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=not headed)
            context = await browser.new_context(user_agent=FIREFOX_UA)
            page = await context.new_page()
            await page.set_viewport_size({"width": 1280, "height": 900})

            try:
                # Navigate to catalog
                await page.goto("https://www.ondemand.labcorp.com/products",
                                wait_until="networkidle", timeout=30_000)
                await page.wait_for_timeout(3000)

                # Dismiss cookie/consent banner if present
                try:
                    accept_btn = await page.query_selector("#onetrust-accept-btn-handler")
                    if accept_btn and await accept_btn.is_visible():
                        await accept_btn.click()
                        await page.wait_for_timeout(1000)
                except Exception:
                    pass

                # Click "Load More" until all tests are loaded
                prev_count = 0
                while True:
                    load_more = await page.query_selector(LOAD_MORE_SELECTOR)
                    if not load_more:
                        break
                    is_visible = await load_more.is_visible()
                    if not is_visible:
                        break
                    await page.wait_for_timeout(2000)
                    await load_more.click()
                    await page.wait_for_timeout(2000)
                    # Stop if card count hasn't grown (button stuck / all loaded)
                    cards_now = await page.query_selector_all(TEST_CARD_SELECTOR)
                    if len(cards_now) == prev_count:
                        break
                    prev_count = len(cards_now)

                # Scrape all test cards
                cards = await page.query_selector_all(TEST_CARD_SELECTOR)
                print(f"labcorp: found {len(cards)} test cards")

                for card in cards:
                    data_el = await card.query_selector(CARD_DATA_SELECTOR)
                    if not data_el:
                        continue

                    name = (await data_el.get_attribute("data-name") or "").strip()
                    price_text = (await data_el.get_attribute("data-price") or "").strip()

                    if not name or not price_text:
                        continue

                    test_id = _LABCORP_EXACT.get(name)

                    if test_id:
                        price, price_flags = parse_price(price_text)
                        prices[test_id] = price
                        flags.extend(price_flags)
                        print(f"  matched: {name} -> {test_id} = {price}")
                    else:
                        print(f"  no match: {name} | {price_text}")

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
