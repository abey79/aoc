from typing import List, Tuple

import aocd

TEST_PROG = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""

TEST_PROG_CORRECTED = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
nop -4
acc +6"""


ProgType = List[Tuple[str, int]]


def parse_program(data: str) -> ProgType:
    def parse_line(line: str) -> Tuple[str, int]:
        parts = line.split()
        return parts[0], int(parts[1])

    return [parse_line(ln) for ln in data.split("\n")]


def run(prog: ProgType) -> Tuple[int, bool]:
    pc = 0
    executed = [False] * len(prog)
    accum = 0

    while True:
        if executed[pc]:
            return accum, False
        executed[pc] = True

        op, param = prog[pc]

        if op == "acc":
            accum += param
            pc += 1
        elif op == "jmp":
            pc += param
        elif op == "nop":
            pc += 1
        else:
            raise ValueError(f"unknown instruction: {op, param}")

        if pc == len(prog):
            break
        elif pc >= len(prog):
            raise RuntimeError(f"jmp past EOF attempted: pc={pc} len={len(prog)}")

    return accum, True


def test_run():
    assert run(parse_program(TEST_PROG)) == (5, False)
    assert run(parse_program(TEST_PROG_CORRECTED)) == (8, True)


def correct_and_run(prog: ProgType) -> int:
    for i in range(len(prog)):
        if prog[i][0] in ("jmp", "nop"):
            fixed_prog = prog.copy()
            fixed_prog[i] = ("jmp" if prog[i][0] == "nop" else "nop", prog[i][1])
            accum, completed = run(fixed_prog)
            if completed:
                return accum
    raise RuntimeError("could not fix program")


def test_correct_and_run():
    assert correct_and_run(parse_program(TEST_PROG)) == 8


def main():
    print(f"day 8 part 1: {run(parse_program(aocd.get_data(day=8, year=2020)))[0]}")
    print(f"day 8 part 2: {correct_and_run(parse_program(aocd.get_data(day=8, year=2020)))}")


if __name__ == "__main__":
    main()
