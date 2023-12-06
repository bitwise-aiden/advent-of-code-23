import math
import re

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
        print(f'day {day}, challenge {ch}: {func(data)}')

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



def main() -> None:
    runner(5)


if __name__ == '__main__':
    main()
