# Vector Memory vs Graph Memory

Most early agent memory systems use vector search. Vector stores are useful, but they are not sufficient for all memory problems. This note compares vector memory with graph and structured memory.

## Vector Memory

Vector memory stores embedded chunks and retrieves them by semantic similarity.

### Strengths

- Simple to implement
- Scales well with existing vector databases
- Good for fuzzy semantic recall
- Works with unstructured documents and chat logs
- Does not require a heavy schema upfront

### Weaknesses

- Semantic similarity is not the same as task relevance
- Time, source, confidence, and causal relations are often implicit
- Contradictions are hard to detect
- Multiple related memories are not naturally connected
- Retrieval can over-focus on text similarity and miss dependency structure

### Best use cases

- Searching prior conversations
- Retrieving document chunks
- Finding semantically related examples
- Bootstrapping an early prototype

## Graph Memory

Graph memory represents memories as nodes and relationships as edges.

Example nodes:

- User
- Project
- Event
- Claim
- Preference
- Tool call
- File
- Procedure
- Failure
- Decision

Example edges:

- `supports`
- `contradicts`
- `updates`
- `caused_by`
- `depends_on`
- `belongs_to_project`
- `observed_at`
- `derived_from`
- `valid_until`
- `used_successfully_in`

### Strengths

- Better temporal and causal reasoning
- Easier contradiction tracking
- More explicit provenance
- Better multi-hop retrieval
- More natural support for entity-centered memory

### Weaknesses

- Requires schema design
- More complex to maintain
- Can become stale if edges are not updated
- Harder to benchmark
- May be overkill for simple agents

### Best use cases

- Long-running project agents
- Personal assistants with evolving preferences
- Multi-agent systems
- Tool-using agents with action traces
- Safety-critical or compliance-sensitive systems

## Hybrid Retrieval

The best architecture is usually hybrid:

```text
User query / task
        ↓
Vector candidate retrieval
        ↓
Graph expansion around candidates
        ↓
Trust, recency, contradiction, and task filters
        ↓
Context compiler
        ↓
Agent response / action
```

## Proposed Memory Object

A memory object should include both vector and graph fields:

```yaml
memory_id: string
text: string
embedding: vector
type: event | claim | preference | procedure | reflection | tool_trace
created_at: timestamp
updated_at: timestamp
source: user | agent | tool | document | system
confidence: float
trust_score: float
valid_from: timestamp
valid_until: timestamp | null
entity_links: list
supports: list[memory_id]
contradicts: list[memory_id]
derived_from: list[memory_id]
usage_stats:
  retrieved_count: int
  helpful_count: int
  harmful_count: int
```

## Fine-Grained Design Principle

Use vectors to find candidates. Use structure to decide whether candidates should be trusted, expanded, included, contradicted, or ignored.

## Research Questions

- Which memory types benefit most from graph structure?
- What is the minimal useful schema for personal agents?
- How can graph edges be generated without accumulating hallucinated relations?
- How should vector similarity and graph distance be combined?
- Can retrieval learn from post-hoc usefulness feedback?
