import os
import sys
import math
import time
import string
import pprint
import itertools
import traceback
import optparse
import copy

parser = optparse.OptionParser()
parser.add_option("-v", action="count", dest="verbose", default=0)
parser.add_option("-e", action="count", dest="example", default=0)
parser.add_option("-2", action="store_true", dest="part2", default=False)
parser.add_option("--step", action="store_true", dest="step", default=False)
parser.add_option("--display", action="store_true", dest="display", default=False)
(opts, args) = parser.parse_args()

in_file_name = "d10_input.txt"
if opts.example > 0:
    in_file_name = "d10_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [int(x.strip()) for x in f.readlines()]

print(in_file_name, len(data))

data.append(0)
data.sort()
data.append(data[-1]+3)
diffs = [0]*4
last_d = 0
for d in data[1:]:
    diffs[d-last_d] = diffs[d-last_d]+1
    last_d = d
if opts.verbose:
    print(data)
    print(diffs)
print('PART1: 1-diffs: {0}, 3-diffs: {1}, product: {2}'.format(diffs[1], diffs[3], diffs[1]*diffs[3]))

sdata = set(data)
connections = {}
for idx, d in enumerate(data):
    connections[d] = set()
    for jdx in (1, 2, 3):
        if d+jdx in sdata:
            connections[d].add(d+jdx)

ways_from_here = {}
def extend(num, ways_from_here):
    if num not in ways_from_here:
        total = 0
        for c in connections[num]:
            if c == data[-1]:
                total += 1
            else:
                total += extend(c, ways_from_here)
        ways_from_here[num] = total
        if opts.verbose > 1:
            print(num, total)
    return ways_from_here[num]

arrangements = extend(0, ways_from_here)

print('PART2: There are {0} distinct arrangements'.format(arrangements))
        


                
    


