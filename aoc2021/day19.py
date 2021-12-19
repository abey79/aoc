import hashlib
import itertools
import pickle
import sys
from pathlib import Path
from typing import Any, Callable, Dict, Set, Tuple

import aocd
import multiprocess
import networkx as nx
import numpy as np
from rich.console import Console
from rich.traceback import install

install(show_locals=True)
console = Console()

DAY = int("".join(s for s in Path(__file__).name if s.isdigit()))
# noinspection SpellCheckingInspection
TEST_DATA: str = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""
TEST_RESULT_PART1: int | None = 79
TEST_RESULT_PART2: int | None = 3621


def read_data(data: str) -> [np.ndarray]:
    return [
        np.array([np.fromstring(line, sep=",") for line in block.splitlines()[1:]], dtype=int)
        for block in data.split("\n\n")
    ]


def compute_permutations():
    # brainless way to compute all permutations
    perm_x = {
        (1, 2, 3),
        (1, -3, 2),
        (1, -2, -3),
        (1, 3, -2),
    }

    perm_xy = set()
    for p in perm_x:
        perm_xy |= {
            p,
            (-p[2], p[1], p[0]),
            (-p[0], p[1], -p[2]),
            (p[2], p[1], -p[0]),
        }

    perm_xyz = set()
    for p in perm_xy:
        perm_xyz |= {
            p,
            (-p[1], p[0], p[2]),
            (-p[0], -p[1], p[2]),
            (p[1], -p[0], p[2]),
        }

    assert len(perm_xyz) == 24
    return perm_xyz


PERMS = compute_permutations()


def block_to_set(b: np.ndarray) -> Set[Tuple[int, int, int]]:
    return set(tuple(x) for x in b)


def find_offset(block0: np.ndarray, block1: np.ndarray) -> Tuple[int, int, int] | None:
    """returns corrected block1 in block0 space if match"""
    s0 = block_to_set(block0)
    for p0, p1 in itertools.product(block0, block1):
        offset = p1 - p0
        if len(s0.intersection(block_to_set(block1 - offset))) >= 12:
            return tuple(offset)
    return None


def permute_axes(block: np.ndarray, perm: (int, int, int)) -> np.ndarray:
    b = np.empty_like(block)
    b[:, 0] = block[:, abs(perm[0]) - 1] * np.sign(perm[0])
    b[:, 1] = block[:, abs(perm[1]) - 1] * np.sign(perm[1])
    b[:, 2] = block[:, abs(perm[2]) - 1] * np.sign(perm[2])
    return b


def find_transform(
    block0: np.ndarray, block1: np.ndarray
) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]] | None:
    # find transform and offset for block1 to match block0
    for perm in PERMS:
        offsets = find_offset(block0, permute_axes(block1, perm))
        if offsets is not None:
            return perm, offsets
    return None


def merge_block_to_set(block: np.ndarray, s: Set[Tuple[int, int, int]]) -> None:
    for i in range(block.shape[0]):
        s.add(block[i, :])


def compute_matches(blocks: [np.ndarray], data: str) -> Dict[Tuple[int, int], Any]:
    file = Path(f"/tmp/day_19_{hashlib.md5(data.encode()).hexdigest()}.pickle")
    if file.exists():
        matches = pickle.loads(file.read_bytes())
    else:
        matches = {}
        with multiprocess.Pool() as pool:
            for (i, j), res in pool.imap(
                lambda p: (p, find_transform(blocks[p[0]], blocks[p[1]])),
                itertools.permutations(range(len(blocks)), 2),
            ):
                if res is not None:
                    perm, offsets = res
                    print(
                        f"match found between blocks {i} and {j}: perm={perm}, "
                        f"offsets={offsets}"
                    )
                    matches[(i, j)] = (perm, offsets)

        file.write_bytes(pickle.dumps(matches))

    return matches


def part1(data: str) -> int:
    blocks = read_data(data)
    matches = compute_matches(blocks, data)
    graph = nx.Graph()

    for i, j in matches:
        graph.add_edge(i, j)

    # from matplotlib import pyplot as plt
    # plt.figure()
    # nx.draw(graph, with_labels=True)
    # plt.show()

    beacons = block_to_set(blocks[0])

    for n in range(1, len(blocks)):
        path = nx.shortest_path(graph, n, 0)

        corrected_block = blocks[n]
        for j, i in itertools.pairwise(path):
            perm, offsets = matches[(i, j)]
            corrected_block = permute_axes(corrected_block, perm) - offsets

        beacons |= block_to_set(corrected_block)

    return len(beacons)


def part2(data: str) -> int:
    blocks = read_data(data)
    matches = compute_matches(blocks, data)
    graph = nx.Graph()

    for i, j in matches:
        graph.add_edge(i, j)

    max_dist = 0
    for n1, n2 in itertools.combinations(range(len(blocks)), 2):
        path = nx.shortest_path(graph, n1, n2)
        off = np.zeros(3, dtype=int)
        for j, i in itertools.pairwise(path):
            perm, offsets = matches[(i, j)]
            off = np.array(
                [
                    off[abs(perm[0]) - 1] * np.sign(perm[0]),
                    off[abs(perm[1]) - 1] * np.sign(perm[1]),
                    off[abs(perm[2]) - 1] * np.sign(perm[2]),
                ]
            )
            off += np.array(offsets, dtype=int)

        dist = np.sum(np.abs(off))
        if dist > max_dist:
            max_dist = dist

    return max_dist


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

    result = solution(aocd.get_data(day=DAY, year=2021), *args, **kwargs)
    console.print(f"{name.capitalize()} solution: {result}", style="blue")


def main() -> None:
    console.print(f"Running for day {DAY}", style="blue")
    run_solution("part 1", run_test_part1, part1)
    run_solution("part 2", run_test_part2, part2)


if __name__ == "__main__":
    main()
