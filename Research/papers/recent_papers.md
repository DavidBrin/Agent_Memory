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
| Temporal graph memory | Zep: A Temporal Knowledge Graph Architecture for Agent Memory | https://arxiv.org/abs/2501.13956 |
| Structured reasoning memory | Hindsight is 20/20: Building Agent Memory that Retains, Recalls, and Reflects | https://arxiv.org/abs/2512.12818 |
| Memory operating system | Memory OS of AI Agent | https://arxiv.org/abs/2506.06326 |
| Memory operating system | MemOS: An Operating System for Memory-Augmented Generation in Large Language Models | https://arxiv.org/abs/2505.22101 |
| Efficient consolidation | LightMem: Lightweight and Efficient Memory-Augmented Generation | https://arxiv.org/abs/2510.18866 |
| Multimodal memory | MIRIX: Multi-Agent Memory System for LLM-Based Agents | https://arxiv.org/abs/2507.07957 |
| Learned memory policy | Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents | https://arxiv.org/abs/2601.01885 |
| Memory poisoning | AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases | https://proceedings.neurips.cc/paper_files/paper/2024/hash/eb113910e9c3f6242541c1652e30dfd6-Abstract-Conference.html |
| Long conversational memory benchmark | LOCOMO | https://arxiv.org/abs/2402.17753 |
| Long-term chat memory benchmark | LongMemEval | https://arxiv.org/abs/2410.10813 |
| Agent-environment memory benchmark | LongMemEval-V2 | https://arxiv.org/abs/2605.12493 |
| Memory-agent benchmark | MemoryAgentBench | https://openreview.net/forum?id=DT7JyQC3MR |
| Multi-level memory benchmark | MemBench | https://aclanthology.org/2025.findings-acl.989/ |
| Current survey | Memory in the Age of AI Agents | https://arxiv.org/abs/2512.13564 |
| Current survey | Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers | https://arxiv.org/html/2603.07670v1 |

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

## Zep: Temporal Knowledge Graph Memory

**Core contribution:** introduces a production-oriented agent memory service built around Graphiti, a temporally aware knowledge graph engine.

### Key insight

The paper reports that dynamic enterprise memory needs more than static document retrieval: it must integrate conversations and business data while preserving historical relationships. Zep reports 94.8% on the Deep Memory Retrieval benchmark versus 93.4% for MemGPT, and up to 18.5% accuracy improvement with 90% lower latency on LongMemEval-style enterprise tasks.

### Design implications

- Store entities, facts, and relationships in a temporal graph.
- Preserve when a fact was true, when it was learned, and when it was superseded.
- Use graph traversal and temporal filters alongside vector retrieval.
- Treat enterprise memory as continuously updated operational data, not static RAG content.

## Hindsight

**Core contribution:** treats agent memory as a structured substrate for reasoning rather than as top-k snippets injected into a stateless prompt.

### Key insight

Hindsight separates world facts, agent experiences, entity summaries, and evolving beliefs into logical networks. It reports strong benchmark results: 83.6% overall accuracy with an open-source 20B model versus 39% for a full-context baseline using the same backbone, 91.4% on LongMemEval with a larger backbone, and up to 89.61% on LoCoMo.

### Design implications

- Separate evidence from inference.
- Keep beliefs traceable to source facts and experiences.
- Add explicit retain, recall, and reflect operations.
- Prefer explainable memory answers that can cite memory provenance.

## MemoryOS

**Core contribution:** proposes an OS-inspired memory hierarchy for personalized agents.

### Key insight

MemoryOS organizes memory into short-term, mid-term, and long-term personal memory with storage, updating, retrieval, and generation modules. On LoCoMo, the EMNLP 2025 version reports average improvements of 48.36% F1 and 46.18% BLEU-1 over baselines on GPT-4o-mini.

### Design implications

- Use explicit memory tiers rather than a single store.
- Promote memories through staged updates.
- Use page-like organization for long-term personal memory.
- Keep personalization as a managed lifecycle, not a prompt append.

## MemOS

**Core contribution:** elevates memory to a first-class operational resource for memory-augmented generation.

### Key insight

MemOS argues that RAG lacks lifecycle management and multimodal integration. It proposes governance across parametric memory, activation memory, and plaintext memory, with MemCube as a standardized abstraction for tracking, fusion, and migration of heterogeneous memory.

### Design implications

- Model memory as a resource with identity, lifecycle, and governance.
- Track memory lineage across parametric, activation, and plaintext forms.
- Use a standardized memory object that can be moved, fused, audited, and exposed through policy.
- Connect agent memory to inference-time memory instead of treating them as separate subjects.

## LightMem

**Core contribution:** reduces the runtime cost of memory by separating fast online filtering from offline consolidation.

### Key insight

