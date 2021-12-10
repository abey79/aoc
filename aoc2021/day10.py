import sys
from pathlib import Path
from typing import Callable

import aocd
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
TEST_DATA: str = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""
TEST_RESULT_PART1: int | None = 26397
TEST_RESULT_PART2: int | None = 288957


MATCHING_BRACE = {
    "}": "{",
    "]": "[",
    ")": "(",
    ">": "<",
}

POINTS_PART1 = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

POINTS_PART2 = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


def analyse_line(line: str) -> (int, [str]):
    stack = []

    for c in line:
        match c:
            case "{" | "(" | "[" | "<":
                stack.append(c)
            case "}" | ")" | "]" | ">":
                if stack[-1] == MATCHING_BRACE[c]:
                    stack.pop()
                else:
                    return POINTS_PART1[c], stack
            case _:
                assert False
    return 0, stack


def part1(data: str) -> int:
    return sum(analyse_line(line)[0] for line in data.splitlines())


def part2(data: str) -> int:
    results = []
    for line in data.splitlines():
        score, stack = analyse_line(line)
        if score != 0:
            continue

        result = 0
        for s in reversed(stack):
            result *= 5
            result += POINTS_PART2[s]
        results.append(result)

    return sorted(results)[len(results) // 2]


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
