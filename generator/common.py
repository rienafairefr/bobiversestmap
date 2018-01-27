from app import db
from generator.models import BookChapter


def get_keys():
    return [bc.k for bc in db.session.query(BookChapter).all()]