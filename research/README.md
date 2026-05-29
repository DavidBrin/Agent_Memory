# Research Hub

This directory is the navigation layer for the Agent_Memory repository. It connects paper summaries, architecture notes, problem analyses, proposed solutions, experiments, and draft-writing materials.

## How to Read This Repository

A useful reading order is:

1. Start with [`../README.md`](../README.md) for the project thesis.
2. Read [`../papers/foundational_papers.md`](../papers/foundational_papers.md) for the core memory architectures.
3. Read [`../papers/recent_papers.md`](../papers/recent_papers.md) for 2024-2026 developments.
4. Read [`../architecture/memory_taxonomy.md`](../architecture/memory_taxonomy.md) and [`../architecture/memory_hierarchy.md`](../architecture/memory_hierarchy.md) for conceptual grounding.
5. Read [`../problems/pain_points.md`](../problems/pain_points.md) for real-world user and system failures.
6. Read [`../proposals/memory_os.md`](../proposals/memory_os.md) for the main synthesis proposal.
7. Read [`../roadmap.md`](../roadmap.md), [`../experiments/prototype_plan.md`](../experiments/prototype_plan.md), and [`../paper_draft.md`](../paper_draft.md) for next steps.

## Repository Organization

```text
papers/        Literature summaries and survey notes
architecture/  Memory-system abstractions and implementation patterns
problems/      Pain points, threat models, contradictions, evaluation gaps
proposals/     Original design proposals and fine-grained solution sketches
experiments/   Benchmark and prototype plans
roadmap.md     Formal research roadmap
paper_draft.md Draft research-paper skeleton
```

## Current Thesis

Agent memory is moving from passive storage to active governance. A useful memory system must not only retrieve relevant snippets, but also decide what to write, what to trust, what to update, what to compress, what to delete, and what to expose to the agent in a given context.

## Current State of the Research Folder

Before this organization pass, GitHub search surfaced only the top-level README for the term `research`, so this tracked `research/` hub is being created as the central index. Git does not preserve empty folders, so any previously empty local `research/` directory would not have appeared in GitHub until a file was committed.

## Cross-Cutting Questions

- What should count as a durable memory rather than a transient observation?
- How should an agent represent uncertainty, source provenance, and time?
- How should memories be merged, contradicted, versioned, decayed, or deleted?
- How can memory retrieval optimize for usefulness rather than semantic similarity alone?
- What is the right interface between KV cache, context window, session memory, and long-term external memory?
- How can memory systems avoid becoming new attack surfaces?
