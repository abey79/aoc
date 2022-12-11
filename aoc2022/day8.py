import aocd
import numpy as np

TEST_DATA = """30373
25512
65332
33549
35390"""
TEST_PART1_RESULT = 21
TEST_PART2_RESULT = 8


def part1(data: str):
    arr = np.array([[int(x) for x in line] for line in data.splitlines()])

    cnt = 0
    for j in range(1, arr.shape[0] - 1):
        for i in range(1, arr.shape[1] - 1):
            val = arr[j, i]
            left = arr[j, 0:i]
            right = arr[j, i + 1 :]
            top = arr[0:j, i]
            bottom = arr[j + 1 :, i]
            if any(i.max() < val for i in (left, right, top, bottom)):
                cnt += 1

    cnt += 2 * arr.shape[0] + 2 * arr.shape[1] - 4
    return cnt


def count_tree(arr: np.ndarray) -> int:
    (tall_tree,) = np.where(arr)
    if len(tall_tree) == 0:
        return len(arr)
    else:
        return tall_tree[0] + 1


def part2(data: str):
    arr = np.array([[int(x) for x in line] for line in data.splitlines()])
    res = np.zeros_like(arr)

    for j in range(1, arr.shape[0] - 1):
        for i in range(1, arr.shape[1] - 1):
            val = arr[j, i]
            left = np.flip(arr[j, 0:i]) >= val
            right = arr[j, i + 1 :] >= val
            top = np.flip(arr[0:j, i]) >= val
            bottom = arr[j + 1 :, i] >= val

            res[j, i] = (
                count_tree(left) * count_tree(right) * count_tree(top) * count_tree(bottom)
            )

    return np.max(res)


def test_part1():
    if TEST_PART1_RESULT is not None:
        assert part1(TEST_DATA) == TEST_PART1_RESULT


def test_part2():
    if TEST_PART2_RESULT is not None:
        assert part2(TEST_DATA) == TEST_PART2_RESULT


def main() -> None:
    data = aocd.get_data(day=8, year=2022)
    print("Running for day 8 of year 2022")
    print("Part 1 solution:", part1(data))
    print("Part 2 solution:", part2(data))


if __name__ == "__main__":
    main()
