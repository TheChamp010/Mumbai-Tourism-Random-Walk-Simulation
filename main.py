import argparse as ap
import sys

from colored import attr, bg, fg, stylize
from pandas import DataFrame as df

from traveller import Traveller, distance
from data import hotels, places
from mapplot import map_path
from random import randint

nhotels = len(hotels)
nplaces = len(places)

hotel_prob_table = [100/nhotels for i in range(nhotels)]
places_prob_table = [[100/(nplaces-1)if i != j else 0 for j in range(nplaces)]
                     for i in range(nplaces)]
hotels_prob_table = [[100/(nplaces) for j in range(nplaces)]
                     for i in range(nhotels)]

arg = ap.ArgumentParser()
arg.add_argument('id')
mid = arg.parse_args().id
tl = randint(12, 16)  # int(input('total travel time: '))
hl = 2.5
inc = .1
trials = 1000  # int(input('number of trials: '))

start = None
path = []
tpath = []
time = []

for i in range(trials):
    Trv = Traveller()
    hotel_prob_table = Trv.choose_hotel(hotels, hotel_prob_table)
    hotels_prob_table = Trv.travel_h(hotels, places, hotels_prob_table)

    t = 0
    ttt = 0
    while t < tl:
        prev = places[Trv.get_location()]
        places_prob_table = Trv.travel(places, places_prob_table)
        curr = places[Trv.get_location()]
        tt = distance(prev, curr)/16
        t += tt
        ttt += tt
        ts = 0
        hp = Trv.calc_hp(curr, ts)
        while hp > hl and t < tl:
            ts += inc
            t += inc
            hp = Trv.calc_hp(curr, ts)
        else:
            Trv.add_timestamp(ts)
            Trv.add_traveltime(tt)

    path = Trv.get_path()
    start = Trv.get_start()
    time = Trv.get_time()
    tpath = list(zip(
        Trv.get_path(),
        map(lambda x: round(x, 2), Trv.get_time())
    ))

    if i == trials-1:
        print(stylize(hotels[Trv.get_start()]['name'],
                      attr(1)+fg('#ff9933')+bg('black')))
        print(stylize(df(zip(
            map(lambda x: places[x]['name'], Trv.get_path()),
            map(lambda x: round(x, 2), Trv.get_time()),
            map(lambda x: round(x, 2), Trv.get_travel())
        ), index=range(1, len(tpath)+1),
            columns=['Location', 'Time Spent', 'Travel Time']),
            attr(21)+bg('black')))
        print(stylize(f'{round(ttt,2)} hrs of Travel Time',
                      fg('#dd7a09')+attr(21)+bg('black')))

print('─'*100)
map_path(start, path, time, f'map/map_{mid}.html')
