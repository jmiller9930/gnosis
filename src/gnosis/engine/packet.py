from __future__ import annotations

from gnosis.models.context import CandidateContext, ContextPacket


def build_context_packet(
    summary: str,
    state: str,
    support: list[CandidateContext],
    challenge: list[CandidateContext],
    relevant: list[CandidateContext],
) -> ContextPacket:
    return ContextPacket(
        summary=summary,
        state=state,
        support=support,
        challenge=challenge,
        relevant=relevant,
        insufficient_context=False,
    )


def build_insufficient_context_packet(stm_context: str) -> ContextPacket:
    return ContextPacket(
        summary="insufficient context",
        state=stm_context,
        support=[],
        challenge=[],
        relevant=[],
        insufficient_context=True,
    )
