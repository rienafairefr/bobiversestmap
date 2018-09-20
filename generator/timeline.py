import os
import re

from app import db
from generator.models.chapters import BookChapter
from generator.utils import json_dump, memoize, sorted_by_key


def strip(li):
    return [l.strip() for l in li]


def import_timeline_descriptions():
    lines = open(os.path.join('public_data', 'timeline_books_1-3.txt'), encoding='utf-8').readlines()
    lines = strip(lines)

    for line in lines:
        line = line.strip().split(';')[0]
        if len(line) == 0:
            continue
        split = strip(line.split('-'))
        matched = re.match('B(\d+)C(\d+)', split[1])
        nb, nc = (int(i) for i in matched.groups())
        book_chapter = db.session.query(BookChapter).get((nb, nc))
        if book_chapter is None:
            pass
        book_chapter.description = split[2]
    db.session.commit()
