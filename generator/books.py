import os
import re

from sortedcontainers import SortedDict

from app import db
from generator.models.books import Book
from generator.models.chapters import BookChapter
from generator.nl import sentences_tokenize, word_tokenize_sentences


def get_books():
    return [book.lines for book in Book.query.all()]


chapter_re = re.compile('^(\d*)\.(.*)$')


def from_chapter(chapter):
    obj = BookChapter()
    obj.bob = chapter[1]
    obj.date = chapter[2]
    obj.raw_location = chapter[3]

    obj.content = chapter[4:]
    obj.all_lines = '\n'.join(chapter[4:])
    obj.sentences = list(sentences_tokenize(obj.content))
    obj.tokenized_content = list(word_tokenize_sentences(obj.sentences))

    return obj


def import_book_chapters(books=None):
    if books is None:
        books = get_books()

    book_chapters = SortedDict()
    for index_book, book_lines in enumerate(books):
        chapter = []
        index_chapter = 0

        def create(idx, ch):
            book_chapter = from_chapter([book_line.content for book_line in ch])
            book_chapter.nb = index_book + 1
            book_chapter.nc = idx + 1
            book_chapter.lines = ch
            book_chapters[index_book + 1, idx + 1] = book_chapter

        for book_line in book_lines:
            line = book_line.content
            if len(line.strip()) == 0:
                continue
            if re.match('^\d*\.', line):
                if len(chapter) > 0:
                    create(index_chapter, chapter)
                    index_chapter = index_chapter + 1
                chapter = []
            chapter.append(book_line)
        create(index_chapter, chapter)

    # Error in the book ? Big Top is in Epsilon Indi
    book_chapters[3, 62].location_id = 'Epsilon Indi'

    db.session.add_all(book_chapters.values())
    db.session.commit()
    return get_book_chapters()


def get_book_chapters(nb=None):
    q = db.session.query(BookChapter)
    if nb is not None:
        q = q.filter(BookChapter.nb == nb)
    return {(b.nb, b.nc): b for b in q.all()}


def get_keys():
    return get_book_chapters().keys()


def write_chapters(book_chapters):
    os.makedirs(os.path.join('generated', 'book_chapters'), exist_ok=True)
    for k, chapter in book_chapters.items():
        os.makedirs(os.path.join('generated', 'chapters', str(k[0])), exist_ok=True)
        with open(os.path.join('generated', 'chapters', str(k[0]), '%d %d' % k), 'w', encoding='utf-8') as chapter_file:
            chapter_file.writelines([l+'\n' for l in chapter.raw])
