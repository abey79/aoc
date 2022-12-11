import itertools
from typing import Optional, Sequence

import aocd


def solve_day1(entries: Sequence[int]) -> Optional[int]:
    for a, b in itertools.permutations(entries, 2):
        if a + b == 2020:
            return a * b
    return None


def solve_day1_part2(entries: Sequence[int]) -> Optional[int]:
    for a, b, c in itertools.permutations(entries, 3):
        if a + b + c == 2020:
            return a * b * c
    return None


def test_solve_day1():
    assert solve_day1([1721, 979, 366, 299, 675, 1456]) == 514579


def test_solve_day1_part2():
    assert solve_day1_part2([1721, 979, 366, 299, 675, 1456]) == 241861950


if __name__ == "__main__":
    data = [int(s) for s in aocd.get_data(day=1, year=2020).split("\n")]
    print(f"Day 1 solution: {solve_day1(data)}")
    print(f"Day 1 part 2 solution: {solve_day1_part2(data)}")
