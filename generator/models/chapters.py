import os

import yaml
from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship, deferred
from sqlalchemy.util import hybridproperty

from app import db
from generator.models.characters import Character
from generator.models.dates import Period
from generator.models.links import Link
from generator.models.locations import Location
from generator.utils import ArrayType, ComparableMixin


class BookChapter(db.Model, ComparableMixin):
    __tablename__ = 'bookchapters'

    nb = Column(Integer, primary_key=True)
    nc = Column(Integer, primary_key=True)

    @hybridproperty
    def k(self):
        return self.nb, self.nc

    bob_id = Column(ForeignKey('characters.id'))
    location_id = Column(String, ForeignKey('locations.id'))
    location = relationship(Location)
    description = Column(String)

    tokenized_content = deferred(Column(ArrayType))
    number_lines = Column(Integer)

    characters = relationship(Character, secondary='chaptercharacters')
    links = relationship(Link, secondary='chapterlinks', backref='chapter')
    period_id = Column(String, ForeignKey('periods.id'))
    period = relationship(Period)
    bob_character = relationship(Character, foreign_keys=[bob_id])

    def _cmpkey(self):
         return self.k