import functools
from typing import Iterable

import aocd

TEST_DATA = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""
TEST_PART1_RESULT = 64
TEST_PART2_RESULT = 58


@functools.cache
def neighbors(cube: tuple[int, int, int]) -> set[tuple[int, int, int]]:
    deltas = ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1))
    return {(cube[0] + dx, cube[1] + dy, cube[2] + dz) for dx, dy, dz in deltas}


def outside_area(cubes: set[tuple[int, int, int]]) -> int:
    area = 0
    for cube in cubes:
        nb = neighbors(cube)
        area += 6 - len(nb & cubes)
    return area


def part1(data: str):
    cubes = {tuple(int(i) for i in s.split(",")) for s in data.splitlines()}
    return outside_area(cubes)


def bounds(
    cubes: Iterable[tuple[int, int, int]]
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
    x, y, z = zip(*cubes)
    return (min(x) - 1, max(x) + 1), (min(y) - 1, max(y) + 1), (min(z) - 1, max(z) + 1)


def part2(data: str):
    cubes = {tuple(int(i) for i in s.split(",")) for s in data.splitlines()}
    (x_min, x_max), (y_min, y_max), (z_min, z_max) = bounds(cubes)

    def inside_bounds(cube: tuple[int, int, int]) -> bool:
        return (
            (x_min <= cube[0] <= x_max)
            and (y_min <= cube[1] <= y_max)
            and (z_min <= cube[2] <= z_max)
        )

    shell_cubes = {(x_min, y_min, z_min)}

    while True:
        tmp_shell_cube = shell_cubes.copy()
        for cube in tmp_shell_cube:
            for nb in neighbors(cube):
                if nb not in cubes and nb not in shell_cubes and inside_bounds(nb):
                    shell_cubes.add(nb)
        if tmp_shell_cube == shell_cubes:
            break

    w, h, d = x_max - x_min + 1, y_max - y_min + 1, z_max - z_min + 1
    return outside_area(shell_cubes) - 2 * (w * h + w * d + h * d)


def test_part1():
    if TEST_PART1_RESULT is not None:
        assert part1(TEST_DATA) == TEST_PART1_RESULT


def test_part2():
    if TEST_PART2_RESULT is not None:
        assert part2(TEST_DATA) == TEST_PART2_RESULT


def main() -> None:
    data = aocd.get_data(day=18, year=2022)
    print("Running for day 18 of year 2022")
    print("Part 1 solution:", part1(data))
    print("Part 2 solution:", part2(data))


if __name__ == "__main__":
    main()
