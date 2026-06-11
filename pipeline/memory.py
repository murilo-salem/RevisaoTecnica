"""
Memória operacional, sidecar e journal do pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

import config


@dataclass
class MemoryJournalEntry:
    """Entrada append-only do journal de execução."""

    timestamp: str
    stage: str
    event: str
    detail: str
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "stage": self.stage,
            "event": self.event,
            "detail": self.detail,
            "payload": self.payload,
        }


@dataclass
class MemorySidecar:
    """Memória operacional separada do estado principal."""

    run_id: str
    max_items_per_slot: int = config.MEMORY_SLOT_MAX_ITEMS
    slots: Dict[str, List[Any]] = field(default_factory=dict)
    journal: List[MemoryJournalEntry] = field(default_factory=list)

    def append(self, stage: str, event: str, detail: str, payload: Dict[str, Any] | None = None) -> None:
        self.journal.append(
            MemoryJournalEntry(
                timestamp=datetime.now().isoformat(timespec="seconds"),
                stage=stage,
                event=event,
                detail=detail,
                payload=payload or {},
            )
        )

    def set_slot(self, slot: str, value: Any, overwrite: bool = False) -> None:
        bucket = self.slots.setdefault(slot, [])
        if overwrite:
            bucket[:] = [value]
            return

        bucket.append(value)
        if len(bucket) > self.max_items_per_slot:
            del bucket[:-self.max_items_per_slot]

    def get_slot(self, slot: str) -> List[Any]:
        return list(self.slots.get(slot, []))

    def to_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "max_items_per_slot": self.max_items_per_slot,
            "slots": self.slots,
            "journal": [entry.to_dict() for entry in self.journal],
        }

    def build_writer_context(self, state_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Compacta a memória operacional para consumo do writer."""
        return {
            "run_id": self.run_id,
            "protocol": state_summary.get("protocol", {}),
            "coverage": state_summary.get("coverage_metrics", {}),
            "top_patents": state_summary.get("top_patents", []),
            "clusters": state_summary.get("thematic_clusters", {}),
            "routes": state_summary.get("route_summary", {}),
            "slot_policy": {
                "max_items_per_slot": self.max_items_per_slot,
                "slots": sorted(self.slots.keys()),
            },
            "journal_highlights": [
                {
                    "stage": entry.stage,
                    "event": entry.event,
                    "detail": entry.detail,
                }
                for entry in self.journal[-10:]
            ],
        }
