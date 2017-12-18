import itertools

from generator.books import get_book_chapters
from generator.chapter_characters import get_chapter_characters
from generator.utils import memoize


@memoize()
def get_links():
    chapters_books = get_book_chapters()

    links = {}
    for k, book_chapter in chapters_books.items():
        links[k] = []
        chapter_characters = get_chapter_characters(book_chapter)

        for tokenized_sentence in book_chapter['tokenized_content']:
            for character_pair in itertools.combinations(chapter_characters, 2):
                character0 = character_pair[0]
                character1 = character_pair[1]
                for name0 in character0['all_names']:
                    for name1 in character1['all_names']:
                        if name0 > name1 and name0 in tokenized_sentence and name1 in tokenized_sentence:
                            links[k].append(character_pair)

    return links

