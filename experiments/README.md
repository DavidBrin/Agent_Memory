# Experiments

Working prototypes of ideas from [`Research/proposed_solutions.md`](../Research/proposed_solutions.md).

## memory_os_v0

A stdlib-only sketch of the Trustworthy Memory OS. It implements Implementation Sequence steps 1–4:

1. Append-only event log with a hash chain
2. Write gate (reject / quarantine / store, with reasons)
3. Temporal store + entity graph (supersession, deletion cascade)
4. Trust-weighted, time-aware retrieval with citations

**Intentionally deferred:** learned ranking, real embeddings, multi-agent scopes, encryption, and online consolidation.

### Run

```bash
cd experiments/memory_os_v0
PYTHONPATH=. python3 -m memory_os.demo
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

Optional persistence:

```bash
PYTHONPATH=. python3 -m memory_os.demo --out /tmp/memory_os_run
```
