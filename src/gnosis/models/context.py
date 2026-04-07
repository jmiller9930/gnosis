from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ContextFingerprint:
    instance_id: str
    conversation_id: str
    active_tags: set[str]
    current_objective: str
    recent_episode_ids: list[str] = field(default_factory=list)
    time_window_hours: int = 24


@dataclass(slots=True)
class CandidateContext:
    candidate_id: str
    tags: set[str]
    relationships: set[str]
    hours_since_event: int
    outcome_similarity: float
    compatibility_ok: bool = True


@dataclass(slots=True)
class Turn:
    turn_id: str
    content: str
    record_class: str
    tags: set[str] = field(default_factory=set)


@dataclass(slots=True)
class ContextPacket:
    summary: str
    state: str
    support: list[CandidateContext]
    challenge: list[CandidateContext]
    relevant: list[CandidateContext]
    insufficient_context: bool
