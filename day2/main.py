#!/usr/bin/env python3


class Sub:
    def __init__(self):
        self.h = 0
        self.d = 0
        self.aim = 0

    def command(self, c: str):
        match c.split():
            case ["forward", count]:
                self.h += int(count)
            case ["down", count]:
                self.d += int(count)
            case ["up", count]:
                self.d -= int(count)
                assert self.d >= 0
            case _:
                print(f"Wrong command {c}")

    def command2(self, c: str):
        match c.split():
            case ["down", count]:
                self.aim += int(count)
            case ["up", count]:
                self.aim -= int(count)
            case ["forward", count]:
                self.h += int(count)
                self.d += self.aim * int(count)
            case _:
                print(f"Wrong command {c}")

    def pos(self):
        return self.h * self.d


if __name__ == "__main__":
    with open("input") as f:
        data = f.read()
    lines = [line.strip() for line in data.split("\n")]
    # do stuff with data
    sub = Sub()
    for c in lines:
        sub.command(c)
    print(sub.pos())
    sub = Sub()
    for c in lines:
        sub.command2(c)
    print(sub.pos())
