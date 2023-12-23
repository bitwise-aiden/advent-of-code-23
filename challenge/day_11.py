from common import *


def __challenge_11_calculate(data : str, scale : int) -> int:
    lines = data.split('\n')

    width = len(lines[0])
    height = len(lines)

    voids = []
    galaxies = []

    # Find vertical voids
    for y in range(height):
        for x in range(width):
            if lines[y][x] == '#':
                break
        else:
            voids.append(Vector2(0, y))

    # Find horizontal voids
    for x in range(width):
        for y in range(height):
            if lines[y][x] == '#':
                break
        else:
            voids.append(Vector2(x, 0))

    scale -= 1
    # Find galaxies and expand for voids
    for y in range(height):
        for x in range(width):
            if lines[y][x] == '#':
                x_expand = len([*filter(lambda v: 0 < v.x < x, voids)])
                y_expand = len([*filter(lambda v: 0 < v.y < y, voids)])

                galaxies.append(
                    Vector2(x + x_expand * scale, y + y_expand * scale)
                )

    result = 0

    galaxy_count = len(galaxies)

    for i in range(galaxy_count - 1):
        for j in range(i + 1, galaxy_count):
            a, b = galaxies[i], galaxies[j]

            delta = b - a

            result += abs(delta.x) + abs(delta.y)


    return result


@challenge
def challenge_11_1(data : str) -> int:
    return __challenge_11_calculate(data, 1)



@challenge
def challenge_11_1(data : str) -> int:
    return __challenge_11_calculate(data, 1_000_000)
