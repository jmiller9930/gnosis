# GNOSIS: Algorithm Design Package (Research-Grade Specification)

**Status:** Paper-first blueprint. **No implementation** is assumed or required for this document to stand.

**Thesis (working):** A memory system should determine whether a memory is **eligible** and **properly bounded** for the present situation **before** ranking it by semantic similarity. Retrieval must allow **insufficiency** as a valid outcome, use **decomposition** to reduce token drowning, and enforce **strict scope and isolation** between agents.

---

## 1. Executive Summary

GNOSIS is specified here as a **composite retrieval-and-decision procedure**: a **qualification layer** (eligibility, scope, isolation) applied **before** similarity-based ranking, followed by **bounded selection** under a finite context budget, **sufficiency** assessment, and an **answer vs abstain** outcome. The procedure is **not** claimed to exist as a single named algorithm in the literature; it is a **composition** of established ideas (multi-stage retrieval, selective prediction, constrained selection) plus an explicit **admissibility-first** ordering that matches the GNOSIS thesis.

This document supplies: a **problem definition**, **formal inputs/outputs**, **assumptions**, an **ordered algorithm**, **mathematical formulation**, **research mapping**, **counterexamples**, **theorem-style claims** (with epistemic status), **open questions**, and an **evaluation blueprint**. The standard of completion is that a reviewer can judge **mathematical coherence**, **literary support** (not proof of novelty), and **what must be validated empirically** before implementation.

---

## 2. Problem Statement

### 2.1 Exact problem

**Given:** a **query** (information need), a **situation** (constraints of the current turn), a **requesting agent** identity, a **memory corpus** (structured or semi-structured records with metadata), and **policies** (scope, provenance, isolation, recency).

**Produce:** either a **bounded** set of memory items that **may** support a downstream answer, with an explicit **sufficiency** judgment, or an **abstention** outcome when admissible evidence is insufficient—**without** treating raw semantic similarity to the query as sufficient for admissibility.

### 2.2 Why similarity-only retrieval is insufficient

Semantic similarity conflates **“looks like”** with **“applies to”**. Embeddings and lexical overlap surface **semantically neighboring** content that may be **wrong tenant**, **wrong time**, **wrong jurisdiction**, or **wrong causal regime**. Unrestricted \(\arg\max\) similarity over the corpus **optimizes the wrong objective** when the task requires **policy-valid** memory, not merely **topic-like** memory.

### 2.3 Why large context windows do not solve the problem

Larger windows **raise capacity** but do not **allocate** evidence correctly: they increase **noise**, **cost**, and **conflict** in the prompt. “Stuff more chunks” does not implement **eligibility** or **isolation**; it often **amplifies** misleading near-neighbors. The limiting factor is not only **size** but **admissibility** and **budgeted** selection.

### 2.4 Why eligibility, bounded recall, decomposition, and abstention are necessary

| Mechanism | Role |
|-----------|------|
| **Eligibility** | Restricts candidates to those **valid under policy and situation** before similarity dominates. |
| **Bounded recall** | Enforces a **finite** context budget; prevents token drowning and forces **prioritization**. |
| **Decomposition** | Breaks **compositional** or **mega** queries into sub-queries so retrieval targets **evidence**, not a monolithic blob. |
| **Abstention** | Allows the system to **refuse** to imply grounding when admissible support is below threshold—**honest** failure vs hallucination. |

### 2.5 Failure modes GNOSIS is intended to prevent

- **Cross-agent / cross-tenant leakage** — memory from agent \(A\) informing agent \(B\)’s context.  
- **Semantically similar but inapplicable** retrieval — “mountain” images or text when the question is **not** about that scope.  
- **Stale-wins** — old but similar content outranking **valid** recent evidence when recency/policy matter.  
- **Over-retrieval** — many marginally related chunks **drown** decisive evidence.  
- **Forced answer** — model answers as if grounded when **support is insufficient** (similarity ≠ permission).

---

## 3. Formal Definitions

### 3.1 Objects

