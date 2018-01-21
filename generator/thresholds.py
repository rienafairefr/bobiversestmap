import os

from app import db
from generator.models.chapters import BookChapter
from generator.models.characters import Character
from generator.utils import memoize, stripped


@memoize()
def get_thresholds_last():
    return get_thresholds('thresholds_last.txt')


@memoize()
def get_thresholds_first():
    return get_thresholds('thresholds_first.txt')


@memoize()
def get_thresholds(filename):
    thresholds = {}
    thresholds_deaths = open(os.path.join('public_data', filename), encoding='utf-8').readlines()
    for line in thresholds_deaths:
        element = stripped(line.split(','))
        if len(element) != 3:
            continue
        thresholds[element[0]] = (int(element[1]), int(element[2]))
    return thresholds


def treat_threshold_lines(set_func, filename):
    lines = open(os.path.join('public_data', filename), encoding='utf-8').readlines()
    for line in lines:
        element = stripped(line.split(','))
        if len(element) != 3:
            continue
        character = db.session.query(Character).get(element[0])
        chapter = db.session.query(BookChapter).get((element[1], element[2]))
        if character is not None and chapter is not None:
            set_func(character, chapter)


def import_thresholds():
    treat_threshold_lines(lambda c, v: setattr(c, 'last_appearance', v), 'thresholds_last.txt')
    treat_threshold_lines(lambda c, v: setattr(c, 'first_appearance', v), 'thresholds_first.txt')
    db.session.commit()
