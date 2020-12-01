import os
import sys
import itertools

with open('d01_input.txt', 'r') as f:
    data = f.readlines()

data = [int(l.strip()) for l in data]

if False:
    #Orig
    for idx1, num1 in enumerate(data[:-1]):
        if num1 > 2020:
            continue
        for idx2 in range(idx1+1, len(data)):
            num2 = data[idx2]
            if num1 + num2 == 2020:
                print('PART1:', idx1, num1, idx2, num2, num1+num2, num1*num2)
            if num1 + num2 > 2020:
                continue
            for idx3 in range(idx2+1, len(data)):
                num3 = data[idx3]
                if num1 + num2 + num3 == 2020:
                    print('PART2:', idx1, num1, idx2, num2, idx3, num3, num1+num2+num3, num1*num2*num3)

if False:
    sdata = set(data)
    for num in data:
        onum = 2020-num
        if onum in sdata:
            print('PART1: {0}, {1}, {2}'.format(num, onum, num*onum))
    for idx1, num1 in enumerate(data[:-2]):
        for idx2 in range(idx1+1, len(data)):
            num2 = data[idx2]
            num3 = 2020 - num1 - num2
            if num3 in sdata:
                print('PART2: {0}, {1}, {2}, {3}'.format(num1, num2, num3, num1*num2*num3))

if True:
    for num1, num2 in itertools.combinations(data, 2):
        if num1 + num2 == 2020:
            print('PART1: {0}, {1}, {2}'.format(num1, num2, num1*num2))
            break
    for num1, num2, num3 in itertools.combinations(data, 3):
        if num1 + num2 + num3 == 2020:
            print('PART2: {0}, {1}, {2}, {3}'.format(num1, num2, num3, num1*num2*num3))
            break

