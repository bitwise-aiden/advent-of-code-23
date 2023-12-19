from common import *


@challenge
def challenge_14_1(data : str) -> int:
    result : int = 0

    columns : dict[int, int] = {}
    lines : list[str] = data.split('\n')
    size : int = len(lines)

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            curr : int = columns.get(j, 0)

            match char:
                case 'O':
                    result += size - curr
                    columns[j] = curr + 1
                case '#':
                    columns[j] = i + 1

    return result


@challenge
def challenge_14_2(data : str) -> int:
    result : int = 0

    return result
