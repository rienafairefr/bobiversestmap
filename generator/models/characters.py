from sqlalchemy import Column, String, Boolean, Integer, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from app import db
from generator.utils import ArrayType


class Character(db.Model):
    __tablename__ = 'characters'

    id = Column(String, primary_key=True)
    is_bob = Column(Boolean)
    name = Column(String)
    affiliation = Column(String)
    other_names = Column(ArrayType, default=lambda:[])

    @property
    def all_names(self):
        return_value = [self.name]
        return_value.extend(self.other_names)
        return return_value

    first_appearance_chapter_nb = Column(Integer)
    first_appearance_chapter_nc = Column(Integer)
    last_appearance_chapter_nb = Column(Integer)
    last_appearance_chapter_nc = Column(Integer)

    first_appearance = relationship('BookChapter')
    last_appearance = relationship('BookChapter')


    __table_args__ = (ForeignKeyConstraint([first_appearance_chapter_nb, first_appearance_chapter_nc, last_appearance_chapter_nb, last_appearance_chapter_nc],
                                           ['bookchapters.nb', 'bookchapters.nc', 'bookchapters.nb', 'bookchapters.nc']),
                      {})