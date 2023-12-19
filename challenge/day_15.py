from common import *


def __challenge_15_hash(value : str) -> int:
    result : int = 0

    for c in value:
        result += ord(c)
        result *= 17
        result = result % 256

    return result


@challenge
def challenge_15_1(data : str) -> int:
    return sum(__challenge_15_hash(v) for v in data.split(','))


@challenge
def challenge_15_2(data : str) -> int:
    result : int = 0

    boxes : list[dict[str, int]] = [{} for i in range(256)]

    re_op : re.Pattern = re.compile(r'([a-z]+)(\=([0-9]+)|-)')

    for label, _, op in re_op.findall(data):
        label_hash : int = __challenge_15_hash(label)
        if op:
            boxes[label_hash][label] = int(op)
        elif label in boxes[label_hash]:
            del boxes[label_hash][label]

    for i, box in enumerate(boxes):
        for j, lense in enumerate(box.values()):
            result += (i + 1) * (j + 1) * lense

    return result
