from app import create_app
from generator.chapter_characters import postprocess_chapter_characters

app = create_app()

with app.app_context():
    postprocess_chapter_characters()