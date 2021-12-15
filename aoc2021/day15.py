import sys
from pathlib import Path
from typing import Callable

import aocd
import numpy as np
from rich.console import Console
from rich.traceback import install
from scipy.signal import convolve2d
from skimage.graph import route_through_array

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
# noinspection SpellCheckingInspection
TEST_DATA: str = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
TEST_RESULT_PART1: int | None = 40
TEST_RESULT_PART2: int | None = 315


def part1(data: str) -> int:
    cavern = np.array([[int(s) for s in line] for line in data.splitlines()], dtype=int)

    energy = -np.ones(cavern.shape, dtype=int)
    energy[-1, -1] = cavern[-1, -1]
    kernel = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=int)

    while np.any(to_fill := energy == -1):
        indices = (convolve2d(~to_fill, kernel, mode="same") > 0) & to_fill
        energy_padded = np.pad(energy, 1, mode="edge")

        for i, j in zip(*np.where(indices)):
            energy[i, j] = cavern[i, j] + min(
                filter(
                    lambda x: x != -1,
                    (
                        energy_padded[i, j + 1],
                        energy_padded[i + 2, j + 1],
                        energy_padded[i + 1, j],
                        energy_padded[i + 1, j + 2],
                    ),
                )
            )

    return energy[0, 0] - cavern[0, 0]


def part2(data: str) -> int:
    cavern = np.array([[int(s) for s in line] for line in data.splitlines()], dtype=int)

    h, w = cavern.shape
    cavern_full = np.empty((w * 5, h * 5), dtype=int)
    for i in range(5):
        for j in range(5):
            cavern_full[i * h : (i + 1) * h, j * w : (j + 1) * w] = cavern + i + j
    cavern = (cavern_full - 1) % 9 + 1

    # Full disclosure: part1 code somehow works for the test grid but *NOT* for my actual data.
    # Couldn't find the issue in a reasonable time, so I basically cheated :)
    _, cost = route_through_array(
        cavern, (0, 0), (-1, -1), fully_connected=False, geometric=False
    )
    return int(cost) - cavern[0, 0]


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
