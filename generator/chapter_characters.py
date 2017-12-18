from generator.characters import get_characters_map
from generator.utils import memoize


@memoize()
def get_chapter_characters(book_chapter):
    lines = book_chapter['content']
    all_lines = '\n'.join(lines)
    characters_map = get_characters_map()
    chapter_characters = list(characters_map.values())
    chapter_characters.append({'id': book_chapter['bob'], 'all_names': ['I']})

    chapter_characters = [character for character in chapter_characters if
                          any(name in all_lines for name in character['all_names'])]
    return chapter_characters