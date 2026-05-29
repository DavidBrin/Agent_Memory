# Survey Notes: Agent Memory Literature

This file distills the survey-level view of agent memory. It is meant to connect individual papers into a coherent research map.

## Core Observation

The literature increasingly treats memory as a **system lifecycle**, not a static store. A useful memory stack must support:

1. Observation capture
2. Write filtering
3. Representation
4. Storage
5. Retrieval
6. Context assembly
7. Use tracking
8. Consolidation
9. Updating
10. Forgetting
11. Security review
12. Evaluation

## Major Memory Pipelines

### 1. RAG-style memory

The agent retrieves documents or chunks from an external store and injects them into context.

**Strengths:** simple, scalable, compatible with existing databases.

**Weaknesses:** retrieval is usually based on semantic similarity, which can miss causally relevant or temporally relevant information.

### 2. Episodic agent memory

The agent stores events, observations, interactions, and tool traces.

**Strengths:** preserves experience and supports auditability.

**Weaknesses:** grows quickly and requires abstraction.

### 3. Reflective memory

The agent summarizes episodes into lessons, beliefs, or plans.

**Strengths:** compresses experience into reusable guidance.

**Weaknesses:** can introduce summary drift, hallucinated lessons, and overgeneralization.

### 4. Procedural memory

The agent stores reusable skills, tool-use patterns, and code.

**Strengths:** converts experience into capability.

**Weaknesses:** learned procedures can become stale, unsafe, or overfit to one environment.

### 5. Structural memory

The agent stores memories as graphs, timelines, schemas, or typed objects.

**Strengths:** supports temporal, relational, and causal reasoning.

**Weaknesses:** harder to maintain and benchmark.

## Repeated Findings Across Surveys

- More memory is not automatically better.
- Flat vector databases are useful but incomplete.
- Memory write policies are underdeveloped.
- Long-term personalization needs deletion and consent.
- Benchmarks often test recall rather than useful behavior change.
- Security risks are still under-addressed.

## Gaps in Existing Surveys

1. **KV cache is usually treated separately** from agent memory, even though it is part of the runtime memory hierarchy.
2. **Memory governance** is less developed than memory retrieval.
3. **Contradiction handling** is usually shallow.
4. **Multi-agent memory trust** remains an open problem.
5. **User-facing controls** are not deeply studied.

## Working Synthesis

Agent memory research is converging on a layered model:

```text
Model weights
    +
KV cache / attention state
    +
Prompt / working context
    +
Session state
    +
External episodic store
    +
Semantic memory
    +
Procedural memory
    +
Structured memory graph
    +
Governance layer
```

The governance layer is the least mature but arguably most important part of the stack.
