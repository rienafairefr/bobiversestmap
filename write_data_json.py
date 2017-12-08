from genealogy import get_characters
from scenes import get_scenes_books
from scenes_locations import get_scenes_locations_book
from utils import json_dump


def get_data_json(nb=None):
    characters = get_characters()

    scenes = get_scenes_books(nb)
    scenes_locations = get_scenes_locations_book(nb)

    data = dict(characters=characters,
                scenes=scenes,
                scenes_locations=scenes_locations)

    return data


def write_data_json(nb=None):
    if nb is None:
        nb = ''
    json_dump(get_data_json(nb), open('data%s.json' % nb, 'w'))


if __name__ == '__main__':
    write_data_json()
