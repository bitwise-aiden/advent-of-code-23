from common import *


pipes : dict[str, tuple[Vector2]] = {
    '|': {U, D},
    '-': {L, R},
    'L': {U, R},
    'J': {U, L},
    '7': {D, L},
    'F': {D, R},
    '.': {I}
}


@challenge
def challenge_10_1(data : str) -> int:
    ground = [
        [pipes.get(char, Z) for char in line]
        for line in data.split('\n')
    ]

    s_loc = data.replace('\n', '').find('S')
    s_loc = Vector2(s_loc % len(ground[0]), s_loc // len(ground[0]))

    directions = []

    for o in [U, D, L, R]:
        c = o + s_loc

        if  -o in ground[c.y][c.x]:
            directions.append(o)


    locations = [s_loc + d for d in directions]
    distance = 1

    while locations[0] != locations[1]:
        directions = [
            list(ground[l.y][l.x] - {-d})[0]
            for d, l in zip(directions, locations)
        ]

        locations = [
            l + d
            for d, l in zip(directions, locations)
        ]

        distance += 1

    return distance


@challenge
def challenge_10_2(data : str) -> int:
    dirs = [U, R, D, L]

    ground = [
        [pipes.get(char, {Z}) for char in line]
        for line in data.split('\n')
    ]

    # Find start location
    s_loc = data.replace('\n', '').find('S')
    s_loc = Vector2(s_loc % len(ground[0]), s_loc // len(ground[0]))

    # Find directions that connect to start
    directions = []
    for o in [U, D, L, R]:
        c = o + s_loc

        if -o in ground[c.y][c.x]:
            directions.append(o)

    direction = directions[0]
    ground[s_loc.y][s_loc.x] = set(directions)
    location = s_loc + direction


    # Store out all path locations
    path = {location}
    while location != s_loc:
        direction = list(ground[location.y][location.x] - {-direction})[0]
        location += direction

        path.add(location)

    def process_pipe(check_location : Vector2) -> (Vector2, int):
        if check_location not in path:
            return check_location, 0

        if R not in ground[check_location.y][check_location.x]:
            return check_location, 1

        exit_location : Vector2 = check_location + R

        while {L, R} == ground[exit_location.y][exit_location.x]:
            exit_location += R

        shared_count : int = len(
            ground[check_location.y][check_location.x] &
            ground[exit_location.y][exit_location.x]
        )

        return exit_location, (shared_count + 1) % 2

    result = 0

    for x in range(len(ground[0])):
        for y in range(len(ground)):
            l = Vector2(x, y)

            if l in path:
                continue

            count = 0

            while l.x < len(ground[0]):
                l, c = process_pipe(l + R)

                count += c

            if count % 2 == 1:
                result += 1

    return result
