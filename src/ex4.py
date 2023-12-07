import os
from line_profiler_pycharm import profile

in_file = open("../data/ex4.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]

@profile
def add_n_cards(card_deck: {}, i, n: int):
    for c in range(i+1, i+n+1):
        if c in card_deck:
            card_deck[c] += card_deck[i]
        else:
            card_deck[c] = card_deck[i]
    return  card_deck

@profile
def do_run():
    total = 0
    card_deck = {}
    for c in range(1, len(lines)+1):
        card_deck[c] = 1
    for i, line in enumerate(lines):
        numbers = line.split(": ")
        input = numbers[1].split(" | ")
        winning = input[0].split(" ")
        mine = input[1].split(" ")
        winning = set(filter(lambda x: len(x) > 0, winning))
        mine = set(filter(lambda x: len(x) > 0, mine))
        intersect = winning.intersection(mine)
        n_overlap  = len(intersect)
        card_deck = add_n_cards(card_deck, i+1, n_overlap)
        if n_overlap > 0:
            total += pow(2, n_overlap-1)


    print(f"ans1 = {total}")
    print(f"ans2 = {sum(card_deck.values())}")

do_run()