| Symbol | Object | Description |
|--------|--------|-------------|
| \(q\) | **Query** | Information need (possibly decomposed into sub-queries). |
| \(s\) | **Situation state** | Fingerprint: tags, objectives, time window, session/conversation scope, modality constraints. |
| \(a\) | **Requesting agent** | Identity in the isolation policy (tenant / `instance_id`). |
| \(\mathcal{M}\) | **Memory corpus** | Set of memory items \(m\) (records, episodes, chunks) each carrying metadata. |
| \(\mathcal{P}\) | **Policy** | Scope rules, provenance requirements, retention, **isolation** mapping (which \(m\) may be read by which \(a\)). |
| \(B\) | **Context budget** | Upper bound on tokens, items, or information-theoretic cost for the output set. |

### 3.2 Memory item

Each \(m \in \mathcal{M}\) is associated with at least:

- **Owner / scope** — which agent(s) or partition(s) may access it.  
- **Provenance** — source class, trust, version.  
- **Temporal metadata** — time of event, ingestion time, decay if modeled.  
- **Structured tags / classes** — for rule-based eligibility.  
- **Optional embedding** — for similarity **within** admissible sets.

### 3.3 Outputs

| Output | Meaning |
|--------|---------|
| \(\mathcal{O} \subseteq \mathcal{M}\) | **Output memory set** — bounded, admissible subset delivered downstream. |
| \(\omega \in \{\textsf{SUFF}, \textsf{INSUFF}\}\) | **Sufficiency outcome** — whether \(\mathcal{O}\) meets internal support threshold for answering. |
| Optional structured **answer channel** | This document treats **retrieval + sufficiency**; generation is downstream. **Abstention** is valid when \(\omega = \textsf{INSUFF}\). |

### 3.4 Notation summary

- \(\mathcal{M}_a \subseteq \mathcal{M}\): memories **readable** by agent \(a\) under \(\mathcal{P}\) (isolation).  
- \(E(m \mid s,a,\mathcal{P}) \in [0,1]\) or \(\{\textsf{true},\textsf{false}\}\): **eligibility** (defined in §5).  
- \(S(m,q) \in \mathbb{R}\): **relevance** or similarity score (e.g. cosine similarity in embedding space).

---

## 4. Candidate GNOSIS Algorithm

**Ordered procedure** (composite; not a single literature method):

1. **Input normalization** — Parse \(q\), \(s\), \(a\), load \(\mathcal{P}\), budget \(B\).

2. **Isolation filter**  
   \(\mathcal{M}^{(0)} = \{ m \in \mathcal{M} : m \text{ readable by } a \text{ under } \mathcal{P} \}\).

3. **Query decomposition** (optional but thesis-aligned for compositional mega-queries)  
   \(q \rightarrow (q_1,\ldots,q_r)\). Each sub-query carries the same \(s,a\) unless decomposition also splits situation (explicitly documented).

4. **Per-branch candidate generation** (narrow funnel)  
   For each \(q_i\), obtain a **candidate pool** \(\mathcal{C}_i \subseteq \mathcal{M}^{(0)}\) via **cheap** filters (metadata, SQL, lexical, class tags) and/or **bounded** ANN retrieval—**not** unbounded global similarity over \(\mathcal{M}\).

5. **Eligibility filtering**  
   \(\mathcal{M}^{(1)}_i = \{ m \in \mathcal{C}_i : E(m \mid s,a,\mathcal{P}) \ge \tau_E \}\) for threshold \(\tau_E\), or Boolean \(E\) must hold.

6. **Relevance ranking inside eligible set**  
   Order \(\mathcal{M}^{(1)}_i\) by \(S(m,q_i)\) (and tie-breakers: recency, provenance).

7. **Bounded subset selection under budget \(B\)**  
   Choose \(\mathcal{O}_i \subseteq \mathcal{M}^{(1)}_i\) solving a **selection objective** (§5.4)—typically **knapsack-like**: maximize weighted relevance subject to \(\sum_{m \in \mathcal{O}_i} \mathrm{cost}(m) \le B\).

