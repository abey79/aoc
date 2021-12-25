import time
from pathlib import Path

import aocd
import pytest
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
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


def main() -> None:
    console.rule(f"AOC {YEAR} day {DAY}", style="blue")
    console.print("Tests: ", end="", style="blue")
    pytest.main(["-q", __file__])
    start = time.time()
    res = part1(DATA)
    delta = time.time() - start
    console.print(
        f"Part [bold cyan]1[/] solution: [bold green]{res}[/] "
        f"(execution time: [bold cyan]{delta * 1000:.2f}ms[/])",
        style="blue",
        highlight=False,
    )
    start = time.time()
    res = part2(DATA)
    delta = time.time() - start
    console.print(
        f"Part [bold cyan]2[/] solution: [bold green]{res}[/] "
        f"(execution time: [bold cyan]{delta * 1000:.2f}ms[/])",
        style="blue",
        highlight=False,
    )


if __name__ == "__main__":
    main()
