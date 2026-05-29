# Research Hub

This directory is the single canonical home for research notes in the Agent_Memory repository. It connects paper summaries, architecture notes, problem analyses, proposed solutions, experiments, and draft-writing materials.

## How to Read This Repository

A useful reading order is:

1. Start with [`../README.md`](../README.md) for the project thesis.
2. Read [`papers/foundational_papers.md`](papers/foundational_papers.md) for the core memory architectures.
3. Read [`papers/recent_papers.md`](papers/recent_papers.md) for 2024-2026 developments.
4. Read [`architecture/memory_taxonomy.md`](architecture/memory_taxonomy.md), [`architecture/memory_hierarchy.md`](architecture/memory_hierarchy.md), and [`architecture/kv_cache_and_inference_memory.md`](architecture/kv_cache_and_inference_memory.md) for conceptual grounding.
5. Read [`problems/pain_points.md`](problems/pain_points.md) for real-world user and system failures.
6. Read [`proposals/memory_os.md`](proposals/memory_os.md) for the main synthesis proposal.
7. Read [`roadmap.md`](roadmap.md), [`experiments/prototype_plan.md`](experiments/prototype_plan.md), [`experiments/benchmark_ideas.md`](experiments/benchmark_ideas.md), and [`paper_draft.md`](paper_draft.md) for next steps.

## Canonical Repository Organization

```text
research/
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
│   ├── pain_points.md
│   ├── memory_poisoning.md
│   ├── contradiction_resolution.md
│   └── evaluation_benchmarks.md
├── proposals/
│   ├── memory_os.md
│   ├── causal_memory_graphs.md
│   ├── trust_weighted_retrieval.md
│   └── adaptive_forgetting.md
├── experiments/
│   ├── prototype_plan.md
│   └── benchmark_ideas.md
├── roadmap.md
└── paper_draft.md
```

## Deduplication Rule

All long-form research artifacts should live under `research/`. Top-level files should be limited to project navigation and repository-level metadata. Empty folders are not preserved by Git, so each folder is tracked through at least one markdown file.

## Current Thesis

Agent memory is moving from passive storage to active governance. A useful memory system must not only retrieve relevant snippets, but also decide what to write, what to trust, what to update, what to compress, what to delete, and what to expose to the agent in a given context.

## Cross-Cutting Questions

- What should count as a durable memory rather than a transient observation?
- How should an agent represent uncertainty, source provenance, and time?
- How should memories be merged, contradicted, versioned, decayed, or deleted?
- How can memory retrieval optimize for usefulness rather than semantic similarity alone?
- What is the right interface between KV cache, context window, session memory, and long-term external memory?
- How can memory systems avoid becoming new attack surfaces?
