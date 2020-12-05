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

in_file_name = "d05_input.txt"
if opts.example > 0:
    in_file_name = "d05_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

def str_to_row_col(s):
    row = int(s[:7].replace('F', '0').replace('B', '1'), 2)
    col = int(s[7:].replace('L', '0').replace('R', '1'), 2)
    return row, col

def row_col_to_sid(r, c):
    return r*8 + c

seen = []
for line in data:
    r, c = str_to_row_col(line)
    sid = row_col_to_sid(r, c)
    seen.append((sid, r, c, line))

if opts.example > 0:
    pprint.pprint(seen)

seen.sort()
print('PART1: max sid= {0} row= {1}, col= {2} str= {3}'.format(*seen[-1]))

sids = set([s[0] for s in seen])
for sid in range(1, row_col_to_sid(127, 8)):
    if sid not in sids and sid-1 in sids and sid+1 in sids:
        print('PART2: {0} is open, {1} and {2} exist'.format(sid, sid-1, sid+1))

if not opts.part2:
    sys.exit(0)

