import aocd
import numba
import numpy as np
from numba import njit

TEST_DATA = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

EMPTY = 0
SEAT = 1
OCCUPIED = 2

MAP = {".": EMPTY, "L": SEAT, "#": OCCUPIED}


def parse(data: str) -> np.ndarray:
    return np.array([[MAP[c] for c in line] for line in data.split("\n")])


def neighborhood(data: np.ndarray) -> np.ndarray:
    data = np.pad(data, ((1, 1), (1, 1)), "constant") == OCCUPIED
    return np.stack(
        [
            data[:-2, :-2],
            data[:-2, 1:-1],
            data[:-2, 2:],
            data[1:-1, :-2],
            data[1:-1, 2:],
            data[2:, :-2],
            data[2:, 1:-1],
            data[2:, 2:],
        ],
        axis=2,
    ).sum(axis=2)


def day11_part1(data: np.ndarray) -> int:
    while True:
        neighbors = neighborhood(data)
        new_data = np.where(
            (data == OCCUPIED) & (neighbors >= 4),
            SEAT,
            np.where((data == SEAT) & (neighbors == 0), OCCUPIED, data),
        )

        if np.all(new_data == data):
            return int(np.sum(new_data == OCCUPIED))
        else:
            data = new_data


def test_day11_part1():
    assert day11_part1(parse(TEST_DATA)) == 37


def to_string(data: np.ndarray) -> str:
    return "\n".join(
        "".join("#" if c == OCCUPIED else ("L" if c == SEAT else ".") for c in data_line)
        for data_line in data
    )


@njit
def first_occupied(line: np.ndarray) -> int:
    (idx,) = np.where(line != EMPTY)
    if len(idx) == 0:
        return 0
    else:
        return 1 if line[idx[0]] == OCCUPIED else 0


@njit
def neighborhood_part2(data: np.ndarray) -> np.ndarray:
    padded_data = np.zeros(shape=(data.shape[0] + 2, data.shape[1] + 2))
    padded_data[1:-1, 1:-1] = data
    out = np.empty(shape=data.shape)
    for i in range(1, padded_data.shape[0] - 1):
        for j in range(1, padded_data.shape[1] - 1):
            out[i - 1, j - 1] = (
                first_occupied(padded_data[i + 1 :, j])
                + first_occupied(padded_data[i, j + 1 :])
                + first_occupied(padded_data[i - 1 :: -1, j])
                + first_occupied(padded_data[i, j - 1 :: -1])
                + first_occupied(np.diag(padded_data[i + 1 :, j + 1 :]))
                + first_occupied(np.diag(padded_data[i - 1 :: -1, j - 1 :: -1]))
                + first_occupied(np.diag(padded_data[i - 1 :: -1, j + 1 :]))
                + first_occupied(np.diag(padded_data[i + 1 :, j - 1 :: -1]))
            )
    return out


@njit
def day11_part2(data: np.ndarray) -> int:
    while True:
        neighbors = neighborhood_part2(data)
        new_data = np.where(
            (data == OCCUPIED) & (neighbors >= 5),
            SEAT,
            np.where((data == SEAT) & (neighbors == 0), OCCUPIED, data),
        )

        if np.all(new_data == data):
            return int(np.sum(new_data == OCCUPIED))
        else:
            data = new_data


def test_day11_part2():
    assert day11_part2(parse(TEST_DATA)) == 26


def main():
    data = parse(aocd.get_data(day=11, year=2020))
    print(f"day 11 part 1: {day11_part1(data)}")
    print(f"day 11 part 2: {day11_part2(data)}")


if __name__ == "__main__":
    main()
