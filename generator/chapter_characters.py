from app import db
from generator.books import get_book_chapters
from generator.characters import get_characters
from generator.models.chapter_characters import ChaptersCharacters
from generator.models.chapters import BookChapter


def import_chapter_characters(book_chapters=None, characters=None):
    if book_chapters is None:
        book_chapters = get_book_chapters()
    if characters is None:
        characters = get_characters()

    for k, book_chapter in book_chapters.items():
        for character in characters:
            for name in character.all_names:
                if name in book_chapter.all_lines:
                    db.session.add(ChaptersCharacters(character=character,chapter=book_chapter))
    db.session.commit()


def get_chapter_characters(k):
    return db.session.query(BookChapter).get(k).characters
