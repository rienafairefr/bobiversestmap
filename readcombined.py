import re
import os
from collections import OrderedDict

from utils import json_dump, memoize


@memoize()
def get_book_chapters():
    with open(os.path.join('data', 'Combined.txt'), encoding='utf-8') as combined:
        content = combined.readlines()

    books = []
    book = []

    for line in content:
        if line.startswith('##'):
            if len(book) > 0:
                books.append(book)
            book = []
        else:
            book.append(line.strip())

    books.append(book)
    book_chapters = []
    index = 0
    for index_book, book in enumerate(books):
        chapter = []
        chapters = []
        for line in book:
            if len(line.strip()) == 0:
                continue
            if re.match('^\d*\.', line):
                if len(chapter) > 0:
                    chapters.append(chapter)
                chapter = []
            chapter.append(line)
        chapters.append(chapter)

        new_chapters = []
        for index_chapter, chap in enumerate(chapters):
            matched = re.match('^(\d*)\.(.*)$', chap[0])
            new_chapters.append(OrderedDict({
                'nb': index_book + 1,
                'nc': index_chapter + 1,
                'n': index + 1,
                'title': matched.groups()[1].strip(),
                'bob': chap[1],
                'date': chap[2],
                'location': chap[3],
                'content': chap[4:]
            }))
            index = index +1

        book_chapters.append(new_chapters)

    return book_chapters

@memoize()
def get_index():
    index = []
    for nb, book_chapters in enumerate(get_book_chapters()):
        for nc, book_chapter in enumerate(book_chapters):
            index.append((nb + 1, nc + 1))
    return index


def write_book_chapters():
    book_chapters = get_book_chapters()
    json_dump(book_chapters, open(os.path.join('generated', 'Combined.json'), 'w'))


if __name__ == '__main__':
    write_book_chapters()
