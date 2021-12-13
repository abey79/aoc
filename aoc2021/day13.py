import sys
from pathlib import Path
from typing import Callable

import aocd
import numpy as np
from matplotlib import pyplot as plt
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
TEST_DATA: str = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
TEST_RESULT_PART1: int | None = 17


def part1(data: str) -> int:
    coords, folds = data.split("\n\n")
    coords_ij = []
    for coord in coords.splitlines():
        j, i = coord.split(",")
        coords_ij.append((int(i), int(j)))

    sheet = np.zeros(
        (max(coords_ij, key=lambda x: x[0])[0] + 1, max(coords_ij, key=lambda x: x[1])[1] + 1),
        dtype=bool,
    )
    for i, j in coords_ij:
        sheet[i, j] = True

    match folds.splitlines()[0].split("="):
        case "fold along y", val:
            val = int(val)
            sheet = sheet[0:val, :] | sheet[-1:val:-1, :]
        case "fold along x", val:
            val = int(val)
            sheet = sheet[:, 0:val] | sheet[:, -1:val:-1]

    return sheet.sum()


def part2(data: str) -> None:
    coords, folds = data.split("\n\n")
    coords_ij = []
    for coord in coords.splitlines():
        j, i = coord.split(",")
        coords_ij.append((int(i), int(j)))

    # HACK: added 1 to y size because my input requires it
    sheet = np.zeros(
        (max(coords_ij, key=lambda x: x[0])[0] + 2, max(coords_ij, key=lambda x: x[1])[1] + 1),
        dtype=bool,
    )
    for i, j in coords_ij:
        sheet[i, j] = True

    for line in folds.splitlines():
        match line.split("="):
            case "fold along y", val:
                val = int(val)
                sheet = sheet[0:val, :] | sheet[-1:val:-1, :]
            case "fold along x", val:
                val = int(val)
                sheet = sheet[:, 0:val] | sheet[:, -1:val:-1]

    plt.imshow(sheet)
    plt.show()


def run_test_part1():
    if TEST_RESULT_PART1 is None:
        raise NotImplementedError
    assert part1(TEST_DATA) == TEST_RESULT_PART1


def run_solution(
    name: str, test_func: Callable[[], None] | None, solution: Callable[[str], int]
):
    proceed = True
    if test_func is None:
        console.print(f"Test {name} skipped.", style="green")
    else:
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
    run_solution("part 2", None, part2)


if __name__ == "__main__":
    main()
