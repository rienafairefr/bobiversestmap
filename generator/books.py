import os
import re
from collections import OrderedDict

from generator.nl import tokenize, word_tokenize_sentences, sentences_tokenize
from generator.utils import sorted_by_key, memoize, stripped


@memoize()
def get_books():
    with open(os.path.join('data', 'Combined.txt'), encoding='utf-8') as combined:
        content = combined.readlines()

    books = []
    book = []

    for line in content:
        if line.startswith('##'):
            if len(book) > 0:
                books.append(stripped(book))
            book = []
        else:
            book.append(line.strip())

    books.append(stripped(book))
    return books


chapter_re = re.compile('^(\d*)\.(.*)$')


@memoize()
def get_book_chapters():
    books = get_books()
    book_chapters = OrderedDict()
    for index_book, book in enumerate(books):
        chapter = []
        index_chapter = 0
        for line in book:
            if len(line.strip()) == 0:
                continue
            if re.match('^\d*\.', line):
                if len(chapter) > 0:
                    book_chapters[index_book + 1, index_chapter + 1] = BookChapter(chapter)
                    index_chapter = index_chapter + 1
                chapter = []
            chapter.append(line)
        book_chapters[index_book + 1, index_chapter + 1] = BookChapter(chapter)

    # Error in the book ? Big Top is in Epsilon Indi
    book_chapters[3, 62].location = 'Epsilon Indi'

    return book_chapters


class BookChapter(object):
    def __init__(self, chapter):
        self.bob = chapter[1]
        self.date = chapter[2]
        self.location = chapter[3]

        self.raw = chapter

        self.content = chapter[4:]
        self.sentences = list(sentences_tokenize(self.content))
        self.tokenized_content = list(word_tokenize_sentences(self.sentences))


@memoize()
def get_keys():
    return get_book_chapters().keys()


def write_chapters(book_chapters):
    os.makedirs(os.path.join('generated', 'book_chapters'), exist_ok=True)
    for k, chapter in book_chapters.items():
        os.makedirs(os.path.join('generated', 'chapters', str(k[0])), exist_ok=True)
        with open(os.path.join('generated', 'chapters', str(k[0]), '%d %d' % k), 'w', encoding='utf-8') as chapter_file:
            chapter_file.writelines([l+'\n' for l in chapter.raw])
