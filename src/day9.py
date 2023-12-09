from . import get_input_data

TEST_DATA = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""


def solve(data: list[str]):
    sensors = [[int(y) for y in x.split()] for x in data]

    def convert(row: list[int]) -> list[int]:
        if len(row) <= 1:
            return []

        return [(r - row[idx-1]) for (idx, r) in enumerate(row[1:], 1)]

    # calculate all triangles
    all_diffs = []
    for sensor in sensors:
        current = sensor[:]
        diffs = [sensor]
        while current:
            current = convert(current)
            diffs.append(current)
            if all((x == 0 for x in current)):
                break

        diffs.reverse()
        all_diffs.append(diffs)

    # step 1: extrapolated is a sum of previous and last
    total = 0
    for diffs in all_diffs:
        delta = 0
        for row in diffs[1:]:
            delta = row[-1] + delta

        total += delta

    print (f"Day 9, Step 1: {total}")

    # step 2: extrapolated is a diff of previous and last
    total = 0
    for diffs in all_diffs:
        delta = 0
        for row in diffs[1:]:
            delta = row[0] - delta
        total += delta

    print (f"Day 9, Step 2: {total}")


if __name__ == "__main__":
    test = TEST_DATA.split("\n")
    data = get_input_data(9)

    solve(data)