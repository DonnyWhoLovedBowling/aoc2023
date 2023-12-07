import os
from line_profiler_pycharm import profile
from copy import deepcopy as dc

in_file = open("../data/ex6.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]
times = [int(num) for num in lines[0].split(":")[1].split(" ") if len(num.strip()) > 0]
dists = [int(num) for num in lines[1].split(":")[1].split(" ") if len(num.strip()) > 0]
games = list(zip(times,dists))


def pt1():
    possibilities = []
    for g in games:
        possible = 0
        for v in range(1, g[0]):
            dist = (g[0]-v)*v
            if dist > g[1]:
                possible += 1
        possibilities.append(possible)
    score = 1
    for p in possibilities:
        score *= p
    print(score)

def pt2():
    time_str = ""
    for t in times:
        time_str += str(t)
    time = int(time_str)
    dist_str = ""
    for t in dists:
        dist_str += str(t)
    min_dist = int(dist_str)


    score = 0
    for v in range(1, time):
        dist = (time-v)*v
        if dist > min_dist:
            score += 1
    print(score)

pt1()
pt2()





