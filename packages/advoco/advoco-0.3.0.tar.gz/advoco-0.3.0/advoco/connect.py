import requests
import os
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any, overload, Literal

from .exceptions import NoTokenError

AOC_URL_TPL = "https://adventofcode.com/{year}/day/{day}"


def get_auth_cookie_from_env() -> dict:
    try:
        token = os.environ["AOC_TOKEN"]
    except KeyError:
        raise NoTokenError(
            "No Advent of Code auth token in environment. Please set 'AOC_TOKEN'."
        )
    else:
        return {"session": token}


@overload
def send_request(
    method: str,
    year: str,
    day: str,
    mmm_soup: Literal[True],
    endpoint: Optional[str] = None,
    body: Optional[dict] = None,
) -> BeautifulSoup:
    ...


@overload
def send_request(
    method: str,
    year: str,
    day: str,
    mmm_soup: Literal[False] = False,
    endpoint: Optional[str] = None,
    body: Optional[dict] = None,
) -> str:
    ...


def send_request(
    method: str,
    year: str,
    day: str,
    mmm_soup: bool = False,
    endpoint: Optional[str] = None,
    body: Optional[dict] = None,
) -> str | BeautifulSoup:
    endpoint = endpoint or ""
    url = AOC_URL_TPL.format(year=year, day=day) + endpoint
    request_kwargs: Dict[str, Any] = {"cookies": get_auth_cookie_from_env()}
    if body:
        request_kwargs["data"] = body

    resp = requests.request(method, url, **request_kwargs)
    resp.raise_for_status()

    if mmm_soup:
        return BeautifulSoup(resp.content, "html.parser")
    else:
        return resp.text
