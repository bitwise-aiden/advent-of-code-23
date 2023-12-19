from common import *


def __challenge_5_data(data : str) -> dict:
    seeds, *sections = data.split('\n\n')

    re_numbers : re.Pattern = re.compile('[0-9]+')

    result : dict = {
        'seeds': [*map(int, re_numbers.findall(seeds))]
    }

    for section in sections:
        name, *values = section.split('\n')
        result[name[:-5]] = [
            [*map(int, re_numbers.findall(value))]
            for value in values
        ]

    return result


@challenge
def challenge_5_1(data : str) -> int:
    parsed_data : dict = __challenge_5_data(data)

    seeds : list = parsed_data.pop('seeds')
    result : int = math.inf

    for seed in seeds:
        lookup : int = seed

        for mappings in parsed_data.values():
            for (dst, src, rng) in mappings:
                if 0 <= lookup - src < rng:
                    lookup = dst + lookup - src
                    break

        result = min(result, lookup)

    return result


@challenge
def challenge_5_2(data : str) -> int:
    parsed_data : dict = __challenge_5_data(data)

    seeds : list = parsed_data.pop('seeds')
    results : list[int] = []

    for (isrc, irng) in zip(seeds[::2], seeds[1::2]):
        lookups : list[tuple[int, int]] = [(isrc, isrc + irng)]

        for mappings in parsed_data.values():
            answers : list[tuple[int, int]] = []

            for (mdst, msrc, mrng) in mappings:
                mend = msrc + mrng

                new_lookups : list[tuple[int, int]] = []

                while lookups:
                    (lsrc, lend) = lookups.pop()

                    if lsrc < min(lend, msrc):
                        new_lookups.append((lsrc, min(lend, msrc)))

                    if max(lsrc, msrc) < min(lend, mend):
                        answers.append((
                            max(lsrc, msrc) + mdst - msrc,
                            min(lend, mend) + mdst - msrc,
                        ))

                    if max(lsrc, mend) < lend:
                        new_lookups.append((max(lsrc, mend), lend))

                lookups = new_lookups

            lookups = answers + new_lookups

        if not lookups:
            continue

        results.append(min(lookups)[0])

    return min(results)
