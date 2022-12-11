import aocd
import numpy as np

TEST_DATA = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

TEST_DATA2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""


def day14_part1(data: str) -> int:
    mem = {}
    mask_and = int("1" * 36, 2)
    mask_or = int("0" * 36, 2)

    for line in data.split("\n"):
        op, val = line.split(" = ")

        if op == "mask":
            mask_and = int(val.replace("X", "1"), 2)
            mask_or = int(val.replace("X", "0"), 2)
        else:
            addr = int(op.lstrip("mem[").rstrip("]"))
            mem[addr] = (int(val) & mask_and) | mask_or

    return sum(mem.values())


def test_day14_part1():
    assert day14_part1(TEST_DATA) == 165


def day14_part2(data: str) -> int:
    mem = {}
    pow_two = 2 ** np.arange(36, dtype=int)[::-1]

    for line in data.split("\n"):
        op, val = line.split(" = ")

        if op == "mask":
            mask = np.array([c == "1" for c in val], dtype=bool)
            floating_bits = np.array([c == "X" for c in val], dtype=bool)
        else:
            addr = int(op.lstrip("mem[").rstrip("]"))

            # convert to 36-bit array
            addr_bits = np.unpackbits(np.array([addr], dtype=">i8").view(np.uint8))[-36:]
            addr_bits[mask] = 1

            for i in range(2 ** floating_bits.sum()):
                bits = np.unpackbits(np.array([i], dtype=">i8").view(np.uint8))
                addr_bits[floating_bits] = bits[-floating_bits.sum() :]
                mem[addr_bits.dot(pow_two)] = int(val)

    return sum(mem.values())


def test_day14_part2():
    assert day14_part2(TEST_DATA2) == 208


def main():
    print(f"day 14 part 1: {day14_part1(aocd.get_data(day=14, year=2020))}")
    print(f"day 14 part 2: {day14_part2(aocd.get_data(day=14, year=2020))}")


if __name__ == "__main__":
    main()
