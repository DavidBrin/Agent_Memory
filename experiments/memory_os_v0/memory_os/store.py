"""Typed memory stores with temporal validity and deletion propagation.

Two behaviours here are the point of the whole prototype, because they are the
two things `Research/current_approaches.md` identifies as missing from almost
every deployed system:

1. A correction *supersedes* the prior value by closing its validity window,
   rather than being appended alongside it as a competing duplicate.
2. Deleting a memory propagates. The superseded versions of the same claim go
   with it, and so does anything derived from it. Otherwise deletion silently
   resurrects an old value or leaves an orphaned summary behind.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .schema import MemoryRecord


class MemoryStore:
    def __init__(self, path: Path | str | None = None) -> None:
        self.path = Path(path) if path else None
        self.records: dict[str, MemoryRecord] = {}
        if self.path and self.path.exists():
            self.load()

    # -- writing ------------------------------------------------------------

    def write(self, record: MemoryRecord) -> MemoryRecord:
        for old_id in record.supersedes:
            old = self.records.get(old_id)
            if old is None:
                continue
            # Close the old window at the moment the new claim became true.
            # The old record is retained: it is still the correct answer to
            # "what did we believe last month?".
            old.valid_until = record.valid_from
            old.superseded_by = record.memory_id
            if record.memory_id not in old.contradicts:
                old.contradicts.append(record.memory_id)
            if old_id not in record.contradicts:
                record.contradicts.append(old_id)
        self.records[record.memory_id] = record
        return record

    # -- reading ------------------------------------------------------------

    def get(self, memory_id: str) -> MemoryRecord | None:
        return self.records.get(memory_id)

    def all(self) -> list[MemoryRecord]:
        return list(self.records.values())

    def by_claim_key(self, claim_key: str, as_of: datetime | None = None) -> list[MemoryRecord]:
        """Currently valid records asserting the same claim."""
        return [
            r
            for r in self.records.values()
            if r.claim_key == claim_key
            and r.superseded_by is None
            and (as_of is None or r.is_valid_at(as_of))
        ]

    def by_entity(self, entity: str) -> list[MemoryRecord]:
        return [r for r in self.records.values() if entity in r.entities]

    def visible(
        self,
        as_of: datetime,
        session_id: str | None = None,
        include_quarantined: bool = False,
    ) -> list[MemoryRecord]:
        """Records eligible for retrieval at a point in time.

        Session records are invisible outside their own session, which is the
        mechanism that stops a one-off instruction becoming a standing
        preference.
        """
        out = []
        for record in self.records.values():
            if not record.is_valid_at(as_of):
                continue
            if record.scope == "session" and record.session_id != session_id:
                continue
            if record.trust_level == "quarantined" and not include_quarantined:
                continue
            out.append(record)
        return out

    def counts_by_type(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for record in self.records.values():
            counts[record.type] = counts.get(record.type, 0) + 1
        return counts

    # -- deletion -----------------------------------------------------------

    def delete(self, memory_id: str, cascade: bool = True) -> list[str]:
        """Remove a memory and everything that would resurrect or outlive it.

        Returns every id removed, so the caller can log the deletion as an
        event and drop the same ids from the graph index.
        """
        if memory_id not in self.records:
            return []
        doomed: list[str] = []
        frontier = [memory_id]
        seen = set()
        while frontier:
            current = frontier.pop()
            if current in seen or current not in self.records:
                continue
            seen.add(current)
            doomed.append(current)
            if not cascade:
                break
            record = self.records[current]
            # Earlier versions of the same claim.
            frontier.extend(record.supersedes)
            # Later versions, and anything distilled from this record. The
            # relation is stored on the newer record, so follow both the
            # back-link and the newer record's explicit supersedes edge.
            for other in self.records.values():
                if (
                    other.superseded_by == current
                    or current in other.supersedes
                    or current in other.derived_from
                ):
                    frontier.append(other.memory_id)
        for dead in doomed:
            self.records.pop(dead, None)
        # Clean dangling references so the store stays internally consistent.
        for record in self.records.values():
            record.supersedes = [i for i in record.supersedes if i not in doomed]
            record.contradicts = [i for i in record.contradicts if i not in doomed]
            record.derived_from = [i for i in record.derived_from if i not in doomed]
            if record.superseded_by in doomed:
                record.superseded_by = None
        return doomed

    # -- persistence --------------------------------------------------------

    def save(self, path: Path | str | None = None) -> None:
        target = Path(path) if path else self.path
        if target is None:
            raise ValueError("no path configured for this store")
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = [r.to_dict() for r in self.records.values()]
        target.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def load(self, path: Path | str | None = None) -> None:
        target = Path(path) if path else self.path
        data = json.loads(Path(target).read_text(encoding="utf-8"))
        self.records = {d["memory_id"]: MemoryRecord.from_dict(d) for d in data}
