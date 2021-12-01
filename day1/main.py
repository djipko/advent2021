#!/usr/bin/env python3
from itertools import pairwise
from more_itertools import triplewise


def increases(ms):
    return sum(1 if snd > fst else 0 for fst, snd in pairwise(ms))


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [int(line.strip()) for line in data.split("\n") if line]
    print(increases(lines))
    print(increases(map(sum, triplewise(lines))))
