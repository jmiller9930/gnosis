# GNOSIS

GNOSIS is a **deterministic context engine**: one product, one version line in this repository. It is not positioned as a “lite” or “heavy” variant—it is the context engine, built to be correct, bounded, and testable rather than maximally feature-stacked.

**Scope:** GNOSIS is aimed at **context that directly influences an agent**—what may be retrieved, what qualifies the next tool or step, and what is **withheld**. It is **not** centered on generic team documentation, wikis, or “notes for humans” as the product category; those may **feed** ingest, but the **primary** problem here is **agent-facing** memory and **gates**, not collaborative editing. For **named competing agent-memory projects** (Zep, Mem0, Letta, Supermemory, Cognee, Hindsight, etc.) and how GNOSIS contrasts, see [architecture overview — agent-native landscape](docs/architecture/overview.md#agent-native-systems-landscape-competing-projects).

Normative behavior and global rules live in the [canonical specification](docs/specs/GNOSIS_FINAL_CANONICAL.md).

## Thesis (three pillars)

**1. A dedicated memory space for every agent** — Each agent has its **own** silo: recorded history and retrieval are **isolated** by identity. No mixing across agents; this is **strict tenant isolation** in spec terms.

**2. Context-triggered recall on every exchange** — Each conversation turn carries a **situation** (topic, tags, time window, objective, conversation scope). The engine does **not** load “entire life” history into play. It **activates only what applies** to *this* situation: **cue-driven** retrieval (like answering a question by pulling what fits the question), then applicability filtering and bounded assembly. When nothing legitimately applies, the system returns **explicit insufficient context**—that is still “triggered” behavior, not a silent guess.

**3. Memory as the qualifier for processing** — **Recorded memory** (after applicability) is what **qualifies** what downstream processing may treat as **grounded** for this step—not raw horsepower or prompt size. If memory does **not** qualify the situation, the honest outcome is **insufficient context**; the system does **not** substitute scale (more tokens, bigger models) for **eligibility**. Novelty is **who may speak** (which memory applies), not **how loud** (how much compute).

Together: **one silo per agent**, **per-turn situation-conditioned memory**, and **memory-gated** processing—not undifferentiated search or “stuff the window.”

**Flagship differentiators** (not the usual “vector DB + big prompt” story): **context triggering** (situation-gated activation), **ingress shaping** (refine/classify/structure **before** API so you limit token burn and store facts not megachats), **applicability before pure similarity**, **explicit insufficient context**, and **preserved support/challenge**—see [architecture overview](docs/architecture/overview.md#flagship-differentiators-vs-mainstream-memory).

**How to explain “better” to a teammate:** use the [ServiceNow / digital SRE discussion sample](docs/architecture/overview.md#discussion-sample-servicenow-and-digital-sre)—memory as **qualifier** vs **millions of tickets** you could naively “search.” For “why not one conversation file?”, see [versus a single conversation file](docs/architecture/overview.md#versus-a-single-conversation-file-or-runbook).

## Three memory horizons (what agents get)

Agents need **short-term**, **intermediate-term**, and **long-term** memory—not as marketing labels, but as **how** memory behaves:

| Horizon | What it is | How it behaves |
|---------|------------|----------------|
| **Short-term** | What is **in play right now**—the working band (this exchange, immediate turns). | Like RAM: **resident**, fast, bounded; not the full archive. |
| **Intermediate** | A **blend**: some material stays **live** in the working path; some is **pulled in** from recent structured memory (episodes, session-scoped or recently promoted material). | Neither “only the last few messages” nor “search the entire past”—**warm + selective lookup** under the same applicability rules. |
| **Long-term** | **Durable** memory you **go look up**—stored episodes, relationships, patterns that cleared promotion and lifecycle. | **Explicit retrieval** from the durable store, not assumed to be already in the prompt. |

The canonical spec implements this mainly as **STM** and **LTM** plus **episodes** and **promotion**; the **intermediate** band is that **bridge** (see [GNOSIS_FINAL_CANONICAL.md](docs/specs/GNOSIS_FINAL_CANONICAL.md) §19). Everything stays **per-agent isolated** and **context-triggered**.

## Agentic workflows (why this exists)

GNOSIS is aimed at **agents that run multi-step work**, not only chatbots. A typical need is **outcome-aware memory**: *have I attempted this kind of step before?* and *did it work out?* That requires **structured** history—**decisions**, **outcomes**, **corrections**—not a blob of text. The engine records those classes, can promote durable episodes, and can surface **supporting** and **contradicting** prior outcomes when the **current situation** matches (tags, relationships, time window). **Pattern** rules (e.g. repeated signals over a window) flag when “this keeps happening.” The agent still decides what to do next; GNOSIS supplies **grounded** “what we know happened before” or **insufficient context** when the record does not support a strong claim.

## Product goals

- **Agent-facing API** — Expose a clear HTTP (or RPC) API so agents can integrate without bespoke wiring: authenticate, write context (ingest turns), and read context (context packets or explicit insufficiency). The goal is *easy connection* for many consumers, not one-off integrations.
- **Per-agent memory silos** — Each connected agent operates in a **dedicated slice of memory**: its history and retrieval are **isolated** from every other agent. No cross-agent reads unless a future, explicitly scoped feature says otherwise. This matches the engine’s requirement for **strict tenant isolation** (see canonical spec); in service terms, the “tenant” is the agent (or the agent’s identity as issued by your auth layer).
- **Context storage as a service** — GNOSIS is deployed and operated as **managed context storage**: callers store and query **grounded, structured memory** through the API; the engine enforces applicability, bounds, and determinism. It is **not** the agent’s brain—only the **durable, auditable context substrate** agents can rely on.

More detail on how the API and isolation sit around the core engine is in [docs/architecture/overview.md](docs/architecture/overview.md).

## What GNOSIS is supposed to do

GNOSIS serves **agents and other callers** by assembling **context packets** from **recorded history**, under strict rules:

- **Ingest** inputs as turns and **classify** them with rule-first logic (no free-form guessing).
- **Separate memory horizons**: **short-term** (working, resident), **intermediate** (blend of live + selective lookup from recent structured memory), **long-term** (durable store and explicit retrieval)—aligned with STM, episodes/promotion, and LTM in the canonical spec.
- **Enforce applicability** before scoring or expanding retrieval—relevance alone is not enough.
- **Retrieve and rank** candidates deterministically, with **bounded** graph expansion and result counts.
- **Preserve disagreement**: supporting and challenging evidence are not collapsed into a single story unless the spec says so.
- **Return** either a **context packet** suited to the request fingerprint or an **explicit insufficient-context** outcome when the record does not justify an answer.

## What GNOSIS is

- A deterministic context system
- Grounded in recorded history
- Repeatable and testable

## What GNOSIS is not

- A reasoning engine
- A learning system
- An LLM
- A decision-maker

## Implementation map

The package layout mirrors the canonical document:

- Context applicability enforcement
- Turn ingestion and rule-first classification
- STM and LTM boundaries and promotion
- Memory episode modeling
- Pattern detection
- Relationship graph traversal (bounded)
- Support and challenge preservation
- Context packet assembly
- Retrieval and scoring

## Project layout

- **Documentation (no creep)** — **Do not** add new markdown files casually. **Primary** architecture and product narrative live in [`docs/architecture/overview.md`](docs/architecture/overview.md). The [`README`](README.md) and [`docs/specs/`](docs/specs/) are the other allowed homes; anything else is **rare** and must be **linked from** the architecture overview. See **Documentation governance** in that file.
- `docs/specs/` — canonical and supporting specifications
- `docs/architecture/` — implementation-facing architecture notes ( **`overview.md` is the hub** )
- `src/gnosis/engine/` — core engine modules
- `src/gnosis/models/` — shared data models
- `tests/unit/` — deterministic unit tests
- `tests/integration/` — reserved for pipeline-level verification
- **Docker** — [`Dockerfile`](Dockerfile), [`docker-compose.yml`](docker-compose.yml), [`.env.example`](.env.example); optional [`docker-compose.lab.yml`](docker-compose.lab.yml) for test lab. Full layout: [Runtime and packaging](docs/architecture/overview.md#runtime-and-packaging-docker-first).

## Getting started

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pytest -q
```

### Docker (portable stack)

Everything that can run in Docker runs in Compose (app + Postgres; optional Redis profile). Copy `.env.example` to `.env`, then:

```bash
docker compose build
docker compose up -d
```

Test lab (same images, merged overrides): `docker compose -f docker-compose.yml -f docker-compose.lab.yml up -d`

Optional cache: `docker compose --profile with-redis up -d` and set `REDIS_URL` in `.env` (see `.env.example`).

## Design notes

- Determinism is treated as a hard requirement.
- Applicability is enforced before retrieval scoring.
- Conflict is preserved through support and challenge outputs.
- Empty or unsupported context must return explicit insufficiency instead of guessing.
- **Anti-bloat:** Extremely long **context windows** (stuffing the whole history into a prompt) do not scale—they get slow, expensive, and hard to reason about. GNOSIS is built around **bounded** working memory, **bounded** retrieval, and **capped** context packets—not “send everything.”
- **Hydration + local-first:** Keep agents **hydrated** on a **small** set of important facts (and **rehydrate** after rest from snapshot + service); do heavy filtering **locally** and hit the API for **durable** or **LTM** needs—limits token and egress burn (see [architecture overview](docs/architecture/overview.md#hydration-and-local-first-operation)).
- The codebase grows with the canonical spec; avoid parallel “product skins” in this repo.
