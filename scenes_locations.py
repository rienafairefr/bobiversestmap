import os
import json

from locations import get_locations
from readcombined import get_index, get_book_chapters
from utils import json_dump, memoize


@memoize()
def get_scenes_locations():
    chapters_books = get_book_chapters()

    locations = get_locations()

    index = []
    for nb, book_chapters in enumerate(chapters_books):
        for nc, book_chapter in enumerate(book_chapters):
            index.append((nb + 1, nc + 1))

    scenes_locations = []
    for nb, book_chapters in enumerate(chapters_books):
        for nc, book_chapter in enumerate(book_chapters):
            scenes_locations.append(book_chapter['location'])

    # Bob on Earth
    for i in range(0, 12):
        scenes_locations[i] = 'Earth'

    # Bob first voyage
    scenes_locations[12] = 'Earth -> Epsilon Eridani'

    # Mulder in Poseidon
    scenes_locations[109] = 'Poseidon'

    # Hal going to GL 54
    scenes_locations[114] = 'GL 877 -> GL 54'

    # Howard moving on
    scenes_locations[118] = 'Vulcan -> HIP 14101'

    # Mulder Leaving Poseidon
    scenes_locations[122] = 'Poseidon'

    # Icarus & Deadalus
    scenes_locations[154] = 'Epsilon Eridani -> Epsilon Indi'
    # Neil & Herschel
    scenes_locations[159] = 'Delta Pavonis'
    scenes_locations[161] = 'Delta Pavonis'
    # Bob on Eden
    scenes_locations[171] = 'Eden'

    # Neil & Herschel moving the Bellerophon
    scenes_locations[175] = 'Delta Pavonis -> Sol'

    # Icarus & Deadalus
    scenes_locations[180] = 'Epsilon Indi -> GL 877'

    # Icarus & Deadalus destroying GL877
    scenes_locations[207] = 'GL 877'

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
        return list(map(treat_one_scene_location, places))

    scenes_locations = list(map(treat_scene_location, scenes_locations))

    return scenes_locations


def get_scenes_locations_book(nb=None):
    index = get_index()
    scenes_locations = get_scenes_locations()
    if nb is None:
        data_scenes_locations = scenes_locations
    else:
        data_scenes_locations = [scenes_locations[i] for i, idx in enumerate(index) if idx[0] == nb]
    return data_scenes_locations


def write_scenes_locations():
    def write_scenes_locations_(nb=None):
        json_dump(get_scenes_locations_book(nb), os.path.join('generated', 'scenes_locations%s.json'%nb))

    write_scenes_locations_()
    write_scenes_locations_(1)
    write_scenes_locations_(2)
    write_scenes_locations_(3)


if __name__ == '__main__':
    write_scenes_locations()
