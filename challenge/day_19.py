from common import *


class XMAS:
    def __init__(self, x = None, m  = None, a  = None, s  = None):
        self.x = x
        self.m = m
        self.a = a
        self.s = s


    def __copy__(self):
        return XMAS(self.x, self.m, self.a, self.s)


    def __iter__(self):
        return iter((self.x, self.m, self.a, self.s))


    def __lshift__(self, other):
        if other.x: self.x = other.x
        if other.m: self.m = other.m
        if other.a: self.a = other.a
        if other.s: self.s = other.s

        return self


def __workflows_1(data : str) -> dict[str, callable]:
    re_rule : re.Pattern = re.compile('([a-z])(\<|\>)([0-9]+):([a-zA-Z]+)')

    workflows : dict[str, callable] = {
        'R': lambda _1, _2: False,
        'A': lambda xmas, _: True
    }

    for line in data.split('\n'):
        name, rules = line.split('{')
        rules = rules.split(',')

        rule_str : str = f'lambda xmas, rules: '

        for rule in rules[:-1]:
            var, op, cond, res = re_rule.match(rule).groups()

            rule_str += f' (rules["{res}"](xmas, rules) if xmas.{var} {op} {cond} else '

        rule_str += f' rules["{rules[-1][:-1]}"](xmas, rules)){")" * (len(rules) - 2)}'

        workflows[name] = eval(rule_str)

    return workflows


def __workflows_2(data : str) -> dict[str, callable]:
    re_rule : re.Pattern = re.compile('([a-z])(\<|\>)([0-9]+):([a-zA-Z]+)')

    workflows : dict[str, callable] = {
        'R': lambda _1, _2: 0,
        'A': lambda xmas, _: math.prod(b - a + 1 for a, b in xmas)
    }

    for line in data.split('\n'):
        name, rules = line.split('{')
        rules = rules.split(',')

        rule_str : str = f'lambda xmas, rules: sum(['

        operations = {
            '>': lambda v, c: (f'{c} + 1', f'xmas.{v}[1]', f'xmas.{v}[0]', f'{c}'),
            '<': lambda v, c: (f'xmas.{v}[0]', f'{c} - 1', f'{c}', f'xmas.{v}[1]'),
        }

        carry_over = []

        for rule in rules[:-1]:
            var, op, cond, res = re_rule.match(rule).groups()

            a, b, *remainder = operations[op](var, cond)

            carry = " << ".join(f'XMAS({v}=({ra, rb}))' for v, ra, rb in carry_over) or 'XMAS()'
            check = f'if {carry_over[-1][1]} <= {carry_over[-1][2]} else 0' if carry_over else ''
            rule_str += f'rules["{res}"](copy(xmas) << XMAS({var}=({a}, {b})) << {carry}, rules) {check},'

            carry_over.append((var, *remainder))

        carry = " << ".join(f'XMAS({v}=({ra, rb}))' for v, ra, rb in carry_over)
        check = f'if {carry_over[-1][1]} <= {carry_over[-1][2]} else 0' if carry_over else ''
        rule_str += f'rules["{rules[-1][:-1]}"](copy(xmas) << {carry or "XMAS()"}, rules) {check}])'

        print(rule_str)

        workflows[name] = eval(rule_str.replace('\'', ''))
        # 300319813012433

    return workflows



def __parts(data : str) -> list[XMAS]:
    parts : list[XMAS] = []

    for line in data.split('\n'):
        parts.append(eval(f'XMAS({line[1:-1]})'))

    return parts


@challenge
def challenge_19_1(data : str) -> int:
    workflows, parts = data.split('\n\n')
    workflows, parts = __workflows_1(workflows), __parts(parts)

    return sum(
        sum(part)
        for part in parts
        if workflows['in'](part, workflows)
    )


@challenge
def challenge_19_2(data : str) -> int:
    result : int = 0

    workflows, _ = data.split('\n\n')
    workflows = __workflows_2(workflows)

    xmas = XMAS((1, 4000), (1, 4000), (1, 4000), (1, 4000))

    result = workflows['in'](xmas, workflows)

    return result
