from __future__ import annotations

import dataclasses
from collections import defaultdict
from typing import Callable

import aocd

TEST_DATA = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""
TEST_PART1_RESULT = 95437
TEST_PART2_RESULT = 24933642


@dataclasses.dataclass
class File:
    name: str
    size: int


@dataclasses.dataclass
class Dir:
    name: str
    files: {str, int} = dataclasses.field(default_factory=dict)
    parent: Dir | None = None
    dirs: {str, Dir} = dataclasses.field(default_factory=dict)

    def size(self):
        return sum(d.size() for d in self.dirs.values()) + sum(self.files.values())


def find_dirs(d: Dir, key: Callable) -> list[Dir]:
    out = []

    if key(d.size()):
        out.append(d)

    for d in d.dirs.values():
        out.extend(find_dirs(d, key))

    return out


def load(data: str) -> Dir:
    root_dir = Dir(name="/")
    current_dir = root_dir

    lines = data.splitlines()
    while lines:
        line = lines.pop(0)
        match line.split(" "):
            case ["$", "cd", "/"]:
                current_dir = root_dir

            case ["$", "cd", ".."]:
                current_dir = current_dir.parent

            case ["$", "cd", dir_name]:
                current_dir = current_dir.dirs[dir_name]

            case ["$", "ls"]:
                while lines and not lines[0].startswith("$"):
                    line = lines.pop(0)
                    match line.split(" "):
                        case ["dir", dir_name]:
                            current_dir.dirs[dir_name] = Dir(name=dir_name, parent=current_dir)

                        case [size, file_name]:
                            current_dir.files[file_name] = int(size)

                        case _:
                            assert False, f"unexpected ls output: {line}"

            case _:
                assert False, f"unexpected line: {line}"
    return root_dir


def part1(data: str):
    root_dir = load(data)
    return sum(d.size() for d in find_dirs(root_dir, lambda i: i <= 100000))


def part2(data: str):
    root_dir = load(data)
    needed_size = 30000000 - (70000000 - root_dir.size())
    dirs = sorted(find_dirs(root_dir, lambda i: i >= needed_size), key=lambda d: d.size())
    return dirs[0].size()


def test_part1():
    if TEST_PART1_RESULT is not None:
        assert part1(TEST_DATA) == TEST_PART1_RESULT


def test_part2():
    if TEST_PART2_RESULT is not None:
        assert part2(TEST_DATA) == TEST_PART2_RESULT


def main() -> None:
    data = aocd.get_data(day=7, year=2022)
    print("Running for day 7 of year 2022")
    print("Part 1 solution:", part1(data))
    print("Part 2 solution:", part2(data))


if __name__ == "__main__":
    main()
