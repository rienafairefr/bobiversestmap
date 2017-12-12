import os
import string
from collections import OrderedDict

from enum import Enum
from genealogy import get_characters_map
from readcombined import get_book_chapters
from scenes_locations import get_scenes_locations, get_sorted_locations
from utils import json_dump, memoize

class RelationShipParsingType(Enum):
    TOKENIZED_SAME_SENTENCE = 1
    NAME_IN_WORDS = 2


@memoize()
def get_scenes(parsingtype=RelationShipParsingType.TOKENIZED_SAME_SENTENCE):
    characters_map = get_characters_map()
    chapters_books = get_book_chapters()
    sorted_locations = get_sorted_locations()
    scenes_locations = get_scenes_locations()

    scenes = OrderedDict()
    for k, book_chapter in chapters_books.items():
        lines = book_chapter['content']
        link = {book_chapter['bob']}
        character_line = {book_chapter['bob']: ['**NAMED CHAPTER**']}
        for line in lines:
            words = line.split()
            words = ["".join(l for l in word if l not in string.punctuation) for word in words]
            for character_id, character in characters_map.items():
                names = [character['name']]
                names.extend(character.get('other_names', []))

                for name in names:
                    if name in words:
                        character_line.setdefault(character['id'], []).append(line)
                        link.add(character_id)

        # scene_characters = list(characters[character_id] for character_id in link)
        # scenes.append(list(link))

     #   if type(scenes_locations[k]) == list:
    #        y = (
   #                 sorted_locations.index(scenes_locations[k][0]) + sorted_locations.index(
  #                      scenes_locations[k][1])) / 2
 #       else:
#            y = sorted_locations.index(scenes_locations[k])

        scenes[k] = OrderedDict({'character_ids': list(link), 'character_line': character_line})

        # {'characters': scene_characters, 'start': book_chapter['date']})

    os.makedirs(os.path.join('generated', 'character_lines'), exist_ok=True)
    for character in characters_map.values():
        filtereds = []
        for (nb, nc), s in scenes.items():
            if character['id'] not in s['character_ids']:
                continue
            if character['id'] not in s['character_line']:
                continue
            for cline in s['character_line'][character['id']]:
                filtereds.append((character['id'], nb, nc, cline))

        open(os.path.join('generated', 'character_lines', '%s' % character['id']), 'w', encoding='utf-8').writelines(
            ['{:^10s} {:3d} {:3d} {:s}\n'.format(*f) for f in filtereds])

    # False positive/ negative matches:
    def remove(nb, nc, id):
        scenes[nb, nc]['character_ids'].remove(id)

    # Tom Hanks in chapter 13
    remove(1, 13, 'Tom')
    # Will
    remove(1, 3, 'Riker')
    remove(1, 37, 'Riker')

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
        for k, s in scenes.items():
            if k > tup and character_id in s['character_ids']:
                scenes[k]['character_ids'].remove(character_id)



    # 1-39 Bob talking about others
    remove(1, 39, 'Milo')
    remove(1, 39, 'Bill')
    remove(1, 39, 'Mario')

    # mentions
    #remove(106, 'Linus')
    #remove(181, 'Linus')
    #remove(62, 'Bert')
    #remove(148, 'Claude')

    # Fred represents 3 different characters
    for k, s in scenes.items():
        if 'Fred' in scenes[k]['character_ids']:
            # the Bob clone
            if k[0] == 1:
                remove(*k, 'Fred_Deltan')
                remove(*k, 'Fred_Carleon')
            # the deltan hunter
            if k[0] == 2:
                remove(*k, 'Fred')
                remove(*k, 'Fred_Carleon')
            # the foe from Carleon
            if k[0] == 3:
                remove(*k, 'Fred')
                remove(*k, 'Fred_Deltan')

    return scenes


def get_scenes_books(nb=None):
    return OrderedDict({k: v for k, v in get_scenes().items() if nb is None or k[0] == nb})


def write_scenes():
    def write_scenes_(nb=None):
        json_dump(list(get_scenes_books(nb).values()), open(os.path.join('generated', 'scenes%s.json' % nb), 'w'))

    write_scenes_()
    write_scenes_(1)
    write_scenes_(2)
    write_scenes_(3)


if __name__ == '__main__':
    write_scenes()
