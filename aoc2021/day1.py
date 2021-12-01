import aocd

from aoc_utils import data_to_int


def solve_day1(data: str) -> int:
    data = data_to_int(data)
    accum = 0
    for a, b in zip(data[:-1], data[1:]):
        match b > a:
            case True:
                accum += 1
    return accum


def solve_day1_part2(data: str) -> int:
    data = data_to_int(data)
    accum = 0

    val = sum(data[:3])

    for back, front in zip(data[:-2], data[3:]):
        new_val = val - back + front
        match new_val > val:
            case True:
                accum += 1
        val = new_val

    return accum


TEST_DATA = """199
200
208
210
200
207
240
269
260
263"""


def test_day1_part2():
    assert solve_day1_part2(TEST_DATA) == 5


def main() -> None:
    print(f"Day 1 solution: {solve_day1(aocd.get_data(day=1, year=2021))}")
    print(f"Day 1 part 2 solution: {solve_day1_part2(aocd.get_data(day=1, year=2021))}")


if __name__ == "__main__":
    main()
