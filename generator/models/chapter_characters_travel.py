from sqlalchemy import Column, String, ForeignKey

from app import db
from generator.models import (
    Character,
    relationship,
    Integer,
    ForeignKeyConstraint,
    BookChapter,
    Location,
)


class CharacterTravel(db.Model):
    __tablename__ = "charactertravels"

    character_id = Column(String, ForeignKey("characters.id"), primary_key=True)
    character = relationship(Character, backref="travels")

    chapter_nb = Column(Integer, primary_key=True)
    chapter_nc = Column(Integer, primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            [chapter_nb, chapter_nc], [BookChapter.nb, BookChapter.nc]
        ),
        {},
    )
    chapter = relationship(BookChapter)

    location_id = Column(String, ForeignKey("locations.id"))
    location = relationship(Location)
