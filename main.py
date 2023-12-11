
import collections
import functools
import math
import re
import time

count : int = 1
challenges : list[callable] = []

def challenge(
    func : callable
) -> None:
    global count

    count += 1

    day : int = count // 2
    ch : int = count % 2 + 1

    def challenge_runner():
        data : str = input_data(day)

        start, result, end = time.time(), func(data), time.time()

        print(f'day {day}, challenge {ch} ({end - start:0.3f} ms): {result}')

    challenges.append(challenge_runner)


def input_data(day : int) -> str:
    with open(f'./data/day_{day:02d}_input', 'r') as in_file:
        return in_file.read().strip()


def runner(day : int = -1) -> None:
    challenges_to_run : list[callable] = challenges

    day -= 1

    if day >= 0:
        challenges_to_run = challenges[day * 2:day * 2 + 2]

    for challenge in challenges_to_run:
        challenge()


@challenge
def challenge_1_1(data : str) -> int:
    data : str = input_data(1)

    re_num : re.Pattern = re.compile(r'[0-9]')
    result : int = 0

    for line in data.split('\n'):
        matches : list[any] = re_num.findall(line)

        result += int(matches[0]) * 10 + int(matches[-1])

    return result


@challenge
def challenge_1_2(data : str) -> int:
    digit_str : list[str] = [
        'zero',
        'one',
        'two',
        'three',
        'four',
        'five',
        'six',
        'seven',
        'eight',
        'nine',
    ]

    def as_int(value : str) -> int:
        return digit_str.index(value) if value in digit_str else int(value)

    re_num : re.Pattern = re.compile(
        f'(?=([0-9]|{"|".join(digit_str)}))',
    )
    result : int = 0

    for line in data.split('\n'):
        matches : list[any] = re_num.findall(line)

        result += as_int(matches[0]) * 10 + as_int(matches[-1])

    return result


@challenge
def challenge_2_1(data : str) -> int:
    target : dict[str, int] = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    re_rounds : re.Pattern = re.compile('( ([0-9]+) (.+?))(?:[,;]|$)')
    result : int = 0

    for line in data.split('\n'):
        game, rounds = line.split(':')

        for round in re_rounds.finditer(rounds):
            _, count, color = round.groups()
            if target[color] < int(count):
                break
        else:
            result += int(game.split(' ')[1])

    return result


@challenge
def challenge_2_2(data: str) -> int:
    re_rounds : re.Pattern = re.compile('( ([0-9]+) (.+?))(?:[,;]|$)')
    result : int = 0

    for line in data.split('\n'):
        _, rounds = line.split(':')

        max_counts : dict[str, int] = {
            'red': 0,
            'green': 0,
            'blue': 0,
        }

        for round in re_rounds.finditer(rounds):
            _, count, color = round.groups()

            max_counts[color] = max(max_counts[color], int(count))

        value : int = 1

        for count in max_counts.values():
            value *= count

        result += value

    return result


@challenge
def challenge_3_1(data : str) -> int:
    numbers : list[tuple[int, int, int, int]] = []
    symbols : set[tuple[int, int]] = set()

    data_split : list[str] = data.split('\n')

    x_extent : int = len(data_split[0])
    y_extent : int = len(data_split)

    def adjacent(y : int, xs : int, xe : int):
        yield (y, xs - 1)
        yield (y, xe)

        for x in range(xs - 1, xe + 1):
            yield(y - 1, x)
            yield(y + 1, x)

    def is_symbol(x : int, y : int) -> bool:
        return (
            0 <= x < x_extent and
            0 <= y < y_extent and
            (y, x) in symbols
        )


    re_number : re.Pattern = re.compile(r'[0-9]+')
    re_symbol : re.Pattern = re.compile(r'[^0-9\.]')

    for i, line in enumerate(data.split('\n')):
        for number in re_number.finditer(line):
            numbers.append((int(number.group()), i, *number.span()))

        for symbol in re_symbol.finditer(line):
            symbols.add((i, symbol.span()[0]))

    result : int = 0

    for (number, y, xs, xe) in numbers:
        for ay, ax in adjacent(y, xs, xe):
            if is_symbol(ax, ay):
                result += number
                break

    return result


@challenge
def challenge_3_2(data : str) -> int:
    symbols : dict[tuple[int, int], list[int]] = {}

    data_split : list[str] = data.split('\n')

    x_extent : int = len(data_split[0])
    y_extent : int = len(data_split)

    def adjacent(y : int, xs : int, xe : int):
        yield (y, xs - 1)
        yield (y, xe)

        for x in range(xs - 1, xe + 1):
            yield(y - 1, x)
            yield(y + 1, x)

    def is_symbol(x : int, y : int) -> bool:
        return (
            0 <= x < x_extent and
            0 <= y < y_extent and
            data_split[y][x] == '*'
        )

    re_number : re.Pattern = re.compile(r'[0-9]+')

    for i, line in enumerate(data_split):
        for number in re_number.finditer(line):
            for y, x in adjacent(i, *number.span()):
                if is_symbol(x, y):
                    symbols[(x, y)] = symbols.get((x, y), [])
                    symbols[(x, y)].append(int(number.group()))

    result : int = 0

    for numbers in symbols.values():
        if len(numbers) == 2:
            result += numbers[0] * numbers[1]

    return result


