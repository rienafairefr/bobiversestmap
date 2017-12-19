import csv
from io import StringIO

from generator.characters import get_characters
from generator.dates import get_dates
from generator.locations import get_locations
from generator.travels import get_travels_book
from generator.utils import memoize, sorted_by_key


@memoize()
def get_travels_book_json(nb=None):
    characters = get_characters()
    locations = get_locations()
    dates = get_dates()

    def _treatvalue(val):
        return list(sorted_by_key(val).values())

    travels_books = get_travels_book(nb).items()

    travels = [{'character_id': character_id, 'travels': _treatvalue(value)} for character_id, value in travels_books]

    return {'locations': locations,
            'dates': _treatvalue(dates),
            'characters': characters,
            'travels': travels}


@memoize()
def get_travels_book_csv(nb=None):
    dates = get_dates()

    travels_books = get_travels_book(nb)
    characters = get_characters()

    output = StringIO()
    fieldnames = ['nb', 'nc', 'date']
    fieldnames.extend(ch.id for ch in characters)
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    rows = {}
    for (character_id, nb, nc), travel_element in travels_books.items():
        date = dates[nb, nc]
        default_row = dict(nb=nb, nc=nc, date=date.datetime.strftime('%Y-%m-%d'))
        rows.setdefault((nb, nc), default_row )[character_id] = travel_element.get('location_id')
    rows = sorted_by_key(rows)
    writer.writeheader()
    writer.writerows(rows.values())
    data = output.getvalue()
    return data
