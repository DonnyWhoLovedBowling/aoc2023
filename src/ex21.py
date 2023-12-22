import heapq
import logging
from line_profiler_pycharm import profile
from collections import deque
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex21.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]



@profile
def solve(graph, source, max_steps, pt2=False):
    priority_queue = deque()
    priority_queue.append((0, source))
    visited = set()
    final_points = set()
    while priority_queue:
        (current_steps, current_position) = priority_queue.popleft()
        if (current_steps, current_position) in visited:
            continue
        visited.add((current_steps, current_position))
        if current_steps == max_steps:
            final_points.add(current_position)
            continue
        for dx in [1, 0, -1]:
            if dx == 0:
                dy_list = [1, -1]
            else:
                dy_list = [0]
            for dy in dy_list:
                neighbour = (current_position[0] + dx, current_position[1] + dy)
                if (neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= len(graph[0])
                        or neighbour[1] >= len(graph)-1):
                    continue
                if graph[neighbour[1]][neighbour[0]] == '#':
                    continue

                priority_queue.append((current_steps + 1, neighbour))

    return len(final_points)


def pt1():
    start = ()
    n_points = 0
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == 'S':
                start = (j, i)
            if c == '.':
                n_points += 1
    print(lines)
    print(n_points)
    # info(solve(lines, start, 64))
    pt2_steps = 26501365
    start = (0, 65)
    for s in range(1, 1000):
        print(s, solve(lines, start, s, True))


if __name__ == '__main__':
    pt1()

