#!/usr/bin/env python3


def expand_by_n(image, n):
    new_w = len(image[0]) + 2 * n
    for _ in range(n):
        yield [0 for _ in range(new_w)]

    for l in image:
        yield [0 for _ in range(n)] + l + [0 for _ in range(n)]

    for _ in range(n):
        yield [0 for _ in range(new_w)]


def process(algo, image, x, y):
    px = "".join(
        (str(image[yy][xx]) for yy in range(y - 1, y + 2) for xx in range(x - 1, x + 2))
    )
    px = "".join(px)
    idx = int(px, 2)
    return 1 if algo[idx] else 0


def display(image):
    for l in image:
        print("".join(["#" if p == 1 else "." for p in l]))


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()
    lines = [line.strip() for line in data.split("\n")]

    algo = [c == "#" for c in lines[0]]
    orig_image = [[1 if c == "#" else 0 for c in line] for line in lines[2:]]

    for steps in (2, 50):
        n = 3 * steps
        image = list(expand_by_n(orig_image, n))
        for step in range(steps):
            h, w = len(image), len(image[0])
            processed = []
            for y in range(1, h - 1):
                processed.append([])
                for x in range(1, w - 1):
                    processed[y - 1].append(process(algo, image, x, y))
            image = processed
        print(sum((sum(l) for l in image)))
