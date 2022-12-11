import aocd

TEST_DATA = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

TEST_DATA2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
TEST_PART1_RESULT = 13
TEST_PART2_RESULT = 36


def part1(data: str):
    H = (0, 0)
    T = (0, 0)

    def step(dx, dy):
        nonlocal H, T
        H = (H[0] + dx, H[1] + dy)
        diff_x = H[0] - T[0]
        diff_y = H[1] - T[1]

        match diff_x, diff_y:
            case (0, 0):
                pass

            case (0, n) if abs(n) > 1:
                T = (T[0], T[1] + (1 if n > 0 else -1))

            case (n, 0) if abs(n) > 1:
                T = (T[0] + (1 if n > 0 else -1), T[1])

            case (n, m) if abs(n) > 1 or abs(m) > 1:
                T = (T[0] + (1 if n > 0 else -1), T[1] + (1 if m > 0 else -1))

            case _:
                pass

    positions = {T}
    for line in data.splitlines():
        cmd, step_count = line.split(" ")

        match cmd:
            case "U":
                delta = (0, 1)
            case "D":
                delta = (0, -1)
            case "L":
                delta = (-1, 0)
            case "R":
                delta = (1, 0)

        for i in range(int(step_count)):
            step(*delta)
            positions.add(T)

    return len(positions)


def part2(data: str):
    rope = [(0, 0)] * 10

    def step(dx, dy, H, T) -> tuple[int, int]:
        diff_x = H[0] - T[0]
        diff_y = H[1] - T[1]

        match diff_x, diff_y:
            case (0, 0):
                pass

            case (0, n) if abs(n) > 1:
                T = (T[0], T[1] + (1 if n > 0 else -1))

            case (n, 0) if abs(n) > 1:
                T = (T[0] + (1 if n > 0 else -1), T[1])

            case (n, m) if abs(n) > 1 or abs(m) > 1:
                T = (T[0] + (1 if n > 0 else -1), T[1] + (1 if m > 0 else -1))

            case _:
                pass

        return T

    positions = {rope[-1]}
    for line in data.splitlines():
        cmd, step_count = line.split(" ")

        match cmd:
            case "U":
                delta = (0, 1)
            case "D":
                delta = (0, -1)
            case "L":
                delta = (-1, 0)
            case "R":
                delta = (1, 0)
            case _:
                assert False

        for i in range(int(step_count)):
            rope[0] = rope[0][0] + delta[0], rope[0][1] + delta[1]
            for j in range(1, len(rope)):
                rope[j] = step(*delta, rope[j - 1], rope[j])
            positions.add(rope[-1])

    return len(positions)


def test_part1():
    if TEST_PART1_RESULT is not None:
        assert part1(TEST_DATA) == TEST_PART1_RESULT


def test_part2():
    if TEST_PART2_RESULT is not None:
        assert part2(TEST_DATA2) == TEST_PART2_RESULT


def main() -> None:
    data = aocd.get_data(day=9, year=2022)
    print("Running for day 9 of year 2022")
    print("Part 1 solution:", part1(data))
    print("Part 2 solution:", part2(data))


if __name__ == "__main__":
    main()
