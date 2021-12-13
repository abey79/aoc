import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable, Set

import aocd
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
TEST_DATA: str = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
TEST_RESULT_PART1: int | None = 10
TEST_RESULT_PART2: int | None = 36


def explore(route: (str,), graph: {str: [str]}) -> Set[(str,)]:
    new_routes = set()

    if route[-1] == "end":
        new_routes.add(route)
    else:
        for node in graph[route[-1]]:
            if node.isupper() or node not in route:
                new_routes |= explore(route + (node,), graph)

    return new_routes


def part1(data: str) -> int:
    graph = defaultdict(list)

    for line in data.splitlines():
        a, b = line.split("-")
        graph[a].append(b)
        graph[b].append(a)

    routes = explore(("start",), graph)
    return len(routes)


def is_route_valid(route: (str,)) -> bool:
    counter = Counter(route)
    double_visit = False
    for k, v in counter.items():
        match k:
            case "start" if v > 1:
                return False
            case "end" if v > 1:
                return False
            case s if s.islower() and v > 1:
                if v == 2 and not double_visit:
                    double_visit = True
                else:
                    return False
    return True


def explore2(route: (str,), graph: {str: [str]}) -> Set[(str,)]:
    new_routes = set()

    if route[-1] == "end":
        new_routes.add(route)
    else:
        for node in graph[route[-1]]:

            if is_route_valid(new_route := route + (node,)):
                new_routes |= explore2(new_route, graph)

    return new_routes


def part2(data: str) -> int:
    graph = defaultdict(list)

    for line in data.splitlines():
        a, b = line.split("-")
        graph[a].append(b)
        graph[b].append(a)

    routes = explore2(("start",), graph)
    return len(routes)


def run_test_part1():
    if TEST_RESULT_PART1 is None:
        raise NotImplementedError
    assert part1(TEST_DATA) == TEST_RESULT_PART1


def run_test_part2():
    if TEST_RESULT_PART2 is None:
        raise NotImplementedError
    assert part2(TEST_DATA) == TEST_RESULT_PART2


def run_solution(name: str, test_func: Callable[[], None], solution: Callable[[str], int]):
    proceed = True
    try:
        test_func()
        console.print(f"Test {name} succeeded.", style="green")
    except NotImplementedError:
        console.print(f"Test {name} not implemented", style="yellow")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]
    except AssertionError:
        console.print(f"Test {name} failed", style="red")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]

    if not proceed:
        sys.exit()

    console.print(
        f"{name.capitalize()} solution: {solution(aocd.get_data(day=DAY, year=2021))}",
        style="blue",
    )


def main() -> None:
    console.print(f"Running for day {DAY}", style="blue")
    run_solution("part 1", run_test_part1, part1)
    run_solution("part 2", run_test_part2, part2)


if __name__ == "__main__":
    main()
