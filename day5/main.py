#!/usr/bin/env python3

from dataclasses import dataclass
import itertools


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class Line:
    def __init__(self, start, end):
        self.start = Point(int(start[0]), int(start[1]))
        self.end = Point(int(end[0]), int(end[1]))
        self.points = self._points()

    def is_vert(self):
        return self.start.x == self.end.x

    def is_hor(self):
        return self.start.y == self.end.y

    def _points(self):
        if self.is_vert():
            y_start = min(self.start.y, self.end.y)
            y_end = max(self.start.y, self.end.y)
            x = self.start.x
            return set(Point(x, y) for y in range(y_start, y_end + 1))

        if self.is_hor():
            x_start = min(self.start.x, self.end.x)
            x_end = max(self.start.x, self.end.x)
            y = self.start.y
            return set(Point(x, y) for x in range(x_start, x_end + 1))

        start, end = (
            (self.start, self.end)
            if self.start.x <= self.end.x
            else (self.end, self.start)
        )
        xs = range(start.x, end.x + 1)
        ys = (
            range(start.y, end.y + 1)
            if start.y < end.y
            else reversed(range(end.y, start.y + 1))
        )
        return set(Point(x, y) for x, y in zip(xs, ys))


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()
    input_lines = [line.strip() for line in data.split("\n")]
    lines = []
    for l in input_lines:
        start, end = l.split(" -> ")
        line = Line(start.split(","), end.split(","))
        lines.append(line)
    only_hv_lines = [l for l in lines if l.is_vert() or l.is_hor()]
    intersections = set()
    for l1, l2 in itertools.combinations(only_hv_lines, 2):
        iss = l1.points & l2.points
        intersections |= iss
    print(len(intersections))
    intersections.clear()
    for l1, l2 in itertools.combinations(lines, 2):
        iss = l1.points & l2.points
        intersections |= iss
    print(len(intersections))
