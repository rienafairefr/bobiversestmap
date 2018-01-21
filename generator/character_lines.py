import itertools
import os

from generator.books import get_book_chapters
from generator.chapter_characters import get_chapter_characters
from generator.characters import get_characters_map, get_characters
from generator.utils import sorted_by_key


def import_character_lines(book_chapters=None, characters=None):
    if book_chapters is None:
        book_chapters = get_book_chapters()
    if characters is None:
        characters = get_characters()

    character_lines = {}
    for character in characters:
        character_lines[character.id] = {}

    for k, book_chapter in book_chapters.items():
        character_lines[book_chapter.bob][k] = ['**NAMED CHAPTER**']
        chapter_characters = get_chapter_characters(k)

        for tokenized_sentence in book_chapter.tokenized_content:
            line = ' '.join(tokenized_sentence)
            for character_pair in itertools.combinations(chapter_characters, 2):
                character0 = character_pair[0]
                character1 = character_pair[1]
                for name0 in character0.all_names:
                    for name1 in character1.all_names:
                        if name0 > name1 and name0 in tokenized_sentence and name1 in tokenized_sentence:
                            character_lines[character0.id].setdefault(k, []).append(line)
                            character_lines[character1.id].setdefault(k, []).append(line)

    write_characters_lines(character_lines)

    return character_lines



def write_characters_lines(scenes):
    characters_map = get_characters_map()

    for character in characters_map.values():
        os.makedirs(os.path.join('generated', character.id), exist_ok=True)
        with open(os.path.join('generated', character.id, 'lines'), 'w', encoding='utf-8') as lines_file:
            for (nb, nc), s in sorted_by_key(scenes).items():
                if character.id not in s['character_ids']:
                    continue
                if character.id not in s['character_line']:
                    continue
                for cline in s['character_line'][character.id]:
                    lines_file.write('{:^10s} {:3d} {:3d} {:s}\n'.format(character.id, nb, nc, cline))

