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

in_file_name = "d18_input.txt"
if opts.example > 0:
    in_file_name = "d18_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

def l_r_eval(sub):
    if opts.verbose > 1:
        print('    l_r_eval({0})'.format(sub))
    parts = sub.split(' ')
    if len(parts) == 3:
        return eval(sub)
    else:
        subsub = eval(' '.join(parts[:3]))
        nextsub = '{0} {1}'.format(subsub, ' '.join(parts[3:]))
        return l_r_eval(nextsub)

def a_m_eval(sub):
    if opts.verbose > 1:
        print('    a_m_eval({0})'.format(sub))
    parts = sub.split(' ')
    try:
        plus_index = parts.index('+')
        subsub = eval(' '.join(parts[plus_index-1:plus_index+2]))
        nextparts = parts[:plus_index-1]
        nextparts.append(str(subsub))
        nextparts.extend(parts[plus_index+2:])
        nextsub = ' '.join(nextparts)
        return a_m_eval(nextsub)
    except ValueError:
        return eval(sub)

        
def process(line, part2=False):
    if opts.verbose > 1:
        print('  process({0}, {1})'.format(line, part2))
    first_right_paren = line.find(')')
    if first_right_paren == -1:
        if part2:
            return a_m_eval(line)
        else:
            return l_r_eval(line)
    left_paren = line.rfind('(', 0, first_right_paren)
    sub = line[left_paren+1:first_right_paren]
    if part2:
        subval = a_m_eval(sub)
    else:
        subval = l_r_eval(sub)
    new_line = '{0}{1}{2}'.format(line[:left_paren], subval, line[first_right_paren+1:])
    return process(new_line, part2)

total = 0
for line in data:
    sub = process(line)
    if opts.verbose:
        print('{0} ==> {1}'.format(line, sub))
    total += sub
print('PART1: sum of all {0} lines using l-r eval is {1}'.format(len(data), total))    

total = 0
for line in data:
    if opts.verbose > 1:
        print('='*30)
    sub = process(line, True)
    if opts.verbose:
        print('{0} ==> {1}'.format(line, sub))
    total += sub
print('PART2: sum of all {0} lines using a-m eval is {1}'.format(len(data), total))    

