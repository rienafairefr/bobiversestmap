from collections import OrderedDict

import os

from genealogy import get_characters_map, get_characters, get_bob_characters, is_bob
from locations import get_locations
from read_dates import get_dates
from readcombined import get_book_chapters
from scenes import get_scenes_books, get_thresholds_deaths
from scenes_locations import get_scenes_locations_book
from utils import memoize, sorted_by_key


@memoize()
def get_travels_book(nb=None):
    scenes = get_scenes_books(nb)
    book_chapters = get_book_chapters()
    scenes_locations = get_scenes_locations_book(nb)
    characters_map = get_characters_map()
    dates = get_dates()
    threshold_deaths = get_thresholds_deaths()

    data_travels_dict = OrderedDict()
    for character_id, character in sorted(characters_map.items()):
        threshold_death = threshold_deaths.get(character_id)
        one_character = {}
        current_location = {}
        for k, scene in scenes.items():
            if threshold_death is not None and k > threshold_death:
                continue
            else:
                if is_bob(character_id):
                    if character_id == book_chapters[k]['bob']:
                        current_location = scenes_locations[k]
                else:
                    if character_id in scene['character_ids']:
                        current_location = scenes_locations[k]

            if isinstance(current_location, list):
                current_location_id = [current_location[0].get('id'), current_location[1].get('id')]
            else:
                current_location_id = current_location.get('id')
            one_character[k] = {'date_id': dates[k]['id'], 'location_id': current_location_id}

        data_travels_dict[character_id] = sorted_by_key({k: v for k, v in one_character.items() if nb is None or k[0] == nb})

    data_travels_dict = postprocess(data_travels_dict)
    write_travels(data_travels_dict)

    return data_travels_dict


def postprocess(data_travels_dict):
    characters_map = get_characters_map()
    for character_id, travel in data_travels_dict.items():
        character = characters_map[character_id]
        if character['affiliation'] == 'Deltans':
            for k, element in travel.items():
                if element['location_id'] is not None:
                    data_travels_dict[character_id][k]['location_id'] = 'Delta Eridani_Eden'
        if character['affiliation'] == 'Poseidon Revolution':
            for k, element in travel.items():
                if element['location_id'] is not None:
                    data_travels_dict[character_id][k]['location_id'] = 'Eta Cassiopeiae_Poseidon'

    def fix(bob, nb, nc, new_id):
        data_travels_dict[bob].setdefault((nb, nc), {})['location_id'] = new_id

    def remove(bob, nb, nc):
        if (nb,nc) in data_travels_dict[bob]:
            del data_travels_dict[bob][nb,nc]

    fix('Arthur', 1, 31, 'Sol_Earth')
    fix('Arthur', 1, 43, 'Sol_Earth')
    fix('Arthur', 1, 60, 'Sol_Earth')

    fix('Barney', 1, 60, 'Sol_Earth')

    fix('Bart', 1, 45, 'Alpha Centauri')

    fix('Calvin', 1, 28, 'Alpha Centauri B')
    fix('Goku', 1, 28, 'Alpha Centauri A')

    fix('Bashful', 2, 13, 'GL 54')
    fix('Dopey', 2, 13, 'GL 54')
    fix('Sleepy', 2, 13, 'GL 54')
    fix('Hungry', 2, 13, 'GL 54')

    fix('Bashful', 2, 15, 'GL 54')
    fix('Dopey', 2, 15, 'GL 54')
    fix('Sleepy', 2, 15, 'GL 54')
    fix('Hungry', 2, 15, 'GL 54')

    fix('Bender', 1, 30, 'Delta Eridani_Eden')

    # Luke leaves for Kappa Ceti in 1,39
    # Bender leaves for Gamma Leporis A in 1,39 (16 ly travel)
    for bob in 'Bender', 'Luke':
        keys = list(data_travels_dict[bob].keys())
        for key in keys:
            if key > (1,39):
                remove(bob, *key)

    # Bert and Ernie in colony ships
    fix('Bert', 1, 60, 'Omicron2 Eridani')
    fix('Ernie', 1, 60, 'Omicron2 Eridani')

    fix('Bert', 2, 5, 'Omicron2 Eridani')
    fix('Ernie', 2, 5, 'Omicron2 Eridani')

    # Bridget doesnt leave Vulcan before being replicated
    for (nb,nc) in list(data_travels_dict['Bridget'].keys()):
        if (nb, nc) < (3,41):
            fix('Bridget', nb, nc, 'Omicron2 Eridani_Vulcan')

    # Bruce from Calvin and Goku, born in Alpha Centauri
    fix('Bruce', 1, 45, 'Alpha Centauri')
    fix('Bruce', 2, 37, '11 Leonis Minoris')

    # Butterworth on Vulcan
    for (nb, nc) in list(data_travels_dict['Bridget'].keys()):
        if (nb, nc) >= (1, 61):
            fix('Butterworth', nb, nc, 'Omicron2 Eridani_Vulcan')

    # Julia and clan Bob aboard Exodus-3 go to Omicron2 Eridani, leave in chapter (2,5)

    # Charles one of the first Riker's clones when back to Sol
    fix('Charles', 1, 25, 'Sol')

    fix('Daedalus', 3, 17, ['Epsilon Eridani','Epsilon Indi'])
    fix('Daedalus', 3, 43, ['Epsilon Indi', 'GL 877'])
    fix('Daedalus', 3, 70, 'GL 877')


    # Dexter from Sol to Vulcan
    fix('Dexter', 2, 51, 'Omicron2 Eridani_Vulcan')

    # Dr Doucette on Vulcan
    for (nb, nc) in list(data_travels_dict['Bridget'].keys()):
        if (nb, nc) > (2, 13):
            remove('Doucette', nb, nc)
        else:
            fix('Doucette', nb, nc, 'Sol_Earth')

    # Both coming from Sol (Exodus-6)
    fix('Edwin', 2, 46, 'Epsilon Indi')
    fix('Rudy', 2, 46, 'Epsilon Indi')

    # fill gaps with current known location
    for character_id, travel in data_travels_dict.items():
        current_location_id = None
        delete = []
        for k, element in travel.items():
            if element['location_id'] is not None:
                # location is filled
                current_location_id = element['location_id']
            else:
                # no location
                if current_location_id is None:
                    # mark for deletion
                    delete.append(k)
                else:
                    # propagate in the gaps
                    travel[k]['location_id'] = current_location_id
        for k in delete:
            del travel[k]

    return data_travels_dict


def write_travels(data_travels_dict):
    characters_map = get_characters_map()

    os.makedirs(os.path.join('generated', 'character_locations'), exist_ok=True)
    for character_id, character in sorted(characters_map.items()):
        with open(os.path.join('generated','character_locations',character_id), 'w', encoding='utf-8') as locations_file:
            for (nb, nc), travel in sorted_by_key(data_travels_dict[character_id]).items():
                if travel['location_id'] is None:
                    location_id = '-----'
                else:
                    location_id = travel['location_id']

                try:
                    locations_file.write('{:^10s} {:3d} {:3d} {:s}\n'.format(character_id, nb, nc, location_id))
                except TypeError:
                    locations_file.write('{:^10s} {:3d} {:3d} {:s} -> {:s}\n'.format(character_id, nb, nc, location_id[0], location_id[1]))


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
