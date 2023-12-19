from common import *


@challenge
def challenge_13_1(data : str) -> int:
    result : int = 0

    sands = data.split('\n\n')

    def find_mirror(sands : list[str]) -> int:
        for i in range(1, len(sands)):
            if all(a == b for a, b in zip(sands[i:], sands[:i][::-1])):
                return i

        return 0

    for sands in data.split('\n\n'):
        vsands : list[str] = sands.split('\n')
        hsands : list[str] = [
            sands[i::len(vsands[0]) + 1]
            for i in range(len(vsands[0]))
        ]

        result += find_mirror(hsands) + find_mirror(vsands) * 100

    return result


@challenge
def challenge_13_2(data : str) -> int:
    result : int = 0

    def find_smudged_mirror(sands : list[str]) -> int:
        for i in range(1, len(sands)):
            diff_count : int = 0

            for a, b in zip(sands[i:], sands[:i][::-1]):
                diff_count += sum(not j == k for j, k in zip(a, b))

            if diff_count == 1:
                return i

        return 0

    for sands in data.split('\n\n'):
        vsands : list[str] = sands.split('\n')
        hsands : list[str] = [
            sands[i::len(vsands[0]) + 1]
            for i in range(len(vsands[0]))
        ]

        result += find_smudged_mirror(hsands) + find_smudged_mirror(vsands) * 100

    return result
