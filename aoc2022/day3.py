import aocd

TEST_DATA = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""
TEST_PART1_RESULT = 157
TEST_PART2_RESULT = 70


def part1(data: str):
    sum = 0
    for line in data.splitlines():

        l = line[: len(line) >> 1]
        r = line[len(line) >> 1 :]
        (item,) = set(l) & set(r)

        sum += ord(item.lower()) - ord("a") + (27 if item == item.upper() else 1)

    return sum


def part2(data: str):
    sum = 0
    lines = data.splitlines()
    while lines:
        l1, l2, l3 = lines.pop(0), lines.pop(0), lines.pop(0)
        (item,) = set(l1) & set(l2) & set(l3)
        sum += ord(item.lower()) - ord("a") + (27 if item == item.upper() else 1)

    return sum


def test_part1():
    if TEST_PART1_RESULT is not None:
        assert part1(TEST_DATA) == TEST_PART1_RESULT


def test_part2():
    if TEST_PART2_RESULT is not None:
        assert part2(TEST_DATA) == TEST_PART2_RESULT


def main() -> None:
    data = aocd.get_data(day=3, year=2022)
    print("Running for day 3 of year 2022")
    print("Part 1 solution:", part1(data))
    print("Part 2 solution:", part2(data))


if __name__ == "__main__":
    main()
