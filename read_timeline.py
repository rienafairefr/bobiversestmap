import os
import re

from utils import json_dump, memoize


def strip(li):
    return [l.strip() for l in li]

@memoize()
def read_timeline():
    lines = open(os.path.join('public_data','timeline_books_1-3.txt'),encoding='utf-8').readlines()
    lines = strip(lines)

    timeline = []
    for line in lines:
        line = line.strip().split(';')[0]
        if len(line)==0:
            continue
        split = strip(line.split('-'))
        matched = re.match('B(\d+)C(\d+)',split[1])
        nb,nc = (int(i) for i in matched.groups())
        timeline.append((nb, nc, split[2]))

    timeline = sorted(timeline, key = lambda el: (el[0], el[1]))

    json_dump([t[2] for t in timeline], open(os.path.join('generated','timeline.json'),'w', encoding='utf-8'))




if __name__ == '__main__':
    read_timeline()