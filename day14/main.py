#!/usr/bin/env python3

from more_itertools import pairwise, chunked
from collections import Counter
from functools import lru_cache

c = {}
hits = 0
miss = 0

def cache(f):
    def _inner(slf, run, cnt):
        global hits
        global miss
        if cnt < 10:
            return f(slf, run, cnt)
        if (run, cnt) in c:
            hits += 1
            return c[(run, cnt)]
        else:
            miss += 1
            c[(run, cnt)] = f(slf, run, cnt)
            return c[(run, cnt)]

    return _inner

class Poly:
    def __init__(self, rules):
        self.rules = {}
        for rule in rules:
            pair, ins = rule.split(" -> ")
            self.rules[pair] = ins
            self.cache = {}

    def step(self, pair):
        def _build():
                yield pair[0]
                yield self.rules[pair]
                yield pair[1]
        return "".join(_build())

    @cache
    def step_run(self, run, cnt):
        if cnt == 0:
            return run
        res = []
        for pair in pairwise(run):
            res.append(self.step_run(self.step(pair), cnt - 1))
        #print(res)

        return res[0] + "".join(c[1:] for c in res[1:])

    @lru_cache(maxsize=100000)
    def step2(self, run):
        l = len(run)
        if l == 1:
            return run
        elif l == 2:
            return f"{run[0]}{self.rules[run]}{run[1]}"
        else:
            fst, snd = self.step2(run[:l//2]), self.step2(run[l//2:])
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


if __name__ == "__main__":
    with open("input.test") as f:
        data = f.read().strip()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    start = lines[0]
    rules = lines[2:]
    poly = Poly(rules)
    for i in range(10):
        start = poly.step2(start)
        #print(start)
        print(poly.step2.cache_info())
    #res = poly.step_run(start, 30)
    #print(hits, miss, len(c))
    #print(res)
    #s = Str(rules, start)
    #for i in range(40):
    #    print(i)
    #    s.step()
    #    #print("".join(s.iter()))

    c = Counter(start)
    print(c.most_common()[0][1] - c.most_common()[-1][1])
