from sqlalchemy import inspect

from app import db
from generator.books import import_book_chapters, get_books
from generator.chapter_characters import postprocess_chapter_characters
from generator.chapters_locations import psotprocess_chapters_locations
from generator.characters import import_characters
from generator.dates import postprocess_dates
from generator.links import treat_scut_links, postprocess_links
from generator.locations import import_locations
from generator.models.books import Book, BookLine
from generator.stars import import_stars, import_starsmap
from generator.thresholds import import_thresholds
from generator.timeline import import_timeline_descriptions
from generator.travels import get_travels, import_chapter_characters_travels, postprocess_character_travels, \
    write_travels


def import_books(path):
    with open(path, encoding='utf-8') as combined:
        content = combined.readlines()

    book = Book(id=0)

    book_lines = []
    for line in content:
        if line.startswith('##'):
            book = Book(id=book.id + 1)
            db.session.add(book)
            db.session.flush()
        else:
            book_lines.append({'content': line.strip(), 'book_id': book.id})

    db.session.add(book)
    mapper = inspect(BookLine)
    db.session.bulk_insert_mappings(mapper, book_lines)
    db.session.commit()
    return get_books()


def import_combined(path):
    books = import_books(path)
    stars = import_stars()
    import_starsmap()
    locations = import_locations()
    characters = import_characters()
    book_chapters = import_book_chapters(books)
    import_chapter_characters_travels(book_chapters)

    postprocess_dates()
    postprocess_chapter_characters(book_chapters)
    postprocess_links()

    import_thresholds()
    psotprocess_chapters_locations()
    import_timeline_descriptions()
    travels = get_travels()
    treat_scut_links()
