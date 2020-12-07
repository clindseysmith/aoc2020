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

in_file_name = "d07_input.txt"
if opts.example > 0:
    in_file_name = "d07_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

rules = {}
for line in data:
    outer, inner = line.split(' contain ')
    outbag = outer.split(' bags')[0]
    rules[outbag] = {}
    if inner == 'no other bags.':
        continue
    for inbag in inner.split(', '):
        count, rest = inbag.split(' ', maxsplit=1)
        name = rest.split(' bag')[0]
        rules[outbag][name] = int(count)

if opts.verbose > 0:
    pprint.pprint(rules)

def fill_bag(outbag, filled):
    if outbag not in filled:
        bags = {outbag: 1}
        for inbag in rules[outbag]:
            count = rules[outbag][inbag]
            inbags = fill_bag(inbag, filled)
            for b in inbags:
                bags[b] = bags.get(b, 0) + count*(inbags[b])
        filled[outbag] = bags
    return filled[outbag]

filled = {}
for outbag in rules:
    filled[outbag] = fill_bag(outbag, filled)

can_contain_shiny_gold = [c for c in filled if 'shiny gold' in filled[c] and c != 'shiny gold']
if opts.verbose > 0:
    print(can_contain_shiny_gold)
print('PART1: {0} outer bags can contain at least one shiny gold bag'.format(len(can_contain_shiny_gold)))

if opts.verbose > 0:
    pprint.pprint(filled['shiny gold'])
total = sum([filled['shiny gold'][c] for c in filled['shiny gold']]) - 1 # don't count the outer shiny gold
print('PART2: a shiny gold bag must contain {0} other bags'.format(total))

