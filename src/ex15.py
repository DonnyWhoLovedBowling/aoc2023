import logging
from logging import info, debug, warning
from line_profiler_pycharm import profile

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex15.txt")
words = [l.replace('\n', '') for l in in_file.readlines()][0].split(',')
cols = []
rows = []


@profile
def find_ix(box, label):
    ix = -1
    for i in range(len(box)):
        if box[i][0] == label:
            ix = i
            break
    return ix


@profile
def solution(pt2=False):
    total_score = 0
    hashmap = dict()
    for word in words:
        score = 0
        label = ''
        for c in word:
            if pt2 and c in '=-':
                box = score
                if box in hashmap.keys():
                    if c == '-':
                        ix = find_ix(hashmap[box], label)
                        if ix != -1:
                            del hashmap[box][ix]
                    elif c == '=':
                        ix = find_ix(hashmap[box], label)
                        if ix != -1:
                            hashmap[box][ix][1] = int(word[-1])
                        else:
                            hashmap[box].append([label, int(word[-1])])

                    else:
                        warning("c not clear")
                elif c == '=':
                    hashmap[box] = [[label, int(word[-1])]]

            score += ord(c)
            score *= 17
            score %= 256
            label += c

        total_score += score
    if pt2:
        info(hashmap)
        score = 0
        for box, lenses in hashmap.items():
            for i, lens in enumerate(lenses):
                score += (i+1)*(box+1)*lens[1]
                debug(f"{box}, {lens}, score: {score}")
        info(f"ans pt2 = {score}")
    else:
        info(f"ans pt1 = {total_score}")


if __name__ == '__main__':
    solution()
    solution(True)
