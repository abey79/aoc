import re
from dataclasses import dataclass
from typing import Dict

import aocd

TEST_DATA = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

TEST_DATA2 = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""


@dataclass
class Bag:
    color: str
    contents: Dict[str, int]

    @staticmethod
    def from_string(rule: str) -> "Bag":
        part1, part2 = rule.rstrip(".").split(" bags contain ")

        out = {}
        for bag in part2.split(", "):
            res = re.match(r"^(\d+) (\w+ \w+) bags?$", bag)
            if res:
                out[res.group(2)] = int(res.group(1))

        return Bag(color=part1, contents=out)

    def contains(self, target: str, bags: Dict[str, "Bag"]) -> bool:
        """Check the existence of a given color in this bag according to the provided rules."""
        for color in self.contents:
            if color == target or bags[color].contains(target, bags):
                return True
        return False

    def count_content(self, bags: Dict[str, "Bag"]) -> int:
        total = 0
        for color, cnt in self.contents.items():
            total += cnt
            total += cnt * bags[color].count_content(bags)
        return total


def test_bag_from_string():
    assert Bag.from_string(
        "light red bags contain 1 bright white bag, 2 muted yellow bags."
    ) == Bag(
        "light red",
        {"bright white": 1, "muted yellow": 2},
    )

    assert Bag.from_string("bright white bags contain 1 shiny gold bag.") == Bag(
        "bright white",
        {"shiny gold": 1},
    )

    assert Bag.from_string("faded blue bags contain no other bags.") == Bag("faded blue", {})


def parse_all(data: str) -> Dict[str, Bag]:
    return {
        bag.color: bag for bag in (Bag.from_string(bag_str) for bag_str in data.split("\n"))
    }


def day7_part1(data: str) -> int:
    # parse all rules
    bags = parse_all(data)
    return sum(bag.contains("shiny gold", bags) for bag in bags.values())


def test_day7_part1():
    assert day7_part1(TEST_DATA) == 4


def day7_part2(data: str) -> int:
    bags = parse_all(data)
    return bags["shiny gold"].count_content(bags)


def test_day7_part2():
    assert day7_part2(TEST_DATA) == 32
    assert day7_part2(TEST_DATA2) == 126


def main():
    print(f"Day 7 part 1: {day7_part1(aocd.get_data(day=7, year=2020))}")
    print(f"Day 7 part 2: {day7_part2(aocd.get_data(day=7, year=2020))}")


if __name__ == "__main__":
    main()
