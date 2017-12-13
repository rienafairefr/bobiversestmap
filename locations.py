import json
import os

from utils import json_dump, memoize


@memoize()
def get_locations():
    with open(os.path.join('public_data', 'locations.txt')) as location:
        lines = location.readlines()

    distances = {}
    for line in lines:
        if len(line.split(':'))==1:
            split_distance = line.strip().split(';')
            distance = float(split_distance[0])
            star_id = split_distance[1]
            distances[star_id] = distance

    places = []
    for line in lines:

        split_distance = line.strip().split(';')
        if len(split_distance) == 2:
            place = split_distance[1].strip().split(':')
        else:
            place = split_distance[0].strip().split(':')

        place_dict = {'star': place[0], 'distance': distances[place[0]]}
        if len(place) >= 2:
            place_dict['planet'] = place[1]
        if len(place) >= 3:
            place_dict['city'] = place[2]

        place_dict['id'] = '_'.join(place)

        places.append(place_dict)
    return places


def write_locations():
    places = get_locations()
    json_dump(places, os.path.join('generated', 'locations.json'))


if __name__ == '__main__':
    write_locations()
