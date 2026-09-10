# Memory OS v0 Adoption Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate an audited, runnable prototype of the repository's temporal, trust-aware Memory OS under `experiments/memory_os_v0`.

**Architecture:** Adopt the existing `codex/publish-memory-os` experiment only after a new public-API acceptance test proves the package is absent. The prototype keeps raw events in a hash-chained log, gates writes, records temporal graph links, and retrieves only valid, permitted, non-quarantined evidence with citations.

**Tech Stack:** Python 3 standard library; `unittest`; repository-local Graphify wrapper.

**Spec:** `docs/superpowers/specs/2026-09-10-memory-os-v0-design.md`

## Global Constraints

- Keep the runtime dependency-free: Python standard library only.
- Keep the experiment at `experiments/memory_os_v0`; do not make it an application dependency.
- Treat raw events as evidence rather than instructions or established claims.
- Quarantine untrusted instruction-like content and exclude it from ordinary retrieval.
- Preserve provenance, validity windows, supersession, and deletion propagation.
- Do not add embeddings, an LLM, a vector/graph database, a web UI, learned policies, or background workers.
- Update the repository knowledge graph after documentation or code changes with `scripts/graphify update .`.

---

## File Structure

| File | Responsibility |
| --- | --- |
| `experiments/README.md` | Index and run instructions for experiments. |
| `experiments/memory_os_v0/memory_os/schema.py` | Typed event and record objects plus metadata vocabularies. |
| `experiments/memory_os_v0/memory_os/event_log.py` | Append-only, hash-chained evidence persistence. |
| `experiments/memory_os_v0/memory_os/write_gate.py` | Explainable admission, routing, quarantine, and supersession policy. |
| `experiments/memory_os_v0/memory_os/store.py` | Record persistence, visibility, deletion, and dependency traversal. |
| `experiments/memory_os_v0/memory_os/graph.py` | Entity and relation indexes used for structural expansion. |
| `experiments/memory_os_v0/memory_os/retrieval.py` | Candidate ranking, graph expansion, policy filters, citations, and feedback. |
| `experiments/memory_os_v0/memory_os/system.py` | Public `MemorySystem` write-manage-read orchestration API. |
| `experiments/memory_os_v0/memory_os/demo.py` | Reproducible end-to-end behavior demonstration. |
| `experiments/memory_os_v0/tests/test_adoption_acceptance.py` | New public-API acceptance test proving adoption is required. |
| `experiments/memory_os_v0/tests/test_memory_os.py` | Full regression suite supplied by the adopted experiment. |
| `README.md`, `Research/README.md` | Navigation links between research and runnable experiment. |

### Task 1: Establish the red acceptance test and adopt the prototype

**Files:**
- Create: `experiments/memory_os_v0/tests/test_adoption_acceptance.py`
- Create: `experiments/README.md`
- Create: `experiments/memory_os_v0/memory_os/{__init__,schema,event_log,write_gate,store,graph,retrieval,system,textutil,demo}.py`
- Create: `experiments/memory_os_v0/tests/test_memory_os.py`
- Modify: `README.md`
- Modify: `Research/README.md`

**Interfaces:**
- Consumes: no implementation code; `codex/publish-memory-os` is read-only source input.
- Produces: `MemorySystem` and `make_event` from `memory_os`, plus `UTC` from `memory_os.schema`; `observe(event) -> tuple[GateDecision, MemoryRecord | None]`, `ask(query, as_of, **kwargs) -> ContextPacket`, and `forget(memory_id, at, reason) -> list[str]`.

- [ ] **Step 1: Write the failing public-API acceptance test**

```python
from datetime import datetime
import unittest


class AdoptionAcceptanceTests(unittest.TestCase):
    def test_current_and_historical_queries_follow_a_correction(self):
        from memory_os import MemorySystem, make_event
        from memory_os.schema import UTC

        system = MemorySystem()
        jan = datetime(2026, 1, 1, tzinfo=UTC)
        mar = datetime(2026, 3, 1, tzinfo=UTC)
        system.observe(make_event(
            jan, "s1", "user", "message", "I prefer concise summaries.",
            entity_hints=("summary_style",),
        ))
        system.observe(make_event(
            mar, "s2", "user", "correction", "I prefer detailed summaries.",
            entity_hints=("summary_style",),
        ))

        self.assertIn("concise summaries", system.ask("what summary format?", jan).render())
        self.assertIn("detailed summaries", system.ask("what summary format?", mar).render())
```

