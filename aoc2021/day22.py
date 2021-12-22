import dataclasses
import itertools
import sys
import time
from pathlib import Path
from typing import Callable, Optional

import aocd
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
# noinspection SpellCheckingInspection
TEST_DATA: str = """on x=-5..47,y=-31..22,z=-19..33
on x=-44..5,y=-27..21,z=-14..35
on x=-49..-1,y=-11..42,z=-10..38
on x=-20..34,y=-40..6,z=-44..1
off x=26..39,y=40..50,z=-2..11
on x=-41..5,y=-41..6,z=-36..8
off x=-43..-33,y=-45..-28,z=7..25
on x=-33..15,y=-32..19,z=-34..11
off x=35..47,y=-46..-34,z=-11..5
on x=-14..36,y=-6..44,z=-16..29
on x=-57795..-6158,y=29564..72030,z=20435..90618
on x=36731..105352,y=-21140..28532,z=16094..90401
on x=30999..107136,y=-53464..15513,z=8553..71215
on x=13528..83982,y=-99403..-27377,z=-24141..23996
on x=-72682..-12347,y=18159..111354,z=7391..80950
on x=-1060..80757,y=-65301..-20884,z=-103788..-16709
on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856
on x=-52752..22273,y=-49450..9096,z=54442..119054
on x=-29982..40483,y=-108474..-28371,z=-24328..38471
on x=-4958..62750,y=40422..118853,z=-7672..65583
on x=55694..108686,y=-43367..46958,z=-26781..48729
on x=-98497..-18186,y=-63569..3412,z=1232..88485
on x=-726..56291,y=-62629..13224,z=18033..85226
on x=-110886..-34664,y=-81338..-8658,z=8914..63723
on x=-55829..24974,y=-16897..54165,z=-121762..-28058
on x=-65152..-11147,y=22489..91432,z=-58782..1780
on x=-120100..-32970,y=-46592..27473,z=-11695..61039
on x=-18631..37533,y=-124565..-50804,z=-35667..28308
on x=-57817..18248,y=49321..117703,z=5745..55881
on x=14781..98692,y=-1341..70827,z=15753..70151
on x=-34419..55919,y=-19626..40991,z=39015..114138
on x=-60785..11593,y=-56135..2999,z=-95368..-26915
on x=-32178..58085,y=17647..101866,z=-91405..-8878
on x=-53655..12091,y=50097..105568,z=-75335..-4862
on x=-111166..-40997,y=-71714..2688,z=5609..50954
on x=-16602..70118,y=-98693..-44401,z=5197..76897
on x=16383..101554,y=4615..83635,z=-44907..18747
off x=-95822..-15171,y=-19987..48940,z=10804..104439
on x=-89813..-14614,y=16069..88491,z=-3297..45228
on x=41075..99376,y=-20427..49978,z=-52012..13762
on x=-21330..50085,y=-17944..62733,z=-112280..-30197
on x=-16478..35915,y=36008..118594,z=-7885..47086
off x=-98156..-27851,y=-49952..43171,z=-99005..-8456
off x=2032..69770,y=-71013..4824,z=7471..94418
on x=43670..120875,y=-42068..12382,z=-24787..38892
off x=37514..111226,y=-45862..25743,z=-16714..54663
off x=25699..97951,y=-30668..59918,z=-15349..69697
off x=-44271..17935,y=-9516..60759,z=49131..112598
on x=-61695..-5813,y=40978..94975,z=8655..80240
off x=-101086..-9439,y=-7088..67543,z=33935..83858
off x=18020..114017,y=-48931..32606,z=21474..89843
off x=-77139..10506,y=-89994..-18797,z=-80..59318
off x=8476..79288,y=-75520..11602,z=-96624..-24783
on x=-47488..-1262,y=24338..100707,z=16292..72967
off x=-84341..13987,y=2429..92914,z=-90671..-1318
off x=-37810..49457,y=-71013..-7894,z=-105357..-13188
off x=-27365..46395,y=31009..98017,z=15428..76570
off x=-70369..-16548,y=22648..78696,z=-1892..86821
on x=-53470..21291,y=-120233..-33476,z=-44150..38147
off x=-93533..-4276,y=-16170..68771,z=-104985..-24507"""
TEST_RESULT_PART1: int | None = 474140
TEST_RESULT_PART2: int | None = 2758514936282235


