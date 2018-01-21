import datetime

from dateutil import parser

from generator.books import get_book_chapters
from generator.models.dates import Period


def treat_dates(book_chapters=None):
    if book_chapters is None:
        book_chapters = get_book_chapters()
    # unit is day
    month = 30.4375

    for k, book_chapter in book_chapters.items():
        default_datetime = datetime.datetime(year=1, month=1, day=1)
        parsed_datetime = parser.parse(book_chapter.date, default=default_datetime)
        book_chapter.period = Period(id='date %d %d' % k,
                           raw=book_chapter.date,
                           datetime=parsed_datetime,
                           duration=month)

    # 1 day for the first 13th chapters
    for i in range(1, 14):
        book_chapters[1,i].period.duration = 1

    # some date/duration special cases
    # GL 877 destruction 5 months relative time
    book_chapters[3, 70].period.duration = 5 * month

    # time zero when Bob wakes up ine 2133
    first_date = book_chapters[1, 2].period

    for k in book_chapters:
        book_chapters[k].period.time_start -= first_date.time_start
