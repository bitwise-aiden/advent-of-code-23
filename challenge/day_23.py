from common import *

import sys

sys.setrecursionlimit(10000)


@challenge
def challenge_23_1(data : str) -> int:
    area = data.splitlines()
    width, height = len(area[0]), len(area)
    bounds = (Z, Vector2(width, height))
    slopes = {'^': U, '>': R, 'v': D, '<': L}

    start, end = Vector2(1, 0), Vector2(width - 2, height - 1)
    seen = {start : 0, end : 0}

    def traverse(path, pos) -> int:
        # This check doesn't actually hold up when trying to find
        # the longest path without using the same location twice as
        # you may want to go a short way to leave other spaces open
        # to be used for the greater length. It is a local maxima issue.
        #
        # That said, I'm leaving it in for this as the longest path
        # for part 1 doesn't have an issue with hitting a local maxima,
        # so the performance benefit is worth it. Data sets may vary.
        if pos in seen and seen[pos] > len(path):
            return 0

        seen[pos] = len(path)

        if pos == end:
            return len(path)

        directions = {U, D, L, R}

        cc = area[pos.y][pos.x]
        if cc in slopes:
            directions = {slopes[cc]}

        options = []

        for o in directions:
            opos = o + pos

            # Don't tred the same path
            if opos in path:
                continue

            # Don't process out of bounds (doesn't matter because
            # bounds are surrounded by #, but /shrug)
            if not opos.inside(bounds):
                continue

            c = area[opos.y][opos.x]

            # Cannot walk through trees
            if c == '#':
                continue

            # Cannot walk up slope that is in the opposite direction
            # of travel
            if c in slopes and slopes[c] == -o:
                continue

            options.append(traverse({*path, opos}, opos))

        return max(options) if options else 0

    return traverse({start}, start) - 1

largest = 0

@challenge
def challenge_23_2(data : str) -> int:
    # This solution has yet to finish, but leaving it overnight meant
    # that it still had enough time to find the global maxima. I'm not
    # going improve it as this solution came out of having a baby who
    # wasn't sleeping well overnight and now that it found the answer
    # I want to imortalize it despite clearly needing to improve it.
    area = data.splitlines()
    width, height = len(area[0]), len(area)
    bounds = (Z, Vector2(width, height))

    start, end = Vector2(1, 0), Vector2(width - 2, height - 1)

    def valid_neighbours(pos, without = None):
        neighbours = set()

        for o in {U, D, L, R}:
            opos = o + pos

            if (
                opos == without or
                not opos.inside(bounds) or
                area[opos.y][opos.x] == '#'
            ):
                continue

            neighbours.add(opos)

        return neighbours

    def traverse(path, path_dist, pos_to, pos_from) -> int:
        dist = 0

        while len(neighbours := valid_neighbours(pos_to, pos_from)) == 1:
            pos_to, pos_from = neighbours.pop(), pos_to
            dist += 1

        path_dist += dist

        if pos_to == end:
            global largest
            largest = max(largest, path_dist)
            print(largest)
            return path_dist

        if pos_to in path:
            return 0

        path = {*path, pos_to}
        options = [
            traverse(path, path_dist + 1, neighbour, pos_to)
            for neighbour in valid_neighbours(pos_to, pos_from)
        ]

        return max(options) if options else 0

    return traverse({start}, 0, start, start)#
