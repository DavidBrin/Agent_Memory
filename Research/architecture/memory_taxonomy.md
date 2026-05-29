# Memory Taxonomy for LLM Agents

This note defines the memory types used throughout the repository. The goal is to avoid treating all memory as a single vector database problem.

## 1. Parametric Memory

**Definition:** Knowledge encoded in model weights during training or fine-tuning.

**Strengths:**

- Fast at inference time
- Broadly available without retrieval calls
- Good for stable world knowledge and learned capabilities

**Weaknesses:**

- Hard to inspect
- Hard to update precisely
- Can become stale
- Cannot easily support user-specific deletion or consent

**Research implication:** Parametric memory is useful for general capability, but it is a poor substrate for rapidly changing user-specific or organization-specific knowledge.

## 2. In-Context Memory

**Definition:** Information placed directly into the model's active context window.

**Strengths:**

- Immediately accessible to the model
- Flexible and easy to modify
- Supports task-specific grounding

**Weaknesses:**

- Expensive at long lengths
- Sensitive to ordering and prompt formatting
- Can distract or overload attention
- Does not persist unless copied elsewhere

**Research implication:** In-context memory is the most direct form of working memory, but it needs careful admission control.

## 3. KV Cache / Inference-Time Memory

**Definition:** Runtime key/value tensors stored by transformer models so previous tokens do not need to be recomputed during autoregressive generation.

**Strengths:**

- Enables efficient continuation of long sequences
- Supports streaming generation
- Extremely fast relative to external retrieval

**Weaknesses:**

- Volatile and session-local
- Memory-intensive on GPU
- Not semantically indexed
- Cannot be queried like a database

**Research implication:** KV cache is a computational memory layer, not a durable semantic memory layer. However, future agents may benefit from hybrid strategies that promote frequently used external memories into active inference state.

## 4. Session Memory

**Definition:** Short-lived memory over the current user session or task episode.

**Strengths:**

- Captures immediate goals, constraints, and corrections
- Often more relevant than old long-term memory
- Can be discarded after task completion

**Weaknesses:**

- Can accidentally be promoted to long-term memory
- May include transient preferences or context-specific instructions

**Research implication:** Session memory needs explicit boundaries so one-off instructions do not become permanent user preferences.

## 5. Episodic Memory

**Definition:** Records of events, observations, interactions, tool calls, failures, and outcomes.

**Strengths:**

- Preserves evidence
- Supports temporal reasoning
- Allows post-hoc auditing
- Enables learning from experience

**Weaknesses:**

- Grows quickly
- Contains noise
- Can include sensitive data
- Requires summarization or retrieval to be useful

**Research implication:** Episodic memory should usually be append-only and evidence-preserving, while derived semantic memory should remain linked back to episodes.

## 6. Semantic Memory

**Definition:** Abstracted facts, beliefs, preferences, and stable world/user knowledge derived from raw episodes or trusted sources.

**Strengths:**

- Compact
- Useful for personalization
- Easier to retrieve than full histories

**Weaknesses:**

- Can become stale
- Can hide uncertainty
- Can lose provenance
- Can conflict with newer information

**Research implication:** Semantic memory must be versioned, sourced, timestamped, and allowed to decay or be contradicted.

## 7. Procedural Memory

**Definition:** Stored skills, workflows, tool-use policies, scripts, code snippets, and action routines.

**Strengths:**

- Converts experience into reusable capability
- Reduces repeated planning overhead
- Enables agent improvement without weight updates

**Weaknesses:**

- Unsafe procedures can persist
- Skills may become obsolete
- Procedures need validation before reuse

**Research implication:** Procedural memory should be sandboxed, tested, and associated with applicability conditions.

## 8. Reflective Memory

**Definition:** Lessons, summaries, critiques, and strategy updates synthesized from prior experience.

**Strengths:**

- Supports learning from failure
- Helps generalize beyond isolated events
- Can improve future planning

**Weaknesses:**

- Can hallucinate false lessons
- Can create self-reinforcing error loops
- Often lacks evidence links

**Research implication:** Reflections should be treated as hypotheses, not facts. They should cite supporting episodes and accumulate confidence through successful reuse.

## 9. Shared Multi-Agent Memory

**Definition:** Memory accessible to multiple agents, teams of agents, or organizational agent systems.

**Strengths:**

- Enables collective learning
- Reduces duplicate discovery
- Supports division of labor

**Weaknesses:**

- Propagates mistakes
- Creates permission and privacy issues
- Increases poisoning risk

**Research implication:** Shared memory needs trust boundaries, source attribution, scopes, review workflows, and quarantine states.

## 10. Structural Memory

**Definition:** Memory represented as graphs, timelines, trees, schemas, or typed objects rather than unstructured text chunks.

**Strengths:**

- Supports relational, causal, temporal, and hierarchical reasoning
- Makes contradictions easier to detect
- Can improve retrieval beyond nearest-neighbor similarity

**Weaknesses:**

- More complex to maintain
- Requires schema design
- May become brittle if over-structured

**Research implication:** Structural memory is likely necessary for reliable long-term agents, but it should coexist with raw episodic evidence.

## Working Principle

The most useful agent memory systems will likely be **multi-tiered**. They should combine volatile high-speed memory, short-term working context, session state, external episodic evidence, distilled semantic memory, procedural skill memory, and structured relationships.
