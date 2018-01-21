from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app import db
from generator.models.characters import Character
from generator.models.dates import Period
from generator.models.links import Link
from generator.models.locations import Location
from generator.utils import ArrayType


class BookChapter(db.Model):
    __tablename__ = 'bookchapters'

    nb = Column(Integer, primary_key=True)
    nc = Column(Integer, primary_key=True)
    bob = Column(String, ForeignKey('characters.id'))
    date = Column(String)
    location_id = Column(String, ForeignKey('locations.id'))
    location = relationship(Location)
    raw_location = Column(String)
    description = Column(String)

    content = Column(ArrayType)
    all_lines = Column(String)
    sentences = Column(ArrayType)
    tokenized_content = Column(ArrayType)

    characters = relationship(Character, secondary='chapterscharacters')
    links = relationship(Link, secondary='chapterslinks', backref='chapter')
    period_id = Column(Integer, ForeignKey('periods.id'))
    period = relationship(Period)
    bob_character = relationship(Character, foreign_keys=[bob])
