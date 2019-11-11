#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

def dump(id, sub):
    sub['style'] = id
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
        sub['vital'] = "IBU: {}-{}, ABV: {}-{}, SRM: {}-{}, OG: {}-{}, FG: {}-{}".format(sub["ibu"]["min"], sub["ibu"]["max"], sub["abv"]["min"], sub["abv"]["max"], sub["srm"]["min"], sub["srm"]["max"], sub["og"]["min"], sub["og"]["max"], sub["fg"]["min"], sub["fg"]["max"])
        del sub['vital_statistics']
    if sub.get('color_classifications'):
        del sub['color_classifications']
    if sub.get('strength_classifications'):
        del sub['strength_classifications']
    if sub.get('styles'):
        for subsub in sub['styles']:
            dump(id, subsub)
    else:
        print('{"index":{}}')
        print(json.dumps(sub))

def calc_avg(sub, item, rename):
    sub[item] = sub['vital_statistics'][item]
    sub[item]['avg'] = float(format( (float(sub[item]['max']) + float(sub[item]['min']))/2, '.1f'))
    sub[rename] = sub[item]
    del sub[item]

def parse():
    with open('bjcp-2015.json') as json_file:
        data = json.load(json_file)
        for style in data:
            try:
                id = format(int(style['id']), '02d')
            except ValueError:
                id = style['id']
            #print(id + ' Name: ' + style['name'])
            for sub in style['subcategories']:
                dump(id, sub)


parse()

