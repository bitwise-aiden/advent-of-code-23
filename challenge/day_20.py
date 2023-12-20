from common import *


def __modules(
    data : str,
) -> dict[str, list]:
    # Create a dictionary of modules
    # key : str = name of module
    # value : ([str*], int, int) = list of receivers, type, state (if any)

    # types:
    # - 0 = button
    # - 1 = broadcaster
    # - 2 = flip-flop
    # - 3 = conjunction
    # - 4 = receiver (unknown / output)
    # - 5 = rx

    modules : dict[str, list] = {
        'button': (['broadcaster'], 0, 0),
        'output': ([], 4, 0),
        'rx': ([], 5, 0),
    }

    conjunction_modules : list[str] = []

    for line in data.split('\n'):
        match line.split(' -> '):
            case ('broadcaster', receivers):
                modules['broadcaster'] = [receivers.split(', '), 1, 0]
            case (name, receivers) if '%' in name:
                modules[name[1:]] = [receivers.split(', '), 2, 0]
            case (name, receivers) if '&' in name:
                modules[name[1:]] = [receivers.split(', '), 3, {}]
                conjunction_modules.append(name[1:])

    # Initialize all connections for conjunction modules
    #   defaults to a low pulse for input

    for module in conjunction_modules:
        for name, (receivers, _, _) in modules.items():
            if module in receivers:
                modules[module][-1][name] = 0


    return modules


def __pulse(
    modules : dict[str, list],
    con_modules : set[str] = set(),
) -> list[int]:
    # Starting with `button`, send a low pulse through the system,
    # monitoring the low and high pulses

    pulses : list[(str, str)] = [('button', 'broadcaster', 0)]
    pulse_count : list[int] = [0, 0]

    while pulses:
        module_from, module_to, pulse = pulses.pop(0)
        receivers, type, state = modules[module_to]

        # print(f'{module_from} -{"high" if pulse else "low"}-> {module_to}')

        pulse_count[pulse] += 1

        match (type, state, pulse):
            case (0 | 1, _, output):
                # button | broadcaster, state ignored, pulse ignored
                pulses.extend(
                    (module_to, receiver, output)
                    for receiver in receivers
                )
            case (2, 0 | 1, 0):
                # flip flop, off | on position, low pulse
                output = modules[module_to][-1] = int(not state)
                pulses.extend(
                    (module_to, receiver, output)
                    for receiver in receivers
                )
            case (2, 0 | 1, 1):
                # flip flop, off | on position, high pulse
                pass
            case (3, state, output):
                # conjunction, connections, pulse ignored
                modules[module_to][-1][module_from] = output
                output = 0 if all(modules[module_to][-1].values()) else 1

                if output: con_modules.add(module_to)

                pulses.extend(
                    (module_to, receiver, output)
                    for receiver in receivers
                )
            case (4, _, output):
                # output, state ignored, pulse ignored
                pass
            case (5, _, 0):
                # rx, state ignored, low pulse
                pass

    return pulse_count


@challenge
def challenge_20_1(data : str) -> int:
    result : int = 0

    modules : dict[str, list] = __modules(data)

    result = math.prod(
        sum(r)
        for r in zip(*[
            __pulse(modules)
            for _ in range(1000)
        ])
    )

    return result


@challenge
def challenge_20_2(data : str) -> int:
    modules : dict[str, list] = __modules(data)
    target_modules, found_modules = {'dc', 'rv', 'vp', 'cq'}, set()
    module_cycles, cycle_count = {}, 0

    while target_modules - found_modules:
        cycle_count += 1

        __pulse(modules, found_modules)

        for module in found_modules:
            if module not in module_cycles:
                module_cycles[module] = cycle_count



    return functools.reduce(
        lcm,
        (module_cycles[target] for target in target_modules),
    )
