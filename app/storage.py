from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .config import HISTORY_PATH, MAX_HISTORY


def _ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def append_event(event: Dict[str, Any]) -> None:
    """
    Append a triage result to a JSONL file.
    This is intentionally simple and works well in Docker with a mounted volume.
    """
    path = Path(HISTORY_PATH)
    _ensure_parent(path)

    # Add timestamp if missing
    if "timestamp" not in event:
        event["timestamp"] = datetime.now(timezone.utc).isoformat()

    line = json.dumps(event, ensure_ascii=False)
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def read_recent(limit: int = MAX_HISTORY) -> List[Dict[str, Any]]:
    path = Path(HISTORY_PATH)
    if not path.exists():
        return []

    # Read last N lines safely
    lines = path.read_text(encoding="utf-8").splitlines()
    tail = lines[-limit:] if limit > 0 else lines
    out: List[Dict[str, Any]] = []
    for line in reversed(tail):
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out
