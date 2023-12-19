from common import *


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
