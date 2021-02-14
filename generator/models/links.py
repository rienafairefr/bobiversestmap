from sqlalchemy import Column, Integer, ForeignKey, Boolean, String
from sqlalchemy.orm import relationship

from app import db
from generator.models.characters import Character


class Link(db.Model):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True)

    characterA_id = Column(Integer, ForeignKey("characters.id"))
    characterA = relationship(Character, foreign_keys=[characterA_id])

    characterB_id = Column(Integer, ForeignKey("characters.id"))
    characterB = relationship(Character, foreign_keys=[characterB_id])

    is_scut = Column(Boolean)
    sentence = Column(String)
    ns = Column(Integer)
