import os

from flask import current_app
from flask_script import Manager, Server

from app import create_app, db
from entry import import_combined
from generator.out.data import data_json as get_data_json
from generator.out.travels import get_travels_book_json, get_travels_book_csv


class CustomServer(Server):
    def __call__(self, app, *args, **kwargs):
        with app.app_context():
            with app.app_context():
                custom_call()
                return Server.__call__(self, app, *args, **kwargs)


def custom_call():
    c_app = current_app
    db.init_app(c_app)
    db.create_all()


    import_combined(os.path.join('data', 'Combined.txt'))

    # cache warmup
    cached = get_data_json()
    cached2 = get_travels_book_json()
    cached3 = get_travels_book_csv()


if __name__ == '__main__':
    app = create_app()
    manager = Manager(app)
    manager.add_command('runserver', CustomServer)
    manager.run()
