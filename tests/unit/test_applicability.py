import pytest

from gnosis.engine.applicability import compute_applicability_score, is_applicable
from gnosis.models.context import CandidateContext, ContextFingerprint


def test_applicability_passes_when_candidate_is_compatible_and_within_window() -> None:
    fingerprint = ContextFingerprint(
        instance_id="tenant-a",
        conversation_id="conv-1",
        active_tags={"memory", "retrieval"},
        current_objective="return applicable context",
        time_window_hours=24,
    )
    candidate = CandidateContext(
        candidate_id="episode-1",
        tags={"retrieval"},
        relationships={"supports"},
        hours_since_event=2,
        outcome_similarity=0.9,
        compatibility_ok=True,
    )

    assert compute_applicability_score(fingerprint, candidate) == pytest.approx(0.99)
    assert is_applicable(fingerprint, candidate) is True


def test_applicability_rejects_incompatible_context_even_with_high_similarity() -> None:
    fingerprint = ContextFingerprint(
        instance_id="tenant-a",
        conversation_id="conv-1",
        active_tags={"memory"},
        current_objective="return applicable context",
    )
    candidate = CandidateContext(
        candidate_id="episode-2",
        tags={"memory"},
        relationships={"supports"},
        hours_since_event=1,
        outcome_similarity=1.0,
        compatibility_ok=False,
    )

    assert is_applicable(fingerprint, candidate) is False
