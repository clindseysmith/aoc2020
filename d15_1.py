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

starting_numbers_by_ex = {
    0: [1, 0, 16, 5, 17, 4],
    1: [0, 3, 6],
    2: [1, 3, 2],
    3: [2, 1, 3],
    4: [1, 2, 3],
    5: [2, 3, 1],
    6: [3, 2, 1],
    7: [3, 1, 2]
}
starting_numbers = starting_numbers_by_ex[opts.example]
print('Staring numbers: {0}'.format(starting_numbers))

spoken = {}
last = starting_numbers[0]
for idx, num in enumerate(starting_numbers):
    spoken[last] = idx
    last = num
for idx in range(len(starting_numbers), 2020):
    if last in spoken:
        next_num = idx - spoken[last]
    else:
        next_num = 0
    spoken[last] = idx
    last = next_num
print('PART1: 2020th number spoken = {0}'.format(last))


if not opts.part2:
    sys.exit(0)

for idx in range(2020, 30000000):
    if last in spoken:
        next_num = idx - spoken[last]
    else:
        next_num = 0
    spoken[last] = idx
    last = next_num
print('PART2: 30000000th number spoken = {0}'.format(last))

