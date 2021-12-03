import sys
from pathlib import Path
from typing import Callable

import aocd
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
TEST_DATA: str = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
TEST_RESULT_PART1: int | None = 198
TEST_RESULT_PART2: int | None = 230


def count_bits(lines: [str]) -> [int]:
    counter = [0] * len(lines[0])
    for line in lines:
        for i, s in enumerate(line):
            counter[i] += int(s)
    return counter


def part1(data: str) -> int:
    lines = data.splitlines()

    counter = count_bits(lines)
    gamma = "".join("1" if cnt > len(lines) / 2 else "0" for cnt in counter)

    epsilon = ""
    for s in gamma:
        match s:
            case "1":
                epsilon += "0"
            case "0":
                epsilon += "1"

    return int(gamma, 2) * int(epsilon, 2)


def part2(data: str) -> int:
    lines = data.splitlines()
    iter_count = len(lines[0])

    for i in range(iter_count):
        counter = count_bits(lines)
        bit = "1" if counter[i] >= len(lines) / 2 else "0"
        lines = [line for line in lines if line[i] == bit]
        if len(lines) == 1:
            oxygen = int("".join(lines[0]), 2)
            break

    lines = data.splitlines()
    for i in range(iter_count):
        counter = count_bits(lines)
        bit = "1" if counter[i] < len(lines) / 2 else "0"
        lines = [line for line in lines if line[i] == bit]
        if len(lines) == 1:
            co2 = int("".join(lines[0]), 2)
            break

    return oxygen * co2


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
