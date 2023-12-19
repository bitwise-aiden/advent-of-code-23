from common import *



__re_can_fit : re.Pattern = re.compile('^[\?#]+$')

@functools.cache
def find_fits(string : str, count : int) -> list[int]:
    result : list[int] = []

    if count > len(string):
        return result

    if count == len(string) and __re_can_fit.match(string):
        return [count]

    for i in range(len(string) - count + 1):
        if '#' in string[:i]:
            continue

        if not __re_can_fit.match(string[i:i + count]):
            continue

        if (i + count < len(string) and string[i + count] != '#') or i + count == len(string):
            result.append(i + count)

    return result


@functools.cache
def __challenge_12_calculate(springs : str, counts : tuple[int]) -> int:
    if len(counts) == 0:
        return 0 if "#" in springs else 1

    result : int = 0

    count, *remaining = counts
    required_space = sum(remaining) + len(remaining)

    for i in find_fits(springs[:len(springs) - required_space + 1], count):
        result += __challenge_12_calculate(springs[i + 1:], tuple(remaining))

    return result


@challenge
def challenge_12_1(data : str) -> int:
    result : int = 0

    for line in data.split('\n'):
        springs, counts = line.split(' ')
        counts = tuple(int(c) for c in counts.split(','))

        result += __challenge_12_calculate(springs, counts)

    return result


@challenge
def challenge_12_2(data : str) -> int:
    result : int = 0

    for line in data.split('\n'):
        springs, counts = line.split(' ')
        springs = "?".join([springs] * 5)
        counts = tuple(int(c) for c in counts.split(',')) * 5

        result += __challenge_12_calculate(springs, counts)

    return result
