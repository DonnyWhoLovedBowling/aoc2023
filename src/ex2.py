import os

in_file = open("../data/ex2.txt")
lines = [l.replace('\\n', '') for l in in_file.readlines()]


def do_run(pt):
    ans = 0
    for line in lines:
        game_id = 0
        blue, green, red = [], [], []
        num = ''
        for i, t in enumerate(line):
            if t.isdigit():
                num += t
            if t == ':':
                game_id = int(num)
                num = ''
            if line[i:i+3] == 'red':
                red.append(int(num))
                num = ''
            if line[i:i+5] == 'green':
                green.append(int(num))
                num = ''
            if line[i:i+4] == 'blue':
                blue.append(int(num))
                num = ''
        if pt == 1 and (max(red) <= 12 and max(green) <= 13 and
                        max(blue) <= 14):
            ans += game_id

        if pt == 2:
            ans += max(red)*max(blue)*max(green)
    return ans


print(f"ans pt1: {do_run(1)}")
print(f"ans pt2: {do_run(2)}")






