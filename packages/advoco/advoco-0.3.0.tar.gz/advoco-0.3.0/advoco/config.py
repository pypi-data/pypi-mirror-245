import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

import pytz

from .connect import send_request
from .exceptions import DateOutOfRangeError

AOC_TZ = pytz.timezone("America/New_York")


def get_day_from_context(context: Path) -> str:
    if context.is_file() and context.suffix == ".py":
        return "".join(filter(str.isdigit, context.stem))
    else:
        return ""


def get_year_from_context(context: Path) -> str:
    context_dir = context.parent if context.is_file() else context
    match = re.search(r"20\d{2}", context_dir.stem)
    if match:
        return match.group()
    else:
        return ""


def resolve_day_and_year(
    calling_context: Path, year: Optional[str] = None, day: Optional[str] = None
) -> Tuple[str, str]:
    now = datetime.now(tz=AOC_TZ)

    resolved_day = day or get_day_from_context(calling_context) or str(now.day)
    resolved_year = year or get_year_from_context(calling_context) or str(now.year)

    if int(resolved_day) not in range(1, 26):
        raise DateOutOfRangeError(f"Day '{resolved_day}' falls outside of Advent!")
    if int(resolved_year) < 2015:
        raise DateOutOfRangeError(f"Year '{resolved_year}' is before AoC started")

    return resolved_day, resolved_year


def get_active_part(year: str, day: str) -> str:
    """
    Return the status of the given year/day combo. Returns the puzzle part that is
    currently active for that day. If the day is complete (both puzzle parts done),
    returns "-1"

    If the day is complete, a "day-success" classed `p` tag will exist on the page.
    If there are two "day-desc" classed `article` tags, we're on part two.
    Otherwise, we're on part 1

    If you pass an invalid day, `send_request` will yell at you so no need to handle
    here
    """
    soup = send_request("get", year, day, mmm_soup=True)

    if soup.find(
        lambda tag: tag.name == "p" and tag.text.startswith("Both parts of this puzzle")
    ):
        return "-1"

    day_descs = soup.find_all("article", {"class": "day-desc"})
    if len(day_descs) == 2:
        return "2"
    else:
        return "1"
