#!/usr/bin/env python3

from math import inf

if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    hs = [int(h) for h in lines[0].split(",")]

    # hs = [16,1,2,0,4,2,7,1,2,14]
    start, end = min(hs), max(hs)
    fuel_l = inf
    fuel = inf
    for p in range(start, end + 1):
        fl = sum(abs(h - p) for h in hs)
        # Sum up to N = N*(N+1) / 2
        f = sum(((abs(h - p) + 1) * abs(h - p)) // 2 for h in hs)
        if fl <= fuel_l:
            fuel_l = fl
        if f <= fuel:
            fuel = f
    print(fuel_l)
    print(fuel)
