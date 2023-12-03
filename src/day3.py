from . import get_input_data

TEST_DATA = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def look(x: int, adj: int, row: str, xs: str = "") -> str:
    if x < 0 or x >= len(row):
        return xs

    if row[x].isdigit():
        return look(x + adj, adj, row,
                    xs + row[x] if adj > 0 else row[x] + xs)

    return xs


def findNumbers(ax: int, bx: int, row: str) -> list[str]:
    results = []

    found = False
    idx = ax
    while idx <= bx:
        x = row[idx]
        if x.isdigit():
            if not found:
                results.append(look(idx-1, -1, row) + x + look(idx+1, 1, row))
                found = True
        else:
            found = False

        idx += 1

    return results


def solve(data: list[str]):
    map_symbols = {}

    for ridx, line in enumerate(data):
        for cidx, s in enumerate(line):
            if s == '.':
                continue

            if not s.isdigit():
                map_symbols[(cidx, ridx, s)] = []

    for (x, y, sym) in map_symbols.keys():
        numbers = []
        for j in (-1, 0, 1):
             if y+j < len(data) and y+j >= 0:
                numbers.extend([int(x) for x in findNumbers(x-1, x+1, data[y+j])])
        map_symbols[(x, y, sym)] = numbers

    part_numbers_sum = sum(sum(map_symbols.values(), []))
    print (f"Day 3, Step 1: {part_numbers_sum}")

    gears = [v for ((_, _, sym), v) in map_symbols.items() if sym == "*" and len(v) == 2]
    gear_ratios = sum((x[0] * x[1] for x in gears))

    print (f"Day 3, Step 2: {gear_ratios}")


if __name__ == "__main__":
    data = get_input_data(3)
    test = TEST_DATA.split("\n")

    solve(data)