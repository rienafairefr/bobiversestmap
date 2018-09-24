from sqlalchemy import Integer, Column
from sqlalchemy.orm import deferred

from app import db
from generator.utils import ArrayType


class Book(db.Model):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    lines = deferred(Column(ArrayType, default=lambda: []))
