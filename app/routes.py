from os import urandom, getenv
from datetime import datetime, timedelta
from pytz import utc
import json

from app import app, db
from flask import request, jsonify, render_template

@app.route('/')
def index():
    data = request.args.to_dict()
    user = db.users.find_one({'token': data['token']})
    return render_template('index.html', token=user['token'])

@app.route('/signup', methods=['POST'])
def register():
    user = request.form.to_dict()
    user['token'] = urandom(32).hex()

    db.users.update({'username': user['username']}, {'$set': user}, upsert=True)
    return jsonify({'response': {'token': user['token'] }})

@app.route('/write', methods=['POST'])
def write():
    data = request.form.to_dict()
    user = db.users.find_one({'token': data['token']})
    if user:
        db.cords.insert_one({
            'lat': float(data['lat']),
            'lng': float(data['lng']),
            'ts':  int(datetime.timestamp(datetime.now())),
            'user': user
        })
    return '', 200

@app.route('/read', methods=['GET'])
def read():
    data = request.args.to_dict()
    if int(data['etime']) == -1: data['etime'] = int(datetime.timestamp(datetime.now()))

    cords = db.cords.find(
        {
            'user.token': data['token'],
            'ts': {
                '$gte': int(data['stime']),
                '$lte': int(data['etime'])
            }
        },
        {'lat': 1, 'lng': 1, 'ts': 1, '_id': 0}
    )
    cords = map(lambda el: {'lat': float(el['lat']), 'lng': float(el['lng']), 'ts': el['ts']}, cords)
    return jsonify(list(cords))

@app.route('/maps_token', methods=['GET'])
def token():
    return app.config['GOOGLE_MAPS_API_TOKEN']

if getenv('FLASK_ENV') == 'development':
    @app.route('/all', methods=['GET'])
    def all():
        return jsonify({
            "users": list(db.users.find()),
            "cords": list(db.cords.find())
        })