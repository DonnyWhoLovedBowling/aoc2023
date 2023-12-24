import math
from scipy.optimize import root
import logging
from logging import info, debug

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex24.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]
hail_stones = list()


def calc_intersection_point(h1, h2):
    b1 = h1['py'] + (-1*h1['px'] / h1['vx']) * h1['vy']
    a1 = (h1['py']-b1)/h1['px']

    b2 = h2['py'] + (-1*h2['px'] / h2['vx']) * h2['vy']
    a2 = (h2['py']-b2)/h2['px']
    if a1 == a2:
        return None
    xi = (b2-b1)/(a1-a2)
    yi = a1*xi+b1
    t1 = (yi-h1['py'])/h1['vy']
    t2 = (yi-h2['py'])/h2['vy']

    if t1 < 0 or t2 < 0:
        return None
    return xi, yi


def pt1():
    global hail_stones
    for i, line in enumerate(lines):
        hail = dict()
        hail['px'], hail['py'], hail['pz'] = tuple(map(int, line.split("@")[0].split(',')))
        hail['vx'], hail['vy'], hail['vz'] = tuple(map(int, line.split("@")[1].split(',')))
        hail_stones.append(hail)

    lower = 200000000000000
    upper = 400000000000000
    # lower = 7
    # upper = 27
    total_collisions = 0.
    for i, h1 in enumerate(hail_stones):
        for j, h2 in enumerate(hail_stones):
            if j >= i:
                continue

            i_point = calc_intersection_point(h1, h2)
            if i_point is not None:
                cx, cy = i_point
                if lower <= cx <= upper and lower <= cy <= upper:
                    debug((cx, cy))
                    # assert calc_intersection_point(h1, tx) == calc_intersection_point(h2, tx)
                    total_collisions += 1

    info(f"ans pt1 = {total_collisions}")


def optimize_wrapper(args):
    global hail_stones
    x, y, z, vx, vy, vz = args
    equations = []

    for i, h in enumerate(hail_stones):
        vx1 = h['vx']
        vy1 = h['vy']
        vz1 = h['vz']
        x1 = h['px']
        y1 = h['py']
        z1 = h['pz']

        equations.append((x - x1) * (vy1 - vy) - (y - y1) * (vx1 - vx))
        equations.append((x - x1) * (vz1 - vz) - (z - z1) * (vx1 - vx))

    return equations


def pt2():
    result = root(optimize_wrapper, [1e14, 1e14, 1e14, 100, 100, 100], method='lm')
    info(f"ans pt2 = {int(sum(result['x'][0:3]))}")


if __name__ == '__main__':
    pt1()
    pt2()
