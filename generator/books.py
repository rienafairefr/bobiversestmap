import os
import re

from sortedcontainers import SortedDict

from app import db
from generator.models.books import Book
from generator.models.chapters import BookChapter
from generator.utils import memoize


def get_books():
    return [[book_line.content for book_line in book.lines] for book in Book.query.all()]


chapter_re = re.compile('^(\d*)\.(.*)$')


def import_book_chapters(books=None):
    if books is None:
        books = get_books()

    book_chapters = SortedDict()
    for index_book, book in enumerate(books):
        chapter = []
        index_chapter = 0
        for line in book:
            if len(line.strip()) == 0:
                continue
            if re.match('^\d*\.', line):
                if len(chapter) > 0:
                    book_chapter = BookChapter.from_chapter(chapter)
                    book_chapter.nb = index_book + 1
                    book_chapter.nc = index_chapter + 1
                    book_chapters[index_book + 1, index_chapter + 1] = book_chapter
                    index_chapter = index_chapter + 1
                chapter = []
            chapter.append(line)
        book_chapter = BookChapter.from_chapter(chapter)
        book_chapter.nb = index_book + 1
        book_chapter.nc = index_chapter + 1
        book_chapters[index_book + 1, index_chapter + 1] = book_chapter

    # Error in the book ? Big Top is in Epsilon Indi
    book_chapters[3, 62].location_id = 'Epsilon Indi'

    db.session.add_all(book_chapters.values())
    db.session.commit()
    return get_book_chapters()


def get_book_chapters():
    return {(b.nb, b.nc): b for b in db.session.query(BookChapter).all()}


def get_keys():
    return get_book_chapters().keys()


def write_chapters(book_chapters):
    os.makedirs(os.path.join('generated', 'book_chapters'), exist_ok=True)
    for k, chapter in book_chapters.items():
        os.makedirs(os.path.join('generated', 'chapters', str(k[0])), exist_ok=True)
        with open(os.path.join('generated', 'chapters', str(k[0]), '%d %d' % k), 'w', encoding='utf-8') as chapter_file:
            chapter_file.writelines([l+'\n' for l in chapter.raw])
