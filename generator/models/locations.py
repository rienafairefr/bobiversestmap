from sqlalchemy import String, Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app import db
from generator.models.stars import Star


class Location(db.Model):
    __tablename__ = "locations"
    id = Column(String, primary_key=True)

    is_travel = Column(Boolean, default=False)
    star_id = Column(String, ForeignKey("stars.id"))
    star = relationship(Star, foreign_keys=[star_id])
    planet_name = Column(String)

    star_destination_id = Column(String, ForeignKey("stars.id"), nullable=True)
    star_destination = relationship(Star, foreign_keys=[star_destination_id])

    def __repr__(self):
        returnvalue = "<Location "
        if self.is_travel:
            returnvalue += self.star.name + " => " + self.star_destination.name
        else:
            if self.planet_name is not None:
                returnvalue += self.star.name + ":" + self.planet_name
            else:
                returnvalue += self.star.name
        returnvalue += ">"
        return returnvalue
