# GNOSIS — DEVELOPMENT CANONICAL DOCUMENT (FINAL)
Version: 1.0
Status: DEVELOPMENT READY
Purpose: Deterministic Context Engine Specification

---

# 0. SYSTEM MISSION (NON-NEGOTIABLE)

GNOSIS is a deterministic context system that ensures:
- context is applicable (not just relevant)
- outputs are grounded in recorded history
- behavior is repeatable and testable

GNOSIS is NOT:
- a reasoning engine
- a learning system
- an LLM
- a decision-maker

---

# 1. GLOBAL RULES

- Deterministic outputs
- No hallucinated memory
- Bounded operations
- Strict tenant isolation
- Idempotent processing
- Full internal traceability

Violation = BLOCKING DEFECT

---

# 2. CORE PIPELINE

Ingestion → Classification → STM → Promotion → LTM  
→ Applicability Filter → Scoring → Relationship Expansion  
→ Support/Challenge Split → Context Packet

---

# 3. INGESTION

Every input becomes a Turn.

Classification:
- decision
- outcome
- correction
- question
- answer
- note
- noise

Rule-first. Fallback = note.

---

# 4. STM

- Max 50 turns OR 30 minutes
- Used for immediate context
- Not durable

---

# 5. LTM

Stores:
- episodes
- relationships
- patterns

No raw noise allowed.

---

# 6. PROMOTION

Promote only:
- decision
- outcome
- correction
- pattern triggers

Never promote noise.

---

# 7. EPISODES

Group records:
- same tags
- within 15 minutes
- max duration 2 hours

---

# 8. PATTERN DETECTION

Trigger:
- 3 occurrences
- within 7 days

---

# 9. RELATIONSHIPS

Types:
- same_strategy
- same_symbol
- correction_of
- supports
- contradicts

Limits:
- depth ≤ 2
- max 10 records

---

# 10. APPLICABILITY ENFORCEMENT (CORE)

Context must be VALID for situation.

Rules:
1. Tag overlap required
2. Reject incompatible context
3. Enforce time relevance
4. Align outcomes

Score:
- tag: 0.40
- relationship: 0.30
- time: 0.20
- outcome: 0.10

Reject if < 0.5

Conflict handling:
- KEEP BOTH (support + challenge)

---

# 11. RETRIEVAL

Pipeline:
filter → applicability → scoring → expand → assemble

Max candidates: 100

---

# 12. SCORING

Final score:
- applicability 0.35
- metadata 0.30
- relationship 0.20
- embedding 0.10
- recency 0.05

---

# 13. SUPPORT / CHALLENGE

Always return:
- supporting evidence
- challenging evidence

Conflict is preserved.

---

# 14. EMPTY CONTEXT

Return:
- STM context
- explicit: "insufficient context"

No guessing.

---

# 15. CONTEXT PACKET

Order:
1. summary
2. state
3. support
4. challenge
5. relevant

Limits:
- max ~2500 tokens

---

# 16. LIFECYCLE

- STM expires
- LTM retained
- archive after 90 days
- compress >10 similar episodes

---

# 17. FAILURE HANDLING

- transactional writes
- retry x3
- rollback on failure

---

# 18. VALIDATION

System must prove:
- determinism
- correct filtering
- correct conflict handling
- no hallucination
- bounded behavior

---

# 19. PRODUCT MEMORY HORIZONS (THREE TIERS)

The engine is specified in this document primarily as **STM** and **LTM**. For product and API explanations, the same behavior may be described as **three horizons**:

| Horizon | Meaning | Maps in this spec |
|---------|---------|-------------------|
| **Short-term** | What is **resident now**—the immediate working band (current conversation / hot buffer). | **STM** (Section 4): bounded turns and time, not durable as long-term store. |
| **Intermediate** | A **blend**: partly **live** (still in the working path) and partly **looked up** from recent structured memory—recent episodes, promotion candidates, session-adjacent material. Not “the whole archive,” not only the last few turns. | **Episode grouping** (Section 7), **promotion** pipeline (Section 6), and selective reads of **recent LTM** under the same applicability rules—not a separate magic store, but the **bridge** between STM and cold LTM. |
| **Long-term** | **Durable** memory you **retrieve** on purpose—episodes, relationships, patterns that survived promotion and lifecycle rules. | **LTM** (Section 5) plus retrieval and lifecycle (Sections 10–12, 16). |

All three remain **per-tenant / per-agent isolated**, **bounded**, and **applicability-gated**; there is no unscoped “load everything.”

---

# FINAL STATEMENT

GNOSIS guarantees:
- context correctness
- deterministic behavior
- evidence-based outputs

It does NOT guarantee:
- truth
- decisions
- reasoning

It guarantees:
"the right context for the situation"

