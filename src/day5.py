from itertools import groupby

from . import get_input_data

TEST_DATA = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


class Range:
    start = None
    end = None

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def has(self, val: "Range") -> bool:
        return self.start <= val.start and val.end <= self.end

    def __add__(self, val: int) -> "Range":
        return Range(self.start + val, self.end + val)

    def __sub__(self, val: int) -> "Range":
        return self + (-val)

    def intersect(self, val: "Range") -> bool:
        return val.start <= self.start <= val.end or val.start <= self.end <= val.end

    def __str__(self):
        return f"R<{self.start}-{self.end}>"
    __repr__ = __str__


def performStepRange(seed: Range, rulebook: list[tuple[Range, tuple]]) -> list[Range]:
    step = seed

    rulebook.sort(key = lambda x: x[0].start)
    # print (f"Rulebook: {[x[0] for x in rulebook]}")
    new_steps = []

    # print (f"-> from step {step}")
    step_consumed = False
    for rule, (_from, _to) in rulebook:
        if step.start < rule.start:
            if step.end < rule.start:
                # print (f"Step {step} ends before the rule {rule}, added it")
                new_steps.append(step)
                # step = Range(step.end, step.end)
                step_consumed = True
                break
            else:
                new_steps.append(Range(step.start, rule.start - 1))
                step = Range(rule.start, step.end)

        if rule.has(step):
            new_steps.append(step - _from + _to)
            # print (f"rule {rule} has step {step}, produces {step - _from + _to}")
            step_consumed = True
            break

        elif rule.intersect(step):
            new_steps.append(Range(step.start, rule.end) - _from + _to)
            # print (f"rule {rule} intersects step {step}, produces {Range(step.start, rule.end) - _from + _to} (from {(step.start, rule.end)})")
            step = Range(rule.end + 1, step.end)

    if not step_consumed:
        # print (f"Final step: {step}")
        new_steps.append(step)

    return new_steps


def solve(data: list[str]):
    rulebooks = [list(g) for k, g in groupby(data, key=lambda x: x == '') if not k]

    _seeds, rulebooks = rulebooks[0], rulebooks[1:]
    rulebooks = [x[1:] for x in rulebooks]
    rulebooks = [[[int(x) for x in j.split()] for j in k] for k in rulebooks]

    # every rule is (Range<x, y>, (from_src, to_dest))
    rulebooks = [
        [(Range(src, src + length - 1), (src, dest))
         for (dest, src, length) in x] for x in rulebooks]

    # Step 1: every seed is a number, or Range with the start equal to end
    _seeds = [int(x) for x in _seeds[0].split(": ")[1].split()]
    steps = [Range(x, x) for x in _seeds]
    for rulebook in rulebooks:
        steps = sum([performStepRange(step, rulebook) for step in steps], [])

    print (f"Day 5, Step 1: {min((x.start for x in steps))}")

    # Step 2: every pair of numbers in seeds is a range
    seeds = []
    for idx in range(0, len(_seeds), 2):
        seeds.append(Range(_seeds[idx], _seeds[idx] + _seeds[idx+1] - 1))

    steps = seeds
    for rulebook in rulebooks:
        steps = sum([performStepRange(step, rulebook) for step in steps], [])

    print (f"Day 5, Step 2: {min((x.start for x in steps))}")


if __name__ == "__main__":
    data = get_input_data(5)
    test = TEST_DATA.split("\n")

    solve(data)