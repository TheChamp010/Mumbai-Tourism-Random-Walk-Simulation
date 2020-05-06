import folium as fl
from data import hotels, places
# 18.89,19.21,19.05
# 72.77,72.95,72.86

plocs = list(map(lambda p: (p['lat'], p['lng']), places))
pnames = list(map(lambda p: p['name'], places))
hlocs = list(map(lambda p: (p['lat'], p['lng']), hotels))
hnames = list(map(lambda p: p['name'], hotels))


def map_path(path, start, file_path):
    mp = fl.Map(location=[19.05, 72.86], zoom_start=16)
    mp.fit_bounds([(18.90, 72.77), (19.16, 72.95)])
    loc_path = list(map(lambda i: plocs[i], path))
    name_path = list(map(lambda i: pnames[i], path))
    fl.PolyLine(locations=[hlocs[start]]+loc_path).add_to(mp)
    fl.Marker(location=hlocs[start], tooltip='1. '+hnames[start], icon=fl.Icon(
        color='green', icon_color='lightgray')).add_to(mp)
    for i, l, n in zip(range(len(path)), loc_path, name_path):
        fl.Marker(location=l, tooltip=str(i+2)+'. '+n, icon=fl.Icon(
            color='red', icon_color='lightgray')).add_to(mp)

    mp.save(file_path)
