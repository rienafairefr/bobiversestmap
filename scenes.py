import os
import json
import string


def read_scenes():
    bob_characters = json.load(open(os.path.join('generated', 'bob_characters.json')))
    characters = bob_characters
    characters.extend(json.load(open(os.path.join('public_data', 'nonbob_characters.json'))))

    characters = {character['id']: character for character in characters}

    chapters_books = json.load(open(os.path.join('generated', 'Combined.json')))

    locations = json.load(open(os.path.join('generated', 'locations.json')))
    scenes_locations = json.load(open(os.path.join('generated', 'scenes_locations.json')))

    def get_index(element):
        try:
            return scenes_locations.index(element)
        except ValueError:
            return len(scenes_locations)

    sorted_locations = sorted(locations, key=get_index)

    index = []
    reverse_index = {}
    i = 0
    for nb, book_chapters in enumerate(chapters_books):
        for nc, book_chapter in enumerate(book_chapters):
            index.append((nb + 1, nc + 1))
            reverse_index[nb + 1, nc + 1] = i
            i = i + 1

    scenes = []
    i = 0
    character_lines = []
    for book_chapters in chapters_books:
        for book_chapter in book_chapters:
            lines = book_chapter['content']
            link = {book_chapter['bob']}
            character_line = {book_chapter['bob']: ['**NAMED CHAPTER**']}
            for line in lines:
                words = line.split()
                words = ["".join(l for l in word if l not in string.punctuation) for word in words]
                for character_id, character in characters.items():
                    names = [character['name']]
                    names.extend(character.get('other_names', []))

                    for name in names:
                        if name in words:
                            character_line.setdefault(character['id'], []).append(line)
                            link.add(character_id)

            # scene_characters = list(characters[character_id] for character_id in link)
            # scenes.append(list(link))

            if type(scenes_locations[i]) == list:
                y = (
                        sorted_locations.index(scenes_locations[i][0]) + sorted_locations.index(
                            scenes_locations[i][1])) / 2
            else:
                y = sorted_locations.index(scenes_locations[i])

            scenes.append({'character_ids': list(link), 'character_line': character_line})

            # {'characters': scene_characters, 'start': book_chapter['date']})
            i = i + 1

    os.makedirs(os.path.join('generated', 'character_lines'), exist_ok=True)
    for character in characters.values():
        filtereds = []
        for i, s in enumerate(scenes):
            if character['id'] not in s['character_ids']:
                continue
            if character['id'] not in s['character_line']:
                continue
            for cline in s['character_line'][character['id']]:
                filtereds.append((character['id'], index[i][0], index[i][1], i, cline))

        open(os.path.join('generated', 'character_lines', '%s' % character['id']), 'w', encoding='utf-8').writelines(
            ['{:^10s} {:3d} {:3d} {:3d} {:s}\n'.format(*f) for f in filtereds])

    # False positive/ negative matches:
    def remove(i, id):
        scenes[i]['character_ids'].remove(id)

    # Tom Hanks in chapter 13
    remove(12,'Tom')
    # Will
    remove(2, 'Riker')
    remove(36, 'Riker')

    thresholds = {
        'Landers': (1, 13),
        'Homer': (2, 28),
        'Moses': (2, 55),
        'Archimedes': (3, 61),
        'Arthur': (1, 43),
        'Bart': (1, 59),
        'Bashful': (1, 30),
        'Bender': (1, 37),
        'Calvin': (1, 40),
        'Stéphane': (2, 67)
    }

    for character_id, tup in thresholds.items():
        # mentioned after last mentions (deaths or otherwise)
        for i, s in enumerate(scenes):
            if index[i] > tup and character_id in s['character_ids']:
                scenes[i]['character_ids'].remove(character_id)



    # 1-39 Bob talking about others
    remove(reverse_index[1, 39], 'Milo')
    remove(reverse_index[1, 39], 'Bill')
    remove(reverse_index[1, 39], 'Mario')

    # mentions
    remove(106, 'Linus')
    remove(181, 'Linus')
    remove(62, 'Bert')
    remove(148, 'Claude')

    # Fred represents 3 different characters
    for i, s in enumerate(scenes):
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
        json.dump(data_scenes, open(os.path.join('generated', 'scenes%s.json' % nb), 'w'), indent=2)

    write_scenes()
    write_scenes(1)
    write_scenes(2)
    write_scenes(3)


if __name__ == '__main__':
    read_scenes()
