from common import *


def __workflows(data : str) -> dict[str, (str, callable, int, str)]:
    workflows : dict[str, list[(str, callable, int, str)]] = {}

    re_rule : re.Pattern = re.compile('([a-z])([\>\<])([0-9]+):([a-zA-Z]+)')

    for line in data.split('\n'):
        name, rules = line[:-1].split('{')
        *rules, fallback = rules.split(',')

        workflows[name] = []

        for rule in rules:
            var, op, comp, fn = re_rule.match(rule).groups()

            workflows[name].append((
                var,
                int.__lt__ if op == '<' else int.__gt__,
                int(comp),
                fn,
            ))

        workflows[name].append((None, None, None, fallback))

    return workflows


def __parts(data : str) -> list[dict[str, int]]:
    return [
        eval(f'dict({line[1:-1]})')
        for line in data.split('\n')
    ]


def __check(part, workflows, current):
    if current == 'R': return False
    if current == 'A': return True

    *rules, fallback = workflows[current]

    for var, op, comp, fn in rules:
        if op(part[var], comp):
            return __check(part, workflows, fn)

    return __check(part, workflows, fallback[-1])


def __permutations(part, workflows, current):
    if current == 'R': return 0
    if current == 'A': return math.prod(b - a + 1 for a, b in part.values())

    *rules, fallback = workflows[current]
    count, remainder = 0, dict(part)

    for var, op, cmp, fn in rules:
        a, b = ra, rb = remainder[var]

        if op == int.__lt__:
            b, ra = cmp - 1, cmp
        else:
            a, rb = cmp + 1, cmp

        if a <= b:
            count += __permutations({**remainder, var: (a, b)}, workflows, fn)

        if ra > rb:
            break

        remainder[var] = (ra, rb)
    else:
        count += __permutations(remainder, workflows, fallback[-1])

    return count


@challenge
def challenge_19_1(data : str) -> int:
    result : int = 0

    workflows, parts = data.split('\n\n')
    workflows, parts = __workflows(workflows), __parts(parts)

    for part in parts:
        if __check(part, workflows, 'in'):
            result += sum(part.values())

    return result


@challenge
def challenge_19_2(data : str) -> int:
    workflows, _ = data.split('\n\n')
    workflows = __workflows(workflows)

    return __permutations({k: (1, 4000) for k in 'xmas'}, workflows, 'in')
