#!/usr/bin/env python3

from collections import defaultdict, Counter
import string

paths = []
graph = defaultdict(list)


def build_paths(start, end, visited, cur_path, max_visits=1):
    if start[0] in string.ascii_lowercase:
        visited[start] += 1
    cur_path.append(start)
    if start == end:
        paths.append(cur_path[:])
    else:
        for to_visit in graph[start]:
            if visited[to_visit] >= max_visits:
                continue
            if to_visit == "start":
                continue
            if (
                visited[to_visit] >= 1
                and to_visit[0] in string.ascii_lowercase
                and visited.most_common()[0][1] >= max_visits
            ):
                continue
            build_paths(to_visit, end, visited, cur_path, max_visits)
    cur_path.pop()
    if visited[start] > 0:
        visited[start] -= 1


if __name__ == "__main__":
    with open("input") as f:
        data = f.read().strip()
    lines = [line.strip() for line in data.split("\n")]
    edges = [line.split("-") for line in lines]
    for s, e in edges:
        graph[s].append(e)
        graph[e].append(s)
    build_paths("start", "end", Counter(), [], 1)
    print(len(paths))
    paths = []
    build_paths("start", "end", Counter(), [], 2)
    print(len(paths))
