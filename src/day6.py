import math

from . import get_input_data

TEST_DATA = """Time:      7  15   30
Distance:  9  40  200"""


def sqrtEqCalc(time: int, dist: int) -> int:
    # -x2 + time*x - dist = 1
    # -b ± sqrt(b2 - 4*a*c) / 2a
    a = math.ceil((-time + math.sqrt(time**2 - 4*(dist+1))) / (-2))
    b = math.floor((-time - math.sqrt(time**2 - 4*(dist+1))) / (-2))

    return b - a + 1


def solve(data: list[str]):
    _times, _dists = [y[1:] for y in [x.split() for x in data]]
    races = list(zip([int(x) for x in _times], [int(x) for x in _dists]))

    total = 1
    for (time, dist) in races:
        total *= sqrtEqCalc(time, dist)

    print (f"Day 6, Step 1: {total}")


def solve2(data: list[str]):
    time, dist = [int(y[1].replace(" ", "")) for y in [x.split(":") for x in data]]

    tries = sqrtEqCalc(time, dist)
    print (f"Day 6, Step 2: {tries}")


if __name__ == "__main__":
    test = TEST_DATA.split("\n")
    data = get_input_data(6)

    solve(data)
    solve2(data)
