import itertools

from generator.books import get_book_chapters
from generator.chapter_characters import get_chapter_characters
from generator.travels import get_travels_book
from generator.utils import memoize


class Link(object):
    def __init__(self, char0, char1, scut):
        self.character0 = char0
        self.character1 = char1
        self.is_scut = scut


@memoize()
def get_links(nb=None):
    chapters_books = get_book_chapters()
    travels = get_travels_book(nb)

    links = {}
    for k, book_chapter in chapters_books.items():
        nb, nc = k
        links[k] = []
        chapter_characters = get_chapter_characters(k)

        for tokenized_sentence in book_chapter['tokenized_content']:
            for character_pair in itertools.combinations(chapter_characters, 2):
                character0 = character_pair[0]
                character1 = character_pair[1]
                location0 = travels.get((character0.id, nb, nc))
                location1 = travels.get((character1.id, nb, nc))

                for name0 in character0.all_names:
                    for name1 in character1.all_names:
                        if name0 > name1 and name0 in tokenized_sentence and name1 in tokenized_sentence:
                            is_scut = location0 != {} and location1 != {} and location0 != location1
                            links[k].append(Link(character0, character1, is_scut))

    return links
