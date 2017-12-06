import os
import json

characters = json.load(open(os.path.join('generated', 'bob_characters.json')))
characters.extend(json.load(open(os.path.join('public_data', 'nonbob_characters.json'))))

chapters_books = json.load(open(os.path.join('generated', 'Combined.json')))

scenes = []
locations = []
for nb, book_chapters in enumerate(chapters_books):
    for nc, book_chapter in enumerate(book_chapters):
        lines = book_chapter['content']
        link = {book_chapter['bob']}
        for line in lines:
            for character in characters:
                if character['name'] in line.split():
                    link.add(character['id'])

        scenes.append(list(link))
        locations.append(book_chapter['location'])

# Removing, false positive matches:

# Tom Hanks in chapter 13
scenes[12].remove('Tom')


def treat_location(location):
    if location == '---':
        # first chapters in book 1
        return 'Earth'
    if 'Poseidon' in location:
        return 'Poseidon'
    if location == 'En Route':
        return 'Earth -> Epsilon Eridani'
    if location == 'En Route to GL 54':
        return 'GL 877 -> GL 54'
    return location

locations = list(map(treat_location, locations))

# Howard moving on
locations[118] = 'Vulcan -> HIP 14101'
# Icarus & Deadalus
locations[154] = 'Epsilon Eridani -> '
# Neil & Herschel
locations[159] = 'Delta Pavonis'
locations[161] = 'Delta Pavonis'
# Bob on Eden
locations[171] = 'Eden'

# Neil & Herschel moving the Bellerophon
locations[175] = 'Delta Pavonis -> Sol'

# Icarus & Deadalus
locations[180] = 'Epsilon Indi -> '

# Icarus & Deadalus destroying GL877
locations[207] = 'GL 877'

json.dump(scenes, open(os.path.join('generated', 'scenes.json'), 'w'), indent=2)
json.dump(locations, open(os.path.join('generated', 'locations.json'), 'w'), indent=2)

