from __future__ import annotations

from pathlib import Path

DATA_DIR: Path = Path(".data")
CACHE_DIR: Path = Path(".cache")
SERIALIZE_DIR: Path = Path(".serialize")
JSON_DIR: Path = Path(f"{DATA_DIR}/json")
LOG_DIR: Path = Path("logs")
DB_DIR: Path = Path(".db")

ENSURE_EXIST_DIRS: list[Path] = [DATA_DIR, CACHE_DIR, SERIALIZE_DIR, LOG_DIR]
