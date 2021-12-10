#!/usr/bin/env python3

chunks = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}

opening = set(chunks.values())
closing = set(chunks.keys())

chunks_p = {v: k for k, v in chunks.items()}

points_corrupt = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

points_complete = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def parse(l):
    stack = []
    for c in l:
        if c in opening:
            stack.append(c)
        if c in closing:
            if not stack:
                return c
            op = stack.pop()
            if chunks[c] != op:
                return c
    return stack


def eval_corrupt(res):
    if isinstance(res, list):
        return 0
    return points_corrupt.get(res, 0)


def eval_incomplete(res):
    if not isinstance(res, list):
        return None
    closing = [chunks_p[op] for op in reversed(res)]
    score = 0
    for c in closing:
        score = score * 5
        score += points_complete[c]
    return score


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()
    lines = [line.strip() for line in data.split("\n")]
    print(sum(eval_corrupt(parse(l)) for l in lines))
    scores = [eval_incomplete(parse(l)) for l in lines]
    scores = [s for s in scores if s is not None]
    scores.sort()
    print(scores[(len(scores) // 2)])
