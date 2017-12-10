from genealogy import get_characters
from scenes import get_scenes_books, RelationShipParsingType
from scenes_locations import get_scenes_locations_book
from utils import json_dump


def get_data_json(nb=None, relationships_parsing_type=RelationShipParsingType.NAME_IN_WORDS):
    characters = get_characters()

    scenes = get_scenes_books(relationships_parsing_type, nb)
    scenes_locations = get_scenes_locations_book(nb)

    data = dict(characters=characters,
                scenes=scenes,
                scenes_locations=scenes_locations)

    return data


def write_data_json(nb=None):
    json_dump(get_data_json(nb), 'data%s.json' % ('' if nb is None else nb))


if __name__ == '__main__':
    write_data_json()
