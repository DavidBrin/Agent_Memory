# The Evolution of Agent Memory

This note traces how agent memory got to its current shape. It is a chronological companion to [`current_approaches.md`](current_approaches.md), which describes the present landscape without the history, and to [`papers/`](papers/), which holds the per-paper detail.

The useful question when reading a phase is not "what was built" but **what was treated as the unit of memory**, because that choice determines what the system can govern.

## Phase Summary

| Phase | Period | Unit of memory | Central metaphor |
|---|---|---|---|
| 0 | pre-2022 | The prompt | Memory is the context window |
| 1 | 2020-2023 | Document chunk | Memory is search |
| 2 | 2023 | Observation and reflection | Memory is cognitive architecture |
| 3 | late 2023-2024 | Context page | Memory is an operating system |
| 4 | 2024-2025 | Managed record | Memory is a lifecycle |
| 5 | 2025 | Entity, relation, validity window | Memory is structure |
| 6 | 2025-2026 | Memory action | Memory is a learned policy |

## Phase 0: Memory as Context (pre-2022)

Before agents, "memory" meant whatever fit in the prompt. Anything the model knew beyond that came from parametric memory, which is fast, opaque, and effectively unupdatable. The tradeoffs are laid out in [`architecture/memory_taxonomy.md`](architecture/memory_taxonomy.md).

This phase set the constraint that still drives everything else: the context window is a scarce, expensive resource, and the entire field is downstream of that scarcity.

## Phase 1: Memory as Retrieval (2020-2023)

Retrieval-augmented generation made external knowledge accessible without retraining. Applied to agents, it became: embed the conversation, retrieve the nearest chunks, paste them in.

**What it solved:** unbounded knowledge without weight updates, and updateable content.

**What it hid:** the assumption that semantic similarity is a good proxy for relevance. That assumption is still the single most common source of memory failure, catalogued as Retrieval Myopia in [`problems/pain_points.md`](problems/pain_points.md).

## Phase 2: Memory as Cognitive Architecture (2023)

Four papers in roughly one year established the archetypes that everything since has recombined. All four are detailed in [`papers/foundational_papers.md`](papers/foundational_papers.md).

- **Generative Agents** introduced the memory stream plus retrieval scored on recency, relevance, and importance, with periodic reflection synthesizing higher-level conclusions. Memory became a *process* rather than a lookup.
- **Reflexion** made memory a substitute for gradient updates: store the verbal lesson from a failure, retrieve it on the next attempt. Memory became policy improvement.
- **Voyager** stored executable skills. Memory became capability, not just recall.
- **MemoryBank** introduced forgetting as a design goal rather than a limitation.

The step change here is the recognition that agents need *derived* memory, not just stored memory. The unsolved problem it created is that derived memory can be wrong, and nothing in these architectures checks it. Reflection Drift enters the pain-points catalogue at this point and has never left.

## Phase 3: Memory as an Operating System (late 2023-2024)

MemGPT reframed the context window as physical memory and the external store as disk, with the agent issuing explicit paging operations. This is the most durable metaphor in the field, and it produced two lasting contributions: memory movement became an inspectable operation, and tiering became the default architecture. The hierarchy that follows from it is developed in [`architecture/memory_hierarchy.md`](architecture/memory_hierarchy.md).

In parallel, the first surveys formalized memory as a multi-stage pipeline (write, manage, read) rather than a module. See [`papers/survey_notes.md`](papers/survey_notes.md). Once memory is a pipeline, each stage can fail independently, which is what made the next phase necessary.

## Phase 4: Memory as a Lifecycle (2024-2025)

This is the phase where the field stopped assuming more memory is better.

Work on memory management showed that badly managed memory actively degrades agent performance through stale context and amplified prior mistakes. Work on structural memory showed flat stores are insufficient for relational and temporal tasks. A-Mem made the memory system itself agentic, reorganizing its own contents between tasks. Mem0 pushed the same concerns into production terms: cost, latency, deletion, consent.

Two things happened simultaneously that are worth separating:

1. **Writes became gated.** Not every turn deserves durable storage.
2. **Maintenance became continuous.** Memory is edited after it is written, not just appended to.

