import collections
from copy import copy
import functools
import math
import re
import queue
import time

count : int = 1
challenges : list[callable] = []

def challenge(
    func : callable
) -> None:
    global count

    count += 1

    day : int = count // 2
    ch : int = count % 2 + 1

    def challenge_runner():
        data : str = input_data(day)

        start, result, end = time.time(), func(data), time.time()

        print(f'day {day}, challenge {ch} ({end - start:0.3f} ms): {result}')

    challenges.append(challenge_runner)


def input_data(day : int) -> str:
    with open(f'./data/day_{day:02d}_input', 'r') as in_file:
        return in_file.read().split('$---$')[0].strip()


def runner(day : int = -1) -> None:
    challenges_to_run : list[callable] = challenges

    day -= 1

    if day >= 0:
        challenges_to_run = challenges[day * 2:day * 2 + 2]

    for challenge in challenges_to_run:
        challenge()


class Vector2():
    def __init__(self, x, y = None, _type=int):
        self.x = _type(x)
        self.y = _type(y if y != None else x)
        self._type = _type

    def x_get(self):
        return self.x

    def x_set(self, value):
        self.x = value

    def y_get(self):
        return self.y

    def y_set(self, value):
        self.y = value

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def neighbours(self) -> tuple:
        return tuple(self + n for n in [U, D, L, R])

    def inside(self, bounds : tuple) -> bool:
        return (
            bounds[0].x <= self.x < bounds[1].x and
            bounds[0].y <= self.y < bounds[1].y
        )

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y, self._type)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __len__(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def __mul__(self, scalar):
        if isinstance(scalar, Vector2):
            return Vector2(self.x * scalar.x, self.y * scalar.y, self._type)

        return Vector2(self.x * scalar, self.y * scalar, self._type)

    def __neg__(self):
        return Vector2(-self.x, -self.y, self._type)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y, self._type)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'({self.x}, {self.y})'


U = Vector2(0, -1)
D = Vector2(0, 1)
L = Vector2(-1, 0)
R = Vector2(1, 0)
Z = Vector2(0, 0)
I = Vector2(100, 100)

class Vector3(Vector2):
    def __init__(self, x, y = None, z = None, _type=int):
        self.x = _type(x)
        self.y = _type(y if y != None else x)
        self.z = _type(z if z != None else x)
        self._type = _type

    def z_get(self):
        return self.z

    def z_set(self, value):
        self.z = value

    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
            self._type
        )

    def neighbours(self) -> tuple:
        ns = []

        for n in super():
            for i in range(-1, 2):
                ns.append(Vector3(n.x, n.y, i, self._type))

        return ns

    def inside(self, bounds : tuple) -> bool:
        return (
            super() and
            bounds[0].z <= self.z < bounds[1].z
        )

    def to_v2(self) -> Vector2:
        return Vector2(self.x, self.y, self._type)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z, self._type)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __lt__(self, other):
        return self.x <= other.x and self.y <= other.y and self.z <= other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __len__(self):
        return int(math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2))

    def __mul__(self, scalar):
        if isinstance(scalar, Vector3):
            return Vector3(
                self.x * scalar.x,
                self.y * scalar.y,
                self.z * scalar.z,
                self._type
            )

        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar, self._type)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z, self._type)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z, self._type)

    def __div__(self, other):
        return Vector3(self.x // other, self.y // other, self.z // other, self._type)

    def __truediv__(self, other):
        return Vector3(self.x // other, self.y // other, self.z // other, self._type)

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def __repr__(self) -> str:
        return f'({self.x}, {self.y}, {self.z})'

U3 = Vector3(0, -1, 0)
D3 = Vector3(0, 1, 0)
L3 = Vector3(-1, 0, 0)
R3 = Vector3(1, 0, 0)
F3 = Vector3(0, 0, 1)
B3 = Vector3(0, 0, -1)
Z3 = Vector3(0, 0, 0)


def gcd(a : int, b : int) -> int:
    while b:
        a, b = b, a % b
    return a

def lcm(a : int, b : int) -> int:
    return a * b // gcd(a, b)


def sign(value : int) -> int:
    if value < 0:
        return -1

    if value > 0:
        return 1

    return 0
