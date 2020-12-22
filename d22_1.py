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

in_file_name = "d22_input.txt"
if opts.example > 0:
    in_file_name = "d22_examples%s.txt" % opts.example

with open(in_file_name, "r") as f:
    data = [x.strip() for x in f.readlines()]

print(in_file_name, len(data))

def get_decks(input_data):
    split = input_data.index('')
    deck1 = [int(x) for x in data[1:split]]
    deck2 = [int(x) for x in data[split+2:]]
    return deck1, deck2, len(deck1) + len(deck2)

player1, player2, n_cards = get_decks(data)
if opts.verbose:
    print('Player1 deck: {0}'.format(player1))
    print('Player2 deck: {0}'.format(player2))

if opts.example == 2:
    print('Not playing non-recursive with Example2')
else:
    while len(player1) > 0 and len(player2) > 0:
        card1, card2 = player1.pop(0), player2.pop(0)
        if card1 > card2:
            player1.extend([card1, card2])
        else:
            player2.extend([card2, card1])

    if len(player1) > 0:
        winner = player1
        wp = '1'
    else:
        winner = player2
        wp = '2'

    part1 = sum([(n_cards-idx)*c for idx, c in enumerate(winner)])
    print("PART1: Player{0} wins with score {1}".format(wp, part1))

player1, player2, n_cards = get_decks(data)

def strstate(d1, d2):
    return '{0}:{1}'.format(''.join([str(x) for x in d1]), ''.join([str(x) for x in d2]))

game_id = 0
def recursive_combat(deck1, deck2):
    global game_id
    game_id += 1
    this_gid = game_id
    if opts.verbose > 1:
        print('* Starting game {0} *'.format(this_gid))
    states_seen = set()
    game_round = 0
    while len(deck1) > 0 and len(deck2) > 0:
        game_round += 1
        state = strstate(deck1, deck2)
        if state in states_seen:
            if opts.verbose > 1:
                print('*** Player1 Wins by Infinite Recursion in round {0} ***'.format(game_round))
            return deck1, [], this_gid
        states_seen.add(state)
        card1, card2 = deck1.pop(0), deck2.pop(0)
        if len(deck1) >= card1 and len(deck2) >= card2:
            subdeck1, subdeck2, sub_gid = recursive_combat(deck1[:card1], deck2[:card2])
            if len(subdeck1) > 1:
                deck1.extend([card1, card2])
                if opts.verbose > 1:
                    print('Player1 wins subgame {0} and round {1} of game {2}'.format(sub_gid, game_round, this_gid))
                    print('* Back to game {0}'.format(this_gid))
            else:
                deck2.extend([card2, card1])
                if opts.verbose > 1:
                    print('Player2 wins subgame {0} and round {1} of game {2}'.format(sub_gid, game_round, this_gid))
                    print('* Back to game {0}'.format(this_gid))
        elif card1 > card2:
            deck1.extend([card1, card2])
            if opts.verbose > 1:
                print('Player1 wins round {0} of game {1} [{2}, {3}]'.format(game_round, this_gid, card1, card2))
        else:
            deck2.extend([card2, card1])
            if opts.verbose > 1:
                print('Player2 wins round {0} of game {1} [{2}, {3}]'.format(game_round, this_gid, card1, card2))
    return deck1, deck2, this_gid

player1, player2, gid = recursive_combat(player1, player2)

if len(player1) > 0:
    winner = player1
    wp = '1'
else:
    winner = player2
    wp = '2'

part2 = sum([(n_cards-idx)*c for idx, c in enumerate(winner)])
print("PART2: Player{0} wins game {1} with score {2}".format(wp, gid, part2))

