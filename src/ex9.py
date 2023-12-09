import logging
import os
import math
from logging import info, debug, error
from line_profiler_pycharm import profile
from copy import deepcopy as dc
from functools import cmp_to_key

logging.basicConfig(level=logging.INFO)
in_file = open("../data/ex9.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]

def pt1():
    total1, total2 = 0, 0
    for line in lines:
        level = [int(n) for n in line.split(" ")]
        levels = [level]
        stop = False
        while level.count(0) != len(level):
            new_level = []
            for i in range(1, len(level)):
                new_level.append(level[i]-level[i-1])
            level = new_level
            levels.append(level)
        app = 0
        levels1 = dc(levels)
        for i in range(len(levels1)-1, 0, -1):
            app = levels1[i][-1] + levels1[i-1][-1]
            levels1[i-1].append(app)

        total1 += levels1[0][-1]

        levels2 = dc(levels)
        for i in range(len(levels2)-1, 0, -1):
            app =  levels2[i-1][0] - levels2[i][0]
            levels2[i-1].insert(0, app)

        total2 += levels2[0][0]

    logging.info(f"ans pt1: {total1}")
    logging.info(f"ans pt2: {total2}")
    logging.debug(levels2)

if __name__ == '__main__':
    pt1()




