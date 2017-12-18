import itertools
import os

from generator.books import get_book_chapters
from generator.chapter_characters import get_chapter_characters
from generator.characters import get_characters_map
from generator.links import get_links
from generator.thresholds import get_thresholds_deaths, get_thresholds_births
from generator.travels import get_travels_book
from generator.utils import json_dump, memoize, sorted_by_key


@memoize()
def get_character_lines():
    chapters_books = get_book_chapters()
    characters_map = get_characters_map()

    character_lines = {}
    for character in characters_map.values():
        character_lines[character['id']] = {}

    for k, book_chapter in chapters_books.items():
        character_lines[book_chapter['bob']][k] = ['**NAMED CHAPTER**']
        chapter_characters = get_chapter_characters(book_chapter)

        for tokenized_sentence in book_chapter['tokenized_content']:
            line = ' '.join(tokenized_sentence)
            for character_pair in itertools.combinations(chapter_characters, 2):
                character0 = character_pair[0]
                character1 = character_pair[1]
                for name0 in character0['all_names']:
                    for name1 in character1['all_names']:
                        if name0 > name1 and name0 in tokenized_sentence and name1 in tokenized_sentence:
                            character_lines[character0['id']].setdefault(k, []).append(line)
                            character_lines[character1['id']].setdefault(k, []).append(line)

    write_characters_lines(character_lines)

    return character_lines


@memoize()
def get_scenes():
    chapters_books = get_book_chapters()
    links = get_links()
    travels = get_travels_book()

    scenes = {}

    for k, book_chapter in chapters_books.items():
        linkset = {book_chapter['bob']}
        for pair in links[k]:
            linkset.add(pair[0]['id'])
            linkset.add(pair[1]['id'])
        scenes[k]={'character_ids':list(linkset)}

    scenes = postprocess(scenes)

    return scenes


