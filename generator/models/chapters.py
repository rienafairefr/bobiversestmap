from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship
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
    raw_location = Column(String)
    description = Column(String)

    all_lines = Column(String)
    sentences = Column(ArrayType)
    tokenized_content = Column(ArrayType)

    characters = relationship(Character, secondary='chapterscharacters')
    links = relationship(Link, secondary='chapterslinks', backref='chapter')
    period_id = Column(String, ForeignKey('periods.id'))
    period = relationship(Period)
    bob_character = relationship(Character, foreign_keys=[bob_id])

    def _cmpkey(self):
         return self.k
