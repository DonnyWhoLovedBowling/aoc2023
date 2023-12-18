from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

import logging
from logging import info, debug, warning, error
from line_profiler_pycharm import profile

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex18.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]


def add_vec(a, b):
    return tuple(map(sum, zip(a, b)))


def pt1():
    cursor = (0, 0)
    sx1y2 = 0
    sy1x2 = 0
    border_length = 0
    for line in lines:
        inputs = line.split(" ")
        if inputs[0] == 'R':
            direction = (1, 0)
        elif inputs[0] == 'U':
            direction = (0, 1)
        elif inputs[0] == 'L':
            direction = (-1, 0)
        elif inputs[0] == 'D':
            direction = (0, -1)
        else:
            raise ValueError("direction not clear!")
        size = int(inputs[1])
        border_length += size
        new_cursor = add_vec(cursor, (direction[0]*size, direction[1] * size))
        sx1y2 += cursor[0]*new_cursor[1]
        sy1x2 += cursor[1]*new_cursor[0]
        cursor = new_cursor
    area = abs(sy1x2-sx1y2)/2.
    correction = border_length/2 + 1
    info(area+correction)


def pt2():
    cursor = (0, 0)
    sx1y2 = 0
    sy1x2 = 0
    border_length = 0
    for line in lines:
        inputs = line.split(" ")[2]
        dir_code = int(inputs[-2])

        if dir_code == 0:
            direction = (1, 0)
        elif dir_code == 1:
            direction = (0, 1)
        elif dir_code == 2:
            direction = (-1, 0)
        elif dir_code == 3:
            direction = (0, -1)
        else:
            raise ValueError("direction not clear!")
        size = int(inputs[2:-2], 16)
        border_length += size
        new_cursor = add_vec(cursor, (direction[0]*size, direction[1] * size))
        sx1y2 += cursor[0]*new_cursor[1]
        sy1x2 += cursor[1]*new_cursor[0]
        cursor = new_cursor
    area = abs(sx1y2-sy1x2)/2.
    correction = border_length/2 + 1
    info(area+correction)


if __name__ == '__main__':
    pt1()
    pt2()
