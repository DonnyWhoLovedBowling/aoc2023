import logging
import os
import math
from logging import info, debug, error
from line_profiler_pycharm import profile
from copy import deepcopy as dc
from functools import cmp_to_key

logging.basicConfig(level=logging.DEBUG)
in_file = open("../data/ex10.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]


def pt1():
    ix, iy = (-1, -1)
    for y, line in enumerate(lines):
        ix = line.find('S')
        if ix != -1:
            iy = y
            break
    if (ix, iy) == (-1, -1):
        error("S not found!")
    instruction = ''
    start = (ix, iy)
    loop = [start]
    if lines[iy+1][ix] in ['|', 'J', 'L']:
        loop.append((ix, iy+1))
        instruction = lines[iy+1][ix]
    elif lines[iy][ix+1] in ['-', 'J', '7']:
        loop.append((ix+1, iy))
        instruction = lines[iy][ix+1]
    elif lines[iy][ix-1] in ['-', 'F', 'L']:
        loop.append((ix-1, iy))
        instruction = lines[iy][ix-1]
    elif lines[iy-1][ix] in ['|', 'F', '7']:
        loop.append((ix, iy-1))
        instruction = lines[iy-1][ix]

    while True:
        ix = loop[-1][0]
        iy = loop[-1][1]
        if instruction == '|':
            if start in [(ix, iy - 1), (ix, iy + 1)] and len(loop) > 2:
                break
            if (ix, iy-1) in loop:
                loop.append((ix, iy+1))
                instruction = lines[iy+1][ix]
            else:
                loop.append((ix, iy-1))
                instruction = lines[iy-1][ix]
        elif instruction == '-':
            if start in [(ix + 1, iy), (ix - 1, iy)] and len(loop) > 2:
                break
            if (ix-1, iy) in loop:
                loop.append((ix+1, iy))
                instruction = lines[iy][ix+1]
            else:
                loop.append((ix-1, iy))
                instruction = lines[iy][ix-1]
        elif instruction == 'L':
            if start in [(ix, iy - 1), (ix + 1, iy)] and len(loop) > 2:
                break
            if (ix+1, iy) in loop:
                loop.append((ix, iy-1))
                instruction = lines[iy-1][ix]
            else:
                loop.append((ix+1, iy))
                instruction = lines[iy][ix+1]
        elif instruction == 'J':
            if start in [(ix, iy - 1), (ix - 1, iy)]  and len(loop) > 2:
                break
            if (ix-1, iy) in loop:
                loop.append((ix, iy-1))
                instruction = lines[iy-1][ix]
            else:
                loop.append((ix-1, iy))
                instruction = lines[iy][ix-1]
        elif instruction == '7':
            if start in [(ix, iy + 1), (ix - 1, iy)] and len(loop) > 2:
                break
            if (ix-1, iy) in loop:
                loop.append((ix, iy+1))
                instruction = lines[iy+1][ix]
            else:
                loop.append((ix-1, iy))
                instruction = lines[iy][ix-1]
        elif instruction == 'F':
            if start in [(ix, iy + 1), (ix + 1, iy)] and len(loop) > 2:
                break
            if (ix+1, iy) in loop:
                loop.append((ix, iy+1))
                instruction = lines[iy+1][ix]
            else:
                loop.append((ix+1, iy))
                instruction = lines[iy][ix+1]

    info(f"ans pt1: {len(loop)/2}")
    debug(loop)
    inside_points = 0

    R = input('Replace S with? ')
    for y, line in enumerate(lines):
        crossings = 0
        last_loop = False
        in_c = ''
        line = line.replace('S', R)
        for x, c in enumerate(line):
            if (x, y) in loop:
                if c == '|' or (in_c == 'F' and c == 'J') or (in_c == 'L' and c == '7'):
                    crossings += 1
                    in_c = ''
                if c == 'F' or c == 'L':
                    in_c = c
                last_loop = True
            else:
                if (crossings % 2) == 1:
                    debug((x,y,c,crossings))
                    inside_points += 1
                last_loop = False
                in_c = ''
            last_c = c

    info(f"ans pt2: {inside_points}")


if __name__ == '__main__':
    pt1()




