import os
import string
from collections import OrderedDict

import itertools

from genealogy import get_characters, get_characters_map
from locations import get_locations
from readcombined import get_index, get_book_chapters
from scenes_locations import get_scenes_locations
from utils import json_dump, memoize


@memoize()
def get_scenes():
    characters_map = get_characters_map()
    characters = get_characters()

    chapters_books = get_book_chapters()

    locations = get_locations()
    scenes_locations = get_scenes_locations()

    def get_index(element):
        try:
            return scenes_locations.index(element)
        except ValueError:
            return len(scenes_locations)

    sorted_locations = sorted(locations, key=get_index)

    index = []
    reverse_index = {}
    i = 0
    for nb, book_chapters in enumerate(chapters_books):
        for nc, book_chapter in enumerate(book_chapters):
            index.append((nb + 1, nc + 1))
            reverse_index[nb + 1, nc + 1] = i
            i = i + 1

    scenes = []
    i = 0
    for book_chapters in chapters_books:
        for book_chapter in book_chapters:
            lines = book_chapter['content']

            link = {book_chapter['bob']}
            if False:
                for tokenized_sentence in book_chapter['tokenized_content']:
                    for character_pair in itertools.combinations([char for char in characters if char in tokenized_sentence], 2):
                        for name0 in character_pair[0]['all_names']:
                            for name1 in character_pair[1]['all_names']:
                                if name0 in tokenized_sentence and name1 in tokenized_sentence:
                                    link.update(character_pair)


            character_line = {book_chapter['bob']: ['**NAMED CHAPTER**']}
            for line in lines:
                words = line.split()
                words = ["".join(l for l in word if l not in string.punctuation) for word in words]
                for character_id, character in characters_map.items():
                    names = character['all_names']

                    for name in names:
                        if name in words:
                            character_line.setdefault(character['id'], []).append(line)
                            link.add(character_id)

            # scene_characters = list(characters[character_id] for character_id in link)
            # scenes.append(list(link))

            if type(scenes_locations[i]) == list:
                y = (
                        sorted_locations.index(scenes_locations[i][0]) + sorted_locations.index(
                            scenes_locations[i][1])) / 2
            else:
                y = sorted_locations.index(scenes_locations[i])

            scenes.append(OrderedDict({'character_ids': list(link), 'character_line': character_line}))

            # {'characters': scene_characters, 'start': book_chapter['date']})
            i = i + 1

    os.makedirs(os.path.join('generated', 'character_lines'), exist_ok=True)
    for character in characters_map.values():
        filtereds = []
        for i, s in enumerate(scenes):
            if character['id'] not in s['character_ids']:
                continue
            if character['id'] not in s['character_line']:
                continue
            for cline in s['character_line'][character['id']]:
                filtereds.append((character['id'], index[i][0], index[i][1], i, cline))

        open(os.path.join('generated', 'character_lines', '%s' % character['id']), 'w', encoding='utf-8').writelines(
            ['{:^10s} {:3d} {:3d} {:3d} {:s}\n'.format(*f) for f in filtereds])

    # False positive/ negative matches:
    def remove(i, id):
        try:
            scenes[i]['character_ids'].remove(id)
        except ValueError:
            # already removed
            pass

    # Tom Hanks in chapter 13
    remove(12,'Tom')
    # Will
    remove(2, 'Riker')
    remove(36, 'Riker')

    thresholds = {
        'Landers': (1, 13),
        'Homer': (2, 28),
        'Moses': (2, 55),
        'Archimedes': (3, 61),
        'Arthur': (1, 43),
        'Bart': (1, 59),
        'Bashful': (1, 30),
        'Bender': (1, 37),
        'Calvin': (1, 40),
        'Stéphane': (2, 67)
    }

    for character_id, tup in thresholds.items():
        # mentioned after last mentions (deaths or otherwise)
        for i, s in enumerate(scenes):
            if index[i] > tup and character_id in s['character_ids']:
                scenes[i]['character_ids'].remove(character_id)



    # 1-39 Bob talking about others
    remove(reverse_index[1, 39], 'Milo')
    remove(reverse_index[1, 39], 'Bill')
    remove(reverse_index[1, 39], 'Mario')

    # mentions
    remove(106, 'Linus')
    remove(181, 'Linus')
    remove(62, 'Bert')
    remove(148, 'Claude')

    # Fred represents 3 different characters
    for i, s in enumerate(scenes):
        ids = scenes[i]['character_ids']

        if 'Fred' in ids:
            # the Bob clone
            if index[i][0] == 1:
                remove(i, 'Fred_Deltan')
                remove(i, 'Fred_Carleon')
            # the deltan hunter
            if index[i][0] == 2:
                remove(i, 'Fred')
                remove(i, 'Fred_Carleon')
            # the foe from Carleon
            if index[i][0] == 3:
                remove(i, 'Fred')
                remove(i, 'Fred_Deltan')

    return scenes


def get_scenes_books(nb=None):
    scenes = get_scenes()
    index = get_index()
    if nb is None:
        data_scenes = get_scenes()
    else:
        data_scenes = [scenes[i] for i, idx in enumerate(index) if idx[0] == nb]
    return data_scenes


def write_scenes():
    def write_scenes_(nb=None):
        json_dump(get_scenes_books(nb), os.path.join('generated', 'scenes%s.json' % ('' if nb is None else nb)))

    write_scenes_()
    write_scenes_(1)
    write_scenes_(2)
    write_scenes_(3)


if __name__ == '__main__':
    write_scenes()
