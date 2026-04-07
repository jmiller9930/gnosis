from __future__ import annotations

from collections.abc import Iterable

from gnosis.models.context import CandidateContext


def split_support_and_challenge(
    candidates: Iterable[CandidateContext],
) -> tuple[list[CandidateContext], list[CandidateContext]]:
    support: list[CandidateContext] = []
    challenge: list[CandidateContext] = []

    for candidate in candidates:
        if "contradicts" in candidate.relationships:
            challenge.append(candidate)
        else:
            support.append(candidate)

    return support, challenge
