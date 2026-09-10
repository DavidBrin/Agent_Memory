# Memory OS v0 — second repair report

## Scope

This repair addresses the two residual final-review findings approved for the
second repair cycle:

1. A persisted event-log integrity failure could let `MemorySystem.forget()`
   mutate the in-memory store and graph before deletion logging failed.
2. A correction that shared an incidental entity with a resource could be
   routed as a resource correction and supersede the wrong record type.

No plan, specification, ledger, database, transaction infrastructure, or
concurrency behavior was changed.

## Root cause and repair

### A. Persistent deletion integrity

`MemorySystem.forget()` called `store.delete()` and dropped graph nodes before
calling `EventLog.append()`. For a reloaded truncated log, `append()` correctly
raises `ValueError`, but the live system had already removed the records.

`forget()` now verifies the persistent event log before its first store or graph
mutation. In the supported single-process sequential boundary, the subsequent
append preserves the existing logging path while the precondition prevents the
identified divergence.

### B. Type-safe correction routing

The correction branch treated *any* resource record sharing any extracted
entity as evidence that the correction was resource-specific. Generic hints are
also graph relations, so a preference sharing one with a resource was routed as
`resource`.

Resource correction routing now requires both a resource marker in the
correction content and an explicitly supplied stable entity hint matching an
existing resource. Other corrections remain preference corrections.

## TDD evidence

Each test was added before its production change. The production mutation each
test catches is stated here independently of its implementation.

### A. Integrity preflight

Test added:
`DeletionTests.test_forget_keeps_persistent_state_when_corrupt_log_rejects_deletion`

It persists a system, truncates `events.jsonl`, reloads, calls `forget()`, and
asserts the `ValueError` plus target visibility in the live store and graph and
after a fresh restart. It fails if deletion mutates state before an invalid log
is rejected.

RED command:

```text
.venv/bin/python -m unittest -v experiments/memory_os_v0/tests/test_memory_os.py -k corrupt_log_rejects_deletion
```

RED result: failed as expected with
`AssertionError: 'mem_dcb04de25e45' not found in set()` at the assertion that
the target remains visible in the reloaded store.

Minimal production change: add the persistent-log `verify()` precondition in
`MemorySystem.forget()` before `store.delete()`.

GREEN command: same focused command.

GREEN result: `Ran 1 test ... OK`.

### B. Correction routing

Test added:
`TemporalTests.test_preference_correction_does_not_supersede_resource_with_shared_hint`

It creates current resource and preference records sharing `project_reference`,
then corrects the preference. It asserts that the resource remains current and
the correction supersedes only the prior preference. It fails if a shared
entity alone classifies a correction as resource-specific.

RED command:

```text
.venv/bin/python -m unittest -v experiments/memory_os_v0/tests/test_memory_os.py -k preference_correction_does_not_supersede_resource_with_shared_hint
```

RED result: failed as expected with
`AssertionError: 'resource' != 'preference'`.

Minimal production change: require both a resource marker and an event entity
hint that matches an existing resource before returning `resource` from the
correction route.

GREEN commands:

```text
.venv/bin/python -m unittest -v experiments/memory_os_v0/tests/test_memory_os.py -k preference_correction_does_not_supersede_resource_with_shared_hint
.venv/bin/python -m unittest -v experiments/memory_os_v0/tests/test_memory_os.py -k resource_correction_supersedes_the_prior_resource_claim
```

GREEN results: both commands reported `Ran 1 test ... OK`. The second preserves
the existing explicit resource-marker + stable-hint regression.

## Validation

Commands run successfully:

```text
.venv/bin/python -m unittest discover -s experiments/memory_os_v0/tests -v
# Ran 32 tests ... OK

# From experiments/memory_os_v0:
../../.venv/bin/python -m unittest -v tests/test_adoption_acceptance.py
# Ran 1 test ... OK

../../.venv/bin/python -m memory_os.demo
# Completed all eight demo phases; Phase 8 reported an intact 10-entry log,
# 6 memory records, and expected graph-edge summary.

scripts/graphify update .
# Rebuilt 560 nodes, 970 edges, and 46 communities.

git diff --check
# Exit 0; no whitespace errors.
```

The first standalone acceptance invocation from the repository root failed
only because the test imports `memory_os` relative to the prototype directory;
the discovery suite had already run it successfully. It was rerun from
`experiments/memory_os_v0` with the successful command above.

## Files changed

- `experiments/memory_os_v0/memory_os/system.py` — integrity preflight before
  deletion mutation.
- `experiments/memory_os_v0/memory_os/write_gate.py` — require a resource
  marker and matching stable entity hint for resource correction routing.
- `experiments/memory_os_v0/tests/test_memory_os.py` — two focused regression
  tests.
- `.superpowers/sdd/2026-09-10-memory-os-v0-adoption/second-repair-report.md`
  — this report.

## Self-review

Reviewed the scoped diff against both approved findings. The deletion repair
changes no ordinary deletion behavior and does not add transactions or claim
cross-process atomicity. The routing repair checks only correction events and
keeps the existing explicit resource-correction path covered. Tests exercise
real persistence, log verification, store visibility, graph indexing, and
restart behavior; no mocks were introduced.

Residual concern: the specified guarantee is deliberately limited to the
single-process sequential boundary. An external writer that changes the log
after the preflight and before append remains outside the approved scope.
