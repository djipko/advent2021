#!/usr/bin/env python3

import re
import itertools
from collections import deque
import sys
import pprint

import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.spatial import distance
from numpy.lib.stride_tricks import sliding_window_view

axis_map = dict(zip(range(3), "xyz"))


def flip_axis(v, *axis):
    f = np.array([1, 1, 1])
    for a in axis:
        f[axis_map[a]] = -1
    return v * f


class Scanner:
    def __init__(self, _id):
        self.id = _id
        self.beacons = []
        self._or = None
        self.others = [np.zeros(3)]

    def np(self):
        self.beacons = np.array(self.beacons)

    def orientations(self):
        if self._or is None:
            self._or = list(self._orientations())
        return self._or

    def _orientations(self):
        rotations = [
            ("z", 0, "x"),
            ("z", 90, "y"),
            ("z", 180, "x"),
            ("z", 270, "y"),
            ("y", 90, "z"),
            ("y", -90, "z"),
        ]
        for axis, deg, facing in rotations:
            r = R.from_euler(axis, deg, degrees=True)
            new_beacons = np.zeros((len(self.beacons), 3))
            for i, v in enumerate(self.beacons):
                new_beacons[i] = np.rint(r.apply(v))
            yield new_beacons
            for spin in (90, 180, 270):
                r = R.from_euler(facing, spin, degrees=True)
                spun = np.zeros((len(self.beacons), 3))
                for i, v in enumerate(new_beacons):
                    spun[i] = np.rint(r.apply(v))
                yield spun

    def add_beacons(self, my, found, other):
        translation = my[0] - found[0]
        new = other + translation
        self.others.append(translation)
        conc = np.concatenate((self.beacons, new))
        unique = set(map(tuple, conc))
        self.beacons = np.array(list(unique))

    def calc_max_dist(self):
        return max(
            distance.cityblock(v1, v2)
            for v1, v2 in itertools.combinations(self.others, 2)
        )


def get_mags(bs):
    return np.sqrt(np.sum(np.apply_along_axis(lambda r: r * r, axis=0, arr=bs), axis=1))


def distances_from(b, bs):
    trans_by_b = bs - b
    return get_mags(trans_by_b)


def align(bs1, bs2, matches=12):
    for b1 in bs1:
        for b2 in bs2:
            trans_by_b1 = bs1 - b1
            trans_by_b2 = bs2 - b2

            matching = set(map(tuple, trans_by_b1)) & set(map(tuple, trans_by_b2))
            if len(matching) < matches:
                continue
            inds1 = np.zeros(len(matching))
            inds2 = np.zeros(len(matching))
            for i, match in enumerate(matching):
                ind = np.where(np.all(np.array(list(match)) == trans_by_b1, axis=1))
                inds1[i] = ind[0][0]
                ind = np.where(np.all(np.array(list(match)) == trans_by_b2, axis=1))
                inds2[i] = ind[0][0]
            return bs1[inds1.astype(int)], bs2[inds2.astype(int)]


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    scanner = None
    scanners = []
    scanner_re = re.compile(r"--- scanner (\d+) ---")
    for line in lines:
        if not line:
            scanner.np()
            scanners.append(scanner)
            scanner = None
            beacons = []
            continue
        if match := scanner_re.match(line):
            scanner = Scanner(int(match.group(1)))
        else:
            scanner.beacons.append(list(map(int, line.split(","))))
    base = None
    found_ids = ()
    for s1, s2 in itertools.combinations(scanners, 2):
        for or2 in s2.orientations():
            res = align(s1.beacons, or2)
            if res is not None:
                # found first match
                my, found = res
                base = s1
                found_ids = (s1.id, s2.id)
                base.add_beacons(my, found, or2)
                break
        if base:
            break
    q = deque(s for s in scanners if s.id not in found_ids)
    while q:
        s = q.popleft()
        found = False
        for ori in s.orientations():
            res = align(base.beacons, ori)
            if res is not None:
                my, found = res
                base.add_beacons(my, found, ori)
                found = True
                break
        if not found:
            q.append(s)

    print(len(base.beacons))
    print(base.calc_max_dist())
