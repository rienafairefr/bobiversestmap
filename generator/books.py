import os
import re

from app import db
from generator.chapter_characters import treat_one_chapters_characters
from generator.dates import treat_one_period
from generator.models.books import Book
from generator.models.chapters import BookChapter
from generator.nl import sentences_tokenize, word_tokenize_sentences


def get_books():
    return [book.lines for book in Book.query.all()]


chapter_re = re.compile('^(\d*)\.(.*)$')


def from_chapter(chapter):
    obj = BookChapter()
    obj.bob_id = chapter[1].content
    obj.period = treat_one_period(chapter[2].content)
    obj.location_id = chapter[3].content

    obj.lines = chapter[4:]

    content = [line.content for line in obj.lines]
    sentences = list(sentences_tokenize(content))
    obj.tokenized_content = list(word_tokenize_sentences(sentences))

    return obj


def import_book_chapters(books=None):
    if books is None:
        books = get_books()

    book_chapters = {}
    for index_book, book_lines in enumerate(books):
        chapter = []
        index_chapter = 0

        def create(idx, chapter):
            with db.session.no_autoflush:
                book_chapter = from_chapter(chapter)
                book_chapter.nb = index_book + 1
                book_chapter.nc = idx + 1
                book_chapter.lines = book_chapter.lines
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

    book_chapters = list(book_chapters.values())

    db.session.add_all(book_chapters)
    db.session.commit()
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
