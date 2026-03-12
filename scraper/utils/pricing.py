"""Price string parsing for LabRecon.io scraper."""

import re


def parse_price(raw: str) -> tuple[float | None, list[str]]:
    """
    Parse a raw price string into a float.

    Returns (price_float, flags) where flags is a list of warning strings.
    """
    flags: list[str] = []
    cleaned = re.sub(r"[\s$,]", "", raw).strip()

    # Handle price ranges like "29.99-39.99" or "29.99\u201339.99"
    if "\u2013" in cleaned or "-" in cleaned:
        sep = "\u2013" if "\u2013" in cleaned else "-"
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
