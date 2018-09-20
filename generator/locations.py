import os

from app import db
from generator.models.locations import Location
from generator.stars import get_stars


def import_locations():
    with open(os.path.join('public_data', 'locations.txt')) as location:
        lines = location.readlines()

    stars = get_stars()

    locations = [Location(id=s.name, star=s) for s in stars]
    for line in lines:

        place = line.strip().split(':')
        if len(place) == 2:
            locations.append(Location(id='_'.join(place),
                                      planet_name=place[1],
                                      star_id=place[0]))

    db.session.add_all(locations)
    db.session.commit()
    return get_locations()


def get_locations():
    return db.session.query(Location).all()
