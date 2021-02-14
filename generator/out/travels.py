import csv
from io import StringIO

from generator.characters import get_characters
from generator.locations import get_locations
from generator.travels import get_travels_dict
from generator.utils import memoize, sorted_by_key


@memoize()
def get_travels_book_json(nb=None):
    characters = get_characters(nb)
    locations = get_locations(nb)

    travels_dict = get_travels_dict(nb)

    travels = [
        {"character_id": character_id, "travels": value}
        for character_id, value in travels_dict.items()
    ]

    return {"locations": locations, "characters": characters, "travels": travels}


@memoize()
def get_travels_book_csv(nb=None):

    travels_dict = get_travels_dict(nb)
    characters = get_characters()

    output = StringIO()
    fieldnames = ["nb", "nc", "date"]
    fieldnames.extend(ch.id for ch in characters)
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    rows = {}
    for character_id, character_travels in travels_dict.items():
        for character_travel in character_travels:
            nb = character_travel.chapter.nb
            nc = character_travel.chapter.nc
            travel_period = character_travel.chapter.period
            location_id = character_travel.location_id

            default_row = dict(
                nb=nb, nc=nc, date=travel_period.time_start.strftime("%Y-%m-%d")
            )

            if location_id is not None:
                rows.setdefault((nb, nc), default_row)[character_id] = location_id
            else:
                rows.setdefault((nb, nc), default_row)[character_id] = "#no_location#"

    rows = sorted_by_key(rows)
    writer.writeheader()
    writer.writerows(rows.values())
    data = output.getvalue()
    return data


if __name__ == "__main__":
    travels_book_csv = get_travels_book_csv()
