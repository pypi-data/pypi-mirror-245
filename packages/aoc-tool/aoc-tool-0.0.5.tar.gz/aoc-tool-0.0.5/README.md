# 🎄aoc-tool 🎁

Python functions to aid in getting inputs and submitting results to Advent of Code. The package provides `get_input` which gets and caches a day's input file and `submit` which submits an answer and displays the server's response. Inputs are cached locally in `$HOME/.cache/aoc_tool`. Please throttle your submissions to Advent of Code's servers when using `submit`.

## Dependencies

None.

## Installation

```bash
python3 -m pip install aoc-tool
```

## Usage

Log in to [Advent of Code](https://adventofcode.com). Get your session cookie from the browser and save it to an environment variable named `AOC_COOKIE`.

```python
from aoc_tool import get_input, submit

if __name__ == "__main__":
    year, day, level = 2022, 10, 1
    aoc_input = get_input(year, day)

    # Do some calculations
    # ans = <calculations>

    submit(ans, year, day, level)
```
