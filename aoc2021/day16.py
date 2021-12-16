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
TEST_DATA_PART1: str = """A0016C880162017C3686B18A3D4780"""
TEST_DATA_PART2: str = """9C0141080250320F1802104A08"""
TEST_RESULT_PART1: int | None = 31
TEST_RESULT_PART2: int | None = 1


def hex2bin(data: str) -> str:
    return "".join((f"{int(c, base=16):04b}" for c in data))


def extract_literal(packet: str, pc: int) -> (int, int):
    res = ""
    while True:
        res += packet[pc + 1 : pc + 5]
        pc += 5
        if packet[pc - 5] == "0":
            break

    return int(res, base=2), pc


def compute_operator(opcode: int, values: [int]) -> int:
    match opcode:
        case 0:  # sum
            return sum(values)

        case 1:  # product
            return math.prod(values)

        case 2:  # min
            return min(values)

        case 3:  # max
            return max(values)

        case 5:  # gt
            v1, v2 = values
            return 1 if v1 > v2 else 0

        case 6:  # lt
            v1, v2 = values
            return 1 if v1 < v2 else 0

        case 7:  # eq
            v1, v2 = values
            return 1 if v1 == v2 else 0


def decode(packet: str, pc: int, version_sum: int) -> (int, int, int):
    version = int(packet[pc : pc + 3], base=2)
    type_id = int(packet[pc + 3 : pc + 6], base=2)
    pc += 6

    match type_id:
        case 4:  # literal
            value, pc = extract_literal(packet, pc)
            print(f"literal (v={version}): {value}, 0x{value:X}")

        case opcode:  # operator
            length_type_id = packet[pc]
            pc += 1
            values = []
            if length_type_id == "0":
                sub_packet_length = int(packet[pc : pc + 15], base=2)
                pc += 15
                print(f"operator (op={opcode}, v={version}): sub length {sub_packet_length}")
                end_pc = pc + sub_packet_length
                while True:
                    val, pc, version_sum = decode(packet, pc, version_sum)
                    values.append(val)
                    if pc == end_pc:
                        break
                    elif pc > end_pc:
                        assert False
            else:
                sub_packet_count = int(packet[pc : pc + 11], base=2)
                pc += 11
                print(f"operator (op={opcode}, v={version}): sub count {sub_packet_count}")

                for _ in range(sub_packet_count):
                    val, pc, version_sum = decode(packet, pc, version_sum)
                    values.append(val)

            value = compute_operator(opcode, values)

    return value, pc, version_sum + version


def part1(data: str) -> int:
    packet = hex2bin(data)
    value, pc, version_sum = decode(packet, 0, 0)
    print(f"version sum: {version_sum}, reminder: {packet[pc:]}")
    return version_sum


def part2(data: str) -> int:
    packet = hex2bin(data)
    value, pc, version_sum = decode(packet, 0, 0)
    print(f"value: {value}, version sum: {version_sum}, reminder: {packet[pc:]}")
    return value


def run_test_part1(*args, **kwargs):
    if TEST_RESULT_PART1 is None:
        raise NotImplementedError
    # noinspection PyArgumentList
    assert part1(TEST_DATA_PART1, *args, **kwargs) == TEST_RESULT_PART1


def run_test_part2(*args, **kwargs):
    if TEST_RESULT_PART2 is None:
        raise NotImplementedError
    # noinspection PyArgumentList
    assert part2(TEST_DATA_PART2, *args, **kwargs) == TEST_RESULT_PART2


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
