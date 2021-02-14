from sqlalchemy import Column, Integer, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from app import db
from generator.models.chapters import BookChapter
from generator.models.links import Link


class ChapterLink(db.Model):
    __tablename__ = "chapterlinks"

    id = Column(Integer, primary_key=True)

    chapter_nb = Column(Integer)
    chapter_nc = Column(Integer)
    ns = Column(Integer)

    __table_args__ = (
        ForeignKeyConstraint(
            [chapter_nb, chapter_nc], [BookChapter.nb, BookChapter.nc]
        ),
        {},
    )
    chapter = relationship(BookChapter)

    link_id = Column(Integer, ForeignKey("links.id"))
    link = relationship(Link)
