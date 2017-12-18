import itertools

from generator.books import get_book_chapters
from generator.chapter_characters import get_chapter_characters
from generator.utils import memoize


@memoize()
def get_characters_presences():
    chapters_books = get_book_chapters()

    presences = {}
    for k, book_chapter in chapters_books.items():
        presences[k] = []
        chapter_characters = get_chapter_characters(book_chapter)

        for tokenized_sentence in book_chapter['tokenized_content']:
            for character in chapter_characters:
                for name in character['all_names']:
                    if name in tokenized_sentence:
                        presences[k].append(character)

    return presences
