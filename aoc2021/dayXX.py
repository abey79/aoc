import contextlib
import time
from pathlib import Path

import aocd
import pytest
from rich.console import Console

console = Console()

YEAR = 2021
DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
# noinspection SpellCheckingInspection
TEST_DATA: str = """"""
TEST_RESULT_PART1: int | None = None
TEST_RESULT_PART2: int | None = None
DATA = aocd.get_data(day=DAY, year=2021)


def part1(data: str) -> int:
    pass


def part2(data: str) -> int:
    pass


@pytest.mark.skipif(TEST_RESULT_PART1 is None, reason="part 1 test result not provided")
def test_part1():
    assert part1(TEST_DATA) == TEST_RESULT_PART1


@pytest.mark.skipif(TEST_RESULT_PART2 is None, reason="part 2 test result not provided")
def test_part2():
    assert part2(TEST_DATA) == TEST_RESULT_PART2


@contextlib.contextmanager
def measure_time():
    start = time.time()
    yield
    delta = time.time() - start
    console.print(
        f"Execution time: [bold cyan]{delta * 1000:.2f}ms[/]",
        style="blue",
        highlight=False,
    )


def main() -> None:
    console.rule(f"AOC {YEAR} day {DAY}", style="blue")
    console.print("Tests: ", end="", style="blue")
    pytest.main(["-q", __file__])
    with measure_time():
        res = part1(DATA)
        console.print(f"Part [bold cyan]1[/] solution: [bold green]{res}[/]", style="blue")
    with measure_time():
        res = part2(DATA)
        console.print(f"Part [bold cyan]2[/] solution: [bold green]{res}[/]", style="blue")


if __name__ == "__main__":
    main()
