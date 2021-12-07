import math
import statistics
import sys
from pathlib import Path
from typing import Callable

import aocd
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
TEST_DATA: str = """16,1,2,0,4,2,7,1,2,14"""
TEST_RESULT_PART1: int | None = 37
TEST_RESULT_PART2: int | None = 168


def part1(data: str) -> int:
    positions = list(map(int, data.split(",")))
    new_pos = round(statistics.median(positions))

    return sum(abs(pos - new_pos) for pos in positions)


def compute_part2(positions: [int], target_pos: int) -> int:
    return int(
        sum(abs(pos - target_pos) * (1 + abs(pos - target_pos)) / 2 for pos in positions)
    )


def part2(data: str) -> int:
    positions = list(map(int, data.split(",")))
    pos1 = int(math.floor(statistics.mean(positions)))
    pos2 = int(math.ceil(statistics.mean(positions)))

    return min(compute_part2(positions, pos1), compute_part2(positions, pos2))


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
