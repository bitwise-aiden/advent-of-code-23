from common import *


def __lines(data : str) -> list[(Vector3, Vector3)]:
    lines : list[(Vector3, Vector3)] = []

    for line in data.splitlines():
        position, velocity = line.split(' @ ')
        position = Vector3(*map(int, position.split(', ')), _type = float)
        velocity = Vector3(*map(int, velocity.split(', ')), _type = float)

        lines.append((position, velocity))

    return lines


def __intersect_2d(p, pv, q, qv, start, end) -> bool:
    pa, pb, pc = pv.y, -pv.x, pv.y * p.x - pv.x * p.y
    qa, qb, qc = qv.y, -qv.x, qv.y * q.x - qv.x * q.y

    if pa * qb == qa * pb:
        return False

    x = (pc * qb - qc * pb) / (pa * qb - qa * pb)
    y = (qc * pa - pc * qa) / (pa * qb - qa * pb)

    return (
        start <= x <= end and start <= y <= end and
        (x - p.x) * pv.x > 0 and (y - p.y) * pv.y > 0 and
        (x - q.x) * qv.x > 0 and (y - q.y) * qv.y > 0
    )


@challenge
def challenge_24_1(data : str) -> int:
    result : int = 0

    lines = __lines(data)

    for i in range(len(lines) - 1):
        for j in range(i + 1, len(lines)):
            (p, r), (q, s) = lines[i], lines[j]

            if __intersect_2d(p, r, q, s, 200000000000000, 400000000000000):
                result += 1

    return result


@challenge
def challenge_24_2(data : str) -> int:
    # I have intentionally not solved today's p2 because this is quite
    # far outside the realm of my expertise and having a 3 month old,
    # not how I want to be spending my Christmas Eve. I am foregoing
    # this one star, but doing so for family <3
    return
