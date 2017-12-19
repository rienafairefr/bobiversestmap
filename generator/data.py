from generator.characters import get_characters
from generator.scenes import get_scenes
from generator.scenes_locations import get_scenes_locations_book
from generator.utils import json_dump


def data_json(nb=None):
    characters = get_characters()

    scenes = list(get_scenes(nb).values())
    scenes_locations = list(get_scenes_locations_book(nb).values())

    data = dict(characters=characters,
                scenes=scenes,
                scenes_locations=scenes_locations)

    return data


def write_data_json(nb=None):
    json_dump(data_json(nb), 'data%s.json' % ('' if nb is None else nb))


if __name__ == '__main__':
    write_data_json()
