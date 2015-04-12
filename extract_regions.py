#!/usr/bin/python2
import vdf
import json
from pprint import pprint

client_schema_file = 'schema_client.vdf'
main_schema_file = 'schema_main.json'

ignore_item_classes = ['tool', 'supply_crate']
accept_item_classes = ['tf_wearable', 'tf_weapon_medigun', 'tf_powerup_bottle']

def prop(dic, prop_name):
    """ Gets the name property and list-ifies it. """
    if prop_name in dic: 
        prop = dic[prop_name]
        if isinstance(prop, str): 
            return set([prop])
        else:
            return set([i.lower() for i in prop])
    return set()

def parse_schema():
    with open(client_schema_file) as client_schema, open(main_schema_file) as main_schema:
        client_schema = vdf.parse(client_schema)

        # Parsing the prefabs
        schema_prefabs = {}
        for pf_name, pf in client_schema['items_game']['prefabs'].iteritems():
            pf_equip_region = prop(pf, 'equip_region')
            if len(pf_equip_region)>0:
                schema_prefabs[pf_name] = list(pf_equip_region)

        # Parsing the items
        items_tmp = {}
        items = {}

        for obj_id, obj in client_schema['items_game']['items'].iteritems():
            item = {}
            item_name = obj['name']

            # Character Classes
            item['classes'] = set()
            item['classes'] |= prop(obj, 'used_by_classes')

            # Equip regions
            item['equip_regions'] = set()
            item['equip_regions'] |= prop(obj, 'equip_regions')
            item['equip_regions'] |= prop(obj, 'equip_region')

            # Prefab also affects the equip regions
            # for each of the item's prefabs, get that
            # prefab's equip regions and add them to the item's
            if 'prefab' in obj:
                item_prefabs = set(obj['prefab'].split(' '))
                prefab_equip_regions = set()
                for ipf in item_prefabs:
                    prefab_equip_regions |= prop(schema_prefabs, ipf)
                item['equip_regions'] |= prefab_equip_regions

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
            if len(item['classes'])==0 or len(item['classes'])>8:
                item['classes'] = ['all']

            item['name'] = ingame_name
            item['image'] = schema_item['image_url']

            items[ingame_name] = item

        return items

def set_default(obj):
    ''' json doesn't like sets '''
    if isinstance(obj, set): return list(obj)
    raise TypeError

items = parse_schema()
print json.dumps(items, default=set_default)
