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
    # Thinking:
    #
    # Clearly this problem is a cellular automata and my guess would be
    # that there is a stable state reached at some point.
    #
    # With plots being infinite, there will be two main types of plots:
    # - stable plots, that oscillate between two positions
    # - frontier plots, ones that are continuing to spread outwards
    #
    # The frontier plots are then split into 8 (?) types based on where
    # the first "step" entered them. e.g.:
    #
    #    ... ... ...
    #    ..x ... x..
    #    .x. .x. .x.
    #
    #    ...     ...
    #    ..x     x..
    #    ...     ...
    #
    #    .x. .x. .x.
    #    ..x ... x..
    #    ... ... ...
    #
    # As the steps expand, the tiles in the centre will reach a state of
    # equilibrium and the outside ones will continue to march along.
    #
    # Some observations can be made such that:
    # - The row / column of the initial step is completely void of
    #   rocks, thus it should take the width of the plot for step to
    #   travel back to the starting point.
    # - We should be able to advance time (steps) based on the grid size
    #   so that we know how many are in one of the above states. This
    #   should then mean that we have to solve the state of those given
    #   plots and we should be good.
    #   - I suspect that edge plots will be easier to solve for since
    #     that should be calculating how many steps are possible for the
    #     step count % grid for that given type.
    #
    # Thinking about it a bit more, the corner ones could be populated
    # by points before the main lines (cardinal from S) come marching
    # in. This would mean that we can't just seed a plot with the main
    # line and calculate it's value. It may also mean that there are
    # more states. Some investigation required.
    #
    #   Running the automata and seeing where bounds are crossed, we
    #   have the cardinal directions being crossed at iteration 66,
    #   having moved exactly half of the plot size + 1 and entering
    #   each of the adjacent plots in a straight line directly from
    #   the start position. This is to be expected.
    #
    #   Running a little longer, we see that the input has been
    #   carefully crafted as at iteration 132 the corners are then
    #   filled for the first time with a single entry point that is
    #   the closest diagonal location from the start point. e.g.:
    #
    #       ... ...
    #       ... ...
    #       ..x x..
    #          S
    #       ..x x..
    #       ... ...
    #       ... ...
    #
    #   Running longer again, it appears that this trend holds up in
    #   that the diagonals are always entered by the closest diagonal
    #   neighbour and at a step count of:
    #       132 * the diagonal distance + 1
    #
    # From this investigation, it would seem that we could figure out
    # some shortcuts by finding how many plots will have been reached
    # with a quick step_count // grid_size
    #
    # !!! Another realization I just had was that because the
    #     oscilation of the pattern is a step of 1, once a plot has been
    #     covered, it will just oscillate between the two states. That
    #     means that we will only have to find the time that it takes
    #     for it to be covered and that will be how many of the stable
    #     plots that we have.
    #
    # Napkin math:
    #   - Need to take 26501365 steps
    #   - Plots are 131x131
    #   - 26501365 // 131 = 202300
    #   - 26501365 - (202300 * 131) = 65 (lol)
    #   Looks like we will be walking the current plot + 202300 more.
    #
    # Looking at the diagonals, there are some that have rocks, but
    # those ones don't have rocks directly next to them. This would lead
    # me to believe that diagonal traversal should be at the same rate
    # of the horizontal and vertical. As shown by the running of the
    # automata above where it takes 132 steps for the first step to
    # appear in the diagonally neighbouring plots.
    #
    # Not sure if there is any mathematical relevance yet, but blurring
    # my eyes and looking at the input pattern there is a blank diamond
    # in the data where there are no rocks present. e.g.:
    #
    #       ###.###
    #       ##.#.##
    #       #.###.#
    #       .#####.
    #       #.###.#
    #       ##.#.##
    #       ###.###
    #
    # Based on the oscillation realization above, we should know the
    # amount of tiles that are present in each step and be able to
    # extrapolate out from there. This should be as simple as
    # counting all the input[1::2] and input[::2] spaces that don't have
    # rocks in them, this works because it's an odd input.
    #
    #   #.#       .#.
    #   .#.  ->   #.#
    #   #.#       .#.
    #
    #   This means that we have:
    #       - 7719 odd spaces without rocks
    #       - 7697 even spaces without rocks
    #
    # With this information we just need to figure out how many stable
    # plots there are in 26501365 steps.
    #
    # Given that we start on an odd space and walk an even number
    # towards the edges before we cross into another plot, we can assume
    # that the plots will also have an oscillating odd/even pattern
    #
    # The steps are odd, so we can also determine that the starting plot
    # will be odd at the time of the 26501365th step. With this, moving
    # out through the plots the adjacent ones will flip between odd and
    # even e.g 1 odd, 4 even, 8 odd, 12 even. Adding that up we can see
    # that there is (n + 1)^2 odd and n^2 even. With that info:
    #   - (202300 + 1) ^ 2 odd = 40925694601 * 7719 = 315905436625119
    #   - 202300 ^ 2 even = 40925290000 * 7697 = 315001957130000
    # note: this includes the edge plots that aren't actually complete
    # as well as missing some of the filler plots too (shown below).
    #
    # I _think_ (and I'll leave this here even if I'm wrong) that all
    # that remains is calculating the final plots that are along
    # the edge of the diamond and either adding or removing as needed.
    # e.g.
    #
    #   ..... ..#.. .....
    #   ..... .###. .....
    #   ..... ##### ..... <-- missing plot (needs to be added)
    #   ....# ##### #....
    #   ...## ##### ##...
    #
    #   ..### ##### ###..
    #   .#### ##### ####.
    #   ##### ##### ##### <-- over counted plot (needed to be
    #   .#### ##### ####.     substracted from)
    #   ..### ##### ###..
    #
    #   ...## ##### ##...
    #   ....# ##### #....
    #   ..... ##### .....
    #   ..... .###. .....
    #   ..... ..#.. .....
    #
    # The 202300 is stepping directly to the middle of the outside plot,
    # so the remaining 65 is stepping to the outside edge of it. This
    # produces the diamond pattern. We just need to calculate the number
    # of even and odd on each of these corner pieces then add that to
    # the total.
    #
    # I think the best way of doing this is going to be finding the
    # amount of each corner for odds and evens. For the odds we subtract
    # it from the total, and for even we just add the value. Each corner
    # will need to be calculated for them as the edges of the diamond
    # will use a different one to calculate. (Annotations added to the
    # diagram above to illustrate).
    #
    # Looking at the diagram above, the corners for each case appear to
    # be outside of that created if traversed from the middle. I am
    # hoping to abuse this by calculating the distance traversed to
    # reach a given point, then trim anything that is less than the
    # distance of a straight walk to the edge. This will give us all 4
    # corner counts at once and given we need all 4 for each side of the
    # diamond, we should be able to multiple this value by the total for
    # a single edge and that _should_ do the trick.
    #
    # To find the number for a given side we need to find the ratio
    # to n like we did for the total traversed.
    #
    #   ....o....
    #   ...eoe...
    #   ..oeoeo..
    #   .eoeoeoe.
    #   oeoeoeoeo
    #   .eoeoeoe.
    #   ..oeoeo..
    #   ...eoe...
    #   ....o....
    #
    # Here n is 4 and it appears that there are twice as many even and
    # odd plots to cover. The extreme corners need to have 2 odd removed
    # from each of them. With each of our counts being all 4 corners
    # this changes the calculation to n/2 for even and n/2 + 1 odd.
    #
    # At present this doesn't work as expected. It feels very close, but
    # there is something about my math that is off.
    #
    #   ......o......
    #   .....eoe.....
    #   ....oeoeo....
    #   ...eoeoeoe...
    #   ..oeoeoeoeo..
    #   .eoeoeoeoeoe.
    #   oeoeoeoeoeoeo
    #   .eoeoeoeoeoe.
    #   ..oeoeoeoeo..
    #   ...eoeoeoe...
    #   ....oeoeo....
    #   .....eoe.....
    #   ......o......
    #
    #   ..... .....
    #   ..... .....
    #   ..... ..... <-- missing plot
    #   #.... .....
    #   ##... .....
    #    v------------- over counted plot
    #   ###.. .....
    #   ####. .....
    #   ##### ..... <-- missing plot
    #   ##### #....
    #   ##### ##...
    #
    #   ##### ###..
    #   ##### ####.
    #   ##### ##### <-- over counted plot
    #   ##### ###..
    #
    # Hmmm, definitely missing something with the math. Feels like it
    # might be an off by 1 somewhere. Scalling up both the diagrams
    # above show that the mental model I have is somewhat on track.
    #   - Corners calculated by `distance > size // 2`
    #
    # Not that it matters with how we are counting spots, but I've found
    # that there are spots in the input data where it is surrounded by
    # rocks. This means that it will never be traversible.
    #
    #  .....
    #  ..#..
    #  .#.#.
    #  ..#..
    #  .....
    #
    # This is likely why this method we had earlier didn't work as it
    # assumed that it could reach every spot that didn't have a rock
    #
    #   even = len(list(filter(lambda x: x != '#', content[0::2])))
    #   odd = len(list(filter(lambda x: x != '#', content[1::2])))
    #
    # Using the following code to debug
    #
    #   ```
    #   with open('./data/test', 'w') as out_file:
    #      d = [list(line) for line in data.splitlines()]
    #      for p in __COORD_SET__.keys():
    #          d[p.y][p.x] = 'o'
    #
    #      d[start.y][start.x] = '!'
    #
    #      print(
    #           *(''.join(line) for line in d),
    #           sep='\n',
    #           file=out_file
    #      )
    #   ```
    #
    #   - Corners data looks correct
    #
    # Uhhh... Not sure when that happend but I had the following and
    # fixing it seems to make it _magically_ (rolls eyes) work now...
    #   `odd_count * even_rockless + even_rockless * odd_rockless
    # Yeah... That'd do it.
    #
    # All the math we went through above still checks out, so we are
    # good I guess :sweat_smile:.

    plot_size = data.find('\n')

    step_count = 26501365
    plot_count = step_count // plot_size

    even_count = plot_count ** 2
    odd_count = (plot_count + 1) ** 2

    plot = data.split('\n')

    start, bounds = Vector(plot_size // 2), (Z, Vector(plot_size))
    todo, visited = [(start, 0)], {}

    while todo:
        point, distance = todo.pop(0)

        if point in visited:
            continue
        visited[point] = distance

        for o in (U, D, L, R):
            new_point = point + o

            if not new_point.inside(bounds):
                continue

            if plot[new_point.y][new_point.x] == '#':
                continue

            todo.append((new_point, distance + 1))

    corners = {p: d for p, d in visited.items() if d > (plot_size // 2)}
    odd_rockless = len([p for p, d in visited.items() if d % 2 == 1])
    odd_corners = len([p for p, d in corners.items() if d % 2 == 1])
    even_rockless = len([p for p, d in visited.items() if d % 2 == 0])
    even_corners = len([p for p, d in corners.items() if d % 2 == 0])

    total = 0
    total += odd_count * odd_rockless
    total += even_count * even_rockless
    total -= (plot_count + 1) * odd_corners
    total += (plot_count) * even_corners

    return total
