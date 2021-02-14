from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.hybrid import hybrid_property

from app import db


class Period(db.Model):
    __tablename__ = "periods"
    id = Column(Integer, primary_key=True)
    time_start = Column(DateTime)
    time_end = Column(DateTime)

    @hybrid_property
    def duration(self):
        return self.time_end - self.time_start

    @duration.setter
    def duration(self, value):
        time_end = self.time_start + value
        self.time_end = time_end

    def __repr__(self):
        return "< Period " + self.time_start + " " + self.duration + ">"
