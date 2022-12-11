import aocd
import numpy as np


def seat_id(seat: str) -> int:
    row = int(seat[:7].replace("F", "0").replace("B", "1"), 2)
    col = int(seat[-3:].replace("L", "0").replace("R", "1"), 2)
    return row * 8 + col


def test_seat_id():
    assert seat_id("BFFFBBFRRR") == 567
    assert seat_id("FFFBBBFRRR") == 119


def day5_part1() -> int:
    return max(seat_id(seat) for seat in aocd.get_data(day=5, year=2020).split("\n"))


def day5_part2() -> int:
    a = np.array(
        list(sorted(seat_id(seat) for seat in aocd.get_data(day=5, year=2020).split("\n")))
    )
    (b,) = np.nonzero(np.diff(a) == 2)
    return a[b[0]] + 1


def main():
    print("day 5 part 1: " + str(day5_part1()))
    print("day 5 part 2: " + str(day5_part2()))


if __name__ == "__main__":
    main()
