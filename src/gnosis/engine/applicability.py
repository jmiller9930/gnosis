from __future__ import annotations

from gnosis.models.context import CandidateContext, ContextFingerprint

DEFAULT_APPLICABILITY_THRESHOLD = 0.50


def compute_applicability_score(
    fingerprint: ContextFingerprint,
    candidate: CandidateContext,
) -> float:
    tag_match = 1.0 if fingerprint.active_tags & candidate.tags else 0.0
    relationship_match = 1.0 if candidate.relationships else 0.0
    time_match = 1.0 if candidate.hours_since_event <= fingerprint.time_window_hours else 0.0
    outcome_match = max(0.0, min(candidate.outcome_similarity, 1.0))

    return (
        0.40 * tag_match
        + 0.30 * relationship_match
        + 0.20 * time_match
        + 0.10 * outcome_match
    )


def is_applicable(
    fingerprint: ContextFingerprint,
    candidate: CandidateContext,
    threshold: float = DEFAULT_APPLICABILITY_THRESHOLD,
) -> bool:
    if not candidate.compatibility_ok:
        return False
    if not (fingerprint.active_tags & candidate.tags or candidate.relationships):
        return False
    return compute_applicability_score(fingerprint, candidate) >= threshold