8. **Merge and deduplicate** across branches → \(\mathcal{O}\).

9. **Sufficiency evaluation**  
   Compute \(T(\mathcal{O},q,s)\) (§5.5). If \(T < \tau_T\), set \(\omega = \textsf{INSUFF}\) (**abstain** for grounding); else \(\omega = \textsf{SUFF}\).

10. **Output** \((\mathcal{O}, \omega)\) to downstream (generator may **abstain** or request more specificity when \(\omega = \textsf{INSUFF}\)).

**Ordering principle:** **Isolation → (optional) decomposition → cheap filter / small pool → eligibility → similarity → bounded pack → sufficiency.**

---

## 5. Mathematical Formulation

### 5.1 Eligibility function

Let \(E: \mathcal{M} \times \mathcal{S} \times \mathcal{A} \times \mathcal{P} \rightarrow [0,1]\) (or Boolean). **Examples of factors** (not all required in every instantiation):

\[
E(m \mid s,a,\mathcal{P}) = f\bigl(\text{tag\_overlap}(m,s),\ \text{time\_valid}(m,s),\ \text{provenance\_ok}(m,\mathcal{P}),\ \text{compatibility}(m,s)\bigr)
\]

with \(f\) monotone in “goodness” of each factor. **GNOSIS-specific requirement:** \(E\) must be **computable without** using full-document semantic similarity as the **only** gate—similarity enters **later** as \(S\).

### 5.2 Candidate set after eligibility

For a single query branch (drop \(i\) for brevity):

\[
\mathcal{M}^{(1)} = \bigl\{ m \in \mathcal{C} : E(m \mid s,a,\mathcal{P}) \ge \tau_E \bigr\}
\]

### 5.3 Relevance / support score

Within \(\mathcal{M}^{(1)}\):

\[
S(m,q) \quad \text{(e.g. cosine similarity between embeddings of } m \text{ and } q\text{)}.
\]

Optional **multi-signal** score (aligned with staged retrieval literature):

\[
\tilde{S}(m,q,s) = \alpha S(m,q) + \beta R_{\text{meta}}(m,s) + \gamma R_{\text{recency}}(m,s)
\]

with \(\alpha+\beta+\gamma=1\) if convex combination—**constants are design parameters**, not claims of optimality here.

### 5.4 Bounded selection objective (token / context budget)

Let \(\mathrm{cost}(m)\) be tokens or a proxy. **Selection problem:**

\[
\mathcal{O}^\star \in \arg\max_{\mathcal{O} \subseteq \mathcal{M}^{(1)}} \ \sum_{m \in \mathcal{O}} w_m \cdot \tilde{S}(m,q,s)
\quad \text{s.t.} \quad \sum_{m \in \mathcal{O}} \mathrm{cost}(m) \le B,\quad |\mathcal{O}| \le K.
\]

This is **NP-hard** in general (knapsack); **greedy** or **LP relaxations** are common in practice—**implementation choice**, not part of the thesis.

### 5.5 Sufficiency and abstention

Let \(T: 2^{\mathcal{M}} \times \mathcal{Q} \times \mathcal{S} \rightarrow [0,1]\) aggregate **support** for answering \(q\) given \(\mathcal{O}\) and \(s\). Examples: max support score, calibrated probability from a verifier, or **structured** checks (“required record classes present”).

\[
\omega = \begin{cases}
\textsf{SUFF} & \text{if } T(\mathcal{O},q,s) \ge \tau_T \\
\textsf{INSUFF} & \text{otherwise (abstain / insufficient context)}
\end{cases}
\]

**Abstention** is **first-class** when \(T < \tau_T\).

### 5.6 Contrast with similarity-only baseline

**Naive baseline (rejected for GNOSIS goals):**

\[
R_{\text{naive}} \in \arg\max_{m \in \mathcal{M}^{(0)}} S(m,q) \quad \text{(subject only to isolation, or worse, none)}.
\]

**GNOSIS-constrained:**

