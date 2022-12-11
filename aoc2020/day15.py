from collections import Counter


def day15_part1(data: str, rank: int) -> int:
    lst = [int(c) for c in data.split(",")]

    cnt = Counter(lst)
    last = {n: i for i, n in enumerate(lst)}
    prev_prev_last = 0

    for i in range(len(lst), rank):
        prev = lst[i - 1]
        if cnt[prev] == 1:
            curr = 0
        else:
            curr = i - 1 - prev_prev_last

        cnt.update([curr])
        if curr in last:
            prev_prev_last = last[curr]
        last[curr] = i
        lst.append(curr)

    return curr


def test_day15_part1():
    assert day15_part1("1,3,2", 2020) == 1
    assert day15_part1("2,1,3", 2020) == 10
    assert day15_part1("1,2,3", 2020) == 27
    assert day15_part1("2,3,1", 2020) == 78
    assert day15_part1("3,2,1", 2020) == 438
    assert day15_part1("3,1,2", 2020) == 1836


def main():
    data = "6,13,1,15,2,0"
    print(f"day 14 part 1: {day15_part1(data, 2020)}")
    print(f"day 14 part 2: {day15_part1(data, 30000000)}")


if __name__ == "__main__":
    main()
