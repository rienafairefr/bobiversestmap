import os

from generator.books import get_book_chapters
from generator.utils import json_dump, memoize, sorted_by_key


@memoize()
def get_scenes(book_chapters=None, nb=None):
    if book_chapters is None:
        book_chapters = get_book_chapters(nb)

    scenes = {}

    for k, book_chapter in book_chapters.items():
        book_chapter_characters = book_chapter.characters

        present_set = {book_chapter.bob}
        for character in book_chapter_characters:
            if not character.is_bob:
                present_set.add(character.id)

        scenes[k] = {'character_ids': list(present_set), 'description': book_chapter.description}

    return sorted_by_key(scenes)


def write_scenes():
    def write_scenes_(nb=None):
        json_dump(list(get_scenes(nb).values()), open(os.path.join('generated', 'scenes%s.json' % nb), 'w'))

    write_scenes_()
    write_scenes_(1)
    write_scenes_(2)
    write_scenes_(3)


if __name__ == '__main__':
    write_scenes()
