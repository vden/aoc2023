from itertools import combinations

from . import get_input_data

TEST_DATA = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""


def solve(data: list[str]):
    _map = [list(x) for x in data]

    def map_galaxies(smap: list[list[str]]):
        # find all the galaxies
        _galaxies = {}
        gidx = 0
        for x, line in enumerate(smap):
            for y, s in enumerate(line):
                if s == '#':
                    _galaxies[gidx] = (x, y)
                    gidx += 1

        return _galaxies

    def expand(smap, galaxies, factor: int = 2):
        gal = dict(galaxies)

        # expand the universe by line, and again after transpose the map
        for x, line in enumerate(smap):
            if all((k == '.' for k in line)):
                for (gid, (gx, gy)) in galaxies.items():
                    if gx > x:
                        gal[gid] = (gal[gid][0] + factor - 1, gal[gid][1])

        _smap = list(zip(*smap))
        for y, line in enumerate(_smap):
            if all((k == '.' for k in line)):
                for (gid, (gx, gy)) in galaxies.items():
                    if gy > y:
                        gal[gid] = (gal[gid][0], gal[gid][1] + factor - 1)

        return gal

    def count_steps(galaxies):
        pairs = combinations(galaxies, 2)
        total = 0
        for f, t in pairs:
            x0, y0 = galaxies[f]
            x1, y1 = galaxies[t]

            total += (abs(x0-x1) + abs(y0-y1))
        return total


    _map = list(zip(*_map))
    galaxies = map_galaxies(_map)

    galaxies_1 = expand(_map, galaxies, 2)
    total = count_steps(galaxies_1)

    print (f"Day 11, Step 1: {total}")

    galaxies_2 = expand(_map, galaxies, 1000000)
    total = count_steps(galaxies_2)

    print (f"Day 11, Step 2: {total}")


if __name__ == "__main__":
    test = TEST_DATA.split("\n")
    data = get_input_data(11)

    solve(data)