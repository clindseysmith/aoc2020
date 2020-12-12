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

in_file_name = "d12_input.txt"
if opts.example > 0:
    in_file_name = "d12_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

loc_x = 0
loc_y = 0
heading = 90

for idx, line in enumerate(data):
    letter, val = line[0], int(line[1:])
    if letter == 'N':
        loc_y += val
    elif letter == 'S':
        loc_y -= val
    elif letter == 'E':
        loc_x += val
    elif letter == 'W':
        loc_x -= val
    elif letter == 'L':
        heading = (heading - val) % 360
    elif letter == 'R':
        heading = (heading + val) % 360
    elif letter == 'F':
        if heading == 0:
            loc_y += val
        elif heading == 90:
            loc_x += val
        elif heading == 180:
            loc_y -= val
        elif heading == 270:
            loc_x -= val
        else:
            raise Exception('Unknown heading {0}, idx {1}, line {2}'.format(heading, idx, line))
    else:
        raise Exception('Unrecognized direction {0}, idx {1}'.format(line, idx))
    if opts.verbose:
        print('{0:3}=>{1:4} => loc: ({2:4},{3:4}), heading: {4:3}, md: {5:4}'.format(idx, line, loc_x, loc_y, heading, abs(loc_x)+abs(loc_y)))

print('PART1: x, y = {0}, {1}   manhattan distance = {2}'.format(loc_x, loc_y, abs(loc_x)+abs(loc_y)))

if not opts.part2:
    sys.exit(0)

loc_x = 0
loc_y = 0
way_x = 10
way_y = 1

for idx, line in enumerate(data):
    letter, val = line[0], int(line[1:])
    if letter == 'N':
        way_y += val
    elif letter == 'S':
        way_y -= val
    elif letter == 'E':
        way_x += val
    elif letter == 'W':
        way_x -= val
    elif letter == 'L':
        while val > 0:
            way_x, way_y = -way_y, way_x
            val -= 90
    elif letter == 'R':
        while val > 0:
            way_x, way_y = way_y, -way_x
            val -= 90
    elif letter == 'F':
        loc_x += val*way_x
        loc_y += val*way_y
    else:
        raise Exception('Unrecognized direction {0}, idx {1}'.format(line, idx))
    if opts.verbose:
        print('{0:3}=>{1:4} => loc: ({2:6},{3:6}), way: ({4:3},{5:3}), md: {6:5}'.format(idx, line, loc_x, loc_y, way_x, way_y, abs(loc_x)+abs(loc_y)))

print('PART2: x, y = {0}, {1}   manhattan distance = {2}'.format(loc_x, loc_y, abs(loc_x)+abs(loc_y)))
