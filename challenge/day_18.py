from common import *


def __challenge_18_shoelace(points : list[Vector]) -> int:
    x = [v.x for v in points]
    y = [v.y for v in points]

    return abs(
        sum(i * j for i, j in zip(x, y[1:] + y[:1]))
        - sum(i * j for i, j in zip(x[1:] + x[:1], y))
    ) / 2


def __challenge_18_data(data : str, processor) -> int:
    re_data : re.Pattern = re.compile('([A-Z]) ([0-9]+) \(#(.*?)\)')

    polygon : list[Vector] = [Z]
    dist = 0

    for line in data.split('\n'):
        dir, dis, col = re_data.match(line).groups()
        dir, dis = processor(dir, dis, col)
        dist += dis

        polygon.append(polygon[-1] + dir * dis)

    return int(__challenge_18_shoelace(polygon) + dist // 2 + 1)


@challenge
def challenge_18_1(data : str) -> int:
    directions = {'U': U, 'D': D, 'L': L, 'R': R}
    return __challenge_18_data(
        data,
        lambda dir, dis, _: (directions[dir], int(dis)),
    )

@challenge
def challenge_18_2(data : str) -> int:
    directions = [R, U, L, D]
    return __challenge_18_data(
        data,
        lambda _1, _2, col: (directions[int(col[-1], 16)], int(col[:5], 16)),
    )
