import os
import json


def read_travels():
    chapters_books = json.load(open(os.path.join('generated', 'Combined.json')))

    scenes_locations = json.load(open(os.path.join('generated', 'scenes_locations.json')))

    index = []
    for nb, book_chapters in enumerate(chapters_books):
        for nc, book_chapter in enumerate(book_chapters):
            index.append((nb + 1, nc + 1))

    travels = []
    i = 0
    for nb, book_chapters in enumerate(chapters_books):
        for nc, book_chapter in enumerate(book_chapters):
            travels.append({'bob': book_chapter['bob'], 'location': scenes_locations[i]})
            i=i+1

    def write_travels(nb=None):
        if nb is None:
            nb = ''
            data_travels = travels
        else:
            data_travels = [travels[i] for i, idx in enumerate(index) if idx[0] == nb]

        bobs = list(set(el['bob'] for el in data_travels))

        data_travels_dict = {}
        for bob in bobs:
            data_travels_dict[bob] = []
            current_location = None
            for data_travel in data_travels:
                if data_travel['bob'] == bob:
                    current_location = data_travel['location']
                data_travels_dict[bob].append(current_location)

        json.dump(data_travels_dict, open(os.path.join('generated', 'travels%s.json' % nb), 'w'), indent=2)

    write_travels()
    write_travels(1)
    write_travels(2)
    write_travels(3)


if __name__ == '__main__':
    read_travels()
