import re
from io import StringIO
from typing import Dict, List, Tuple

import aocd
import numpy as np

TEST_DATA = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""


def parse(data: str) -> Tuple[Dict[str, List[Tuple[int, int]]], np.ndarray, np.ndarray]:
    sec1, sec2, sec3 = data.split("\n\n")

    rules = {}
    for rule in sec1.split("\n"):
        res = re.match(r"([\w ]+): (\d+)-(\d+) or (\d+)-(\d+)", rule)
        rules[res.group(1)] = [
            (int(res.group(2)), int(res.group(3))),
            (int(res.group(4)), int(res.group(5))),
        ]

    my_ticket = np.fromstring(sec2.split("\n")[1], sep=",")
    other_tickets = np.genfromtxt(StringIO("\n".join(sec3.split("\n")[1:])), delimiter=",")

    return rules, my_ticket, other_tickets


def test_parse():
    parse(TEST_DATA)


def day16_part1(data: str) -> int:
    rules, my_ticket, other_tickets = parse(data)

    invalid = np.ones(shape=other_tickets.shape, dtype=bool)
    for (lo1, hi1), (lo2, hi2) in rules.values():
        invalid = invalid & ~(
            ((lo1 <= other_tickets) & (other_tickets <= hi1))
            | ((lo2 <= other_tickets) & (other_tickets <= hi2))
        )

    return other_tickets[invalid].sum()


def test_day16_part1():
    assert day16_part1(TEST_DATA) == 71


def day16_part2(data: str) -> int:
    rules, my_ticket, other_tickets = parse(data)

    invalid = np.ones(shape=other_tickets.shape, dtype=bool)
    for (lo1, hi1), (lo2, hi2) in rules.values():
        invalid = invalid & ~(
            ((lo1 <= other_tickets) & (other_tickets <= hi1))
            | ((lo2 <= other_tickets) & (other_tickets <= hi2))
        )

    other_tickets = other_tickets[~np.any(invalid, axis=1), :]

    compat_rule = []
    for field in range(other_tickets.shape[1]):
        compat_keys = set()
        for (key, ((lo1, hi1), (lo2, hi2))) in rules.items():
            d = other_tickets[:, field]
            if np.all(((lo1 <= d) & (d <= hi1)) | ((lo2 <= d) & (d <= hi2))):
                compat_keys.add(key)
        compat_rule.append(compat_keys)

    # match field name to idx
    matched_field = {}
    while len(matched_field) < len(rules):
        # find field with single rule
        match_idx = -1
        match_field = ""
        for i, cr in enumerate(compat_rule):
            if len(cr) == 1:
                match_idx = i
                match_field = list(cr)[0]
                break

        print(f"field {match_field} matched to index {match_idx}")

        if match_idx == -1:
            raise RuntimeError("didnt find a one-match field")

        for cr in compat_rule:
            cr.discard(match_field)
        matched_field[match_field] = match_idx

    # compute sum
    total = 1
    for name, idx in matched_field.items():
        if name.startswith("departure"):
            total *= my_ticket[idx]

    return total


def main():
    print(f"day 16 part 1: {day16_part1(aocd.get_data(day=16, year=2020))}")
    print(f"day 16 part 2: {day16_part2(aocd.get_data(day=16, year=2020))}")


if __name__ == "__main__":
    main()
