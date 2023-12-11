from __future__ import annotations

import pkgutil

if pkgutil.find_loader("rich"):
    from . import cli_spinners
    from .cli_spinners import SimpleSpinner
