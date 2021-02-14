from app import create_app
from generator.links import postprocess_scut_links
from generator.out.genealogy import get_genealogy
from generator.out.travels import get_travels_book_json, get_travels_book_csv

app = create_app()

with app.app_context():
    get_genealogy()
