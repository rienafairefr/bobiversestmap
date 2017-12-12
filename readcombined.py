import re
import os
from collections import OrderedDict

from nl import tokenize
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
    book_chapters = OrderedDict()
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

        for index_chapter, chap in enumerate(chapters):
            matched = re.match('^(\d*)\.(.*)$', chap[0])
            new_chapter = OrderedDict({
                'nb': index_book + 1,
                'nc': index_chapter + 1,
                'n': index + 1,
                'title': re.match('^(\d*)\.(.*)$', chap[0]).groups()[1].strip(),
                'bob': chap[1],
                'date': chap[2],
                'location': chap[3],
                'content': chap[4:]
            })
            index = index +1

            book_chapters[index_book+1,index_chapter+1] = new_chapter

    return book_chapters
