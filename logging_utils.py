"""
Helpers para logging estruturado em JSON.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict


class StructuredLogFormatter(logging.Formatter):
    """Renderiza logs como JSON lines estáveis."""

    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(timespec="seconds"),
            "level": record.levelname,
            "logger": record.name,
        }

        event_name = getattr(record, "event_name", "")
        event_fields = getattr(record, "event_fields", {})

        if event_name:
            payload["event"] = event_name
            if isinstance(event_fields, dict):
                payload.update(event_fields)
        else:
            payload["message"] = record.getMessage()

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False, default=str, sort_keys=True)


def configure_structured_logging(level: int = logging.INFO) -> None:
    """Configura o root logger para emitir JSON lines."""
    root_logger = logging.getLogger()
    handler = logging.StreamHandler(stream=sys.stderr)
    handler.setFormatter(StructuredLogFormatter())
    root_logger.handlers = [handler]
    root_logger.setLevel(level)


def log_event(logger: logging.Logger, level: int, event: str, **fields: Any) -> None:
    """Emite um evento estruturado."""
    logger.log(
        level,
        event,
        extra={
            "event_name": event,
            "event_fields": fields,
        },
    )
