from __future__ import annotations

from typing import Union

from .constants import (
    default_format,
    default_tz,
    safe_str_replace_map,
    twelve_hour_format,
)
from .validators import valid_time_periods

import pendulum

def get_ts(
    tz: str = default_tz,
    as_str: bool = False,
    str_fmt: str = default_format,
    safe_str: bool = False,
    char_replace_map: list[dict] = safe_str_replace_map,
) -> pendulum.DateTime:
    """Return a Pendulum.DateTime object of the current time. Optionally
    return timestamp as a string.

    Params:
    -------
    - tz (str): Unix timezone string, defaults to 'America/New_York'.
        - [Unix timezone strings](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)
    - as_str (bool): If True, returns timestamp as a string instead of DateTime.
    - str_fmt (str): String that defines the format of the timestamp if as_str=True.
        - [Pendulum Docs: String Formatting](https://pendulum.eustace.io/docs/#string-formatting)
    - safe_str (bool): If True, replaces characters (like ':' and ' ') with a string that is safe
        to use in a terminal, as a filename, etc.
    - char_replace_map (list[dict]): A list of dicts defining characters to search for and replace
        in the timestamp str.
        - Example replace map: `[{"search": ":", "replace": "-"}, {"search": " ", "replace": "_"}]`
    """
    now = pendulum.now(tz=tz)

    if not as_str:
        return now
    else:
        if safe_str:
            str_fmt

            for r in char_replace_map:
                str_fmt = str_fmt.replace(r["search"], r["replace"])

        now_fmt = now.format(fmt=str_fmt)

        return now_fmt
