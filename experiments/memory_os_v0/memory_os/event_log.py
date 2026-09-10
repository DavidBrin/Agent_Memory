"""Append-only event log: the immutable evidence layer.

Section 1 of `Research/proposed_solutions.md` is explicit that "events are not
automatically beliefs, they are evidence candidates." Nothing in this module
interprets content. It only guarantees that what was observed stays observable.

Each entry carries the hash of its predecessor, and a sidecar anchor records
the expected length and head hash. Editing, reordering, or truncating history
after the anchor is created breaks `verify()`. That property is what makes
provenance claims elsewhere in the system worth anything.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .schema import MemoryEvent

GENESIS = "0" * 64


def _entry_hash(prev_hash: str, payload: dict) -> str:
    body = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(f"{prev_hash}{body}".encode()).hexdigest()


class EventLog:
    def __init__(self, path: Path | str | None = None) -> None:
        self.path = Path(path) if path else None
        self.anchor_path = self.path.with_name(f"{self.path.name}.anchor.json") if self.path else None
        self._entries: list[dict] = []
        if self.path and self.path.exists():
            self._load()
        if self.anchor_path and not self.anchor_path.exists() and not self._entries:
            self._write_anchor()

    # -- writing ------------------------------------------------------------

    def append(self, event: MemoryEvent) -> dict:
        # An existing persisted log whose chain or anchor no longer verifies
        # is evidence of tampering or loss. Do not add a new event and rewrite
        # the anchor, which would make a truncated history appear healthy.
        if self.path is not None:
            valid, error = self.verify()
            if not valid:
                raise ValueError(f"event log integrity check failed; refusing append: {error}")
        payload = event.to_dict()
        prev_hash = self._entries[-1]["hash"] if self._entries else GENESIS
        entry = {
            "seq": len(self._entries),
            "prev_hash": prev_hash,
            "hash": _entry_hash(prev_hash, payload),
            "event": payload,
        }
        self._entries.append(entry)
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(entry, sort_keys=True) + "\n")
            if self.anchor_path and self.anchor_path.exists():
                self._write_anchor()
        return entry

    # -- reading ------------------------------------------------------------

    def _load(self) -> None:
        with self.path.open(encoding="utf-8") as handle:
            self._entries = [json.loads(line) for line in handle if line.strip()]

    def _write_anchor(self) -> None:
        if self.anchor_path is None:
            return
        self.anchor_path.parent.mkdir(parents=True, exist_ok=True)
        head_hash = self._entries[-1]["hash"] if self._entries else GENESIS
        self.anchor_path.write_text(
            json.dumps({"count": len(self._entries), "head_hash": head_hash}, sort_keys=True),
            encoding="utf-8",
        )

    def _read_anchor(self) -> dict | None:
        if self.anchor_path is None or not self.anchor_path.exists():
            return None
        return json.loads(self.anchor_path.read_text(encoding="utf-8"))

    def events(self) -> list[MemoryEvent]:
        return [MemoryEvent.from_dict(entry["event"]) for entry in self._entries]

    def get(self, event_id: str) -> MemoryEvent | None:
        for entry in self._entries:
            if entry["event"]["event_id"] == event_id:
                return MemoryEvent.from_dict(entry["event"])
        return None

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self):
        return iter(self.events())

    # -- integrity ----------------------------------------------------------

    def verify(self) -> tuple[bool, str | None]:
        prev_hash = GENESIS
        for expected_seq, entry in enumerate(self._entries):
            if entry.get("seq") != expected_seq:
                return False, f"sequence {entry.get('seq')}: expected {expected_seq}"
            if entry["prev_hash"] != prev_hash:
                return False, f"seq {entry['seq']}: broken chain link"
            expected = _entry_hash(prev_hash, entry["event"])
            if entry["hash"] != expected:
                return False, f"seq {entry['seq']}: content does not match hash"
            prev_hash = entry["hash"]
        anchor = self._read_anchor()
        if self.path is not None and self._entries and anchor is None:
            return False, "anchor is missing for an existing log"
        if anchor is not None and (
            anchor.get("count") != len(self._entries) or anchor.get("head_hash") != prev_hash
        ):
            return False, "anchor does not match the current log head"
        return True, None
