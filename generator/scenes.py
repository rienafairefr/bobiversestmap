import os

from generator.book_chapters import get_book_chapters
from generator.utils import json_dump, memoize


@memoize()
def get_scenes(book_chapters=None, nb=None):
    if book_chapters is None:
        book_chapters = get_book_chapters(nb)

    scenes = []

    for book_chapter in book_chapters:
        book_chapter_characters = book_chapter.characters

        present_set = {book_chapter.bob_character.id}
        for character in book_chapter_characters:
            if not character.is_bob:
                present_set.add(character.id)

        scenes.append(
            {
                "character_ids": list(present_set),
                "description": book_chapter.description,
            }
        )

    return scenes


def write_scenes():
    def write_scenes_(nb=None):
        json_dump(
            get_scenes(nb), open(os.path.join("generated", "scenes%s.json" % nb), "w")
        )

    write_scenes_()
    write_scenes_(1)
    write_scenes_(2)
    write_scenes_(3)


if __name__ == "__main__":
    write_scenes()
