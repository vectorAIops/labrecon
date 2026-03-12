"""Fuzzy test name matching for LabRecon.io scraper."""

import re
from difflib import SequenceMatcher


def find_match(scraped_name: str, catalog: list[dict]) -> tuple[str | None, str]:
    """
    Find the best match for a scraped test name in the catalog.

    Returns (test_id, match_type) where match_type is
    "exact", "alt_exact", "fuzzy", or "none".
    """
    normalized = re.sub(r"\s+", " ", scraped_name.strip()).lower()

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
