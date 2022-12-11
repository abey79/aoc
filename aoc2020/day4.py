import re
from typing import Dict, List

import aocd


def parse(data: str) -> List[Dict[str, str]]:
    def parse_from_passport(passport: str) -> Dict[str, str]:
        out = {}
        for item in passport.split():
            a, b = item.split(":")
            out[a] = b
        return out

    return [parse_from_passport(passport) for passport in data.split("\n\n")]


def test_parse():
    out = parse(
        """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""
    )

    assert len(out) == 4
    assert len(out[0]) == 8
    assert out[3]["eyr"] == "2025"


def day4_part1() -> int:
    data = parse(aocd.get_data(day=4, year=2020))
    req_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}

    count = 0
    for passport in data:
        if req_fields.issubset(passport):
            count += 1
    return count


def validate_passport(pp: Dict[str, str]) -> bool:
    try:

        def check_year(year, lo, hi):
            assert len(year) == 4
            assert lo <= int(year) <= hi

        check_year(pp["byr"], 1920, 2002)
        check_year(pp["iyr"], 2010, 2020)
        check_year(pp["eyr"], 2020, 2030)

        hgt = pp["hgt"]
        assert hgt[-2:] in ("cm", "in")

        if hgt[-2:] == "cm":
            assert 150 <= int(hgt[:-2]) <= 193
        elif hgt[-2:] == "in":
            assert 59 <= int(hgt[:-2]) <= 76

        assert re.match(r"^#[a-f0-9]{6}$", pp["hcl"]) is not None
        assert pp["ecl"] in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
        assert re.match(r"^\d{9}$", pp["pid"]) is not None
    # except (AssertionError, KeyError, ValueError, IndexError):
    except Exception:
        return False

    return True


def day4_part2_count_valid(data: str) -> int:
    count = 0
    for pp in parse(data):
        if validate_passport(pp):
            count += 1
    return count


def test_day4_part2_count_valid():
    assert (
        day4_part2_count_valid(
            """eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007"""
        )
        == 0
    )

    assert (
        day4_part2_count_valid(
            """pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""
        )
        == 4
    )


def main():
    print(f"day 4 part 1: {day4_part1()}")
    print(f"day 4 part 2: {day4_part2_count_valid(aocd.get_data(day=4, year=2020))}")


if __name__ == "__main__":
    main()
