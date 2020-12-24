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

in_file_name = "d24_input.txt"
if opts.example > 0:
    in_file_name = "d24_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

drow = {
    'e': 0,
    'a': 1,
    'b': 1,
    'w': 0,
    'c': -1,
    'd': -1
}
ddiag = {
    'e': 1,
    'a': 0,
    'b': -1,
    'w': -1,
    'c': 0,
    'd': 1
}

def walk(line):
    steps = list(line.replace('se', 'a').replace('sw', 'b').replace('nw', 'c').replace('ne', 'd'))
    row, diag = 0, 0
    for step in steps:
        row, diag = row + drow[step], diag + ddiag[step]
    return row, diag

black_tiles = set()
for line in data:
    row, diag = walk(line)
    if (row, diag) in black_tiles:
        black_tiles.remove((row, diag))
    else:
        black_tiles.add((row, diag))

print('PART1: total black tiles = {0}'.format(len(black_tiles)))

def neighbors(tile):
    row, diag = tile
    return set([(row+drow[step], diag+ddiag[step]) for step in ('e', 'a', 'b', 'w', 'c', 'd')])

def hex_conway(tiles):
    new_tiles = set()
    tiles_to_check = tiles.copy()
    for tile in tiles:
        tiles_to_check.update(neighbors(tile))
    for tile in tiles_to_check:
        count = len([n for n in neighbors(tile) if n in tiles])
        if tile in tiles:
            # starts black
            if count in (1, 2):
                new_tiles.add(tile)
        else:
            # starts while
            if count == 2:
                new_tiles.add(tile)
    return new_tiles

n_days = 100
for day in range(n_days):
    black_tiles = hex_conway(black_tiles)
    if opts.verbose > 1 or (opts.verbose > 0 and day < 10 or day % 10 == 9):
        print('Day {0}: {1}'.format(day+1, len(black_tiles)))

print('PART2: total black tiles = {0}'.format(len(black_tiles)))

