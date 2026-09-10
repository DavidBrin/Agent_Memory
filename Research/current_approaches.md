# Current Approaches to Agent Memory

This note describes how agent memory is actually built today, as opposed to how it is proposed in papers. It is the bridge between [`papers/recent_papers.md`](papers/recent_papers.md), which tracks individual systems, and [`proposed_solutions.md`](proposed_solutions.md), which argues for a specific architecture.

Scope note: performance numbers referenced here are self-reported by the systems' own papers. They are recorded with sources in [`papers/recent_papers.md`](papers/recent_papers.md) and should not be read as independent replication.

## The Nine Approaches in Practice

| # | Approach | Unit of memory | Typical failure |
|---|---|---|---|
| 1 | Long-context stuffing | Raw turns | Cost, distraction, position sensitivity |
| 2 | Vector RAG over history | Text chunk | Similar but irrelevant retrieval |
| 3 | Rolling summarization | Summary blob | Irreversible detail loss |
| 4 | OS-style paged memory | Context page | Depends on LLM self-management |
| 5 | Extracted fact memory | Atomic fact | Stale and contradictory facts |
| 6 | Temporal knowledge graph | Entity, relation, validity window | Extraction cost and hallucinated edges |
| 7 | Self-organizing memory | Linked note | Consolidation drift |
| 8 | Typed multi-store systems | Type-specific record | Routing errors between stores |
| 9 | Procedural runbooks | Validated workflow | Stale environment assumptions |

### 1. Long-context stuffing

The whole conversation, or as much as fits, goes into the prompt each turn. This remains the default in many shipped products because it requires no infrastructure.

It works until it does not. [LongMemEval](papers/recent_papers.md) reports roughly 30% accuracy degradation for both commercial assistants and long-context models on sustained interaction, and [`architecture/kv_cache_and_inference_memory.md`](architecture/kv_cache_and_inference_memory.md) explains the compute side: every additional token of history is paid for in KV cache footprint and per-turn latency.

### 2. Vector RAG over conversation history

Chat turns are chunked, embedded, and retrieved by cosine similarity. This is the most common "we have memory" implementation.

What it gets right: it scales, it reuses existing infrastructure, and it is a reasonable bootstrap.

Where it breaks is documented in [`problems/pain_points.md`](problems/pain_points.md) under Retrieval Myopia. Similarity is not relevance. Similar wording with different intent, the same task under different constraints, and the same code in a different environment all score highly and all mislead. Vector stores also have no native representation of time, source, or contradiction, which means stale memory and corrected memory look identical to the retriever.

### 3. Rolling summarization and state blobs

The system periodically compresses history into a summary and carries that forward, sometimes alongside a structured "user profile" blob.

This is cheap and bounded, but it is lossy in one direction only. Once evidence has been summarized away it cannot be recovered, which is exactly the failure [`proposed_solutions.md`](proposed_solutions.md) warns against in "What Not To Build First." It also has no mechanism for detecting that the summary itself is wrong.

### 4. OS-style paged memory

MemGPT, and the Letta line of work that followed it, treats the context window as scarce physical memory and gives the agent tool calls to page information between core context and an archival store. See [`papers/foundational_papers.md`](papers/foundational_papers.md).

This was the conceptual unlock: memory movement became an explicit, inspectable operation rather than an implicit side effect. The weakness is that it delegates policy to the model. If the LLM decides badly about what to page in, there is no independent gate to catch it.

### 5. Extracted fact memory services

Mem0, and the memory features in mainstream assistants, run an extraction step over each interaction and store compact atomic facts and preferences rather than raw turns. Retrieval then pulls a handful of facts into the prompt.

This is the current production mainstream, and it is a genuine improvement: memory becomes small, human-readable, and editable. Its unsolved problems are stated directly in the pain-points note: facts go stale, corrections create contradictions rather than replacing the original, and deletion does not propagate to summaries derived from the deleted fact.

