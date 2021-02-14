from app import db
from generator.models import Book


def import_books(path):
    with open(path, encoding="utf-8") as combined:
        content = combined.readlines()

    book_id = 0
    book_lines = {}
    for line in content:
        if line.startswith("##"):
            book_id += 1
            book_lines[book_id] = []
        else:
            book_lines[book_id].append(line.strip())

    for book_id, book_lines in book_lines.items():
        book = Book(id=book_id, lines=book_lines)

        db.session.add(book)
    db.session.commit()


def get_books():
    return Book.query.all()
