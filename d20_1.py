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

in_file_name = "d20_input.txt"
if opts.example > 0:
    in_file_name = "d20_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

tiles = {}
for line in data:
    if line.startswith('Tile'):
        tile_num = int(line[5:9])
        tile = []
    elif len(line) == 10:
        tile.append(line)
    else:
        tiles[tile_num] = {'tile': tile}
        tile = []
num_tiles = len(tiles)
side_len = int(math.sqrt(num_tiles))
assert(side_len*side_len == num_tiles)
print('Found {0} tiles input, images is {1}x{1} tiles'.format(num_tiles, side_len))

def dothash_to_int(dh):
    b = dh.replace('.','0').replace('#','1')
    return int(b, 2)

def invert(num):
    b = '{0:10b}'.format(num).replace(' ', '0')
    binv = b[::-1]
    return int(binv, 2)

all_sides = {}
def set_sides(tn):
    tile = tiles[tn]['tile']
    tiles[tn]['top'] = dothash_to_int(tile[0])
    tiles[tn]['right'] = dothash_to_int(''.join([l[-1] for l in tile]))
    tiles[tn]['bottom'] = dothash_to_int(tile[-1])
    tiles[tn]['left'] = dothash_to_int(''.join([l[0] for l in tile]))
    for side in ('top', 'right', 'bottom', 'left'):
        side = tiles[tn][side]
        all_sides.setdefault(side, []).append(tile_num)
        iside = invert(side)
        all_sides.setdefault(iside, []).append(tile_num)

for tile_num in tiles:
    set_sides(tile_num)

idx = 0
lone_sides = {}
lone_side_numbers = []
for side in all_sides:
    if len(all_sides[side]) == 1:
        idx += 1
        if opts.verbose > 2:
            print(idx, side, all_sides[side])
        tile_num = all_sides[side][0]
        lone_sides.setdefault(tile_num, []).append(side)
        lone_side_numbers.append(side)
lone_side_numbers.sort()
if opts.verbose > 1:
    print('({0}), {1}'.format(len(lone_side_numbers), lone_side_numbers))
slone_side_numbers = set(lone_side_numbers)

part1 = 1
corners = []
edges = []
for tn in lone_sides:
    if opts.verbose > 0:
        print(tn, len(lone_sides[tn]), lone_sides[tn])
    if len(lone_sides[tn]) == 4:
        part1 *= tn
        corners.append(tn)
    elif len(lone_sides[tn]) == 2:
        edges.append(tn)
print('PART1: product of four corner tile numbers is {0}'.format(part1))

scorners = set(corners)
sedges = set(edges)
middles = [tn for tn in tiles if tn not in scorners and tn not in sedges]
corners.sort()
edges.sort()
middles.sort()
if opts.verbose > 0:
    print('corners: ({0}) {1}'.format(len(corners), corners))
    print('edges: ({0}) {1}'.format(len(edges), edges))
    print('middles: ({0}) {1}'.format(len(middles), middles))

top_left = corners[0]
tile_array = [[] for idx in range(side_len)]
tile_array[0].append(top_left)

def print_tile(tn):
    tile = tiles[tn]['tile']
    for row in tile:
        print(row)

def flip_tile_lr(tn):
    tiles[tn]['left'], tiles[tn]['right'] = tiles[tn]['right'], tiles[tn]['left']
    tiles[tn]['top'] = invert(tiles[tn]['top'])
    tiles[tn]['bottom'] = invert(tiles[tn]['bottom'])
    old_subimage = tiles[tn]['tile']
    tiles[tn]['tile'] = [row[::-1] for row in tiles[tn]['tile']]
def flip_tile_tb(tn):
    tiles[tn]['top'], tiles[tn]['bottom'] = tiles[tn]['bottom'], tiles[tn]['top']
    tiles[tn]['left'] = invert(tiles[tn]['left'])
    tiles[tn]['right'] = invert(tiles[tn]['right'])
    tiles[tn]['tile'] = tiles[tn]['tile'][::-1]
def rotate_tile(tn):
    old_top = tiles[tn]['top']
    tiles[tn]['top'] = tiles[tn]['right']
    tiles[tn]['right'] = invert(tiles[tn]['bottom'])
    tiles[tn]['bottom'] = tiles[tn]['left']
    tiles[tn]['left'] = invert(old_top)
    old_tile = tiles[tn]['tile']
    new_tile = []
    nrows = len(old_tile)
    for row in range(nrows):
        new_tile.append(''.join([s[nrows-row-1] for s in old_tile]))
    tiles[tn]['tile'] = new_tile

def get_sides(tn):
    return {'top': tiles[tn]['top'],'right': tiles[tn]['right'],'bottom': tiles[tn]['bottom'],'left': tiles[tn]['left']}
