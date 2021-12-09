import sys
from functools import reduce
from pathlib import Path
from typing import Callable

import aocd
import numpy as np
from rich.console import Console
from rich.traceback import install
from scipy.signal import convolve2d

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
TEST_DATA: str = """2199943210
3987894921
9856789892
8767896789
9899965678"""
TEST_RESULT_PART1: int | None = 15
TEST_RESULT_PART2: int | None = 1134


def part1(data: str) -> int:
    floor = np.array([[int(c) for c in s] for s in data.splitlines()], dtype=int)
    floor_n = np.roll(floor, 1, axis=0)
    floor_n[0, :] = 9
    floor_s = np.roll(floor, -1, axis=0)
    floor_s[-1, :] = 9
    floor_e = np.roll(floor, -1, axis=1)
    floor_e[:, -1] = 9
    floor_w = np.roll(floor, 1, axis=1)
    floor_w[:, -0] = 9

    idx = floor < np.stack([floor_n, floor_s, floor_w, floor_e], axis=2).min(axis=2)
    return (floor[idx] + 1).sum()


def part2(data: str) -> int:
    floor = np.array([[int(c) for c in s] for s in data.splitlines()], dtype=int)
    floor_n = np.roll(floor, 1, axis=0)
    floor_n[0, :] = 9
    floor_s = np.roll(floor, -1, axis=0)
    floor_s[-1, :] = 9
    floor_e = np.roll(floor, -1, axis=1)
    floor_e[:, -1] = 9
    floor_w = np.roll(floor, 1, axis=1)
    floor_w[:, -0] = 9

    # find lows
    idx = floor < np.stack([floor_n, floor_s, floor_w, floor_e], axis=2).min(axis=2)
    lows = [tuple(coord) for coord in np.argwhere(idx)]

    kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]])

    basin_size = []
    for low in lows:

        basin = np.zeros(floor.shape, dtype=bool)
        basin[low] = True

        while True:
            expend = (convolve2d(basin, kernel, mode="same") > 0) & ~basin
            expend &= floor != 9
            new_basin = basin | expend

            if np.all(new_basin == basin):
                break
            else:
                basin = new_basin

        basin_size.append(basin.sum())

    return reduce(lambda x, y: x * y, sorted(basin_size, reverse=True)[:3])


def run_test_part1():
    if TEST_RESULT_PART1 is None:
        raise NotImplementedError
    assert part1(TEST_DATA) == TEST_RESULT_PART1


def run_test_part2():
    if TEST_RESULT_PART2 is None:
        raise NotImplementedError
    assert part2(TEST_DATA) == TEST_RESULT_PART2


def run_solution(name: str, test_func: Callable[[], None], solution: Callable[[str], int]):
    proceed = True
    try:
        test_func()
        console.print(f"Test {name} succeeded.", style="green")
    except NotImplementedError:
        console.print(f"Test {name} not implemented", style="yellow")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]
    except AssertionError:
        console.print(f"Test {name} failed", style="red")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]

    if not proceed:
        sys.exit()

    console.print(
        f"{name.capitalize()} solution: {solution(aocd.get_data(day=DAY, year=2021))}",
        style="blue",
    )


def main() -> None:
    console.print(f"Running for day {DAY}", style="blue")
    run_solution("part 1", run_test_part1, part1)
    run_solution("part 2", run_test_part2, part2)


if __name__ == "__main__":
    main()
