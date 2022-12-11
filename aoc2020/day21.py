import copy
from collections import defaultdict
from typing import DefaultDict, Dict, List, Set, Tuple

import aocd

TEST_DATA = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
"""

FoodsType = List[Set[str]]
AllergensType = Dict[str, List[int]]


def parse(data: str) -> Tuple[FoodsType, AllergensType]:
    foods = []
    allergens: DefaultDict[str, List[int]] = defaultdict(list)
    for i, line in enumerate(data.splitlines()):
        s1, s2 = line.split(" (contains ")
        foods.append(set(s1.split()))
        for allergen in s2.strip(")").split(", "):
            allergens[allergen].append(i)

    return foods, allergens


def day21_part1(foods: FoodsType, allergens: AllergensType) -> int:
    for allergen, indices in allergens.items():
        itrsct = set.intersection(*[foods[idx] for idx in indices])
        for ingredient in itrsct:
            for food in foods:
                food.discard(ingredient)

    return sum(len(food) for food in foods)


def test_day21_part1():
    foods, allergens = parse(TEST_DATA)
    assert day21_part1(foods, allergens) == 5


def day21_part2(foods: FoodsType, allergens: AllergensType) -> str:
    matches = {}
    while True:
        new_allergens = {}
        for allergen, indices in allergens.items():
            itrsct = set.intersection(*[foods[idx] for idx in indices])
            if len(itrsct) == 1:
                ingredient = list(itrsct)[0]
                matches[allergen] = ingredient
                for food in foods:
                    food.discard(ingredient)
            else:
                new_allergens[allergen] = indices
        allergens = new_allergens
        if len(new_allergens) == 0:
            break

    return ",".join(matches[allergen] for allergen in sorted(matches))


def test_day21_part2():
    foods, allergens = parse(TEST_DATA)
    assert day21_part2(foods, allergens) == "mxmxvkd,sqjhc,fvjkl"


def main():
    foods, allergens = parse(aocd.get_data(day=21, year=2020))
    print(f"day 21 part 1: {day21_part1(copy.deepcopy(foods), copy.deepcopy(allergens))}")
    print(f"day 21 part 2: {day21_part2(foods, allergens)}")


if __name__ == "__main__":
    main()
