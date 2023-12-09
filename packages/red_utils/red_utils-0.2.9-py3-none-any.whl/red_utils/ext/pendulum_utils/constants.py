from __future__ import annotations

default_format: str = "YYYY-MM-DD HH:MM:SS"
twelve_hour_format: str = "YYYY-MM-DD hh:mm:ssA"
default_tz: str = "America/New_York"

## Mapping for string character replacement
safe_str_replace_map = [
    {"search": ":", "replace": "-"},
    {"search": " ", "replace": "_"},
]
