from app import db
from generator.models import Character


def get_genealogy():
    bobs = db.session.query(Character).filter_by(is_bob=True)

    data = [{'id': bob.id, 'parentId': bob.affiliation if bob.affiliation else '__root'} for bob in bobs]
    data.append({'id': '__root', 'parentId': None})

    return data