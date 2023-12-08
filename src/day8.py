import re
from itertools import groupby
from math import lcm
from typing import Generator

from . import get_input_data

TEST_DATA1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

TEST_DATA2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""


TEST_DATA3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def solve(data: list[str]):
    points = [list(g) for k, g in groupby(data, key=lambda x: x == '') if not k]

    turns, points = list(points[0][0]), points[1]

    def make_turner() -> Generator[str, None, None]:
        def get_next_turn() -> str:
            idx = 0
            while True:
                yield turns[idx]
                idx += 1
                if idx == len(turns):
                    idx = 0

        return get_next_turn

    points = [x.split(" = ") for x in points]
    points = {x[0]: re.findall("[0-9A-Z]{3}", x[1]) for x in points}

    # print (points)

    def perform_steps(start: str) -> int:
        steps = 0
        next_point = start
        next_turn = make_turner()
        for turn in next_turn():
            next_point = points[next_point][0 if turn == 'L' else 1]
            steps += 1

            if next_point.endswith('Z'):
                break

        return steps

    steps = perform_steps('AAA')
    print (f"Day 8, Step 1: {steps}")

    loops = []
    for start in [x for x in points if x.endswith('A')]:
        loops.append(perform_steps(start))

    print (f"Day 8, Step 2: {lcm(*loops)}")


if __name__ == "__main__":
    test1 = TEST_DATA1.split("\n")
    test2 = TEST_DATA2.split("\n")
    test3 = TEST_DATA3.split("\n")

    data = get_input_data(8)

    solve(data)