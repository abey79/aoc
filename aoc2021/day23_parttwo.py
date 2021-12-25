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
TEST_RESULT_PART2: int | None = 44169
DATA = aocd.get_data(day=DAY, year=2021)

Spot = Optional[str]
State = Tuple[
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
    Spot,
]

TOPO = nx.Graph()

for i in (0, 4, 8, 12):
    TOPO.add_edge(i, i + 1, value=1)
    TOPO.add_edge(i + 1, i + 2, value=1)
    TOPO.add_edge(i + 2, i + 3, value=1)

TOPO.add_edge(16, 17, value=1)
TOPO.add_edge(17, 18, value=2)
TOPO.add_edge(18, 19, value=2)
TOPO.add_edge(19, 20, value=2)
TOPO.add_edge(20, 21, value=2)
TOPO.add_edge(21, 22, value=1)
TOPO.add_edge(3, 17, value=2)
TOPO.add_edge(3, 18, value=2)
TOPO.add_edge(7, 18, value=2)
TOPO.add_edge(7, 19, value=2)
TOPO.add_edge(11, 19, value=2)
TOPO.add_edge(11, 20, value=2)
TOPO.add_edge(15, 20, value=2)
TOPO.add_edge(15, 21, value=2)


# precompute paths from top of room to any hall
ROOM_TO_HALL = {}
for from_idx, to_idx in itertools.product(range(23), repeat=2):
    if from_idx == to_idx:
        continue
    ROOM_TO_HALL[(from_idx, to_idx)] = (
        nx.shortest_path(TOPO, from_idx, to_idx, weight="value"),
        nx.shortest_path_length(TOPO, from_idx, to_idx, weight="value"),
    )

ITEM_TO_ROOM = {
    "A": (0, 1, 2, 3),
    "B": (4, 5, 6, 7),
    "C": (8, 9, 10, 11),
    "D": (12, 13, 14, 15),
}


def read_data(data: str) -> State:
    def convert(s: str) -> Spot:
        assert s != "."
        return s

    lines = data.splitlines()
    state = (
        convert(lines[3][3]),
        "D",
        "D",
        convert(lines[2][3]),
        convert(lines[3][5]),
        "B",
        "C",
        convert(lines[2][5]),
        convert(lines[3][7]),
        "A",
        "B",
        convert(lines[2][7]),
        convert(lines[3][9]),
        "C",
        "A",
        convert(lines[2][9]),
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )

    return state


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
    val = state[index]
    dests = ITEM_TO_ROOM[val]
    return index in dests and all(state[idx] == val for idx in dests[: dests.index(index)])


def possible_final_move(state: State, index: int) -> Optional[Tuple[int, int]]:
    val = state[index]
    dests = ITEM_TO_ROOM[state[index]]

    for i, dest in enumerate(dests):
        if (
            index != dest
            and all(state[idx] == val for idx in dests[:i])
            and (cost := path_cost(state, index, dest)) is not None
        ):
            return dest, cost

    return None


def possible_exploration_moves(state: State, index: int) -> Dict[int, int]:
    assert index < 16

    result = {}
    for dest in range(16, 23):
        cost = path_cost(state, index, dest)
        if cost is not None:
            result[dest] = cost

    return result


TARGET_STATE: State = ("A",) * 4 + ("B",) * 4 + ("C",) * 4 + ("D",) * 4 + (None,) * 7


def explore(state: State, cost: int, all_states: Dict[State, int]):
    # dont pursue this avenue if it has been explored already
    if state in all_states and cost >= all_states[state]:
        return None
    else:
        all_states[state] = cost

    # check if a "final move" is possible
    for index in range(23):
        if state[index] is not None and not is_final(state, index):
            res = possible_final_move(state, index)
            if res is not None:
                dest, added_cost = res
                explore(move(state, index, dest), cost + added_cost, all_states)
                return

    # no final move is possible, explore everything
    for index in range(16):
        if state[index] is not None and not is_final(state, index):
            moves = possible_exploration_moves(state, index)
            for dest, added_cost in moves.items():
                explore(move(state, index, dest), cost + added_cost, all_states)


def part2(data: str) -> int:
    state = read_data(data)
    all_states = {}
    explore(state, 0, all_states)
    print(f"States visited: {len(all_states)}")
    return all_states[TARGET_STATE]


@pytest.mark.skipif(TEST_RESULT_PART2 is None, reason="part 2 test result not provided")
def test_part2():
    assert part2(TEST_DATA) == TEST_RESULT_PART2


def main() -> None:
    console.print(f"AOC {YEAR} day {DAY}", style="blue")
    console.print("Tests: ", end="", style="blue")
    pytest.main(["-q", __file__])
    start = time.time()
    res = part2(DATA)
    delta = time.time() - start
    console.print(f"Part 2 solution: {res} (execution time: {delta*1000:.2f}ms)", style="blue")


if __name__ == "__main__":
    main()
