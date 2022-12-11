import aocd

TEST_DATA = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""
TEST_PART1_RESULT = 2
TEST_PART2_RESULT = 4


def part1(data: str):
    cnt = 0
    for line in data.splitlines():
        a, b = line.split(",")
        a1, a2 = a.split("-")
        b1, b2 = b.split("-")

        sa = set(range(int(a1), int(a2) + 1))
        sb = set(range(int(b1), int(b2) + 1))
        su = sa & sb

        if su == sa or su == sb:
            cnt += 1
    return cnt


def part2(data: str):
    cnt = 0
    for line in data.splitlines():
        a, b = line.split(",")
        a1, a2 = a.split("-")
        b1, b2 = b.split("-")

        sa = set(range(int(a1), int(a2) + 1))
        sb = set(range(int(b1), int(b2) + 1))

        if len(sa & sb) > 0:
            cnt += 1
    return cnt


def test_part1():
    if TEST_PART1_RESULT is not None:
        assert part1(TEST_DATA) == TEST_PART1_RESULT


def test_part2():
    if TEST_PART2_RESULT is not None:
        assert part2(TEST_DATA) == TEST_PART2_RESULT


def main() -> None:
    data = aocd.get_data(day=4, year=2022)
    print("Running for day 4 of year 2022")
    print("Part 1 solution:", part1(data))
    print("Part 2 solution:", part2(data))


if __name__ == "__main__":
    main()
