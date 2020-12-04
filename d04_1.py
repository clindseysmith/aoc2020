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

in_file_name = "d04_input.txt"
if opts.example > 0:
    in_file_name = "d04_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

def process(passport, p2=False):
    items = ' '.join(passport).split(' ')
    items = {x.split(':')[0]: x.split(':')[1] for x in items}
    for req in ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'):
        if not req in items:
            return False
    if p2:
        if len(items['byr']) != 4:
            return False
        byr = int(items['byr'])
        if byr < 1920 or byr > 2002:
            return False

        if len(items['iyr']) != 4:
            return False
        iyr = int(items['iyr'])
        if iyr < 2010 or iyr > 2020:
            return False

        if len(items['eyr']) != 4:
            return False
        eyr = int(items['eyr'])
        if eyr < 2020 or eyr > 2030:
            return False

        hgt = items['hgt']
        if hgt[-2:] == 'in':
            hgt = int(hgt[:-2])
            if hgt < 59 or hgt > 76:
                return False
        elif hgt[-2:] == 'cm':
            hgt = int(hgt[:-2])
            if hgt < 150 or hgt > 193:
                return False
        else:
            return False

        hcl = items['hcl']
        if hcl[0] != '#':
            return False
        if len(hcl) != 7:
            return False
        for c in hcl[1:]:
            if not c in '0123456789abcdef':
                return False

        ecl = items['ecl']
        if ecl not in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'):
            return False

        pid = items['pid']
        if len(pid) != 9:
            return False
        for c in pid:
            if not c in '0123456789':
                return False
    return True

valid = 0
valid2 = 0
total = 0
passport = []
for line in data:
    if line == '':
        total += 1
        valid += process(passport)
        valid2 += process(passport, p2=True)
        passport = []
    else:
        passport.append(line)
if len(passport) > 0:
    print('end process')
    total += 1
    valid += process(passport)

print('PART1: {0} of {1} passports are valid'.format(valid, total))

print('PART2: {0} of {1} passports are valid'.format(valid2, total))

if not opts.part2:
    sys.exit(0)

