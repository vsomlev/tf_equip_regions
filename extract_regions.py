#!/usr/bin/python2
import vdf
import json
from pprint import pprint

client_schema_file = 'schema_client.vdf'
schema_file = 'schema_main.json'

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
                item['classes'] = [class_name for class_name in obj['used_by_classes']]

            # Equip regions
            # there's both 'equip_region' as well as 'equip_regions'
            # they can be either a string, a list, or a dict...
            item['equip_regions'] = []
            if 'equip_regions' in obj:
                obj_eqs = obj['equip_regions']
                if isinstance(obj_eqs, str):
                    item['equip_regions'].append(obj_eqs)
                else:
                    item['equip_regions'].extend([eqr for eqr in obj_eqs])
            if 'equip_region' in obj:
                obj_eq = obj['equip_region']
                if isinstance(obj_eq, str):
                    item['equip_regions'].append(obj_eq)
                else:
                    item['equip_regions'].extend([eqr for eqr in obj_eq])
            
            # Prefab also affects the equip regions
            # special_prefabs = ['hat', 'base_hat', 'misc', 'tournament_medal']
            special_prefabs = ['hat', 'tournament_medal', 'powerup_bottle']
            if 'prefab' in obj:
                for sp in special_prefabs:
                    obj_prefab = obj['prefab']
                    if not isinstance(obj_prefab, list): obj_prefab=[obj_prefab]
                    if sp in obj_prefab:
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
        ignore_item_classes = ['tool', 'supply_crate']
        accept_item_classes = ['tf_wearable', 'tf_weapon_medigun', 'tf_powerup_bottle']

        schema = json.loads(schema.read())
        schema_items = schema['result']['items']
        for schema_item in schema_items:
            # if schema_item['item_class'] in ignore_item_classes: continue
            if schema_item['item_class'] not in accept_item_classes: continue
            name = schema_item['name']
            item = items_tmp[name]
            real_name = schema_item['item_name']
            if 'used_by_classes' in schema_item and 'classes' not in item:
                item['classes'] = [cl.lower() for cl in schema_item['used_by_classes']]
            if 'classes' not in item:
                item['classes'] = ['all']
            item['name'] = real_name
            item['image'] = schema_item['image_url']
            items[real_name] = item

        return items

items = parse_schema()
print json.dumps(items)
