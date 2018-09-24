from flask import jsonify, render_template, Response
from flask.blueprints import Blueprint

from generator.characters import get_bob_characters, get_bob_styles, get_characters
from generator.locations import get_locations
from generator.out.cooccurences import get_cooccurences_json
from generator.out.data import data_json as get_data_json
from generator.out.genealogy import get_genealogy
from generator.out.travels import get_travels_book_json, get_travels_book_csv

main = Blueprint('main', 'name')


@main.route('/locations.json')
def locations():
    return jsonify(get_locations())


@main.route('/bob_characters.json')
def bob_characters():
    return jsonify(get_bob_characters())


@main.route('/characters.json')
def all_characters():
    return jsonify(get_characters())


@main.route('/locations.json')
def all_locations():
    return jsonify(get_locations())


@main.route('/css/bob_styles.css')
def bob_styles():
    return Response(get_bob_styles(), mimetype='text/css')


@main.route('/book/<int:book_number>/data.json')
def data_json_book(book_number):
    return jsonify(get_data_json(book_number))


@main.route('/data.json')
def data_json():
    return jsonify(get_data_json())


@main.route('/book/<int:book_number>/travels.json')
def travels_json_book(book_number):
    return jsonify(get_travels_book_json(book_number))


@main.route('/travels.json')
def travels_json():
    return jsonify(get_travels_book_json())


@main.route('/book/<int:book_number>/travels.csv')
def travels_csv_book(book_number):
    return Response(get_travels_book_csv(book_number), mimetype='text/csv')


@main.route('/travels.csv')
def travels_csv():
    return Response(get_travels_book_csv(), mimetype='text/csv')


@main.route('/cooccurences.json')
def cooccurences_json():
    return jsonify(get_cooccurences_json())


@main.route('/genealogy.json')
def genealogy_json():
    return jsonify(get_genealogy())


@main.route('/book/<int:book_number>/cooccurences.json')
def cooccurences_json_book(book_number):
    return jsonify(get_cooccurences_json(book_number))


@main.route('/')
def index_view():
    return render_template('narrative_chart.html')


@main.route('/timeline.html')
def timeline_view():
    return render_template('timeline.html')


@main.route('/cooccurrences.html')
def cooccurences_view():
    return render_template('cooccurrences.html')


@main.route('/genealogy.html')
def genealogy_view():
    return render_template('genealogy.html')
