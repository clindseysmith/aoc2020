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

in_file_name = "d13_input.txt"
if opts.example > 0:
    in_file_name = "d13_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

arrive = int(data[0])
buses = [int(x) for x in data[1].split(',') if x != 'x']
print(arrive, buses)

waits = [(bus-arrive%bus, bus) for bus in buses]
waits.sort()
print('PART1: would wait {0} mins for bus {1}, answer: {2}'.format(waits[0][0], waits[0][1], waits[0][0]*waits[0][1]))

times = [(int(x), idx) for idx, x in enumerate(data[1].split(',')) if x != 'x']
print(times)
times.sort(reverse=True)
print(times)

if opts.example == 0:
    n = 100000000000000
else:
    n = 1
tdx = 0
step = 1
while True:
    if (n+times[tdx][1])%times[tdx][0] == 0:
        step *= times[tdx][0]
        tdx += 1
        print('{0} satisfies {1}/{2} buses, step = {3}'.format(n, tdx, len(times), step))
        if tdx == len(times):
            break
    n += step

print('PART2: earliest timestamp = {0}'.format(n))

