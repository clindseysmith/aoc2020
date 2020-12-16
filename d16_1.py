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

in_file_name = "d16_input.txt"
if opts.example > 0:
    in_file_name = "d16_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

rules = []
valid_nums = [False]*1000
for idx1, line in enumerate(data):
    if line == '':
        break
    field, ranges = line.split(': ')
    range1, range2 = ranges.split(' or ')
    valids = set()
    for rng in (range1, range2):
        start, stop = rng.split('-')
        for num in range(int(start), int(stop)+1):
            valid_nums[num] = True
            valids.add(num)
    rules.append((field, valids))
        
my_ticket = []
for idx2, line in enumerate(data[idx1+1:]):
    if line == '':
        break
    print(line)
    if line.startswith('your'):
        continue
    my_ticket = [int(x) for x in line.split(',')]
print(my_ticket)

nearby_tickets = []
for idx3, line in enumerate(data[idx1+idx2+3:]):
    nearby_tickets.append([int(x) for x in line.split(',')])
print(len(nearby_tickets))

invalid_sum = 0
valid_tickets = []
for ticket in nearby_tickets:
    invalids =  sum([num for num in ticket if not valid_nums[num]])
    invalid_sum += invalids
    if invalids == 0:
        valid_tickets.append(ticket)
print('PART1: sum of invalid nums in nearby_tickets: {0}'.format(invalid_sum))

print(len(valid_tickets))
num_fields = len(rules)
fields = []
for idx in range(num_fields):
    fields.append([True]*num_fields)

for ticket in valid_tickets:
    for tdx in range(num_fields):
        for rdx in range(num_fields):
            _, valids = rules[rdx]
            if ticket[tdx] not in valids:
                fields[rdx][tdx] = False

for rdx in range(num_fields):
    print(rdx, fields[rdx].count(True), fields[rdx])

field_poss = [(field.count(True), rdx) for rdx, field in enumerate(fields)]
field_poss.sort()
print(field_poss)
for _, rdx in field_poss:
    if fields[rdx].count(True) == 1:
        fdx1 = fields[rdx].index(True)
        print('Removing {0} from all but {1}'.format(fdx1, rdx))
        for fdx2 in range(num_fields):
            if fdx2 == rdx:
                continue
            fields[fdx2][fdx1] = False

for rdx in range(num_fields):
    print(rdx, fields[rdx].count(True), fields[rdx])

product = 1
for rdx in range(6):
    fdx = fields[rdx].index(True)
    product *= my_ticket[fdx]
print('PART2: product of destination values on my ticket: {0}'.format(product))




