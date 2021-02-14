import datetime

from dateutil import parser
from dateutil.relativedelta import relativedelta

from app import db
from generator.models import BookChapter
from generator.models.dates import Period

# unit is day
month = relativedelta(months=1)
day = relativedelta(days=1)
default_datetime = datetime.datetime(year=1, month=1, day=1)


def treat_one_period(date):
    parsed_datetime = parser.parse(date, default=default_datetime)
    # period = Period(id='period %u %u' % book_chapter.k,
    #                             time_start=parsed_datetime)
    period = Period(time_start=parsed_datetime)
    period.duration = month
    return period


def postprocess_dates():
    def get(*k):
        return db.session.query(BookChapter).get(k)

    # 1 day for the first 13th chapters
    for i in range(1, 14):
        get(1, i).period.duration = day

    # some date/duration special cases
    # GL 877 destruction 5 months relative time
    get(3, 70).period.duration = 5 * month

    pass
