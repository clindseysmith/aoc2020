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

in_file_name = "d02_input.txt"
if opts.example > 0:
    in_file_name = "d02_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

good_passwords = 0
for line in data:
    policy, password = line.split(': ')
    minmax, letter = policy.split(' ')
    minl, maxl = minmax.split('-')
    minl, maxl = int(minl), int(maxl)
    n = password.count(letter)
    if n >= minl and n <= maxl:
        if opts.verbose > 0:
            print("GOOD:", minl, maxl, letter, password, n)
        good_passwords += 1
    else:
        if opts.verbose > 0:
            print("BAAD:", minl, maxl, letter, password, n)

print('PART1: {0} of {1} passwords are good'.format(good_passwords, len(data)))

if not opts.part2:
    sys.exit(0)

good_passwords = 0
for line in data:
    policy, password = line.split(': ')
    positions, letter = policy.split(' ')
    pos1, pos2 = positions.split('-')
    pos1, pos2 = int(pos1)-1, int(pos2)-1
    good = (password[pos1] == letter) ^ (password[pos2] == letter)
    if good:
        if opts.verbose > 0:
            print("GOOD:", pos1, pos2, letter, password, password[pos1], password[pos2])
        good_passwords += 1
    else:
        if opts.verbose > 0:
            print("BAAD:", pos1, pos2, letter, password, password[pos1], password[pos2])

print('PART2: {0} of {1} passwords are good'.format(good_passwords, len(data)))

