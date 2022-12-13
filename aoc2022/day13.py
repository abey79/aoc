import functools

import aocd

TEST_DATA = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""
TEST_PART1_RESULT = 13
TEST_PART2_RESULT = 140


def is_ordered(l, r) -> bool | None:
    if isinstance(l, list) and isinstance(r, list):
        for l1, r1 in zip(l, r):
            res = is_ordered(l1, r1)
            if res is not None:
                return res
        if len(l) < len(r):
            return True
        elif len(l) > len(r):
            return False
        else:
            return None
    elif isinstance(l, list):
        return is_ordered(l, [r])
    elif isinstance(r, list):
        return is_ordered([l], r)
    elif l < r:
        return True
    elif l > r:
        return False
    else:
        return None


def part1(data: str):
    cnt = 0
    for i, pair in enumerate(data.split("\n\n")):
        l, r = pair.splitlines()

        if is_ordered(eval(l), eval(r)):
            cnt += i + 1
    return cnt


def part2(data: str):
    data = data.replace("\n\n", "\n")
    packets = [eval(x) for x in data.splitlines()] + [[[2]], [[6]]]

    def cmp(a, b):
        res = is_ordered(a, b)
        if res:
            return -1
        elif res is False:
            return 1
        else:
            return 0

    sorted_packets = sorted(packets, key=functools.cmp_to_key(cmp))

    idx1 = sorted_packets.index([[2]])
    idx2 = sorted_packets.index([[6]])
    return (idx1 + 1) * (idx2 + 1)


def test_part1():
    if TEST_PART1_RESULT is not None:
        assert part1(TEST_DATA) == TEST_PART1_RESULT


def test_part2():
    if TEST_PART2_RESULT is not None:
        assert part2(TEST_DATA) == TEST_PART2_RESULT


def main() -> None:
    data = aocd.get_data(day=13, year=2022)
    print("Running for day 13 of year 2022")
    print("Part 1 solution:", part1(data))
    print("Part 2 solution:", part2(data))


if __name__ == "__main__":
    main()
