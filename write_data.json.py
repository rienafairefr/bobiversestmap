import os
import json

characters = json.load(open(os.path.join('generated', 'bob_characters.json')))
characters.extend(json.load(open(os.path.join('public_data', 'nonbob_characters.json'))))

scenes = json.load(open(os.path.join('generated', 'scenes.json')))

json.dump({'characters': characters, 'scenes': scenes}, open('data.json', 'w'))
