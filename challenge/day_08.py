from common import *


@challenge
def challenge_8_1(data : str) -> int:
    directions, nodes = data.split('\n\n')

    re_letters : re.Pattern = re.compile('[A-Z]+')

    directions = [
        0 if direction == 'L' else 1
        for direction in directions
    ]

    map : dict[str, str] = {
        k: v
        for k, *v in (re_letters.findall(node) for node in nodes.split('\n'))
    }

    current_location : str = 'AAA'
    direction_index : int = 0

    result : int = 0

    while current_location != 'ZZZ':
        direction = directions[direction_index]

        current_location = map[current_location][direction]

        direction_index = (direction_index + 1) % len(directions)
        result += 1

    return result


@challenge
def challenge_8_2(data : str) -> int:
    directions, nodes = data.split('\n\n')

    re_letters : re.Pattern = re.compile('[A-Z]+')

    directions = [
        0 if direction == 'L' else 1
        for direction in directions
    ]

    map : dict[str, str] = {
        k: v
        for k, *v in (re_letters.findall(node) for node in nodes.split('\n'))
    }

    def __length(location : str) -> int:
        length : int = 0
        index : int = 0

        while location[-1] != 'Z':
            direction = directions[index]
            location = map[location][direction]

            index = (index + 1) % len(directions)
            length += 1

        return length

    lengths : list[int] = [
        __length(location)
        for location in map.keys() if location[-1] == 'A'
    ]

    return functools.reduce(lcm, lengths)
