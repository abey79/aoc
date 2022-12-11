import datetime
import os
import pathlib

import click

TEMPLATE = '''import aocd

TEST_DATA = """"""
TEST_PART1_RESULT = None
TEST_PART2_RESULT = None


def part1(data: str):
    pass


def part2(data: str):
    pass


def test_part1():
    if TEST_PART1_RESULT is not None:
        assert part1(TEST_DATA) == TEST_PART1_RESULT

    
def test_part2():
    if TEST_PART2_RESULT is not None:
        assert part2(TEST_DATA) == TEST_PART2_RESULT


def main() -> None:
    data = aocd.get_data(day={day}, year={year})
    print("Running for day {day} of year {year}")
    print("Part 1 solution:", part1(data))
    print("Part 2 solution:", part2(data))


if __name__ == "__main__":
    main()
'''


@click.command()
@click.option("-d", "--day", type=int)
@click.option("-y", "--year", type=int)
@click.option("-e", "--editor", type=str)
def cli(day: int | None, year: int | None, editor: str | None):
    today = datetime.date.today()
    if day is None:
        day = today.day
    if year is None:
        year = today.year

    path = pathlib.Path(f"aoc{year}") / f"day{day}.py"
    path.parent.mkdir(exist_ok=True)
    path.write_text(TEMPLATE.format(day=day, year=year))

    if editor is not None:
        os.system(f"{editor} {path.absolute()}")


def main():
    cli()