\[
R \in \arg\max_{m \in \mathcal{O}^\star} S(m,q) \quad \text{after } E,\ \text{budget},\ \text{and sufficiency logic}.
\]

---

## 6. Research Support by Component

| Component | Research families | Support level |
|-----------|-------------------|---------------|
| **RAG / two-stage retrieval** | Lewis et al. (RAG); subsequent open-domain QA retrieval | **Strong** — retrieve then generate; GNOSIS **reorders** gates (eligibility before similarity dominance). |
| **Decomposition / multi-hop / iterative retrieval** | Multi-hop QA, query decomposition, IR “query splitting” | **Strong** — compositional queries benefit from staged retrieval; **emerging** in LLM agents. |
| **Selective prediction / abstention** | Classifier rejection; selective classification; “I don’t know” calibration | **Strong** — abstention as valid output; mapping to **insufficient context** is natural. |
| **Constrained / budgeted selection** | Knapsack, submodular maximization for summarization/diversity | **Strong** — formal **budget** on context; greedy approximations well studied. |
| **Irrelevant context robustness** | “Distracting” retrieved passages hurting LM performance | **Strong empirically** — motivates **filter-before-fill**. |
| **Governed / federated memory, isolation** | Access control, multi-tenant DBs; **less** unified “agent memory” theory | **Plausible in systems**; **GNOSIS-specific** enforcement as **first-class** retrieval constraint is the **design contribution**. |
| **Eligibility before similarity** | Case-based reasoning constraints; constrained retrieval; **not** one standard name | **Emerging / composable** — philosophically aligned; **formal universal theorem** may require narrow definitions. |

**Distinction:**

- **Well supported:** staged retrieval, budgets, abstention, harm from irrelevant context.  
- **Emerging / composite:** explicit **eligibility layer** as **hard** gate before embedding rank—**architecturally** clear; **novelty** as a **single** published algorithm is **not** claimed here.  
- **GNOSIS-specific contribution (candidate):** **admissibility-first** ordering + **isolation** + **insufficiency** as contractually valid, in one **specified** pipeline.

---

## 7. Counterexamples (Paper Examples)

Each example supports future **hypotheses** or **theorems** under formalized assumptions.

### 7.1 Semantically similar but inapplicable

**Setup:** \(m_1, m_2\) both embed “mountain hiking safety.” Query asks for **policy in jurisdiction J**. \(m_1\) is tagged **J**; \(m_2\) is **not** in scope for \(J\) but is **closer** in cosine distance to \(q\).

**Failure of naive similarity:** \(m_2\) ranks first.  
**GNOSIS intent:** \(E(m_2 \mid s,\mathcal{P}) < \tau_E\); \(m_2\) excluded before dominance of \(S\).

### 7.2 Stale outranks fresh

**Setup:** Old popular doc \(m_{\text{old}}\) has high similarity; recent correction \(m_{\text{new}}\) has slightly lower \(S\) but **strong** recency and **validity** under \(s\).

**Failure:** Pure similarity prefers \(m_{\text{old}}\).  
**GNOSIS intent:** \(E\) or \(\tilde{S}\) incorporates **time validity**; budgeted set prefers \(m_{\text{new}}\) when policy demands.

### 7.3 Cross-agent leakage

**Setup:** Agent **Bob**’s query is semantically close to **Alice**’s private memory \(m_A\).

**Failure:** Global ANN returns \(m_A\).  
**GNOSIS intent:** \(\mathcal{M}^{(0)}\) excludes \(m_A\) for Bob; **impossible** to rank it.

### 7.4 Over-retrieval drowns signal

**Setup:** 50 marginally related chunks; 2 decisive chunks with moderate \(S\).

**Failure:** Max window stuffing adds noise; LM attends to wrong passages.  
**GNOSIS intent:** **Budget** \(B\) and **knapsack** selection favor **high marginal value**; decomposition may **isolate** sub-queries.

### 7.5 Abstention is correct

**Setup:** No \(m\) passes \(E\) with sufficient support for the claim asked.

