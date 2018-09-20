from app import create_app
from generator.links import postprocess_scut_links, import_links
from generator.travels import get_travels_dict, import_chapter_characters_travels

app = create_app({'SQLALCHEMY_DATABASE_URI': 'sqlite:///bobiverse.db'})

with app.app_context():
    postprocess_scut_links()