### 6. Temporal knowledge graph memory

Zep, built on Graphiti, stores entities, relationships, and facts with explicit validity intervals: when a fact was true, when it was learned, and when it was superseded. Hindsight takes a related position, separating world facts, agent experiences, entity summaries, and evolving beliefs into linked networks.

This is the approach with the strongest current evidence for multi-session and temporal reasoning, and it is the one [`proposed_solutions.md`](proposed_solutions.md) adopts as the coordinating index. The costs are real: extraction requires model calls, edges can be hallucinated, and graph maintenance is ongoing work rather than a one-time write. The tradeoffs are compared in detail in [`architecture/vector_vs_graph_memory.md`](architecture/vector_vs_graph_memory.md).

### 7. Self-organizing and offline-consolidated memory

A-Mem links memories Zettelkasten-style and revises that structure as new memories arrive. LightMem splits the work by latency budget: lightweight filtering online, heavier consolidation offline in a "sleep-time" pass, reporting large token and API-call reductions.

The shared insight is that memory maintenance does not belong in the user-facing request path. This is the least-adopted good idea in the current landscape, largely because it requires background infrastructure that a single-process agent does not have.

### 8. Typed multi-store systems

MIRIX runs six specialized stores including resource memory and a knowledge vault. MemoryOS uses short, mid, and long-term personal memory tiers. MemOS generalizes further, treating parametric, activation, and plaintext memory as one governed resource with a common object abstraction.

The premise, argued in [`architecture/memory_taxonomy.md`](architecture/memory_taxonomy.md), is that different memory types have different failure modes and therefore need different policies. The practical cost is a routing problem: something must decide which store a new memory belongs to, and that decision is now a new place to be wrong.

### 9. Procedural and environment memory

Voyager established the skill library. LongMemEval-V2 extends the idea to web agents, asking whether an agent can remember interface affordances, workflows, and environment gotchas across hundreds of trajectories; its strongest reported method is runbook-based rather than retrieval-based.

Procedural memory converts experience into capability, which is a qualitatively different payoff than recall. It also carries the safety burden described under Procedural Memory Safety in [`problems/pain_points.md`](problems/pain_points.md): a workflow that succeeded once may be unsafe on reuse.

## Learned Memory Policy: The Newest Category

AgeMem exposes store, retrieve, update, summarize, and discard as tool-like actions and trains the policy with reinforcement learning rather than hand-writing heuristics. This is early, but it changes what a memory system is: not a database with rules attached, but a learned control loop.

The practical implication for anyone building now is architectural rather than immediate. Memory operations should be defined as explicit, named, loggable actions from the start, so that heuristic gates can later be replaced by learned ones without redesigning the system.

## What Almost No Deployed System Does Yet

This is the gap the repository is interested in.

- **Trust scoring at retrieval time.** AgentPoison showed memory is an attack surface. Most systems still treat a memory written from a scraped web page identically to one stated by the user.
- **Contradiction as a first-class relation.** Corrections usually append rather than supersede.
- **Deletion propagation.** Deleting a source memory rarely invalidates the summaries and beliefs derived from it.
- **Utility feedback.** Almost nothing tracks whether a retrieved memory actually helped, despite this being cheap to log.
- **Abstention.** Systems retrieve their top-k regardless of whether the evidence supports an answer at all.
- **Cache-aware assembly.** Retrieval and inference-state management are designed by separate teams with no shared notion of salience.

## Where This Repository Sits

[`proposed_solutions.md`](proposed_solutions.md) argues for combining approaches 6, 7, and 8 under an explicit governance layer, then treating the write gate and retrieval filter as the primary design surface rather than the storage engine.

The bet is that the storage substrate is close to solved and the lifecycle is not. A first implementation of that bet lives in [`../experiments/memory_os_v0/`](../experiments/memory_os_v0/), which builds the event log, write gate, temporal index, and trust-weighted retrieval as working code so the governance claims can be tested rather than asserted.
