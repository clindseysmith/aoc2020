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

in_file_name = "d21_input.txt"
if opts.example > 0:
    in_file_name = "d21_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

all_ingredients = set()
ingredient_count = {}
possible_allergens = {}
for line in data:
    ingredients, allergens = line.split(' (contains ')
    ingredients = ingredients.split(' ')
    for ingredient in ingredients:
        ingredient_count[ingredient] = ingredient_count.get(ingredient, 0) + 1
    allergens = allergens[:-1].split(', ')
    if opts.verbose > 1:
        print('ingr: {0}, allergens: {1}'.format(','.join(ingredients), ','.join(allergens)))
    set_of_ingredients = set(ingredients)
    all_ingredients.update(set_of_ingredients)
    for allergen in allergens:
        if allergen in possible_allergens:
            possible_allergens[allergen] = possible_allergens[allergen].intersection(set_of_ingredients)
        else:
            possible_allergens[allergen] = set_of_ingredients

if opts.verbose:
    pprint.pprint(possible_allergens)

all_allergens = set()
for a in possible_allergens:
    all_allergens.update(possible_allergens[a])
safe_ingredients = [ingr for ingr in all_ingredients if ingr not in all_allergens]
part1 = sum([ingredient_count[si] for si in safe_ingredients])
print('PART1: Found {0} safe ingredients, listed {1} times'.format(len(safe_ingredients), part1))

allergens = [a for a in possible_allergens]
allergens.sort()
if opts.verbose > 1:
    print(allergens)

allergens_count = [(len(possible_allergens[a]), a) for a in possible_allergens]
allergens_count.sort()
if opts.verbose > 1:
    print(allergens_count)
idx = 0
while allergens_count[-1][0] != 1 and idx < 1000:
    idx += 1
    for c, a in allergens_count:
        if c == 1:
            taken = list(possible_allergens[a])[0]
            for a2 in possible_allergens:
                if a2 == a:
                    continue
                possible_allergens[a2].discard(taken)
        else:
            break
    allergens_count = [(len(possible_allergens[a]), a) for a in possible_allergens]
    allergens_count.sort()
if opts.verbose:
    print(possible_allergens, idx)
part2 = ','.join([possible_allergens[a].pop() for a in allergens])
print('PART2: canonical dangerous ingredient list = {0}'.format(part2))

