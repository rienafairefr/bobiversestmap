from app import db
from generator.models.chapters import BookChapter
from generator.models.locations import Location, Star
from generator.utils import get_one_or_create


def treat_one_location(scene_location):
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


def psotprocess_chapters_locations():

    chapters_locations = {}

    # Bob on Earth
    for i in range(1, 13):
        chapters_locations[1, i] = 'Sol_Earth'

    # Bob first voyage
    chapters_locations[1, 13] = 'Sol -> Epsilon Eridani'

    for k, v in chapters_locations.items():
        if v == 'Gliese 877':
            chapters_locations[k] = 'GL 877'
        if v == 'Gliese 54':
            chapters_locations[k] = 'GL 54'

    # Calvin in Alpha Centauri B
    chapters_locations[1, 28] = 'Alpha Centauri B'

    # Mulder in Poseidon
    chapters_locations[2, 49] = 'Eta Cassiopeiae_Poseidon'

    # Hal going to GL 54
    chapters_locations[2, 54] = 'GL 877 -> GL 54'

    # Howard moving on
    chapters_locations[2, 58] = 'Omicron2 Eridani -> HIP 14101'

    # Mulder Leaving Poseidon
    chapters_locations[2, 62] = 'Eta Cassiopeiae_Poseidon'

    #  Bob in Camelot
    chapters_locations[3, 10] = 'Delta Eridani_Eden'

    # Icarus & Deadalus
    chapters_locations[3, 17] = 'Epsilon Eridani -> Epsilon Indi'
    # Neil & Herschel
    chapters_locations[3, 22] = 'Delta Pavonis'
    chapters_locations[3, 24] = 'Delta Pavonis'
    # Bob on Eden
    chapters_locations[3, 34] = 'Delta Eridani_Eden'

    # Neil & Herschel moving the Bellerophon
    chapters_locations[3, 38] = 'Delta Pavonis -> Sol'

    # Icarus & Deadalus
    chapters_locations[3, 43] = 'Epsilon Indi -> GL 877'

    # Icarus & Deadalus destroying GL877
    chapters_locations[3, 70] = 'GL 877'

    for k, v in chapters_locations.items():
        db.session.query(BookChapter).get(k).location=treat_one_location(v)

    db.session.commit()

    # treat_scene_location(v.strip())
