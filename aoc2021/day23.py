import itertools
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

import aocd
import networkx as nx
import pytest
from rich.console import Console

console = Console()

YEAR = 2021
DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
# noinspection SpellCheckingInspection
TEST_DATA: str = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########"""
TEST_RESULT_PART1: int | None = 12521
DATA = aocd.get_data(day=DAY, year=2021)

Spot = Optional[str]
State = Tuple[
    Spot, Spot, Spot, Spot, Spot, Spot, Spot, Spot, Spot, Spot, Spot, Spot, Spot, Spot, Spot
]

TOPO = nx.Graph()
TOPO.add_edge(0, 1, value=1)
TOPO.add_edge(2, 3, value=1)
TOPO.add_edge(4, 5, value=1)
TOPO.add_edge(6, 7, value=1)
TOPO.add_edge(8, 9, value=1)
TOPO.add_edge(9, 10, value=2)
TOPO.add_edge(10, 11, value=2)
TOPO.add_edge(11, 12, value=2)
TOPO.add_edge(12, 13, value=2)
TOPO.add_edge(13, 14, value=1)
TOPO.add_edge(1, 9, value=2)
TOPO.add_edge(1, 10, value=2)
TOPO.add_edge(3, 10, value=2)
TOPO.add_edge(3, 11, value=2)
TOPO.add_edge(5, 11, value=2)
TOPO.add_edge(5, 12, value=2)
TOPO.add_edge(7, 12, value=2)
TOPO.add_edge(7, 13, value=2)

# precompute paths from top of room to any hall
ROOM_TO_HALL = {}
for from_idx, to_idx in itertools.product(range(15), repeat=2):
    if from_idx == to_idx:
        continue
    ROOM_TO_HALL[(from_idx, to_idx)] = (
        nx.shortest_path(TOPO, from_idx, to_idx, weight="value"),
        nx.shortest_path_length(TOPO, from_idx, to_idx, weight="value"),
    )

ITEM_TO_ROOM = {"A": (0, 1), "B": (2, 3), "C": (4, 5), "D": (6, 7)}


def read_data(data: str) -> State:
    def convert(s: str) -> Spot:
        return s if s != "." else None

    lines = data.splitlines()
    state = (
        convert(lines[3][3]),
        convert(lines[2][3]),
        convert(lines[3][5]),
        convert(lines[2][5]),
        convert(lines[3][7]),
        convert(lines[2][7]),
        convert(lines[3][9]),
        convert(lines[2][9]),
        convert(lines[1][1]),
        convert(lines[1][2]),
        convert(lines[1][4]),
        convert(lines[1][6]),
        convert(lines[1][8]),
        convert(lines[1][10]),
        convert(lines[1][11]),
    )

    return state


def test_read_data():
    assert read_data(TEST_DATA) == ("A", "B", "D", "C", "C", "B", "A", "D") + (None,) * 7


def move(state: State, from_index: int, to_index: int) -> State:
    assert state[to_index] is None
    new_state = list(state)
    new_state[to_index] = new_state[from_index]
    new_state[from_index] = None
    # noinspection PyTypeChecker
    return tuple(new_state)


MULTIPLIER = {"A": 1, "B": 10, "C": 100, "D": 1000}


def path_cost(state: State, from_index: int, to_index: int) -> Optional[int]:
    path, val = ROOM_TO_HALL[(from_index, to_index)]
    if all(state[i] is None for i in path[1:]):
        return val * MULTIPLIER[state[from_index]]
    else:
        return None


def is_final(state: State, index: int) -> bool:
    bottom_dest, top_dest = ITEM_TO_ROOM[state[index]]
    return index == bottom_dest or (index == top_dest and state[bottom_dest] == state[index])


def possible_final_move(state: State, index: int) -> Optional[Tuple[int, int]]:
    bottom_dest, top_dest = ITEM_TO_ROOM[state[index]]

    # if we can score a final move, we do it in priority!
    if index != bottom_dest and (cost := path_cost(state, index, bottom_dest)) is not None:
        return bottom_dest, cost
    elif (
        index != top_dest
        and state[bottom_dest] == state[index]
        and (cost := path_cost(state, index, top_dest)) is not None
    ):
        return top_dest, cost

    return None


def possible_exploration_moves(state: State, index: int) -> Dict[int, int]:
    assert index < 8

    result = {}
    for dest in range(8, 15):
        cost = path_cost(state, index, dest)
        if cost is not None:
            result[dest] = cost

    return result


TARGET_STATE: State = ("A", "A", "B", "B", "C", "C", "D", "D") + (None,) * 7


def explore(state: State, cost: int, all_states: Dict[State, int]):
    # dont pursue this avenue if it has been explored already
    if state in all_states and cost >= all_states[state]:
        return None
    else:
        all_states[state] = cost

    # check if a "final move" is possible
    for index in range(15):
        if state[index] is not None and not is_final(state, index):
            res = possible_final_move(state, index)
            if res is not None:
                dest, added_cost = res
                explore(move(state, index, dest), cost + added_cost, all_states)
                return

    # no final move is possible, explore everything
    for index in range(8):
        if state[index] is not None and not is_final(state, index):
            moves = possible_exploration_moves(state, index)
            for dest, added_cost in moves.items():
                explore(move(state, index, dest), cost + added_cost, all_states)


def part1(data: str) -> int:
    state = read_data(data)
    all_states = {}
    explore(state, 0, all_states)
    return all_states[TARGET_STATE]


@pytest.mark.parametrize(
    ("state", "cost"),
    [
        [
            ("A", None, "B", "B", "C", "C", "D", "D", "A", None, None, None, None, None, None),
            3,
        ],
        [
            ("B", "B", "A", "A", "C", "C", "D", "D", None, None, None, None, None, None, None),
            114,
        ],
    ],
)
def test_explore(state, cost):
    all_states = {}
    explore(state, 0, all_states)
    assert TARGET_STATE in all_states
    assert all_states[TARGET_STATE] == cost


@pytest.mark.skipif(TEST_RESULT_PART1 is None, reason="part 1 test result not provided")
def test_part1():
    assert part1(TEST_DATA) == TEST_RESULT_PART1


def main() -> None:
    console.print(f"AOC {YEAR} day {DAY}", style="blue")
    console.print("Tests: ", end="", style="blue")
    pytest.main(["-q", __file__])
    start = time.time()
    res = part1(DATA)
    delta = time.time() - start
    console.print(f"Part 1 solution: {res} (execution time: {delta*1000:.2f}ms)", style="blue")


if __name__ == "__main__":
    main()
