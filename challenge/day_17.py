from common import *


def __challenge_17_process(
    data : str,
    distance_min : int,
    distance_max : int,
) -> int:
    grid : list[list[int]] = [
        [int(cell) for cell in line]
        for line in data.split('\n')
    ]

    width, height = len(grid[0]), len(grid)
    directions, bounds = {U, D, L, R}, (Z, Vector(width, height))

    start, end = Z, Vector(width - 1, height - 1)

    seen, todo = set(), queue.PriorityQueue()
    todo.put((0, start, Z, 0))

    while todo:
        cost, position, direction, distance = todo.get()

        if position == end and distance >= distance_min:
            return cost

        seen_key = (position, direction, distance)

        if seen_key in seen:
            continue

        seen.add(seen_key)

        for ndirection in directions - {direction, -direction}:
            travel_cost = 0

            for ndistance in range(distance_min, distance_max + 1):
                nposition = position + ndirection * ndistance

                if not nposition.inside(bounds):
                    continue

                travel_cost += grid[nposition.y][nposition.x]
                ncost = cost + travel_cost

                todo.put((ncost, nposition, ndirection, ndistance))

    return math.inf


@challenge
def challenge_17_1(data : str) -> int:
    return __challenge_17_process(data, 1, 3)


@challenge
def challenge_17_2(data : str) -> int:
    return __challenge_17_process(data, 4, 10)
