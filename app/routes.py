from os import urandom
from datetime import datetime, timedelta
from pytz import utc
import json

from app import app, db
from flask import request, jsonify

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
            'lat': data['lat'],
            'lng': data['lng'],
            'ts':  int(datetime.timestamp(datetime.now())),
            'user': user
        })
    return '', 200

@app.route('/read', methods=['GET'])
def read():
    data = request.form.to_dict()
    if data['etime'] == -1: data['etime'] = int(datetime.timestamp(datetime.now()))
    cords = db.cords.find(
        {
            'user.token': data['token'],
            'ts': {
                '$gte': data['stime'],
                '$lte': data['etime']
            }
        },
        {'lat': 1, 'lng': 1, 'ts': 1, '_id': 0}
    )
    return jsonify(list(cords))