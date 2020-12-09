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

in_file_name = "d09_input.txt"
preamble_len = 25
if opts.example > 0:
    in_file_name = "d09_examples%s.txt" % opts.example
    preamble_len = 5

with open(in_file_name, "r") as f:
    data = [int(x.strip()) for x in f.readlines()]

print(in_file_name, len(data))

for idx in range(preamble_len, len(data)):
    valid = set(data[idx-preamble_len:idx])
    for jdx in range(idx-preamble_len, idx):
        if data[idx] == 2*data[jdx]:
            continue
        if data[idx]-data[jdx] in valid:
            break
    else:
        print('PART1: Did not find two prev {1} numbers in range to sum to {0} at index {2}'.format(data[idx], preamble_len, idx))
        weakness = data[idx]
        break

wsum = data[0]
fdx = 0
ldx = 0
while True:
    if opts.verbose:
        print(fdx, ldx, wsum, wsum - weakness)
    if wsum == weakness:
        break
    elif wsum < weakness:
        ldx += 1
        wsum += data[ldx]
    elif wsum > weakness:
        wsum -= data[fdx]
        fdx += 1
    else:
        raise Exception('Huh? {0}, {1}, {2}, {3}'.format(fdx, ldx, wsum, weakness))

if opts.verbose:
    print(data[fdx:ldx+1])
minnum = min(data[fdx:ldx+1])
maxnum = max(data[fdx:ldx+1])
print('PART2: numbers {0}:{1} sum to weakness. Min= {2}, Max= {3}, Answer= {4}'.format(fdx, ldx, minnum, maxnum, minnum+maxnum))

if not opts.part2:
    sys.exit(0)

