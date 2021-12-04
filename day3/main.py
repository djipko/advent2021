#!/usr/bin/env python3

from collections import Counter


def count(data):
    cs = [Counter() for _ in range(len(data[0]))]
    for b in data:
        for c, dig in zip(cs, b):
            c[dig] += 1
    return cs


def get_gama(counters):
    binary = "".join(c.most_common()[0][0] for c in counters)
    return int(binary, 2)


def get_epsilon(counters):
    binary = "".join(c.most_common()[-1][0] for c in counters)
    return int(binary, 2)


def get_most_common(c):
    return "0" if c["0"] > c["1"] else "1"


def get_least_common(c):
    return "1" if c["1"] < c["0"] else "0"


def get_oxygen(data, cntrs):
    cand = data
    it = len(cand[0])
    for pos in range(it):
        new_cand = [c for c in cand if c[pos] == get_most_common(cntrs[pos])]
        if len(new_cand) == 1:
            return int(new_cand[0], 2)
        cand = new_cand
        cntrs = count(cand)


def get_co2_scrub(data, cntrs):
    cand = data
    it = len(cand[0])
    for pos in range(it):
        new_cand = [c for c in cand if c[pos] == get_least_common(cntrs[pos])]
        if len(new_cand) == 1:
            return int(new_cand[0], 2)
        cand = new_cand
        cntrs = count(cand)


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    counters = count(lines)
    print(get_gama(counters) * get_epsilon(counters))
    print(get_oxygen(lines, counters) * get_co2_scrub(lines, counters))
