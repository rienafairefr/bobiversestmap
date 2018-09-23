from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_sqlalchemy import SQLAlchemy

from generator.utils import ObjectEncoder

nav = Nav()
bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app(config_dict=None):
    from generator.blueprints import main
    app = Flask('Bobiverse visualisations')
    app.config['FREEZER_DESTINATION'] = 'docs'
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///bobiverse.db?check_same_thread=False"
    app.config['SQLALCHEMY_ECHO'] = True # for debugging db problems
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.json_encoder = ObjectEncoder

    if config_dict is not None:
        app.config.from_mapping(config_dict)

    nav.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    app.register_blueprint(main)

    return app


@nav.navigation()
def navbar():
    return Navbar(
        'Bobiverse',
        View('Narrative Chart', 'main.index_view'),
        View('Timeline Travels', 'main.timeline_view'),
        View('Cooccurences Matrix', 'main.cooccurences_view'),
    )
