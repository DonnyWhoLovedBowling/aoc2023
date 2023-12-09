import logging
import os
import math
from logging import info, debug, error
from line_profiler_pycharm import profile
from copy import deepcopy as dc
from functools import cmp_to_key

logging.basicConfig(level=logging.INFO)
in_file = open("../data/ex8.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]
instructions = lines[0]
node_map = {}
found = set()

for line in lines[2:]:
    in_node = line.split(" = ")[0]
    line = line.replace("(", "").replace(")", "")
    out_nodes = line.split(" = ")[1].split(", ")
    node_map[in_node] = out_nodes

def new_instruction(instruction_ix):
    global instructions
    instruction = instructions[instruction_ix]
    if instruction == 'L':
        ix = 0
    elif instruction == 'R':
        ix = 1
    else:
        error("instruction not clear!")
    instruction_ix = (instruction_ix + 1) % len(instructions)
    return ix, instruction_ix

def pt1():
    loc = 'AAA'
    instruction_ix = 0
    steps = 0
    while loc != 'ZZZ':
        ix, instruction_ix = new_instruction(instruction_ix)
        loc = node_map[loc][ix]
        steps += 1

    info(f"ans pt1: {steps}")


def pt2():
    nodes = [node for node in list(node_map.keys()) if node[2] == 'A']
    debug(nodes)
    step_map = {}
    for node in nodes:
        instruction_ix = 0
        steps = 0
        loc = dc(node)
        while loc[2] != 'Z':
            ix, instruction_ix = new_instruction(instruction_ix)
            loc = node_map[loc][ix]
            steps += 1
        step_map[node] = steps
        debug((node, steps))
    info(step_map)
    ans = math.lcm(*step_map.values())
    info(f"ans pt2: {ans}")

if __name__ == '__main__':
    pt1()
    pt2()




