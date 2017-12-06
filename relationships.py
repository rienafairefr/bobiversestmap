import os
import json

characters = json.load(open(os.path.join('generated', 'bob_characters.json')))
characters.extend(json.load(open(os.path.join('public_data', 'nonbob_characters.json'))))

characters = {character['id']: character for character in characters}

chapters_books = json.load(open(os.path.join('generated', 'Combined.json')))

locations = json.load(open(os.path.join('generated', 'locations.json')))

scenes = []
scenes_locations = []
for nb, book_chapters in enumerate(chapters_books):
    for nc, book_chapter in enumerate(book_chapters):
        lines = book_chapter['content']
        link = {book_chapter['bob']}
        for line in lines:
            words = line.split()
            for character_id, character in characters.items():
                if character['name'] in words:
                    link.add(character['id'])
                if 'other_names' in character:
                    for name in character['other_names']:
                        if name in words:
                            link.add(character_id)

        # scene_characters = list(characters[character_id] for character_id in link)
        # scenes.append(list(link))

        scenes.append({'character_ids': list(link)})
        # {'characters': scene_characters, 'start': book_chapter['date']})
        scenes_locations.append(book_chapter['location'])

# Removing, false positive matches:

# Tom Hanks in chapter 13
scenes[12]['character_ids'].remove('Tom')

# Dr Landers mentions after his death
for i, s in enumerate(scenes):
    if i > 13 and 'Landers' in s['character_ids']:
        scenes[i]['character_ids'].remove('Landers')

# Bob on Earth
for i in range(0, 12):
    scenes_locations[i] = 'Earth'

# Bob first voyage
scenes_locations[12] = 'Earth -> Epsilon Eridani'

# Mulder in Poseidon
scenes_locations[109] = 'Poseidon'

# Hal going to GL 54
scenes_locations[114] = 'GL 877 -> GL 54'

# Howard moving on
scenes_locations[118] = 'Vulcan -> HIP 14101'

# Mulder Leaving Poseidon
scenes_locations[122] = 'Poseidon'

# Icarus & Deadalus
scenes_locations[154] = 'Epsilon Eridani -> '
# Neil & Herschel
scenes_locations[159] = 'Delta Pavonis'
scenes_locations[161] = 'Delta Pavonis'
# Bob on Eden
scenes_locations[171] = 'Eden'

# Neil & Herschel moving the Bellerophon
scenes_locations[175] = 'Delta Pavonis -> Sol'

# Icarus & Deadalus
scenes_locations[180] = 'Epsilon Indi -> '

# Icarus & Deadalus destroying GL877
scenes_locations[207] = 'GL 877'

# scenes_dates = json.load(open(os.path.join('generated', 'scenes_dates.json')))

# for i,s in enumerate(scenes):
#    scenes[i].update(scenes_dates[i])

json.dump(scenes, open(os.path.join('generated', 'scenes.json'), 'w'), indent=2)


def treat_one_scene_location(scene_location):
    for location in locations:
        if ('city' in location and location['city'] == scene_location) \
                or ('planet' in location and location['planet'] == scene_location) \
                or ('star' in location and location['star'] == scene_location):
            return location


def treat_scene_location(scene_location):
    treat_one = treat_one_scene_location(scene_location)
    if treat_one:
        return treat_one

    places = [el.strip() for el in scene_location.split('->')]
    return list(map(treat_one_scene_location, places))


scenes_locations = list(map(treat_scene_location, scenes_locations))

json.dump(scenes_locations, open(os.path.join('generated', 'scenes_locations.json'), 'w'), indent=2)
