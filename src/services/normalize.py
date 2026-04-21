"""Small text/number helpers shared by providers and the renderer."""
from __future__ import annotations

import re


_NUM_RE = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?")

MISSING_VALUE_PLACEHOLDER = "--"


def parse_int(text: str | None) -> int | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return int(m.group(0).replace(",", "").split(".")[0])
    except ValueError:
        return None


def parse_float(text: str | None) -> float | None:
    if text is None:
        return None
    m = _NUM_RE.search(str(text))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def format_int(value) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return "--"


def format_ratio(value, decimals: int = 2) -> str:
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return "--"


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def format_headline_value(value) -> str:
    """Format a headline value (int, float, str, or None) for display."""
    if value is None:
        return MISSING_VALUE_PLACEHOLDER
    if isinstance(value, (int, float)):
        return format_int(value)
    return str(value)


def format_substat_value(value) -> str:
    """Format a substat value (int, float, bool, str, or None) for display."""
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, float):
        return format_ratio(value)
    if isinstance(value, int):
        return format_int(value)
    return str(value)
