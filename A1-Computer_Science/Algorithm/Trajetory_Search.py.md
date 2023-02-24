```python
import time
from collections import deque
from copy import deepcopy

import termcolor


class Map(object):
    def __init__(self, map_data):
        self.map_data = map_data
        self.x_size = len(map_data)
        self.y_size = len(map_data[0])

    def __repr__(self):
        result = list()
        for line in self.map_data:
            for item in line:
                elem = f"{item}".rjust(2)
                if isinstance(item, int) and item != 0:
                    elem = termcolor.colored(elem, 'red')
                if isinstance(item, str):
                    elem = termcolor.colored(elem, 'green')
                result.append(elem)
            result.append('\n')
        return ''.join(result)

    def __getitem__(self, pos):
        return self.map_data[pos[0]][pos[1]]

    def __setitem__(self, pos, value):
        self.map_data[pos[0]][pos[1]] = value

    def neighbor(self, pos):
        x, y = pos
        for dx in [-1, 0, 1]:
            xi = x + dx
            if 0 <= xi < self.x_size:
                for dy in [-1, 0, 1]:
                    yi = y + dy
                    if dx == dy == 0:
                        continue
                    if 0 <= yi < self.y_size:
                        if self[xi, yi] == 0:
                            yield (xi, yi), {0: 0, 1: 1, 2: 1.41}[abs(dx) + abs(dy)]


def distance_manhatton(p1, p2):
    return sum(abs(i - j) for i, j in zip(p1, p2))


def distance_eular(p1, p2):
    return sum((i - j)**2 for i, j in zip(p1, p2))


def breadth_first_search(problem: Map, departure, destination):
    queue = deque()
    queue.appendleft((departure, 0, ()))
    visited = set()
    loops = 0
    while queue:
        top, distance, traj = queue.pop()
        loops += 1
        if top == destination:
            return distance, traj, loops, visited
        visited.add(top)
        for n, d in problem.neighbor(top):
            if n not in visited:
                queue.appendleft((n, distance + d, traj + (top,)))
    return -1, (), loops, visited


def best_first_search(problem: Map, departure, destination, distance_metric=distance_manhatton):
    queue = deque()
    queue.appendleft((departure, 0, (), distance_metric(departure, destination)))
    visited = set()
    loops = 0
    while queue:
        best = min(queue, key=lambda x: x[-1])
        queue.remove(best)
        top, distance, traj, score = best
        loops += 1
        if top == destination:
            return distance, traj, loops, visited
        visited.add(top)
        for next_pos, ds in problem.neighbor(top):
            if next_pos not in visited:
                queue.appendleft((next_pos, distance + ds, traj + (top,), distance_metric(next_pos, destination)))
    return -1, (), loops, visited


def a_star_search(problem: Map, departure, destination, distance_metric=distance_manhatton):
    queue = deque()
    queue.appendleft((departure, 0, (), distance_metric(departure, destination)))
    visited = set()
    loops = 0
    while queue:
        best = min(queue, key=lambda x: x[-1])
        queue.remove(best)
        top, distance, traj, score = best
        loops += 1
        if top == destination:
            return distance, traj, loops, visited
        visited.add(top)
        for next_pos, ds in problem.neighbor(top):
            if next_pos not in visited:
                queue.appendleft((next_pos, distance + ds, traj + (top,), distance + ds + distance_metric(next_pos, destination)))
    return -1, (), loops, visited


if __name__ == '__main__':
    destination = (13, 10)
    departure = (8, 5)
    map_data = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    for search_method in (
        breadth_first_search,
        best_first_search,
        a_star_search
    ):
        problem = Map(deepcopy(map_data))
        start = time.time()
        distance, traj, loops, visited = search_method(problem, departure, destination)
        end = time.time()
        for i, p in enumerate(traj):
            problem[p] = str(i)
        problem[departure] = 'DP'
        problem[destination] = 'DS'
        print(problem)
        print(search_method.__name__, f"{distance=}, {len(traj)=}, {loops=}, {end-start=:0.2f}")

```
