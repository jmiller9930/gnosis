from __future__ import annotations

from dataclasses import dataclass

VALID_CLASSES = {
    "decision",
    "outcome",
    "correction",
    "question",
    "answer",
    "note",
    "noise",
}


@dataclass(slots=True)
class IngestedRecord:
    content: str
    record_class: str


def classify_record(content: str, labels: set[str] | None = None) -> IngestedRecord:
    labels = labels or set()

    for label in VALID_CLASSES:
        if label in labels:
            return IngestedRecord(content=content, record_class=label)

    return IngestedRecord(content=content, record_class="note")
