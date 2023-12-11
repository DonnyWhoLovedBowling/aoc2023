import os
from line_profiler_pycharm import profile
from copy import deepcopy as dc

in_file = open("../data/ex5.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]

@profile
def split_range(r1, r2, t):
    if r1[0] >= r2[0] and r1[1] <= r2[1]: # whole input ranged enclosed
        return [(r1[0]+t, r1[1]+t)]
    if r1[1] <= r2[0] or r1[0] >= r2[1]: # disjoint
        return []
    if r1[0] < r2[1] and r1[0] >= r2[0]: # lower part enclosed
        return [(r2[1], r1[1]), (r1[0]+t, r2[1]+t)]
    if r1[1] <= r2[1] and r1[1] >= r2[0]: # upper part enclosed
        return [(r1[0], r2[0]), (r2[0]+t, r1[1]+t)]
    if r1[0] <= r2[0] and r1[1] >= r2[1]: # input range encloses map-range
        return [(r1[0], r2[0]), (r2[0]+t, r2[1]+t), (r2[1], r1[1])]
    print('error')


@profile
def do_run():
    input = []
    new_input = []
    is_map = False
    for i, line in enumerate(lines):
        if 'seeds:' in line:
            nums = line.split(":")[1].split(" ")
            input = [int(num) for num in nums if len(num) > 0]
            input_zip = list(zip(input[::2], input[1::2]))
            input_ranges = []
            for ix in range(0,len(input_zip)):
                input_ranges.append((input_zip[ix][0], input_zip[ix][0]+input_zip[ix][1]))

        elif 'map:' in line:
            is_map = True
            map_type = line
            old_input = dc(input_ranges)
        elif line == '':
            is_map = False
            input_ranges = input_ranges + new_input
            new_input = []
            changed = set()
        elif is_map:
            nums = line.split(" ")
            mapline = [int(num) for num in nums if len(num) > 0]
            map_range = (mapline[1], mapline[1]+mapline[2])
            delta = mapline[0]-mapline[1]
            for ix, inp in enumerate(dc(input)):
                if ix in changed:
                    continue
                if inp >= mapline[1] and inp < mapline[1]+mapline[2]:
                    input[ix] = inp + delta
                    changed.add(ix)
            for ix, inp in enumerate(dc(input_ranges)):
                split_ranges = split_range(inp, map_range, delta )
                if len(split_ranges) == 1:
                    input_ranges.remove(inp)
                    new_input.append(split_ranges[0])

                if len(split_ranges) == 2:
                    input_ranges.remove(inp)
                    input_ranges.append(split_ranges[0])
                    new_input.append(split_ranges[1])
                if len(split_ranges) == 3:
                    input_ranges.remove(inp)
                    new_input.append(split_ranges[1])
                    input_ranges.append(split_ranges[0])
                    input_ranges.append(split_ranges[2])
        for inp in input_ranges:
            if inp[0] == inp[1]:
                print('error')

    input_ranges = input_ranges + new_input
    for i in input_ranges:
        print(i)
    print(f"ans pt1 = {min(input)}")
    print(f"ans pt2 = {min(list(zip(*input_ranges))[0])}")


do_run()





