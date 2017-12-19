from generator.books import get_book_chapters
from generator.characters import get_characters_map
from generator.utils import memoize


@memoize()
def get_chapter_characters(k):
    chapters_books = get_book_chapters()
    book_chapter = chapters_books[k]
    all_lines = '\n'.join(book_chapter['content'])
    characters_map = get_characters_map()
    chapter_characters = list(characters_map.values())

    chapter_characters = {character for character in chapter_characters if
                          any(name in all_lines for name in character.all_names)}

    if 'I' in all_lines:
        chapter_characters.add(characters_map[book_chapter['bob']])

    return list(chapter_characters)