@dataclasses.dataclass(frozen=True)
class Range:
    min: int
    max: int

    @classmethod
    def from_string(cls, s: str) -> "Range":
        return cls(*[int(val) for val in s.split("..")])

    def count(self) -> int:
        return self.max + 1 - self.min

    def intersects(self, other: "Range") -> bool:
        return (
            self.min <= other.min <= self.max
            or self.min <= other.max <= self.max
            or (other.min <= self.min and other.max >= self.max)
        )

    def intersection(self, other: "Range") -> Optional["Range"]:
        if not self.intersects(other):
            return None

        return Range(max(self.min, other.min), min(self.max, other.max))

    def __and__(self, other: "Range") -> Optional["Range"]:
        return self.intersection(other)

    def difference(self, other: "Range") -> ["Range"]:
        if not self.intersects(other):
            return self
        elif other.min <= self.min and other.max >= self.max:
            return []
        elif other.min > self.min and other.max < self.max:
            return [Range(self.min, other.min - 1), Range(other.max + 1, self.max)]
        elif other.min <= self.min:
            return [Range(other.max + 1, self.max)]
        else:
            return [Range(self.min, other.min - 1)]

    def __sub__(self, other: "Range") -> ["Range"]:
        return self.difference(other)


@dataclasses.dataclass(frozen=True)
class Cube:
    x: Range
    y: Range
    z: Range

    @classmethod
    def from_string(cls, s: str) -> "Cube":
        ranges = [Range.from_string(r.split("=")[1]) for r in s.split(",")]
        return cls(*ranges)

    @classmethod
    def from_coord(cls, x1: int, x2: int, y1: int, y2: int, z1: int, z2: int) -> "Cube":
        return cls(Range(x1, x2), Range(y1, y2), Range(z1, z2))

    def count(self) -> int:
        return self.x.count() * self.y.count() * self.z.count()

    def intersects(self, other: "Cube") -> bool:
        return (
            self.x.intersects(other.x)
            and self.y.intersects(other.y)
            and self.z.intersects(other.z)
        )

    def difference(self, other: "Cube") -> ["Cube"]:
        if not self.intersects(other):
            return [self]

        xi = self.x & other.x
        yi = self.y & other.y
        zi = self.z & other.z
        xd = self.x - other.x
        yd = self.y - other.y
        zd = self.z - other.z

        res = []
        for x, y, z in itertools.product((xi, *xd), (yi, *yd), (zi, *zd)):
            assert x is not None and y is not None and z is not None

            if x == xi and y == yi and z == zi:
                continue

            res.append(Cube(x, y, z))

        return res

    def __sub__(self, other: "Cube") -> ["Cube"]:
        return self.difference(other)

    def crop(self, low: int, high: int) -> Optional["Cube"]:
        r = Range(low, high)
        if self.x.intersects(r) and self.y.intersects(r) and self.z.intersects(r):
            return Cube(
                Range(max(self.x.min, low), min(self.x.max, high)),
                Range(max(self.y.min, low), min(self.y.max, high)),
                Range(max(self.z.min, low), min(self.z.max, high)),
            )
        else:
            return None


def part1(data: str) -> int:
    all_cubes = []

    for line in data.splitlines():
        onoff, cube_str = line.split(" ")
        new_cube = Cube.from_string(cube_str).crop(-50, 50)
        if new_cube is None:
            continue

        if onoff == "on":
            # diff all exising cubes from cube
            new_cubes = [new_cube]

            for cube in all_cubes:
                new_cubes = sum((c - cube for c in new_cubes), [])

            all_cubes.extend(new_cubes)
        else:
            all_cubes = sum((cube - new_cube for cube in all_cubes), [])

    return sum(cube.count() for cube in all_cubes)


def part2(data: str) -> int:
    all_cubes = []

    for line in data.splitlines():
        onoff, cube_str = line.split(" ")
        new_cube = Cube.from_string(cube_str)

        if onoff == "on":
            # diff all exising cubes from cube
            new_cubes = [new_cube]

            for cube in all_cubes:
                new_cubes = sum((c - cube for c in new_cubes), [])

            all_cubes.extend(new_cubes)
        else:
            all_cubes = sum((cube - new_cube for cube in all_cubes), [])

    return sum(cube.count() for cube in all_cubes)


