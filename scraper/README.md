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
