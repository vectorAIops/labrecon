"""Quest Health scraper for LabRecon.io."""

import asyncio
import json
import random
from pathlib import Path

from playwright.async_api import async_playwright

from scraper.tests_catalog import TESTS
from scraper.utils.matching import find_match
from scraper.utils.pricing import parse_price

# ---- CSS Selectors (verified 2026-03-10 against questhealth.com DOM) ----
TEST_CARD_SELECTOR = "a.qd-product-tile-link"
TEST_NAME_SELECTOR = "h3.qd-product-tile-name"
PRICE_SELECTOR = ".qd-product-tile-price strong"
SHOW_MORE_SELECTOR = "button#search-results-more"

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
        flags.append("quest: scraping error - see debug/quest_error.png")
        print(msg)

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=not headed)
            context = await browser.new_context(user_agent=random.choice(UA_LIST))
            page = await context.new_page()
            await page.set_viewport_size({"width": 1280, "height": 900})

            try:
                # Navigate to catalog
                await page.goto("https://www.questhealth.com/shop-tests",
                                wait_until="networkidle", timeout=30_000)
                await asyncio.sleep(2)

                # Dismiss cookie consent banner if present
                try:
                    accept_btn = await page.query_selector("#onetrust-accept-btn-handler")
                    if accept_btn:
                        await accept_btn.click()
                        await asyncio.sleep(1)
                except Exception:
                    pass

                # Click "Show More" until all tests are loaded
                while True:
                    show_more = await page.query_selector(SHOW_MORE_SELECTOR)
                    if not show_more:
                        break
                    is_visible = await show_more.is_visible()
                    if not is_visible:
                        break
                    await show_more.click()
                    await asyncio.sleep(1.5)

                # Scrape all test cards
                cards = await page.query_selector_all(TEST_CARD_SELECTOR)
                print(f"quest: found {len(cards)} test cards")

                for card in cards:
                    inner = await card.inner_html()
                    print(inner[:200])
                    break
                    name_el = await card.query_selector(TEST_NAME_SELECTOR)
                    price_el = await card.query_selector(PRICE_SELECTOR)

                    if not name_el or not price_el:
                        continue

                    name = (await name_el.text_content() or "").strip()
                    price_text = (await price_el.text_content() or "").strip()

                    if not name or not price_text:
                        continue

                    test_id, match_type = find_match(name, TESTS)

                    if test_id:
                        price, price_flags = parse_price(price_text)
                        prices[test_id] = price
                        flags.extend(price_flags)
                        if match_type == "fuzzy":
                            flags.append(f"quest: fuzzy match \"{name}\" -> {test_id}")
                        print(f"  matched: {name} -> {test_id} = {price}")
                    else:
                        print(f"  no match: {name} | {price_text}") 

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
