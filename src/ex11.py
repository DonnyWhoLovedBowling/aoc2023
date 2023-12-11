import logging
import os
import math
from logging import info, debug, error
from line_profiler_pycharm import profile
from copy import deepcopy as dc
from functools import cmp_to_key

logging.basicConfig(level=logging.DEBUG)
in_file = open("../data/ex11.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]


def pt1(expansion_factor=1):
    galaxies = set()
    xs = set()
    ys = set()
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == '#':
                xs.add(j)
                ys.add(i)
                galaxies.add((j,i))

    x_max = max(xs)
    y_max = max(ys)
    missing_x = set(range(0, x_max)).difference(xs)
    missing_y = set(range(0, y_max)).difference(ys)
    pairs = set()
    total = 0
    for g1 in galaxies:
        for g2 in galaxies:
            if (g1, g2) in pairs or (g2, g1) in pairs:
                continue
            xmin = min(g1[0], g2[0])
            xmax = max(g1[0], g2[0])
            ymin = min(g1[1], g2[1])
            ymax = max(g1[1], g2[1])

            length = (xmax-xmin) + (ymax-ymin)
            length += len(set(range(xmin, xmax)).intersection(missing_x))*(expansion_factor-1)
            length += len(set(range(ymin, ymax)).intersection(missing_y))*(expansion_factor-1)
            total += length
            pairs.add((g1, g2))

    info(f"ans pt1 = {total}")

if __name__ == '__main__':
    pt1()
    pt1(1000000)




