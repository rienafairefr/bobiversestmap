from collections import OrderedDict

import dateutil

from genealogy import get_characters_map, get_characters
from locations import get_locations
from read_dates import get_dates
from scenes import get_scenes_books
from scenes_locations import get_scenes_locations_book
from utils import memoize, sorted_by_key


@memoize()
def get_travels_book(nb=None):
    scenes = get_scenes_books(nb)
    scenes_locations = get_scenes_locations_book(nb)
    characters_map = get_characters_map()
    dates = get_dates()

    data_travels_dict = OrderedDict()
    for character_id, character in sorted(characters_map.items()):
        one_character = {}
        current_location = {}
        for k, scene in scenes.items():
            if character_id in scene['character_ids']:
                current_location = scenes_locations[k]
            if isinstance(current_location, list):
                current_location_id = [current_location[0].get('id'), current_location[1].get('id')]
            else:
                current_location_id = current_location.get('id')
            one_character[k] = {'date_id': dates[k]['id'], 'location_id': current_location_id}

        one_character = postprocess(one_character, character)
        one_character = {k: v for k, v in one_character.items() if nb is None or k[0] == nb}
        data_travels_dict[character_id] = one_character

    return data_travels_dict


def postprocess(input, character):
    if character['affiliation'] == 'Deltans':
        for k, element in input.items():
            if element['location_id'] is not None:
                input[k]['location_id'] = 'Delta Eridani_Eden'
    if character['affiliation'] == 'Poseidon Revolution':
        for k, element in input.items():
            if element['location_id'] is not None:
                input[k]['location_id'] = 'Eta Cassiopeiae_Poseidon'

    return input


@memoize()
def get_travels_book_json(nb=None):
    characters = get_characters()
    locations = get_locations()
    dates = get_dates()

    def _treatvalue(val):
        return list(sorted_by_key(val).values())

    travels = [{'character_id': character_id, 'travels': _treatvalue(value)} for character_id,value in get_travels_book(nb).items()]

    return {'locations': locations,
            'dates': _treatvalue(dates),
            'characters':characters,
            'travels': travels}
