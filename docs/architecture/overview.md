# GNOSIS architecture overview

This file is the **hub** for product and implementation architecture. There is **one** GNOSIS product line in this repository—**GNOSIS**—implemented as a deterministic pipeline aligned with [GNOSIS_FINAL_CANONICAL.md](../specs/GNOSIS_FINAL_CANONICAL.md). Normative rules live in that spec; **this page** is the narrative spine.

---

## The story

### The problem

It is easy to ship an agent; it is hard to keep one useful and agentic over time without deep memory in the right sense—not a bigger context window, but durable, scoped, qualified history (what was decided, what happened, what applies here?). Without that, the agent stays clever in the moment and does not compound trustworthy behavior.

### What runs today — GNOSIS

The context engine in this repo. It qualifies memory: per-agent silos, context-triggered recall, applicability before naive similarity, explicit insufficient context when precedent does not apply. GNOSIS is not a learning system; it is memory as the gate for what downstream steps may treat as grounded.

### In the repo, not operating — learning engine

A learning layer is part of the long-term powerhouse story next to GNOSIS: adaptation that shows up in observable behavior (your test: can you see learning change what the agent does?). Code is present in this repository, but the learning engine is not operating in production paths yet (disabled, unwired, or limited tests only—implementation detail). When it runs, it must not bypass applicability, tenant isolation, or honest insufficiency; changes should write through structured, auditable paths into the same system GNOSIS protects.

### One backend, many agents

A single GNOSIS-style service for the whole agent fleet cuts duplicated glue and centralizes operations—one place for auth, quotas, observability, schema and version discipline, and upgrades instead of N ad-hoc memory stacks. That is not rigid one-size-fits-all policy for every team: you still want wiggle room—tenant-scoped knobs, tags and fingerprints, connectors, deployment options, and bounded customization where the business needs it. The through-line teams accept when they adopt the platform is the standard contract: memory as qualifier, ingress shaping, per-agent silos, and explicit insufficient context. Enforce that standard for safety and auditability; allow controlled variation around it so product teams are not strangled.

### Together

Qualified memory (GNOSIS, running) + learning (in repo, not on) + one shared backend (with standard gate and room to move) is the full-stack aim. This document still centers on GNOSIS as the live product contract.

### Beyond agentic workflows — any LLM-backed use

GNOSIS is not limited to “agents” in the narrow sense. The same context service can back **any** AI-assisted conversation or **in-house** workload that needs **grounded, scoped** memory: assistants, copilots, support flows, tools with an LLM front. **Local LLMs** fit naturally: GNOSIS runs as a **sidecar or service** next to the model—you keep data and policy **under your control** and send **bounded packets** to whichever model runs locally or remote. The LLM is **swappable**; the **memory contract** stays the same.

### Standard retrieval — plus triggering as the gate

You still use **normal** building blocks where they belong: **indexes**, **filters**, **vectors**, **recency**, **SQL**—often **after** narrowing by tenant, time, and class. What is **distinctive** here is not “no vectors”; it is **order of operations** and **product emphasis**: **context triggering** and **applicability** decide **what may inform this turn** before you treat similarity as enough. Same idea as a person answering “how old are you?” or “what’s your name?”—they do **not** reload their **entire biography**; the **question** **cues** a **small** relevant slice. GNOSIS tries to **emulate** that: **cue-driven**, **eligible** memory, not **undifferentiated** replay of everything you ever stored.

---

## Thesis (three pillars)

**1. A dedicated memory space for every agent** — Each agent has its **own** silo: recorded history and retrieval are **isolated** by identity. No mixing across agents (**strict tenant isolation** in spec terms).

**2. Context-triggered recall on every exchange** — Each turn carries a **situation** (topic, tags, time window, objective, conversation scope). The engine does **not** load “entire life” history. It **activates only what applies** to *this* situation—**cue-driven** retrieval, then applicability and bounded assembly. When nothing legitimately applies, the system returns **explicit insufficient context**.

**3. Memory as the qualifier for processing** — **Recorded memory** (after applicability) is what **qualifies** what downstream steps may treat as **grounded**—not raw horsepower or prompt size. If memory does **not** qualify, the honest outcome is **insufficient context**; the system does **not** substitute scale (more tokens, bigger models) for **eligibility**.

**Together:** one silo per agent, per-turn situation-conditioned memory, and **memory-gated** processing—not undifferentiated search or “stuff the window.”

---

## Scope

