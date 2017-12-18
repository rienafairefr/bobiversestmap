import datetime
import os
from collections import OrderedDict

from dateutil import parser

from generator.books import get_book_chapters
from generator.utils import json_dump, memoize


@memoize()
def get_dates():
    chapters_books = get_book_chapters()
    # unit is day
    month = 30.4375

    parsed_dates = OrderedDict()
    for k, book_chapter in chapters_books.items():
        default_datetime = datetime.datetime(year=1, month=1, day=1)
        parsed_datetime = parser.parse(book_chapter['date'], default=default_datetime)
        parsed_date = dict(id='date %d %d' % k,
                           raw=book_chapter['date'],
                           start=int(parsed_datetime.timestamp() / (24 * 3600)),
                           datetime=parsed_datetime,
                           duration=month)
        parsed_dates[k] = parsed_date

    # 1 day for the first 13th chapters
    for i in range(1, 14):
        parsed_dates[1, i]['duration'] = 1

    # some date/duration special cases
    # GL 877 destruction 5 months relative time
    parsed_dates[3, 70]['duration'] = 5 * month

    # time zero when Bob wakes up ine 2133
    first_date = parsed_dates[1, 2]

    for k in parsed_dates:
        parsed_dates[k]['start'] = parsed_dates[k]['start'] - first_date['start']

    return parsed_dates


def write_dates():
    parsed_dates = get_dates()
    json_dump(parsed_dates, os.path.join('generated', 'scenes_dates.json'))


if __name__ == '__main__':
    write_dates()
