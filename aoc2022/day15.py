import re
from collections import defaultdict
from typing import Iterable

import aocd
import tqdm

TEST_DATA = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""
TEST_PART1_RESULT = 26
TEST_PART2_RESULT = 56000011


EXPR = re.compile(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)")


def load(data: str) -> Iterable[tuple[int, int, int, int]]:
    for mo in EXPR.finditer(data):
        yield tuple(map(int, mo.groups()))


def part1(data: str, row: int):
    ranges = []
    beacons = set()
    sensors = set()
    for x, y, i, j in load(data):
        dist = abs(x - i) + abs(y - j)
        dist_to_row = abs(y - row)
        if dist_to_row <= dist:
            delta = dist - dist_to_row
            ranges.append(range(x - delta, x + delta + 1))
        if j == row:
            beacons.add(i)
        if y == row:
            sensors.add(x)

    occupancy = set.union(*(set(rng) for rng in ranges)) - beacons - sensors
    return len(occupancy)


def merge_ranges(ranges: Iterable[range]) -> Iterable[range]:
    # thank you copilot
    ranges = sorted(ranges, key=lambda rng: rng.start)
    merged = []
    for rng in ranges:
        if merged and merged[-1].stop >= rng.start:
            merged[-1] = range(merged[-1].start, max(merged[-1].stop, rng.stop))
        else:
            merged.append(rng)
    return merged


def crop_ranges(ranges: Iterable[range], min_val: int, max_val: int) -> Iterable[range]:
    # thank you copilot
    for rng in ranges:
        if rng.stop <= min_val:
            continue
        if rng.start >= max_val:
            continue
        yield range(max(rng.start, min_val), min(rng.stop, max_val))


def test_merge_ranges():
    res = merge_ranges(
        [range(2, 3), range(11, 14), range(3, 14), range(-3, 4), range(15, 26), range(15, 18)]
    )
    assert res == [range(-3, 14), range(15, 26)]


def test_crop_ranges():
    res = crop_ranges([range(-3, 14), range(15, 26)], 0, 20)
    assert list(res) == [range(0, 14), range(15, 20)]

    res = crop_ranges(
        merge_ranges(
            [
                range(2, 3),
                range(11, 14),
                range(3, 14),
                range(-3, 4),
                range(15, 26),
                range(15, 18),
            ]
        ),
        0,
        20,
    )
    assert list(res) == [range(0, 14), range(15, 20)]


def part2(data: str, coord_range: int):
    ranges = defaultdict(list)
    beacons = defaultdict(list)
    sensors = defaultdict(list)
    for x, y, i, j in tqdm.tqdm(list(load(data))):
        dist = abs(x - i) + abs(y - j)
        for delta in range(-dist, dist + 1):
            dx = dist - abs(delta)
            ranges[y + delta].append(range(x - dx, x + dx + 1))
        beacons[j].append(i)
        sensors[y].append(x)

    for y in tqdm.tqdm(range(coord_range + 1)):
        occupancy = list(
            crop_ranges(
                merge_ranges(
                    ranges[y]
                    + [range(i, i + 1) for i in beacons[y]]
                    + [range(i, i + 1) for i in sensors[y]]
                ),
                0,
                coord_range,
            )
        )
        if len(occupancy) == 2:
            return occupancy[0].stop * 4000000 + y


def test_part1():
    if TEST_PART1_RESULT is not None:
        assert part1(TEST_DATA, 10) == TEST_PART1_RESULT


def test_part2():
    if TEST_PART2_RESULT is not None:
        assert part2(TEST_DATA, 20) == TEST_PART2_RESULT


def main() -> None:
    data = aocd.get_data(day=15, year=2022)
    print("Running for day 15 of year 2022")
    print("Part 1 solution:", part1(data, 2000000))
    print("Part 2 solution:", part2(data, 4000000))


if __name__ == "__main__":
    main()
