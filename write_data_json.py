import os
import json


def write_data_json(nb=None):
    if nb is None:
        nb=''

    characters = json.load(open(os.path.join('generated', 'bob_characters.json')))
    characters.extend(json.load(open(os.path.join('public_data', 'nonbob_characters.json'))))

    scenes = json.load(open(os.path.join('generated', 'scenes%s.json'%nb)))
    scenes_locations = json.load(open(os.path.join('generated', 'scenes_locations%s.json'%nb)))

    data = dict(characters=characters,
                scenes=scenes,
                scenes_locations=scenes_locations)

    json.dump(data, open('data%s.json' % nb, 'w'), indent=2)


if __name__ == '__main__':
    write_data_json()