**Failure:** System still generates an answer from weak similarity.  
**GNOSIS intent:** \(T < \tau_T\) → \(\omega = \textsf{INSFF}\); **no grounded answer** implied.

---

## 8. Theorem Candidates / Claims

Epistemic labels: **(P)** plausibly provable under explicit assumptions; **(E)** likely empirical only; **(S)** speculative without more formalization.

| Claim | Status |
|-------|--------|
| **C1.** If eligibility \(E\) enforces a **policy** \(\mathcal{P}\) and naive retrieval ignores \(E\), then the set of **inadmissible** memories returned by naive retrieval can be **non-empty** while GNOSIS returns **none** of them. | **(P)** — set inclusion; trivial once \(\mathcal{P}\) formalized. |
| **C2.** Under fixed budget \(B\), **bounded** maximization of relevance subject to \(\mathrm{cost}\) **weakly dominates** unbounded stuffing in **expected irrelevant token mass** if irrelevance correlates with marginal chunks. | **(E)** — needs generative model of noise; **directional** only here. |
| **C3.** Decomposition **reduces** average candidate pool size per sub-query vs monolithic \(q\) under fixed ANN \(k\). | **(E)** — depends on decomposition quality. |
| **C4.** Abstention when \(T < \tau_T\) **dominates** forced answer under a **calibration** loss if false grounding is costlier than abstaining. | **(P)** under explicit cost model; **(E)** for real LMs. |
| **C5.** “Admissibility-first is always better” globally | **(S)** — **false** without restrictions; **counterexample**: overly strict \(E\) drops all useful evidence. |

---

## 9. Open Questions

1. **Closed form for \(E\)** — What minimal sufficient statistics of \((m,s,a,\mathcal{P})\) are needed for **auditable** eligibility (regulatory / enterprise)?  
2. **Sufficiency \(T\)** — Verifier model vs structural rules vs hybrid; **calibration** of \(\tau_T\).  
3. **Decomposition** — Learned vs rule-based; error modes when decomposition is wrong.  
4. **Multi-agent isolation** — Formal **non-interference** properties under concurrent writes.  
5. **Optimality** — Under what loss is the knapsack greedy **within** constant factor (submodularity)?  
6. **Interaction with LLM** — Does abstention at retrieval **reduce** hallucination measurably on **same** generator?

---

## 10. Future Evaluation Plan

### 10.1 Baselines

- **B1:** Isolation-only + **global** top-\(k\) similarity (no eligibility).  
- **B2:** RAG as usual (retrieve top-\(k\) then generate) with **same** generator.  
- **B3:** Eligibility **without** budget (to isolate effect of \(E\) vs \(B\)).  
- **B4:** GNOSIS full pipeline (E + S + budget + sufficiency).

### 10.2 Metrics

- **Grounding / factuality** on labeled queries where support is or is not present.  
- **Abstention quality** — precision/recall of “should abstain” cases.  
- **Cross-agent leakage rate** — must be **zero** on constructed suites.  
- **Token efficiency** — relevant evidence per token vs baselines.  
- **Downstream task success** when applicable.

### 10.3 Synthetic evaluation first

- Controlled corpora with **injected** inapplicable-but-similar items.  
- **Isolation** tests: partitions A/B with overlapping semantics.  
- **Budget** sweeps: measure performance vs \(B\).

### 10.4 Open empirical questions post-design

- Real embeddings and domain shift effects on \(E\) vs \(S\) tradeoffs.  
- Human eval of **insufficient context** UX.  
- Latency cost of multi-stage pipeline vs single ANN call.

---

## Document control

| Item | Note |
|------|------|
| **Implementation** | Out of scope for this document. |
| **Literature citations** | Expand with full bibliographies in a future revision; names in §6 are **pointers to families**, not complete refs. |
| **Alignment with product spec** | Must remain consistent with `docs/specs/GNOSIS_FINAL_CANONICAL.md`; numerical weights in the spec are **one** possible instantiation of \(\tilde{S}\) and \(E\). |

---

*End of algorithm design package (v1).*
