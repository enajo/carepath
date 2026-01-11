from __future__ import annotations

import os


def getenv(name: str, default: str) -> str:
    val = os.getenv(name)
    return default if val is None or val.strip() == "" else val.strip()


ENV: str = getenv("ENV", "dev")
APP_VERSION: str = getenv("APP_VERSION", "local")

HISTORY_PATH: str = getenv("HISTORY_PATH", "history.jsonl")

MAX_HISTORY_RAW = getenv("MAX_HISTORY", "30")
try:
    MAX_HISTORY: int = max(1, int(MAX_HISTORY_RAW))
except ValueError:
    MAX_HISTORY = 30