@challenge
def challenge_4_1(data : str) -> int:
    result : int = 0

    re_numbers : re.Pattern = re.compile('[0-9]+')

    for line in data.split('\n'):
        _, numbers = line.split(':')
        winners, current = numbers.split('|')

        winners = {int(w.group()) for w in re_numbers.finditer(winners)}
        current = {int(c.group()) for c in re_numbers.finditer(current)}

        count : int = len(winners & current)

        if count > 0:
            result += 2 ** (count - 1)

    return result


@challenge
def challenge_4_2(data : str) -> int:
    re_card : re.Pattern = re.compile('Card\s+([0-9]+): (.*?)\|(.*)')
    re_numbers : re.Pattern = re.compile('[0-9]+')

    data_processed : dict[int, int] = {}

    for line in data.split('\n'):
        number, winners, current = re_card.match(line).groups()
        winners = {int(w.group()) for w in re_numbers.finditer(winners)}
        current = {int(c.group()) for c in re_numbers.finditer(current)}

        data_processed[int(number)] = len(winners & current)

    def tally(number):
        count = data_processed[number]

        result : int = 1

        if count == 0:
            return result

        for i in range(number + 1, number + count + 1):
            result += tally(i)

        return result

    final : int = 0

    for number in data_processed.keys():
        final += tally(number)

    return final


def __challenge_5_data(data : str) -> dict:
    seeds, *sections = data.split('\n\n')

    re_numbers : re.Pattern = re.compile('[0-9]+')

    result : dict = {
        'seeds': [*map(int, re_numbers.findall(seeds))]
    }

    for section in sections:
        name, *values = section.split('\n')
        result[name[:-5]] = [
            [*map(int, re_numbers.findall(value))]
            for value in values
        ]

    return result


@challenge
def challenge_5_1(data : str) -> int:
    parsed_data : dict = __challenge_5_data(data)

    seeds : list = parsed_data.pop('seeds')
    result : int = math.inf

    for seed in seeds:
        lookup : int = seed

        for mappings in parsed_data.values():
            for (dst, src, rng) in mappings:
                if 0 <= lookup - src < rng:
                    lookup = dst + lookup - src
                    break

        result = min(result, lookup)

    return result


@challenge
def challenge_5_2(data : str) -> int:
    parsed_data : dict = __challenge_5_data(data)

    seeds : list = parsed_data.pop('seeds')
    results : list[int] = []

    for (isrc, irng) in zip(seeds[::2], seeds[1::2]):
        lookups : list[tuple[int, int]] = [(isrc, isrc + irng)]

        for mappings in parsed_data.values():
            answers : list[tuple[int, int]] = []

            for (mdst, msrc, mrng) in mappings:
                mend = msrc + mrng

                new_lookups : list[tuple[int, int]] = []

                while lookups:
                    (lsrc, lend) = lookups.pop()

                    if lsrc < min(lend, msrc):
                        new_lookups.append((lsrc, min(lend, msrc)))

                    if max(lsrc, msrc) < min(lend, mend):
                        answers.append((
                            max(lsrc, msrc) + mdst - msrc,
                            min(lend, mend) + mdst - msrc,
                        ))

                    if max(lsrc, mend) < lend:
                        new_lookups.append((max(lsrc, mend), lend))

                lookups = new_lookups

            lookups = answers + new_lookups

        if not lookups:
            continue

        results.append(min(lookups)[0])

    return min(results)


@challenge
def challenge_6_1(data : str) -> int:
    re_numbers : re.Pattern = re.compile('[0-9]+')

    races : list[tuple[int, int]] = zip(
        *[
            tuple(map(int, re_numbers.findall(line)))
            for line in data.split('\n')
        ]
    )

    result : int = 1

    for time, distance in races:
        count : int = 0

        for i in range(1, time):
            if i * (time - i) > distance:
                count += 1

        result *= count

    return result

@challenge
def challenge_6_2(data : str) -> int:
    re_numbers : re.Pattern = re.compile('[0-9]+')

    races : list[tuple[int, int]] = zip(
        *[
            [int("".join(re_numbers.findall(line)))]
            for line in data.split('\n')
        ]
    )

    result : int = 1

    for time, distance in races:
        count : int = 0

        for i in range(1, time):
            if i * (time - i) > distance:
                count += 1

        result *= count

    return result


