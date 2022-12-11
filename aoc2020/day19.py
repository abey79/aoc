from dataclasses import dataclass
from typing import Dict, List, Tuple

import aocd
import pytest

TEST_DATA = """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb"""


TEST_DATA2 = """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""

TEST_DATA2_OK = """bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba""".splitlines()


class Matcher:
    def match(self, s: str) -> Tuple[bool, str]:
        raise NotImplementedError()


@dataclass
class LiteralMatcher(Matcher):
    literal: str

    def match(self, s: str) -> Tuple[bool, str]:
        if s.startswith(self.literal):
            return True, s[1:]
        else:
            return False, s


@dataclass
class CompositionMatcher(Matcher):
    matchers: List[Matcher]

    def match(self, s: str) -> Tuple[bool, str]:
        orig = s
        for matcher in self.matchers:
            res, s = matcher.match(s)
            if not res:
                return False, orig
        return True, s


@dataclass
class OptionMatcher(Matcher):
    matchers: List[Matcher]

    def match(self, s: str) -> Tuple[bool, str]:

        orig = s
        for matcher in self.matchers:
            res, s = matcher.match(s)
            if res:
                return res, s
        return False, orig


def parse(data: str) -> Tuple[List[str], Dict[int, str]]:
    part1, part2 = data.split("\n\n")

    rules = {}
    for line in part1.splitlines():
        a, b = line.split(": ")
        rules[int(a)] = b

    messages = list(part2.splitlines())

    return messages, rules


def build_matcher(rule: str, rules: Dict[int, str]) -> Matcher:
    if rule.startswith('"') and rule.endswith('"'):
        return LiteralMatcher(rule.strip('"'))
    elif "|" in rule:
        return OptionMatcher(
            [build_matcher(sub_rule.strip(), rules) for sub_rule in rule.split("|")]
        )
    else:
        return CompositionMatcher(
            [build_matcher(rules[int(idx)], rules) for idx in rule.split()]
        )


def day19_part1(data: str) -> int:
    messages, rules = parse(data)
    matcher = build_matcher(rules[0], rules)

    return sum(matcher.match(msg) == (True, "") for msg in messages)


def day19_part2(data: str) -> int:
    messages, rules = parse(data)
    matcher_42 = build_matcher(rules[42], rules)
    matcher_31 = build_matcher(rules[31], rules)

    matches = []
    for msg in messages:
        res = True
        cnt_a = 0
        while res:
            res, msg = matcher_42.match(msg)
            if res:
                cnt_a += 1
        res = True
        cnt_b = 0
        while res:
            res, msg = matcher_31.match(msg)
            if res:
                cnt_b += 1

        matches.append(msg == "" and cnt_a > cnt_b > 0)

    return sum(matches)


def test_with_test_data2():
    assert day19_part1(TEST_DATA2) == 3
    assert day19_part2(TEST_DATA2) == 12


def test_day19_part1():
    assert day19_part1(TEST_DATA) == 2


def main():
    print(f"day 19 part 1: {day19_part1(aocd.get_data(day=19, year=2020))}")
    print(f"day 19 part 2: {day19_part2(aocd.get_data(day=19, year=2020))}")


if __name__ == "__main__":
    main()


##################
# inline version #
##################
# 2.5x slower


def match_rule(s: str, rule: str, rules: Dict[int, str]) -> Tuple[bool, str]:
    orig = s
    if rule.startswith('"') and rule.endswith('"'):
        pattern = rule.strip('"')
        if s.startswith(pattern):
            return True, s[len(pattern) :]
        else:
            return False, s
    elif "|" in rule:
        for sub_rule in rule.split("|"):
            res, s = match_rule(orig, sub_rule, rules)
            if res:
                return res, s
        return False, s
    else:
        for rule_idx in rule.split():
            res, s = match_rule(s, rules[int(rule_idx)], rules)
            if not res:
                return False, orig
        return True, s


def day19_part1_v2(data: str) -> int:
    messages, rules = parse(data)
    return sum(match_rule(msg, rules[0], rules) == (True, "") for msg in messages)


def test_day18_part1_v2():
    assert day19_part1_v2(TEST_DATA) == 2
    assert day19_part1_v2(aocd.get_data(day=19, year=2020)) == 192


def day19_part2_v2(data: str) -> int:
    messages, rules = parse(data)

    matches = []
    for msg in messages:
        res = True
        cnt_a = 0
        while res:
            res, msg = match_rule(msg, rules[42], rules)
            if res:
                cnt_a += 1
        res = True
        cnt_b = 0
        while res:
            res, msg = match_rule(msg, rules[31], rules)
            if res:
                cnt_b += 1

        matches.append(msg == "" and cnt_a > cnt_b > 0)

    return sum(matches)


@pytest.mark.benchmark(group="day19_part1")
@pytest.mark.parametrize("func", [day19_part1, day19_part1_v2])
def test_benchmarks(benchmark, func):
    data = aocd.get_data(day=19, year=2020)
    res = benchmark(func, data)
    assert res == 192


@pytest.mark.benchmark(group="day19_part2")
@pytest.mark.parametrize("func", [day19_part2, day19_part2_v2])
def test_benchmarks_part2(benchmark, func):
    data = aocd.get_data(day=19, year=2020)
    res = benchmark(func, data)
    assert res == 296
