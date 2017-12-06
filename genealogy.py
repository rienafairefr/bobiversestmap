import json
import os

with open(os.path.join('public_data', 'genealogy.txt')) as genealogy:
    lines = genealogy.readlines()

bob_characters = []
for line in lines:
    bob = line.strip().split(':')

    char = {'id': bob[-1], 'name': bob[-1]}
    if len(bob) != 1:
        char['affiliation'] = bob[-2]
    else:
        char['affiliation'] = bob[-1]
    bob_characters.append(char)

json.dump(bob_characters, open(os.path.join('generated', 'bob_characters.json'), 'w'), indent=2)
