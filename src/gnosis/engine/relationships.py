from __future__ import annotations


def bounded_traversal(depth: int, records: int, max_depth: int = 2, max_records: int = 10) -> bool:
    return depth <= max_depth and records <= max_records
