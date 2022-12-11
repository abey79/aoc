import aocd
import numpy as np

TEST_DATA = """F10
N3
F7
R90
F11"""

R90 = np.array([[0, 1], [-1, 0]])
L90 = np.array([[0, -1], [1, 0]])


def test_rl90():
    heading = np.array([1, 0])

    assert np.all(R90 @ heading == np.array([0, -1]))
    assert np.all(L90 @ heading == np.array([0, 1]))

    heading = np.array([0, 1])
    assert np.all(R90 @ heading == np.array([1, 0]))
    assert np.all(L90 @ heading == np.array([-1, 0]))


# noinspection DuplicatedCode
def day12_part1(data: str) -> int:
    pos = np.array([0, 0])
    heading = np.array([1, 0])

    for instr in data.split("\n"):
        op = instr[0]
        param = int(instr[1:])

        if op == "N":
            pos[1] += param
        elif op == "S":
            pos[1] -= param
        elif op == "E":
            pos[0] += param
        elif op == "W":
            pos[0] -= param
        elif op == "F":
            pos += param * heading
        elif op in ["R", "L"] and param == 180:
            heading = -heading
        elif (op == "R" and param == 90) or (op == "L" and param == 270):
            heading = R90 @ heading
        elif (op == "L" and param == 90) or (op == "R" and param == 270):
            heading = L90 @ heading
        else:
            raise ValueError(f"unknown operand {op} (param: {param})")

    return abs(pos[0]) + abs(pos[1])


# noinspection DuplicatedCode
def day12_part2(data: str) -> int:
    pos = np.array([0, 0])
    wpt = np.array([10, 1])

    for instr in data.split("\n"):
        op = instr[0]
        param = int(instr[1:])

        if op == "N":
            wpt[1] += param
        elif op == "S":
            wpt[1] -= param
        elif op == "E":
            wpt[0] += param
        elif op == "W":
            wpt[0] -= param
        elif op == "F":
            pos += param * wpt
        elif op in ["R", "L"] and param == 180:
            wpt = -wpt
        elif (op == "R" and param == 90) or (op == "L" and param == 270):
            wpt = R90 @ wpt
        elif (op == "L" and param == 90) or (op == "R" and param == 270):
            wpt = L90 @ wpt
        else:
            raise ValueError(f"unknown operand {op} (param: {param})")

    return abs(pos[0]) + abs(pos[1])


def test_day12_part1():
    assert day12_part1(TEST_DATA) == 25


def test_day12_part2():
    assert day12_part2(TEST_DATA) == 286


def main():
    print(f"day 12 part 1: {day12_part1(aocd.get_data(day=12, year=2020))}")
    print(f"day 12 part 2: {day12_part2(aocd.get_data(day=12, year=2020))}")


if __name__ == "__main__":
    main()
