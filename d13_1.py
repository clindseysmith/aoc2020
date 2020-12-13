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
times.sort()
l0, b0 = times[-1]
l1, b1 = times[-2]
l2, b2 = times[-3]
print(l0, l1, l2)

if opts.example == 0:
    n = 100000000000000
else:
    n = 1
valid = []
while True:
    if (n+b0)%l0 == 0 and (n+b1)%l1 == 0 and (n+b2)%l2 == 0:
        valid.append(n)
        if len(valid) == 2:
            break
    n += 1
step = valid[1] - valid[0]
print('step = {0}'.format(step))
a0 = int((n+b0)/l0)
a1 = int((n+b1)/l1)
a2 = int((n+b2)/l2)
print('{0} = {1}*{2} + {3}'.format(l0*a0-b0, l0, a0, b0))
print('{0} = {1}*{2} + {3}'.format(l1*a1-b1, l1, a1, b1))
print('{0} = {1}*{2} + {3}'.format(l2*a2-b2, l2, a2, b2))

idx = 0
while True and idx < 100000000:
    idx += 1
    valid = [(n+b)%l == 0 for l, b in times]
    if idx % 1000000 == 0:  
        print(n, valid, valid.count(True))
    if all(valid):
        print('FOUND')
        break
    n += step

if all(valid):
    print('PART2: earliest timestamp = {0}  {1}'.format(n, valid))
else:
    print('P2: Not enough iterations, {0}  {1}'.format(n, valid))

