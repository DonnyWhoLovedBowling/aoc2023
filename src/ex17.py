import heapq
import logging
from logging import info, debug, warning, error
from line_profiler_pycharm import profile

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex17.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]


@profile
def visualize(visited):
    for i, line in enumerate(lines):
        new_line = ''
        for j, c in enumerate(line):
            if (j, i) in visited.keys():
                new_line += str(visited[(j, i)]).ljust(3)
            else:
                new_line += str('   ')
        info(new_line)


@profile
def solve(graph, source, end, pt2):
    pt1 = not pt2
    priority_queue = []
    heapq.heappush(priority_queue, (0, (source, (0, 0), 0)))
    visited = set()
    max_dist = 0
    while priority_queue:
        (current_distance, current_tuple) = heapq.heappop(priority_queue)
        current = current_tuple[0]
        last_dir = current_tuple[1]
        straights = current_tuple[2]
        if current_tuple in visited:
            continue
        visited.add(current_tuple)
        if (current[0] + current[1]) > max_dist:
            max_dist = (current[0] + current[1])
            debug((current_distance, current, len(visited), len(priority_queue)))

        for dx in [1, 0, -1]:
            if dx == 0:
                dy_list = [1, -1]
            else:
                dy_list = [0]
            for dy in dy_list:
                new_straights = straights
                if (dx, dy) == last_dir:
                    new_straights += 1
                else:
                    new_straights = 0
                if pt1 and new_straights == 3:
                    continue
                if pt2:
                    if new_straights == 0 and straights < 3 and current != (0, 0):
                        continue
                    if new_straights == 10:
                        continue

                if ((dx == (-1 * last_dir[0])) and dx != 0) or ((dy == (-1 * last_dir[1])) and dy != 0):
                    continue

                neighbour = (current[0] + dx, current[1] + dy)
                if neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] > end[0] or neighbour[1] > end[1]:
                    continue

                new_distance = current_distance + graph[neighbour]
                if end == neighbour:
                    if pt1 or new_straights >= 3:
                        debug((new_distance, current_distance, current_tuple))
                        return new_distance
                heapq.heappush(priority_queue, (new_distance, (neighbour, (dx, dy), new_straights)))

    return -1


# @profile
def solution():
    graph = {}
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            graph[(j, i)] = int(c)
    start = (0, 0)
    end = (len(lines[0]) - 1, len(lines) - 1)
    info(f"ans pt1 = {solve(graph, start, end, False)}")
    info(f"ans pt2 = {solve(graph, start, end, True)}")


if __name__ == '__main__':
    solution()
