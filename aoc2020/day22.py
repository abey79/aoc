from collections import deque
from typing import Tuple

import aocd

TEST_DATA = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""


def parse(data: str) -> Tuple[deque, deque]:
    p1, p2 = data.split("\n\n")

    return (
        deque(int(card) for card in p1.splitlines()[1:]),
        deque(int(card) for card in p2.splitlines()[1:]),
    )


def day22_part1(data: str) -> int:
    p1, p2 = parse(data)

    while len(p1) > 0 and len(p2) > 0:
        c1, c2 = p1.popleft(), p2.popleft()
        assert c1 != c2
        if c1 > c2:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)

    p = p1 if len(p1) > 0 else p2
    return sum((i + 1) * c for i, c in enumerate(reversed(p)))


def test_day22_part1():
    assert day22_part1(TEST_DATA) == 306


def game(p1: deque, p2: deque) -> Tuple[int, deque, deque]:
    history = set()

    while len(p1) > 0 and len(p2) > 0:

        fingerprint = (tuple(p1), tuple(p2))
        if fingerprint in history:
            return 1, p1, p2
        else:
            history.add(fingerprint)

        c1, c2 = p1.popleft(), p2.popleft()

        if c1 <= len(p1) and c2 <= len(p2):
            winner, _, _ = game(deque(list(p1)[:c1]), deque(list(p2)[:c2]))
        else:
            winner = 1 if c1 > c2 else 2

        if winner == 1:
            p1.append(c1)
            p1.append(c2)
        elif winner == 2:
            p2.append(c2)
            p2.append(c1)
        else:
            assert False

    return 1 if len(p1) > 0 else 2, p1, p2


def day22_part2(data: str) -> int:
    p1, p2 = parse(data)

    winner, p1, p2 = game(p1, p2)
    p = p1 if winner == 1 else p2
    return sum((i + 1) * c for i, c in enumerate(reversed(p)))


def test_day22_part2():
    assert day22_part2(TEST_DATA) == 291


def main():
    print(f"day 22 part 1: {day22_part1(aocd.get_data(day=22, year=2020))}")
    print(f"day 22 part 2: {day22_part2(aocd.get_data(day=22, year=2020))}")


if __name__ == "__main__":
    main()
