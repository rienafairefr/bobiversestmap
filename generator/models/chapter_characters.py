from sqlalchemy import Column, Integer, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from app import db
from generator.models.chapters import BookChapter
from generator.models.characters import Character


class ChaptersCharacters(db.Model):
    __tablename__ = 'chapterscharacters'

    id = Column(Integer, primary_key=True)


    chapter_nb = Column(Integer)
    chapter_nc = Column(Integer)

    __table_args__ = (ForeignKeyConstraint([chapter_nb, chapter_nc],
                                           [BookChapter.nb, BookChapter.nc]),
                      {})
    chapter = relationship(BookChapter)

    character_id = Column(Integer, ForeignKey('characters.id'))
    character = relationship(Character)
