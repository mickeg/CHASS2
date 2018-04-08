import flask
from flask import request, jsonify
import xmltodict
from ArtDatabanken import ArtDatabanken
import json

app = flask.Flask(__name__)
app.debug = True


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/', methods=['GET'])
def home():
    return '''<h1>CHASS</h1><p>Main Page. Hello animals.</p>'''

@app.route('/api/v1/observations', methods=['GET'])
def api_filter():
    taxonId = -1
    query_parameters = request.args
    taxonId = query_parameters.get('TaxonID')
    if taxonId is None:
        return 'TaxonID is not provided.'
    adb = ArtDatabanken()
    adb.ping()
    result = adb.getSpeciesObservationCoordinatesBySearchCriteria(taxonId)
    return result


@app.route('/api/v1/ping', methods=['GET'])
def api_ping():
    return 'Ping. ArtdatabankenSOA Service is up.'

@app.route('/api/v1/methods', methods=['GET'])
def api_methods():
    adb = ArtDatabanken()
    result = adb.getListOfMethods()
    return str(result)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>No animals were hurt.</p>", 404


app.run()
