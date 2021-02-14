from app import db
from generator.characters import get_characters
from generator.models import BookChapter
from generator.scenes import get_scenes


def get_scenes_locations(nb=None):
    q = db.session.query(BookChapter)
    if nb is not None:
        q = q.filter(BookChapter.nb == nb)
    return [r.location for r in q]


def data_json(nb=None):
    return {
        "characters": get_characters(),
        "scenes": get_scenes(nb=nb),
        "scenes_locations": get_scenes_locations(nb=nb),
    }
