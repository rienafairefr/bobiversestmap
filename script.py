from app import create_app
from generator.links import import_links
from generator.out.cooccurences import get_cooccurences_json

app = create_app()

with app.app_context():
    coocurrences = get_cooccurences_json()