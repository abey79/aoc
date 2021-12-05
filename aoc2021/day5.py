import re
import sys
from collections import Counter
from pathlib import Path
from typing import Callable

import aocd
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
TEST_DATA: str = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""
TEST_RESULT_PART1: int | None = 5
TEST_RESULT_PART2: int | None = 12


def part1(data: str) -> int:
    counter = Counter()
    for line in data.splitlines():
        coords = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line).groups()
        match tuple(int(c) for c in coords):
            case (x1, y1, x2, y2) if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    counter.update([(x1, y)])
            case (x1, y1, x2, y2) if y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    counter.update([(x, y1)])

    return sum(1 if cnt >= 2 else 0 for cnt in counter.values())


def part2(data: str) -> int:
    counter = Counter()
    for line in data.splitlines():
        coords = re.match(r"(\d+),(\d+) -> (\d+),(\d+)", line).groups()
        match tuple(int(c) for c in coords):
            case (x1, y1, x2, y2) if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    counter.update([(x1, y)])
            case (x1, y1, x2, y2) if y1 == y2:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    counter.update([(x, y1)])
            case (x1, y1, x2, y2) if (x1 - x2) == (y1 - y2):
                for i in range(abs(x1 - x2) + 1):
                    counter.update([(min(x1, x2) + i, min(y1, y2) + i)])
            case (x1, y1, x2, y2) if (x1 - x2) == -(y1 - y2):
                for i in range(abs(x1 - x2) + 1):
                    counter.update([(min(x1, x2) + i, max(y1, y2) - i)])

    return sum(1 if cnt >= 2 else 0 for cnt in counter.values())


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
