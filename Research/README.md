# Research Hub

This directory is the single canonical home for research notes in the Agent_Memory repository. It connects paper summaries, architecture notes, problem analyses, and proposed solutions.

## How to Read This Repository

A useful reading order is:

1. Start with [`../README.md`](../README.md) for the project thesis.
2. Read [`papers/foundational_papers.md`](papers/foundational_papers.md) for the core memory architectures.
3. Read [`papers/recent_papers.md`](papers/recent_papers.md) for 2024-2026 developments.
4. Read [`architecture/memory_taxonomy.md`](architecture/memory_taxonomy.md), [`architecture/memory_hierarchy.md`](architecture/memory_hierarchy.md), and [`architecture/kv_cache_and_inference_memory.md`](architecture/kv_cache_and_inference_memory.md) for conceptual grounding.
5. Read [`problems/pain_points.md`](problems/pain_points.md) for real-world user and system failures.
6. Read [`evolution.md`](evolution.md) for how the field arrived at its current shape.
7. Read [`current_approaches.md`](current_approaches.md) for what is actually built today.
8. Read [`proposed_solutions.md`](proposed_solutions.md) for the main synthesis proposal.
9. Run the stdlib-only [`../experiments/memory_os_v0/`](../experiments/memory_os_v0/)
    prototype for the proposed event log, write gate, temporal store, and retrieval flow.

## Canonical Repository Organization

```text
Research/
├── README.md
├── papers/
│   ├── foundational_papers.md
│   ├── recent_papers.md
│   └── survey_notes.md
├── architecture/
│   ├── memory_taxonomy.md
│   ├── memory_hierarchy.md
│   ├── kv_cache_and_inference_memory.md
│   └── vector_vs_graph_memory.md
├── problems/
│   └── pain_points.md
├── evolution.md
├── current_approaches.md
└── proposed_solutions.md
```

## Deduplication Rule

All long-form research artifacts should live under `Research/`. Top-level repository files should be limited to project navigation and repository-level metadata.

Within `Research/`, the layout rule is:

- **Subfolders hold topic-scoped notes.** A note that is primarily about papers, architecture, or observed problems belongs in `papers/`, `architecture/`, or `problems/`.
- **The root holds cross-cutting syntheses.** `evolution.md`, `current_approaches.md`, and `proposed_solutions.md` each draw on all three subfolders, so they have no natural home inside any one of them.
- **A topic has exactly one canonical file.** Do not create a root-level file that shadows a subfolder note.

### Removed parallel files

An earlier consolidation left six empty root-level files. Four of them shadowed canonical notes and were removed rather than filled, because keeping both copies is exactly what the deduplication rule exists to prevent. If you followed an old link, the canonical locations are:

| Removed | Canonical location |
|---|---|
| `pain-points.md` | [`problems/pain_points.md`](problems/pain_points.md) |
| `kv_cache_inference.md` | [`architecture/kv_cache_and_inference_memory.md`](architecture/kv_cache_and_inference_memory.md) |
| `memory_taxonomy.md` | [`architecture/memory_taxonomy.md`](architecture/memory_taxonomy.md) |
| `papers_summaries.md` | the [`papers/`](papers/) folder as a whole |

The remaining two, `current_approaches.md` and `evolution.md`, had no canonical counterpart, so they were written as real notes instead of removed.

## Current Thesis

Agent memory is moving from passive storage to active governance. A useful memory system must not only retrieve relevant snippets, but also decide what to write, what to trust, what to update, what to compress, what to delete, and what to expose to the agent in a given context.

## Cross-Cutting Questions

- What should count as a durable memory rather than a transient observation?
- How should an agent represent uncertainty, source provenance, and time?
- How should memories be merged, contradicted, versioned, decayed, or deleted?
- How can memory retrieval optimize for usefulness rather than semantic similarity alone?
- What is the right interface between KV cache, context window, session memory, and long-term external memory?
- How can memory systems avoid becoming new attack surfaces?
