# Recent Agent Memory Papers and Directions

This file tracks papers and systems that extend the early agent-memory patterns into lifecycle management, structural memory, shared memory, production memory, and memory safety.

## Source List

| Topic | Representative work | Link |
|---|---|---|
| Memory survey | A Survey on the Memory Mechanism of LLM-based Agents | https://arxiv.org/abs/2404.13501 |
| Structural memory | On the Structural Memory of LLM Agents | https://arxiv.org/abs/2412.15266 |
| Shared memory | Memory Sharing for LLM-based Agents | https://arxiv.org/abs/2404.09982 |
| Memory management | How Memory Management Impacts LLM Agents | https://arxiv.org/abs/2505.16067 |
| Agentic memory | A-Mem: Agentic Memory for LLM Agents | https://openreview.net/forum?id=FiM0M8gcct |
| Production memory | Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory | https://arxiv.org/abs/2504.19413 |
| Memory poisoning | AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases | https://proceedings.neurips.cc/paper_files/paper/2024/hash/eb113910e9c3f6242541c1652e30dfd6-Abstract-Conference.html |
| Long conversational memory benchmark | LOCOMO | https://arxiv.org/abs/2402.17753 |

## A Survey on the Memory Mechanism of LLM-based Agents

**Core contribution:** provides a taxonomy of memory mechanisms for LLM agents, including memory writing, storage, retrieval, updating, and use.

### Key insight

The survey makes clear that memory is not a single module. It is a pipeline with several stages, each of which can fail independently:

1. Memory source selection
2. Memory representation
3. Memory storage
4. Retrieval strategy
5. Memory updating
6. Memory utilization
7. Evaluation

### Implication for this repo

The repository should not focus only on vector search. It should treat memory as an end-to-end control loop.

## On the Structural Memory of LLM Agents

**Core contribution:** argues that the structure of memory substantially affects agent performance.

### Key insight

Flat vector stores are often insufficient because many tasks require relational reasoning, temporal ordering, causal dependencies, or abstraction. Structural memory uses graphs, hierarchies, schemas, or other explicit organizations to make stored information more useful.

### Design implications

- Represent events separately from beliefs.
- Store links between memories, not only embeddings.
- Add temporal, causal, source, and task-type edges.
- Allow retrieval to traverse memory structure, not just nearest neighbors.

## Memory Sharing for LLM-based Agents

**Core contribution:** explores memory sharing across multiple agents.

### Key insight

A group of agents can benefit from shared experience, but shared memory introduces contamination risk. A bad memory from one agent can degrade others. Shared memory needs trust, permissions, provenance, and scoped visibility.

### Design implications

- Shared memory should be tiered by trust level.
- Memories should carry source-agent metadata.
- Agents should not automatically treat shared memory as verified truth.
- Shared memory needs quarantine and review mechanisms.

## How Memory Management Impacts LLM Agents

**Core contribution:** studies how different memory management policies affect agent behavior.

### Key insight

More memory is not always better. Poorly managed memory can introduce stale context, distract retrieval, amplify previous mistakes, and degrade performance. Memory should be filtered, compressed, pruned, and audited.

### Design implications

- Track memory utility after retrieval.
- Delete or archive memories that repeatedly fail to help.
- Separate memory creation from durable promotion.
- Maintain memory-health metrics such as redundancy, contradiction density, and retrieval hit quality.

## A-Mem: Agentic Memory for LLM Agents

**Core contribution:** treats memory management as an agentic process rather than a static database operation.

### Key insight

Memory systems can themselves become autonomous: clustering, updating, consolidating, and reorganizing memories over time. This moves agent memory closer to a self-maintaining subsystem.

### Design implications

- Use memory managers that operate between tasks.
- Let memories accumulate metadata through use.
- Add consolidation passes that turn raw episodes into stable semantic memory.
- Keep raw evidence rather than overwriting it with summaries.

## Mem0: Production-Ready Long-Term Memory

**Core contribution:** focuses on scalable, production-oriented long-term memory for AI agents.

### Key insight

Production agent memory needs cost control, latency control, privacy controls, and user-specific personalization. It cannot be only a research prototype.

### Design implications

- Add explicit write gates.
- Store compact user and task memories.
- Separate profile memories from task memories.
- Support deletion, privacy, and consent.

## AgentPoison

**Core contribution:** shows that long-term memory and knowledge bases can be attacked.

### Key insight

If an attacker can cause an agent to store malicious content, the agent may later retrieve and obey it. Memory is therefore part of the system's security boundary.

### Design implications

- Treat all retrieved memory as untrusted input.
- Strip instructions from memories unless explicitly authorized.
- Preserve source and trust metadata.
- Add memory quarantine for suspicious content.
- Run retrieval-time policy checks.

## LOCOMO

**Core contribution:** introduces a benchmark for long-term conversational memory.

### Key insight

A useful memory benchmark needs to test temporal reasoning, fact updates, multi-session recall, and long-range dependencies. Single-turn question answering is too weak to evaluate durable memory.

### Design implications

- Benchmarks should include changing user preferences.
- They should test contradictions and correction handling.
- They should measure whether memories help future tasks, not merely whether the agent can recall isolated facts.

## Synthesis

The recent literature suggests a shift from memory as storage to memory as governance.

Important trends:

1. **From flat to structured memory**: graph, hierarchy, and schema-based memory.
2. **From retrieval to lifecycle management**: write, consolidate, prune, audit, and forget.
3. **From private to shared memory**: multi-agent systems with scoped trust.
4. **From capability to safety boundary**: memory poisoning and privacy become first-class risks.
5. **From toy agents to production agents**: latency, cost, deletion, and user control matter.

## Open Questions

- What should be the unit of memory: event, claim, belief, procedure, tool trace, or user preference?
- When should an episodic memory become semantic memory?
- Can an LLM reliably decide what it should remember?
- How do we prevent memory systems from preserving attacker instructions?
- What benchmarks capture the real utility of long-term memory?
