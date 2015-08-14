#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
from pymongo import MongoClient
from dateutil import parser
from datetime import datetime
from hashlib import md5

app = Flask(__name__)

client = MongoClient()
db = client['storage']
users = db['users']


@app.route('/add', methods=['POST'])
def add_entry():
    """Reads JSON entries, checks their md5checksums and stores only valid entries in db, discards the rest."""
    all_entries = True
    entries = request.get_json(force=True, silent=True)
    app.logger.debug('[add_entry] Entries: %s' % request.data)
    if type(entries) == list:
        for entry in entries[:]:
            uid, name, date, md5checksum = (entry.get('uid'), entry.get('name'), entry.get('date'), entry.get('md5checksum'))
            checksum_string = '{"date": "%s", "uid": "%s", "name": "%s"}' % (date, uid, name)
            checksum = md5(checksum_string).hexdigest()
            if checksum != md5checksum:
                app.logger.debug('[add_entry] Checksum mismatch: %s' % entry)
                entries.remove(entry)
                all_entries = False
            else:
                try:
                    entry['uid'] = int(uid)
                    entry['date'] = parser.parse(date if date else None)
                except (ValueError, TypeError, AttributeError, KeyError):
                    app.logger.debug('[add_entry] Invalid format: %s' % entry)
                    entries.remove(entry)
                    all_entries = False
        if entries:
            users.insert_many(entries)
            if all_entries:
                return jsonify(success='true', message='All entries added')
            else:
                return jsonify(success='true', message='Only some entries added (checksum mismatch or invalid format)')
        else:
            return jsonify(success='false', message='No entries added (checksum mismatch or invalid format)')
    else:
        app.logger.error('[add_entry] Invalid input: %s' % request.data)
        return jsonify(success='false', message='Invalid input'), 400


@app.route('/show', methods=['GET'])
def show_entry():
    """Shows the number of occurrences of an uid on a given date."""
    app.logger.debug('[show_entry] Parameters: ?%s' % request.query_string)
    counter = 0
    try:
        uid = int(request.args.get('uid'))
        date = request.args.get('date')
        date = parser.parse(date if date else None)
    except (ValueError, TypeError, AttributeError):
        app.logger.error('[show_entry] Invalid parameters: %s' % request.args)
        return jsonify(success='false', message='Invalid parameters'), 400
    if uid and date:
        start = datetime(date.year, date.month, date.day, 0, 0, 0)
        end = datetime(date.year, date.month, date.day, 23, 59, 59)
        for user in users.find({'uid': uid, 'date': {'$gte': start, '$lte': end}}):
            counter += 1
        return jsonify(success='true', uid=uid, date=request.args.get('date'), occurrences=counter)
    else:
        app.logger.error('[show_entry] Invalid parameters: %s' % request.args)
        return jsonify(success='false', message='Invalid parameters'), 400

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
