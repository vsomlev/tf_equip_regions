#!/usr/bin/python2
import vdf
import json
from pprint import pprint


client_schema_file = 'client_schema.vdf'
schema_file = 'schema.json'

def parse_schema():
    with open(client_schema_file) as client_schema, open(schema_file) as schema:
        client_schema = vdf.parse(client_schema)
        items_tmp = {}
        items = {}

        for obj_id, obj in client_schema['items_game']['items'].iteritems():
            item = {}
            if 'name' in obj:
                item_name = obj['name']
            else:
                item_name = obj_id

            # Character Classes
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
            special_prefabs = ['hat', 'tournament_medal', 'powerup_bottle']
            if 'prefab' in obj:
                for sp in special_prefabs:
                    if sp in obj['prefab']:
                        item['equip_regions'].append(sp)

            items_tmp[item_name] = item

        """
            Going over the schema (not the client one) we do two things:
            1. Add an image URL
            2. Recreate the item list, this time using the item's real name.
            Some items (like the Proffessor Speks) feature in the client schema under
            an unfamiliar internal name. The name which is put here is instead the one
            people see in-game.
        """
        schema = json.loads(schema.read())
        schema_items = schema['result']['items']
        ignore_item_classes = ['tool', 'supply_crate']
        accept_item_classes = ['tf_wearable', 'tf_weapon_medigun', 'tf_powerup_bottle']
        for schema_item in schema_items:
            #if schema_item['item_class'] in ignore_item_classes:
            #    continue
            if schema_item['item_class'] not in accept_item_classes:
                continue
            name = schema_item['name']
            item = items_tmp[name]
            real_name = schema_item['item_name']
            item['image_url'] = schema_item['image_url']
            item['name'] = real_name
            items[real_name] = item

        return items

items = parse_schema()
j = json.dumps(items)
print j
# pprint(items)
# for a,b, in items.iteritems():
#     print a
