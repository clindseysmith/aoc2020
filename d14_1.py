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

in_file_name = "d14_input.txt"
if opts.example > 0:
    in_file_name = "d14_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

def update_mask(bitmask):
    mask0 = 0
    mask1 = 0
    for bit in bitmask:
        mask0 = mask0 << 1
        mask1 = mask1 << 1
        if bit == '0':
            mask0 += 0
            mask1 += 0
        elif bit == '1':
            mask0 += 1
            mask1 += 1
        elif bit == 'X':
            mask0 += 1
            mask1 += 0
        else:
            raise Exception('unrecognized bit {0}'.format(bit))
    return mask0, mask1

def apply_mask(val, mask):
    return (val & mask[0]) | mask[1]

mask = 0, 0
memory = {}
for line in data:
    if line.startswith('mask'):
        mask = update_mask(line.split(' = ')[1])
        c = line.count('X')
    else:
        memloc, val = line.split(' = ')
        loc = int(memloc[4:-1])
        memory[loc] = apply_mask(int(val), mask)

total = sum([memory[loc] for loc in memory])
print('PART1: sum of memory locations is {0}'.format(total))

if not opts.part2:
    sys.exit(0)

def update_mask2(bitmask):
    x_locs = [idx for idx, bit in enumerate(bitmask[::-1]) if bit == 'X']
    base_mask = 0
    for bit in bitmask:
        base_mask = base_mask << 1
        if bit == '1':
            base_mask += 1
    return base_mask, x_locs

def apply_mask2(baseloc, masks):
    base_mask, x_locs = masks
    x_count = len(x_locs)
    addresses = []
    for mdx in range(2**x_count):
        addr = baseloc | base_mask
        for b in range(x_count):
            if mdx & (1 << b):
                addr = addr | (1 << x_locs[b])
            else:
                if addr & (1 << x_locs[b]):
                    addr = addr ^ (1 << x_locs[b])
        addresses.append(addr)
    return addresses

masks = (0, [0])
memory = {}
for line in data:
    if line.startswith('mask'):
        masks = update_mask2(line.split(' = ')[1])
    else:
        memloc, val = line.split(' = ')
        baseloc = int(memloc[4:-1])
        if opts.verbose > 1:
            print('baseloc = {0}, addresses per baseloc = {1}'.format(baseloc, 2**len(masks[1])))
        for addr in apply_mask2(baseloc, masks):
            if opts.verbose > 1:
                print('  addr = {0}'.format(addr))
            memory[addr] = int(val)
if opts.verbose:
    pprint.pprint(memory)
total = sum([memory[loc] for loc in memory])
print('PART2: sum of memory locations is {0}'.format(total))

