import os
import sys
import math
import time
import string
import pprint
import itertools
import traceback
import optparse
import copy

parser = optparse.OptionParser()
parser.add_option("-v", action="count", dest="verbose", default=0)
parser.add_option("-e", action="count", dest="example", default=0)
parser.add_option("-2", action="store_true", dest="part2", default=False)
parser.add_option("--step", action="store_true", dest="step", default=False)
parser.add_option("--display", action="store_true", dest="display", default=False)
(opts, args) = parser.parse_args()

in_file_name = "d08_input.txt"
if opts.example > 0:
    in_file_name = "d08_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    instructions = {idx: x.strip().split(' ') for idx, x in enumerate(f.readlines())}

print(in_file_name, len(instructions))

def run_computer(l_instructions):
    def do_instruction(cmd, val, idx, acc):
        if cmd == 'nop':
            return idx+1, acc
        elif cmd == 'acc':
            return idx+1, acc + int(val)
        elif cmd == 'jmp':
            return idx + int(val), acc
        else:
            raise Exception('WARNING - unknown instruction at idx {0}: {1}'.format(idx, cmd))

    visited = set()
    iptr = 0
    accumulator = 0
    while True:
        if iptr in visited:
            break
        if iptr not in l_instructions:
            return 'halted', accumulator, iptr
        visited.add(iptr)
        cmd, val = l_instructions[iptr]
        iptr, accumulator = do_instruction(cmd, val, iptr, accumulator)
    return 'revisited', accumulator, iptr

status, acc, iptr = run_computer(instructions) 
print('PART1: accumulator = {0}, right before instruction {1} is run a second time'.format(acc, iptr))

for cdx in range(len(instructions)):
    cmd, val = instructions[cdx]
    if cmd == 'acc':
        continue
    instr_copy = copy.deepcopy(instructions)
    if cmd == 'nop':
        instr_copy[cdx] = ('jmp', val)
    elif cmd == 'jmp':
        instr_copy[cdx] = ('nop', val)
    else:
        raise Exception('WARNING - unk instruction at cdx {0}: {1}'.format(cdx, cmd))
    status, acc, iptr = run_computer(instr_copy)
    if status == 'halted':
        print('PART2: accumulator = {0} when program terminates after switching line {1}'.format(acc, cdx))
        break


