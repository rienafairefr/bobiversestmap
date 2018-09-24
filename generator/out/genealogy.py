from app import db
from generator.models import Character


def get_genealogy():
    bobs = db.session.query(Character).filter_by(is_bob=True).all()

    def get_id(bob):
        print(bob)
        if bob.affiliation:
            parent_bob = db.session.query(Character).get(bob.affiliation)
            if parent_bob != bob:
                return get_id(parent_bob) + "." + bob.id
            else:
                return bob.id
        else:
            return bob.id


    data = []

    for bob in bobs:
        data.append({'id': get_id(bob)})

    return data