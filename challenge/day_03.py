from common import *


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
