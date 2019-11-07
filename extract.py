#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

def dump(id, sub):
    sub['style'] = id
    subId = sub['id']
    if subId[0].isdigit() and subId[1].isalpha():
        sub['subcategory'] = "0" + sub['id'] + " " + sub['name']
    else:
        sub['subcategory'] = sub['id'] + " " + sub['name']
    if sub.get('vital_statistics'):
        calc_avg(sub, 'original_extract')
        calc_avg(sub, 'terminal_extract')
        calc_avg(sub, 'alcohol')
        calc_avg(sub, 'bitterness')
        calc_avg(sub, 'color')
        sub['vital'] = "IBU: {}-{}, ABV: {}-{}, SRM: {}-{}, OG: {}-{}, FG: {}-{}".format(sub["bitterness"]["min"], sub["bitterness"]["max"], sub["alcohol"]["min"], sub["alcohol"]["max"], sub["color"]["min"], sub["color"]["max"], sub["original_extract"]["min"], sub["original_extract"]["max"], sub["terminal_extract"]["min"], sub["terminal_extract"]["max"])
        del sub['vital_statistics']
    if sub.get('color_classifications'):
        del sub['color_classifications']
    if sub.get('strength_classifications'):
        del sub['strength_classifications']
    if sub.get('styles'):
        for subsub in sub['styles']:
            dump(id, subsub)
    else:
        print '{"index":{}}'
        print json.dumps(sub)
    
def calc_avg(sub, item):
    sub[item] = sub['vital_statistics'][item]
    sub[item]['avg'] = float(format( (float(sub[item]['max']) + float(sub[item]['min']))/2, '.1f'))


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

