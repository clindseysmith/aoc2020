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

in_file_name = "d06_input.txt"
if opts.example > 0:
    in_file_name = "d06_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

def process_group(group):
    c1 = [any([l in p for p in group]) for l in string.ascii_lowercase]
    c2 = [all([l in p for p in group]) for l in string.ascii_lowercase]
    return c1.count(True), c2.count(True)

groups = []
group = []
for line in data:
    if line == '':
        group = [set(p) for p in group]
        groups.append(process_group(group))
        group = []
    else:
        group.append(line)
groups.append(process_group(group))

if opts.example > 0:
    pprint.pprint(groups)

print('PART1: {0} groups, {1} sum of any-yes answers per group'.format(len(groups), sum([g[0] for g in groups])))
print('PART2: {0} groups, {1} sum of all-yes answers per group'.format(len(groups), sum([g[1] for g in groups])))


