# GNOSIS — Canonical Build Specification (v1.1)

## FINAL INTEGRATED DOCUMENT

---

## GLOBAL ENFORCEMENT RULES

- Deterministic outputs (same input = same result)
- No hallucination
- Bounded operations
- Strict tenant isolation
- Idempotent writes
- Full internal observability
- Schema versioning required

> Any violation = blocking defect

---

# 0) CONTEXT INTEGRITY & APPLICABILITY ENFORCEMENT

## MISSION (NON-NEGOTIABLE)

Ensure all returned context is actually applicable, not just similar.

### Failure Conditions
- Similar but irrelevant context returned  
- Conflicting strategies mixed  
- Ignoring prior outcomes  
- Non-deterministic filtering  

---

## Context Fingerprint

instance_id, conversation_id, active_tags, current_objective, recent_episode_ids, time_window

---

## Applicability Rules

1. Tag Overlap → must share ≥1 tag or relationship  
2. Compatibility → reject conflicts  
3. Temporal Relevance → within window or high confidence  
4. Outcome Alignment → prioritize relevant outcomes  

---

## Applicability Score

0.40 tag_match  
0.30 relationship  
0.20 time relevance  
0.10 outcome similarity  

Reject if < 0.5

---

# 1) MEMORY SYSTEM

## MISSION
Store meaningful events only.

STM:
- 50 turns OR 30 min  

LTM:
- structured episodes only  

Promotion:
- decisions, outcomes, corrections, patterns  
- exclude noise  

Episode Rules:
- group within 15 minutes  
- max duration 2 hours  

---

# 2) INGESTION & CLASSIFICATION

Classes:
decision, outcome, correction, question, answer, note, noise  

Rule-first classification  
Fallback → note  

---

# 3) PATTERN DETECTION

Trigger:
- 3 occurrences  
- within 7 days  

---

# 4) RELATIONSHIP GRAPH

Types:
same_strategy, same_symbol, correction_of, supports, contradicts  

Traversal:
- depth ≤ 2  
- max 10 records  

---

# 5) RETRIEVAL & SCORING

Pipeline:
filter → applicability → scoring → expand → assemble  

Score:
0.35 applicability  
0.30 metadata  
0.20 relationship  
0.10 embedding  
0.05 recency  

---

# FINAL STATEMENT

GNOSIS guarantees context correctness, not just relevance.
