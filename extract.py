#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

# If you want the gravity in Specific Gravity instead of Plato degree
USE_SG = False
BJCP_GUIDE_JSON = 'bjcp-2015.json'


def dump(sid, sub):
    sub['style'] = sid
    sub_id = sub['id']
    if sub_id[0].isdigit() and sub_id[1].isalpha():
        sub['subcategory'] = "0" + sub['id'] + " " + sub['name']
    else:
        sub['subcategory'] = sub['id'] + " " + sub['name']
    if sub.get('vital_statistics'):
        calc_avg(sub, 'original_extract', 'og')
        calc_avg(sub, 'terminal_extract', 'fg')
        if USE_SG:
            convert_to_sg(sub, 'og')
            convert_to_sg(sub, 'fg')
        calc_avg(sub, 'alcohol', 'abv')
        calc_avg(sub, 'bitterness', 'ibu')
        calc_avg(sub, 'color', 'srm')
        sub['vital'] = "SRM: {:,}-{:,}, IBU: {:,}-{:,}, OG: {:,}-{:,}, FG: {:,}-{:,}, ABV: {:,}-{:,}".format(
            sub["srm"]["min"], sub["srm"]["max"], sub["ibu"]["min"], sub["ibu"]["max"], sub["og"]["min"],
            sub["og"]["max"], sub["fg"]["min"], sub["fg"]["max"], sub["abv"]["min"], sub["abv"]["max"])
        del sub['vital_statistics']
    if sub.get('color_classifications'):
        del sub['color_classifications']
    if sub.get('strength_classifications'):
        del sub['strength_classifications']
    if sub.get('styles'):
        for sub_sub in sub['styles']:
            dump(sid, sub_sub)
    else:
        print('{"index":{}}')
        print(json.dumps(sub))


def calc_avg(sub, item, rename):
    sub[item] = sub['vital_statistics'][item]
    sub[item]['avg'] = float(format((float(sub[item]['max']) + float(sub[item]['min'])) / 2, '.1f'))
    sub[rename] = sub[item]
    del sub[item]


def convert_to_sg(sub, item):
    sub[item] = {'min': plato_to_sg(sub[item]['min']), 'max': plato_to_sg(sub[item]['max']),
                 'avg': plato_to_sg(sub[item]['avg'])}


def plato_to_sg(plato):
    return int(round(1000 * (1 + (plato / (258.6 - ((plato / 258.2) * 227.1))))))


def parse(file):
    with open(file) as json_file:
        data = json.load(json_file)
        for style in data:
            try:
                sid = format(int(style['id']), '02d')
            except ValueError:
                sid = style['id']
            # print(id + ' Name: ' + style['name'])
            for sub in style['subcategories']:
                dump(sid, sub)


parse(BJCP_GUIDE_JSON)
