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

in_file_name = "d19_input.txt"
if opts.example > 0:
    in_file_name = "d19_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

rules = {}
for line in data:
    if line == '':
        break
    rule_num, rule = line.split(': ')
    if 'a' in rule:
        rules[rule_num] = 'a'
    elif 'b' in rule:
        rules[rule_num] = 'b'
    else:
        rules[rule_num] = [v.split(' ') for v in rule.split(' | ')]

messages = data[len(rules)+1:]

if opts.verbose > 1:
    pprint.pprint(rules)
    pprint.pprint(messages)

def create_valid_messages(rule):
    if rule in ('a', 'b'):
        return [rule]
    messages = []
    for part in rule:
        subs = create_valid_messages(rules[part[0]])
        for pdx in range(1, len(part)):
            next_set = create_valid_messages(rules[part[pdx]])
            new_subs = []
            for s1 in subs:
                for s2 in next_set:
                    new_subs.append(s1+s2)
            subs = new_subs
        messages.extend(subs)
    return messages

valid = create_valid_messages(rules['0'])
valid_set = set(valid)
if opts.verbose:
    print('Discovered {0} total possible valid messages'.format(len(valid)))
    if opts.verbose > 1:
        pprint.pprint(valid)

valid_messages = [m for m in messages if m in valid_set]
print('PART1: there are {0} valid messages'.format(len(valid_messages)))

part2_rules = rules.copy()
part2_rules['8'] = [['42'], ['42', '8']]
part2_rules['11'] = [['42', '31'], ['42', '11', '31']]
if opts.verbose > 1:
    pprint.pprint(part2_rules)

def is_valid(message, rules_subset):
    if len(rules_subset) == 0:
        return len(message) == 0
    if len(rules_subset) > len(message):
        return False
    next_part = rules_subset.pop()
    if next_part in ('a', 'b'):
        if message[0] == next_part:
            return is_valid(message[1:], rules_subset.copy())
        else:
            return False
    else:
        for rule in part2_rules[next_part]:
            if rule in ('a', 'b'):
                rule = [rule]
            if is_valid(message, rules_subset + rule[::-1]):
                return True
        else:
            return False

valid_messages2 = [m for m in messages if is_valid(m, part2_rules['0'][0][::-1])]
print('PART2: there are {0} valid messages'.format(len(valid_messages2)))