LightMem uses sensory memory, topic-aware short-term memory, and sleep-time long-term updates. It reports improved QA accuracy on LongMemEval and LoCoMo while reducing token usage and API calls by large factors, including up to 38x / 20.9x total token reduction and up to 30x / 55.5x fewer API calls.

### Design implications

- Do lightweight filtering during interaction.
- Move expensive consolidation out of the user-facing latency path.
- Cluster and summarize by topic before durable promotion.
- Measure memory systems on latency and cost as well as answer quality.

## MIRIX

**Core contribution:** introduces a multimodal, multi-agent memory system with six specialized memory types.

### Key insight

MIRIX separates Core, Episodic, Semantic, Procedural, Resource Memory, and Knowledge Vault, coordinated by a multi-agent framework. It reports 35% higher accuracy than RAG on ScreenshotVQA while reducing storage by 99.9%, and 85.4% on LoCoMo.

### Design implications

- Do not limit agent memory to text.
- Use different memory managers for different memory types.
- Store screen, file, workflow, and resource memories under separate policies.
- Favor local storage and visualization for privacy-sensitive personal memory.

## AgeMem

**Core contribution:** learns unified long-term and short-term memory management as part of the agent policy.

### Key insight

AgeMem exposes store, retrieve, update, summarize, and discard as tool-like memory actions and trains memory behavior with progressive reinforcement learning. It reports improved long-horizon task performance, higher-quality long-term memory, and more efficient context use across five benchmarks.

### Design implications

- Treat memory operations as first-class actions available to the agent.
- Learn or tune memory policies instead of relying only on hand-written heuristics.
- Evaluate the quality of memory actions step by step, not only final answers.
- Keep heuristic gates initially, but design them so they can later be learned.

## LongMemEval

**Core contribution:** evaluates long-term chat memory across information extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention.

### Key insight

The benchmark shows that both commercial chat assistants and long-context LLMs can suffer a 30% accuracy drop on sustained-interaction memory tasks. It also identifies practical design optimizations: session decomposition, fact-augmented key expansion, and time-aware query expansion.

### Design implications

- Test memory on updates, abstention, and temporal reasoning, not only recall.
- Decompose sessions into meaningful memory units.
- Expand memory keys with extracted facts.
- Make retrieval time-aware.

## LongMemEval-V2

**Core contribution:** extends long-term memory evaluation to specialized web-agent environments.

### Key insight

LME-V2 asks whether an agent can remember interface affordances, dynamic state, workflows, environment gotchas, and premise awareness from up to 500 trajectories and 115M tokens of history. The strongest reported method, AgentRunbook-C, reaches 72.5% average accuracy versus 48.5% for the strongest RAG baseline, but with higher latency.

### Design implications

- Store procedural runbooks and environment-specific gotchas.
- Preserve tool traces and workflow outcomes as evidence.
- Evaluate memory retrieval as compact evidence gathering for downstream answering.
- Track the accuracy-latency tradeoff explicitly.

## MemoryAgentBench

**Core contribution:** evaluates memory agents through incremental multi-turn interaction.

### Key insight

The benchmark identifies four core competencies: accurate retrieval, test-time learning, long-range understanding, and selective forgetting. Its results indicate that current methods do not master all four.

### Design implications

- Add selective forgetting to evaluation, not just storage and retrieval.
- Include incremental information accumulation in benchmarks.
- Test whether memory updates improve future behavior.
- Avoid optimizing only for static long-context QA.

## MemBench

**Core contribution:** evaluates factual and reflective memory across participation and observation scenarios.

### Key insight

MemBench argues that memory evaluation needs multiple levels and scenarios, with metrics for effectiveness, efficiency, and capacity.

### Design implications

- Evaluate factual memory and reflective memory separately.
- Test both memories created from direct participation and memories created by observing events.
- Track memory capacity and efficiency alongside quality.

## Memory in the Age of AI Agents

**Core contribution:** provides a current survey that distinguishes agent memory from LLM memory, RAG, and context engineering.

### Key insight

The survey argues that long-term versus short-term memory is too coarse for current systems. It frames memory through forms, functions, and dynamics, including token-level, parametric, latent, factual, experiential, and working memory.

### Design implications

- Keep the repository's taxonomy multidimensional.
- Avoid collapsing agent memory into RAG.
- Represent memory dynamics: formation, evolution, retrieval, and trust.
- Track open-source frameworks and benchmarks as part of the research map.

## Memory for Autonomous LLM Agents

**Core contribution:** surveys autonomous-agent memory from 2022 through early 2026.

### Key insight

The survey formalizes agent memory as a write-manage-read loop coupled to perception and action, and highlights open challenges in continual consolidation, causally grounded retrieval, trustworthy reflection, learned forgetting, and multimodal embodied memory.

### Design implications

- Center the architecture around the write-manage-read loop.
- Treat perception, action, and memory as linked processes.
- Make consolidation, causality, reflection trust, forgetting, and multimodality explicit research requirements.

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
