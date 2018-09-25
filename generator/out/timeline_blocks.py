from app import db
from generator.models import BookChapter, Character


def get_timeline_blocks_json(nb=None):
    chapters = db.session.query(BookChapter).all()
    characters = db.session.query(Character).all()

    data = []
    for ichap,chapter in enumerate(chapters):
        for ichar,character in enumerate(characters):
            data.append({
                'x':ichap,
                'y':ichar,
                'value': 1 if character in chapter.characters else 0
            })

    return data