import itertools
from collections import Counter

import aocd
import numpy as np
from scipy.signal import convolve


def update_world(world: np.ndarray) -> np.ndarray:
    padded_world = np.pad(world, pad_width=1)
    slices = [slice(2, None), slice(1, -1), slice(0, -2)]

    summed_world = np.zeros(shape=world.shape)
    for ss in itertools.product(*([slices] * world.ndim)):
        if all(s == slice(1, -1) for s in ss):
            continue
        summed_world += padded_world[ss]

    return np.where(world, (summed_world == 2) | (summed_world == 3), summed_world == 3)


def day17(data: str, niter: int, ndim: int) -> int:
    seed = np.array([[c == "#" for c in line] for line in data.split("\n")], dtype=bool)

    world = np.pad(np.expand_dims(seed, axis=tuple(range(2, ndim))), pad_width=niter)
    for _ in range(niter):
        world = update_world(world)
    return world.sum()


def test_day17():
    data = ".#.\n..#\n###"
    assert day17(data, 6, 3) == 112
    assert day17(data, 6, 4) == 848


def main():
    print(f"day 17 part 1: {day17(aocd.get_data(day=17, year=2020), 6, 3)}")
    print(f"day 17 part 2: {day17(aocd.get_data(day=17, year=2020), 6, 4)}")


if __name__ == "__main__":
    main()


def day17_pure_python_u_leijurv(data, dims):

    neighbors = [()]
    for x in range(dims):
        neighbors = [x + (i,) for i in [-1, 0, 1] for x in neighbors]
    neighbors.remove(dims * (0,))

    state = set(
        (dims - 2) * (0,) + (i, j)
        for i, v in enumerate(data.splitlines())
        for j, v in enumerate(v)
        if v == "#"
    )

    for i in range(6):
        state = set(
            pos
            for pos, cnt in Counter(
                tuple(map(sum, zip(pos, n))) for pos in state for n in neighbors
            ).items()
            if cnt == 3 or pos in state and cnt == 2
        )

    return len(state)


def test_day17_pure_python_u_leijurv():
    data = ".#.\n..#\n###"
    assert day17_pure_python_u_leijurv(data, 3) == 112
    assert day17_pure_python_u_leijurv(data, 4) == 848


def day17_part2_scipy_u_wimglenn(data):
    def evolve(A, n=6):
        kernel = np.ones((3,) * A.ndim, dtype=A.dtype)
        kernel[(1,) * A.ndim] = 0  # hollow center
        for _ in range(n):
            C = convolve(A, kernel)
            A = np.pad(A, pad_width=1)
            A = ((A == 1) & ((C == 2) | (C == 3))) | ((A == 0) & (C == 3))
            A = A.astype(int)
        return A

    A0 = (np.array([[*r] for r in data.splitlines()]) == "#").astype(int)
    return evolve(A0[..., None, None]).sum()


def test_day17_part2_scipy_u_wimglenn():
    data = ".#.\n..#\n###"
    assert day17_part2_scipy_u_wimglenn(data) == 848
