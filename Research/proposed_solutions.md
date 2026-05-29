# Proposed Solution: Trustworthy Memory OS for Agents

This proposal updates the repository's working solution in light of the recent agent-memory literature through May 2026. The strongest recent evidence points away from a simple vector database and toward a managed memory operating system: hierarchical, structured, temporal, cost-aware, and security-aware.

## Recommendation

Build agent memory as a **Trustworthy Memory OS** with a temporal knowledge graph at its center, surrounded by typed memory stores and lifecycle governance.

The most successful recent technology pattern is:

```text
session traces
    -> gated episodic writes
    -> offline consolidation
    -> temporal entity/fact graph
    -> semantic, procedural, and profile memories
    -> trust-weighted, time-aware retrieval
    -> compact context assembly
    -> use tracking, correction, decay, and deletion
```

The key shift is that memory should be managed as a living system, not retrieved as a pile of snippets.

## Evidence Comparison

| Technology pattern | Strong recent evidence | What it proves | Design decision |
|---|---|---|---|
| Temporal knowledge graph memory | Zep reports better Deep Memory Retrieval performance than MemGPT and large latency reductions on enterprise-style long-term memory tasks. Hindsight reports strong LongMemEval and LoCoMo results using structured memory networks. | Entity, relationship, and time structure beat flat snippet retrieval for multi-session reasoning. | Use a temporal graph as the main durable memory index. |
| Agentic linked memory | A-Mem dynamically links memories using a Zettelkasten-style structure and outperforms baselines on LOCOMO and LongMemEval. | Memory should reorganize itself after use, not remain a static store. | Run consolidation jobs that link, cluster, and revise memory metadata. |
| OS-style hierarchy | MemoryOS reports large LoCoMo gains with short-term, mid-term, and long-term personal memory. MemOS frames memory as a governed resource across parametric, activation, and plaintext memory. | Memory tiers and managed movement between tiers are now a proven design direction. | Use explicit promotion and demotion gates between volatile, episodic, semantic, procedural, graph, and archive layers. |
| Lightweight offline consolidation | LightMem improves memory QA while sharply reducing tokens and API calls. | Durable memory updates should not all happen in the user-facing latency path. | Split online filtering from offline consolidation and memory maintenance. |
| Specialized multimodal stores | MIRIX reports strong ScreenshotVQA and LoCoMo results with six specialized memory types. | Personal agent memory must cover screens, files, workflows, and resources, not just chat text. | Add resource and procedural memory alongside text memories. |
| Learned memory operations | AgeMem trains agents to store, retrieve, update, summarize, and discard memory actions. | Hand-written memory heuristics are useful, but learned policy is the likely next step. | Define memory actions as explicit tools so policies can later be learned or tuned. |
| Benchmark-driven evaluation | LongMemEval, LongMemEval-V2, MemoryAgentBench, MemBench, and LOCOMO evaluate temporal reasoning, updates, abstention, selective forgetting, reflective memory, and web-agent workflows. | Recall-only tests are insufficient. | Evaluate memory utility with update, contradiction, forgetting, provenance, and procedural-reuse tests. |
| Memory security | AgentPoison shows memory and knowledge bases are attack surfaces. | Retrieved memory must be treated as untrusted input. | Add trust scoring, quarantine, instruction stripping, and retrieval-time policy checks. |

## Architecture

### 1. Memory Event Log

The event log is the immutable evidence layer. It stores raw or lightly structured observations:

- user messages and corrections
- assistant actions and tool traces
- task outcomes
- retrieved source snippets
- UI or file observations
- failures and repair attempts

Events are not automatically beliefs. They are evidence candidates.

### 2. Memory Write Gate

Every possible memory write passes through a gate that decides:

- whether the event is worth storing
- which memory type it belongs to
- whether it contains sensitive information
- whether it includes instructions that should be stripped
- whether it conflicts with existing memory
- whether it should remain session-local, become episodic, or enter durable memory

This gate should start heuristic and auditable. Later, it can become a learned policy in the style of AgeMem.

### 3. Typed Memory Stores

Use separate stores because different memories have different failure modes.

| Store | Purpose | Example |
|---|---|---|
| Session memory | Current task state and temporary preferences | "For this report, use APA style." |
| Episodic memory | Time-stamped events and outcomes | "On May 28, a retrieval query returned stale docs." |
| Semantic memory | Stable facts, preferences, and beliefs | "User prefers concise final summaries." |
| Procedural memory | Reusable workflows, prompts, code, and tool routines | "Run benchmark X before updating memory policy." |
| Resource memory | Files, UI screens, documents, screenshots, links, and artifacts | "The pricing spreadsheet lives at path Y." |
| Temporal graph | Entities, relations, claims, contradictions, provenance, and validity windows | "Project A replaced system B after decision C." |
| Archive | Low-access historical evidence | old session traces and superseded facts |

The temporal graph is the coordinating index. Text/vector stores still matter, but graph structure decides what relationships, contradictions, and time windows are relevant.

