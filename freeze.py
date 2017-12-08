from flask_frozen import Freezer
from app import app

freezer = Freezer(app)


@freezer.register_generator
def data_json_book():
    for i in range(1,4):
        yield {'book_number':i}


if __name__ == '__main__':
    freezer.freeze()
