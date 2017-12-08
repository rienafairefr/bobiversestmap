import os

import datetime
from dateutil import parser

from readcombined import get_book_chapters
from utils import json_dump, memoize


@memoize()
def get_dates():
    chapters_books = get_book_chapters()
    month = 30.4375

    parsed_dates = []
    for book_chapters in chapters_books:
        for book_chapter in book_chapters:
            default_datetime = datetime.datetime(year=1, month=1, day=1)
            parsed_datetime = parser.parse(book_chapter['date'],default=default_datetime)
            parsed_date = dict(raw=book_chapter['date'],
                               nb = book_chapter['nb'],
                               nc = book_chapter['nc'],
                               start=parsed_datetime.timestamp()/(24*3600),
                               duration=month)
            parsed_dates.append(parsed_date)

    for i in range(13):
        parsed_dates[i]['duration'] = 1

    # some date/duration special cases
    # GL 877 destruction 5 months relative time
    parsed_dates[207]['duration'] = 5*month
    #book_chapters[2][69]['duration'] = '5 months'

    for i,d in enumerate(parsed_dates):
        parsed_dates[i]['start']=parsed_dates[i]['start']-parsed_dates[1]['start']


def write_dates():
    parsed_dates = get_dates()
    json_dump(parsed_dates, open(os.path.join('generated', 'scenes_dates.json'), 'w'))


if __name__ == '__main__':
    write_dates()