import aocd

TEST_DATA = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""
TEST_PART1_RESULT = 7
TEST_PART2_RESULT = 19


def part1(data: str):
    for i in range(4, len(data)):
        marker = data[i - 4 : i]
        if len(set(marker)) == 4:
            return i


def part2(data: str):
    for i in range(14, len(data)):
        marker = data[i - 14 : i]
        if len(set(marker)) == 14:
            return i


def test_part1():
    if TEST_PART1_RESULT is not None:
        assert part1(TEST_DATA) == TEST_PART1_RESULT


def test_part2():
    if TEST_PART2_RESULT is not None:
        assert part2(TEST_DATA) == TEST_PART2_RESULT


def main() -> None:
    data = aocd.get_data(day=6, year=2022)
    print("Running for day 6 of year 2022")
    print("Part 1 solution:", part1(data))
    print("Part 2 solution:", part2(data))


if __name__ == "__main__":
    main()
