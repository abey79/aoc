import sys
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
# noinspection SpellCheckingInspection
TEST_DATA: str = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
TEST_RESULT_PART1: int | None = 35
TEST_RESULT_PART2: int | None = 3351


def load_data(data: str) -> (np.ndarray, np.ndarray):
    lookup_data, img_data = data.split("\n\n")
    return (
        np.array([1 if c == "#" else 0 for c in lookup_data], dtype=int),
        np.array(
            [[1 if c == "#" else 0 for c in line] for line in img_data.splitlines()],
            dtype=int,
        ),
    )


KERNEL = np.array([2 ** i for i in range(9)], dtype=int).reshape((3, 3))


def enhance(data: str, num: int) -> int:
    lookup, img = load_data(data)
    assert len(lookup) == 512
    pad = 0

    for _ in range(num):
        img = np.pad(img, 2, constant_values=pad)
        idx = convolve2d(img, KERNEL, mode="valid")
        img = lookup[idx]
        pad = lookup[-1] if pad else lookup[0]

    return np.sum(img)


def part1(data: str) -> int:
    return enhance(data, 2)


def part2(data: str) -> int:
    return enhance(data, 50)


def run_test_part1(*args, **kwargs):
    if TEST_RESULT_PART1 is None:
        raise NotImplementedError
    # noinspection PyArgumentList
    assert part1(TEST_DATA, *args, **kwargs) == TEST_RESULT_PART1


def run_test_part2(*args, **kwargs):
    if TEST_RESULT_PART2 is None:
        raise NotImplementedError
    # noinspection PyArgumentList
    assert part2(TEST_DATA, *args, **kwargs) == TEST_RESULT_PART2


def run_solution(name: str, test_func: Callable, solution: Callable, *args, **kwargs):
    proceed = True
    try:
        test_func(*args, **kwargs)
        console.print(f"Test {name} succeeded.", style="green")
    except NotImplementedError:
        console.print(f"Test {name} not implemented", style="yellow")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]
    except AssertionError:
        console.print(f"Test {name} failed", style="red")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]

    if not proceed:
        sys.exit()

    result = solution(aocd.get_data(day=DAY, year=2021), *args, **kwargs)
    console.print(f"{name.capitalize()} solution: {result}", style="blue")


def main() -> None:
    console.print(f"Running for day {DAY}", style="blue")
    run_solution("part 1", run_test_part1, part1)
    run_solution("part 2", run_test_part2, part2)


if __name__ == "__main__":
    main()
