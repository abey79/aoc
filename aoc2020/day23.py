from typing import Dict, Iterable, List

import numpy as np
import tqdm


def modn(it: Iterable[int], n: int):
    for i in it:
        yield i % n


def game(cups: List[int], n: int) -> List[int]:
    current_index = 0

    for _ in range(n):
        removed_indices = list(modn(range(current_index + 1, current_index + 4), len(cups)))
        removed = [cups[idx] for idx in removed_indices]

        # find destination
        dest = cups[current_index] - 1
        if dest == 0:
            dest = len(cups)
        while dest in removed:
            dest -= 1
            if dest == 0:
                dest = len(cups)
        dest_index = cups.index(dest)

        new_cups = [0] * len(cups)
        dst_offset = 0
        for i in range(len(cups)):
            idx = (i + current_index) % len(cups)
            if idx not in removed_indices:
                new_cups[(idx + dst_offset) % len(cups)] = cups[idx]
            else:
                dst_offset -= 1
            if idx == dest_index:
                for r in removed:
                    dst_offset += 1
                    new_cups[(idx + dst_offset) % len(cups)] = r

        cups = new_cups
        current_index = (current_index + 1) % len(cups)

    return cups


def process_range(a, b, l):
    a = a % l
    b = b % l
    if a == b:
        return []
    elif b > a:
        return [slice(a, b)]
    else:
        return [slice(a, l), slice(0, b)]


# @profile
def game_np(cups: List[int], n: int) -> List[int]:
    cups = np.array(cups, dtype=int)
    len_cups = len(cups)

    current_index = 0
    for _ in tqdm.tqdm(range(n)):
        removed_indices = np.arange(current_index + 1, current_index + 4) % len_cups
        removed = cups[removed_indices]

        # find destination
        dest = cups[current_index] - 1
        if dest == 0:
            dest = len_cups
        while dest in removed:
            dest -= 1
            if dest == 0:
                dest = len_cups
        ([dest_index],) = np.where(cups == dest)

        parts = [np.array([cups[current_index]])]
        for slc in process_range(current_index + 4, dest_index + 1, len_cups):
            parts.append(cups[slc])
        parts.append(cups[removed_indices])
        for slc in process_range(dest_index + 1, current_index, len_cups):
            parts.append(cups[slc])
        new_cups = np.hstack(parts)

        cups = np.roll(new_cups, current_index)
        current_index = (current_index + 1) % len_cups

    # noinspection PyTypeChecker
    return cups.tolist()


def game_map(cup_list: List[int], n: int) -> Dict[int, int]:
    cups = {}
    for i in range(len(cup_list)):
        cups[cup_list[i]] = cup_list[(i + 1) % len(cup_list)]

    current = cup_list[0]
    for _ in tqdm.tqdm(range(n)):
        # remove 3 cups
        r1 = cups[current]
        r2 = cups[r1]
        r3 = cups[r2]
        cups[current] = cups[r3]

        dest = current - 1
        if dest == 0:
            dest = len(cups)
        while dest in (r1, r2, r3):
            dest -= 1
            if dest == 0:
                dest = len(cups)

        cups[r3] = cups[dest]
        cups[dest] = r1

        current = cups[current]

    return cups


def day23_part1(data: str, n: int) -> str:
    cups = [int(c) for c in data]

    if False:
        cups = game_np(cups, n)

        one_idx = cups.index(1)
        final = cups[one_idx + 1 :] + cups[:one_idx]
        return "".join(str(c) for c in final)
    else:
        cups = game_map(cups, n)
        lst = []
        current = 1
        while cups[current] != 1:
            current = cups[current]
            lst.append(current)
        return "".join(str(c) for c in lst)


def test_day23_part1():
    assert day23_part1("389125467", 10) == "92658374"
    assert day23_part1("389125467", 100) == "67384529"


def day23_part2(data: str, n: int) -> int:
    cups = [int(c) for c in data]
    cups += list(range(len(cups) + 1, 1000001))

    if False:
        cups = game_np(cups, n)

        one_idx = cups.index(1)
        return cups[(one_idx + 1) % len(cups)] * cups[(one_idx + 2) % len(cups)]
    else:
        cups = game_map(cups, n)
        return cups[1] * cups[cups[1]]


def test_day23_part2():
    # assert day23_part2("389125467", 10000000) == 149245887792
    day23_part2("389125467", 1000)


def main():
    print(f"day 23 part 1: {day23_part1('916438275', 100)}")
    print(f"day 23 part 2: {day23_part2('916438275', 10000000)}")


if __name__ == "__main__":
    main()
