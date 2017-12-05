import os
import json

characters = json.load(open(os.path.join('generated', 'bob_characters.json')))
characters.extend(json.load(open(os.path.join('public_data', 'nonbob_characters.json'))))

chapters_books = json.load(open(os.path.join('generated', 'Combined.json')))

scenes = []
for nb, book_chapters in enumerate(chapters_books):
    for nc, book_chapter in enumerate(book_chapters):
        lines = book_chapter['content']
        link = {book_chapter['bob']}
        for line in lines:
            for character in characters:
                if character['name'] in line.split():
                    link.add(character['id'])
        if len(link) > 0:
            scenes.append(list(link))

json.dump(scenes, open(os.path.join('generated','scenes.json', 'w')), indent=2)
