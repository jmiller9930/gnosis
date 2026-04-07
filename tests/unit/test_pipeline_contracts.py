from gnosis.engine.evidence import split_support_and_challenge
from gnosis.engine.lifecycle import should_archive, should_compress_similar_episodes
from gnosis.engine.memory import should_promote, within_stm_limits
from gnosis.engine.packet import build_insufficient_context_packet
from gnosis.engine.retrieval import within_candidate_limit
from gnosis.models.context import CandidateContext


def test_pattern_trigger_is_promotable_but_note_is_not() -> None:
    assert should_promote("pattern_trigger") is True
    assert should_promote("note") is False


def test_stm_limits_follow_canonical_bounds() -> None:
    assert within_stm_limits(turn_count=50, elapsed_minutes=30) is True
    assert within_stm_limits(turn_count=51, elapsed_minutes=30) is False


def test_support_and_challenge_are_preserved_separately() -> None:
    support_candidate = CandidateContext(
        candidate_id="episode-1",
        tags={"alpha"},
        relationships={"supports"},
        hours_since_event=1,
        outcome_similarity=0.8,
    )
    challenge_candidate = CandidateContext(
        candidate_id="episode-2",
        tags={"alpha"},
        relationships={"contradicts"},
        hours_since_event=1,
        outcome_similarity=0.7,
    )

    support, challenge = split_support_and_challenge([support_candidate, challenge_candidate])

    assert support == [support_candidate]
    assert challenge == [challenge_candidate]


def test_empty_context_packet_is_explicit() -> None:
    packet = build_insufficient_context_packet("recent stm state")

    assert packet.summary == "insufficient context"
    assert packet.state == "recent stm state"
    assert packet.insufficient_context is True


def test_retrieval_and_lifecycle_limits_match_canonical_rules() -> None:
    assert within_candidate_limit(100) is True
    assert within_candidate_limit(101) is False
    assert should_archive(90) is True
    assert should_compress_similar_episodes(11) is True
