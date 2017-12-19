from flask import Flask, jsonify, render_template, Response
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from generator.characters import get_bob_characters, get_bob_styles
from generator.travels_out import get_travels_book_json, get_travels_book_csv
from generator.locations import get_locations
from generator.data import data_json as get_data_json
from generator.utils import ObjectEncoder

app = Flask('Bobiverse visualisations')
app.config['FREEZER_DESTINATION'] = 'docs'
app.json_encoder = ObjectEncoder

nav = Nav()
bootstrap = Bootstrap(app)


@app.route('/locations.json')
def locations():
    return jsonify(get_locations())


@app.route('/bob_characters.json')
def bob_characters():
    return jsonify(get_bob_characters())


@app.route('/css/bob_styles.css')
def bob_styles():
    return Response(get_bob_styles(), mimetype='text/css')


@app.route('/book/<int:book_number>/data.json')
def data_json_book(book_number):
    return jsonify(get_data_json(book_number))


@app.route('/data.json')
def data_json():
    return jsonify(get_data_json())


@app.route('/book/<int:book_number>/travels.json')
def travels_json_book(book_number):
    return jsonify(get_travels_book_json(book_number))


@app.route('/travels.json')
def travels_json():
    return jsonify(get_travels_book_json())


@app.route('/book/<int:book_number>/travels.csv')
def travels_csv_book(book_number):
    return Response(get_travels_book_csv(book_number), mimetype='test/csv')


@app.route('/travels.csv')
def travels_csv():
    return Response(get_travels_book_csv(), mimetype='test/csv')


@app.route('/')
def index_view():
    return render_template('narrative_chart.html')


@app.route('/timeline.html')
def timeline_view():
    return render_template('timeline.html')


@nav.navigation()
def navbar():
    return Navbar(
        'Bobiverse',
        View('Narrative Chart', 'index_view'),
        View('Timeline Travels', 'timeline_view'),
    )


nav.init_app(app)


if __name__ == '__main__':
    # cache warmup
    cached = get_data_json()
    cached2 = get_travels_book_json()
    cached3 = get_travels_book_csv()
    app.run(host='0.0.0.0', port=8000, debug=True)