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

input_data = '872495136'
if opts.example == 1:
    input_data = '389125467'
print('Input = {0}'.format(input_data))
data = [int(x) for x in input_data]

def play(cups, n_cups):
    jdx = cups[0] - 1
    if jdx == 0:
        jdx = n_cups
    while jdx in cups[1:4]:
        jdx -= 1
        if jdx == 0:
            jdx = n_cups
    kdx = cups.index(jdx)
    new_cups = cups[4:kdx+1]
    new_cups.extend(cups[1:4])
    new_cups.extend(cups[kdx+1:])
    new_cups.append(cups[0])
    return new_cups

n_moves = 100
n_cups = len(data)
for move in range(n_moves):
    data = play(data, n_cups)
    if opts.verbose > 1:
        print('{0}: {1}'.format(move, ''.join([str(x) for x in data])))

def final_answer(cups):
    kdx = cups.index(1)
    new_cups = cups[kdx+1:]
    new_cups.extend(cups[:kdx])
    return ''.join([str(x) for x in new_cups])

print('PART1: arrangement = {0}'.format(final_answer(data)))

if not opts.part2:
    sys.exit(0)

class Cup(object):
    def __init__(self, val):
        self.val = val
        self.next = None
        self.prev = None

data = [int(x) for x in input_data]
n_cups = 1000000

cups = [None]
for val in range(1, 10):
    c = Cup(val)
    cups.append(c)
for idx in range(9):
    cups[data[idx]].prev = cups[data[(idx-1)%9]]
    cups[data[idx]].next = cups[data[(idx+1)%9]]
last_cup = cups[data[8]]
for val in range(10, n_cups+1):
    c = Cup(val)
    c.prev = last_cup
    c.prev.next = c
    cups.append(c)
    last_cup = c
cups[n_cups].next = cups[data[0]]
cups[n_cups].next.prev = cups[n_cups]

n_moves = 10000000
current = cups[data[0]]
for move in range(n_moves):
    first = current.next
    second = first.next
    third = second.next
    current.next = third.next
    current.next.prev = current
    insert_val = current.val - 1
    if insert_val == 0:
        insert_val = n_cups
    while insert_val in (first.val, second.val, third.val):
        insert_val -= 1
        if insert_val == 0:
            insert_val = n_cups
    insert = cups[insert_val]
    third.next = insert.next
    third.next.prev = third
    insert.next = first
    first.prev = insert
    current = current.next
    if opts.verbose and (move+1) % 10000 == 0:
        print('Progress {0:.1f}%'.format(100*(move+1)/n_moves), end='\r', flush=True)
print('')

part2 = cups[1].next.val * cups[1].next.next.val
print('PART2: next cups after cup 1: {0} and {1}, product = {2}'.format(cups[1].next.val, cups[1].next.next.val, part2))

