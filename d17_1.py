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

in_file_name = "d17_input.txt"
if opts.example > 0:
    in_file_name = "d17_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

space = {}
for ydx, line in enumerate(data):
    if opts.verbose:
        print(line)
    for xdx, char in enumerate(line):
        if char == '#':
            space[(xdx, ydx, 0)] = True

neighbor_offsets = []
for x in (-1, 0, 1):
    for y in (-1, 0, 1):
        for z in (-1, 0, 1):
            if (x, y, z) == (0, 0, 0):
                continue
            neighbor_offsets.append((x, y, z))

def update(x, y, z, space):
    active_neighbors = sum([1 for dx, dy, dz in neighbor_offsets if space.get((x+dx, y+dy, z+dz), False)])
    if space.get((x, y, z), False):
        return active_neighbors in (2, 3)
    else:
        return active_neighbors in (3, )

for cycle in range(6):
    if opts.verbose:
        print('cycle: {0}, count: {1}'.format(cycle, len(space)))
    space_keys = [k for k in space.keys()]
    min_x, min_y, min_z = space_keys[0]
    max_x, max_y, max_z = space_keys[0]
    for x, y, z in space_keys[1:]:
        min_x, min_y, min_z = min(min_x, x), min(min_y, y), min(min_z, z)
        max_x, max_y, max_z = max(max_x, x), max(max_y, y), max(max_z, z)
    new_space = {}
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            for z in range(min_z-1, max_z+2):
                if update(x, y, z, space):
                    new_space[(x, y, z)] = True
    space = new_space

print('PART1: after 6 cycles there are {0} active cubes'.format(len(space)))

if not opts.part2:
    sys.exit(0)

space = {}
for ydx, line in enumerate(data):
    for xdx, char in enumerate(line):
        if char == '#':
            space[(xdx, ydx, 0, 0)] = True

neighbor_offsets = []
for x in (-1, 0, 1): 
    for y in (-1, 0, 1): 
        for z in (-1, 0, 1): 
            for w in (-1, 0, 1): 
                if (x, y, z, w) == (0, 0, 0, 0): 
                    continue
                neighbor_offsets.append((x, y, z, w)) 

def update(x, y, z, w, space):
    active_neighbors = sum([1 for dx, dy, dz, dw in neighbor_offsets if space.get((x+dx, y+dy, z+dz, w+dw), False)])
    if space.get((x, y, z, w), False):
        return active_neighbors in (2, 3)
    else:
        return active_neighbors in (3, )

for cycle in range(6):
    if opts.verbose:
        print('cycle: {0}, count: {1}'.format(cycle, len(space)))
    space_keys = [k for k in space.keys()]
    min_x, min_y, min_z, min_w = space_keys[0]
    max_x, max_y, max_z, max_w = space_keys[0]
    for x, y, z, w in space_keys[1:]:
        min_x, min_y, min_z, min_w = min(min_x, x), min(min_y, y), min(min_z, z), min(min_w, w)
        max_x, max_y, max_z, max_w = max(max_x, x), max(max_y, y), max(max_z, z), max(max_w, w)
    new_space = {}
    for x in range(min_x-1, max_x+2):
        for y in range(min_y-1, max_y+2):
            for z in range(min_z-1, max_z+2):
                for w in range(min_w-1, max_w+2):
                    if update(x, y, z, w, space):
                        new_space[(x, y, z, w)] = True
    space = new_space

print('PART2: after 6 cycles there are {0} active hyper-cubes'.format(len(space)))


