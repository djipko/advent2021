#!/usr/bin/env python3

from dataclasses import dataclass
import math
import itertools


def add(left, right):
    return [left, right]


@dataclass
class Regular:
    num: int


def build_tree(pair):
    left, right = pair
    if isinstance(left, list):
        left = build_tree(left)
    else:
        left = Regular(left)
    if isinstance(right, list):
        right = build_tree(right)
    else:
        right = Regular(right)
    return [left, right]


class Transformer:
    def __init__(self, tree):
        self.tree = tree
        self.prev = None
        self.to_add = None
        self.exploded = False
        self.split = False

    def apply_one(self):
        self.exploded = False
        self.split = False
        self.tree = self._dfs(self.tree)
        self.prev = None
        self.to_add = None
        return self.exploded or self.split

    def transform(self):
        while self.apply_one():
            pass

    def _dfs(self, tree, lvl=1):
        if isinstance(tree, Regular):
            self.prev = tree
            if self.to_add is not None:
                tree.num += self.to_add
                self.to_add = None
            if tree.num >= 10 and not self.split and not self.exploded:
                self.split = True
                return [
                    Regular(math.floor(tree.num / 2)),
                    Regular(math.ceil(tree.num / 2)),
                ]

            return tree
        left, right = tree
        if lvl == 5:
            if not self.exploded:
                if self.prev is not None:
                    self.prev.num += left.num
                self.to_add = right.num
                self.exploded = True
                self.split = False
                return Regular(0)
        return [self._dfs(left, lvl + 1), self._dfs(right, lvl + 1)]

    def magnitude(self):
        def _dfs_mag(tree):
            if isinstance(tree, Regular):
                return tree.num
            else:
                left, right = tree
                return 3 * _dfs_mag(left) + 2 * _dfs_mag(right)

        return _dfs_mag(self.tree)


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()
    ns = [build_tree(eval(line.strip())) for line in data.split("\n")]
    trans = None
    for n in ns:
        if not trans:
            trans = Transformer(n)
        else:
            trans.tree = add(trans.tree, n)
        trans.transform()
    print(trans.magnitude())
    ss = []
    ls = [line.strip() for line in data.split("\n")]
    for l1, l2 in itertools.permutations(ls, 2):
        t = Transformer(add(build_tree(eval(l1)), build_tree(eval(l2))))
        t.transform()
        ss.append(t.magnitude())
    print(max(ss))