- [ ] **Step 2: Run the acceptance test to verify red**

Run: `PYTHONPATH=experiments/memory_os_v0 python3 -m unittest experiments/memory_os_v0/tests/test_adoption_acceptance.py -v`

Expected: `ModuleNotFoundError: No module named 'memory_os'`, proving the test requires the missing experiment.

- [ ] **Step 3: Apply reviewed upstream code**

Run:

```bash
git cherry-pick 9711d89
git cherry-pick 98422f1
```

If documentation conflicts, preserve the current design and plan docs, stage the experiment and navigation files listed above, and complete the cherry-pick. Do not take unrelated research-history changes.

- [ ] **Step 4: Run the acceptance test to verify green**

Run: `PYTHONPATH=experiments/memory_os_v0 python3 -m unittest experiments/memory_os_v0/tests/test_adoption_acceptance.py -v`

Expected: PASS; January context contains the superseded preference and March context contains the correcting preference.

- [ ] **Step 5: Commit the acceptance test**

```bash
git add experiments/memory_os_v0/tests/test_adoption_acceptance.py
git commit -m "test: cover temporal memory adoption"
```

### Task 2: Audit governed-memory behavior with the complete suite

**Files:**
- Test: `experiments/memory_os_v0/tests/test_memory_os.py`
- Test: `experiments/memory_os_v0/tests/test_adoption_acceptance.py`
- Modify only if an audit fails: the smallest owning module among `event_log.py`, `write_gate.py`, `store.py`, `graph.py`, `retrieval.py`, or `system.py`.

**Interfaces:**
- Consumes: `MemorySystem`, `EventLog`, `MemoryStore`, `TemporalGraph`, `WriteGate`, and `Retriever` from Task 1.
- Produces: verified supersession, provenance, quarantine, clearance, abstention, feedback, cascading deletion, persistence, and hash-chain integrity.

- [ ] **Step 1: Run the full supplied regression suite**

Run from `experiments/memory_os_v0`: `PYTHONPATH=. python3 -m unittest discover -s tests -v`

Expected: all tests pass, including correction, quarantine, retrieval filters, deletion propagation, persistence, and event-log integrity.

- [ ] **Step 2: When a behavior fails, name the break and add one narrow regression test**

If forgetting a correction revives its predecessor, add this before production code changes:

```python
def test_forgetting_a_correction_does_not_revive_its_predecessor(self):
    system = MemorySystem()
    _, old = system.observe(make_event(at(0), "s1", "user", "message",
        "I prefer concise summaries.", entity_hints=("summary_style",)))
    _, new = system.observe(make_event(at(20), "s2", "user", "correction",
        "I prefer detailed summaries.", entity_hints=("summary_style",)))
    system.forget(new.memory_id, at(30))
    self.assertTrue(system.ask("what summary format?", at(30)).abstain)
    self.assertIsNone(system.store.get(old.memory_id))
```

- [ ] **Step 3: Run the narrow test and confirm red**

Run: `PYTHONPATH=. python3 -m unittest tests.test_memory_os.DeletionTests.test_forgetting_a_correction_does_not_revive_its_predecessor -v`

Expected: FAIL only if the named non-revival contract is broken. If the original suite is green, do not make speculative production edits.

- [ ] **Step 4: Repair the smallest owning component, only for a red test**

Keep deletion traversal in `MemoryStore.delete`, graph cleanup in `MemorySystem.forget`, and visibility filtering in `MemoryStore.visible`. Preserve Task 1 public method signatures and return types.

- [ ] **Step 5: Run narrow and complete tests after every repair**

Run:

