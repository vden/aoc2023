from pprint import pprint

from . import get_input_data

TEST_DATA1 = """.....
.S-7.
.|.|.
.L-J.
....."""

TEST_DATA2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

TEST_DATA3 = """...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""

TEST_DATA4 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""

TEST_DATA5 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""

TEST_DATA6 = """..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
.........."""


def solve(data: list[str]):
    _pmap = [list(x) for x in data]
    pmap = list(zip(*_pmap))

    # pprint (_pmap)
    start = (0, 0)
    for x, row in enumerate(pmap):
        for y, pt in enumerate(row):
            if pt == 'S':
                start = (x, y)
                break

    visited = [[0 for _ in range(0, len(y))] for y in pmap]
    visited[start[0]][start[1]] = 1

    def buildPath(path, pt):
        last = path[-1]
        # print (f"Map: {pmap[pt[0]][pt[1]]}")
        match pmap[pt[0]][pt[1]]:
            case '-':
                if last[0] < pt[0]:
                    pnext = (pt[0] + 1, pt[1])
                else:
                    pnext = (pt[0] - 1, pt[1])
            case '|':
                if last[1] < pt[1]:
                    pnext = (pt[0], pt[1] + 1)
                else:
                    pnext = (pt[0], pt[1] - 1)
            case 'F':
                if last[1] == pt[1] + 1:
                    pnext = (pt[0] + 1, pt[1])
                else:
                    pnext = (pt[0], pt[1] + 1)
            case '7':
                if last[1] == pt[1] + 1:
                    pnext = (pt[0] - 1, pt[1])
                else:
                    pnext = (pt[0], pt[1] + 1)
            case 'L':
                if last[1] == pt[1] - 1:
                    pnext = (pt[0] + 1, pt[1])
                else:
                    pnext = (pt[0], pt[1] - 1)
            case 'J':
                if last[1] == pt[1] - 1:
                    pnext = (pt[0] - 1, pt[1])
                else:
                    pnext = (pt[0], pt[1] - 1)

        # print (f"Decided next: {pnext}, {pmap[pnext[0]][pnext[1]]}, {visited[pnext[0]][pnext[1]]}")

        if pmap[pnext[0]][pnext[1]] == '.' or visited[pnext[0]][pnext[1]] == 1:
            return path + [pt, ], None

        path = path + [pt, ]
        visited[pnext[0]][pnext[1]] = 1
        return (path, pnext)

    entries = []
    adj = ((-1, 0), (0, -1), (0, 1), (1, 0))
    allowed = (('-', 'F', 'L'), ('|', '7', 'F'), ('|', 'L', 'J'), ('-', '7', 'J'))
    for (ax, ay), kinds in zip(adj, allowed):
        if 0 <= start[0] + ax < len(pmap) and 0 <= start[1] + ay < len(pmap[0]):
            if pmap[start[0] + ax][start[1] + ay] in kinds:
                entries.append((start[0] + ax, start[1] + ay))
                visited[start[0] + ax][start[1] + ay] = 1
    print (entries)

    paths = [[start, x] for x in entries]
    while True:
        new_points = []
        for idx, path in enumerate(paths):
            path, pt = path[:-1], path[-1]
            path, pnext = buildPath(path, pt)
            if pnext:
                new_points.append(pnext)
                paths[idx] = path + [pnext, ]

        if not new_points:
            break

    max_path = max([len(x) for x in paths])
    print (f"Day 10, Step 1: {max_path - 1}")

    # area = 0
    _visited = list(zip(*visited))
    # pprint (_visited)

    # expand visited cells to 3x3
    # need to manually fix type of the S cell
    newv = []
    for x, row in enumerate(_visited):
        newr = []
        for y, pt in enumerate(row):
            if pt == 1:
                match pmap[y][x]:
                    case '-':
                        newr.append([[0, 0, 0], [1, 1, 1], [0, 0, 0]])
                    case '|':
                        newr.append([[0, 1, 0], [0, 1, 0], [0, 1, 0]])
                    case 'F':
                        newr.append([[0, 0, 0], [0, 1, 1], [0, 1, 0]])
                    case 'L':
                        newr.append([[0, 1, 0], [0, 1, 1], [0, 0, 0]])
                    case '7':
                        newr.append([[0, 0, 0], [1, 1, 0], [0, 1, 0]])
                    case 'J':
                        newr.append([[0, 1, 0], [1, 1, 0], [0, 0, 0]])
                    case 'S':
                        # newr.append([[0, 0, 0], [0, 1, 1], [0, 1, 0]]) # test 3 / 4 / 6
                        # newr.append([[0, 0, 0], [1, 1, 0], [0, 1, 0]]) # test 5
                        newr.append([[0, 1, 0], [1, 1, 0], [0, 0, 0]]) # data

            else:
                newr.append([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        newv.extend(list([sum(x, []) for x in zip(*newr)]))

    visited = list(zip(*newv))


    # expand it by 1 more cell each side to start flood fill
    visited = [[0, *x, 0] for x in visited]
    visited = [[0] * len(visited[0]), *visited, [0] * len(visited[0])]

    # pprint(_pmap, width=240)
    # _visited = list(zip(*visited))
    # print ("\n".join(["".join(['.' if z else ' ' for z in x]) for x in _visited]))

    # perform flood fill from 0, 0
    next_points = [(0, 0)]
    visited[0][0] = 2
    while next_points:
        points = []
        for pt in next_points:
            for (ax, ay) in adj:
                if 0 <= pt[0] + ax < len(visited) and 0 <= pt[1] + ay < len(visited[0]):
                    if visited[pt[0] + ax][pt[1] + ay] == 0:
                        visited[pt[0] + ax][pt[1] + ay] = 2
                        points.append((pt[0] + ax, pt[1] + ay))

        next_points = points

    area = 0
    #visited = [x[1:-1] for x in visited[1:-1]]
    # _visited = list(zip(*visited))
    # pprint (["".join([str(z) if z else '.' for z in x]) for x in _visited])

    # pprint (_visited)
    # pprint (_pmap, width=120)

    # try to find empty 3x3 cells and count each for 1 area point
    for x in range(0, len(visited)):
        for y in range(0, len(visited[x])):
            pt = visited[x][y]
            if pt == 0:
                cells = []

                for ax in (-1, 0, 1):
                    for ay in (-1, 0, 1):
                        cells.append((x+ax, y+ay))

                if all((visited[n[0]][n[1]] == 0 for n in cells)):
                    area += 1
                    for cx, cy in cells:
                        visited[cx][cy] = 3

    # _visited = list(zip(*visited))
    # pprint (["".join([str(z) if z else '.' for z in x]) for x in _visited])

    print (f"Day 10, Step 2: {area}")


if __name__ == "__main__":
    test1 = TEST_DATA1.split("\n")
    test2 = TEST_DATA2.split("\n")
    test3 = TEST_DATA3.split("\n")
    test4 = TEST_DATA4.split("\n")
    test5 = TEST_DATA5.split("\n")
    test6 = TEST_DATA6.split("\n")

    data = get_input_data(10)

    solve(data)