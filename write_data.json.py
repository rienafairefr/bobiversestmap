import os
import json

characters = json.load(open(os.path.join('generated', 'bob_characters.json')))
characters.extend(json.load(open(os.path.join('public_data', 'nonbob_characters.json'))))

scenes = json.load(open(os.path.join('generated', 'scenes.json')))
locations = json.load(open(os.path.join('generated', 'locations.json')))

data = dict(characters=characters,
            scenes=scenes,
            locations=locations)

json.dump(data, open('data.json', 'w'), indent=2)
