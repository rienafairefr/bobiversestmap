import contextlib
import os
from sortedcontainers import SortedDict

from generator.characters import get_characters_map
from generator.dates import get_dates
from generator.books import get_book_chapters, get_keys
from generator.presences import get_characters_presences
from generator.thresholds import get_thresholds_last, get_thresholds_first
from generator.scenes_locations import get_scenes_locations_book
from generator.utils import memoize


@memoize()
def get_travels_book(nb=None, presences=None, book_chapters=None, scenes_locations=None, characters_map=None):
    if presences is None:
        presences = get_characters_presences(nb)
    if book_chapters is None:
        book_chapters = get_book_chapters()
    if scenes_locations is None:
        scenes_locations = get_scenes_locations_book(nb)
    if characters_map is None:
        characters_map = get_characters_map()

    data_travels_dict = SortedDict()
    for character_id, character in sorted(characters_map.items()):
        for k, present_characters in presences.items():
            current_location = None
            if character.is_bob:
                if character_id == book_chapters[k].bob :
                    current_location = scenes_locations[k]
            else:
                if character_id in present_characters:
                    current_location = scenes_locations[k]

            if current_location is not None:
                current_location_id = current_location.id
            else:
                current_location_id = None
            nb, nc = k
            data_travels_dict[character_id, nb, nc] = {'location_id': current_location_id}

    data_travels_dict = postprocess(data_travels_dict)
    data_travels_dict = postproces_births_deaths(data_travels_dict)
    write_travels(data_travels_dict)

    return data_travels_dict


def postproces_births_deaths(data_travels_dict, threshold_deaths=None, threshold_births=None):
    if threshold_deaths is None:
        threshold_deaths = get_thresholds_last()
    if threshold_births is None:
        threshold_births = get_thresholds_first()

    for (character_id, nb, nc), element in data_travels_dict.items():
        threshold_death = threshold_deaths.get(character_id)
        threshold_birth = threshold_births.get(character_id)
        if (threshold_birth is not None and (nb, nc) < threshold_birth) \
                or (threshold_death is not None and (nb, nc) > threshold_death):
            data_travels_dict[character_id, nb, nc] = {}
    return data_travels_dict


