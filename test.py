#!/usr/bin/python2
# import json
import vdf
from pprint import pprint

def parse_client_schema(schema_file='client_schema.vdf'):
    with open(schema_file) as schema:
        # data = json.load(schema)
        data = vdf.parse(schema)

    items = []

    def copy_field(obj_a, obj_b, field_name):
        if field_name in obj_a:
            obj_b[field_name] = obj_a[field_name]

    for obj_id, obj in data['items_game']['items'].iteritems():
        item = {}
        item['id'] = obj_id
        copy_field(obj, item, 'name')
        copy_field(obj, item, 'prefab')
        copy_field(obj, item, 'used_by_classes')
        item['equip_regions'] = []
        if 'equip_regions' in obj:
            for eq in obj['equip_regions']:
                item['equip_regions'].append(eq)
        if 'equip_region' in obj:
            item['equip_regions'].append(obj['equip_region'])
        items.append(item)

        if item['name']=='Vive La France':
            print item
        if item['name']=='The Gunboats':
            print item

    return items

items = parse_client_schema()