This document focuses on systems that **directly influence an LLM or agent run**: memory APIs, retrieval that **qualifies** what may count, tool-time context, and execution gates—including **local** and **in-house** models. Generic team wikis or human note apps are **out of scope** as product analogues (they may still be **ingest sources**). The **learning engine** is summarized in [The story](#the-story) above.

---

## Documentation governance (no document creep)

**Hard rule:** Do **not** add scattered `*.md` files for every topic. **Document creep is not allowed.**

| Rule | Detail |
|------|--------|
| **Default narrative home** | This file (`overview.md`). Extend it; do not spawn parallel overviews. |
| **Allowed without exception** | [`README.md`](../../README.md) (entry), [`docs/specs/`](../specs/) (normative specs). |
| **Rare separate doc** | Only when unavoidable (e.g. compliance pack). Create **one** focused file and **link it from here**—no orphans. |
| **Everyone** | Prefer **editing** existing docs over creating new ones. |

---

## Purpose

GNOSIS answers: *what context from recorded history **legitimately** applies to this request?* Outputs are a **context packet** or **insufficient context**, with explicit bounds and traceability. Persistence and APIs wrap this core.

---

## Flagship differentiators (vs mainstream “memory”)

GNOSIS leads with **eligibility, bounds, and structure**—not “vector similarity + longest prompt.”

| Flagship | What it is | Why it’s uncommon |
|----------|------------|-------------------|
| **Context triggering** | Memory is **activated** by the **current situation** (fingerprint)—**cue-driven**, not top‑*k* similarity alone. | Few products treat **situation validity** as a **hard gate** before ranking. |
| **Ingress shaping** | Before sync/API: **rule-first classification**, structured fields, dedupe—**bounded** records, not raw megachats. Cuts token burn and aids audit. | Most pipelines forward **full text** first. |
| **Applicability before relevance** | **Reject** ineligible candidates, **then** score. | Common pattern is **embed → rank** without a **validity** layer. |
| **Explicit insufficient context** | Normal when the record does not support a strong answer—**no** filler. | Many systems always return something “close enough.” |
| **Support + challenge preserved** | Conflicting outcomes stay **visible**. | Retrieval often **flattens** tension. |

**Hydration / local-first** (below) pairs with ingress shaping: work **locally**, sync **structured** deltas, keep prompts **small**.

---

## Core flow

1. Ingest structured inputs; classify with rule-first logic.  
2. Keep immediate history in STM; promote only eligible records to LTM.  
3. Store durable episodes, relationships, and patterns in LTM.  
4. Enforce applicability before retrieval expansion.  
5. Rank candidates deterministically; expand through **bounded** relationships.  
6. Preserve support and challenge evidence.  
7. Assemble a context packet or return **explicit** insufficient context.

---

## Module responsibilities

| Module | Role |
|--------|------|
| `models/context.py` | Request, turn, candidate, packet structures. |
| `engine/applicability.py` | Reject-first applicability rules and scoring. |
| `engine/ingestion.py` | Rule-first classification. |
| `engine/memory.py` | STM, promotion, episode grouping. |
| `engine/patterns.py` | Repeated signals in bounded windows. |
| `engine/relationships.py` | Bounded graph expansion. |
| `engine/retrieval.py` | Weighted component scores. |
| `engine/evidence.py` | Supporting vs challenging evidence. |
| `engine/packet.py` | Context packet and insufficient-context fallback. |
| `engine/lifecycle.py` | Retention and compression guardrails. |

---

## Memory horizons (short, intermediate, long)

See canonical §19. Three **product** horizons map to STM / episodes / LTM:

- **Short-term** — **Resident** working memory (immediate turns / hot buffer) → **STM** in the spec.  
- **Intermediate** — **Hybrid**: live + selective lookup from recent structured memory (episodes, promotion). → Bridge between STM and cold LTM.  
- **Long-term** — **Durable** store; explicit retrieval → **LTM**.

All tiers stay **applicability-gated** and **per-agent isolated**.

---

## Agentic workflows

Consumers are **autonomous or semi-autonomous agents** (tools, planners, long tasks). Typical need: **outcome-aware** memory—*have we done this? what happened?* The spec’s classes (`decision`, `outcome`, `correction`, …), **promotion**, **episodes**, **relationships**, and **patterns** support that without turning GNOSIS into a learner or policy engine.

---

## Service model (target)

**Context storage as a service:** operators run GNOSIS; **agents** are clients.

- **API** — Ingest turns, query context packets, health/metadata.  
- **Per-agent silos** — Map agent identity → isolated `instance_id` / partition; **strict tenant isolation** in the spec.  
- **Separation** — GNOSIS does not replace agent reasoning or tools; auth, quotas, and rate limits sit at the edge.

Implementation order is flexible (engine → persistence → public API); the goal is a **multi-tenant context API** with **one silo per agent**.

---

## Hydration and local-first operation

- **Hydration** — Keep a **small** set of important facts (goals, constraints, last state). **Rehydration** reloads that slice after rest—aligned with fingerprints and **bounded** packets.  
- **Local-first** — Filter and narrow **next to the agent**; call the GNOSIS API for **durable** writes, **LTM** reads, or **cross-session** truth—not necessarily every turn at full text.  
- **Wire discipline** — Structured writes on milestones; reads via **fingerprint-scoped** packets.

---

## Build vs integrate

| Build in GNOSIS | Integrate (commodity) |
|-----------------|------------------------|
| Classification, STM/LTM/promotion, applicability, packets, insufficiency, tenant rules, public **contract** | Durable stores, queues, vector search, embeddings, caches, observability |

---

## Typical infrastructure integrations (purpose)

| Piece | Purpose |
|-------|---------|
| **Durable storage** (Postgres, SQLite, managed SQL) | Source of truth for turns, episodes, indexes; tenant-scoped query. |
| **Queues / async** | Decouple ingest from indexing; backpressure and replay. |
| **Vector ANN** (managed DB, pgvector, …) | Fast similarity **within** filtered candidates. |
| **Embeddings** | Vectors for similarity; **version** models for reproducibility. |
| **Metrics / traces** (e.g. OpenTelemetry) | Find latency in ingest vs index vs pack. |
| **Caching** (Redis, in-process LRU) | Hot paths; scope and invalidate consistently. |

---

## Bounded context (anti-bloat)

Long prompts do not equal reliable memory. GNOSIS outputs **bounded** packets (canonical cap), uses **STM/LTM** rules, caps **candidates** and **graph** depth, and uses **three horizons**. Retrieval is **applicability-gated**, not “fill the window with top‑*k* chunks.” Infra adds speed—not an excuse to bloat prompts.

---

## Implementation principles

- Deterministic functions where possible  
- Bounded traversal and result counts  
- Explicit weights and thresholds  
- No hidden fallback behavior  
- Preserve conflict; prefer **smaller, defensible** packets  

---

## Runtime and packaging (Docker-first)

**Goal:** The same **container images** move from development to a **test lab** with **environment and secrets** differences—not different install steps on the host.

**Portable application:** GNOSIS is meant to run as a **portable stack**: **images + Compose + `.env`**. The same artifacts run on a dev machine, CI, or a lab host **without** per-host installs of Python, Postgres, or app code—the host only needs a container runtime (and, for real runs, secrets and port choices). No bespoke “only works on server X” install path is the target.

| Piece | Role |
|-------|------|
| **Language** | Python **3.11+** ([`pyproject.toml`](../../pyproject.toml)); the engine is a **package** under `src/gnosis/`. |
| **Application image** | [`Dockerfile`](../../Dockerfile) at repo root: slim base, `pip install` the package, **non-root** user (`uid 1000`), `HEALTHCHECK` via `python -c "import gnosis"`. **CMD** keeps the process alive until an ASGI server replaces it. |
| **Compose stack** | [`docker-compose.yml`](../../docker-compose.yml): **`app`** (build) + **`db`** (Postgres 16) + named volume for data. Optional **`redis`** behind Compose **profile** `with-redis` (`docker compose --profile with-redis up`). **Principle:** everything that **can** run in Docker **does**—no “install Postgres on your laptop” for real runs. |
| **Configuration** | [`.env.example`](../../.env.example) → copy to **`.env`** (gitignored): `DATABASE_URL`, Postgres vars, optional `REDIS_URL`. |
| **Test lab** | [`docker-compose.lab.yml`](../../docker-compose.lab.yml): merge with `-f docker-compose.yml -f docker-compose.lab.yml` for resource hints and lab env; **inject secrets** from CI or a vault, not the image. |
| **Local overrides** | Optional `docker-compose.override.yml` (gitignored): Compose merges it automatically—e.g. bind-mount `./src` for iterative work. Do not use override files in the lab image pipeline. |
| **Host prerequisites** | Docker Engine + Compose v2. Optional: registry to **push/pull** tagged images into the lab. |

**Smoke test:** `docker compose build` and `docker compose up -d`; `app` healthcheck passes; `db` healthy. **Exec:** `docker compose exec app python -c "import gnosis"`.

**GPU / local LLM:** If a model needs a GPU, treat it as a **separate** service or host attach when Compose cannot satisfy it; keep GNOSIS and data services **containerized** where possible.

---

## Could (pending review — not a committed rollout)

Nothing here is **normative** until the team reviews and adopts it. This is **structural could**—examples and ordering ideas—not a promise of schedule, environment, or go-live.

### Structural rollout and lab placement (example only)

When you **do** place GNOSIS on a shared host, a **dedicated directory** keeps it separate from other projects—**illustrative** layout:

```text
~/server/Gnosis/       # example: git clone root (Dockerfile, docker-compose.yml, …)
  .env                 # from .env.example; never commit
```

**Illustrative** workflow: `cd` there, `git pull`, `docker compose build && docker compose up -d`. Paths, hostnames, and promotion steps stay **open** until reviewed.

### Phased capability expansion (suggested order, not a timeline)

**Not** a product rollout calendar—only **when** you might add **capabilities** to the stack as needs appear:

1. Engine + one DB + synchronous API — correctness and contracts first.  
2. Hybrid retrieval (filters + vectors) — when filters alone are thin.  
3. Async indexing + queues — when ingest cost hurts latency.  
4. Partitioning / sharding — when single DB or region limits you.  
5. Aggressive caching — when hot patterns are clear and safe.

---

## Pilot validation scenarios

After a **working pilot** is running, these scenarios demonstrate **effectiveness** in a short demo or **automated** regression suite. They are **post-operational** checks: small, high-signal, aligned with the GNOSIS thesis (isolation, qualification, honesty, bounded context).

### 1 — Silo isolation (must never fail)

| Field | Example |
|-------|---------|
| Ingest (Agent A only) | `instance_id: agent-alice`, turn: “Payroll cutoff for Acme is Friday 17:00 ET.” Tags: `acme`, `payroll`, `policy`. |
| Query (as Agent B) | `instance_id: agent-bob`, fingerprint tags include `payroll`, objective “when is cutoff?” |
| Question | “What is Acme’s payroll cutoff?” |
| Pass | No Alice-only fact returned; **insufficient context** or empty—not cross-tenant leakage. |

### 2 — Insufficient context (precedent required, none stored)

| Field | Example |
|-------|---------|
| Setup | `instance_id: agent-carlos`, minimal history, **no** LTM about refund policy. |
| Fingerprint | Tags `billing`, `refunds`; objective “apply refund policy.” |
| Question | “Under our **official refund policy**, can I approve a **partial** refund for order **ORD-7788** after 45 days?” |
| Why it matters | Answer should depend on **policy you did not ingest**. |
| Pass | **Explicit insufficient context**, not a fabricated policy. |

### 3 — Similar but not applicable (QA vs prod)

| Field | Example |
|-------|---------|
| Ingest | One change: “Flag `FEATURE_X` enabled in **QA**, no incident.” Tags: `qa`, `feature-x`, `change`. **No** matching prod record. |
| Fingerprint | Tags `prod`, `feature-x`, `change`; objective “approve prod rollout.” |
| Question | “Is it **safe to enable `FEATURE_X` in prod** given our **prior changes**?” |
| Pass | Does **not** treat QA success as prod proof; **insufficient** or explicit “no applicable prod precedent.” |

### 4 — Context triggering (cue, not full history)

| Field | Example |
|-------|---------|
| Ingest | Long noisy transcript **plus** structured facts: display name “Jordan”, age 34 (or classified turns with tags `profile`, `stable`). |
| Fingerprint | Tags `profile`; objective “answer identity fact”; narrow time window. |
| Question | “What is my **first name**?” or “How **old** am I?” |
| Pass | Small, relevant packet; does **not** require the entire transcript to answer. |

### 5 — Conflict preservation

| Field | Example |
|-------|---------|
| Ingest | Episode A: Strategy S worked in Q1; +5%. Episode B: Strategy S failed in Q3 after rule change; −2%. |
| Fingerprint | Tags `strategy-s`; objective “should we use S now?” |
| Question | “Should we **still** use strategy S **this quarter**?” |
| Pass | **Support** and **challenge** both visible, or explicit tension—not one flattened verdict. |

### 6 — Ingress shaping (optional)

| Field | Example |
|-------|---------|
| Raw input | Long chat plus one line: “**Decision:** blue-green for **checkout**; approved by Jane; effective Monday.” |
| After shaping | Stored: `record_class: decision`, tags `checkout`, `blue-green`, `prod`, short summary—**not** full paste as the durable row. |
| Question | “What **deploy pattern** did we **approve** for checkout?” |
| Pass | Answer from **structured** fields, not re-sending the whole raw blob each time. |

**One-slide demo:** Run **1 + 2 + (3 or 4)** in about ten minutes: **safe**, **honest**, **situation-aware**.

---

## Discussion sample: ServiceNow and digital SRE

Use this when explaining **memory as qualifier** vs “search millions of tickets and pick what feels similar.” Illustrative only.

**Setup:** ServiceNow-scale ITSM; **human** doing change work; **DigiSRE** agent executes against tickets/CMDB; **GNOSIS** supplies **applicable** memory or **insufficient context**.

**When memory qualifies**

- **Human:** Tonight we deploy **CHG0045123** — **rolling restart** of **payment API** in **prod US-East**, like last month’s success.  
- **DigiSRE:** Context for **CHG0045123**, **CI payment-api-prod-useast**, model **rolling restart**.  
- **GNOSIS:** Applicable: **CHG0038891** closed **successful**, same CI/region/category, no Sev-1 follow-up. “Rolling restart **worked in prod** before” is **grounded**.  
- **DigiSRE:** Attach **CHG0038891**; proceed with approved **standard** automation.

**When memory does *not* qualify**

- **Human:** Also enable **`PAY_EXP_BYPASS`** like in **QA** last week.  
- **DigiSRE:** Checking **prod** applicability for that flag.  
- **GNOSIS:** **Insufficient context** to treat QA as prod. No **closed successful prod** change for that flag on this CI under current CAB scope.  
- **DigiSRE:** No prod execution on “QA was fine” alone—open sub-task / separate CR if needed.  
- **Human:** Split it out of tonight’s restart.

**Why this beats naive search**

- Scale of the DB does not matter until **applicability** selects what may inform **this** change.  
- **Similarity** is not enough—**governance scope** must **qualify** memory.  
- The agent can **stop** honestly instead of **hallucinating** continuity.

---

## Versus a single conversation file (or runbook)

A **single megadoc** can work for **solo**, **manual**, **low-stakes** work. GNOSIS pays off when you need **structure, scope, and automation** at scale.

| Topic | One conversation file | GNOSIS |
|-------|------------------------|--------|
| **Scale** | You summarize ITSM by hand. | Structured ingest + scoped retrieval. |
| **Structure** | Implicit types. | Typed turns; checkable applicability and insufficiency. |
| **Isolation** | QA/prod blur in one blob. | Per-agent silos + fingerprints. |
| **Qualification** | Hope + prose inference. | Rules + records for **this** change. |
| **Automation** | Re-encode into tools ad hoc. | API contract for ingest/query. |
| **Audit** | Weak evidence. | Append-only, classified history with ids. |
| **Drift** | Huge window / re-strike. | Bounded packets and horizons. |

**Summary:** A file is **tribal prose** until scale and governance bite. GNOSIS is **memory that can refuse to qualify**—with **isolation** and **bounds**.

---

## Agent-native systems landscape (competing projects)

Examples of **agent-runtime** memory/context products—not exhaustive, not endorsements. Verify on each vendor’s site.

| Project | Agent-facing role | GNOSIS contrast |
|---------|-------------------|-----------------|
| **[Zep](https://www.getzep.com/)** | Graphs, sessions, ingestion, context for LLMs. | GNOSIS: **applicability gate**, **insufficient context**, **memory as qualifier**—rule-first packets. |
| **[Mem0](https://mem0.ai/)** | Add/get memory, vectors + KV (+ optional graph). | GNOSIS: **whether** recall **may** apply to **this** situation. |
| **[Letta](https://www.letta.com/)** | Agent platform with long-lived agent state/memory. | GNOSIS is **not** an agent—**context + rules** for other stacks. |
| **[Supermemory](https://supermemory.ai/)** | API + graph/profile/retrieval. | Same broad space; GNOSIS thesis: qualifier, support/challenge, bounded packets. |
| **[Cognee](https://www.cognee.ai/)** | Pipelines, connectors, graphs + vectors. | GNOSIS: **eligibility**, deterministic engine bounds, anti-bloat. |
| **[Hindsight](https://hindsight.vectorize.io/)** | Retain/recall/reflect; multi-strategy search. | GNOSIS: **hard applicability** + **insufficient context** as first-class—not only richer recall. |

**Frameworks** (LangGraph, LangChain checkpointers, Semantic Kernel, CrewAI, AutoGen): you supply **policy**; they do not define GNOSIS-style **qualification**.

**Infrastructure** (Pinecone, Weaviate, Qdrant, Chroma, pgvector): **storage**, not memory policy.

For GNOSIS differentiation in one place, see [flagship differentiators](#flagship-differentiators-vs-mainstream-memory) above.
