#!/usr/bin/python2
import vdf
import json
from pprint import pprint

def parse_client_schema(schema_file='client_schema.vdf'):
    with open(schema_file) as schema:
        data = vdf.parse(schema)
        items = {}

        for obj_id, obj in data['items_game']['items'].iteritems():
            item = {}
            if 'name' in obj:
                item['name'] = obj['name']
            else:
                item['name'] = obj_id

            # Classes
            if 'used_by_classes' in obj:
                item['used_by_classes'] = [class_name for class_name in obj['used_by_classes']]

            # Equip regions
            item['equip_regions'] = []
            if 'equip_regions' in obj:
                item['equip_regions'] = [eqr for eqr in obj['equip_regions']]
            if 'equip_region' in obj:
                item['equip_regions'].append(obj['equip_region'])
            
            # Prefab also affects the equip regions
            # Not sure about 'misc'
            # special_prefabs = ['hat', 'base_hat', 'misc', 'tournament_medal']
            special_prefabs = ['tournament_medal']
            if 'prefab' in obj:
                for sp in special_prefabs:
                    if sp in obj['prefab']:
                        item['equip_regions'].append(sp)

            items[obj['name']] = item

        return items

items = parse_client_schema()
j = json.dumps(items)
print j
# pprint(items)
# for a,b, in items.iteritems():
#     print a