@challenge
def challenge_7_1(data : str) -> int:
    hands : list[tuple[str, str]] = [
        line.split(' ')
        for line in data.split('\n')
    ]

    hand_order : list[tuple] = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 2],
        [1, 2, 2],
        [1, 1, 3],
        [2, 3],
        [1, 4],
        [5],
    ]

    card_order : list[str] = [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'T', 'J', 'Q', 'K', 'A',
    ]

    def __hand_value(hand_data : tuple[str, str]) -> tuple:
        hand, _ = hand_data

        count : collections.Counter = collections.Counter(hand)

        hand_value : int = hand_order.index(sorted(count.values()))
        card_values : list[int] = [
            card_order.index(card)
            for card in hand
        ]

        return (hand_value, *card_values)

    result : int = 0

    for i, (hand, bid) in enumerate(sorted(hands, key=__hand_value), 1):
        result += i * int(bid)

    return result


@challenge
def challenge_7_2(data : str) -> int:
    hands : list[tuple[str, str]] = [
        line.split(' ')
        for line in data.split('\n')
    ]

    hand_order : list[tuple] = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 2],
        [1, 2, 2],
        [1, 1, 3],
        [2, 3],
        [1, 4],
        [5],
    ]

    card_order : list[str] = [
        'J', '2', '3', '4', '5', '6', '7', '8', '9',
        'T', 'Q', 'K', 'A',
    ]

    def __hand_value(hand_data : tuple[str, str]) -> tuple:
        hand, _ = hand_data

        count : collections.Counter = collections.Counter(hand)
        joker_count : int = count.pop('J', 0)

        hand_value : int = 0

        if joker_count == 5:
            hand_value = len(hand_order) - 1
        elif joker_count > 0:
            count_values : list[int] = count.values()

            for i in range(len(count_values)):
                possible_hand : tuple = [c for c in count.values()]
                possible_hand[i] += joker_count
                possible_hand = sorted(possible_hand)

                hand_value = max(hand_value, hand_order.index(possible_hand))
        else:
            hand_value = hand_order.index(sorted(count.values()))

        card_values : list[int] = [
            card_order.index(card)
            for card in hand
        ]

        return (hand_value, *card_values)

    result : int = 0

    for i, (_, bid) in enumerate(sorted(hands, key=__hand_value), 1):
        result += i * int(bid)

    return result


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

    def __gcd(a : int, b : int) -> int:
        while b:
            a, b = b, a % b
        return a

    def __lcm(a : int, b : int) -> int:
        return a * b // __gcd(a, b)

    lengths : list[int] = [
        __length(location)
        for location in map.keys() if location[-1] == 'A'
    ]

    return functools.reduce(__lcm, lengths)


@challenge
def challenge_9_1(data : str) -> int:
    result : int = 0

    def determine_next(seed : list[int]) -> int:
        differences : list[int] = [
            seed[i] - seed[i - 1]
            for i in range(1, len(seed))
        ]

        if all((x == 0 for x in differences)):
            return seed[-1] + differences[-1]

        return seed[-1] + determine_next(differences)

    for line in data.split('\n'):
        numbers : list[int] = [int(i) for i in line.split(' ')]

        result += determine_next(numbers)

    return result


@challenge
def challenge_9_1(data : str) -> int:
    result : int = 0

    def determine_previous(seed : list[int]) -> int:
        print(seed)
        differences : list[int] = [
            seed[i] - seed[i - 1]
            for i in range(1, len(seed))
        ]

        if all((x == 0 for x in differences)):
            return seed[0] - differences[0]

        return seed[0] - determine_previous(differences)

    for line in data.split('\n'):
        numbers : list[int] = [int(i) for i in line.split(' ')]
        print(determine_previous(numbers))

        result += determine_previous(numbers)

    return result


class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f'({self.x}, {self.y})'

U = Vector(0, -1)
D = Vector(0, 1)
L = Vector(-1, 0)
R = Vector(1, 0)
Z = Vector(0, 0)
I = Vector(100, 100)

pipes : dict[str, tuple[Vector]] = {
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
    s_loc = Vector(s_loc % len(ground[0]), s_loc // len(ground[0]))

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
    s_loc = Vector(s_loc % len(ground[0]), s_loc // len(ground[0]))

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

    def process_pipe(check_location : Vector) -> (Vector, int):
        if check_location not in path:
            return check_location, 0

        if R not in ground[check_location.y][check_location.x]:
            return check_location, 1

        exit_location : Vector = check_location + R

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
            l = Vector(x, y)

            if l in path:
                continue

            count = 0

            while l.x < len(ground[0]):
                l, c = process_pipe(l + R)

                count += c

            if count % 2 == 1:
                result += 1

    return result


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
            voids.append(Vector(0, y))

    # Find horizontal voids
    for x in range(width):
        for y in range(height):
            if lines[y][x] == '#':
                break
        else:
            voids.append(Vector(x, 0))

    scale -= 1
    # Find galaxies and expand for voids
    for y in range(height):
        for x in range(width):
            if lines[y][x] == '#':
                x_expand = len([*filter(lambda v: 0 < v.x < x, voids)])
                y_expand = len([*filter(lambda v: 0 < v.y < y, voids)])

                galaxies.append(
                    Vector(x + x_expand * scale, y + y_expand * scale)
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


def main() -> None:
    runner(11)


if __name__ == '__main__':
    main()
