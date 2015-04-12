#!/usr/bin/python2
import vdf
import json
from pprint import pprint
from sets import Set

client_schema_file = 'schema_client.vdf'
main_schema_file = 'schema_main.json'

# TODO: Makes sure that this list works as intended.
special_prefabs = Set(['hat', 'tournament_medal', 'powerup_bottle'])
ignore_item_classes = ['tool', 'supply_crate']
accept_item_classes = ['tf_wearable', 'tf_weapon_medigun', 'tf_powerup_bottle']

def prop(dic, prop_name):
    """ Gets the name property and list-ifies it. """
    if prop_name in dic: 
        prop = dic[prop_name]
        if isinstance(prop, str): 
            return Set([prop])
        else:
            return Set([i.lower() for i in prop])
    return Set()

def parse_schema():
    with open(client_schema_file) as client_schema, open(main_schema_file) as main_schema:
        client_schema = vdf.parse(client_schema)
        items_tmp = {}
        items = {}

        for obj_id, obj in client_schema['items_game']['items'].iteritems():
            item = {}
            item_name = obj['name']

            # Character Classes
            item['classes'] = Set()
            item['classes'] |= prop(obj, 'used_by_classes')

            # Equip regions
            item['equip_regions'] = Set()
            item['equip_regions'] |= prop(obj, 'equip_regions')
            item['equip_regions'] |= prop(obj, 'equip_region')
            # Prefab also affects the equip regions
            obj_prefabs = prop(obj, 'prefab')
            special_prefab_matches = obj_prefabs.intersection(special_prefabs)
            item['equip_regions'] |= special_prefab_matches

            items_tmp[item_name] = item

        """
            Going over the schema (not the client one) we do two things:
            1. Add an image URL
            2. Recreate the item list, this time using the item's real (in-game) name.
            Some items (like the Proffessor Speks) feature in the client schema under
            an unfamiliar internal name. The name which is put here is instead the one
            people see in-game.
        """

        schema = json.loads(main_schema.read())
        schema_items = schema['result']['items']
        for schema_item in schema_items:
            # if schema_item['item_class'] in ignore_item_classes: continue
            if schema_item['item_class'] not in accept_item_classes: continue
            name = schema_item['name']
            ingame_name = schema_item['item_name']
            item = items_tmp[name]

            # sometimes the classes list is only present in the main schema
            item['classes'] |= prop(schema_item, 'used_by_classes')
            if len(item['classes'])==0 or len(items['classes'])>8:
                item['classes'] = ['all']

            item['name'] = ingame_name
            item['image'] = schema_item['image_url']

            # json doesn't like Sets
            item['equip_regions'] = list(item['equip_regions'])
            item['classes'] = list(item['classes'])

            items[ingame_name] = item

        return items

items = parse_schema()
print json.dumps(items)
