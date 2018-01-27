import contextlib
import os

from app import db
from generator.characters import get_characters_map, get_characters
from generator.common import get_keys
from generator.models.chapter_characters_travel import CharacterTravel
from generator.thresholds import get_thresholds_last, get_thresholds_first


def treat_one(character, book_chapter):
    current_location = None
    if (character.is_bob and character == book_chapter.bob_character)\
            or (character in book_chapter.characters):
        current_location = book_chapter.location

    character_travel = CharacterTravel(character=character,
                                       chapter=book_chapter,
                                       location=current_location)
    character.travels.append(character_travel)


def import_chapter_characters_travels(book_chapters):
    for character in get_characters():
        for book_chapter in book_chapters.values():
            treat_one(character, book_chapter)
    postprocess_character_travels()
    db.session.commit()
    write_travels()


def get_travels(nb=None):
    q = db.session.query(CharacterTravel)
    if nb is not None:
        q = q.filter(CharacterTravel.chapter.nb==nb)
    return {(ct.character.character_id,ct.chapter.nb, ct.chapter.nc):ct.location.id for ct in
            q.all()}


def postproces_births_deaths(thresholds_last=None, thresholds_first=None):
    characters_travels = db.session.query(CharacterTravel).all()
    if thresholds_last is None:
        thresholds_last = get_thresholds_last()
    if thresholds_first is None:
        thresholds_first = get_thresholds_first()

    for character_travel in characters_travels:
        character_id = character_travel.character_id
        nb, nc = character_travel.chapter.k
        threshold_last = thresholds_last.get(character_id)
        threshold_first = thresholds_first.get(character_id)
        if (threshold_first is not None and (nb, nc) < threshold_first) \
                or (threshold_last is not None and (nb, nc) > threshold_last):
            db.session.remove(character_travel)
    db.session.commit()


