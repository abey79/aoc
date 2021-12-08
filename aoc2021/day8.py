import sys
from pathlib import Path
from typing import AbstractSet, Callable, Collection, Dict, FrozenSet, Generator, Iterable, Set

import aocd
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
TEST_DATA: str = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
TEST_RESULT_PART1: int | None = 26
TEST_RESULT_PART2: int | None = 61229


def part1(data: str) -> int:
    cnt = 0
    for line in data.splitlines():
        output = line.split("|")[1].strip()
        for word in output.split(" "):
            match len(word):
                case 2 | 3 | 4 | 7:
                    cnt += 1
    return cnt


def infer_digit(digits: Iterable[FrozenSet[str]]) -> FrozenSet[str]:
    digit_list = list(digits)
    assert len(digit_list) == 1
    return digit_list[0]


def filter_by_length(
    digits: Iterable[FrozenSet[str]], length: int
) -> Generator[FrozenSet[str], None, None]:
    for digit in filter(lambda x: len(x) == length, digits):
        yield digit


def filter_by_containing(
    digits: Iterable[FrozenSet[str]], segs: FrozenSet[str]
) -> Generator[FrozenSet[str], None, None]:
    for digit in digits:
        if segs.issubset(digit):
            yield digit


# noinspection PyUnboundLocalVariable
def infer_mapping(digits: Set[FrozenSet[str]]) -> Dict[FrozenSet[str], int]:
    # find 1, 4, 7, 8 based on their length
    for digit in digits:
        match len(digit):
            case 2:
                set_1 = digit
            case 4:
                set_4 = digit
            case 3:
                set_7 = digit
            case 7:
                set_8 = digit
    digits -= {set_1, set_4, set_7, set_8}

    # digit 2 is only 5-len to contain segment e and g
    set_eg = set_8 - (set_7 | set_4)
    assert len(set_eg) == 2
    set_2 = infer_digit(filter_by_containing(filter_by_length(digits, 5), set_eg))
    digits -= {set_2}

    # digit 3 is only remaining 5-len to contain 1
    set_3 = infer_digit(filter_by_containing(filter_by_length(digits, 5), set_1))
    digits -= {set_3}
    set_5 = infer_digit(filter_by_length(digits, 5))
    digits -= {set_5}

    # digit 9 is only 6-len digit to contain 4
    set_9 = infer_digit(filter_by_containing(filter_by_length(digits, 6), set_4))
    digits -= {set_9}

    # of remaining 6-len digits, only 0 contains 1
    set_0 = infer_digit(filter_by_containing(filter_by_length(digits, 6), set_1))
    digits -= {set_0}
    set_6 = infer_digit(digits)

    return {
        set_0: 0,
        set_1: 1,
        set_2: 2,
        set_3: 3,
        set_4: 4,
        set_5: 5,
        set_6: 6,
        set_7: 7,
        set_8: 8,
        set_9: 9,
    }


def part2(data: str) -> int:
    total = 0
    for line in data.splitlines():
        digits, display = line.split(" | ")

        digit_map = infer_mapping({frozenset(digit) for digit in digits.split(" ")})

        output_value = 0
        for display_digit in display.split(" "):
            output_value *= 10
            output_value += digit_map[frozenset(display_digit)]

        total += output_value
    return total


def run_test_part1():
    if TEST_RESULT_PART1 is None:
        raise NotImplementedError
    assert part1(TEST_DATA) == TEST_RESULT_PART1


def run_test_part2():
    if TEST_RESULT_PART2 is None:
        raise NotImplementedError
    assert part2(TEST_DATA) == TEST_RESULT_PART2


def run_solution(name: str, test_func: Callable[[], None], solution: Callable[[str], int]):
    proceed = True
    try:
        test_func()
        console.print(f"Test {name} succeeded.", style="green")
    except NotImplementedError:
        console.print(f"Test {name} not implemented", style="yellow")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]
    except AssertionError:
        console.print(f"Test {name} failed", style="red")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]

    if not proceed:
        sys.exit()

    console.print(
        f"{name.capitalize()} solution: {solution(aocd.get_data(day=DAY, year=2021))}",
        style="blue",
    )


def main() -> None:
    console.print(f"Running for day {DAY}", style="blue")
    run_solution("part 1", run_test_part1, part1)
    run_solution("part 2", run_test_part2, part2)


if __name__ == "__main__":
    main()
