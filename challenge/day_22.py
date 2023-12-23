from common import *


class Brick():
    def __init__(self, id, points : list[Vector3]) -> None:
        self.id = id
        self.points = points
        self.supported = set()
        self.supporting = set()

    def is_supported(self) -> bool:
        return len(self.supported) > 0

    def is_supported_without(self, *bricks) -> bool:
        return len(self.supported - set(bricks)) > 0

    def is_supporting(self) -> bool:
        return len(self.supporting) > 0

    def supports(self, brick) -> None:
        self.supporting.add(brick)
        brick.support(self)

    def support(self, brick) -> None:
        self.supported.add(brick)

    def update_height(self, bottom : int) -> None:
        lowest : int = min([p.z for p in self.points])
        delta : int = bottom - lowest

        for point in self.points:
            point.z += delta

    def lowest(self) -> int:
        return min(p.z for p in self.points)

    def heightest(self) -> int:
        return max(p.z for p in self.points)

    def __iter__(self):
        return iter(self.points)

    def __str__(self):
        return f'<brick {self.id}: {str(self.points)}>'

    def __repr__(self):
        return f'<brick {self.id}: {str(self.points)}>'

    def __hash__(self):
        return hash(self.id)


def __bricks(data : str) -> list[Brick]:
    bricks : list[tuple[Vector3]] = []

    for line in data.splitlines():
        a, b = line.split('~')

        a : Vector3 = Vector3(*map(int, a.split(',')))
        b : Vector3 = Vector3(*map(int, b.split(',')))

        if a != b:
            delta : Vector3 = b - a
            length : int = len(delta)
            delta = delta / length

            points : list[int] = []

            for i in range(length + 1):
                points.append(a + delta * i)

            bricks.append(Brick(len(bricks), points))
        else:
            bricks.append(Brick(len(bricks), [a]))

    fallen_bricks = {
        # Vector2 : {
        #   int : brick
        # }
    }

    for brick in sorted(bricks, key=lambda ps: ps.lowest()):
        possible_supports : list[(int, Brick)] = []

        for point in brick:
            p2 = point.to_vector2()
            if p2 in fallen_bricks:
                max_height = max(fallen_bricks[p2].keys())
                possible_supports.append((
                    max_height,
                    fallen_bricks[p2][max_height],
                ))

        if possible_supports:
            height, _ = max(possible_supports, key=lambda s: s[0])

            for sh, s in possible_supports:
                if sh == height:
                    s.supports(brick)

            brick.update_height(height + 1)
        else:
            brick.update_height(1)

        for point in brick:
            p2 = point.to_vector2()
            fallen_bricks[p2] = fallen_bricks.get(p2, {})
            fallen_bricks[p2][point.z] = brick

    return bricks


@challenge
def challenge_22_1(data : str) -> int:
    result : int = 0

    for brick in __bricks(data):
        if (
            not brick.is_supporting() or
            all(len(b.supported) > 1 for b in brick.supporting)
        ):
            result += 1

    return result



@challenge
def challenge_22_2(data : str) -> int:
    result : int = 0

    bricks = {b.id: b for b in __bricks(data)}

    for id, brick in bricks.items():
        solo_support = list(filter(lambda s: len(s.supported) == 1, brick.supporting))
        will_fall = {brick, *solo_support}

        while solo_support:
            b = solo_support.pop()

            for s in b.supporting - will_fall:
                if len(s.supported - will_fall) == 0:
                    solo_support.append(s)
                    will_fall.add(s)

        result += len(will_fall) - 1

    return result
