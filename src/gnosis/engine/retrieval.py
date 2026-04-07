from __future__ import annotations

MAX_CANDIDATES = 100


def retrieval_score(
    applicability: float,
    metadata: float,
    relationship: float,
    embedding: float,
    recency: float,
) -> float:
    return (
        0.35 * applicability
        + 0.30 * metadata
        + 0.20 * relationship
        + 0.10 * embedding
        + 0.05 * recency
    )


def within_candidate_limit(candidate_count: int, max_candidates: int = MAX_CANDIDATES) -> bool:
    return candidate_count <= max_candidates
