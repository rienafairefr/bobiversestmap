import os

from stars import get_stars
from utils import json_dump, memoize


@memoize()
def get_locations():
    with open(os.path.join('public_data', 'locations.txt')) as location:
        lines = location.readlines()

    places = get_stars().copy()
    for line in lines:

        place = line.strip().split(':')
        if len(place) == 2:

            place_dict = dict(id='_'.join(place),
                              name=place[1],
                              star_id=place[0],
                              other_names=[])

            places['_'.join(place)] = place_dict

    def treat_one(id, element):
        element['id'] = id
        return element

    places_list = [treat_one(id, element) for id,element in places.items()]
    return places_list


def write_locations():
    places = get_locations()
    json_dump(places, os.path.join('generated', 'locations.json'))


if __name__ == '__main__':
    write_locations()
