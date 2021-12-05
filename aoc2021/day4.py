import sys
from pathlib import Path
from typing import Callable

import aocd
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
TEST_DATA: str = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""
TEST_RESULT_PART1: int | None = 4512
TEST_RESULT_PART2: int | None = 1924


class Board:
    def __init__(self, data_str: str):
        self.data = [[int(num) for num in s.split(" ") if num] for s in data_str.splitlines()]
        assert len(self.data) == 5

        self.sets = [set(row) for row in self.data]
        for i in range(5):
            self.sets.append({row[i] for row in self.data})
        assert len(self.sets) == 10

    def mark(self, number: int) -> None:
        for s in self.sets:
            s.discard(number)

    def is_winning(self) -> bool:
        for s in self.sets:
            if s == set():
                return True
        return False

    def sum_remaining(self) -> int:
        return sum(set().union(*self.sets))


def part1(data: str) -> int:
    blocks = data.split("\n\n")
    numbers = [int(s) for s in blocks[0].split(",")]
    boards = [Board(s) for s in blocks[1:]]

    for num in numbers:
        for board in boards:
            board.mark(num)
            if board.is_winning():
                return board.sum_remaining() * num

    assert False


def part2(data: str) -> int:
    blocks = data.split("\n\n")
    numbers = [int(s) for s in blocks[0].split(",")]
    boards = [Board(s) for s in blocks[1:]]

    for num in numbers:
        for board in boards:
            board.mark(num)

        if len(boards) > 1:
            boards = [board for board in boards if not board.is_winning()]

        if len(boards) == 1 and boards[0].is_winning():
            return boards[0].sum_remaining() * num

    assert False


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
