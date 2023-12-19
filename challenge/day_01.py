from common import *


@challenge
def challenge_1_1(data : str) -> int:
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
