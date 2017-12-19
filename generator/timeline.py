import os
import re

from generator.utils import json_dump, memoize, sorted_by_key


def strip(li):
    return [l.strip() for l in li]


@memoize()
def _get_timeline_descriptions():
    lines = open(os.path.join('public_data','timeline_books_1-3.txt'),encoding='utf-8').readlines()
    lines = strip(lines)

    timeline = {}
    for line in lines:
        line = line.strip().split(';')[0]
        if len(line)==0:
            continue
        split = strip(line.split('-'))
        matched = re.match('B(\d+)C(\d+)',split[1])
        nb, nc = (int(i) for i in matched.groups())
        timeline[nb, nc] = split[2]

    return timeline


def get_timeline_descriptions(nb=None):
    return sorted_by_key({k: v for k, v in _get_timeline_descriptions().items() if nb is None or k[0] == nb})
