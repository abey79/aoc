import dataclasses
import itertools
import math
import sys
from pathlib import Path
from typing import Callable, Optional

import aocd
import pytest
import tqdm
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
# noinspection SpellCheckingInspection
TEST_DATA: str = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
TEST_RESULT_PART1: int | None = 4140
TEST_RESULT_PART2: int | None = 3993


@dataclasses.dataclass
class Node:
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None
    value: int | None = None

    @classmethod
    def from_string(cls, data: str) -> "Node":
        return cls._from_string(data, 0)[0]

    @classmethod
    def _from_string(cls, data: str, pc: int) -> ("Node", int):
        if data[pc] == "[":
            left, pc = cls._from_string(data, pc + 1)
            assert data[pc] == ","
            right, pc = cls._from_string(data, pc + 1)
            assert data[pc] == "]"
            node = Node(left=left, right=right)
            left.parent = node
            right.parent = node
            return node, pc + 1
        else:
            digits = ""
            while data[pc].isdigit():
                digits += data[pc]
                pc += 1
            node = Node(value=int(digits))
            return node, pc

    def is_pair(self):
        return self.left is not None and self.right is not None

    def is_value(self):
        return self.value is not None

    def nullify(self):
        self.left = self.right = None
        self.value = 0

    def find_first_of_depth(self, depth: int) -> Optional["Node"]:
        if depth == 0 and self.is_pair():
            return self

        node = None
        if self.left is not None:
            node = self.left.find_first_of_depth(depth - 1)
        if node is None and self.right is not None:
            node = self.right.find_first_of_depth(depth - 1)
        return node

    def find_last_leaf(self) -> "Node":
        node = self
        while not node.is_value():
            node = node.right
        return node

    def find_left_value(self) -> Optional["Node"]:
        if self.parent is not None:
            if self.parent.left.is_value():
                return self.parent.left
            elif self.parent.right is self:
                return self.parent.left.find_last_leaf()
            else:
                return self.parent.find_left_value()

    def find_first_leaf(self) -> "Node":
        node = self
        while not node.is_value():
            node = node.left
        return node

    def find_right_value(self) -> Optional["Node"]:
        if self.parent is not None:
            if self.parent.right.is_value():
                return self.parent.right
            elif self.parent.left is self:
                return self.parent.right.find_first_leaf()
            else:
                return self.parent.find_right_value()

    def explode(self) -> bool:
        node = self.find_first_of_depth(4)
        if node is None:
            return False
        assert node.left.is_value() and node.right.is_value()

        lnode = node.find_left_value()
        if lnode is not None:
            lnode.value += node.left.value

        rnode = node.find_right_value()
        if rnode is not None:
            rnode.value += node.right.value

        node.nullify()
        return True

    def split(self) -> bool:
        node = self.find_value_to_split()
        if node is not None:
            node.left = Node(value=node.value // 2, parent=node)
            node.right = Node(value=math.ceil(node.value / 2), parent=node)
            node.value = None
            return True
        else:
            return False

    def find_value_to_split(self) -> Optional["Node"]:
        if self.is_value() and self.value >= 10:
            return self

        node = None
        if self.left is not None:
            node = self.left.find_value_to_split()
        if node is None and self.right is not None:
            node = self.right.find_value_to_split()
        return node

    def magnitude(self):
        if self.is_value():
            return self.value
        else:
            return 3 * self.left.magnitude() + 2 * self.right.magnitude()

    def __add__(self, other: "Node") -> "Node":
        node = Node(left=self, right=other)
        node.left.parent = node
        node.right.parent = node
        while True:
            if not node.explode():
                if not node.split():
                    break
        return node

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        else:
            return f"[{self.left},{self.right}]"


@pytest.mark.parametrize(
    ["base", "expected"],
    [
        ("[1,2]", "[1,2]"),
        ("[10,2]", "[[5,5],2]"),
        ("[11,2]", "[[5,6],2]"),
    ],
)
def test_split(base, expected):
    node = Node.from_string(base)
    res = node.split()
    assert res == (not base == expected)
    assert str(node) == expected


def test_magnitude():
    assert Node.from_string("[[1,2],[[3,4],5]]").magnitude() == 143
    assert Node.from_string("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]").magnitude() == 1384
    assert Node.from_string("[[[[1,1],[2,2]],[3,3]],[4,4]]").magnitude() == 445
    assert Node.from_string("[[[[3,0],[5,3]],[4,4]],[5,5]]").magnitude() == 791
    assert Node.from_string("[[[[5,0],[7,4]],[5,5]],[6,6]]").magnitude() == 1137
    assert (
        Node.from_string("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]").magnitude()
        == 3488
    )


@pytest.mark.parametrize(
    ["base", "exploded"],
    [
        ("[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"),
        ("[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"),
        ("[1,2]", None),
        ("[[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"),
    ],
)
def test_explode(base: str, exploded: str | None):
    node = Node.from_string(base)
    res = node.explode()
    assert res == (exploded is not None)
    if res:
        assert str(node) == exploded


def test_find_first_of_depth():
    assert str(Node.from_string("[[[[[9,8],1],2],3],4]").find_first_of_depth(4)) == "[9,8]"
    assert Node.from_string("[[[[5,1],2],3],4]").find_first_of_depth(4) is None
    assert str(Node.from_string("[7,[6,[5,[4,[3,2]]]]]").find_first_of_depth(4)) == "[3,2]"
    assert (
        str(Node.from_string("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]").find_first_of_depth(4))
        == "[7,3]"
    )


def test_addition():
    node1 = Node.from_string("[[[[4,3],4],4],[7,[[8,4],9]]]")
    node2 = Node.from_string("[1,1]")
    node = node1 + node2
    assert str(node) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"


def part1(data: str) -> int:
    lines = data.splitlines()
    node = Node.from_string(lines[0])

    for line in lines[1:]:
        node += Node.from_string(line)

    return node.magnitude()


def part2(data: str) -> int:
    lines = data.splitlines()
    return max(
        (Node.from_string(line1) + Node.from_string(line2)).magnitude()
        for line1, line2 in tqdm.tqdm(itertools.permutations(lines, 2))
    )


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
