import math
import sympy
import logging
from logging import info, debug

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex24.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]
hail_stones = list()


def loss_function(h1, h2):
    # px1 + vx1*t = px2 + vx2*t
    # t = (px1-px2)/(vx2-vx1)

    dvx = (h2['vx'] - h1['vx'])
    if dvx != 0:
        tc = (h1['px'] - h2['px']) / dvx
        h1_new = calc_collision_point(h1, tc)
        h2_new = calc_collision_point(h2, tc)
        return calc_distance(h1_new, h2_new)
    else:
        return 1e17


def calc_distance(h1: dict, h2: dict):
    return math.sqrt(pow(h1['px']-h2['px'], 2)+pow(h1['py']-h2['py'], 2)+pow(h1['pz']-h2['pz'], 2))
    # return h1['px']-h2['px'] + h1['py']-h2['py'] + h1['pz']-h2['pz']


def calc_collision_point(h, t):
    h_new = dict()
    h_new['px'] = h['px']+h['vx']*t
    h_new['py'] = h['py']+h['vy']*t
    h_new['pz'] = h['pz']+h['vz']*t
    return h_new


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
    global hail_stoned
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
    # start = datetime.now()
    x, y, z, vx, vy, vz = args
    global hail_stones
    h_sol = dict()
    h_sol['px'] = math.floor(x)
    h_sol['py'] = math.floor(y)
    h_sol['pz'] = math.floor(z)
    h_sol['vx'] = math.floor(vx)
    h_sol['vy'] = math.floor(vy)
    h_sol['vz'] = math.floor(vz)
    total_distance = 0
    collided = 0
    for h_test in hail_stones:
        l = loss_function(h_test, h_sol)
        # debug(l)
        total_distance += l
        if total_distance == 0:
            collided += 1
    debug(collided)
    # print(h_sol)
    # print(total_distance)
    # end = datetime.now()
    # elapsed = difference = end - start
    # print(f"elapsed: {elapsed.microseconds/1000.}" )
    debug(total_distance)
    return total_distance


def pt2():
    x, y, z, vx, vy, vz = sympy.symbols("x, y, z, vx, vy, vz")
    equations = []

    for h in hail_stones:
        vx1 = h['vx']
        vy1 = h['vy']
        vz1 = h['vz']
        x1 = h['px']
        y1 = h['py']
        z1 = h['pz']

        equations.append((x - x1) * (vy1 - vy) - (y - y1) * (vx1 - vx))
        equations.append((x - x1) * (vz1 - vz) - (z - z1) * (vx1 - vx))

    ans = sympy.solve(equations)
    debug(ans)
    info(f"ans pt2 = {ans[0][x]+ans[0][y]+ans[0][z]}")


if __name__ == '__main__':
    pt1()
    pt2()
