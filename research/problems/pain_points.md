# Agent Memory Pain Points

This file identifies the recurring problems that agentic users and system builders face when memory becomes persistent.

## 1. Memory Bloat

### Problem

Agents that store everything eventually retrieve too much, retrieve the wrong things, or spend excessive tokens on irrelevant history.

### User-facing symptom

The agent brings up old context that no longer matters, becomes slower, or seems distracted by stale information.

### Fine-grained failure modes

- Redundant memories crowd out useful memories.
- Temporary task constraints become permanent assumptions.
- Old tool traces pollute future planning.
- Retrieval returns semantically similar but operationally irrelevant items.

### Possible approaches

- Write gating before storage
- Utility tracking after retrieval
- Decay functions
- Compression and summarization
- Archival tiers
- Memory health audits

## 2. Retrieval Myopia

### Problem

Vector similarity often retrieves memories that look textually similar but are not useful for the current task.

### User-facing symptom

The agent says something related but unhelpful, or applies an old example to a task where it does not belong.

### Fine-grained failure modes

- Similar wording, different intent
- Similar task, different constraints
- Similar user, different project
- Similar code, different environment

### Possible approaches

- Combine vector similarity with task-state matching
- Add graph expansion and entity filters
- Rerank by recency, source, confidence, and goal relevance
- Track retrieval usefulness over time

## 3. Stale Memory

### Problem

Long-term agents preserve information after it has expired.

### User-facing symptom

The agent remembers an old preference, old deadline, old address, deprecated API, or past project decision as if it were current.

### Fine-grained failure modes

- Preferences change without explicit correction.
- Project facts are superseded.
- External facts drift.
- Tool schemas and APIs evolve.

### Possible approaches

- `valid_until` metadata
- time-aware retrieval
- recency-dependent confidence
- user-visible memory editing
- contradiction-triggered memory review

## 4. Contradictions

### Problem

Agents store mutually inconsistent beliefs and retrieve whichever one happens to score highly.

### User-facing symptom

The agent seems inconsistent across sessions, remembers both old and new preferences, or cannot resolve corrected facts.

### Fine-grained failure modes

- Old memory says the user prefers X; new memory says Y.
- One memory says a task is done; another says it is blocked.
- Summaries omit the evidence needed to resolve the conflict.

### Possible approaches

- claim-level memory records
- contradiction edges
- belief versioning
- confidence arbitration
- evidence-linked semantic memory

## 5. Reflection Drift

### Problem

Agents summarize experience into lessons, but those summaries may be incomplete, exaggerated, or false.

### User-facing symptom

The agent overlearns from one event, becomes rigid, or repeats an incorrect lesson.

### Fine-grained failure modes

- A failed attempt becomes an overgeneralized rule.
- A summary removes an important exception.
- A hallucinated reflection is treated as ground truth.

### Possible approaches

- Treat reflections as hypotheses
- Link reflections to supporting episodes
- Require repeated successful reuse before promotion
- Keep raw episodes intact

## 6. Memory Poisoning

### Problem

If malicious or low-quality content is stored, the agent may later retrieve and follow it.

### User-facing symptom

The agent unexpectedly follows old instructions, leaks information, or behaves according to a malicious memory.

### Fine-grained failure modes

- Prompt injection is stored as a memory.
- A malicious web page becomes trusted context.
- One agent pollutes shared memory used by another.
- Retrieved memory contains executable instructions disguised as facts.

### Possible approaches

- provenance tracking
- trust scoring
- quarantine states
- instruction stripping
- retrieval-time policy checks
- source-aware access control

## 7. Privacy and Consent

### Problem

Personalization requires remembering user-specific information, but users need control over what is stored, used, shared, and deleted.

### User-facing symptom

The agent remembers something surprising, sensitive, or out of context.

### Fine-grained failure modes

- Sensitive content stored without explicit user intent.
- Memory shared across contexts where it does not belong.
- User deletion does not propagate to derived summaries.

### Possible approaches

- memory scopes
- deletion propagation
- user-visible memory ledger
- sensitivity classification
- consent gates for durable storage

## 8. Procedural Memory Safety

### Problem

Agents can store workflows or code-like procedures that may later be reused unsafely.

### User-facing symptom

The agent repeats an outdated workflow, runs unsafe commands, or applies an automation in the wrong context.

### Fine-grained failure modes

- Skill applicability conditions are missing.
- Procedure was successful once but not robust.
- Tool permissions have changed.
- Environment assumptions are stale.

### Possible approaches

- sandboxed skill testing
- skill versioning
- applicability predicates
- safety review before execution
- deprecation policies

## 9. Multi-Agent Contamination

### Problem

Shared memory lets agents learn collectively, but also lets errors propagate collectively.

### User-facing symptom

One agent's mistake appears in another agent's work.

### Fine-grained failure modes

- Shared memory lacks trust levels.
- Agent-specific assumptions become global.
- No review separates private, team, and system-wide memories.

### Possible approaches

- scoped shared memory
- source-agent metadata
- confidence and trust thresholds
- quarantine before global promotion

## 10. Benchmark Mismatch

### Problem

Many benchmarks test factual recall, but users need memory that improves real behavior.

### User-facing symptom

A system scores well on memory QA but still fails in realistic long-running work.

### Fine-grained failure modes

- Benchmarks ignore changing preferences.
- They do not test harmful retrieval.
- They under-test deletion, privacy, and contradictions.
- They measure recall rather than task outcomes.

### Possible approaches

- task-based memory benchmarks
- contradiction and correction suites
- poisoning-resistance benchmarks
- longitudinal preference-change tests
- cost/latency measurements

## Priority Problems

The highest-leverage problems for this repository are:

1. Memory write gating
2. Contradiction-aware semantic memory
3. Trust-weighted retrieval
4. Adaptive forgetting
5. Cache-aware context assembly
6. Benchmarks that measure behavior, not recall alone
