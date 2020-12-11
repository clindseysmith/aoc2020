import os
import sys
import math
import time
import string
import pprint
import itertools
import traceback
import optparse

parser = optparse.OptionParser()
parser.add_option("-v", action="count", dest="verbose", default=0)
parser.add_option("-e", action="count", dest="example", default=0)
parser.add_option("-2", action="store_true", dest="part2", default=False)
parser.add_option("--step", action="store_true", dest="step", default=False)
parser.add_option("--display", action="store_true", dest="display", default=False)
(opts, args) = parser.parse_args()

in_file_name = "d11_input.txt"
if opts.example > 0:
    in_file_name = "d11_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    seat_map = [list(x.strip()) for x in f.readlines()]

nrows = len(seat_map)
ncols = len(seat_map[0])
print(in_file_name, nrows, ncols)

def count_surrounding1(r, c, seat_map):
    r1, r2 = max(0, r-1), min(nrows, r+2)
    c1, c2 = max(0, c-1), min(ncols, c+2)
    o = 0
    for rx in range(r1, r2):
        for cx in range(c1, c2):
            if rx == r and cx == c:
                continue
            try:
                if seat_map[rx][cx] == 'L':
                    o += 1
            except:
                print(rx, cx, 'error')
                raise
    return o

seat_check = {}
for r in range(nrows):
    for c in range(ncols):
        look = set()
        directions = ((1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1))
        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            while nr >= 0 and nr < nrows and nc >= 0 and nc < ncols:
                if seat_map[nr][nc] in ('#' 'L'):
                    look.add((nr, nc))
                    break
                nr, nc = nr+dr, nc+dc
        seat_check[(r, c)] = look

def count_surrounding2(r, c, seat_map):
    count = 0
    for nr, nc in seat_check[(r, c)]:
        if seat_map[nr][nc] == 'L':
            count += 1
    return count

def print_map(idx, seat_map):
    print('idx = {0}'.format(idx))
    for row in seat_map:
        print(''.join(row))
    print('')

if opts.part2:
    count_surrounding = count_surrounding2
    part = 'PART2'
    get_up = 5
else:
    count_surrounding = count_surrounding1
    part = 'PART1'
    get_up = 4

idx = 0
changed = True
while changed and idx<1000:
    idx += 1
    changed = False
    new_map = [['.']*ncols for r in range(nrows)]
    for r in range(nrows):
        for c in range(ncols):
            state = seat_map[r][c]
            if state == '.':
                continue
            s = count_surrounding(r, c, seat_map)
            if s == 0:
                new_map[r][c] = 'L'
                if state == '#':
                    changed = True
            elif s >= get_up:
                new_map[r][c] = '#'
                if state == 'L':
                    changed = True
            else:
                new_map[r][c] = seat_map[r][c]
    seat_map = new_map
    if opts.display:
        print_map(idx, seat_map)
    elif opts.verbose or opts.step:
        print('idx = {0}'.format(idx))
    if opts.step and changed:
        _ = input('press enter')

if changed:
    print('{0}: not enough iterations!'.format(part))
else:
    occupied = sum([row.count('L') for row in seat_map])
    print('{2}: unchanged after {0} iterations, occupied seats = {1}'.format(idx, occupied, part))