def postprocess(scenes):
    # False positive/ negative matches:
    def remove(nb, nc, id):
        try:
            if isinstance(nc, int):
                scenes[nb, nc]['character_ids'].remove(id)
            else:
                for nc_element in nc:
                    scenes[nb, nc_element]['character_ids'].remove(id)
        except ValueError:
            pass

    # Tom Hanks in chapter 13
    remove(1, 13, 'Tom')
    # Will
    remove(1, 3, 'Riker')
    remove(1, 37, 'Riker')

    thresholds_last = {
        'Bart': (1, 59),
        'Bender': (1, 37),
        'Calvin': (1, 40),
        'Verne': (2, 50),
        'Valter': (2, 29),
        'Tom': (1, 60),
        'Marcus': (3, 39),
        'Linus': (2, 34),
        'Khan': (1, 60),
        'Jeffrey': (2, 50),  # ignore the deltan
        'Howard': (3, 62),
        'Goku': (1, 28),
        'Ernie': (1, 61),
        'Bridget': (3, 62),
        'Sam': (2, 8),
        'Doucette': (1, 13)
    }

    thresholds_first = {
        'Archimedes': (1, 30),
        'Bridget': (2, 2)
    }

    thresholds_last.update(get_thresholds_deaths())
    thresholds_first.update(get_thresholds_births())

    for character_id, tup in thresholds_last.items():
        # mentioned after last mentions (deaths or otherwise)
        for k, s in scenes.items():
            if k > tup and character_id in s['character_ids']:
                scenes[k]['character_ids'].remove(character_id)

    # 1-39 Bob talking about others
    remove(1, 39, 'Milo')
    remove(1, 39, 'Bill')
    remove(1, 39, 'Mario')

    # mentions
    # remove(106, 'Linus')
    # remove(181, 'Linus')
    # remove(62, 'Bert')
    # remove(148, 'Claude')

    # mentions
    remove(2, 14, 'Ralph')  # talk about sending him a missive
    remove(2, 77, 'Oliver')  # talk about him building a fleet
    remove(3, 15, 'Oliver')  # same

    remove(3, 68, 'Neil')  # same

    remove(2, [16, 30, 38, 39, 52, 54, 55, 60, 64], 'Mario')
    remove(3, [17, 33, 38, 70, 71], 'Mario')

    remove(3, [25, 75], 'Mack')

    remove(3, 73, 'Luke')
    remove(2, [17, 22, 24], 'Luke')

    remove(2, [52, 56], 'Loki')

    remove(2, 7, 'Julia')  # in stasis

    remove(2, [50, 60, 72], "Jacques")

    remove(3, [71, 73], "Icarus")

    remove(2, [33, 52, 61], "Howard")
    remove(3, [16, 18, 39], "Howard")

    remove(2, [12, 18, 26], "Homer")

    remove(2, 42, "Henry")

    remove(2, 55, "Hal")

    remove(1, 22, "Goku")
    remove(3, 39, "Goku")

    remove(2, 53, "Garfield")
    remove(3, 39, "Garfield")

    remove(3, 45, "Ferb")

    remove(2, 15, "Dopey")

    remove(3, [18, 51], "Dexter")

    remove(3, [11, 71], "Daedalus")

    remove(3, 11, "Claude")

    remove(1, 47, "Charles")
    remove(2, 14, "Charles")  # talk about sending him a missive

    remove(1, [22, 40], "Calvin")

    remove(3, [73, 57, 60, 54, 55, 51, 47, 45, 44, 41, 39, 35, 33, 30, 21, 18, 15, 14, 13, 8, 4], "Bob")
    remove(2, [77, 72, 70, 67, 63, 59, 52, 51, 50, 48, 46, 42, 39, 34, 32, 31, 30, 28, 20, 18, 15, 13, 10, 7, 5], "Bob")
    remove(1, [60, 58, 57, 54, 49, 47, 45, 42, 40, 38, 34, 32, 29, 25, 24, 22, 21, 20, 18], "Bob")

    remove(1, [19, 21, 23, 24, 26, 27, 28, 40, 46, 47, 53, 57, 58], "Bill")
    remove(2, [1, 2, 4, 10, 13, 14, 17, 19, 20, 27, 38, 41, 48, 49, 50, 53, 58, 65, 68, 73], "Bill")
    remove(3, [16, 18, 22, 24, 26, 31, 38, 39, 41, 45, 48, 67, 74, 75], "Bill")

    remove(2, 2, 'Bert')
    remove(2, 15, 'Bashful')

    remove(1, range(1, 44), 'Archimedes')  # remove instances before first contact with Archimedes

    # Fred represents 3 different characters
    for (nb, nc), s in scenes.items():
        if 'Fred' in scenes[nb, nc]['character_ids']:
            # the Bob clone in book1
            if nb == 1:
                remove(nb, nc, 'Fred_Deltan')
            remove(nb, nc, 'Fred_Carleon')
            # the deltan hunter
            if nb == 2:
                remove(nb, nc, 'Fred')
            remove(nb, nc, 'Fred_Carleon')
            # the foe from Carleon
            if nb == 3:
                remove(nb, nc, 'Fred')
            remove(nb, nc, 'Fred_Deltan')

    remove(3, 40, "Fred_Carleon")

    remove(1, 54, 'Sam')
    remove(2, 2, 'Sam')
    remove(2, 7, 'Sam')

    return scenes


def write_characters_lines(scenes):
    characters_map = get_characters_map()

    for character in characters_map.values():
        os.makedirs(os.path.join('generated', character['id']), exist_ok=True)
        with open(os.path.join('generated', character['id'], 'lines'), 'w', encoding='utf-8') as lines_file:
            for (nb, nc), s in sorted_by_key(scenes).items():
                if character['id'] not in s['character_ids']:
                    continue
                if character['id'] not in s['character_line']:
                    continue
                for cline in s['character_line'][character['id']]:
                    lines_file.write('{:^10s} {:3d} {:3d} {:s}\n'.format(character['id'], nb, nc, cline))


def get_scenes_books(nb=None):
    return sorted_by_key({k: v for k, v in get_scenes().items() if nb is None or k[0] == nb})


def write_scenes():
    def write_scenes_(nb=None):
        json_dump(list(get_scenes_books(nb).values()), open(os.path.join('generated', 'scenes%s.json' % nb), 'w'))

    write_scenes_()
    write_scenes_(1)
    write_scenes_(2)
    write_scenes_(3)


if __name__ == '__main__':
    write_scenes()
