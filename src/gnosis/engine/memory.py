from __future__ import annotations

PROMOTABLE_CLASSES = {"decision", "outcome", "correction", "pattern_trigger"}

STM_MAX_TURNS = 50
STM_MAX_MINUTES = 30


def should_promote(record_class: str) -> bool:
    return record_class in PROMOTABLE_CLASSES


def within_stm_limits(turn_count: int, elapsed_minutes: int) -> bool:
    return turn_count <= STM_MAX_TURNS and elapsed_minutes <= STM_MAX_MINUTES


def within_episode_window(minutes_apart: int, max_minutes: int = 15) -> bool:
    return minutes_apart <= max_minutes
