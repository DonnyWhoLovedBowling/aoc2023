import logging
from logging import info, debug, warning
from copy import deepcopy as dc
from line_profiler_pycharm import profile

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex13.txt")
lines = in_file.readlines()
lines.append('\n')
valleys = []


@profile
def mirror_point(point, mirror, direction, max_val):
    if direction == 'hor':
        ix = 1
    else:
        ix = 0
    new_coor = int(mirror + mirror-point[ix])
    if 0 > new_coor or new_coor > max_val:
        return point

    if direction == 'hor':
        return point[0], new_coor
    else:
        return new_coor, point[1]


@profile
def find_mirror(rocks, max_x, max_y, exclude_mirror=-1, exclude_direction=''):
    # n_points = max_x/y + 1
    # row/columns below mirror: i+1
    # row/columns above mirror: max_x-i
    for direction in ['hor', 'ver']:
        if direction == 'hor':
            max_p = max_y
            ix = 1
        else:
            max_p = max_x
            ix = 0
        for i in range(0, max_p):
            mirror = i+0.5
            if mirror == exclude_mirror and direction == exclude_direction:
                continue
            n_below = i+1
            n_above = max_p-i
            if n_below > n_above:
                points_to_be_mapped = set(filter(lambda x: x[ix] < mirror, rocks))
            else:
                points_to_be_mapped = set(filter(lambda x: x[ix] > mirror, rocks))
            points_to_be_matched = rocks.difference(points_to_be_mapped)
            mapped_points = set()
            fits = True
            for p in points_to_be_mapped:
                new_p = mirror_point(p, mirror, direction, max_p)
                mapped_points.add(new_p)
                if new_p not in rocks:
                    fits = False
                    break
            if fits and len(points_to_be_matched.difference(mapped_points)) == 0:
                if direction == 'ver':
                    return i+1, mirror, direction
                else:
                    return (i+1) * 100, mirror, direction

    return None, None, None


@profile
def pt1():
    global valleys
    rocks = set()
    i = 0
    max_x = 0
    max_y = 0
    score = 0
    for line in lines:
        if line == '\n':
            i = 0
            this_score, mirror, direction = find_mirror(rocks, max_x, max_y)
            debug((this_score, mirror, direction))
            score += this_score
            valleys.append((rocks, max_x, max_y, mirror, direction))
            rocks = set()
            max_x = 0
            max_y = 0
            continue
        for j, c in enumerate(line):
            if c == '#':
                rocks.add((j, i))
                if j > max_x:
                    max_x = j
                if i > max_y:
                    max_y = i
        i += 1
    info(f"ans pt1 = {score}")


@profile
def pt2():
    score = 0
    for valley in valleys:
        found = False
        rocks: set = valley[0]
        for i in range(0, valley[1]+1):
            if found:
                break
            for j in range(0, valley[2]+1):
                rocks_new = dc(rocks)
                if (i, j) in rocks:
                    rocks_new.remove((i, j))
                else:
                    rocks_new.add((i, j))
                this_score, mirror, direction = find_mirror(rocks_new, valley[1], valley[2], valley[3], valley[4])
                if this_score is not None:
                    debug(f"found! {this_score}, {(i,j)} changed, mirror: {mirror}")
                    score += this_score
                    found = True
                    break
        if not found:
            warning(f"no alternative found! {valley}")

    info(f"ans pt2 = {score}")


if __name__ == '__main__':
    pt1()
    pt2()
