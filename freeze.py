import argparse

from flask_frozen import Freezer
from app import app

freezer = Freezer(app)


@freezer.register_generator
def data_json_book():
    for i in range(1,4):
        yield {'book_number':i}


@freezer.register_generator
def travels_csv_book():
    for i in range(1,4):
        yield {'book_number':i}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('type',default='freeze')
    args = parser.parse_args()
    if args.type == 'serve':
        freezer.serve()
    if args.type == 'run':
        freezer.run()
    if args.type == 'freeze':
        freezer.freeze()
