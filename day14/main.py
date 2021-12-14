#!/usr/bin/env python3

from more_itertools import pairwise, chunked
from collections import Counter
from functools import lru_cache
import math


class Poly:
    def __init__(self, rules):
        self.rules = {}
        for rule in rules:
            pair, ins = rule.split(" -> ")
            self.rules[pair] = ins
            self.cache = {}

    @lru_cache(maxsize=1024)
    def step(self, run):
        """This one was actually fairly OK but broke down after 30 steps"""
        l = len(run)
        if l == 1:
            return run
        elif l == 2:
            return f"{run[0]}{self.rules[run]}{run[1]}"
        else:
            fst, snd = self.step2(run[: l // 2]), self.step2(run[l // 2 :])
            mid = f"{fst[-1]}{snd[0]}"
            return f"{fst}{self.rules[mid]}{snd}"


class Ch:
    def __init__(self, c):
        self.c = c
        self.nxt = None


class Str:
    def __init__(self, rules, chain):
        self.rules = {}
        self.start = None
        for rule in rules:
            pair, ins = rule.split(" -> ")
            self.rules[tuple(pair)] = ins
        self._build_str(chain)

    def _build_str(self, chain):
        cur = None
        for c in chain:
            nxt = Ch(c)
            if not self.start:
                self.start = nxt
            else:
                cur.nxt = nxt
            cur = nxt

    def iter(self):
        cur = self.start
        while cur:
            yield cur.c
            cur = cur.nxt

    def step(self):
        fst, snd = self.start, self.start.nxt
        while snd and fst:
            ins = Ch(self.rules[(fst.c, snd.c)])
            fst.nxt = ins
            ins.nxt = snd
            fst = snd
            snd = snd.nxt


class PairPoly:
    def __init__(self, rules, template):
        self.rules = {}
        for rule in rules:
            pair, ins = rule.split(" -> ")
            self.rules[pair] = ins
            self.cache = {}
        self.pairs = Counter("".join(pair) for pair in pairwise(template))
        self.start = template[0]
        self.end = template[-1]

    def step(self):
        new_pairs = Counter()
        for pair, cnt in self.pairs.items():
            ins = self.rules[pair]
            new_pairs[f"{pair[0]}{ins}"] += cnt
            new_pairs[f"{ins}{pair[1]}"] += cnt
        self.pairs = +new_pairs

    def count(self):
        c = Counter()
        for pair, cnt in self.pairs.items():
            c[pair[0]] += cnt
            c[pair[1]] += cnt
        c = Counter({ch: math.ceil(cnt / 2) for ch, cnt in c.items()})
        if self.start == self.end:
            c[self.start] += 1
        return c


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    start = lines[0]
    rules = lines[2:]
    s = Str(rules, start)
    for i in range(10):
        s.step()
    c = Counter(s.iter())
    print(c.most_common()[0][1] - c.most_common()[-1][1])

    # poly = Poly(rules)
    # for i in range(30):
    #     start = poly.step(start)
    #     print(poly.step.cache_info())
    # c = Counter(start)
    # print(c.most_common()[0][1] - c.most_common()[-1][1])

    poly = PairPoly(rules, start)
    for i in range(40):
        poly.step()

    c = poly.count()
    print(c.most_common()[0][1] - c.most_common()[-1][1])
