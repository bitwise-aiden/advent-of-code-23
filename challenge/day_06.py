from common import *


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
