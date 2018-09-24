from app import db
from generator.models import BookChapter, Character


def get_timeline_blocks_json(nb=None):
    chapters = db.session.query(BookChapter).all()
    characters = db.session.query(Character).all()

    data = {'matrix': []}
    for ichap,chapter in enumerate(chapters):
        for ichar,character in enumerate(characters):
            data['matrix'].append({
                'dim1':ichap,
                'dim2':ichar,
                'value': 1 if character in chapter.characters else 0
            })
    data['dim1'] = [{'label': chapter.k} for chapter in chapters]
    data['dim2'] = [{'label': character.name} for character in characters]

    return data