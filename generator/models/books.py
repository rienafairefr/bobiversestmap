from sqlalchemy import Integer, Column, String, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from app import db
from generator.models.chapters import BookChapter
from generator.models.characters import Character


class Book(db.Model):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)


class BookLine(db.Model):
    __tablename__ = 'booklines'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)
    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship(Book, backref='lines')

    chapter_nb = Column(Integer)
    chapter_nc = Column(Integer)
    __table_args__ = (ForeignKeyConstraint([chapter_nb, chapter_nc],
                                           [BookChapter.nb, BookChapter.nc]),
                      {})
    chapter = relationship(BookChapter, backref='lines')
