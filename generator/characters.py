import json
import os

import colorcet as cc

from generator.utils import json_dump, memoize, sorted_by_key, JsonSerializable


class Character(JsonSerializable):
    def __init__(self, id, name, affiliation=None, other_names=None):
        self.id = id
        self.name = name
        self.affiliation = affiliation
        self.other_names = [] if other_names is None else other_names

    def __repr__(self):
        return '[%s %s %s]' % (self.id, self.name, ','.join(self.other_names))

    @property
    def all_names(self):
        return_value = [self.name]
        return_value.extend(self.other_names)
        return return_value


@memoize()
def get_bob_characters():
    with open(os.path.join('public_data', 'genealogy.txt')) as genealogy:
        lines = genealogy.readlines()

    bob_characters = []
    for line in lines:
        stripped = line.strip().split(';')[0]
        if len(stripped) == 0:
            continue

        bob = [el.strip() for el in stripped.split(':')]

        char = Character(bob[-1], name=bob[-1])
        if len(bob) != 1:
            char.affiliation = bob[-2]
        else:
            char.affiliation = bob[-1]

        if char.id == 'Riker':
            char.other_names = ['Will', 'William']
        if char.id == 'Arthur':
            char.other_names = ['Eeyore']
        if char.id == 'Sam':
            char.other_names = ['Exodus-3']
        if char.id == 'Dexter':
            char.other_names = ['Dex']
        if char.id == 'Daedalus':
            char.other_names = ['Dae']
        bob_characters.append(char)

    return bob_characters


def is_bob(character_id):
    return character_id in [el.id for el in get_bob_characters()]


@memoize()
def get_characters():
    characters = list(get_bob_characters())  # copy
    nonbobs = json.load(open(os.path.join('public_data', 'nonbob_characters.json')))
    characters.extend([Character(**nonbob) for nonbob in nonbobs])
    return characters


@memoize()
def get_characters_map():
    return sorted_by_key({character.id: character for character in get_characters()})


@memoize()
def get_bob_styles():
    bob_characters = get_bob_characters()
    styles = ''
    for i, bob_character in enumerate(bob_characters):
        template = 'path.%s {stroke: %s;}\n'

        styles += template % (bob_character.id, cc.colorwheel[int(256 * i / len(bob_characters))])
    return styles


def write_genealogy():
    bob_characters = get_bob_characters()
    json_dump(bob_characters, os.path.join('generated', 'bob_characters.json'))


def write_bob_styles():
    with open(os.path.join('css', 'bob_styles.css'), 'w') as css:
        css.write(get_bob_styles())


if __name__ == '__main__':
    write_genealogy()
    write_bob_styles()
