from flask import Flask, jsonify, request, render_template, send_from_directory, Response

from genealogy import get_genealogy, get_bob_styles
from locations import get_locations
from write_data_json import get_data_json

app = Flask('Bobiverse visualisations')
app.config['FREEZER_DESTINATION'] = 'docs'


@app.route('/locations.json')
def locations():
    return jsonify(get_locations())


@app.route('/bob_characters.json')
def bob_characters():
    return jsonify(get_genealogy())


@app.route('/css/bob_styles.css')
def bob_styles():
    return Response(get_bob_styles(), mimetype='text/css')


@app.route('/book/<int:book_number>/data.json')
def data_json_book(book_number):
    return jsonify(get_data_json(book_number))


@app.route('/data.json')
def data_json():
    return jsonify(get_data_json())


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    # cache warmup
    cached = get_data_json()
    app.run(host='0.0.0.0', port=8000, debug=True)