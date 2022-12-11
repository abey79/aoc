from typing import List

import aocd
import numpy as np

TEST_DATA = [16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4]

TEST_DATA2 = [
    28,
    33,
    18,
    42,
    31,
    14,
    46,
    20,
    48,
    47,
    24,
    23,
    49,
    45,
    19,
    38,
    39,
    11,
    1,
    32,
    25,
    35,
    8,
    17,
    7,
    9,
    4,
    2,
    34,
    10,
    3,
]


def day10_part1(data: List[int]) -> int:
    data = list(sorted(data))
    arr = np.array([0] + data + [data[-1] + 3])
    d = np.diff(arr)
    print(arr[-1])
    print(np.histogram(d))
    return np.sum(d == 1) * np.sum(d == 3)


def test_day10_part1():
    assert day10_part1(TEST_DATA2) == 22 * 10


def day10_part2(data: List[int]) -> int:
    data = list(sorted(data))
    arr = np.array([0] + data + [data[-1] + 3])
    s = (
        "".join(chr(a) for a in np.diff(arr) + ord("a") - 1)
        .replace("aaaa", "W")
        .replace("aaa", "X")
        .replace("aa", "Y")
    )
    return (7 ** s.count("W")) * (4 ** s.count("X")) * (2 ** s.count("Y"))


def test_day10_part2():
    # assert day10_part2(TEST_DATA) == 8
    # assert day10_part2(TEST_DATA2) == 19208

    data = [int(item) for item in aocd.get_data(day=10, year=2020).split("\n")]
    day10_part2(data)


def main():
    data = [int(item) for item in aocd.get_data(day=10, year=2020).split("\n")]
    print(f"day 10 part 1: {day10_part1(data)}")
    print(f"day 10 part 2: {day10_part2(data)}")


if __name__ == "__main__":
    main()
