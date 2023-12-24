import logging
from logging import info, debug
from collections import deque

junction_map = dict()
junctions = set()

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex23.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]


def shortest_path(start, end):
    queue = deque()
    queue.append((0, start))
    visited = set()
    while queue:
        length, current_position = queue.popleft()
        if current_position in visited:
            continue
        visited.add(current_position)
        if current_position == end:
            return length

        if current_position in junctions and current_position != start:
            continue

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = current_position[0] + dx, current_position[1] + dy

            if (0 <= new_y < len(lines) and
                    0 <= new_x < len(lines[0]) and
                    lines[new_y][new_x] != '#' and
                    (new_x, new_y) not in visited):
                queue.append((length + 1, (new_x, new_y)))
    return -1


seen = set()


def find_longest_path(source, end):
    global junction_map, seen
    if source == end:
        return 0
    length = - 1000000
    seen.add(source)
    for n, segment in junction_map[source].items():
        if n in seen:
            continue
        new_l = find_longest_path(n, end)+segment
        if new_l > length:
            length = new_l
        elif length == -100:
            debug((source, end,  n, length, new_l))
    seen.remove(source)
    return length


def pt1():
    global junctions, junction_map
    start = (1, 0)
    end = (len(lines) - 2, len(lines) - 1)
    junctions.add(start)
    junctions.add(end)

    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '#':
                continue
            neighbours = 0
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                i2 = i + dy
                j2 = j + dx
                if 0 <= i2 < len(lines) and 0 <= j2 < len(lines[0]) and lines[i2][j2] != '#':
                    neighbours += 1
            if neighbours >= 3:
                junctions.add((j, i))

    for j1 in junctions:
        for j2 in junctions:
            if j1 == j2:
                continue
            length = shortest_path(j1, j2)
            if length > 0:
                if j1 in junction_map:
                    junction_map[j1][j2] = length
                else:
                    junction_map[j1] = {j2: length}
    print(f"ans pt2 = {find_longest_path(start, end)}")


if __name__ == '__main__':
    pt1()
