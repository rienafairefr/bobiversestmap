import os

from sqlalchemy import or_

from app import db
from generator.books import get_book_chapters
from generator.models.locations import Location, Star
from generator.utils import json_dump, memoize, sorted_by_key, get_one_or_create
from generator.locations import get_locations


def treat_scenes_locations(chapters_books=None):
    if chapters_books is None:
        chapters_books = get_book_chapters()

    scenes_locations = {}
    for k, book_chapter in chapters_books.items():
        scenes_locations[k] = book_chapter.raw_location

    # Bob on Earth
    for i in range(1, 13):
        scenes_locations[1, i] = 'Sol_Earth'

    # Bob first voyage
    scenes_locations[1, 13] = 'Sol -> Epsilon Eridani'

    for k, v in scenes_locations.items():
        if v == 'Gliese 877':
            scenes_locations[k] = 'GL 877'
        if v == 'Gliese 54':
            scenes_locations[k] = 'GL 54'

    # Calvin in Alpha Centauri B
    scenes_locations[1, 28] = 'Alpha Centauri B'

    # Mulder in Poseidon
    scenes_locations[2, 49] = 'Eta Cassiopeiae_Poseidon'

    # Hal going to GL 54
    scenes_locations[2, 54] = 'GL 877 -> GL 54'

    # Howard moving on
    scenes_locations[2, 58] = 'Omicron2 Eridani -> HIP 14101'

    # Mulder Leaving Poseidon
    scenes_locations[2, 62] = 'Eta Cassiopeiae_Poseidon'

    #  Bob in Camelot
    scenes_locations[3, 10] = 'Delta Eridani_Eden'

    # Icarus & Deadalus
    scenes_locations[3, 17] = 'Epsilon Eridani -> Epsilon Indi'
    # Neil & Herschel
    scenes_locations[3, 22] = 'Delta Pavonis'
    scenes_locations[3, 24] = 'Delta Pavonis'
    # Bob on Eden
    scenes_locations[3, 34] = 'Delta Eridani_Eden'

    # Neil & Herschel moving the Bellerophon
    scenes_locations[3, 38] = 'Delta Pavonis -> Sol'

    # Icarus & Deadalus
    scenes_locations[3, 43] = 'Epsilon Indi -> GL 877'

    # Icarus & Deadalus destroying GL877
    scenes_locations[3, 70] = 'GL 877'

    def treat_scene_location(scene_location):
        if '->' in scene_location:
            places = [el.strip() for el in scene_location.split('->')]
            star0 = db.session.query(Star).get(places[0])
            star1 = db.session.query(Star).get(places[1])
            returnvalue, _ = get_one_or_create(db.session, Location,
                                               id=scene_location,
                                               star=star0,
                                               star_destination=star1,
                                               is_travel=True)
            pass
        else:
            potential_planet = db.session.query(Location).filter(Location.planet_name == scene_location).first()
            if potential_planet:
                returnvalue = potential_planet
                pass
            else:
                returnvalue = db.session.query(Location).get(scene_location)
                pass
        return returnvalue

    for k, v in scenes_locations.items():
        book_chapter = chapters_books[k]
        book_chapter.location = treat_scene_location(v.strip())

    db.session.commit()

    # treat_scene_location(v.strip())


def get_scenes_locations(book_chapters=None):
    if book_chapters is None:
        book_chapters = get_book_chapters()
    scenes_locations = sorted_by_key({k: book_chapter.location for k, book_chapter in book_chapters.items()})

    return scenes_locations

def get_scenes_locations_book(nb=None):
    return sorted_by_key({k: v for k, v in get_scenes_locations().items() if nb is None or k[0] == nb})