AgentPoison landed in the same window and added a third concern that runs through everything afterward: stored memory that an agent will later retrieve and act on is an attack surface. Memory security stops being hypothetical once memory is durable.

## Phase 5: Memory as Structure (2025)

The temporal knowledge graph became the strongest single answer to Phase 4's problems. Zep stores facts with explicit validity intervals, so a superseded preference is representable as superseded rather than as a competing duplicate. Hindsight separates world facts, experiences, entity summaries, and beliefs into distinct linked networks. The graph-versus-vector tradeoff is worked through in [`architecture/vector_vs_graph_memory.md`](architecture/vector_vs_graph_memory.md).

At the same time, typing and tiering matured. MemoryOS layered short, mid, and long-term personal memory. MemOS generalized memory into a governed resource spanning parametric, activation, and plaintext forms. MIRIX added specialized multimodal stores for screens, files, and resources. LightMem split online filtering from offline consolidation and demonstrated that the efficiency gains are large, not marginal.

The convergent conclusion across these systems: **time and provenance must be in the schema, not inferred at read time.** Once `valid_from`, `valid_until`, and `source_event_ids` exist as fields, contradiction detection, temporal queries, and deletion propagation all become tractable. Without them, none of the three are.

## Phase 6: Memory as Learned Policy (2025-2026)

Two things define the current frontier.

**Evaluation caught up.** LongMemEval tests updates, temporal reasoning, and abstention rather than recall. MemoryAgentBench adds selective forgetting and test-time learning. MemBench separates factual from reflective memory. LongMemEval-V2 pushes into environment and workflow memory for web agents. The shared finding is that no current method handles all the competencies, which means the architecture question is genuinely open rather than merely unimplemented.

**Policy started being learned.** AgeMem exposes store, retrieve, update, summarize, and discard as trainable actions instead of hand-written heuristics. This is early work, but it reframes the whole stack: the write gate is not a rule set to be perfected, it is a policy to be optimized against measured downstream utility.

The current surveys, tracked in [`papers/recent_papers.md`](papers/recent_papers.md), also argue that the long-term/short-term split is now too coarse, and that memory should be described by form, function, and dynamics instead.

## What Has Not Changed

Six years of progress, and these remain open:

- **Write policy is still crude.** Deciding what deserves to be remembered is the least-developed stage of the pipeline, which is why it is the first thing built in [`../experiments/memory_os_v0/`](../experiments/memory_os_v0/).
- **Corrections append instead of superseding.** Most deployed systems still cannot cleanly retire a fact.
- **Deletion does not propagate.** Removing a source rarely invalidates what was derived from it.
- **Provenance is optional.** Derived beliefs frequently lose their link to the evidence that produced them.
- **Utility is not measured.** Almost nothing records whether a retrieved memory helped, despite being trivially loggable.
- **Inference memory and agent memory are separate fields.** KV cache management and retrieval policy still share no notion of salience, as argued in [`architecture/kv_cache_and_inference_memory.md`](architecture/kv_cache_and_inference_memory.md).

## Direction of Travel

The trajectory across all six phases is one direction: **from storage toward governance.** Each phase moved a decision that used to be implicit into something explicit and inspectable. What to include in context (Phase 1), what to derive (Phase 2), what to page in (Phase 3), what to keep (Phase 4), when it was true (Phase 5), and what action to take on memory at all (Phase 6).

The obvious remaining move is to make trust explicit in the same way. That is the argument of [`proposed_solutions.md`](proposed_solutions.md).

## Open Question

It is not yet clear whether memory ends up as a *service* the agent calls, a *substrate* the agent lives inside, or something absorbed back into the model as parametric or latent state. Phases 3 through 6 assume the first two. The long-term bet on the third is that if models can be cheaply and precisely updated, most of this infrastructure becomes a compatibility layer.

Nothing currently suggests that is close, and the governance requirements — deletion, consent, provenance, audit — argue that an external, inspectable memory layer will remain necessary regardless of how good parametric updating becomes. You cannot show a user a weight.
