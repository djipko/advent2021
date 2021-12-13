#!/usr/bin/env python3

from collections import defaultdict


class Paper:
    def __init__(self, dots):
        self.xs = defaultdict(set)
        self.ys = defaultdict(set)
        for x, y in dots:
            self.xs[x].add(y)
            self.ys[y].add(x)

    def fold_along(self, axis, d):
        modify = self.xs if axis == "x" else self.ys
        other = self.ys if axis == "x" else self.xs
        to_fold = [dd for dd in modify.keys() if dd > d]
        for dd in to_fold:
            new_d = d - dd + d
            modify[new_d] |= modify.pop(dd)
        for dist in other.keys():
            other[dist] = set(dd if dd <= d else d - dd + d for dd in other[dist])

    def display(self):
        for y, xs in sorted(self.ys.items()):
            w = max(xs)
            line = ["#" if x in xs else "." for x in range(w + 1)]
            print("".join(line))


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    dots = [
        list(map(int, line.split(",")))
        for line in lines
        if line and not line.startswith("fold")
    ]
    instructions = [line[11:].split("=") for line in lines if line.startswith("fold")]
    paper = Paper(dots)
    axis, d = instructions[0]
    paper.fold_along(axis, int(d))
    print(sum(len(xx) for xx in paper.xs.values()))

    for axis, d in instructions[1:]:
        paper.fold_along(axis, int(d))
    paper.display()
