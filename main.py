import re

count = 1
challenges = []

def challenge(
    func : callable
) -> None:
    global count

    count += 1

    day = count // 2
    ch = count % 2


    def challenge_runner():
        data : str = input_data(day)
        print(f'day {day}, challenge {ch}: {func(data)}')

    challenges.append(challenge_runner)


def input_data(day : int) -> str:
    with open(f'./data/day_{day:02d}_input', 'r') as in_file:
        return in_file.read().strip()


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


def main() -> None:
    for challenge in challenges:
        challenge()


if __name__ == '__main__':
    main()
