#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import json

GEN_DATA = False
# If you want the gravity in Specific Gravity instead of Plato degree
USE_SG = False

BJCP_GUIDE_JSON = 'bjcp-2015.json'

MAX_SRM = {'min': 30, 'avg': 35, 'max': 40}
MAX_IBU = {'min': 60, 'avg': 90, 'max': 120}
MAX_OG = {'min': 18.8, 'avg': 23.6, 'max': 30.1}
MAX_FG = {'min': 5.1, 'avg': 7.3, 'max': 10}
MAX_ABV = {'min': 7.1, 'avg': 9.1, 'max': 11.1}
MAX_BUGU = {'min': 0.71, 'avg': 1.2, 'max': 1.85}

MIN_SRM = {'min': 2, 'avg': 2.5, 'max': 3}
MIN_IBU = {'min': 0, 'avg': 5, 'max': 8}
MIN_OG = {'min': 6.5, 'avg': 7.5, 'max': 8}
MIN_FG = {'min': -0.5, 'avg': 0.8, 'max': 1.5}
MIN_ABV = {'min': 1.9, 'avg': 2.2, 'max': 2.5}
MIN_BUGU = {'min': 0, 'avg': 0.1, 'max': 0.2}


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
        sub['bugu'] = {'min': bu_gu_ratio(float(sub['ibu']['min']), float(sub['og']['max'])),
                       'avg': bu_gu_ratio(float(sub['ibu']['avg']), float(sub['og']['avg'])),
                       'max': bu_gu_ratio(float(sub['ibu']['max']), float(sub['og']['min']))}
        sub['vector'] = calc_vector(sub, 'avg')
        sub['vector_min'] = calc_vector(sub, 'min')
        sub['vector_max'] = calc_vector(sub, 'max')
        if USE_SG:
            convert_to_sg(sub, 'og')
            convert_to_sg(sub, 'fg')
        sub[
            'vital'] = "SRM: {:,}-{:,}, IBU: {:,}-{:,}, OG: {:,}-{:,}, FG: {:,}-{:,}, ABV: {:,}-{:,}, BU:GU: {:,}-{:,}".format(
            sub["srm"]["min"], sub["srm"]["max"], sub["ibu"]["min"], sub["ibu"]["max"], sub["og"]["min"],
            sub["og"]["max"], sub["fg"]["min"], sub["fg"]["max"], sub["abv"]["min"], sub["abv"]["max"],
            sub["bugu"]["min"], sub["bugu"]["max"])
        sub[
            'vital_avg'] = "SRM: {:,}, IBU: {:,}, OG: {:,}, FG: {:,}, ABV: {:,}, BU:GU: {:,}".format(
            sub["srm"]["avg"], sub["ibu"]["avg"], sub["og"]["avg"], sub["fg"]["avg"], sub["abv"]["avg"],
            sub["bugu"]["avg"])
        del sub['vital_statistics']
    if sub.get('color_classifications'):
        del sub['color_classifications']
    if sub.get('strength_classifications'):
        del sub['strength_classifications']
    if sub.get('styles'):
        for sub_sub in sub['styles']:
            dump(sid, style, sub_sub)
    else:
        output(sub)


def output(sub):
    if GEN_DATA:
        output_file(sub)
    else:
        output_es(sub)


def output_es(sub):
    print('{"index":{"_id":"' + sub['id'] + '"}}')
    print(json.dumps(sub))


def output_file(sub):
    f = open("/tmp/" + sub['id'] + ".json", "w+")
    f.write(json.dumps(sub))
    f.close()
    output_md_file(sub)


def output_md_file(sub):
    f = codecs.open("/tmp/" + sub['id'] + ".md", "w+", "utf-8")
    f.write('---\nid: "' + sub['id'] + '"\ntitle: "' + sub['subcategory'] + '"\ntype: beer\n---\n\n.\n')
    f.close()


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


def calc_vector(sub, dim):
    return calc_vector_5(sub, dim)


def calc_vector_5_unorm(sub):
    dim = 'avg'
    return [float(sub['ibu'][dim]), float(sub['srm'][dim]),
            float(sub['og'][dim]), float(sub['fg'][dim]),
            float(sub['abv'][dim])]


def calc_vector_6(sub, dim):
    srm = float(sub['srm'][dim])
    ibu = float(sub['ibu'][dim])
    og = float(sub['og'][dim])
    fg = float(sub['fg'][dim])
    abv = float(sub['abv'][dim])
    bugu = float(sub['bugu'][dim])
    return [normalize(ibu, MIN_IBU['min'], MAX_IBU['max']), normalize(srm, MIN_SRM['min'], MAX_SRM['max']),
            normalize(og, MIN_OG['min'], MAX_OG['max']), normalize(fg, MIN_FG['min'], MAX_FG['max']),
            normalize(abv, MIN_ABV['min'], MAX_ABV['max']), normalize(bugu, MIN_BUGU['min'], MAX_BUGU['max'])]


def calc_vector_5(sub, dim):
    srm = float(sub['srm'][dim])
    ibu = float(sub['ibu'][dim])
    og = float(sub['og'][dim])
    fg = float(sub['fg'][dim])
    abv = float(sub['abv'][dim])
    return [normalize(ibu, MIN_IBU['min'], MAX_IBU['max']), normalize(srm, MIN_SRM['min'], MAX_SRM['max']),
            normalize(og, MIN_OG['min'], MAX_OG['max']), normalize(fg, MIN_FG['min'], MAX_FG['max']),
            normalize(abv, MIN_ABV['min'], MAX_ABV['max'])]


def normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)


def calc_vector_15(sub):
    ret = []
    for dim in ['avg', 'max', 'min']:
        ret.extend([float(sub['srm'][dim]) / MAX_SRM[dim], float(sub['ibu'][dim]) / MAX_IBU[dim],
                    float(sub['og'][dim]) / MAX_OG[dim], float(sub['fg'][dim]) / MAX_FG[dim],
                    float(sub['abv'][dim]) / MAX_ABV[dim]])
    return ret


def parse(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        for style in data:
            # print(id + ' Name: ' + style['name'])
            for sub in style['subcategories']:
                dump(style['id'], style['name'], sub)


parse(BJCP_GUIDE_JSON)