def postprocess(data_travels_dict, dates=None, characters_map=None, keys=None):
    if dates is None:
        dates = get_dates()
    if characters_map is None:
        characters_map = get_characters_map()
    if keys is None:
        keys = get_keys()

    for (character_id, nb, nc), element in data_travels_dict.items():
        character = characters_map[character_id]
        if character.affiliation == 'Deltans':
            if element['location_id'] is not None:
                data_travels_dict[character_id, nb, nc]['location_id'] = 'Delta Eridani_Eden'
        if character.affiliation == 'Poseidon Revolution':
            if element['location_id'] is not None:
                data_travels_dict[character_id, nb, nc]['location_id'] = 'Eta Cassiopeiae_Poseidon'

    def fix(bob, nb, nc, new_id):
        data_travels_dict.setdefault((bob, nb, nc), {'date_id': dates[nb, nc].id})['location_id'] = new_id

    def remove(bob, nb, nc):
        data_travels_dict[bob, nb, nc] = {}

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
        for key in keys:
            if key > (1, 39):
                remove(bob, *key)

    # Bert and Ernie in colony ships
    fix('Bert', 1, 58, 'Sol_Earth')
    fix('Ernie', 1, 58, 'Sol_Earth')
    fix('Bert', 1, 61, 'Omicron2 Eridani')
    fix('Ernie', 1, 61, 'Omicron2 Eridani')

    fix('Bert', 2, 5, 'Omicron2 Eridani')
    fix('Ernie', 2, 5, 'Omicron2 Eridani')

    # Bridget arrives on Vulcan at (1, 61)
    fix('Bridget', 1, 61, 'Omicron2 Eridani_Vulcan')
    # Bridget doesnt leave Vulcan before being replicated
    fix('Bridget', 3, 40, 'Omicron2 Eridani_Vulcan')

    # Bruce from Calvin and Goku, born in Alpha Centauri
    fix('Bruce', 1, 45, 'Alpha Centauri')
    fix('Bruce', 2, 37, '11 Leonis Minoris')

    # Milo
    fix('Milo', 1, 17, 'Epsilon Eridani')
    fix('Milo', 1, 19, 'Omicron2 Eridani')
    fix('Milo', 1, 46, '82 Eridani')

    # Landers on Vulcan
    for k in keys:
        if k> (1, 1) and k <= (1, 13):
            fix('Landers', *k, 'Sol_Earth')

    # Butterworth on Vulcan
    for k in keys:
        if k >= (1, 61):
            fix('Butterworth', *k, 'Omicron2 Eridani_Vulcan')

    # Julia and clan Bob aboard Exodus-3 go to Omicron2 Eridani, leave in chapter (2,5)

    # Charles one of the first Riker's clones when back to Sol
    fix('Charles', 1, 25, 'Sol')

    fix('Daedalus', 3, 17, ['Epsilon Eridani', 'Epsilon Indi'])
    fix('Daedalus', 3, 43, ['Epsilon Indi', 'GL 877'])
    fix('Daedalus', 3, 70, 'GL 877')

    #  Dexter from Sol to Vulcan
    fix('Dexter', 2, 51, 'Omicron2 Eridani_Vulcan')

    # Dr Doucette on Vulcan
    for k in keys:
        if k > (2, 13):
            remove('Doucette', *k)
        else:
            fix('Doucette', *k, 'Sol_Earth')

    # Both coming from Sol (Exodus-6)
    fix('Edwin', 2, 46, 'Epsilon Indi')
    fix('Rudy', 2, 46, 'Epsilon Indi')

    # Going agains Medeiros
    # the cohort of 8 being built by Bill in Epsilon Eridani in (1,51)
    fix('Elmer', 1, 51, 'Epsilon Eridani')
    fix('Elmer', 1, 60, '82 Eridani')
    fix('Khan', 1, 51, 'Epsilon Eridani')
    fix('Khan', 1, 60, '82 Eridani')
    fix('Fred', 1, 51, 'Epsilon Eridani')
    fix('Fred', 1, 60, '82 Eridani')

    # second wave
    fix('Elmer', 2, 34, 'Epsilon Eridani')
    fix('Elmer', 2, 50, '82 Eridani')
    fix('Loki', 2, 34, 'Epsilon Eridani')
    fix('Loki', 2, 50, '82 Eridani')
    fix('Verne', 2, 34, 'Epsilon Eridani')
    fix('Verne', 2, 50, '82 Eridani')
    fix('Hank', 2, 34, 'Epsilon Eridani')
    fix('Hank', 2, 50, '82 Eridani')

    # Elmer destroyed in 1,60 ; restored in in 2,34
    # Khan restored a backup in 2,34 named Loki

    # Phineas and Ferb come online in Delta Pavonis for Pav extraction
    # Jacques arrived there in 2,60
    fix('Phineas', 2, 73, 'Delta Pavonis')
    fix('Ferb', 2, 73, 'Delta Pavonis')

    #  Jacques killed in battle of Delta pavonis, but restored
    fix('Phineas', 3, 48, 'HIP 84051')
    fix('Ferb', 3, 48, 'HIP 84051')
    fix('Jacques', 3, 48, 'HIP 84051')

    fix('Ferb', 3, 74, 'HIP 84051')

    # stays with Bill all the way
    fix('Garfield', 1, 20, 'Epsilon Eridani')

    # Hal blown up in GL 877 in (2,38)
    # goes back there in (2,53)
    remove('Hal', 2, 39)

    # Hannibal blown up in (1,60)
    # restored ?
    # leads the Jokers in Sol in (3,64)
    fix('Hannibal', 1, 60, '82 Eridani')
    fix('Hannibal', 3, 64, 'Sol')

    # Mario leaves GL 54 in (2,54)

    # Hank mentioned in 3,21
    fix('Hank', 3, 21, "P Eridani")

    # Assume Henry Roberts doesnt leave Epsilon Indi after leaving Earth
    for k in keys:
        if k > (1, 13):
            fix('Henry', *k, 'Epsilon Indi')
        else:
            fix('Henry', *k, 'Sol_Earth')

    remove('Henry', 1, 1)
    fix('Henry', 1, 13, ['Sol_Earth', 'Epsilon Indi'])

    # Herschel and Neil leaving for 82 Eridani in (3,75)

    #  Homer going to Sol with Riker
    fix('Homer', 1, 20, 'Epsilon Eridani')
    fix('Homer', 1, 21, 'Sol')
    fix('Riker', 1, 20, 'Epsilon Eridani')
    fix('Riker', 1, 21, 'Sol')

    # Howard from Sol to Omicron2 Eridani/Vulcan
    fix('Howard', 1, 58, 'Sol')
    fix('Howard', 1, 61, 'Omicron2 Eridani')
    fix('Howard', 3, 20, 'HIP 14101_Odin')

    fix('Howard', 3, 62, 'Epsilon Indi_Big Top')

    # Isaac, Jack, and Owen three colony ships arriving in 82 Eridani from Sol in (3,18)

    delete = []
    current_location_id = None
    # fill gaps with current known location
    for (character_id, nb, nc), element in data_travels_dict.items():
        if (nb, nc) == (1, 1):
            current_location_id = None

        if element.get('location_id') is not None:
            # location is filled
            current_location_id = element['location_id']
        else:
            # no location
            if current_location_id is None:
                # mark for deletion
                delete.append((character_id, nb, nc))
            else:
                # propagate in the gaps
                data_travels_dict[character_id, nb, nc]['location_id'] = current_location_id
    for k in delete:
        data_travels_dict[k] = {}

    return data_travels_dict


def write_travels(data_travels_dict, characters_map=None):
    if characters_map is None:
        characters_map = get_characters_map()

    with contextlib.ExitStack() as stack:

        locations_files = {}
        for character_id in characters_map.keys():
            os.makedirs(os.path.join('generated', character_id), exist_ok=True)
            locations_files[character_id] = stack.enter_context(open(os.path.join('generated', character_id, 'locations'), 'w',
                                                 encoding='utf-8'))

        for (character_id, nb, nc), element in data_travels_dict.items():
            locations_file = locations_files[character_id]

            if element.get('location_id') is None:
                location_id = '-----'
            else:
                location_id = element['location_id']

            try:
                locations_file.write('{:^10s} {:3d} {:3d} {:s}\n'.format(character_id, nb, nc, location_id))
            except TypeError:
                locations_file.write(
                    '{:^10s} {:3d} {:3d} {:s} -> {:s}\n'.format(character_id, nb, nc, location_id[0],
                                                                location_id[1]))


