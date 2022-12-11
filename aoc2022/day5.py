import aocd

TEST_DATA = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
TEST_PART1_RESULT = "CMZ"
TEST_PART2_RESULT = "MCD"


def part1(data: str):
    stack_def, instructions = data.split("\n\n")

    # load stacks
    stack_lines = stack_def.splitlines()
    stack_count = round((len(stack_lines[-1]) + 1) / 4)
    stacks = [[] for _ in range(stack_count)]
    for i in range(len(stack_lines) - 2, -1, -1):
        for j in range(stack_count):
            c = stack_lines[i][j * 4 + 1]
            if c != " ":
                stacks[j].append(c)

    # load instructions
    for instr in instructions.splitlines():
        _, num, _, src, _, dst = instr.split()
        for i in range(int(num)):
            stacks[int(dst) - 1].append(stacks[int(src) - 1].pop())

    return "".join(stack[-1] for stack in stacks)


def part2(data: str):
    stack_def, instructions = data.split("\n\n")

    # load stacks
    stack_lines = stack_def.splitlines()
    stack_count = round((len(stack_lines[-1]) + 1) / 4)
    stacks = [[] for _ in range(stack_count)]
    for i in range(len(stack_lines) - 2, -1, -1):
        for j in range(stack_count):
            c = stack_lines[i][j * 4 + 1]
            if c != " ":
                stacks[j].append(c)

    # load instructions
    for instr in instructions.splitlines():
        _, num, _, src, _, dst = instr.split()
        num = int(num)

        stacks[int(dst) - 1].extend(stacks[int(src) - 1][-num:])
        stacks[int(src) - 1] = stacks[int(src) - 1][:-num]

    return "".join(stack[-1] for stack in stacks)


def test_part1():
    if TEST_PART1_RESULT is not None:
        assert part1(TEST_DATA) == TEST_PART1_RESULT


def test_part2():
    if TEST_PART2_RESULT is not None:
        assert part2(TEST_DATA) == TEST_PART2_RESULT


def main() -> None:
    data = aocd.get_data(day=5, year=2022)
    print("Running for day 5 of year 2022")
    print("Part 1 solution:", part1(data))
    print("Part 2 solution:", part2(data))


if __name__ == "__main__":
    main()
