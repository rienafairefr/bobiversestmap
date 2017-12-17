import csv
import os

from utils import memoize, stripped


@memoize()
def get_stars():
    with open(os.path.join('public_data', 'locations.txt')) as location:
        lines = location.readlines()

    stars = {}
    for line in lines:
        place = stripped(line.strip().split(':'))
        if len(place) == 1:
            star = {'name': place[0], 'other_names':[]}

            stars[place[0]] = star

    stars['GL 877']['other_names'].append('Gliese 877')
    stars['GL 54']['other_names'].append('Gliese 54')

    return stars


@memoize()
def get_starsmap():
    starsmap = {}
    with open(os.path.join('public_data', 'stars.csv')) as starsmap_file:
        csv_reader = csv.DictReader(starsmap_file)
        for row in csv_reader:
            starsmap[row['ProperName']] = row

    return starsmap


if __name__ == '__main__':
    data= get_starsmap()