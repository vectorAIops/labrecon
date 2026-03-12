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