### 4. Memory Record Schema

Each durable memory should carry enough metadata to be governed:

```yaml
id: stable_memory_id
type: episodic | semantic | procedural | resource | belief | preference | policy
content: concise memory content
source_event_ids: []
entities: []
relations: []
created_at: timestamp
valid_from: timestamp
valid_until: optional timestamp
last_confirmed_at: optional timestamp
confidence: 0.0-1.0
trust_level: private | verified | inferred | shared | untrusted | quarantined
sensitivity: public | personal | confidential | secret
retrieval_count: integer
helpful_count: integer
harmful_count: integer
supersedes: []
contradicts: []
policy_flags: []
```

The schema deliberately separates content from trust, source, time, and utility.

### 5. Retrieval Pipeline

Retrieval should be multi-stage:

1. Parse the task into entities, time constraints, memory types, and risk level.
2. Retrieve candidates from vector search, graph traversal, recent session state, and procedural memory.
3. Filter by trust, sensitivity, validity window, and user permissions.
4. Resolve contradictions by preferring newer, better-sourced, and explicitly confirmed memories.
5. Assemble a compact context packet with citations back to memory IDs.
6. Track whether the retrieved memories helped, hurt, or were ignored.

The context packet should be small and structured. Memory should guide the model, not flood it.

### 6. Offline Consolidation

Follow the LightMem and A-Mem pattern: keep interaction latency low, then do heavier memory work asynchronously.

Consolidation jobs should:

- cluster related episodes by topic, entity, and task
- extract candidate semantic facts and preferences
- update entity summaries
- link memories in the temporal graph
- detect contradictions and stale facts
- compress repeated traces into procedures
- archive low-value memories
- flag suspicious or instruction-like content for review

This is where the system becomes self-maintaining.

### 7. Trust and Security Layer

Long-term memory is part of the security boundary.

Required controls:

- treat retrieved memory as untrusted context, not an instruction source
- strip or quote stored instructions unless they come from trusted policy memory
- quarantine memories created from adversarial, web, or shared-agent sources
- preserve provenance for every semantic and procedural memory
- require explicit user control for deletion, correction, export, and privacy-sensitive promotion
- separate private user memory from shared project or multi-agent memory

### 8. Evaluation Plan

The prototype should be evaluated against the capabilities now used in recent benchmarks:

| Capability | Benchmark inspiration | Test example |
|---|---|---|
| Multi-session recall | LongMemEval, LOCOMO | Remember a preference stated weeks earlier. |
| Temporal reasoning | LongMemEval | Answer which preference was current at a given time. |
| Knowledge updates | LongMemEval, MemoryAgentBench | Replace an old fact after correction. |
| Abstention | LongMemEval | Refuse when memory does not contain evidence. |
| Selective forgetting | MemoryAgentBench | Delete a memory and avoid using it later. |
| Reflective memory | MemBench, Reflexion | Turn a failure into a reusable lesson without overgeneralizing. |
| Procedural memory | Voyager, LongMemEval-V2 | Reuse a validated workflow in a future task. |
| Environment memory | LongMemEval-V2, MIRIX | Remember UI affordances, files, and recurring web-app states. |
| Poison resistance | AgentPoison | Store malicious content without later obeying it. |
| Efficiency | LightMem, Zep | Track latency, token use, API calls, and storage growth. |

## Implementation Sequence

1. **Start with the memory schema and event log.** Without evidence and provenance, later graph and trust work will be brittle.
2. **Add gated episodic and semantic writes.** Keep the first write policy conservative.
3. **Introduce temporal graph indexing.** Link entities, claims, source events, contradictions, and validity windows.
4. **Build trust-weighted retrieval.** Combine vector similarity, graph traversal, recency, source confidence, and permissions.
5. **Add offline consolidation.** Summarize, cluster, link, archive, and promote memories outside the live interaction path.
6. **Add procedural and resource memory.** Store validated workflows, files, UI observations, and environment-specific gotchas.
7. **Benchmark continuously.** Use small local versions of LongMemEval-style tasks before optimizing architecture.
8. **Experiment with learned policy.** Once logs exist, train or tune memory actions instead of relying only on heuristics.

## What Not To Build First

- Do not start with a generic vector database as the core abstraction.
- Do not store every conversation turn as durable semantic memory.
- Do not let retrieved memories behave like system instructions.
- Do not summarize away raw evidence before it is linked and archived.
- Do not optimize only for recall accuracy; include deletion, update, contradiction, abstention, and latency.

## Working Thesis

The best near-term architecture is a temporal, trust-weighted memory operating system. It should combine Zep-style temporal graphs, MemoryOS/MemOS-style hierarchy, A-Mem and LightMem-style consolidation, MIRIX-style typed multimodal stores, AgeMem-style explicit memory actions, and AgentPoison-aware security boundaries.

In short: **memory should be structured like a graph, managed like an operating system, updated like a lifecycle, and treated like an attack surface.**
