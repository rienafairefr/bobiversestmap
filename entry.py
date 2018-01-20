from sqlalchemy import inspect

from app import db
from generator.books import import_book_chapters, get_books
from generator.chapter_characters import get_chapter_characters, import_chapter_characters
from generator.characters import import_characters
from generator.locations import import_locations
from generator.models.books import Book, BookLine
from generator.scenes_locations import treat_scenes_locations
from generator.stars import import_stars
from generator.thresholds import import_thresholds
from generator.timeline import import_timeline_descriptions


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
    locations = import_locations()
    characters = import_characters()
    book_chapters = import_book_chapters(books)
    import_thresholds()
    treat_scenes_locations(book_chapters)
    import_timeline_descriptions()
    import_chapter_characters(book_chapters, characters)
