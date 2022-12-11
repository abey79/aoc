import math
from fractions import Fraction
from typing import Optional

import aocd
import numpy as np

TEST_DATA = """939
7,13,x,x,59,x,31,19"""


def day13_part1(data: str) -> int:
    departure, bus_list = data.split("\n")
    departure = int(departure)
    bus_ids = [int(bus) for bus in bus_list.split(",") if bus != "x"]

    time, bus_id = min(
        ((math.ceil(departure / bus_id) * bus_id, bus_id) for bus_id in bus_ids),
        key=lambda x: x[0],
    )
    return bus_id * (time - departure)


def test_day13_part1():
    assert day13_part1(TEST_DATA) == 295


def day13_part2(data: str, max_n: Optional[int] = None) -> int:
    data = [(int(x), i) for i, x in enumerate(data.split(",")) if x != "x"]

    first_id = data[0][0]

    if max_n is None:
        max_n = 100000
    set_list = []
    for bus_id, offset in data[1:]:
        s = set()
        for i in range(max_n):
            f = Fraction(bus_id * i - offset, first_id)
            if f.denominator == 1:
                s.add(f)
        set_list.append(s)

    itrsct = set.intersection(*set_list)
    if len(itrsct) == 0:
        raise RuntimeError("increase MAX_N")
    else:
        return min(itrsct) * first_id


def day13_part2_v2(data: str, max_n: Optional[int] = None) -> int:
    data = [(int(x), i) for i, x in enumerate(data.split(",")) if x != "x"]

    first_id = data[0][0]

    if max_n is None:
        max_n = 1000

    set_start = []
    for bus_id, offset in data[1:]:
        i = 0
        while True:
            f = Fraction(bus_id * i - offset, first_id)
            if f.denominator == 1:
                break
            else:
                i += 1
        set_start.append(int(f))

    set_list = []
    for i, (bus_id, _) in enumerate(data[1:]):
        max_k = math.floor(max_n / bus_id)
        set_list.append(set(np.arange(set_start[i], max_k, bus_id)))

    itrsct = set.intersection(*set_list)
    if len(itrsct) == 0:
        raise RuntimeError("increase MAX_N")
    else:
        return min(itrsct) * first_id


# noinspection DuplicatedCode
def day13_part2_v3(data: str, max_n: Optional[int] = None) -> int:
    data = [(int(x), i) for i, x in enumerate(data.split(",")) if x != "x"]

    first_id = data[0][0]

    if max_n is None:
        max_n = 1000

    set_start = []
    for bus_id, offset in data[1:]:
        i = 0
        while True:
            f = Fraction(bus_id * i - offset, first_id)
            if f.denominator == 1:
                break
            else:
                i += 1
        set_start.append(int(f))

    # this is the sparsest set that goes to our set max
    max_idx, (max_bus_id, max_offset) = max(enumerate(data[1:]), key=lambda x: x[1][0])
    max_k = math.floor(max_n / max_bus_id)
    base_set = np.arange(set_start[max_idx], max_k, max_bus_id)

    for i, (bus_id, _) in enumerate(data[1:]):
        if bus_id == max_bus_id:
            continue

        frac, _ = np.modf((base_set - set_start[i]) / bus_id)
        base_set = base_set[frac == 0]

    if len(base_set) == 0:
        raise RuntimeError("increase MAX_N")
    else:
        return base_set[0] * first_id


# noinspection DuplicatedCode
def day13_part2_v4(data: str, max_n: Optional[int] = None) -> int:
    data = [(int(x), i) for i, x in enumerate(data.split(",")) if x != "x"]

    first_id = data[0][0]

    if max_n is None:
        max_n = 1000

    new_data = []
    for bus_id, offset in data[1:]:
        i = 0
        while True:
            f = Fraction(bus_id * i - offset, first_id)
            if f.denominator == 1:
                break
            else:
                i += 1
        new_data.append((bus_id, offset, int(f)))

    # sort be decreasing bus_id to limit the size of the set
    new_data = sorted(new_data, reverse=True, key=lambda x: x[0])

    base_set = None
    for bus_id, offset, set_start in new_data:
        print(f"{bus_id} {offset} {set_start}")
        if base_set is None:
            max_k = math.floor(max_n / bus_id)
            base_set = np.arange(set_start, max_k, bus_id)
        else:
            frac, _ = np.modf((base_set - set_start) / bus_id)
            base_set = base_set[frac == 0]

        print(f"len base set {len(base_set)}")

    if len(base_set) == 0:
        raise RuntimeError("increase MAX_N")
    else:
        return base_set[0] * first_id


def day13_part2_v5(data: str) -> int:
    from sympy.ntheory.modular import crt

    data = [(int(x), i) for i, x in enumerate(data.split(",")) if x != "x"]
    return crt([a[0] for a in data], [-a[1] for a in data])[0]


def test_day13_part2():
    assert day13_part2_v4("17,x,13,19", 10000) == 3417
    assert day13_part2_v4("67,7,59,61", 1000000) == 754018
    assert day13_part2_v4("67,x,7,59,61", 1000000) == 779210
    assert day13_part2_v4("67,7,x,59,61", 10000000) == 1261476
    assert day13_part2_v4("1789,37,47,1889", 10000000000) == 1202161486


def main():
    data = aocd.get_data(day=13, year=2020)
    print(f"day 13 part 1: {day13_part1(data)}")

    _, data_part2 = data.split("\n")
    print(f"day 13 part 2: {day13_part2_v5(data_part2)}")


if __name__ == "__main__":
    main()


def extended_gcd(a, b):
    """Extended Greatest Common Divisor Algorithm

    Returns:
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def extended_gcd_data(bus_a, bus_b, offset_a, offset_b):
    r, s, t = extended_gcd(bus_a, bus_b)

    return s * (offset_a - offset_b), t * (offset_b - offset_a)