```bash
PYTHONPATH=. python3 -m unittest tests.test_memory_os.DeletionTests.test_forgetting_a_correction_does_not_revive_its_predecessor -v
PYTHONPATH=. python3 -m unittest discover -s tests -v
```

Expected: the newly added regression and full suite pass. If no repair was needed, run only the full suite.

- [ ] **Step 6: Commit any real audit repair**

```bash
git add experiments/memory_os_v0
git commit -m "fix: preserve governed memory deletion semantics"
```

### Task 3: Verify the runnable experiment and integration

**Files:**
- Modify only if verification proves inaccuracy: `experiments/README.md`, `README.md`, `Research/README.md`, `experiments/memory_os_v0/memory_os/demo.py`.
- Test: both test files under `experiments/memory_os_v0/tests/`.

**Interfaces:**
- Consumes: the adopted public package and test suite.
- Produces: reproducible terminal behavior and correct navigation from repository docs.

- [ ] **Step 1: Run the in-memory demo**

Run from `experiments/memory_os_v0`: `PYTHONPATH=. python3 -m memory_os.demo`

Expected: accepted and session-only preferences, quarantined web instruction content, temporal answers, clearance-filtered confidential content, graph-expanded resource evidence, deletion without predecessor revival, and an intact hash chain.

- [ ] **Step 2: Run the persistent demo and verify its artifacts**

Run:

```bash
run_dir=$(mktemp -d)
PYTHONPATH=. python3 -m memory_os.demo --out "$run_dir"
test -s "$run_dir/events.jsonl"
test -s "$run_dir/memories.json"
```

Expected: exit zero and nonempty event-log and memory-store files.

- [ ] **Step 3: Check documentation and update the knowledge graph**

Run:

```bash
rg -n "memory_os_v0" README.md Research/README.md experiments/README.md
scripts/graphify update .
git diff --check
```

Expected: all three indexes name the experiment, Graphify rebuilds, and there are no whitespace errors.

- [ ] **Step 4: Commit only verified documentation corrections**

```bash
git add README.md Research/README.md experiments/README.md experiments/memory_os_v0/memory_os/demo.py
git commit -m "docs: document memory OS experiment"
```

Skip this commit when the adopted documentation is accurate.

### Task 4: Independent review, final verification, and handoff

**Files:**
- Review: the complete `main...HEAD` diff.

**Interfaces:**
- Consumes: green tests, both demo runs, and Graphify output from Tasks 1-3.
- Produces: a reviewable feature branch ready for a pull request to `main`.

- [ ] **Step 1: Inspect the final change set**

Run:

```bash
git diff --check main...HEAD
git diff --stat main...HEAD
git status --short --branch
```

Expected: no whitespace errors and only intended setup/docs, prototype code/tests, and navigation changes.

- [ ] **Step 2: Request independent code review**

Send the reviewer: "Audit `main...HEAD` for the stdlib-only `experiments/memory_os_v0` temporal memory prototype. It must retain raw-event provenance; filter by time, trust, sensitivity, and deletion; quarantine untrusted instructions; preserve no-revival deletion semantics; and expose a deterministic demo. Report evidence-backed critical, important, and minor findings."

- [ ] **Step 3: Fix every verified critical or important finding with red-green tests**

For each verified issue, add a test that fails against it, run the test, repair the owning module minimally, then rerun the new test and complete suite before committing the repair.

- [ ] **Step 4: Run final verification**

Run:

```bash
(cd experiments/memory_os_v0 && PYTHONPATH=. python3 -m unittest discover -s tests -v)
(cd experiments/memory_os_v0 && PYTHONPATH=. python3 -m memory_os.demo >/tmp/memory_os_demo.txt)
scripts/graphify update .
git diff --check main...HEAD
```

Expected: all tests pass, demo exits zero, Graphify rebuilds, and final diff has no whitespace errors.

- [ ] **Step 5: Push and open a pull request**

Run: `git push -u origin codex/memory-os-v0-implementation`

Open a pull request to `main` titled `Add temporal Memory OS v0 experiment`, including the research basis, scope boundaries, test and demo commands, and independent-review outcome.
