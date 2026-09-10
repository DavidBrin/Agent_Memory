"""Wires the four layers together into one object.

    observe -> event log -> write gate -> typed stores -> temporal graph
                                                              |
                                          ask <- context packet <- retriever

This is the write-manage-read loop that the surveys in
`Research/papers/survey_notes.md` describe, with the manage stage reduced to
what a single process can do synchronously. Offline consolidation, which is
where the manage stage properly belongs, is deferred; see the README.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .event_log import EventLog
from .graph import TemporalGraph
from .retrieval import ContextPacket, Retriever
from .schema import MemoryEvent, MemoryRecord, make_event
from .store import MemoryStore
from .write_gate import GateDecision, WriteGate


class MemorySystem:
    def __init__(self, root: Path | str | None = None) -> None:
        root_path = Path(root) if root else None
        self.log = EventLog(root_path / "events.jsonl" if root_path else None)
        self.store = MemoryStore(root_path / "memories.json" if root_path else None)
        self.graph = TemporalGraph()
        self.gate = WriteGate(self.store)
        self.retriever = Retriever(self.store, self.graph)
        if self.store.records:
            self.graph.reindex(self.store.all())

    def observe(self, event: MemoryEvent) -> tuple[GateDecision, MemoryRecord | None]:
        """Record evidence, then decide what if anything it justifies believing."""
        self.log.append(event)
        decision = self.gate.evaluate(event)
        record = self.gate.apply(event, decision)
        if record is not None:
            # Superseding a record changes its validity window, so both ends of
            # the relationship need reindexing.
            self.graph.index(record)
            for old_id in record.supersedes:
                old = self.store.get(old_id)
                if old is not None:
                    self.graph.index(old)
        return decision, record

    def ask(self, query: str, as_of: datetime, **kwargs) -> ContextPacket:
        return self.retriever.retrieve(query, as_of, **kwargs)

    def forget(self, memory_id: str, at: datetime, reason: str = "user request") -> list[str]:
        """User-initiated deletion, propagated and logged."""
        removed = self.store.delete(memory_id, cascade=True)
        for dead in removed:
            self.graph.drop(dead)
        self.log.append(
            make_event(
                ts=at,
                session_id="system",
                actor="user",
                kind="deletion",
                content=f"Deleted {memory_id} and {len(removed) - 1} linked record(s): {reason}",
                deleted_ids=removed,
            )
        )
        return removed

    def save(self) -> None:
        if self.store.path:
            self.store.save()
