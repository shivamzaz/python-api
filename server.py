#!/usr/bin/env python

from flask import Flask, request, jsonify
import requests
import json


app = Flask(__name__)


KEY = 'AIzaSyAoGt7dvW1JJDnIkP7ghQbLn6V6imd3eW4'
RADIUS = '500'
TYPES = 'atm'
INVALID_REQUEST = {"error": "Something wrong happend!"}
MAPS_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'


"""
Sample Request:

https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=28.677031,77.501339&radius=500&types=atm&key=AIzaSyAoGt7dvW1JJDnIkP7ghQbLn6V6imd3eW4
"""


def prepare_request(lattitude, longitude, url=MAPS_URL, types=TYPES,
                    radius=RADIUS, key=KEY):
    location = str(lattitude) + ',' + str(longitude)
    url = '%s?location=%s&radius=%s&types=%s&key=%s' % (url, location, radius,
                                                        types, key)
    return url


def get_result(lattitude, longitude):
    url = prepare_request(lattitude, longitude)
    try:
        data = requests.get(url)
        data.raise_for_status()
        data = json.loads(data.content)
    except:
        data = INVALID_REQUEST
    return data


@app.route('/get-atm', methods=['POST'])
def hello_world():
    request_info = request.get_json()
    try:
        lat = request_info['lat']
        lon = request_info['long']
        result = get_result(lat, lon)
    except:
        result = INVALID_REQUEST
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
