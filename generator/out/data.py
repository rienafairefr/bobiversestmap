from generator.books import get_book_chapters
from generator.characters import get_characters
from generator.scenes import get_scenes
from generator.utils import json_dump, sorted_by_key


def get_chapters_locations(book_chapters=None):
    if book_chapters is None:
        book_chapters = get_book_chapters()
    scenes_locations = sorted_by_key({k: book_chapter.location for k, book_chapter in book_chapters.items()})

    return scenes_locations


def get_chapters_locations_book(nb=None):
    return sorted_by_key({k: v for k, v in get_chapters_locations().items() if nb is None or k[0] == nb})


def data_json(nb=None):
    characters = get_characters()

    scenes = list(get_scenes(nb=nb).values())
    scenes_locations = list(get_chapters_locations_book(nb).values())

    data = dict(characters=characters,
                scenes=scenes,
                scenes_locations=scenes_locations)

    return data


def write_data_json(nb=None):
    json_dump(data_json(nb), 'data%s.json' % ('' if nb is None else nb))


if __name__ == '__main__':
    write_data_json()