def test_range():
    assert Range.from_string("50..60") == Range(50, 60)
    assert Range(-10, 40).intersects(Range(40, 43))
    assert not Range(-10, 40).intersects(Range(41, 43))
    assert Range(-10, 40).intersects(Range(-20, -8))
    assert Range(-10, 40).intersects(Range(-20, -10))
    assert not Range(-10, 40).intersects(Range(-20, -11))
    assert Range(50, 60).intersects(Range(49, 61))
    assert Range(50, 60) & Range(55, 70) == Range(55, 60)
    assert Range(0, 10) & Range(12, 20) is None
    assert Range(50, 60) & Range(10, 50) == Range(50, 50)
    assert Range(50, 60) - Range(55, 60) == [Range(50, 54)]
    assert Range(50, 60) - Range(0, 50) == [Range(51, 60)]
    assert Range(50, 60) - Range(0, 55) == [Range(56, 60)]
    assert Range(50, 60) - Range(50, 60) == []
    assert Range(50, 60) - Range(49, 60) == []
    assert Range(50, 60) - Range(50, 61) == []
    assert Range(50, 60) - Range(49, 61) == []
    assert set(Range(0, 10) - Range(5, 7)) == {Range(0, 4), Range(8, 10)}
    assert Range(50, 50).count() == 1
    assert Range(50, 60).count() == 11


def test_cube():
    assert (
        Cube.from_coord(0, 10, 0, 10, 0, 10) - Cube.from_coord(-10, 20, -10, 20, -10, 20) == []
    )
    assert Cube.from_coord(0, 10, 0, 10, 0, 10) - Cube.from_coord(0, 10, 0, 10, 0, 10) == []
    assert Cube.from_coord(0, 10, 0, 10, 0, 10) - Cube.from_coord(0, 10, 0, 10, 0, 5) == [
        Cube.from_coord(0, 10, 0, 10, 6, 10)
    ]
    assert set(Cube.from_coord(0, 10, 0, 10, 0, 10) - Cube.from_coord(0, 10, 0, 10, 5, 6)) == {
        Cube.from_coord(0, 10, 0, 10, 7, 10),
        Cube.from_coord(0, 10, 0, 10, 0, 4),
    }
    assert set(
        Cube.from_coord(0, 10, 0, 10, 0, 10) - Cube.from_coord(8, 20, 8, 20, 8, 20)
    ) == {
        Cube.from_coord(0, 7, 0, 7, 0, 7),
        Cube.from_coord(0, 7, 0, 7, 8, 10),
        Cube.from_coord(0, 7, 8, 10, 0, 7),
        Cube.from_coord(8, 10, 0, 7, 0, 7),
        Cube.from_coord(8, 10, 8, 10, 0, 7),
        Cube.from_coord(8, 10, 0, 7, 8, 10),
        Cube.from_coord(0, 7, 8, 10, 8, 10),
    }


def run_test_part1(*args, **kwargs):
    if TEST_RESULT_PART1 is None:
        raise NotImplementedError
    # noinspection PyArgumentList
    assert part1(TEST_DATA, *args, **kwargs) == TEST_RESULT_PART1


def run_test_part2(*args, **kwargs):
    if TEST_RESULT_PART2 is None:
        raise NotImplementedError
    # noinspection PyArgumentList
    assert part2(TEST_DATA, *args, **kwargs) == TEST_RESULT_PART2


def run_solution(name: str, test_func: Callable, solution: Callable, *args, **kwargs):
    proceed = True
    try:
        test_func(*args, **kwargs)
        console.print(f"Test {name} succeeded.", style="green")
    except NotImplementedError:
        console.print(f"Test {name} not implemented", style="yellow")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]
    except AssertionError:
        console.print(f"Test {name} failed", style="red")
        proceed = console.input("Proceed? ").lower() in ["y", "yes"]

    if not proceed:
        sys.exit()
    data = aocd.get_data(day=DAY, year=2021)
    start_time = time.time()
    result = solution(data, *args, **kwargs)
    delta = time.time() - start_time
    console.print(
        f"{name.capitalize()} solution: {result} (execution time: {delta*1000:.2f}ms)",
        style="blue",
    )


def main() -> None:
    console.print(f"Running for day {DAY}", style="blue")
    run_solution("part 1", run_test_part1, part1)
    run_solution("part 2", run_test_part2, part2)


if __name__ == "__main__":
    main()
