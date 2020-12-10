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
if opts.verbose:
    print(data)

last_d = 0
diffs = [0]*4

run_len = 1
run_lens = [0]*7
arrs_per_len = [1, 1, 1, 2, 4, 7, 12]
arrangements = 1
for idx, d in enumerate(data[1:]):
    diffs[d-last_d] = diffs[d-last_d]+1
    if d - last_d > 1:
        run_lens[run_len] = run_lens[run_len] + 1
        if opts.verbose:
            print(' [{0}] ({1})'.format(','.join([str(n) for n in data[idx-run_len+1:idx+1]]), run_len))
        arrangements = arrangements * arrs_per_len[run_len]
        run_len = 1
    else:
        run_len += 1
    last_d = d

if opts.verbose:
    print(diffs)
print('PART1: 1-diffs: {0}, 3-diffs: {1}, product: {2}'.format(diffs[1], diffs[3], diffs[1]*diffs[3]))

if opts.verbose:
    print(' Run lengths:', run_lens)
print('PART2: There are {0} distinct arrangements'.format(arrangements))


