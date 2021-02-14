import os

from app import db
from generator.models.chapters import BookChapter
from generator.models.characters import Character
from generator.utils import stripped


def get_thresholds_last():
    characters = db.session.query(Character).all()
    return {
        c.id: c.last_appearance for c in characters if c.last_appearance is not None
    }


def get_thresholds_first():
    characters = db.session.query(Character).all()
    return {
        c.id: c.first_appearance for c in characters if c.first_appearance is not None
    }


def import_threshold(set_func, filename):
    lines = open(os.path.join("public_data", filename), encoding="utf-8").readlines()
    for line in lines:
        element = stripped(line.split(","))
        if len(element) != 3:
            continue
        character = db.session.query(Character).get(element[0])
        chapter = db.session.query(BookChapter).get((element[1], element[2]))
        if character is not None and chapter is not None:
            set_func(character, chapter)


def import_thresholds():
    import_threshold(
        lambda c, v: setattr(c, "last_appearance", v), "thresholds_last.txt"
    )
    import_threshold(
        lambda c, v: setattr(c, "first_appearance", v), "thresholds_first.txt"
    )
    db.session.commit()
