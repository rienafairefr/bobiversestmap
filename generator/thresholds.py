import os

from generator.utils import memoize, stripped


@memoize()
def get_thresholds_deaths():
    return get_thresholds('thresholds_deaths.txt')


@memoize()
def get_thresholds_births():
    return get_thresholds('thresholds_births.txt')


@memoize()
def get_thresholds(filename):
    thresholds = {}
    thresholds_deaths = open(os.path.join('public_data', filename), encoding='utf-8').readlines()
    for line in thresholds_deaths:
        element = stripped(line.split(','))
        thresholds[element[0]] = (int(element[1]), int(element[2]))
    return thresholds