import logging
from logging import info, debug
from copy import deepcopy as dc
from functools import reduce
from operator import mul

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex19.txt")
lines = in_file.readlines()
workflows = dict()
total_possibilities = 0
total_impossibilities = 0


def pt1():
    global workflows
    is_rules = True
    parts = []
    for line in lines:
        if line == '\n':
            is_rules = False
            continue
        line = line.replace('\n', '')
        if is_rules:
            name, rules_txt = line.split('{')
            rules = rules_txt[0:-1].split(',')
            workflows[name] = rules
        else:
            parts.append({prt.split('=')[0]: int(prt.split('=')[1]) for prt in line[1:-1].split(',')})

    debug(parts)
    debug(workflows)

    total = 0
    for part in parts:
        decision = ''
        wf_name = 'in'
        while decision == '':
            wf = workflows[wf_name]
            wf_name = ''
            for rule in wf:
                if '<' in rule:
                    var, remainder = rule.split('<')
                    threshold, next_wf = remainder.split(':')
                    if part[var] < int(threshold):
                        wf_name = next_wf
                elif '>' in rule:
                    var, remainder = rule.split('>')
                    threshold, next_wf = remainder.split(':')
                    if part[var] > int(threshold):
                        wf_name = next_wf
                else:
                    wf_name = rule

                if wf_name in 'AR':
                    decision = wf_name
                if wf_name:
                    break
        if decision == 'A':
            total += part['x']+part['m']+part['a']+part['s']

    info(f"ans pt1 = {total}")


def calc_possibilities(constraints, wf_name):
    global total_possibilities, total_impossibilities, workflows
    possibilities = reduce(mul, [(v[1]-v[0]) for k, v in constraints.items()])
    if possibilities < 0:
        return

    new_constraints = dc(constraints)
    debug((wf_name, constraints))

    if wf_name not in 'AR':
        for rule in workflows[wf_name]:
            next_constraints = dc(new_constraints)
            if '<' in rule:
                var, remainder = rule.split('<')
                threshold, next_wf = remainder.split(':')
                cur_constraints = new_constraints[var]
                next_constraints[var] = [cur_constraints[0], min(int(threshold)-1, cur_constraints[1])]
                calc_possibilities(next_constraints, next_wf)
                new_constraints[var] = [next_constraints[var][1], new_constraints[var][1]]

            elif '>' in rule:
                var, remainder = rule.split('>')
                threshold, next_wf = remainder.split(':')
                cur_constraints = new_constraints[var]
                next_constraints[var] = [max(cur_constraints[0], int(threshold)), cur_constraints[1]]
                calc_possibilities(next_constraints, next_wf)
                new_constraints[var] = [new_constraints[var][0], next_constraints[var][0]]
            else:
                calc_possibilities(new_constraints, rule)
    else:
        if wf_name == 'A':
            total_possibilities += possibilities
        else:
            total_impossibilities += possibilities


def pt2():
    global total_possibilities, total_impossibilities
    ratings = ['x', 'm', 'a', 's']
    constraints = {r: [0, 4000] for r in ratings}
    calc_possibilities(constraints, 'in')
    info(f"ans pt2 = {total_possibilities}")
    debug(f"total impossibilities = {total_impossibilities}")
    debug(f"total total = {total_impossibilities+total_possibilities}")


if __name__ == '__main__':
    pt1()
    pt2()
