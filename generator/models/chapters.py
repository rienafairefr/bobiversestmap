from sqlalchemy import String, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app import db
from generator.models.characters import Character
from generator.models.locations import Location
from generator.nl import sentences_tokenize, word_tokenize_sentences
from generator.utils import ArrayType


class BookChapter(db.Model):
    __tablename__ = 'bookchapters'

    nb = Column(Integer, primary_key=True)
    nc = Column(Integer, primary_key=True)
    bob = Column(String)
    date = Column(String)
    location_id = Column(String, ForeignKey('locations.id'))
    location = relationship(Location)
    raw_location = Column(String)
    description = Column(String)

    content = Column(ArrayType)
    all_lines = Column(String)
    sentences = Column(ArrayType)
    tokenized_content = Column(ArrayType)

    @classmethod
    def from_chapter(cls, chapter):
        obj = BookChapter()
        obj.bob = chapter[1]
        obj.date = chapter[2]
        obj.raw_location = chapter[3]

        obj.content = chapter[4:]
        obj.all_lines = '\n'.join(chapter[4:])
        obj.sentences = list(sentences_tokenize(obj.content))
        obj.tokenized_content = list(word_tokenize_sentences(obj.sentences))
        return obj

    characters = relationship(Character, secondary='chapterscharacters')
