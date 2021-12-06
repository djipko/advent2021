#!/usr/bin/env python3

from collections import defaultdict


class Fish:
    def __init__(self, timer):
        self.timer = timer

    def tick(self):
        if self.timer == 0:
            self.timer = 6
            return Fish(8)
        self.timer -= 1


class FishGen:
    def __init__(self, timers):
        self.gen = defaultdict(int)
        for t in timers:
            self.gen[t] += 1

    def tick(self):
        new_fish = self.gen.get(0, 0)
        gen_6 = new_fish
        for i in range(1, 9):
            self.gen[i - 1] = self.gen.get(i, 0)
        self.gen[8] = new_fish
        self.gen[6] += gen_6

    def total(self):
        return sum(self.gen.values())


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    fish = [Fish(int(t)) for t in lines[0].split(",")]
    fish_gen = FishGen(map(int, lines[0].split(",")))

    # Naive implementation
    for i in range(80):
        new_gen = []
        for f in fish:
            new = f.tick()
            if new:
                new_gen.append(new)
        fish.extend(new_gen)
    print(len(fish))

    # Keep track of gens
    for i in range(80):
        fish_gen.tick()
    print(fish_gen.total())
    fish_gen = FishGen(map(int, lines[0].split(",")))
    for i in range(256):
        fish_gen.tick()
    print(fish_gen.total())
