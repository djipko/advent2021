#!/usr/bin/env python3

digit_len_map = {
    2: [1],
    3: [7],
    4: [4],
    5: [5, 2, 3],
    6: [0, 9, 6],
    7: [8],
}


class SevSeg:
    ORIG_MAP = {
        "0": "abcefg",
        "1": "cf",
        "2": "acdeg",
        "3": "acdfg",
        "4": "bcdf",
        "5": "abdfg",
        "6": "abdefg",
        "7": "acf",
        "8": "abcdefg",
        "9": "abcdfg",
    }

    def __init__(self, digs):
        self.trans = {v: k for k, v in self.ORIG_MAP.items()}
        self._build_map(digs)

    def _build_map(self, digs):
        digs = ["".join(sorted(dig)) for dig in digs]
        one = [dig for dig in digs if len(dig) == 2][0]
        four = [dig for dig in digs if len(dig) == 4][0]
        seven = [dig for dig in digs if len(dig) == 3][0]
        eight = [dig for dig in digs if len(dig) == 7][0]

        _all = set("abcdefg")

        cf = set(one)
        bd = set(four) - set(one)
        a = set(seven) - set(one)
        eg = set(eight) - (cf | bd | a)
        adg = set.intersection(*(set(dig) for dig in digs if len(dig) == 5))
        e = eg - adg
        g = eg - e
        d = adg - (a | g)
        b = bd - d
        _069 = [set(dig) for dig in digs if len(dig) == 6]
        cde = set.union(*(_all - d for d in _069))
        c = cde - (d | e)
        f = cf - c
        self._map = {
            a.pop(): "a",
            b.pop(): "b",
            c.pop(): "c",
            d.pop(): "d",
            e.pop(): "e",
            f.pop(): "f",
            g.pop(): "g",
        }

    def decode(self, digs):
        decoded_digs = ["".join(sorted(self._map[c] for c in dig)) for dig in digs]
        return int("".join(self.trans[d] for d in decoded_digs))


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()
    lines = [line.strip() for line in data.split("\n")]

    total = 0
    for l in lines:
        fst, snd = l.split(" | ")
        digs = snd.split()
        total += sum(1 for dig in digs if len(digit_len_map.get(len(dig))) == 1)
    print(total)

    s = 0
    for l in lines:
        coded, digs = l.split(" | ")
        ss = SevSeg(coded.split())
        dec = ss.decode(digs.split())
        s += dec
    print(s)
