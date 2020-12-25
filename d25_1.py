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

in_file_name = "d25_input.txt"
if opts.example > 0:
    in_file_name = "d25_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

subject_number = 7
magic_date = 20201227
card_pub = int(data[0])
door_pub = int(data[1])
print('Card public = {0}\nDoor public = {1}'.format(card_pub, door_pub))

loop_size = 0
encryption_key = None
new_val, card_enc_key, door_enc_key = 1, 1, 1
while encryption_key is None:
    loop_size += 1
    new_val = new_val * subject_number % magic_date
    card_enc_key = card_enc_key * door_pub % magic_date
    door_enc_key = door_enc_key * card_pub % magic_date
    if new_val == card_pub:
        if opts.verbose:
            print('')
        print('Found card loop size = {0}'.format(loop_size))
        encryption_key = card_enc_key
    if new_val == door_pub:
        if opts.verbose:
            print('')
        print('Found door loop size = {0}'.format(loop_size))
        encryption_key = door_enc_key
    if opts.verbose and loop_size % 1000 == 0:
        print('Checking loop_size {0} = {1}'.format(loop_size, new_val), end='\r', flush=True)

print('PART1: Encyption key = {0}'.format(encryption_key))

