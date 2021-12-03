import sys
from pathlib import Path

import aocd
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
TEST_DATA: str = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""
TEST_RESULT_PART1: int | None = 150
TEST_RESULT_PART2: int | None = 900


def part1(data: str) -> int:
    pos = depth = 0
    for line in data.splitlines():
        cmd, arg = line.split()
        arg = int(arg)

        match cmd:
            case "forward":
                pos += arg
            case "down":
                depth += arg
            case "up":
                depth -= arg

    return depth * pos


def part2(data: str) -> int:
    pos = depth = aim = 0
    for line in data.splitlines():
        cmd, arg = line.split()
        arg = int(arg)

        match cmd:
            case "forward":
                pos += arg
                depth += aim * arg
            case "down":
                aim += arg
            case "up":
                aim -= arg

    return depth * pos


def run_test_part1():
    if TEST_RESULT_PART1 is None:
        raise NotImplementedError
    assert part1(TEST_DATA) == TEST_RESULT_PART1


def run_test_part2():
    if TEST_RESULT_PART2 is None:
        raise NotImplementedError
    assert part2(TEST_DATA) == TEST_RESULT_PART2


def main() -> None:
    console.print(f"Running for day {DAY}", style="blue")

    # part 1
    proceed = True
    try:
        run_test_part1()
        console.print("Test part 1 succeeded.", style="green")
    except NotImplementedError:
        console.print("Test part 1 not implemented", style="yellow")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]
    except AssertionError:
        console.print("Test part 1 failed", style="red")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]

    if not proceed:
        sys.exit()

    console.print(
        f"Day {DAY} part 1 solution: {part1(aocd.get_data(day=DAY, year=2021))}", style="blue"
    )

    # part 2
    proceed = True
    try:
        run_test_part2()
        console.print("Test part 2 succeeded.", style="green")
    except NotImplementedError:
        console.print("Test part 2 not implemented", style="yellow")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]
    except AssertionError:
        console.print("Test part 2 failed", style="red")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]

    if not proceed:
        sys.exit()

    console.print(
        f"Day {DAY} part 2 solution: {part2(aocd.get_data(day=DAY, year=2021))}", style="blue"
    )


if __name__ == "__main__":
    main()
