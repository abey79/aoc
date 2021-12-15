import itertools
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
TEST_DATA: str = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
TEST_RESULT_PART1: int | None = 1588
TEST_RESULT_PART2: int | None = 2188189693529


def part1(data: str, iter_count: int) -> int:
    template, rule_data = data.split("\n\n")

    rules = {}
    for rule in rule_data.splitlines():
        (a, b), c = rule.split(" -> ")
        rules[(a, b)] = c

    letter_counter = Counter(template)
    pair_counter = Counter(itertools.pairwise(template))

    for _ in range(iter_count):
        new_pair_counter = Counter()

        for (a, b), n in pair_counter.items():
            c = rules[(a, b)]

            new_pair_counter.update({a + c: n, c + b: n})
            letter_counter.update({c: n})

        pair_counter = new_pair_counter

    res = letter_counter.most_common()
    return res[0][1] - res[-1][1]


def run_test_part1(*args, **kwargs):
    if TEST_RESULT_PART1 is None:
        raise NotImplementedError
    assert part1(TEST_DATA, *args, **kwargs) == TEST_RESULT_PART1


def run_test_part2(*args, **kwargs):
    if TEST_RESULT_PART2 is None:
        raise NotImplementedError
    assert part1(TEST_DATA, *args, **kwargs) == TEST_RESULT_PART2


def run_solution(
    name: str,
    test_func: Callable,
    solution: Callable,
    *args,
    **kwargs,
):
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
    run_solution("part 1", run_test_part1, part1, 10)
    run_solution("part 2", run_test_part2, part1, 40)


if __name__ == "__main__":
    main()
