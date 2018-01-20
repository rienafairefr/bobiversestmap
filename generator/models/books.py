from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app import db


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
