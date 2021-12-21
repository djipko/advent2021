#!/usr/bin/env python3

from dataclasses import dataclass
from functools import lru_cache
from itertools import cycle, count, combinations, product
from more_itertools import chunked, flatten
import math
import sys


@dataclass(frozen=True)
class Player:
    pos: int
    score: int


universes = list(map(sum, product((1, 2, 3), repeat=3)))


@lru_cache(maxsize=100000)
def _quantum_game(p1, p2, throw, p1_move=True):
    p = p1 if p1_move else p2
    new_pos = (p.pos + throw - 1) % 10 + 1
    new_score = p.score + new_pos
    if new_score >= 21:
        return (1, 0) if p1_move else (0, 1)
    new_p = Player(new_pos, new_score)

    p1 = new_p if p1_move else p1
    p2 = new_p if not p1_move else p2
    for throw in universes:
        return tuple(
            sum(p)
            for p in zip(
                *(_quantum_game(p1, p2, throw, not p1_move) for throw in universes)
            )
        )


def quantum_game(p1, p2):
    return tuple(
        sum(p) for p in zip(*(_quantum_game(p1, p2, initial) for initial in universes))
    )


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]

    p1_pos = int(lines[0].split(" ")[-1])
    p2_pos = int(lines[1].split(" ")[-1])
    p1 = [p1_pos, 0]
    p2 = [p2_pos, 0]

    die = chunked(cycle(range(1, 10001)), 3)
    players = cycle((p1, p2))

    for roll, throw, p in zip(count(3, 3), die, players):
        t = sum(throw)
        p[0] = (p[0] + t - 1) % 10 + 1
        p[1] += p[0]
        if p[1] >= 1000:
            break
    print(min(p1[1], p2[1]) * roll)

    p1 = Player(p1_pos, 0)
    p2 = Player(p2_pos, 0)
    ps = quantum_game(p1, p2)
    print(max(ps))