def postprocess_character_travels():
    keys = get_keys()
    characters_travels = db.session.query(CharacterTravel).all()
    postproces_births_deaths()

    for characters_travel in characters_travels:
        character = characters_travel.character
        if character.affiliation == 'Deltans':
            if characters_travel.location_id is not None:
                characters_travel.location_id = 'Delta Eridani_Eden'
        if character.affiliation == 'Poseidon Revolution':
            if characters_travel.location_id is not None:
                characters_travel.location_id = 'Eta Cassiopeiae_Poseidon'

    def get(character_id, nb, nc):
        return db.session.query(CharacterTravel).get(character_id, nb, nc)

    def fix(character_id, nb, nc, new_id):
        get(character_id, nb, nc).location_id = new_id

    def remove(character_id, nb, nc):
        db.session.remove(get(character_id, nb, nc))

    fix('Arthur', 1, 31, 'Sol_Earth')
    fix('Arthur', 1, 43, 'Sol_Earth')
    fix('Arthur', 1, 60, 'Sol_Earth')

    fix('Barney', 1, 60, 'Sol_Earth')

    fix('Bart', 1, 45, 'Alpha Centauri')

    fix('Calvin', 1, 28, 'Alpha Centauri B')
    fix('Goku', 1, 28, 'Alpha Centauri A')

    fix('Bashful', 2, 13, 'GL 54')
    fix('Dopey', 2, 13, 'GL 54')
    fix('Sleepy', 2, 13, 'GL 54')
    fix('Hungry', 2, 13, 'GL 54')

    fix('Bashful', 2, 15, 'GL 54')
    fix('Dopey', 2, 15, 'GL 54')
    fix('Sleepy', 2, 15, 'GL 54')
    fix('Hungry', 2, 15, 'GL 54')

    fix('Bender', 1, 30, 'Delta Eridani_Eden')

    # Luke leaves for Kappa Ceti in 1,39
    # Bender leaves for Gamma Leporis A in 1,39 (16 ly travel)
    for bob in 'Bender', 'Luke':
        for key in keys:
            if key > (1, 39):
                remove(bob, *key)

    # Bert and Ernie in colony ships
    fix('Bert', 1, 58, 'Sol_Earth')
    fix('Ernie', 1, 58, 'Sol_Earth')
    fix('Bert', 1, 61, 'Omicron2 Eridani')
    fix('Ernie', 1, 61, 'Omicron2 Eridani')

    fix('Bert', 2, 5, 'Omicron2 Eridani')
    fix('Ernie', 2, 5, 'Omicron2 Eridani')

    # Bridget arrives on Vulcan at (1, 61)
    fix('Bridget', 1, 61, 'Omicron2 Eridani_Vulcan')
    # Bridget doesnt leave Vulcan before being replicated
    fix('Bridget', 3, 40, 'Omicron2 Eridani_Vulcan')

    # Bruce from Calvin and Goku, born in Alpha Centauri
    fix('Bruce', 1, 45, 'Alpha Centauri')
    fix('Bruce', 2, 37, '11 Leonis Minoris')

    #  Milo
    fix('Milo', 1, 17, 'Epsilon Eridani')
    fix('Milo', 1, 19, 'Omicron2 Eridani')
    fix('Milo', 1, 46, '82 Eridani')

    # Landers on Vulcan
    for k in keys:
        if k > (1, 1) and k <= (1, 13):
            fix('Landers', *k, 'Sol_Earth')

    # Butterworth on Vulcan
    for k in keys:
        if k >= (1, 61):
            fix('Butterworth', *k, 'Omicron2 Eridani_Vulcan')

    # Julia and clan Bob aboard Exodus-3 go to Omicron2 Eridani, leave in chapter (2,5)

    # Charles one of the first Riker's clones when back to Sol
    fix('Charles', 1, 25, 'Sol')

    fix('Daedalus', 3, 17, ['Epsilon Eridani', 'Epsilon Indi'])
    fix('Daedalus', 3, 43, ['Epsilon Indi', 'GL 877'])
    fix('Daedalus', 3, 70, 'GL 877')

    #  Dexter from Sol to Vulcan
    fix('Dexter', 2, 51, 'Omicron2 Eridani_Vulcan')

    # Dr Doucette on Vulcan
    for k in keys:
        if k > (2, 13):
            remove('Doucette', *k)
        else:
            fix('Doucette', *k, 'Sol_Earth')

    # Both coming from Sol (Exodus-6)
    fix('Edwin', 2, 46, 'Epsilon Indi')
    fix('Rudy', 2, 46, 'Epsilon Indi')

    # Going agains Medeiros
    # the cohort of 8 being built by Bill in Epsilon Eridani in (1,51)
    fix('Elmer', 1, 51, 'Epsilon Eridani')
    fix('Elmer', 1, 60, '82 Eridani')
    fix('Khan', 1, 51, 'Epsilon Eridani')
    fix('Khan', 1, 60, '82 Eridani')
    fix('Fred', 1, 51, 'Epsilon Eridani')
    fix('Fred', 1, 60, '82 Eridani')

    # second wave
    fix('Elmer', 2, 34, 'Epsilon Eridani')
    fix('Elmer', 2, 50, '82 Eridani')
    fix('Loki', 2, 34, 'Epsilon Eridani')
    fix('Loki', 2, 50, '82 Eridani')
    fix('Verne', 2, 34, 'Epsilon Eridani')
    fix('Verne', 2, 50, '82 Eridani')
    fix('Hank', 2, 34, 'Epsilon Eridani')
    fix('Hank', 2, 50, '82 Eridani')

    # Elmer destroyed in 1,60 ; restored in in 2,34
    # Khan restored a backup in 2,34 named Loki

    # Phineas and Ferb come online in Delta Pavonis for Pav extraction
    # Jacques arrived there in 2,60
    fix('Phineas', 2, 73, 'Delta Pavonis')
    fix('Ferb', 2, 73, 'Delta Pavonis')

    #  Jacques killed in battle of Delta pavonis, but restored
    fix('Phineas', 3, 48, 'HIP 84051')
    fix('Ferb', 3, 48, 'HIP 84051')
    fix('Jacques', 3, 48, 'HIP 84051')

    fix('Ferb', 3, 74, 'HIP 84051')

    # stays with Bill all the way
    fix('Garfield', 1, 20, 'Epsilon Eridani')

    # Hal blown up in GL 877 in (2,38)
    # goes back there in (2,53)
    remove('Hal', 2, 39)

    # Hannibal blown up in (1,60)
    # restored ?
    # leads the Jokers in Sol in (3,64)
    fix('Hannibal', 1, 60, '82 Eridani')
    fix('Hannibal', 3, 64, 'Sol')

    # Mario leaves GL 54 in (2,54)

    # Hank mentioned in 3,21
    fix('Hank', 3, 21, "P Eridani")

    # Assume Henry Roberts doesnt leave Epsilon Indi after leaving Earth
    for k in keys:
        if k > (1, 13):
            fix('Henry', *k, 'Epsilon Indi')
        else:
            fix('Henry', *k, 'Sol_Earth')

    remove('Henry', 1, 1)
    fix('Henry', 1, 13, ['Sol_Earth', 'Epsilon Indi'])

    # Herschel and Neil leaving for 82 Eridani in (3,75)

    #  Homer going to Sol with Riker
    fix('Homer', 1, 20, 'Epsilon Eridani')
    fix('Homer', 1, 21, 'Sol')
    fix('Riker', 1, 20, 'Epsilon Eridani')
    fix('Riker', 1, 21, 'Sol')

    # Howard from Sol to Omicron2 Eridani/Vulcan
    fix('Howard', 1, 58, 'Sol')
    fix('Howard', 1, 61, 'Omicron2 Eridani')
    fix('Howard', 3, 20, 'HIP 14101_Odin')

    fix('Howard', 3, 62, 'Epsilon Indi_Big Top')

    # Isaac, Jack, and Owen three colony ships arriving in 82 Eridani from Sol in (3,18)

    delete = []
    current_location_id = None
    # fill gaps with current known location
    for characters_travel in characters_travels:
        nb, nc = characters_travel.chapter.k

        if (nb, nc) == (1, 1):
            current_location_id = None

        if characters_travel.location_id is not None:
            # location is filled
            current_location_id = characters_travel.location_id
        else:
            # no location
            if current_location_id is None:
                # mark for deletion
                delete.append(characters_travel)
            else:
                # propagate in the gaps
                current_location_id.location_id = current_location_id
    for characters_travel in delete:
        db.session.remove(characters_travel)


def write_travels(characters_map=None):
    if characters_map is None:
        characters_map = get_characters_map()

    with contextlib.ExitStack() as stack:

        locations_files = {}
        for character_id in characters_map.keys():
            os.makedirs(os.path.join('generated', character_id), exist_ok=True)
            locations_files[character_id] = stack.enter_context(
                open(os.path.join('generated', character_id, 'locations'), 'w',
                     encoding='utf-8'))

        for character_travel in db.session.query(CharacterTravel).all():
            locations_file = locations_files[character_id]

            if character_travel.location_id is None:
                location_id = '-----'
            else:
                location_id = character_travel.location_id

            nb, nc = character_travel.chapter.k
            try:
                locations_file.write('{:^10s} {:3d} {:3d} {:s}\n'.format(character_id, nb, nc, location_id))
            except TypeError:
                locations_file.write(
                    '{:^10s} {:3d} {:3d} {:s} -> {:s}\n'.format(character_id, nb, nc, location_id[0],
                                                                location_id[1]))
