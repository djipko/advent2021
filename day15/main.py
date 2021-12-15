#!/usr/bin/env python3

from functools import lru_cache
import sys

def adj(cave, x, y):
    #coord = [(x, y + 1), (x + 1, y), (x - 1, y), (x, y - 1)]
    coord = [(x + 1, y), (x, y + 1)]
    #coord = [(x + 1, y), (x, y + 1)]
    #coord = [(x, y + 1), (x + 1, y)]
    for c in coord:
        if 0 <= c[0] < len(cave[0]) and 0 <= c[1] < len(cave) and c != (x, y):
            yield c

risks = []
visited = set()
cave = None

hit = 0
miss = 0
cache = {}

def memo(f):
    def _inner(x, y):
        global hit
        global miss
        global cache
        if (x, y) in cache:
            hit += 1
            return cache[(x, y)]
        else:
            miss += 1
            res = f(x, y)
            if res is not None:
                cache[(x, y)] = res
            return res
    return _inner

@memo
#@lru_cache(maxsize=100_000)
def explore(x, y):
    global cave
    end = (len(cave[0]) - 1, len(cave) - 1)
    if (x, y) == end:
        risk = cave[y][x]
    else:
        risks = []
        for nx, ny in adj(cave, x, y):
            if (nx, ny) not in visited:
                r = explore(nx, ny)
                risks.append((r, (nx, ny)))
        print("returning from", (x,y), risks)
        if not risks:
            risk = None
        else:
            risks = [r for r in risks if r[0] is not None]
            if risks:
                min_risk = min(risks, key=lambda r: r[0])
                risk = cave[y][x] + min_risk[0]
            else:
                risk = None
    return risk
    

if __name__ == "__main__":
    with open("input.test") as f:
        data = f.read().strip()
    lines = [line.strip() for line in data.split("\n")]
    cave = [list(map(int, l)) for l in lines]
    # do stuff with data
            
    #r = explore(0, 0)
    #print(explore.cache_info())
    #print(r - cave[0][0])

    w = len(cave[0]) + 1 
    h = len(cave) + 1

    new_w = (w - 1) * 5
    new_h = (h - 1) * 5

    new_cave = [[None for col in range(new_w)] for row in range(new_h)]
    for x in range(new_w):
        for y in range(new_h):
            orig_x = x % (w - 1)
            orig_y = y % (h - 1)
            off_x = x // (w - 1)
            off_y = y // (h - 1)
            #print(x, y, orig_x, orig_y, off_x, off_y)
            new_val = cave[orig_y][orig_x] + (off_x + off_y)
            new_cave[y][x] = (new_val - 1) % 9 + 1
    #for y in range(new_h):
    #    print("".join(map(str, new_cave[y])))

    #cave = new_cave
    sys.setrecursionlimit(40000)
    r = explore(0, 0)
    print(hit, miss)
    print(cache)
    print(r - cave[0][0])
