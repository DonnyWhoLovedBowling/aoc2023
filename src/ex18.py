import heapq
import logging
from logging import info, debug, warning, error
from line_profiler_pycharm import profile

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex18.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]


@profile
def visualize(visited, min_x, max_x, min_y, max_y):
    for i in range(min_y, max_y+1):
        new_line = ''
        for j in range(min_x, max_x+1):
            if (j, i) in visited:
                new_line += '#'
            else:
                new_line += '.'
        info(new_line)

@profile
def calc_interior(visited, min_x, max_x, min_y, max_y):
    lagoon = set()
    for i in range(min_y, max_y+1):
        in_border = False
        from_above = False
        crossings = 0
        for j in range(min_x, max_x+1):
            if (j, i) in visited:
                if in_border:
                    in_polygon = True
                else:
                    in_polygon = True
                    if (j, i+1) in visited and (j, i-1) in visited:
                        crossings += 1
                    elif (j, i+1) in visited:
                        in_border = True
                        from_above = False
                    elif (j, i-1) in visited:
                        in_border = True
                        from_above = True
                    else:
                        raise ValueError(f"horizontal single line? {(j, i)}")
            else:
                if in_border:
                    if ((j-1, i-1) in visited) != from_above:
                        crossings += 1
                in_polygon = ((crossings % 2) == 1)
                in_border = False
                from_above = False

            if in_polygon:
                lagoon.add((j, i))
    return lagoon

def add_vec(a, b):
    return tuple(map(sum, zip(a, b)))


def solution():
    min_x, min_y, max_x, max_y = (0, 0, 0, 0)
    cursor = (0, 0)
    polygon = {cursor}

    for line in lines:
        inputs = line.split(" ")
        if inputs[0] == 'R':
            direction = (1, 0)
        elif inputs[0] == 'U':
            direction = (0, -1)
        elif inputs[0] == 'L':
            direction = (-1, 0)
        elif inputs[0] == 'D':
            direction = (0, 1)
        else:
            raise ValueError("direction not clear!")

        for i in range(0, int(inputs[1])):
            cursor = add_vec(cursor, direction)
            polygon.add(cursor)
            if cursor[0] < min_x:
                min_x = cursor[0]
            if cursor[0] > max_x:
                max_x = cursor[0]
            if cursor[1] < min_y:
                min_y = cursor[1]
            if cursor[1] > max_y:
                max_y = cursor[1]
    lagoon = calc_interior(polygon, min_x, max_x, min_y, max_y)
    visualize(lagoon, min_x, max_x, min_y, max_y)
    info(f"ans pt1 = {len(lagoon)}")


if __name__ == '__main__':
    solution()
