"""
LabCorp OnDemand DOM discovery script.

Temporary script — run once to identify correct CSS selectors,
then update labcorp.py and delete this file.

Usage:
    python -m scraper.providers.labcorp_inspect
"""

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

FIREFOX_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
TARGET_URL = "https://www.ondemand.labcorp.com/products"
CARD_SELECTOR = "a.productcollection__item"


async def inspect() -> None:
    debug_dir = Path("scraper/debug")
    debug_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(user_agent=FIREFOX_UA)
        page = await context.new_page()
        await page.set_viewport_size({"width": 1280, "height": 900})

        print(f"\n-- Navigating to {TARGET_URL} --")
        await page.goto(TARGET_URL, wait_until="networkidle", timeout=30_000)
        await page.wait_for_timeout(3000)

        # -- Dismiss consent/cookie banners --
        consent_selectors = [
            "#onetrust-accept-btn-handler",
            'button[id*="accept"]',
            'button[class*="accept"]',
        ]
        for sel in consent_selectors:
            try:
                btn = await page.query_selector(sel)
                if btn and await btn.is_visible():
                    await btn.click()
                    print(f"  dismissed banner via: {sel}")
                    await page.wait_for_timeout(1000)
                    break
            except Exception:
                pass

        cards = await page.query_selector_all(CARD_SELECTOR)
        print(f"\n-- Found {len(cards)} cards with selector: {CARD_SELECTOR!r} --\n")

        # Print first two cards with full inner_html and key attributes
        for idx in range(min(2, len(cards))):
            card = cards[idx]
            inner = await card.inner_html()
            title_attr = await card.get_attribute("title")
            href_attr = await card.get_attribute("href")
            print(f"=== CARD {idx + 1} ===")
            print(f"  title attr : {title_attr!r}")
            print(f"  href attr  : {href_attr!r}")
            print(f"  inner_html :\n{inner}\n")

        print("-- Done --\n")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(inspect())
