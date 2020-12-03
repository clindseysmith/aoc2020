import os
import sys
import math
import time
import json
import string
import pprint
import itertools
import traceback
import optparse

parser = optparse.OptionParser()
parser.add_option("-v", action="count", dest="verbose", default=0)
parser.add_option("-u", action="store_true", dest="by_user", default=False, help="Show by user rather than by day")
parser.add_option("-z", action="store_true", dest="include_zero_stars", default=False, help="Include users with 0 stars")
parser.add_option("-a", action="store_true", dest="sort_alpha", default=False, help="Sort users by name rather than stars")
parser.add_option("-r", action="store_true", dest="sort_rev", default=False, help="Display most recent day first")
(opts, args) = parser.parse_args()

in_file_name = args[0]

with open(in_file_name, "r") as f:
    data = json.loads(f.read())
for user in data['members'].keys():
    if data['members'][user]['name'] is None:
        data['members'][user]['name'] = 'Anon{0}'.format(data['members'][user]['id'])


if opts.verbose > 1:
    print(in_file_name)
    pprint.pprint(data)

days = [str(x) for x in range(1, 26)]
if opts.sort_rev:
    days = days[::-1]

def ts_to_asctime(ts):
    if ts is None:
        return ''
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(ts)))

if opts.by_user:
    users = [data['members'][u] for u in data['members'].keys()]
    if opts.sort_alpha:
        users.sort(key=lambda x: x['name'])
    else:
        users.sort(key=lambda x: (x['stars'], -float(x['last_star_ts'])), reverse=True)

    for user in users:
        if user['stars'] == 0 and not opts.include_zero_stars:
            continue
        user_str = '{0} ({1})'.format(user['name'], user['id'])
        print('{0:<30s}  {1} stars'.format(user_str, user['stars']))
        for day in days:
            if day in user['completion_day_level']:
                ts1 = user['completion_day_level'][day].get('1', {'get_star_ts': None})['get_star_ts']
                ts2 = user['completion_day_level'][day].get('2', {'get_star_ts': None})['get_star_ts']
                star1 = ts_to_asctime(ts1)
                star2 = ts_to_asctime(ts2)
                print('    Day {0:>2s}: {1}, {2}'.format(day, star1, star2))
        print('')
else:
    for day in days:
        users = [data['members'][u] for u in data['members'].keys() if day in data['members'][u]['completion_day_level']]
        if len(users) == 0:
            continue
        users.sort(key=lambda x: (x['completion_day_level'][day].get('2', {'get_star_ts': '9'})['get_star_ts'],
                                  x['completion_day_level'][day].get('1', {'get_star_ts': '9'})['get_star_ts']))
        print('Day {0:>2s}'.format(day))
        for user in users:
            user_str = '{0} ({1})'.format(user['name'], user['id'])
            ts1 = user['completion_day_level'][day].get('1', {'get_star_ts': None})['get_star_ts']
            ts2 = user['completion_day_level'][day].get('2', {'get_star_ts': None})['get_star_ts']
            star1 = ts_to_asctime(ts1)
            star2 = ts_to_asctime(ts2)
            print('    {0:<30s}  {1}, {2}'.format(user_str, star1, star2))


