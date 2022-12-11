import re
from collections import Counter
from typing import Tuple

import aocd


def parse(pwd: str) -> Tuple[int, int, str, str]:
    res = re.search(r"(\d+)-(\d+) (\w): (\w+)", pwd)
    return int(res.group(1)), int(res.group(2)), res.group(3), res.group(4)


def test_parse():
    assert parse("1-3 b: cdefg") == (1, 3, "b", "cdefg")


def check_password(pwd_string: str) -> bool:
    lo, hi, c, pwd = parse(pwd_string)
    return lo <= Counter(pwd)[c] <= hi


def test_check_password():
    assert check_password("1-3 a: abcde")
    assert not check_password("1-3 b: cdefg")
    assert check_password("2-9 c: ccccccccc")


def check_password_part2(pwd_string: str) -> bool:
    idx1, idx2, c, pwd = parse(pwd_string)
    return (pwd[idx1 - 1] == c) != (pwd[idx2 - 1] == c)


def test_check_password_part2():
    assert check_password_part2("1-3 a: abcde")
    assert not check_password_part2("1-3 b: cdefg")
    assert not check_password_part2("2-9 c: ccccccccc")


if __name__ == "__main__":
    res = sum(check_password(s) for s in aocd.get_data(day=2, year=2020).split("\n"))
    print("Day 1 part 1 solution: ", res)

    res = sum(check_password_part2(s) for s in aocd.get_data(day=2, year=2020).split("\n"))
    print("Day 1 part 2 solution: ", res)
