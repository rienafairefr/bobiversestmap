import os
from collections import OrderedDict

from readcombined import get_book_chapters
from scenes_locations import get_scenes_locations
from utils import json_dump, memoize


@memoize()
def get_travels():
    chapters_books = get_book_chapters()

    scenes_locations = get_scenes_locations()

    combined = zip(chapters_books.keys(),
                   zip(chapters_books.values(), scenes_locations.values()))

    travels = OrderedDict()
    for (nb,nc), book_chapter, scene_location in combined:
        travels[nb,nc] = OrderedDict({'bob': book_chapter['bob'], 'location': scene_location})

    return travels


def write_travels():
    travels = get_travels()
    def write_travels_(nb=None):
        if nb is None:
            nb = ''
            data_travels = travels
        else:
            data_travels = OrderedDict({k:travel for k, travel in travels.items() if k[0] == nb})

        bobs = list(set(el['bob'] for el in data_travels))

        data_travels_dict = OrderedDict()
        for bob in bobs:
            data_travels_dict[bob] = []
            current_location = None
            for data_travel in data_travels:
                if data_travel['bob'] == bob:
                    current_location = data_travel['location']
                data_travels_dict[bob].append(current_location)

        json_dump(data_travels_dict, os.path.join('generated', 'travels%s.json' % nb))

    write_travels_()
    write_travels_(1)
    write_travels_(2)
    write_travels_(3)


if __name__ == '__main__':
    write_travels()
