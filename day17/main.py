#!/usr/bin/env python3

from dataclasses import dataclass
from enum import Enum, auto
from itertools import count


class MoveResult(Enum):
    UNDER = auto()
    ON = auto()
    OVER = auto()


class ShotResult(Enum):
    FLIGH = auto()
    HIT = auto()
    MISS = auto()


class Area:
    def __init__(self, xrange, yrange):
        self.xrange = xrange
        self.yrange = yrange

    def gague_shot(self, x, y):
        return self.gague_x(x), self.gague_y(y)

    def gague_x(self, x):
        low, high = self.xrange
        if x < low:
            return MoveResult.UNDER
        if low <= x <= high:
            return MoveResult.ON
        if high < x:
            return MoveResult.OVER

    def gague_y(self, y):
        high, low = self.yrange
        if y > low:
            return MoveResult.UNDER
        if low >= y >= high:
            return MoveResult.ON
        if high > y:
            return MoveResult.OVER


class Shot:
    def __init__(self, area, xv, yv):
        self.area = area
        self.xv = xv
        self.yv = yv
        self.x = 0
        self.y = 0
        self.max_h = 0

    def step(self):
        new_x = self.x + self.xv
        new_y = self.y + self.yv
        self.x, self.y = new_x, new_y
        self.max_h = max(new_y, self.max_h)
        # print(self.x, self.y)

        if self.xv < 0:
            sefl.xv = max(self.xv + 1, 0)
        elif self.xv > 0:
            self.xv = max(self.xv - 1, 0)
        self.yv = self.yv - 1

        gx, gy = self.area.gague_shot(new_x, new_y)
        res = ShotResult.FLIGH
        if gx == MoveResult.ON and gy == MoveResult.ON:
            res = ShotResult.HIT
        if gx == MoveResult.OVER or gy == MoveResult.OVER:
            res = ShotResult.MISS
        # We won't make progress towards x ever may as well bail
        if gx == MoveResult.UNDER and self.xv <= 0:
            res = ShotResult.MISS
        return res

    def shoot(self):
        for s in count():
            res = self.step()
            if res in (ShotResult.HIT, ShotResult.MISS):
                return res
        return res


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]

    target_area = lines[0]
    coords = target_area[13:]
    x, y = coords.split(", ")
    _, xrange = x.split("=")
    x_start, x_end = map(int, xrange.split(".."))
    _, yrange = y.split("=")
    y_start, y_end = map(int, yrange.split(".."))

    target = Area((x_start, x_end), (y_start, y_end))
    tries = 2 * max(
        target.xrange[1] - target.xrange[0], abs(target.yrange[1] - target.yrange[0])
    )
    hs = []
    for x in range(1, x_end + 2):
        miss_cnt = 0
        for y in count(y_end):
            shot = Shot(target, x, y)
            res = shot.shoot()
            if res == ShotResult.MISS:
                miss_cnt += 1
                if miss_cnt > tries:
                    break
            elif res == ShotResult.HIT:
                hs.append((shot.max_h, (x, y)))
                miss_cnt = 0

    print(max(h[0] for h in hs))
    print(len(hs))
