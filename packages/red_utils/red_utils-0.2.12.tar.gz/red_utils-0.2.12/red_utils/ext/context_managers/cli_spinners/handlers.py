from __future__ import annotations

from contextlib import contextmanager
import time

import rich

from rich.console import Console

@contextmanager
def SimpleSpinner(message: str = "Loading..."):
    rich_console: Console = Console()

    try:
        with rich_console.status(message) as status:
            yield status
    except Exception as exc:
        raise Exception(f"Unhandled exception yielding spinner. Details: {exc}")
    finally:
        # rich_console.clear()
        rich_console.clear_live()
