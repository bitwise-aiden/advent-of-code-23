from common import *


pipes : dict = {
    '|': ({U, D}),
    '-': ({L, R}),
    '/': ({L, U}, {R, D}),
    '\\': ({L, D}, {R, U}),
}


def __challenge_16_filled(grid, position, direction):
    height = len(grid)
    width = len(grid[0])

    seen = set()
    todo = [(position, direction)]

    while todo:
        p, d = todo.pop()

        if not (0 <= p.x < width and 0 <= p.y < height):
            continue

        if (p, d) in seen:
            continue
        seen.add((p, d))

        t = grid[p.y][p.x]

        match t:
            case '.':
                todo.append((p + d, d))
            case '|' | '-':
                ss = pipes[t]
                if ss in pipes[t]:
                    todo.append((p + d, d))
                else:
                    for s in ss:
                        todo.append((p + s, s))
            case '\\' | '/':
                for ss in pipes[t]:
                    if -d in ss:
                        ed = (ss - {-d}).pop()
                        todo.append((p + ed, ed))

    cells = {p for p, _ in seen}

    return len(cells)



@challenge
def challenge_16_1(data : str) -> int:
    grid = [list(line) for line in data.split('\n')]
    return __challenge_16_filled(grid, Z, R)


@challenge
def challenge_16_2(data : str) -> int:
    result : int = 0

    grid = [list(line) for line in data.split('\n')]
    height = len(grid)
    width = len(grid[0])

    for y in range(height):
        l, r = Vector(0, y), Vector(width - 1, y)

        result = max(result, __challenge_16_filled(grid, l, R))
        result = max(result, __challenge_16_filled(grid, r, L))

    for x in range(width):
        t, b = Vector(x, 0), Vector(x, height - 1)

        result = max(result, __challenge_16_filled(grid, t, D))
        result = max(result, __challenge_16_filled(grid, b, U))

    return result