def get_isides(tn):
    return {'top': invert(tiles[tn]['top']),'right': invert(tiles[tn]['right']),'bottom': invert(tiles[tn]['bottom']),'left': invert(tiles[tn]['left'])}

flip_tile_lr(top_left)
if opts.verbose > 0:
    print('top_left corner: {0}'.format(top_left))
    print(get_sides(top_left))
# rotate this tile until it's lone sides are top and left
while tiles[top_left]['top'] not in slone_side_numbers or tiles[top_left]['left'] not in slone_side_numbers:
    rotate_tile(top_left)
if opts.verbose > 0:
    print(get_sides(top_left), tiles[top_left]['top'] in slone_side_numbers, tiles[top_left]['left'] in slone_side_numbers)
    print(all_sides[tiles[top_left]['right']])
this_tile = top_left
for i in range(1, side_len):
    right_side = tiles[this_tile]['right']
    next_tile = [x for x in all_sides[right_side] if x != this_tile][0]
    for rdx in range(4):
        if tiles[next_tile]['left'] == right_side:
            break
        flip_tile_tb(next_tile)
        if tiles[next_tile]['left'] == right_side:
            break
        flip_tile_tb(next_tile)
        rotate_tile(next_tile)
    if tiles[next_tile]['left'] == right_side:
        tile_array[0].append(next_tile)
        this_tile = next_tile
    else:
        print(this_tile, get_sides(this_tile), right_side)
        print(next_tile, get_sides(next_tile), get_isides(next_tile))
        raise Exception('We have the wrong tile, col = {0}'.format(i))
if opts.verbose > 0:
    print(tile_array)
for row in range(1, side_len):
    for col in range(side_len):
        tile_above = tile_array[row-1][col]
        bottom = tiles[tile_above]['bottom']
        next_tile = [x for x in all_sides[bottom] if x != tile_above][0]
        for rdx in range(4):
            if tiles[next_tile]['top'] == bottom:
                break
            flip_tile_lr(next_tile)
            if tiles[next_tile]['top'] == bottom:
                break
            flip_tile_lr(next_tile)
            rotate_tile(next_tile)
        if tiles[next_tile]['top'] == bottom:
            tile_array[row].append(next_tile)
        else:
            print(tile_above, get_sides(tile_above), bottom)
            print(next_tile, get_sides(next_tile), get_isides(next_tile))
            raise Exception('We have the wrong tile row,col = {0},{1}'.format(row, col))
    if opts.verbose > 1:
        print(tile_array)

def print_image(image):
    for row in image:
        print(row)
def flip_image(image):
    return image[::-1]
def rotate_image(image):
    new_image = []
    nrows = len(image)
    for row in range(nrows):
        new_image.append(''.join([l[nrows-row-1] for l in image]))
    return new_image

image = []
for row in range(side_len):
    for sub_row in range(1,9):
        str_row = ''
        for col in range(side_len):
            tile = tile_array[row][col]
            str_row += tiles[tile]['tile'][sub_row][1:9]
        image.append(str_row)

if opts.verbose > 2:
    print_image(image)

seamonster = [
  '                  # ',
  '#    ##    ##    ###',
  ' #  #  #  #  #  #   '
]
seamonster_hashes = []
for rdx, row in enumerate(seamonster):
    for cdx, col in enumerate(row):
        if col == '#':
            seamonster_hashes.append((rdx, cdx))
if opts.verbose > 1:
    print(seamonster_hashes)
def count_seamonsters(image):
    monster_count = 0
    for rdx in range(len(image)-3):
        for cdx in range(len(image)-19):
            for rs, cs in seamonster_hashes:
                if image[rdx+rs][cdx+cs] != '#':
                    break
            else:
                monster_count += 1
    return monster_count

counts = []
for idx in range(4):
    counts.append((count_seamonsters(image), image))
    image = flip_image(image)
    counts.append((count_seamonsters(image), image))
    image = flip_image(image)
    image = rotate_image(image)
highest_count, true_image = max(counts)
if opts.verbose > 0:
    print([c[0] for c in counts], highest_count)

total_hashes = sum([row.count('#') for row in image])
non_seamonster_hashes = total_hashes - highest_count*len(seamonster_hashes)
print('PART2: Saw {0} seamonsters, surrounted by {1} hashes'.format(highest_count, non_seamonster_hashes))

if opts.display:
    def highlight_seamonsters(image):
        new_image = [list(row) for row in image]
        for rdx in range(len(image)-3):
            for cdx in range(len(image)-19):
                for rs, cs in seamonster_hashes:
                    if image[rdx+rs][cdx+cs] != '#':
                        break
                else:
                    for rs, cs in seamonster_hashes:
                        new_image[rdx+rs][cdx+cs] = 'O'
        return [''.join(row) for row in new_image]

    seamonster_image = highlight_seamonsters(true_image)
    print_image(seamonster_image)

