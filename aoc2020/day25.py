CARD_PUB = 13135480
DOOR_PUB = 8821721


def find_loops(pub: int, sn: int = 7) -> int:
    cnt = 0
    val = 1
    while val != pub:
        val = (val * sn) % 20201227
        cnt += 1
    return cnt


def transform(loops: int, sn: int = 7) -> int:
    val = 1
    for _ in range(loops):
        val = (val * sn) % 20201227
    return val


def test_find_loops_transforms():
    assert find_loops(5764801) == 8
    assert transform(8) == 5764801

    for i in range(100):
        assert find_loops(transform(i)) == i


def test_encryption_key():
    n_card = find_loops(CARD_PUB)
    n_door = find_loops(DOOR_PUB)

    assert transform(n_card, DOOR_PUB) == transform(n_door, CARD_PUB)


def day25_part1() -> int:
    n_card = find_loops(CARD_PUB)
    n_door = find_loops(DOOR_PUB)

    key = transform(n_card, DOOR_PUB)
    assert key == transform(n_door, CARD_PUB)
    return key


def main():
    print(f"day 25 part 1: {day25_part1()}")
    # print(f"day 14 part 2: {day14_part2(aocd.get_data(day=14, year=2020))}")


if __name__ == "__main__":
    main()
