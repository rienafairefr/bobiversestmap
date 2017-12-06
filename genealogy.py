import json
import os


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
        bob_characters.append(char)

    json.dump(bob_characters, open(os.path.join('generated', 'bob_characters.json'), 'w'), indent=2)


if __name__ == '__main__':
    read_genealogy()