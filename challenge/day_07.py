from common import *


@challenge
def challenge_7_1(data : str) -> int:
    hands : list[tuple[str, str]] = [
        line.split(' ')
        for line in data.split('\n')
    ]

    hand_order : list[tuple] = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 2],
        [1, 2, 2],
        [1, 1, 3],
        [2, 3],
        [1, 4],
        [5],
    ]

    card_order : list[str] = [
        '2', '3', '4', '5', '6', '7', '8', '9',
        'T', 'J', 'Q', 'K', 'A',
    ]

    def __hand_value(hand_data : tuple[str, str]) -> tuple:
        hand, _ = hand_data

        count : collections.Counter = collections.Counter(hand)

        hand_value : int = hand_order.index(sorted(count.values()))
        card_values : list[int] = [
            card_order.index(card)
            for card in hand
        ]

        return (hand_value, *card_values)

    result : int = 0

    for i, (hand, bid) in enumerate(sorted(hands, key=__hand_value), 1):
        result += i * int(bid)

    return result


@challenge
def challenge_7_2(data : str) -> int:
    hands : list[tuple[str, str]] = [
        line.split(' ')
        for line in data.split('\n')
    ]

    hand_order : list[tuple] = [
        [1, 1, 1, 1, 1],
        [1, 1, 1, 2],
        [1, 2, 2],
        [1, 1, 3],
        [2, 3],
        [1, 4],
        [5],
    ]

    card_order : list[str] = [
        'J', '2', '3', '4', '5', '6', '7', '8', '9',
        'T', 'Q', 'K', 'A',
    ]

    def __hand_value(hand_data : tuple[str, str]) -> tuple:
        hand, _ = hand_data

        count : collections.Counter = collections.Counter(hand)
        joker_count : int = count.pop('J', 0)

        hand_value : int = 0

        if joker_count == 5:
            hand_value = len(hand_order) - 1
        elif joker_count > 0:
            count_values : list[int] = count.values()

            for i in range(len(count_values)):
                possible_hand : tuple = [c for c in count.values()]
                possible_hand[i] += joker_count
                possible_hand = sorted(possible_hand)

                hand_value = max(hand_value, hand_order.index(possible_hand))
        else:
            hand_value = hand_order.index(sorted(count.values()))

        card_values : list[int] = [
            card_order.index(card)
            for card in hand
        ]

        return (hand_value, *card_values)

    result : int = 0

    for i, (_, bid) in enumerate(sorted(hands, key=__hand_value), 1):
        result += i * int(bid)

    return result
