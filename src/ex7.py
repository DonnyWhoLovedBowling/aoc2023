import os
from line_profiler_pycharm import profile
from copy import deepcopy as dc
from functools import cmp_to_key

in_file = open("../data/ex7.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]
hand_map = {k: v for k,v in [line.split(" ") for line in lines]}
hands = list(hand_map.keys())


def calc_base(hand, pt2=False):

    return pow(15, 4) * char_score(hand[0], pt2) + \
           pow(15, 3) * char_score(hand[1], pt2) + \
           pow(15, 2) * char_score(hand[2], pt2) + \
           pow(15, 1) * char_score(hand[3], pt2) + \
           pow(15, 0) * char_score(hand[4], pt2)


def char_score(c: str, pt2 = False):
    # A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2
    if c.isdigit():
        return int(c)
    elif c == 'T':
        return 10
    elif c == 'J' and not pt2:
        return 11
    elif c == 'Q':
        return 12
    elif c == 'K':
        return 13
    elif c == 'A':
        return 14
    elif c == 'J' and pt2:
        return 1


def scorept1(hand):
    return score(hand, False)
def scorept2(hand1, hand2):
    score1 = score(hand1, True)
    score2 = score(hand2, True)
    if score1 > score2:
        return 1
    if score1 < score2:
        return -1
    if score1 == score2:
        score1 = calc_base(hand1, True)
        score2 = calc_base(hand2, True)
    if score1 > score2:
        return 1
    if score1 < score2:
        return -1
    else:
        return 0

def score(hand, pt2=False):
    cnt_mp = {}
    init_hand = dc(hand)
    if pt2 and 'JJJJJ' == hand:
        return score('AAAAA', True)

    if pt2:
        base = 0
    else:
        base = calc_base(hand)

    for c in hand:
        cnt_mp[c] = hand.count(c)
    cnts = list(cnt_mp.values())
    had_J = False
    if pt2 and 'J' in hand:
        had_J = True
        max_cnt = 0
        max_vals = []
        for c, cnt in cnt_mp.items():
            if cnt >= max_cnt and c != 'J':
                max_cnt = cnt
                max_vals = c
        max_val = max_vals[0]
        hand = hand.replace('J', max_val)
        cnt_mp = {}
        for c in hand:
            cnt_mp[c] = hand.count(c)
        cnts = list(cnt_mp.values())

    if 5 in cnts:
        return base + pow(15,5)*7
    if 4 in cnts:
        return base + pow(15,5)*6
    if 3 in cnts and 2 in cnts:
        return base + pow(15,5)*5
    if 3 in cnts:
        return base + pow(15,5)*4
    if cnts.count(2) == 2:
        return base + pow(15,5)*3
    if 2 in cnts:
        return base + pow(15,5)*2
    elif pt2 and had_J:
        return pow(15,5)
    else:
        return base + pow(15,5)

def pt1():
    hands.sort(key=scorept1)
    total = 0
    for i, hand in enumerate(hands):
        total += (i+1)*int(hand_map[hand])
    print(f"ans pt1: {total}")

def pt2():
    hands_sorted = sorted(hands, key=cmp_to_key(scorept2))

    total = 0
    for i, hand in enumerate(hands_sorted):
        total += (i+1)*int(hand_map[hand])
    print(f"ans pt2: {total}")

pt1()
pt2()




