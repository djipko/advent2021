#!/usr/bin/env python3

from collections import deque

def increases(ms):
    prev = None
    inc = 0
    for m in ms:
        if prev is not None and m > prev:
            inc += 1
        prev = m
    return inc

def increases_w(ms):
    w = deque(ms[:3])
    ms = ms[3:]
    inc = 0
    cur = sum(w)
    for m in ms:
        lft = w.popleft()
        nxt = cur - lft + m
        if nxt > cur:
            inc += 1
        cur = nxt
        w.append(m)
    return inc


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [int(line.strip()) for line in data.split("\n") if line]
    print(increases(lines))
    print(increases_w(lines))
