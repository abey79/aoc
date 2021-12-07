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
TEST_DATA: str = """3,4,3,1,2"""
TEST_RESULT_PART1: int | None = 5934
TEST_RESULT_PART2: int | None = 26984457539


def part1(data: str) -> int:
    fishes = list(map(int, data.split(",")))

    for gen in range(80):
        fishes = [f - 1 for f in fishes]
        offsprings = 0
        for i in range(len(fishes)):
            if fishes[i] == -1:
                fishes[i] = 6
                offsprings += 1
        fishes += [8] * offsprings

    return len(fishes)


def part2(data: str, gen_count: int) -> int:
    fish_count = Counter(map(int, data.split(",")))

    for _ in range(gen_count):
        new_fish_count = Counter()
        new_fish_count[8] += fish_count[0]
        new_fish_count[6] += fish_count[0]
        new_fish_count.update({k - 1: v for k, v in fish_count.items() if k > 0})
        fish_count = new_fish_count

    return fish_count.total()


def run_test_part1():
    if TEST_RESULT_PART1 is None:
        raise NotImplementedError
    assert part1(TEST_DATA) == TEST_RESULT_PART1


def run_test_part2():
    if TEST_RESULT_PART2 is None:
        raise NotImplementedError
    assert part2(TEST_DATA, 18) == 26
    assert part2(TEST_DATA, 80) == TEST_RESULT_PART1
    assert part2(TEST_DATA, 256) == TEST_RESULT_PART2


def run_solution(name: str, test_func: Callable[[], None], solution: Callable[[str], int]):
    proceed = True
    try:
        test_func()
        console.print(f"Test {name} succeeded.", style="green")
    except NotImplementedError:
        console.print(f"Test {name} not implemented", style="yellow")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]
    except AssertionError as err:
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
    run_solution("part 2", run_test_part2, lambda x: part2(x, 256))


if __name__ == "__main__":
    main()
