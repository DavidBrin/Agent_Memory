# Research Hub

This directory is the single canonical home for research notes in the Agent_Memory repository. It connects paper summaries, architecture notes, problem analyses, and proposed solutions.

## How to Read This Repository

A useful reading order is:

1. Start with [`../README.md`](../README.md) for the project thesis.
2. Read [`papers/foundational_papers.md`](papers/foundational_papers.md) for the core memory architectures.
3. Read [`papers/recent_papers.md`](papers/recent_papers.md) for 2024-2026 developments.
4. Read [`architecture/memory_taxonomy.md`](architecture/memory_taxonomy.md), [`architecture/memory_hierarchy.md`](architecture/memory_hierarchy.md), and [`architecture/kv_cache_and_inference_memory.md`](architecture/kv_cache_and_inference_memory.md) for conceptual grounding.
5. Read [`problems/pain_points.md`](problems/pain_points.md) for real-world user and system failures.
6. Read [`proposed_solutions.md`](proposed_solutions.md) for the main synthesis proposal.

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
├── pain-points.md
├── proposed_solutions.md
├── current_approaches.md
├── papers_summaries.md
├── evolution.md
├── kv_cache_inference.md
└── memory_taxonomy.md
```

## Deduplication Rule

All long-form research artifacts should live under `Research/`. Top-level files should be limited to project navigation and repository-level metadata.

## Current Thesis

Agent memory is moving from passive storage to active governance. A useful memory system must not only retrieve relevant snippets, but also decide what to write, what to trust, what to update, what to compress, what to delete, and what to expose to the agent in a given context.

## Cross-Cutting Questions

- What should count as a durable memory rather than a transient observation?
- How should an agent represent uncertainty, source provenance, and time?
- How should memories be merged, contradicted, versioned, decayed, or deleted?
- How can memory retrieval optimize for usefulness rather than semantic similarity alone?
- What is the right interface between KV cache, context window, session memory, and long-term external memory?
- How can memory systems avoid becoming new attack surfaces?
