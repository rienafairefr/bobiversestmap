from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from app import db
from generator.models.books import BookLine
from generator.models.characters import Character


class CharacterLine(db.Model):
    __tablename__ = 'characterlines'
    id = Column(Integer, primary_key=True)

    bookline_id = Column(Integer, ForeignKey('booklines.id'))
    bookline = relationship(BookLine)

    character_id = Column(String, ForeignKey('characters.id'))
    character = relationship(Character)
