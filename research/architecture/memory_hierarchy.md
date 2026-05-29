# Agent Memory Hierarchy

A mature agent memory system should be treated as a hierarchy rather than a single store. Different memory layers have different latency, cost, durability, trust, and governance properties.

## Working Hierarchy

```text
1. Model weights / parametric memory
2. KV cache / inference state
3. Prompt / active context
4. Scratchpad / working state
5. Session memory
6. Long-term episodic memory
7. Semantic memory
8. Procedural memory
9. Structured memory graph
10. Cold archival store
```

## Layer 1: Parametric Memory

This is the model's built-in knowledge and capabilities. It is fast and always available, but difficult to inspect, update, delete, or personalize.

**Best for:** stable general knowledge, linguistic competence, reasoning priors, tool-use priors.

**Bad for:** personal facts, recent information, compliance-sensitive data, user-specific preferences.

## Layer 2: KV Cache / Inference State

KV cache stores attention keys and values for tokens already processed during generation. It is not a durable knowledge base, but it is the fastest available memory layer during inference.

**Best for:** fast continuation, local coherence, streaming generation.

**Bad for:** durable storage, semantic search, cross-session memory.

## Layer 3: Active Context

The active prompt is the model's immediate working memory. Anything included here can directly influence generation.

**Best for:** current task instructions, retrieved memories, tool outputs, constraints, user preferences relevant to the current task.

**Bad for:** unfiltered memory dumps, stale histories, irrelevant retrieved chunks.

## Layer 4: Scratchpad / Working State

The scratchpad is a transient reasoning and planning layer. It may include plans, intermediate results, hypotheses, or task-local notes.

**Best for:** multi-step problem solving, tool planning, task decomposition.

**Bad for:** long-term storage, durable user profile updates.

## Layer 5: Session Memory

Session memory persists within a conversation or task episode. It should capture local goals, decisions, corrections, and constraints.

**Best for:** temporary user preferences, current project assumptions, recent decisions.

**Bad for:** permanent profile updates unless explicitly promoted.

## Layer 6: Episodic Memory

Episodic memory stores raw or lightly structured records of events: interactions, observations, tool calls, outcomes, errors, and user feedback.

**Best for:** auditability, temporal reasoning, evidence preservation, learning from experience.

**Bad for:** direct prompt stuffing, permanent beliefs without consolidation.

## Layer 7: Semantic Memory

Semantic memory stores distilled facts, preferences, beliefs, and stable knowledge. It should be linked to evidence and versioned over time.

**Best for:** personalization, durable project facts, stable preferences, reusable context.

**Bad for:** uncertain facts, volatile information, unsupported inferences.

## Layer 8: Procedural Memory

Procedural memory stores reusable actions: workflows, code, tool-use routines, prompts, plans, and validated skills.

**Best for:** repeated tasks, tool automation, environment-specific capability.

**Bad for:** unsafe procedures, untested scripts, brittle routines.

## Layer 9: Structured Memory Graph

A structured graph links memories by time, source, task, entity, causal relation, contradiction, dependency, and provenance.

**Best for:** reasoning over relationships, contradiction detection, temporal updates, causal retrieval.

**Bad for:** very small or purely ad hoc tasks where structure would add overhead.

## Layer 10: Cold Archival Store

Cold storage keeps low-access raw records or historical data. It is durable but should not be retrieved by default.

**Best for:** compliance logs, old project history, audit trails, rarely used evidence.

**Bad for:** low-latency interaction.

## Promotion and Demotion Policies

A useful memory hierarchy needs explicit transitions:

- **Observation -> episodic memory** when an event is worth preserving.
- **Episodic -> semantic memory** when a pattern is stable, useful, and supported by evidence.
- **Semantic -> active context** when a memory is relevant, trusted, and timely.
- **Procedure -> procedural memory** when a repeated action chain succeeds across multiple contexts.
- **Long-term -> archive** when memory is stale or rarely useful.
- **Any layer -> deletion** when required by privacy, correction, or user control.

## Main Design Principle

Memory should flow between layers only through explicit gates. The most dangerous failure mode is silent promotion: transient or malicious information becomes durable memory without review.
