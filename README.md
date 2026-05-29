# Agent_Memory

Research notes, paper summaries, architectural analysis, experiments, and original proposals on **memory for AI agents**.

This repository studies agent memory across the full stack: from LLM inference-time memory such as KV cache, to in-context memory, retrieval-augmented generation, long-term episodic memory, semantic memory, procedural memory, reflection, shared multi-agent memory, and self-maintaining memory systems.

## Core Question

How should AI agents remember, forget, retrieve, update, verify, and use information over long periods of time?

The working hypothesis of this repo is that agent memory is becoming less like a simple vector database and more like a managed cognitive operating system: layered, structured, self-editing, security-aware, and optimized across latency, cost, reliability, and trust.

## Current Research Hub

All long-form research artifacts live under [`Research/`](Research/). Start there for the organized reading path.

Important entry points:

- [`Research/README.md`](Research/README.md) — research hub and navigation
- [`Research/papers/foundational_papers.md`](Research/papers/foundational_papers.md) — foundational papers
- [`Research/papers/recent_papers.md`](Research/papers/recent_papers.md) — recent papers and directions
- [`Research/architecture/memory_taxonomy.md`](Research/architecture/memory_taxonomy.md) — memory type taxonomy
- [`Research/architecture/memory_hierarchy.md`](Research/architecture/memory_hierarchy.md) — tiered memory architecture
- [`Research/architecture/kv_cache_and_inference_memory.md`](Research/architecture/kv_cache_and_inference_memory.md) — KV cache and inference-time memory
- [`Research/problems/pain_points.md`](Research/problems/pain_points.md) — real-world problems for agent users
- [`Research/proposed_solutions.md`](Research/proposed_solutions.md) — proposed memory operating-system architecture

## Graphify Indexing

This repo includes a portable Graphify wrapper for building and querying a local knowledge graph over the research docs.

```bash
scripts/graphify update .
scripts/graphify query "What is the proposed memory architecture?"
scripts/graphify explain "Trustworthy Memory OS"
```

The first run creates `.venv/` and installs the pinned development dependency from [`requirements-dev.txt`](requirements-dev.txt). Generated graph files live in `graphify-out/` and are intentionally ignored by Git.

For Codex auto-check hooks on your machine, run:

```bash
scripts/graphify codex install
```

That writes local `.codex/` hook config with machine-specific paths, so it is not committed.

## Research Scope

This project covers:

- **Foundational agent-memory papers** such as Generative Agents, MemGPT, MemoryBank, Reflexion, and Voyager
- **Recent memory-management work** on structural memory, memory sharing, self-organizing memory, memory pruning, and memory poisoning
- **Memory architectures** including vector memory, graph memory, hierarchical memory, scratchpads, skill libraries, and archival stores
- **Inference-time memory** such as KV cache, attention state, long-context mechanisms, compression, sliding-window attention, and sparse attention
- **Practical agent-user pain points** including stale memories, hallucinated memories, privacy risks, contradiction handling, retrieval failures, and memory bloat
- **Future design proposals** for robust, personalized, long-running agents

## Memory Types Considered

| Memory Type | Description | Key Issues |
|---|---|---|
| Parametric memory | Knowledge stored in model weights | Hard to update, opaque, stale |
| In-context memory | Information inside the prompt/context window | Expensive, limited, order-sensitive |
| KV cache | Runtime attention state used during inference | Fast but volatile, memory-intensive |
| Vector memory | Embedding-based external retrieval | Similarity is not always relevance |
| Episodic memory | Records of events, interactions, and experiences | Bloat, noise, privacy, temporal drift |
| Semantic memory | Abstracted facts and beliefs | Contradictions, provenance, staleness |
| Procedural memory | Skills, tools, workflows, executable routines | Verification, transferability, safety |
| Reflective memory | Lessons synthesized from prior experience | Reflection drift, self-reinforcing errors |
| Shared memory | Multi-agent collective state | Contamination, access control, trust |
| Structural memory | Graphs, hierarchies, schemas, and causal links | Complexity, maintenance, evaluation |

## Key Research Themes

### 1. Memory is not just retrieval

Early agent systems often treated memory as a vector search problem. Recent systems increasingly show that retrieval alone is insufficient. Effective memory requires lifecycle management: creation, consolidation, prioritization, contradiction detection, pruning, access control, and forgetting.

### 2. Forgetting is a feature

Unbounded memory accumulation can degrade agent performance. Agents need principled forgetting policies, memory audits, staleness detection, and mechanisms for separating durable knowledge from transient interaction traces.

### 3. Structure matters

Flat memory stores are easy to implement but weak for reasoning. Graphs, hierarchies, timelines, causal links, and typed memory objects may support more reliable long-term behavior than unstructured embedding stores.

### 4. Memory is a security boundary

Long-term memory creates new attack surfaces. Poisoned memories, malicious instructions stored as memories, privacy leakage, and cross-agent contamination are major risks for production systems.

### 5. Agent memory is becoming multi-tiered

A mature agent memory stack may resemble a computer memory hierarchy:

```text
KV cache / inference state
        ↓
Working context
        ↓
Session memory
        ↓
Long-term episodic memory
        ↓
Semantic + procedural memory
        ↓
Cold archival storage
```

## Working Problems

This repo is especially interested in fine-grained problems such as:

- How should an agent decide whether a memory is worth storing?
- How should old memories decay, compress, or disappear?
- How should agents detect contradictions between memories?
- How should memories be versioned and traced back to evidence?
- How should agents distinguish user preferences from one-off instructions?
- How can agents avoid retrieving semantically similar but task-irrelevant memories?
- How can procedural memory be safely learned and reused?
- How should KV cache, long-context memory, and external memory interact?
- How can shared multi-agent memory avoid contamination?
- What benchmarks actually measure useful long-term memory?

## Emerging Direction

The next generation of agent memory systems will likely be:

- **Self-maintaining**: able to audit, compress, and reorganize themselves
- **Contradiction-aware**: able to represent uncertainty and resolve conflicting claims
- **Trust-weighted**: retrieval and use depend on source reliability and evidence
- **Causally structured**: memories are linked by dependency, not only similarity
- **Privacy-preserving**: sensitive memory is scoped, encrypted, permissioned, or forgettable
- **Multi-modal**: memory spans text, code, documents, images, audio, tools, and actions
- **Multi-tiered**: fast volatile memory and slow durable memory work together

## Status

Early-stage research repository. The current structure is consolidated under `Research/` so papers, architecture notes, problem analyses, and proposed solutions do not diverge across parallel folders.
