import pandas as pd
from math import sqrt, fsum

hotels_data: pd.DataFrame = pd.read_csv('./data/hotels_data.csv')
places_data: pd.DataFrame = pd.read_csv('./data/places_data.csv')


def avg(nl):
    return fsum(nl)/len(nl)


def std(nl):
    mu = avg(nl)
    n = len(nl)
    return sqrt(fsum([(x-mu)**2 for x in nl])/n)


def normalise(v, mu, std):
    return (v-mu)/std


def map_range(vr, rs, re):
    vs, ve = min(vr)-1, max(vr)+1
    return [rs+(v-vs)*(re-rs)/(ve-vs)for v in vr]


def normalise_range(rn, rs, re):
    return map_range([normalise(x, avg(rn), std(rn)) for x in rn], rs, re)


hr = hotels_data['rating']
htr = hotels_data['total_rating']
hp = hotels_data['price']

n_hotel_rating = normalise_range(hr, 0, 100)
n_hotel_total_rating = normalise_range(htr, 0, 100)
n_hotel_price = normalise_range(hp, 0, 100)

pr = places_data['rating']
ptr = places_data['total_rating']

n_places_rating = normalise_range(pr, 0, 100)
n_places_total_rating = normalise_range(ptr, 0, 100)

hotels_data['n_rating'] = n_hotel_rating
hotels_data['n_total_rating'] = n_hotel_total_rating
places_data['n_rating'] = n_places_rating
places_data['n_total_rating'] = n_places_total_rating
hotels_data['n_price'] = n_hotel_price

# print(list(hotels_data['n_rating']), list(hotels_data['n_total_rating']),
#       list(places_data['n_rating']), list(places_data['n_total_rating']), sep='\n')

hotels = list(hotels_data.to_dict(orient='index').values())
places = list(places_data.to_dict(orient='index').values())
