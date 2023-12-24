from collections import deque
import logging
from logging import info, debug
from line_profiler_pycharm import profile
from copy import deepcopy as dc

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex23.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]


@profile
def solve(graph, source, end, slippery):
    paths = []
    priority_queue = deque()
    priority_queue.append((0, source, False, set()))
    while priority_queue:
        (current_steps, current_position, was_slope, visited) = priority_queue.pop()
        if current_position == end:
            paths.append(visited)
            debug(f"path found: {len(visited)}")
            continue
        if graph[current_position[1]][current_position[0]] in '<>^v':
            next_slope = not was_slope
        else:
            next_slope = was_slope
        for dx in [1, 0, -1]:
            if dx == 0:
                dy_list = [1, -1]
            else:
                dy_list = [0]
            for dy in dy_list:
                neighbour = (current_position[0] + dx, current_position[1] + dy)
                if (neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= len(graph[0])
                        or neighbour[1] >= len(graph)):
                    continue
                tile_type = graph[neighbour[1]][neighbour[0]]
                if tile_type == '#':
                    continue
                if (slippery and was_slope and
                        next_slope):
                    if (dx == 1 and tile_type != '>') or (dx == -1 and tile_type != '<') or \
                            (dy == 1 and tile_type != 'v') or (dy == -1 and tile_type != '^'):
                        continue

                if neighbour in visited:
                    continue
                new_visited = dc(visited)
                new_visited.add(neighbour)
                priority_queue.append((current_steps + 1, neighbour, next_slope, new_visited))

    return paths


def pt1():
    start = (1, 0)
    end = (len(lines)-2, len(lines)-1)
    # paths = solve(lines, start, end, True)
    paths = solve(lines, start, end, False)


    max_path = 0
    for path in paths:
        debug(f"path pt1 = {len(path)}")
        max_path = max(max_path, len(path))
    debug(f"ans pt1 = {max_path}")


if __name__ == '__main__':
    pt1()
