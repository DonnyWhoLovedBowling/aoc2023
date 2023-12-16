import sys
import logging
from logging import info, debug, warning, error
from line_profiler_pycharm import profile

sys.setrecursionlimit(1000)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex16.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]
energized = set()
trajectory = set()
# checked = 0


def in_scope(pos):
    x = pos[0]
    y = pos[1]
    in_scope = (0 <= y < len(lines)) and (0 <= x < len(lines[0]))
    return in_scope


def add_vec(a, b):
    return tuple(map(sum, zip(a, b)))


def move_beam(init_direction, init_position):
    global lines, energized, trajectory
    beams = [(init_direction, init_position)]
    while len(beams) > 0:
        beam = beams.pop(0)
        direction = beam[0]
        pos = beam[1]
        key = (str(direction), str(pos))
        if key in trajectory:
            continue
        trajectory.add(key)
        if in_scope(pos):
            tile = lines[pos[1]][pos[0]]
            energized.add(pos)
            # debug(f"{pos} {direction} {tile}")
        else:
            continue

        if tile == '.':
            beams.append((direction, add_vec(direction, pos)))
        elif tile == '|':
            if direction[0] in [1, -1]:
                dir1 = (0, 1)
                dir2 = (0, -1)
                beams.append((dir1, add_vec(dir1, pos)))
                beams.append((dir2, add_vec(dir2, pos)))
            else:
                beams.append((direction, add_vec(direction, pos)))
        elif tile == '-':
            if direction[1] in [1, -1]:
                dir1 = (1, 0)
                dir2 = (-1, 0)
                beams.append((dir1, add_vec(dir1, pos)))
                beams.append((dir2, add_vec(dir2, pos)))
            else:
                beams.append((direction, add_vec(direction, pos)))
        elif tile == '/':
            if direction[0] in [1, -1]:
                new_dir = (0, -direction[0])
            else:
                new_dir = (-direction[1], 0)

            beams.append((new_dir, add_vec(new_dir, pos)))
        elif tile == '\\':
            if direction[0] in [1, -1]:
                new_dir = (0, direction[0])
            else:
                new_dir = (direction[1], 0)
            beams.append((new_dir, add_vec(new_dir, pos)))
    return

@profile
def solution():
    global energized, trajectory, lines
    direction = (1, 0)
    pos = (0, 0)
    move_beam(direction, pos)
    info(f"ans pt1 = {len(energized)}")
    max_score = len(energized)
    for direction in [(1, 0), (-1, 0)]:
        for i in range(0, len(lines)):
            energized = set()
            trajectory = set()
            if direction == (1, 0):
                pos = (0, i)
            else:
                pos = (len(lines[0])-1, i)
            move_beam(direction, pos)
            if len(energized) > max_score:
                max_score = len(energized)
                debug(f"improved score: {direction} {pos} {max_score}")

    for direction in [(0, 1), (0, -1)]:
        for i in range(0, len(lines[0])):
            energized = set()
            trajectory = set()
            if direction == (0, 1):
                pos = (i, 0)
            else:
                pos = (i, len(lines)-1)
            move_beam(direction, pos)
            if len(energized) > max_score:
                max_score = len(energized)
                debug(f"improved score: {direction} {pos} {max_score}")
    info(f"ans pt2: {max_score}")

if __name__ == '__main__':
    solution()
