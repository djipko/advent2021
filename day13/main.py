#!/usr/bin/env python3

from collections import defaultdict


class Paper:
    def __init__(self, dots):
        self.ys = defaultdict(set)
        for x, y in dots:
            self.ys[y].add(x)

    def fold_along(self, axis, d):
        match axis:
            case "x":
                for y in self.ys.keys():
                    self.ys[y] = set(x if x <= d else 2 * d - x for x in self.ys[y])
            case "y":
                to_fold = [y for y in self.ys.keys() if y > d]
                for y in to_fold:
                    new_y = 2 * d - y
                    self.ys[new_y] |= self.ys.pop(y)

    def dot_count(self):
        return sum(len(yy) for yy in paper.ys.values())

    def display(self):
        for y, xs in sorted(self.ys.items()):
            w = max(xs)
            line = ["#" if x in xs else " " for x in range(w + 1)]
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
    print(paper.dot_count())

    for axis, d in instructions[1:]:
        paper.fold_along(axis, int(d))
    paper.display()
