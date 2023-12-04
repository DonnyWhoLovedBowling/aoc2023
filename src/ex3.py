import os
from line_profiler_pycharm import profile

in_file = open("../data/ex3.txt")
lines = [l.replace('\\n', '') for l in in_file.readlines()]


@profile
def do_run():
    parts = []
    symbols = set()
    gears = set()
    for y, line in enumerate(lines):
        num = ''
        coordinates = []
        for x, t in enumerate(line.replace('\n', '')):
            coordinate = (x, y)
            if t.isdigit():
                num += t
                coordinates.append(coordinate)
                if x == (len(line.replace('\n', ''))-1):
                    parts.append((int(num), coordinates))
                    coordinates = []
                    num = ''

            elif len(num) > 0:
                parts.append((int(num), coordinates))
                coordinates = []
                num = ''
            if (not t.isalnum()) and t != '.':
                symbols.add(coordinate)
                if t == '*':
                    gears.add(coordinate)
                # print(t)
    total = 0
    for p in parts:
        n, coordinates = p[0], p[1]
        is_part = False
        for c in coordinates:
            if is_part:
                break
            for dx in [-1, 0, 1]:
                if is_part:
                    break
                x = c[0] + dx
                if x < 0 or x > len(lines[0].replace('\n', '')):
                    continue
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    y = c[1] + dy
                    if y < 0 or y > len(lines):
                        continue
                    if (x, y) in symbols:
                        is_part = True
                        total += n
                        break

    print(f"ans pt 1: {total}")
    total = 0

    for g in gears:
        pts = set()
        for p in parts:
            n, coordinates = p[0], p[1]
            for c in coordinates:
                dx = g[0] - c[0]
                if abs(dx) > 1:
                    continue
                dy = g[1] - c[1]
                if abs(dy) > 1:
                    continue
                pts.add(n)
        if len(pts) != 2:
            continue
        first = pts.pop()
        second = pts.pop()
        total += first*second
    print(f"ans pt 2: {total}")


do_run()





