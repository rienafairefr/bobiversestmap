from astropy import units as u
from astropy.coordinates import SkyCoord

import csv
import os

from sqlalchemy import inspect

from app import db
from generator.models.locations import Star
from generator.utils import memoize, stripped, get_one_or_create


def import_stars():
    with open(os.path.join('public_data', 'locations.txt')) as location:
        lines = location.readlines()

    stars = {}
    for line in lines:
        place = stripped(line.strip().split(':'))
        if len(place) == 1:
            stars[place[0]], _  = get_one_or_create(db.session, Star, id=place[0], name=place[0], other_names=[])

    stars['GL 877'].other_names.append('Gliese 877')
    stars['GL 54'].other_names.append('Gliese 54')

    db.session.add_all(stars.values())
    db.session.commit()


def import_starsmap():
    with open(os.path.join('public_data', 'stars.csv')) as starsmap_file:
        csv_reader = csv.DictReader(starsmap_file)
        for row in csv_reader:
            star = get_one_or_create(db.session, Star, name=row['ProperName'])

            try:
                c = SkyCoord(ra=float(row['RA'])*u.degree, dec=float(row['Dec'])*u.degree,
                             distance=float(row['Distance'])*u.lyr)
                c.representation = 'cartesian'
                star.x = c.x
                star.y = c.y
                star.z = c.z
            except:
                pass
    db.session.commit()


def get_stars():
    return db.session.query(Star).all()
