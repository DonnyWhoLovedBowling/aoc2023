import logging
from line_profiler_pycharm import profile

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

in_file = open("../data/ex14.txt")
lines = [l.replace('\n', '') for l in in_file.readlines()]
cols = []
rows = []


def count_north_weight():
    global cols, rows
    total_score = 0
    for i, col in enumerate(cols):
        for j, c in enumerate(col):
            if c == 'O':
                total_score += (len(col) - j)
    print(total_score)


@profile
def shift_north():
    global cols, rows
    for i, col in enumerate(cols):
        block = len(col)
        for j, c in enumerate(col):
            if c == 'O':
                row_ix = len(col) - block
                cols[i][j] = '.'
                cols[i][row_ix] = 'O'
                rows[j][i] = '.'
                rows[row_ix][i] = 'O'
                block -= 1
            if c == '#':
                block = len(col) - (j + 1)


@profile
def shift_west():
    global cols, rows
    for i, row in enumerate(rows):
        block = len(row)
        for j, c in enumerate(row):
            if c == 'O':
                col_ix = len(row) - block
                rows[i][j] = '.'
                rows[i][col_ix] = 'O'
                cols[j][i] = '.'
                cols[col_ix][i] = 'O'
                block -= 1
            if c == '#':
                block = len(row) - (j + 1)


@profile
def shift_south():
    global cols, rows
    for i, col in enumerate(cols):
        block = len(col) - 1
        for j, c in enumerate(reversed(col)):
            if c == 'O':
                row_ix = block
                this_row = len(col) - (j + 1)
                cols[i][this_row] = '.'
                cols[i][row_ix] = 'O'
                rows[this_row][i] = '.'
                rows[row_ix][i] = 'O'
                block -= 1
            if c == '#':
                block = len(col) - (j + 2)


@profile
def shift_east():
    global cols, rows
    for i, row in enumerate(rows):
        block = len(row) - 1
        for j, c in enumerate(reversed(row)):
            if c == 'O':
                col_ix = block
                this_row = len(row) - (j + 1)
                rows[i][this_row] = '.'
                rows[i][col_ix] = 'O'
                cols[this_row][i] = '.'
                cols[col_ix][i] = 'O'
                block -= 1
            if c == '#':
                block = len(row) - (j + 2)


@profile
def pt1():
    global cols, rows
    for line in lines:
        rows.append([*line])
        for j, c in enumerate(line):
            if len(cols) > j:
                cols[j].append(c)
            else:
                cols.append([c])

    n = 1000000000
    for i in range(1, n):
        shift_north()
        shift_west()
        shift_south()
        shift_east()
        count_north_weight()

    #
    # print range of shifts, find the repetition pattern. For the example it is: (1000000000-3)%7
    # For the real exercise: (1000000000-115)%42
    #
    for r in rows:
        print(r)


if __name__ == '__main__':
    pt1()
