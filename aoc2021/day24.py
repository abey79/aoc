from pathlib import Path
from typing import Callable

import aocd

# import numba
import numpy as np
from rich.console import Console

console = Console()

YEAR = 2021
DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
DATA = aocd.get_data(day=DAY, year=2021)


def compile_code(data: str) -> Callable:
    code = (
        "import numba\n"
        "@numba.jit(nopython=True)\n"
        "def monad(arr):\n"
        "    i = w = x = y = z = 0\n"
    )

    for line in data.splitlines():
        match line.split():
            case ["inp", a]:
                code += f"    {a} = arr[i]\n    i += 1\n"

            case ["add", a, b]:
                code += f"    {a} += {b}\n"

            case ["mul", a, b]:
                code += f"    {a} *= {b}\n"

            case ["div", a, b]:
                code += f"    {a} //= {b}\n"

            case ["mod", a, b]:
                code += f"    {a} %= {b}\n"

            case ["eql", a, b]:
                code += f"    {a} = int({a} == {b})\n"

            case _:
                assert False

    code += "    return w, x, y, z"

    local_variables = {}
    exec(code, globals(), local_variables)
    return local_variables["monad"]


def test_exec_code():
    monad = compile_code(
        """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2"""
    )
    assert monad(np.array([3], dtype=int)) == (0, 0, 1, 1)


def monad_reverse_engineered(arr):
    # w = arr[0]
    # x = int(z % 26 + 11 != w)  # always x = 1
    # z //= 1
    # z *= 25 * x + 1
    # z += (w + 3) * x

    # In order to have z == 0, x must have a value of zero at each step where it's possible.
    # As a result, the following constraints exists:
    #   arr[2] - 3 = arr[3]
    #   arr[5] + 3 = arr[6]
    #   arr[4] + 2 = arr[7]
    #   arr[8] - 5 = arr[9]
    #   arr[10] - 1 = arr[11]
    #   arr[1] + 7 = arr[12]
    #   arr[0] - 8 = arr[13]
    #
    # These constraints make it easy to compute the highest/lowest set of input by hand.

    z = 0
    z += arr[0] + 3

    z *= 26
    z += arr[1] + 7

    z *= 26
    z += arr[2] + 1

    w = arr[3]
    x = int(arr[2] - 3 != arr[3])
    z //= 26
    z *= 25 * x + 1
    z += (w + 6) * x

    z *= 26
    z += arr[4] + 14

    z *= 26
    z += arr[5] + 7

    w = arr[6]
    x = int(arr[5] + 3 != w)
    z //= 26
    z *= 25 * x + 1
    z += (w + 9) * x

    w = arr[7]
    x = int(z % 26 - 12 != w)
    z //= 26
    z *= 25 * x + 1
    z += (w + 9) * x

    z *= 26
    z += arr[8] + 6

    w = arr[9]
    x = int(z % 26 - 11 != w)
    z //= 26
    z *= 25 * x + 1
    z += (w + 4) * x

    z *= 26
    z += arr[10]

    w = arr[11]
    x = int(z % 26 - 1 != w)
    z //= 26
    z *= 25 * x + 1
    z += (w + 7) * x

    w = arr[12]
    x = int(z % 26 + 0 != w)
    z //= 26
    z *= 25 * x + 1
    z += (w + 12) * x

    w = arr[13]
    x = int(z % 26 - 11 != w)
    z //= 26
    z *= 25 * x + 1
    z += (w + 1) * x

    # for compatibility
    y = (w + 1) * x

    return w, x, y, z


def test_part1():
    assert (
        monad_reverse_engineered(np.array([9, 2, 9, 6, 7, 6, 9, 9, 9, 4, 9, 8, 9, 1, 9]))[-1]
        == 0
    )


def test_part2():
    assert (
        monad_reverse_engineered(np.array([9, 1, 4, 1, 1, 1, 4, 3, 6, 1, 2, 1, 8, 1, 4]))[-1]
        == 0
    )


def test_monad_reverse_engineered():
    monad = compile_code(DATA)
    for _ in range(10000):
        inp = np.random.randint(1, 10, 14)
        assert monad(inp) == monad_reverse_engineered(inp)
