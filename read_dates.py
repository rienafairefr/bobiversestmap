import os
import json

import datetime
from dateutil import parser


def read_dates():
    chapters_books = json.load(open(os.path.join('generated', 'Combined.json')))
    month = 30.4375

    parsed_dates = []
    for nb, book_chapters in enumerate(chapters_books):
        for nc, book_chapter in enumerate(book_chapters):
            default_datetime = default=datetime.datetime(year=1, month=1, day=1)
            parsed_datetime = parser.parse(book_chapter['date'],default=default_datetime)
            parsed_date = dict(raw=book_chapter['date'],
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

    json.dump(parsed_dates, open(os.path.join('generated', 'scenes_dates.json'), 'w'), indent=2)


if __name__ == '__main__':
    read_dates()