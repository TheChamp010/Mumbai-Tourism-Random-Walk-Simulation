from random import random
from math import radians, cos, sin, asin, sqrt, log1p, prod


def distance(l1, l2):
    lt1, ln1 = radians(l1['lat']), radians(l1['lng'])
    lt2, ln2 = radians(l2['lat']), radians(l2['lng'])
    return 12742*asin(sqrt(sin((lt2-lt1)/2)**2+cos(lt1)*cos(lt2)*sin((ln2-ln1)/2)**2))


def map_to_range(v, vs, ve, rs, re):
    return rs+(v-vs)*(re-rs)/(ve-vs)


def prob_index(val, prob_list):
    cp = 0
    for i, p in enumerate(prob_list):
        cp += p
        if val < cp:
            return i


def calc_hp(dir=[1], inv=[1]):
    # * map_to_range(random(), 0, 1, 0.5, 1.5)
    return round(log1p(prod(dir)*prod(map(lambda x: 1/x, inv))), 2)


class Traveller(object):
    id = 0

    def __init__(self):
        self.path = []
        self.time = []
        self.traveltime = []
        self.id = Traveller.id
        Traveller.id += 1

    def get_location(self): return self.current
    def get_start(self): return self.start
    def get_path(self): return self.path
    def get_time(self): return self.time
    def get_travel(self): return self.traveltime

    def add_timestamp(self, time): self.time.append(time)
    def add_traveltime(self, time): self.traveltime.append(time)

    def next_dest(self, prob_table):
        p = 100*random()
        pl = prob_table[self.current]
        return prob_index(p, pl)

    def calc_hp_p(self, next_dest, places):
        f, t = self.current, next_dest
        d = distance(places[f], places[t])
        r, tr = places[t]['n_rating'], places[t]['n_total_rating']
        v = next_dest in self.path
        hp = calc_hp([r, tr], [35, d])
        if v:
            return -hp*(round(random(), 1)+1)
        else:
            return hp

    def calc_hp_h(self, next_dest, hotels, places):
        f, t = self.current, next_dest
        d = distance(hotels[f], places[t])
        r, tr = places[t]['n_rating'], places[t]['n_total_rating']
        v = next_dest in self.path
        hp = calc_hp([r, tr], [35, d])
        if v:
            return -hp * (round(random(), 1)+1)
        else:
            return hp

    def travel(self, places, prob_table):
        nd = self.next_dest(prob_table)
        hp = self.calc_hp_p(nd, places)

        pt = prob_table.copy()
        pl = pt[self.current]
        d = hp
        dv = d/(len(pl)-2)

        for i in range(len(pl)):
            if i == nd:
                pl[i] += d
            elif pl[i] != 0:
                pl[i] -= dv

        self.current = nd
        self.path.append(nd)
        return pt

    def travel_h(self, hotels, places, prob_table):
        nd = self.next_dest(prob_table)
        hp = self.calc_hp_h(nd, hotels, places)

        pt = prob_table.copy()
        pl = pt[self.current]
        d = hp
        dv = d/(len(pl)-1)

        for i in range(len(pl)):
            if i == nd:
                pl[i] += d
            elif pl[i] != 0:
                pl[i] -= dv

        self.current = nd
        self.path.append(nd)
        return pt

    def choose_hotel(self, hotels, prob_table):
        h = prob_index(100*random(), prob_table)
        ht = hotels[h]
        pl = prob_table.copy()

        r, tr, p = ht['n_rating'], ht['n_total_rating'], ht['n_price']
        hp = calc_hp([r, tr], [p])

        d = hp
        dv = d/(len(pl)-1)
        for i in range(len(pl)):
            if i == h:
                pl[i] += d
            else:
                pl[i] -= dv
        self.start = h
        self.current = h
        return pl

    def calc_hp(self, place, time_spent):
        return calc_hp([place['n_rating'], place['n_total_rating'], 0.1**time_spent])
