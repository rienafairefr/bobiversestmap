import json
import os

with open(os.path.join('public_data', 'locations.txt')) as location:
    lines = location.readlines()

places = []
for line in lines:
    place = line.strip().split(':')

    place_dict = {'star': place[0]}
    if len(place)>=2:
        place_dict['planet'] = place[1]
    if len(place)>=3:
        place_dict['city'] = place[2]

    place_dict['id'] = '_'.join(place)

    places.append(place_dict)

json.dump(places, open(os.path.join('generated', 'locations.json'), 'w'), indent=2)
