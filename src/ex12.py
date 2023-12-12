import logging
import regex as re
from copy import deepcopy as dc
from logging import info, debug
from line_profiler_pycharm import profile

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex12.txt")
lines = [line.replace('\n', '') for line in in_file.readlines()]
regex_map = dict()
find_map = dict()


@profile
def calc_regex(sizes):
    global regex_map
    if str(sizes) in regex_map.keys():
        return regex_map[str(sizes)]
    new_sizes = dc(sizes)
    size = new_sizes.pop(0)
    if len(new_sizes) == 0:
        regex = f"[#?]{{{size}}}(?![#])"
    else:
        regex = f"[#?]{{{size}}}[.?]{{1}}"
        for i, s in enumerate(new_sizes):
            if i == len(new_sizes) - 1:
                regex += f"(?=[.?]*[#?]{{{s}}}(?![#])"
            else:
                regex += f"(?=[.?]*[#?]{{{s}}}[.?]+"
        regex += ")"*len(new_sizes)
    regex_map[str(sizes)] = regex
    return regex


@profile
def find(sub_line: str, sizes: list, possibilities):
    global find_map
    key = sub_line+str(sizes)
    if key in find_map.keys():
        return find_map[key]
    regexp = calc_regex(sizes)
    regs1 = re.finditer(regexp, sub_line, overlapped=True)
    for r in regs1:
        if sub_line[0:r.start()].find('#') != -1:
            continue
        new_sub_line = sub_line[r.end():]
        if len(sizes) > 1:
            possibilities += find(new_sub_line, sizes[1:], 0)
        elif new_sub_line.find('#') != -1:
            continue
        else:
            possibilities += 1
    find_map[key] = possibilities
    return possibilities


@profile
def pt1(unfold=False):
    total = 0
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
