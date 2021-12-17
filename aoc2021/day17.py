import itertools
import math
import sys
from pathlib import Path
from typing import Callable

import aocd
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
# noinspection SpellCheckingInspection
TEST_DATA: str = """target area: x=20..30, y=-10..-5"""
TEST_RESULT_PART1: int | None = 45
TEST_RESULT_PART2: int | None = 112


def extract_area(data: str) -> (int, int, int, int):
    _, _, xr, yr = data.split(" ")
    xmin, xmax = xr.strip("x=,").split("..")
    ymin, ymax = yr.strip("y=").split("..")
    return tuple(int(v) for v in (xmin, xmax, ymin, ymax))


def valid(vx: int, vy: int, target: (int, int, int, int)) -> bool:
    minx, maxx, miny, maxy = target
    px = py = 0
    while True:
        px += vx
        py += vy

        if (minx <= px <= maxx) and (miny <= py <= maxy):
            return True
        elif px > maxx or py < miny:
            return False

        vy -= 1
        vx = max(0, vx - 1)


def part1(data: str) -> int:
    _, _, ymin, _ = extract_area(data)
    return sum(range(-ymin))


def part2(data: str) -> int:
    xmin, xmax, ymin, ymax = extract_area(data)

    return sum(
        1
        for vx, vy in itertools.product(range(xmax + 1), range(ymin, -ymin + 1))
        if valid(vx, vy, (xmin, xmax, ymin, ymax))
    )


####################################################
# Shameless, non-working, "smart", initial attempt #
####################################################

TEST_PART2_DATA = {
    (23, -10),
    (25, -9),
    (27, -5),
    (29, -6),
    (22, -6),
    (21, -7),
    (9, 0),
    (27, -7),
    (24, -5),
    (25, -7),
    (26, -6),
    (25, -5),
    (6, 8),
    (11, -2),
    (20, -5),
    (29, -10),
    (6, 3),
    (28, -7),
    (8, 0),
    (30, -6),
    (29, -8),
    (20, -10),
    (6, 7),
    (6, 4),
    (6, 1),
    (14, -4),
    (21, -6),
    (26, -10),
    (7, -1),
    (7, 7),
    (8, -1),
    (21, -9),
    (6, 2),
    (20, -7),
    (30, -10),
    (14, -3),
    (20, -8),
    (13, -2),
    (7, 3),
    (28, -8),
    (29, -9),
    (15, -3),
    (22, -5),
    (26, -8),
    (25, -8),
    (25, -6),
    (15, -4),
    (9, -2),
    (15, -2),
    (12, -2),
    (28, -9),
    (12, -3),
    (24, -6),
    (23, -7),
    (25, -10),
    (7, 8),
    (11, -3),
    (26, -7),
    (7, 1),
    (23, -9),
    (6, 0),
    (22, -10),
    (27, -6),
    (8, 1),
    (22, -8),
    (13, -4),
    (7, 6),
    (28, -6),
    (11, -4),
    (12, -4),
    (26, -9),
    (7, 4),
    (24, -10),
    (23, -8),
    (30, -8),
    (7, 0),
    (9, -1),
    (10, -1),
    (26, -5),
    (22, -9),
    (6, 5),
    (7, 5),
    (23, -6),
    (28, -10),
    (10, -2),
    (11, -1),
    (20, -9),
    (14, -2),
    (29, -7),
    (13, -3),
    (23, -5),
    (24, -8),
    (27, -9),
    (30, -7),
    (28, -5),
    (21, -10),
    (7, 9),
    (6, 6),
    (21, -5),
    (27, -10),
    (7, 2),
    (30, -9),
    (21, -8),
    (22, -7),
    (24, -9),
    (20, -6),
    (6, 9),
    (29, -5),
    (8, -2),
    (27, -8),
    (30, -5),
    (24, -7),
}


def steps_for_speed(v: int, target: int) -> float:
    # https://www.wolframalpha.com/input/?i=solve+n%2F2*%28v+-+n+%2B+1+%2B+v%29+%3D+t+for+n
    return abs((math.sqrt((2 * v + 1) ** 2 - 8 * target) + 2 * v + 1) / 2)


def speed_for_step(n: int, target: int) -> float:
    # https://www.wolframalpha.com/input/?i=solve+n%2F2*%28max%280%2C+v+-+n+%2B+1%29+%2B+v%29+%3D+t+for+v
    assert n > 0
    if target < 0.5 * (n - 1) * n:
        return 2 * target / n
    else:
        return 0.5 * (2 * target / n + n - 1)


def part2_old(data: str) -> int:
    xmin, xmax, ymin, ymax = extract_area(data)

    # find all possible vy with assorted step count
    possible_vy = set()
    for vy in range(-ymax - 1, -ymin):
        possible_vy.add((vy, 2 * vy + 2))
    for vy in range(ymin, ymax + 1):
        possible_vy.add((vy, 1))
    for vy in range(ymax + 1, 1):
        nmin = math.ceil(steps_for_speed(vy, ymax))
        nmax = math.floor(steps_for_speed(vy, ymin))
        for n in range(nmin, nmax + 1):
            possible_vy.add((vy, n))
    for vy in range(1, -ymax - 1):
        nmin = math.ceil(steps_for_speed(-vy - 1, ymax))
        nmax = math.floor(steps_for_speed(-vy - 1, ymin))
        for n in range(nmin, nmax + 1):
            possible_vy.add((vy, n + 2 * vy + 1))

    # check that this list is correct!
    for vy, n in possible_vy:
        pos = 0
        vy_this_step = vy
        for _ in range(n):
            pos += vy
            vy -= 1
        if not (ymin <= pos <= ymax):
            print(f"WRONG: vy={vy_this_step}, n={n}")

    possible_speeds = set()
    for vy, n in possible_vy:
        vxmin = math.ceil(speed_for_step(n, xmin))
        vxmax = math.floor(speed_for_step(n, xmax))
        for vx in range(vxmin, vxmax + 1):
            possible_speeds.add((vx, vy))

    print("missing:", TEST_PART2_DATA - possible_speeds)
    print("extra", possible_speeds - TEST_PART2_DATA)

    return len(possible_speeds)


##########################################################


def run_test_part1(*args, **kwargs):
    if TEST_RESULT_PART1 is None:
        raise NotImplementedError
    # noinspection PyArgumentList
    assert part1(TEST_DATA, *args, **kwargs) == TEST_RESULT_PART1


def run_test_part2(*args, **kwargs):
    if TEST_RESULT_PART2 is None:
        raise NotImplementedError
    # noinspection PyArgumentList
    assert part2(TEST_DATA, *args, **kwargs) == TEST_RESULT_PART2


def run_solution(name: str, test_func: Callable, solution: Callable, *args, **kwargs):
    proceed = True
    try:
        test_func(*args, **kwargs)
        console.print(f"Test {name} succeeded.", style="green")
    except NotImplementedError:
        console.print(f"Test {name} not implemented", style="yellow")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]
    except AssertionError:
        console.print(f"Test {name} failed", style="red")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]

    if not proceed:
        sys.exit()

    result = solution(aocd.get_data(day=DAY, year=2021), *args, **kwargs)
    console.print(f"{name.capitalize()} solution: {result}", style="blue")


def main() -> None:
    console.print(f"Running for day {DAY}", style="blue")
    run_solution("part 1", run_test_part1, part1)
    run_solution("part 2", run_test_part2, part2)


if __name__ == "__main__":
    main()
