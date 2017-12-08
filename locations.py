import json
import os

from utils import json_dump, memoize


@memoize()
def get_locations():
    with open(os.path.join('public_data', 'locations.txt')) as location:
        lines = location.readlines()

    places = []
    for line in lines:
        place = line.strip().split(':')

        place_dict = {'star': place[0]}
        if len(place) >= 2:
            place_dict['planet'] = place[1]
        if len(place) >= 3:
            place_dict['city'] = place[2]

        place_dict['id'] = '_'.join(place)

        places.append(place_dict)
    return places


def write_locations():
    places = get_locations()
    json_dump(places, open(os.path.join('generated', 'locations.json'), 'w'))


if __name__ == '__main__':
    write_locations()
