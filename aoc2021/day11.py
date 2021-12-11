import itertools
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
TEST_DATA: str = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
TEST_RESULT_PART1: int | None = 1656
TEST_RESULT_PART2: int | None = 195

KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=int)


def part1(data: str) -> int:
    cavern = np.array([[int(s) for s in line] for line in data.splitlines()], dtype=int)

    flash_count = 0

    for _ in range(100):
        cavern += 1
        flashing_this_step = np.zeros(shape=cavern.shape, dtype=bool)

        while (flashing := (cavern > 9) & (~flashing_this_step)).sum() > 0:
            energy = convolve2d(flashing, KERNEL, mode="same")
            flashing_this_step |= flashing
            cavern[flashing] = 0
            cavern[~flashing_this_step] += energy[~flashing_this_step]

        flash_count += flashing_this_step.sum()

    return flash_count


def part2(data: str) -> int:
    cavern = np.array([[int(s) for s in line] for line in data.splitlines()], dtype=int)

    flash_count = 0

    for step in itertools.count():
        if np.all(cavern == 0):
            return step
        cavern += 1

        flashing_this_step = np.zeros(shape=cavern.shape, dtype=bool)

        while (flashing := (cavern > 9) & (~flashing_this_step)).sum() > 0:
            energy = convolve2d(flashing, KERNEL, mode="same")
            flashing_this_step |= flashing
            cavern[flashing] = 0
            cavern[~flashing_this_step] += energy[~flashing_this_step]

        flash_count += flashing_this_step.sum()


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
