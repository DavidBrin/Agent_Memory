# Memory OS v0 Experiment Design

## Decision

Adopt and audit the existing unpublished `codex/publish-memory-os` prototype as
`experiments/memory_os_v0`. The experiment implements the first four stages of
the repository's proposed Trustworthy Memory OS: immutable evidence, gated
writes, a temporal graph, and trust-aware retrieval.

This is a focused prototype of temporal, provenance-aware claim memory. It is
not a production memory service or a generic vector database.

## Research Basis

The repository recommends a temporal knowledge graph surrounded by lifecycle
governance (`Research/proposed_solutions.md`). It specifically sequences:

1. event log and schema,
2. gated episodic and semantic writes,
3. temporal graph indexing, and
4. trust-weighted retrieval.

This experiment follows that sequence. It addresses the documented risks of
stale memories, contradictory updates, retrieval myopia, poisoning, and
non-propagating deletion. It also deliberately defers offline consolidation,
embeddings, learned policies, and multimodal stores.

## Scope

The adopted prototype will provide:

- an append-only, hash-chained event log for raw evidence;
- an auditable write gate that rejects, quarantines, or stores candidate
  memories;
- typed temporal memory records with source provenance, validity windows,
  trust, sensitivity, and utility metadata;
- entity and relationship links, including `supersedes`, `contradicts`, and
  `derived_from`;
- retrieval that filters by trust, clearance, validity, and deletion state,
  then returns a compact cited context packet;
- correction, feedback, forgetting, and deletion propagation; and
- a deterministic demo plus unit tests.

The prototype will use Python's standard library only. Its deterministic text
matching is intentionally a candidate-finding mechanism for a small local
experiment, not a claim to implement semantic vector retrieval.

## Integration Shape

```text
experiments/
  README.md
  memory_os_v0/
    memory_os/
      event_log.py
      write_gate.py
      schema.py
      store.py
      graph.py
      retrieval.py
      system.py
      demo.py
    tests/
      test_memory_os.py
```

The public system API records evidence, proposes memory writes, retrieves a
time- and trust-filtered context packet, records usefulness feedback, deletes
memory, and exposes provenance. The demo shows a corrected preference, a
historical query, rejected malicious instruction-like content, and abstention
after deletion.

## Data Flow and Safety Rules

```text
observation -> event log -> write gate -> stored or quarantined claim
     -> temporal/entity graph -> filtered and ranked retrieval -> citations
```

Raw events are evidence, not instructions or established beliefs. Untrusted
instruction-like content is quarantined and excluded from ordinary retrieval.
A correction supersedes an older memory by closing its validity window instead
of silently retaining two equally-current facts. Forgetting marks a memory
deleted and cascades to dependent derived memories.

## Acceptance Tests

Before adopting the implementation, add an acceptance test that cannot import
the experiment from the current branch; this establishes the required red
state. After the selected upstream commits are applied, the complete suite must
verify these behaviors:

- current and historical recall respect supersession and validity windows;
- each recallable claim retains event provenance and explainable links;
- only eligible trust and sensitivity levels reach a context packet;
- instruction-like untrusted content is quarantined and never returned by
  default;
- forgetting cascades to dependent memories and returns abstention rather than
  reviving an expired predecessor; and
- event-log tampering is detectable.

Verification will run the full experiment test suite and demo, then update the
repository knowledge graph.

## Adoption and Audit Plan

The source is `codex/publish-memory-os`, commits `9711d89` and `98422f1`.
Their code and documentation will be applied selectively after the acceptance
test is red. Each adopted file will be reviewed locally, the test suite will
be run, and an independent reviewer will assess the final diff. Any issue
found in the review will be fixed in this branch rather than silently accepted
from the source branch.
