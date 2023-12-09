from __future__ import annotations

import pkgutil

## Use pkgutil to only load modules
#  if dependencies are met
if pkgutil.find_loader("arrow"):
    from . import arrow_utils

if pkgutil.find_loader("pendulum"):
    from . import pendulum_utils

if pkgutil.find_loader("loguru"):
    from . import loguru_utils

if pkgutil.find_loader("pydantic"):
    from . import pydantic_utils

if pkgutil.find_loader("msgpack"):
    from . import msgpack_utils

if pkgutil.find_loader("diskcache"):
    from . import diskcache_utils

if pkgutil.find_loader("httpx"):
    from . import httpx_utils

if pkgutil.find_loader("fastapi"):
    from . import fastapi_utils

if pkgutil.find_loader("sqlalchemy"):
    from . import sqlalchemy_utils

if pkgutil.find_loader("rich"):
    from . import context_managers
