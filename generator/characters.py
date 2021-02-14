import json
import os

import colorcet as cc
from sqlalchemy import inspect

from app import db
from generator.models import ChapterCharacter
from generator.models.characters import Character
from generator.utils import sorted_by_key


def get_bob_characters():
    return db.session.query(Character).filter_by(is_bob=True).all()


def import_bob_characters():
    with open(os.path.join("public_data", "genealogy.txt")) as genealogy:
        lines = genealogy.readlines()

    for line in lines:
        stripped = line.strip().split(";")[0]
        if len(stripped) == 0:
            continue

        bob = [el.strip() for el in stripped.split(":")]

        char = Character(id=bob[-1], name=bob[-1], is_bob=True)
        if len(bob) != 1:
            char.affiliation = bob[-2]

        if char.id == "Riker":
            char.other_names = ["Will", "William"]
        if char.id == "Arthur":
            char.other_names = ["Eeyore"]
        if char.id == "Sam":
            char.other_names = ["Exodus-3"]
        if char.id == "Dexter":
            char.other_names = ["Dex"]
        if char.id == "Daedalus":
            char.other_names = ["Dae"]
        db.session.add(char)

    db.session.commit()
    return get_bob_characters()


def import_characters():
    import_bob_characters()

    nonbobs = json.load(open(os.path.join("public_data", "nonbob_characters.json")))
    mapper = inspect(Character)
    db.session.bulk_insert_mappings(mapper, nonbobs)
    db.session.commit()


def get_characters(nb=None):
    q = db.session.query(Character)
    if nb is not None:
        q = q.join(ChapterCharacter).filter(ChapterCharacter.chapter_nb == nb)
    return q.all()


def get_characters_map():
    return sorted_by_key({character.id: character for character in get_characters()})


def get_bob_styles():
    bob_characters = get_bob_characters()
    styles = ""
    for i, bob_character in enumerate(bob_characters):
        template = "path.%s {stroke: %s;}\n"

        styles += template % (
            bob_character.id,
            cc.colorwheel[int(256 * i / len(bob_characters))],
        )
    return styles
