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
        return in_file.read().strip()


def runner(day : int = -1) -> None:
    challenges_to_run : list[callable] = challenges

    day -= 1

    if day >= 0:
        challenges_to_run = challenges[day * 2:day * 2 + 2]

    for challenge in challenges_to_run:
        challenge()


class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def x_get(self):
        return self.x

    def x_set(self, value):
        self.x = value

    def y_get(self):
        return self.y

    def y_set(self, value):
        self.y = value

    def neighbours(self) -> tuple:
        return tuple(self + n for n in [U, D, L, R])

    def inside(self, bounds : tuple) -> bool:
        return (
            bounds[0].x <= self.x < bounds[1].x and
            bounds[0].y <= self.y < bounds[1].y
        )

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f'({self.x}, {self.y})'

U = Vector(0, -1)
D = Vector(0, 1)
L = Vector(-1, 0)
R = Vector(1, 0)
Z = Vector(0, 0)
I = Vector(100, 100)
