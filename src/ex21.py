from math import ceil, floor
import logging
from logging import info, debug
from line_profiler_pycharm import profile
from collections import deque
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex21.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]


@profile
def solve(graph, source, max_steps):
    priority_queue = deque()
    priority_queue.append((0, source))
    visited = set()
    final_points = set()
    while priority_queue:
        (current_steps, current_position) = priority_queue.popleft()
        if (current_steps, current_position) in visited:
            continue
        visited.add((current_steps, current_position))
        if current_steps == max_steps:
            final_points.add(current_position)
            continue
        for dx in [1, 0, -1]:
            if dx == 0:
                dy_list = [1, -1]
            else:
                dy_list = [0]
            for dy in dy_list:
                neighbour = (current_position[0] + dx, current_position[1] + dy)
                if (neighbour[0] < 0 or neighbour[1] < 0 or neighbour[0] >= len(graph[0])
                        or neighbour[1] >= len(graph)):
                    continue
                if graph[neighbour[1]][neighbour[0]] == '#':
                    continue
                if (current_steps + 1, neighbour) in visited:
                    continue

                priority_queue.append((current_steps + 1, neighbour))

    return len(final_points)


def pt1():
    start = ()
    n_points = 0
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == 'S':
                start = (j, i)
            if c == '.':
                n_points += 1

    info(f"ans pt1 = {solve(lines, start, 64)}")

    # Middle column, row and border are empty, so gardens can be reached by manhattan distance
    # Better picture: ex21.jpg
    #             SCS
    #            SLELS
    #           SLEOELS
    #          SLEOEOELS
    #          CEOESEOEC
    #          SLEOEOELS
    #           SLEOELS
    #            SLELS
    #             SCS
    #
    # Number of gardens between S and C: N=(26501365-(len(garden)-1/2)/len(garden))-1
    # In a square described above, given a size N, a number of N: (odd, even) gardens are apparent such as:
    # 0: (1, 0), 1: (1, 4), 2: (9, 4), 3: (9, 16), 4: (25, 16)  5: (25, 36).....
    # Number of odd gardens: ((floor(N/2))  * 2 + 1)^2
    # Number of even gardens: ((ceil(N/2) * 2)^2
    #
    # E: Even (fully covered with an even number of steps)
    # O: Odd (fully covered with an odd number of steps)
    # C: Corner (Not fully covered, beam reaches middle of a side with len(garden)-1 steps left
    # L: A large share can be reached, starting at a corner with 2*len(garden) - 1 - (len(garden)-1/2) - 1 steps left
    # S: A small share can be reached, starting at a corner with len(garden) - 1 - (len(garden)-1/2) - 1 steps left
    # Number of L's = N for each side (which each has a different starting point)
    # Number of S's = N+1 for each side

    pt2_steps = 26501365
    n = ((pt2_steps - 65) / 131) - 1
    n_odd = pow(floor(n/2.)*2+1, 2)
    n_even = pow(ceil(n/2.)*2, 2)
    debug((n_odd, n_even))
    tiles_per_odd = solve(lines, start, 135) # empirically verified that N starts alternating > 129 steps
    tiles_per_even = solve(lines, start, 136)
    regulars = tiles_per_odd*n_odd + tiles_per_even*n_even
    debug(f"regulars: {regulars}")

    cl = solve(lines, (130, 65), 130)
    cr = solve(lines, (0, 65), 130)
    ct = solve(lines, (65, 0), 130)
    cb = solve(lines, (65, 130), 130)
    cs = cl + cr + ct + cb
    debug(f"cs: {cs}")

    steps_l = 2*131 - 67
    ltr = solve(lines, (0, 130), steps_l)
    ltl = solve(lines, (130, 130), steps_l)
    lbr = solve(lines, (0, 0), steps_l)
    lbl = solve(lines, (130, 0), steps_l)
    ls = n * (ltr + ltl + lbr + lbl)
    debug(f"ls: {ls}")

    steps_s = 131 - 67
    str_ = solve(lines, (0, 130), steps_s)
    stl = solve(lines, (130, 130), steps_s)
    sbr = solve(lines, (0, 0), steps_s)
    sbl = solve(lines, (130, 0), steps_s)
    ss = (n+1) * (str_ + stl + sbr + sbl)
    debug(f"ss: {ss}")

    total = regulars + cs + ls + ss
    info(f"ans pt2 = {total}")


if __name__ == '__main__':
    pt1()

