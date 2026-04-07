from __future__ import annotations


def pattern_triggered(occurrences: int, days: int, min_occurrences: int = 3, max_days: int = 7) -> bool:
    return occurrences >= min_occurrences and days <= max_days
