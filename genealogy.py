import json
import os

import colorcet as cc


def read_genealogy():
    with open(os.path.join('public_data', 'genealogy.txt')) as genealogy:
        lines = genealogy.readlines()

    bob_characters = []
    for line in lines:
        stripped = line.strip().split(';')[0]
        if len(stripped)==0:
            continue

        bob = stripped.split(':')

        char = {'id': bob[-1], 'name': bob[-1]}
        if len(bob) != 1:
            char['affiliation'] = bob[-2]
        else:
            char['affiliation'] = bob[-1]
        char['level'] = len(bob)
        bob_characters.append(char)

    json.dump(bob_characters, open(os.path.join('generated', 'bob_characters.json'), 'w'), indent=2)

    with open(os.path.join('css', 'bob_styles.css'),'w') as css:
        for i, bob_character in enumerate(bob_characters):
            template = 'path.%s {stroke: %s;}\n'

            css.write(template % (bob_character['id'], cc.colorwheel[int(256 * i/len(bob_characters))]))



if __name__ == '__main__':
    read_genealogy()