#!/usr/bin/python2
import vdf
import json

client_schema_file = 'schema_client.vdf'
main_schema_file = 'schema_main.json'

ignore_item_classes = ['tool', 'supply_crate']
accept_item_classes = ['tf_wearable', 'tf_weapon_medigun', 'tf_powerup_bottle']

# does 'whole head' conflict with 'lenses' by transitivity?
conflicts_table = {
	'glasses' : ['face', 'lenses'],
	'whole_head' : ['hat', 'face', 'glasses', 'lenses'],
}

def prop(dic, prop_name):
    """ Gets name property and set-ifies it. """
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

        # Parsing the prefabs' equip regions
        schema_prefabs = {}
        for pf_name, pf in client_schema['items_game']['prefabs'].iteritems():
            pf_equip_region = prop(pf, 'equip_region')
            if len(pf_equip_region)>0:
                schema_prefabs[pf_name] = list(pf_equip_region)

        # Parsing the items
        items_tmp = {}
        for obj_id, obj in client_schema['items_game']['items'].iteritems():
            item = {}
            item_name = obj['name']

            """
                Short strings are used for the fields (saving ~32KiB):
                c - classes
                e - equip_regions
                i - image
            """

            # Character Classes
            item['c'] = prop(obj, 'used_by_classes')

            # Equip regions
            equip_regions = set()
            equip_regions |= prop(obj, 'equip_regions')
            equip_regions |= prop(obj, 'equip_region')

            # Prefab also affects the equip regions.
            # We already parsed the prefabs earlier.
            # For each of the item's prefabs, get that
            # prefab's equip regions and add them to the item's.
            if 'prefab' in obj:
                item_prefabs = set(obj['prefab'].split(' '))
                for ipf in item_prefabs:
                    equip_regions |= prop(schema_prefabs, ipf)
            item['e'] = set(equip_regions)    
            
            # add equip_regions from the conflicts_table dict
            for eq in equip_regions:
                if eq in conflicts_table:
                    item['e'] |= set(conflicts_table[eq])
                    
            items_tmp[item_name] = item

        """
            Going over the schema (not the client one) we do two things:
            1. Add an image URL
            2. Recreate the item list, this time using the item's real (in-game) name.
            Some items (like the Proffessor Speks) feature in the client schema under
            an unfamiliar internal name. The name which is put here is instead the one
            people see in-game.
        """
        items = {}
        schema = json.loads(main_schema.read())
        schema_items = schema['result']['items']
        for schema_item in schema_items:
            # if schema_item['item_class'] in ignore_item_classes: continue
            if schema_item['item_class'] not in accept_item_classes: continue
            
            # item is refered in both schemas by its internal 'name'
            item = items_tmp[schema_item['name']]

            # sometimes the classes list is only present in the main schema
            item['c'] |= prop(schema_item, 'used_by_classes')
            if len(item['c'])==9: item['c'] = []
            # deleting this element if empty saves only ~2KiB, so don't bother
            
            # the common image location prefix is 45 characters long (saving ~65KiB)
            # http://media.steampowered.com/apps/440/icons/
            item['i'] = schema_item['image_url'][45:]
            # the actual in-game name of the item
            ingame_name = schema_item['item_name']
            items[ingame_name] = item
        
        return items

def set_default(obj):
    ''' json doesn't like sets '''
    if isinstance(obj, set): return list(obj)
    raise TypeError

items = parse_schema()
print json.dumps(items, default=set_default)
