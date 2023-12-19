from common import *


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
