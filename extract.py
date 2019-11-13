#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

# If you want the gravity in Specific Gravity instead of Plato degree
USE_SG = False
BJCP_GUIDE_JSON = 'bjcp-2015.json'


def dump(sid, style, sub):
    sub['style_id'] = sid
    sub['style'] = style
    try:
        sub['style_num'] = int(sid)
    except ValueError:
        sub['style_num'] = 99
    sub_id = sub['id']
    if sub_id[0].isdigit() and sub_id[1].isalpha():
        sub['subcategory'] = "0" + sub['id'] + " " + sub['name']
    else:
        sub['subcategory'] = sub['id'] + " " + sub['name']
    if sub.get('vital_statistics'):
        calc_avg(sub, 'original_extract', 'og')
        calc_avg(sub, 'terminal_extract', 'fg')
        calc_avg(sub, 'alcohol', 'abv')
        calc_avg(sub, 'bitterness', 'ibu')
        calc_avg(sub, 'color', 'srm')
        sub['bugu'] = {'min': bu_gu_ratio(float(sub['ibu']['min']), float(sub['og']['min'])),
                       'avg': bu_gu_ratio(float(sub['ibu']['avg']), float(sub['og']['avg'])),
                       'max': bu_gu_ratio(float(sub['ibu']['max']), float(sub['og']['max']))}
        if USE_SG:
            convert_to_sg(sub, 'og')
            convert_to_sg(sub, 'fg')
        sub[
            'vital'] = "SRM: {:,}-{:,}, IBU: {:,}-{:,}, OG: {:,}-{:,}, FG: {:,}-{:,}, ABV: {:,}-{:,}, BU:GU: {:,}-{:,}".format(
            sub["srm"]["min"], sub["srm"]["max"], sub["ibu"]["min"], sub["ibu"]["max"], sub["og"]["min"],
            sub["og"]["max"], sub["fg"]["min"], sub["fg"]["max"], sub["abv"]["min"], sub["abv"]["max"],
            sub["bugu"]["min"], sub["bugu"]["max"])
        del sub['vital_statistics']
    if sub.get('color_classifications'):
        del sub['color_classifications']
    if sub.get('strength_classifications'):
        del sub['strength_classifications']
    if sub.get('styles'):
        for sub_sub in sub['styles']:
            dump(sid, style, sub_sub)
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


def plato_to_gu(plato):
    return int(round(1000 * (plato / (258.6 - ((plato / 258.2) * 227.1)))))


def bu_gu_ratio(ibu, plato):
    return float(format(ibu / plato_to_gu(plato), '.2f'))


def parse(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        for style in data:
            # print(id + ' Name: ' + style['name'])
            for sub in style['subcategories']:
                dump(style['id'], style['name'], sub)


parse(BJCP_GUIDE_JSON)
