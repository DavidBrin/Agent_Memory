# Foundational Agent Memory Papers

This file summarizes the papers that established the dominant patterns in modern agent memory systems.

## Generative Agents: Interactive Simulacra of Human Behavior

**Core contribution:** introduced a practical architecture for believable long-horizon agents using a memory stream, retrieval, reflection, and planning.

**Link:** https://arxiv.org/abs/2304.03442

### Memory mechanism

The agent stores observations in an append-only memory stream. When deciding what to do, it retrieves memories according to a weighted combination of:

- **Recency**: more recent memories are more likely to be used.
- **Relevance**: semantic similarity to the current situation.
- **Importance**: an LLM-generated estimate of salience.

The system periodically synthesizes higher-level reflections from low-level episodes.

### Key insight

Agent behavior becomes more coherent when memory is not merely a transcript but a structured process that retrieves, reflects, and plans.

### Limitations

- Reflection can amplify incorrect memories.
- Importance scoring is subjective and prompt-sensitive.
- Retrieval is still mostly similarity-based.
- The architecture lacks explicit contradiction handling.

## MemGPT: Towards LLMs as Operating Systems

**Core contribution:** reframed LLM memory as a virtual memory problem.

**Link:** https://arxiv.org/abs/2310.08560

### Memory mechanism

MemGPT separates memory into:

- **Main context**: the current prompt/context window.
- **Core memory**: high-priority persistent information.
- **Archival memory**: large external long-term store.

The agent controls memory movement through tool-like operations, deciding when to write, search, or page information into context.

### Key insight

Memory should be managed like an operating system resource. The context window is scarce, and agents need explicit policies for moving information between hot and cold storage.

### Limitations

- Requires reliable self-management by the LLM.
- Retrieval and memory writes can be brittle.
- Does not fully solve memory verification or poisoning.

## MemoryBank: Enhancing Large Language Models with Long-Term Memory

**Core contribution:** explored persistent user-specific conversational memory and forgetting.

**Link:** https://arxiv.org/abs/2305.10250

### Memory mechanism

MemoryBank stores user interactions and uses forgetting-inspired mechanisms to prioritize memories over time.

### Key insight

For personalized agents, remembering everything is not ideal. Forgetting, decay, and salience are necessary for stable long-term user models.

### Limitations

- User preferences can change over time.
- Memory decay alone does not resolve contradictions.
- Sensitive information needs stronger access control.

## Reflexion: Language Agents with Verbal Reinforcement Learning

**Core contribution:** introduced reflection as a form of learning from failure without updating model weights.

**Link:** https://arxiv.org/abs/2303.11366

### Memory mechanism

After an attempt, the agent writes a verbal reflection describing what went wrong and how to improve. Future attempts retrieve these reflections as guidance.

### Key insight

Memory can function as policy improvement. Instead of storing only facts, agents can store lessons, heuristics, and failure analyses.

### Limitations

- Reflections may be wrong.
- Bad reflections can cause persistent failure loops.
- Reflection quality depends heavily on the evaluator.

## Voyager: An Open-Ended Embodied Agent with Large Language Models

**Core contribution:** demonstrated procedural memory through a growing skill library.

**Link:** https://arxiv.org/abs/2305.16291

### Memory mechanism

Voyager stores executable code skills that can be reused in future tasks. Successful behaviors are consolidated into a reusable procedural library.

### Key insight

Agent memory is not only textual. Durable memory can be procedural: skills, tools, scripts, workflows, and policies.

### Limitations

- Learned skills require validation.
- Skill libraries can become redundant or unsafe.
- Procedural transfer is environment-dependent.

## Synthesis

These papers establish four major memory archetypes:

1. **Episodic memory**: logs of experience.
2. **Reflective memory**: lessons synthesized from experience.
3. **Procedural memory**: reusable skills and actions.
4. **Managed memory hierarchy**: hot context plus cold archival storage.

The common gap across all of them is lifecycle governance: deciding what should be stored, trusted, updated, forgotten, or promoted into durable knowledge.
