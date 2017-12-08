import json
import os

import colorcet as cc

from utils import json_dump, memoize


@memoize()
def get_genealogy():
    with open(os.path.join('public_data', 'genealogy.txt')) as genealogy:
        lines = genealogy.readlines()

    bob_characters = []
    for line in lines:
        stripped = line.strip().split(';')[0]
        if len(stripped) == 0:
            continue

        bob = stripped.split(':')

        char = {'id': bob[-1], 'name': bob[-1]}
        if len(bob) != 1:
            char['affiliation'] = bob[-2]
        else:
            char['affiliation'] = bob[-1]
        char['level'] = len(bob)
        if char['id'] == 'Riker':
            char['other_names'] = ['Will', 'William']
        bob_characters.append(char)

    return bob_characters


@memoize()
def get_characters():
    characters = get_genealogy()
    characters.extend(json.load(open(os.path.join('public_data', 'nonbob_characters.json'))))
    return characters


@memoize()
def get_characters_map():
    return {character['id']: character for character in get_characters()}


@memoize()
def get_bob_styles():
    bob_characters = get_genealogy()
    styles = ''
    for i, bob_character in enumerate(bob_characters):
        template = 'path.%s {stroke: %s;}\n'

        styles += template % (bob_character['id'], cc.colorwheel[int(256 * i / len(bob_characters))])
    return styles


def write_genealogy():
    bob_characters = get_genealogy()
    json_dump(bob_characters, open(os.path.join('generated', 'bob_characters.json'), 'w'))


def write_bob_styles():
    with open(os.path.join('css', 'bob_styles.css'), 'w') as css:
        css.write(get_bob_styles())


if __name__ == '__main__':
    write_genealogy()
    write_bob_styles()
