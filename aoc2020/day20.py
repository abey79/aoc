import re
from collections import Counter, defaultdict
from typing import Dict, List, Optional, Set, Tuple

import aocd
import numpy as np

TEST_DATA = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""

POW2 = 2 ** np.arange(10)

MONSTER_DATA = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """

MONSTER = np.array([[c == "#" for c in line] for line in MONSTER_DATA.splitlines()])


class Tile:
    @staticmethod
    def from_data(data: str) -> "Tile":
        lines = data.splitlines()
        res = re.match(r"Tile (\d+):", lines[0])
        tile_id = int(res.group(1))
        arr = np.array([[c == "#" for c in line] for line in lines[1:]])
        arr.flags.writeable = False
        return Tile(tile_id, arr)

    def __init__(self, tile_id: int, arr: np.ndarray):
        self.id = tile_id
        self.data = arr

        self.north = self.data[0, :].dot(POW2)
        self.east = self.data[:, -1].dot(POW2)
        self.south = self.data[-1, ::-1].dot(POW2)
        self.west = self.data[::-1, 0].dot(POW2)

        self.edges = (self.north, self.east, self.south, self.west)
        self.edges_r = (
            self.data[0, ::-1].dot(POW2),
            self.data[::-1, -1].dot(POW2),
            self.data[-1, :].dot(POW2),
            self.data[:, 0].dot(POW2),
        )

    def flip(self):
        return Tile(self.id, self.data[::-1, :])

    def rotate(self):
        return Tile(self.id, np.rot90(self.data))

    def __repr__(self):
        return f"Tile(id={self.id})"

    def __hash__(self):
        return hash(self.data.data.tobytes())


def parse(data: str) -> Tuple[Dict[int, Tile], Dict[int, List[Tuple[Tile, int]]]]:
    tile_map = {}
    edge_map = defaultdict(list)
    for tile_data in data.split("\n\n"):
        tile = Tile.from_data(tile_data)
        tile_map[tile.id] = tile
        for i, edge in enumerate(tile.edges):
            edge_map[edge].append((tile, i, False))
        for i, edge in enumerate(tile.edges_r):
            edge_map[edge].append((tile, i, True))
    return tile_map, edge_map


def find_corners(edge_map):

    cnt = Counter()
    for tile_list in edge_map.values():
        if len(tile_list) == 1:
            cnt.update({tile_list[0][0].id: 1})

    res = []
    for k, v in cnt.items():
        if v == 4:
            res.append(k)
    return tuple(res)


def day20_part1(data: str) -> int:
    tile_map, edge_map = parse(data)
    res = find_corners(edge_map)
    assert len(res) == 4
    return res[0] * res[1] * res[2] * res[3]


def test_day20_part1():
    assert day20_part1(TEST_DATA) == 20899048083289


def find_edge(edge, tiles: Set[Tile]) -> Optional[Tile]:
    for tile in tiles:
        if edge in tile.edges:
            return tile
        if edge in tile.edges_r:
            return tile
    return None


def orient_tile(tile: Tile, edge: int, index: int) -> Tile:
    if edge not in tile.edges_r:
        tile = tile.flip()
    while tile.edges_r[index] != edge:
        tile = tile.rotate()
    return tile


def remove_monster(img: np.ndarray) -> np.ndarray:
    img = img.copy()
    di, dj = MONSTER.shape
    for i in range(img.shape[0] - di):
        for j in range(img.shape[1] - dj):
            if (img[i : i + di, j : j + dj] & MONSTER).sum() == MONSTER.sum():
                img[i : i + di, j : j + dj] = img[i : i + di, j : j + dj] & (~MONSTER)
    return img


def day20_part2(data: str, n: int) -> int:
    tile_map, edge_map = parse(data)
    seed_id, _, _, _ = find_corners(edge_map)
    seed = tile_map[seed_id]

    tile_set = set(tile_map.values())
    tile_set.discard(seed)

    # orient seed tile
    while (
        find_edge(seed.north, tile_set) is not None
        or find_edge(seed.west, tile_set) is not None
    ):
        seed = seed.rotate()

    # first line
    line = [seed]
    for _ in range(n - 1):
        edge = line[-1].east
        tile = find_edge(edge, tile_set)
        tile_set.discard(tile)
        tile = orient_tile(tile, edge, 3)
        assert find_edge(tile.north, tile_set) is None
        line.append(tile)

    image = [line]

    # all lines
    for _ in range(n - 1):
        edge = image[-1][0].south
        tile = find_edge(edge, tile_set)
        tile_set.discard(tile)
        tile = orient_tile(tile, edge, 0)

        line = [tile]
        for i in range(1, n):
            edge = line[-1].east
            tile = find_edge(edge, tile_set)
            tile_set.discard(tile)
            tile = orient_tile(tile, edge, 3)
            assert tile.north == image[-1][i].edges_r[2]
            line.append(tile)

        image.append(line)

    assert len(tile_set) == 0

    # build big image
    img = np.empty(shape=(n * 8, n * 8), dtype=bool)
    for i in range(n):
        for j in range(n):
            img[i * 8 : (i + 1) * 8, j * 8 : (j + 1) * 8] = image[i][j].data[1:-1, 1:-1]

    # find monster
    for _ in range(4):
        new_img = remove_monster(img)
        if not np.all(new_img == img):
            return new_img.sum()
        else:
            img = np.rot90(img)

    img = np.fliplr(img)

    for _ in range(4):
        new_img = remove_monster(img)
        if not np.all(new_img == img):
            return new_img.sum()
        else:
            img = np.rot90(img)

    assert False


def test_day20_part2():
    assert day20_part2(TEST_DATA, 3) == 273


def main():
    print(f"day 20 part 1: {day20_part1(aocd.get_data(day=20, year=2020))}")
    print(f"day 20 part 2: {day20_part2(aocd.get_data(day=20, year=2020), 12)}")


if __name__ == "__main__":
    main()
