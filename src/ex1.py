import os

in_file = open("../data/ex1.txt")
lines = [l.replace('\\n', '') for l in in_file.readlines()]

ans = 0
for line in lines:
    x = 0
    for c in line:
        if c.isdigit():
            x = 10*int(c)
            break
    rev = line[::-1]
    for c in rev:
        if c.isdigit():
            x += int(c)
            break
    ans += x

print(f"part1 ans = {ans}")


def find_number(in_text, dct, text, value):
    ix_all = [i for i in range(len(in_text)) if in_text.startswith(text, i)]
    for i in ix_all:
        dct[i] = value
    return dct


ans = 0
for line in lines:
    ixs = {}
    ixs = find_number(line, ixs, "one", 1)
    ixs = find_number(line, ixs, "two", 2)
    ixs = find_number(line, ixs, "three", 3)
    ixs = find_number(line, ixs, "four", 4)
    ixs = find_number(line, ixs, "five", 5)
    ixs = find_number(line, ixs, "six", 6)
    ixs = find_number(line, ixs, "seven", 7)
    ixs = find_number(line, ixs, "eight", 8)
    ixs = find_number(line, ixs, "nine", 9)
    ixs = find_number(line, ixs, "1", 1)
    ixs = find_number(line, ixs, "2", 2)
    ixs = find_number(line, ixs, "3", 3)
    ixs = find_number(line, ixs, "4", 4)
    ixs = find_number(line, ixs, "5", 5)
    ixs = find_number(line, ixs, "6", 6)
    ixs = find_number(line, ixs, "7", 7)
    ixs = find_number(line, ixs, "8", 8)
    ixs = find_number(line, ixs, "9", 9)

    lvalue = min(ixs.keys())
    rvalue = max(ixs.keys())
    x = 10 * ixs[lvalue]
    x += ixs[rvalue]
    ans += x

print(f"part2 ans = {ans}")

