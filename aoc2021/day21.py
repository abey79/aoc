import dataclasses
import sys
from functools import cache
from pathlib import Path
from typing import Callable

import aocd
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
# noinspection SpellCheckingInspection
TEST_DATA: str = """Player 1 starting position: 4
Player 2 starting position: 8"""
TEST_RESULT_PART1: int | None = 739785
TEST_RESULT_PART2: int | None = 444356092776315


def part1(data: str) -> int:
    p1, p2 = [int(line.split(" ")[-1]) - 1 for line in data.splitlines()]
    rolls = 0
    dice = 1
    p1_score = p2_score = 0

    def roll():
        nonlocal dice, rolls
        val = dice
        rolls += 1
        dice = (dice % 100) + 1
        return val

    while True:
        p1 = (p1 + sum(roll() for _ in range(3))) % 10
        p1_score += p1 + 1

        if p1_score >= 1000:
            return p2_score * rolls

        p2 = (p2 + sum(roll() for _ in range(3))) % 10
        p2_score += p2 + 1

        if p2_score >= 1000:
            return p1_score * rolls


@dataclasses.dataclass(frozen=True)
class State:
    p1: int
    p2: int
    p1_score: int = 0
    p2_score: int = 0

    def roll(self, roll: int, p1_turn: bool) -> "State":
        if p1_turn:
            new_pos = (self.p1 + roll) % 10
            return State(
                p1=new_pos,
                p1_score=self.p1_score + new_pos + 1,
                p2=self.p2,
                p2_score=self.p2_score,
            )
        else:
            new_pos = (self.p2 + roll) % 10
            return State(
                p2=new_pos,
                p2_score=self.p2_score + new_pos + 1,
                p1=self.p1,
                p1_score=self.p1_score,
            )


DIRAC = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


@cache
def count_wins(state: State, p1_turn: bool, max_score: int) -> (int, int):
    p1_tot = p2_tot = 0
    for roll, weight in DIRAC.items():
        new_state = state.roll(roll, p1_turn)
        if p1_turn and new_state.p1_score >= max_score:
            p1_tot += weight
        elif not p1_turn and new_state.p2_score >= max_score:
            p2_tot += weight
        else:
            p1_wins, p2_wins = count_wins(new_state, not p1_turn, max_score)
            p1_tot += weight * p1_wins
            p2_tot += weight * p2_wins
    return p1_tot, p2_tot


def part2(data: str) -> int:
    p1, p2 = [int(line.split(" ")[-1]) - 1 for line in data.splitlines()]
    return max(count_wins(State(p1, p2), True, 21))


def run_test_part1(*args, **kwargs):
    if TEST_RESULT_PART1 is None:
        raise NotImplementedError
    # noinspection PyArgumentList
    assert part1(TEST_DATA, *args, **kwargs) == TEST_RESULT_PART1


def run_test_part2(*args, **kwargs):
    if TEST_RESULT_PART2 is None:
        raise NotImplementedError
    # noinspection PyArgumentList
    assert part2(TEST_DATA, *args, **kwargs) == TEST_RESULT_PART2


def run_solution(name: str, test_func: Callable, solution: Callable, *args, **kwargs):
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
    run_solution("part 1", run_test_part1, part1)
    run_solution("part 2", run_test_part2, part2)


if __name__ == "__main__":
    main()
