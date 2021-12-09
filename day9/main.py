#!/usr/bin/env python3


def adj(heatmap, x, y):
    coord = [(x - 1, y), (x + 1, y), (x, y + 1), (x, y - 1)]
    for c in coord:
        if 0 <= c[0] < len(heatmap[0]) and 0 <= c[1] < len(heatmap) and c != (x, y):
            yield c


def find_basin(heatmap, x, y, visited) -> int:
    if heatmap[y][x] >= 9:
        return 0
    visited.add((x, y))
    val = heatmap[y][x]
    s = 1
    for cx, cy in adj(heatmap, x, y):
        if (cx, cy) in visited:
            continue
        if heatmap[cy][cx] > val:
            s += find_basin(heatmap, cx, cy, visited)
    return s


def is_lowpoint(heatmap, x, y):
    return all(point < heatmap[ay][ax] for ax, ay in adj(heatmap, x, y))


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()
    lines = [line.strip() for line in data.split("\n")]
    heatmap = [list(map(int, l)) for l in lines]

    s = 0
    for y, row in enumerate(heatmap):
        for x, point in enumerate(row):
            if is_lowpoint(heatmap, x, y):
                s += point + 1
    print(s)
    basins = []
    for y, row in enumerate(heatmap):
        for x, point in enumerate(row):
            if is_lowpoint(heatmap, x, y):
                b = find_basin(heatmap, x, y, set())
                basins.append(b)

    basins.sort(reverse=True)
    print(basins[0] * basins[1] * basins[2])
