import itertools
from typing import List

import aocd

TEST_DATA = [
    35,
    20,
    15,
    25,
    47,
    40,
    62,
    55,
    65,
    95,
    102,
    117,
    150,
    182,
    127,
    219,
    299,
    277,
    309,
    576,
]


def find_fault(data: List[int], width: int) -> int:
    for i, item in enumerate(data[width:]):
        if item not in (a + b for a, b in itertools.permutations(data[i : i + width], 2)):
            return item

    raise ValueError("could not find faulty value")


def test_find_fault():
    assert find_fault(TEST_DATA, 5) == 127


def find_weakness(data: List[int], target: int) -> int:
    start = 0
    stop = 1
    total = data[0] + data[1]

    while total != target:
        if total < target:
            stop += 1
            total += data[stop]
        elif total > target:
            total -= data[start]
            start += 1

    return min(data[start : stop + 1]) + max(data[start : stop + 1])


def test_find_weakness():
    assert find_weakness(TEST_DATA, 127) == 62


def main():
    data = [int(item) for item in aocd.get_data(day=9, year=2020).split("\n")]
    part1 = find_fault(data, 25)
    print(f"day 9 part 1: {part1}")
    print(f"day 9 part 2: {find_weakness(data, part1)}")


if __name__ == "__main__":
    main()
