#!/usr/bin/env python3

import itertools


def adj(octopi, x, y):
    xs = (x - 1, x, x + 1)
    ys = (y - 1, y, y + 1)
    for xc in xs:
        for yc in ys:
            if (
                0 <= xc < len(octopi[0])
                and 0 <= yc < len(octopi)
                and (xc, yc) != (x, y)
            ):
                yield (xc, yc)


def step(octopi):
    w = len(octopi[0])
    h = len(octopi)
    flashes = 0
    flashed = set()
    for y in range(h):
        for x in range(w):
            flashes += flash(octopi, x, y, flashed)
    return flashes


def flash(octopi, x, y, flashed):
    if (x, y) in flashed:
        return 0
    flashes = 0
    octopi[y][x] += 1
    if octopi[y][x] > 9:
        octopi[y][x] = 0
        flashed.add((x, y))
        flashes += 1
        for ax, ay in adj(octopi, x, y):
            flashes += flash(octopi, ax, ay, flashed)
    return flashes


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()
    lines = [line.strip() for line in data.split("\n")]
    octopi = [list(map(int, l)) for l in lines]
    flashes = 0
    for i in range(100):
        flashes += step(octopi)
    print(flashes)
    octopi = [list(map(int, l)) for l in lines]
    for i in itertools.count():
        step(octopi)
        if all(all(o == 0 for o in row) for row in octopi):
            print(i + 1)
            break
