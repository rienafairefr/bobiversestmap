import os
import re

from app import db
from generator.books import get_books
from generator.dates import treat_one_period
from generator.models.chapters import BookChapter
from generator.nl import sentences_tokenize, word_tokenize_sentences

chapter_re = re.compile('^(\d*)\.(.*)$')


def from_chapter_lines(chapter_lines):
    book_chapter = BookChapter()
    book_chapter.bob_id = chapter_lines[1]
    book_chapter.period = treat_one_period(chapter_lines[2])
    book_chapter.location_id = chapter_lines[3]

    book_chapter.lines = chapter_lines[4:]

    sentences = list(sentences_tokenize(book_chapter.lines))
    book_chapter.tokenized_content = list(word_tokenize_sentences(sentences))

    return book_chapter


def postprocess_book_chapters():
    # Error in the book ? Big Top is in Epsilon Indi
    book_chapter = db.session.query(BookChapter).get((3, 62))
    book_chapter.location_id = 'Epsilon Indi'
    db.session.commit()


def import_book_chapters(books=None):
    if books is None:
        books = get_books()

    for index_book, book in enumerate(books):
        book_lines = book.lines

        chapter_id = 0
        chapters_lines = {}

        for book_line in book_lines:
            if re.match('^\d*\.', book_line):
                chapter_id += 1
                chapters_lines[chapter_id] = []

            chapters_lines[chapter_id].append(book_line)

        with db.session.no_autoflush:
            for index_chapter, chapter_lines in chapters_lines.items():
                book_chapter = from_chapter_lines(chapter_lines)
                book_chapter.nb = index_book + 1
                book_chapter.nc = index_chapter
                book_chapter.lines = book_chapter.lines
                db.session.add(book_chapter)

    db.session.commit()

    postprocess_book_chapters()

    return get_book_chapters()


def get_book_chapters(nb=None):
    q = db.session.query(BookChapter)
    if nb is not None:
        q = q.filter(BookChapter.nb == nb)
    return q.all()


def write_chapters(book_chapters):
    os.makedirs(os.path.join('generated', 'book_chapters'), exist_ok=True)
    for k, chapter in book_chapters.items():
        os.makedirs(os.path.join('generated', 'chapters', str(k[0])), exist_ok=True)
        with open(os.path.join('generated', 'chapters', str(k[0]), '%d %d' % k), 'w', encoding='utf-8') as chapter_file:
            chapter_file.writelines([l+'\n' for l in chapter.raw])
