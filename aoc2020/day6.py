import aocd

TEST_DATA = """abc

a
b
c

ab
ac

a
a
a
a

b"""


def day6_part1(data: str) -> int:
    return sum(len(set(group.replace("\n", ""))) for group in data.split("\n\n"))


def test_day6_part1():
    assert day6_part1(TEST_DATA) == 11


def day6_part2(data: str) -> int:
    def count_group_answers(group):
        answers = group.split("\n")
        qs = set(answers[0])
        for answer in answers[1:]:
            qs = qs.intersection(set(answer))
        return len(qs)

    return sum(count_group_answers(group) for group in data.split("\n\n"))


def day6_part2_v2(data: str) -> int:
    return sum(
        len(set.intersection(*[set(answer) for answer in group.split("\n")]))
        for group in data.split("\n\n")
    )


def test_day6_part2():
    assert day6_part2(TEST_DATA) == 6
    assert day6_part2_v2(TEST_DATA) == 6


def main():
    print("day 6 part 1: " + str(day6_part1(aocd.get_data(day=6, year=2020))))
    print("day 6 part 2: " + str(day6_part2(aocd.get_data(day=6, year=2020))))


if __name__ == "__main__":
    main()
