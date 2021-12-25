import itertools
import time
from pathlib import Path

import aocd
import numpy as np
import pytest
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

YEAR = 2021
DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
# noinspection SpellCheckingInspection
TEST_DATA: str = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""
TEST_RESULT_PART1: int | None = 58
DATA = aocd.get_data(day=DAY, year=2021)


def part1_set(data: str) -> int:
    east_set = set()
    south_set = set()
    lines = data.splitlines()
    width = len(lines[0])
    height = len(lines)

    for j, line in enumerate(lines):
        for i, c in enumerate(line):
            match c:
                case "v":
                    south_set.add((i, j))
                case ">":
                    east_set.add((i, j))
                case ".":
                    pass
                case _:
                    assert False

    for n in itertools.count():
        new_east_set = set()
        new_south_set = set()

        for east in east_set:
            new_east = (east[0] + 1) % width, east[1]
            if new_east not in east_set and new_east not in south_set:
                new_east_set.add(new_east)
            else:
                new_east_set.add(east)

        for south in south_set:
            new_south = south[0], (south[1] + 1) % height
            if new_south not in new_east_set and new_south not in south_set:
                new_south_set.add(new_south)
            else:
                new_south_set.add(south)

        if new_south_set == south_set and new_east_set == east_set:
            return n + 1
        else:
            east_set = new_east_set
            south_set = new_south_set


def part1_numpy(data: str) -> int:
    east_set = set()
    south_set = set()
    lines = data.splitlines()
    world = np.zeros(shape=(len(lines), len(lines[0])), dtype=np.uint8)

    for j, line in enumerate(lines):
        for i, c in enumerate(line):
            match c:
                case "v":
                    world[j, i] = 2
                case ">":
                    world[j, i] = 1
                case ".":
                    pass
                case _:
                    assert False

    for n in itertools.count():
        new_world = world.copy()

        # east
        idx = (world == 1) & (np.roll(world, -1, axis=1) == 0)
        new_world[idx] = 0
        new_world[np.roll(idx, 1, axis=1)] = 1

        # south
        idx = (new_world == 2) & (np.roll(new_world, -1, axis=0) == 0)
        new_world[idx] = 0
        new_world[np.roll(idx, 1, axis=0)] = 2

        if np.all(world == new_world):
            return n + 1
        else:
            world = new_world


@pytest.mark.skipif(TEST_RESULT_PART1 is None, reason="part 1 test result not provided")
def test_part1_set():
    assert part1_set(TEST_DATA) == TEST_RESULT_PART1


@pytest.mark.skipif(TEST_RESULT_PART1 is None, reason="part 1 test result not provided")
def test_part1_numpy():
    assert part1_numpy(TEST_DATA) == TEST_RESULT_PART1


def main() -> None:
    console.rule(f"AOC {YEAR} day {DAY}", style="blue")
    console.print("Tests: ", end="", style="blue")
    pytest.main(["-q", __file__])
    start = time.time()
    res = part1_set(DATA)
    delta = time.time() - start
    console.print(
        f"Part [bold cyan]1[/] (set) solution: [bold green]{res}[/] "
        f"(execution time: [bold cyan]{delta*1000:.2f}ms[/])",
        style="blue",
        highlight=False,
    )

    start = time.time()
    res = part1_numpy(DATA)
    delta = time.time() - start
    console.print(
        f"Part [bold cyan]1[/] (numpy) solution: [bold green]{res}[/] "
        f"(execution time: [bold cyan]{delta * 1000:.2f}ms[/])",
        style="blue",
        highlight=False,
    )


if __name__ == "__main__":
    main()
