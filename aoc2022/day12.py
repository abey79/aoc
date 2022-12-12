import aocd
import numpy as np

TEST_DATA = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""
TEST_PART1_RESULT = 31
TEST_PART2_RESULT = 29


def altitude(letter: str) -> int:
    if letter == "S":
        letter = "a"
    elif letter == "E":
        letter = "z"
    return ord(letter) - ord("a")


def part1(data: str):
    map = np.array([list(line) for line in data.splitlines()])
    dist_map = -np.ones_like(map, dtype=int)

    end_j, end_i = np.where(map == "E")
    (start_j,), (start_i,) = np.where(map == "S")
    dist_map[end_j, end_i] = 0

    cur_dist = 0
    while True:
        idx_j, idx_i = np.where(dist_map == cur_dist)

        for i, j in zip(idx_i, idx_j):
            assert dist_map[j, i] == cur_dist

            # inspect adjacent cells
            cur_alt = altitude(map[j, i])
            for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if (
                    0 <= i + di < map.shape[1]
                    and 0 <= j + dj < map.shape[0]
                    and dist_map[j + dj, i + di] == -1
                ):
                    alt = altitude(map[j + dj, i + di])
                    if alt >= cur_alt - 1:
                        dist_map[j + dj, i + di] = cur_dist + 1
                        if (i + di) == start_i and (j + dj) == start_j:
                            return cur_dist + 1

        cur_dist += 1


def part2(data: str):
    map = np.array([list(line) for line in data.splitlines()])
    dist_map = -np.ones_like(map, dtype=int)

    end_j, end_i = np.where(map == "E")
    (start_j,), (start_i,) = np.where(map == "S")
    dist_map[end_j, end_i] = 0

    cur_dist = 0
    while True:
        idx_j, idx_i = np.where(dist_map == cur_dist)

        if len(idx_j) == 0:
            assert len(idx_i) == 0
            break

        for i, j in zip(idx_i, idx_j):
            assert dist_map[j, i] == cur_dist

            # inspect adjacent cells
            cur_alt = altitude(map[j, i])
            for di, dj in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                if (
                    0 <= i + di < map.shape[1]
                    and 0 <= j + dj < map.shape[0]
                    and dist_map[j + dj, i + di] == -1
                ):
                    alt = altitude(map[j + dj, i + di])
                    if alt >= cur_alt - 1:
                        dist_map[j + dj, i + di] = cur_dist + 1

        cur_dist += 1

    candidates_j, candidates_i = np.where(((map == "a") | (map == "S")) & (dist_map != -1))
    return np.min(dist_map[candidates_j, candidates_i])


def test_part1():
    if TEST_PART1_RESULT is not None:
        assert part1(TEST_DATA) == TEST_PART1_RESULT


def test_part2():
    if TEST_PART2_RESULT is not None:
        assert part2(TEST_DATA) == TEST_PART2_RESULT


def main() -> None:
    data = aocd.get_data(day=12, year=2022)
    print("Running for day 12 of year 2022")
    print("Part 1 solution:", part1(data))
    print("Part 2 solution:", part2(data))


if __name__ == "__main__":
    main()
