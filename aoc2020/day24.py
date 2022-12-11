from collections import defaultdict
from typing import Dict, Tuple

import aocd
import numpy as np

TEST_DATA = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew"""

COORD_TO_TUPLE = {
    "e": (1, 0),
    "w": (-1, 0),
    "A": (0, 1),
    "B": (-1, 1),
    "C": (0, -1),
    "D": (1, -1),
}


def calc_coords(path: str) -> Tuple[int, int]:
    # e, se, sw, w, nw, ne
    # e, A,  B,  w, C,  D

    path = path.replace("se", "A").replace("sw", "B").replace("nw", "C").replace("ne", "D")

    x, y = 0, 0
    for c in path:
        offset = COORD_TO_TUPLE[c]
        x += offset[0]
        y += offset[1]

    return x, y


def test_calc_coords():
    assert calc_coords("nwwswee") == (0, 0)


def load_tiles(data: str) -> Dict[Tuple[int, int], bool]:
    tiles = defaultdict(lambda: False)

    for path in data.splitlines():
        coord = calc_coords(path)
        tiles[coord] = not tiles[coord]

    return tiles


def day24_part1(data: str) -> int:
    tiles = load_tiles(data)
    return sum(tiles.values())


def test_day24_part1():
    assert day24_part1(TEST_DATA) == 10


def day24_part2(data: str) -> int:
    tiles = load_tiles(data)
    x_coords = [tile[0] for tile, flipped in tiles.items() if flipped]
    y_coords = [tile[1] for tile, flipped in tiles.items() if flipped]
    span_x = abs(max(x_coords, key=lambda x: abs(x)))
    span_y = abs(max(y_coords, key=lambda x: abs(x)))
    span = max(span_x, span_y) + 2 * 100 + 6
    hspan = round(span / 2)
    floor = np.zeros(shape=(span, span), dtype=bool)
    for tile, flipped in tiles.items():
        floor[hspan + tile[0], hspan + tile[1]] = flipped

    for _ in range(100):
        padded_floor = np.pad(floor, 1)
        neighbors = np.stack(
            [
                padded_floor[2:, 1:-1],
                padded_floor[:-2, 1:-1],
                padded_floor[1:-1, 2:],
                padded_floor[1:-1, :-2],
                padded_floor[:-2, 2:],
                padded_floor[2:, :-2],
            ],
            axis=2,
        ).sum(axis=2)

        new_floor = floor.copy()
        new_floor[floor & ((neighbors == 0) | (neighbors > 2))] = False
        new_floor[~floor & (neighbors == 2)] = True
        floor = new_floor

    return floor.sum()


def test_day24_part2():
    assert day24_part2(TEST_DATA) == 2208


def main():
    print(f"day 24 part 1: {day24_part1(aocd.get_data(day=24, year=2020))}")
    print(f"day 24 part 2: {day24_part2(aocd.get_data(day=24, year=2020))}")


if __name__ == "__main__":
    main()
