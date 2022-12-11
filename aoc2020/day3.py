from typing import List, Tuple

import aocd
import numpy as np

DEMO_DATA = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""


def parse(data: str) -> np.ndarray:
    return np.array([[1 if c == "#" else 0 for c in line] for line in data.split("\n")])


def test_parse():
    res = parse(DEMO_DATA)
    assert res[0, 2] == 1
    assert res[3, 2] == 1
    assert res[5, 6] == 0


def get_indices(
    data: np.ndarray, col_offset: int, row_offset: int = 1
) -> Tuple[List[int], List[int]]:
    rows = np.arange(data.shape[0], step=row_offset)
    cols = (np.arange(len(rows)) * col_offset) % data.shape[1]
    return list(rows), list(cols)


def solve_day3(data: np.ndarray, col_offset: int = 3, row_offset: int = 1) -> int:
    rows, cols = get_indices(data, col_offset, row_offset)
    return data[rows, cols].sum()


def test_solve_day3():
    assert solve_day3(parse(DEMO_DATA)) == 7


def solve_day3_part2(data: np.ndarray) -> int:
    return (
        solve_day3(data, 1, 1)
        * solve_day3(data, 3, 1)
        * solve_day3(data, 5, 1)
        * solve_day3(data, 7, 1)
        * solve_day3(data, 1, 2)
    )


def test_solve_day3_part2():
    assert solve_day3_part2(parse(DEMO_DATA)) == 336


def main():
    data = aocd.get_data(day=3, year=2020)
    print("Day 3 part 1 results: " + str(solve_day3(parse(data))))
    print("Day 3 part 2 results: " + str(solve_day3_part2(parse(data))))


if __name__ == "__main__":
    main()
