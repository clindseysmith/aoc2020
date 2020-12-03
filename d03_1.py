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

in_file_name = "d03_input.txt"
if opts.example > 0:
    in_file_name = "d03_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

n_cols = len(data[0])
n_rows = len(data)

def is_tree(x, y):
    if y >= n_rows:
        raise Exception('past last row {0} >= {1}'.format(y, n_rows))
    return data[y][x%n_cols] == '#'

tcount = sum([1 for y in range(n_rows) if is_tree(3*y, y)])
print('PART1: {0} trees'.format(tcount))

if not opts.part2:
    sys.exit(0)

slopes = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]

tree_count = []
for dx, dy in slopes:
    tcount = sum([1 for xdx, y in enumerate(range(0, n_rows, dy)) if is_tree(dx*xdx, y)])
    tree_count.append(tcount)
tcount = 1
for tc in tree_count:
    tcount *= tc
print(tree_count)
print('PART2: {0}'.format(tcount))

