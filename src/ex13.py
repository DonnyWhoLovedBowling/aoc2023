import logging
import regex as re
from copy import deepcopy as dc
from logging import info, debug
from line_profiler_pycharm import profile

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex13.txt")
lines = in_file.readlines()
@profile
def pt1(unfold=False):
    total = 0
    rocks = set()

    for i, line in enumerate(lines):

        reqs = [int(n) for n in line.split(" ")[1].split(',')]
        line = line.split(" ")[0]
        if unfold:
            line_list = [line]*5
            line = '?'.join(line_list)
            reqs = reqs*5
        total += find(line, reqs, 0)
        # total = 0
        debug((i, total))
    info(f"total possibilities = {total}")


if __name__ == '__main__':
    pt1()
    pt1(True)
