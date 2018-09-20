import os

from flask_script import Manager, Server, Command
from flask_frozen import Freezer

from app import create_app, db
from entry import import_combined
from generator.nl import download_ntlk


class ImportData(Command):
    def run(self):
        db.init_app(app)
        db.create_all()

        download_ntlk()

        import_combined(os.path.join('data', 'Combined.txt'))


def get_freezer(app):
    freezer = Freezer(app)

    @freezer.register_generator
    def data_json_book():
        for i in range(1,4):
            yield 'main.data_json_book', {'book_number':i}

    @freezer.register_generator
    def travels_csv_book():
        for i in range(1,4):
            yield 'main.travels_csv_book', {'book_number':i}

    return freezer


if __name__ == '__main__':
    app = create_app()
    manager = Manager(app)
    freezer = get_freezer(app)
    freezer_manager = Manager(app)

    serve = freezer_manager.command(freezer.serve)
    run = freezer_manager.command(freezer.run)
    freeze = freezer_manager.command(freezer.freeze)

    manager.add_command('freeze', freezer_manager)
    manager.add_command('runserver', Server)
    manager.add_command('importdata', ImportData)

    manager.run()
