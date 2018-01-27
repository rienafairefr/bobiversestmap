
from sqlalchemy import Column, String, Float
from sqlalchemy.util import hybridproperty

from app import db
from generator.utils import ArrayType


class Star(db.Model):
    __tablename__ = 'stars'

    id = Column(String, primary_key=True)

    @hybridproperty
    def name(self):
        return self.id

    other_names = Column(ArrayType)
    x = Column(Float)
    y= Column(Float)
    z = Column(Float)