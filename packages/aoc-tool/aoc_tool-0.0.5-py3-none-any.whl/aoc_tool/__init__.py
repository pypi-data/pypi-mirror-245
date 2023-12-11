"""
Helper functions for Advent of Code. You will need to get your session cookie after logging in and save to the
environment variable AOC_COOKIE.
"""

import os
import re
from pathlib import Path
from typing import Any
from urllib import parse, request

USER_AGENT = "github.com/wesbarnett/aoc-tool by wes@barnettphd.com"


def get_input(year: int, day: int) -> str:
    """Get input for specified year & day, cache locally."""
    basepath = Path(f"{os.environ['HOME']}/.cache/aoc_tool")
    basepath.mkdir(parents=True, exist_ok=True)
    p = basepath / f"infile_{year}_{day}"

    try:
        cookie = os.environ["AOC_COOKIE"]
    except KeyError:
        raise KeyError(
            "Environment variable AOC_COOKIE is not set. Log in to Advent of Code, get your session cookie from the "
            "browser, and set it to the environment variable AOC_COOKIE."
        )

    try:
        aoc_input = p.read_text()
    except FileNotFoundError:
        url = f"https://adventofcode.com/{year}/day/{day}/input"
        headers = {
            "Cookie": f"session={cookie}",
            "User-Agent": USER_AGENT,
        }
        req = request.Request(url, headers=headers)
        with request.urlopen(req) as response:
            aoc_input = response.read().decode("utf-8")
            p.write_text(aoc_input)
    return aoc_input


def submit(answer: Any, year: int, day: int, level: int) -> None:
    """Submit answer to Advent of Code for given day, year, and level."""
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    try:
        cookie = os.environ["AOC_COOKIE"]
    except KeyError:
        raise KeyError(
            "Environment variable AOC_COOKIE is not set. Log in to Advent of Code, get your session cookie from the "
            "browser, and set it to the environment variable AOC_COOKIE."
        )
    headers = {
        "Cookie": f"session={cookie}",
        "User-Agent": USER_AGENT,
    }
    data = parse.urlencode({"level": level, "answer": answer}).encode()
    req = request.Request(url, data=data, headers=headers)
    with request.urlopen(req) as response:
        resp = response.read().decode("utf-8")
    match = re.findall("<article>(.*)</article>", resp, re.S)
    tag_re = re.compile(r"(<!--.*?-->|<[^>]*>)")
    text = tag_re.sub("", match[0]).lstrip("\n").rstrip("\n")
    print(text)
