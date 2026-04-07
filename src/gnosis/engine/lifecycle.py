from __future__ import annotations


def should_archive(days_since_last_access: int, archive_after_days: int = 90) -> bool:
    return days_since_last_access >= archive_after_days


def should_compress_similar_episodes(similar_episode_count: int, threshold: int = 10) -> bool:
    return similar_episode_count > threshold
