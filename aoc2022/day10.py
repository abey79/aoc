import aocd

TEST_DATA = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""
TEST_PART1_RESULT = 13140
TEST_PART2_RESULT = """##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######....."""


def exec(data: str) -> list[int]:
    x = 1
    history = [x]

    for line in data.splitlines():
        args = line.split(" ")
        match args:
            case ["addx", val]:
                history.append(x)
                x += int(val)
                history.append(x)

            case ["noop"]:
                history.append(x)

            case _:
                assert False, f"Unknown command {' '.join(args)}"

    return history


def part1(data: str):
    history = exec(data)

    return sum(history[i] * (i + 1) for i in range(19, len(history), 40))


def part2(data: str):
    history = exec(data)

    res = [["." for _ in range(40)] for _ in range(6)]

    for i in range(240):
        col = i % 40
        row = i // 40
        x = history[i]

        if abs(history[i] - col) <= 1:
            res[row][col] = "#"

    return res


def test_part1():
    if TEST_PART1_RESULT is not None:
        assert part1(TEST_DATA) == TEST_PART1_RESULT


def test_part2():
    if TEST_PART2_RESULT is not None:
        assert part2(TEST_DATA) == TEST_PART2_RESULT


def main() -> None:
    data = aocd.get_data(day=10, year=2022)
    print("Running for day 10 of year 2022")
    print("Part 1 solution:", part1(data))

    res = part2(data)
    print("Part 2 solution:")
    for row in res:
        print("".join(row))


if __name__ == "__main__":
    main()
