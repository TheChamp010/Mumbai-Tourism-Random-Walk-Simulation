import folium as fl
from data import hotels, places
from functools import reduce
from pandas import DataFrame as df
# 18.89,19.21,19.05
# 72.77,72.95,72.86

plocs = list(map(lambda p: (p['lat'], p['lng']), places))
pnames = list(map(lambda p: p['name'], places))
hlocs = list(map(lambda p: (p['lat'], p['lng']), hotels))
hnames = list(map(lambda p: p['name'], hotels))


def map_path(start, path, time, file_path):
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

    # reduce(lambda a, x: a + f'<li> {x[0]}', name_path, '')
    plist = df(zip(name_path, map(lambda x: f'{int(x//1)} hrs {int((x%1)*60)} mins', time)),
               columns=['Location', 'Time spent'], index=range(1, len(path))).to_html(border=0, classes='tbl')

    legend = f'''<div style="
        width: max-content;
        height: max-content;
        top: 50px;
        left: 80px;
        background: rgba(0,0,0,0.8);
        z-index: 999;
        position: fixed;
        color: #ddd;
        padding: 1em;
        font-size: 16pt;
        ">
        <style> .tbl td,th {{padding: 0 .5em}}</style>
        <div>
            <span style="margin-left: .5em"><b>Hotel:</b> {hnames[start]} </span>
            {plist}  
        </div></div>'''
    mp.get_root().html.add_child(fl.Element(legend))

    mp.save(file_path)
