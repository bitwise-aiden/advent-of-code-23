from common import *


@challenge
def challenge_21_1(data : str) -> int:
    start : Vector
    rocks : set[Vector] = set()

    for y, line in enumerate(data.split('\n')):
        for x, char in enumerate(line):
            match char:
                case 'S':
                    start = Vector(x, y)
                case '#':
                    rocks.add(Vector(x, y))

    width, height = x + 1, y + 1
    bounds : tuple[Vector] = (Z, Vector(width, height))
    current : set[Vector] = {start}

    for _ in range(64):
        next : set[Vector] = set()

        for location in current:
            for offset in [U, D, L, R]:
                location_step : Vector = location + offset

                if location_step in rocks:
                    continue

                if not location_step.inside(bounds):
                    continue

                next.add(location_step)

        current = next

    return len(current)


@challenge
def challenge_21_2(data : str) -> int:
    start : Vector
    rocks : set[Vector] = set()

    for y, line in enumerate(data.split('\n')):
        for x, char in enumerate(line):
            match char:
                case 'S':
                    start = Vector(x, y)
                case '#':
                    rocks.add(Vector(x, y))

    width, height = x + 1, y + 1
    bounds : tuple[Vector] = (Z, Vector(width, height))

    seen : dict[tuple(Vector), tuple(Vector)] = {}
    current : dict[Vector, set[Vector]] = {Z: {start}}


    for _ in range(100):
        next : dict[Vector, set[Vector]] = {}

        for key, plot in current.items():
            plot_locations : tuple[Vector] = tuple(plot)
            if plot_locations in seen:
                next[key] = seen[plot_locations]
                continue

            for location in plot:
                for offset in [U, D, L, R]:
                    location_step : Vector = location + offset

                    plot_coord : Vector = Vector(
                        abs(location_step.x // width) * sign(location_step.x),
                        abs(location_step.y // height) * sign(location_step.y),
                    )

                    localized_step = location_step - plot_coord * bounds[1]

                    if localized_step in rocks:
                        continue

                    next[plot_coord] = next.get(plot_coord, set())
                    next[plot_coord].add(location_step)

            seen[plot_locations] = next[key]

        current = next

    return sum(len(plot) for plot in current.values())
