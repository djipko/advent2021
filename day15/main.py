#!/usr/bin/env python3

from functools import lru_cache
import sys
import math
import heapq


def adj(cave, x, y):
    coord = [(x, y + 1), (x + 1, y), (x, y - 1), (x - 1, y)]
    for c in coord:
        if 0 <= c[0] < len(cave[0]) and 0 <= c[1] < len(cave) and c != (x, y):
            yield c


def dijkstra(cave, start):
    w, h = len(cave[0]), len(cave)
    unvisited = set((x, y) for x in range(w) for y in range(h))
    shortest = {c: math.inf for c in unvisited}
    frontier = []
    # previous = {}
    shortest[start] = 0
    heapq.heappush(frontier, (0, start))
    while unvisited:
        _dist, current_min = heapq.heappop(frontier)

        for nx, ny in adj(cave, *current_min):
            if (nx, ny) not in unvisited:
                continue
            tentative = shortest[current_min] + cave[ny][nx]
            if tentative < shortest[(nx, ny)]:
                shortest[(nx, ny)] = tentative
                heapq.heappush(frontier, (tentative, (nx, ny)))
                # previous[(nx, ny)] = current_min
        unvisited.discard(current_min)
    return shortest


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()
    lines = [line.strip() for line in data.split("\n")]
    cave = [list(map(int, l)) for l in lines]

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
            # print(x, y, orig_x, orig_y, off_x, off_y)
            new_val = cave[orig_y][orig_x] + (off_x + off_y)
            new_cave[y][x] = (new_val - 1) % 9 + 1
    # for y in range(new_h):
    #    print("".join(map(str, new_cave[y])))

    shortest = dijkstra(cave, (0, 0))
    print(shortest[(w - 2, h - 2)])
    shortest = dijkstra(new_cave, (0, 0))
    print(shortest[(new_w - 1, new_h - 1)])
