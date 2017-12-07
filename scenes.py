import os
import json


def read_scenes():
    characters = json.load(open(os.path.join('generated', 'bob_characters.json')))
    characters.extend(json.load(open(os.path.join('public_data', 'nonbob_characters.json'))))

    characters = {character['id']: character for character in characters}

    chapters_books = json.load(open(os.path.join('generated', 'Combined.json')))

    locations = json.load(open(os.path.join('generated', 'locations.json')))
    scenes_locations = json.load(open(os.path.join('generated', 'scenes_locations.json')))

    sorted_locations = sorted(locations, key=scenes_locations.index)

    index = []
    for nb, book_chapters in enumerate(chapters_books):
        for nc, book_chapter in enumerate(book_chapters):
            index.append((nb + 1, nc + 1))

    scenes = []
    i=0
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

            if type(scenes_locations[i])==list:
                y = (sorted_locations.index(scenes_locations[i][0])+sorted_locations.index(scenes_locations[i][1]))/2
            else:
                y = sorted_locations.index(scenes_locations[i])

            scenes.append({'character_ids': list(link)})
            # {'characters': scene_characters, 'start': book_chapter['date']})
            i = i +1

    # Removing, false positive matches:

    # Tom Hanks in chapter 13
    scenes[12]['character_ids'].remove('Tom')

    # Dr. Landers mentioned after his death
    for i, s in enumerate(scenes):
        if index[i] > (1, 13) and 'Landers' in s['character_ids']:
            scenes[i]['character_ids'].remove('Landers')

    # Homer mentioned after his death
    for i, s in enumerate(scenes):
        if index[i] > (2, 28) and 'Homer' in s['character_ids']:
            scenes[i]['character_ids'].remove('Homer')

    # Fred represents 3 different characters
    for i,s in enumerate(scenes):
        ids = scenes[i]['character_ids']

        if 'Fred' in ids:
            # the Bob clone
            if index[i][0] == 1:
                ids.remove('Fred_Deltan')
                ids.remove('Fred_Carleon')
            # the deltan hunter
            if index[i][0] == 2:
                ids.remove('Fred')
                ids.remove('Fred_Carleon')
            # the foe from Carleon
            if index[i][0] == 3:
                ids.remove('Fred')
                ids.remove('Fred_Deltan')

        scenes[i]['character_ids'] = ids

    # scenes_dates = json.load(open(os.path.join('generated', 'scenes_dates.json')))

    # for i,s in enumerate(scenes):
    #    scenes[i].update(scenes_dates[i])

    def write_scenes(nb=None):
        if nb is None:
            nb = ''
            data_scenes = scenes
        else:
            data_scenes = [scenes[i] for i, idx in enumerate(index) if idx[0] == nb]
        json.dump(data_scenes, open(os.path.join('generated', 'scenes%s.json'%nb), 'w'), indent=2)

    write_scenes()
    write_scenes(1)
    write_scenes(2)
    write_scenes(3)


if __name__ == '__main__':
    read_scenes()
