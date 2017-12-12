import os

from locations import get_locations
from readcombined import get_book_chapters
from utils import json_dump, memoize, sorted_by_key


@memoize()
def get_scenes_locations():
    chapters_books = get_book_chapters()

    locations = get_locations()

    scenes_locations = {}
    for k, book_chapter in chapters_books.items():
        scenes_locations[k] = book_chapter['location']

    # Bob on Earth
    for i in range(1, 13):
        scenes_locations[1, i] = 'Earth'

    # Bob first voyage
    scenes_locations[1, 13] = 'Earth -> Epsilon Eridani'

    # Mulder in Poseidon
    scenes_locations[2, 49] = 'Poseidon'

    # Hal going to GL 54
    scenes_locations[2, 54] = 'GL 877 -> GL 54'

    # Howard moving on
    scenes_locations[2, 58] = 'Vulcan -> HIP 14101'

    # Mulder Leaving Poseidon
    scenes_locations[2, 62] = 'Poseidon'

    # Icarus & Deadalus
    scenes_locations[3, 17] = 'Epsilon Eridani -> Epsilon Indi'
    # Neil & Herschel
    scenes_locations[3, 22] = 'Delta Pavonis'
    scenes_locations[3, 24] = 'Delta Pavonis'
    # Bob on Eden
    scenes_locations[3, 34] = 'Eden'

    # Neil & Herschel moving the Bellerophon
    scenes_locations[3, 38] = 'Delta Pavonis -> Sol'

    # Icarus & Deadalus
    scenes_locations[3, 43] = 'Epsilon Indi -> GL 877'

    # Icarus & Deadalus destroying GL877
    scenes_locations[3, 70] = 'GL 877'

    def treat_one_scene_location(scene_location):
        for location in locations:
            if ('city' in location and location['city'] == scene_location) \
                    or ('planet' in location and location['planet'] == scene_location) \
                    or ('star' in location and location['star'] == scene_location):
                return location

    def treat_scene_location(scene_location):
        treat_one = treat_one_scene_location(scene_location)
        if treat_one:
            return treat_one

        places = [el.strip() for el in scene_location.split('->')]
        return_value = list(map(treat_one_scene_location, places))
        return return_value

    scenes_locations = sorted_by_key({k: treat_scene_location(v) for k, v in scenes_locations.items()})

    return scenes_locations


def get_scenes_locations_book(nb=None):
    return sorted_by_key({k: v for k, v in get_scenes_locations().items() if nb is None or k[0] == nb})


@memoize()
def get_sorted_locations():
    scenes_locations = get_scenes_locations()
    list_scenes_locations = list(scenes_locations.values())
    locations = get_locations()

    def get_index(element):
        try:
            return list_scenes_locations.index(element)
        except ValueError:
            return len(scenes_locations)

    return sorted(locations, key=get_index)


def write_scenes_locations():
    def write_scenes_locations_(nb=None):
        json_dump(get_scenes_locations_book(nb), os.path.join('generated', 'scenes_locations%s.json' % nb))

    write_scenes_locations_()
    write_scenes_locations_(1)
    write_scenes_locations_(2)
    write_scenes_locations_(3)


if __name__ == '__main__':
    write_scenes_locations()
