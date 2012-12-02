#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

"""
main.py

Created by Lorenzo Setale.
Copyright (c) 2012 Lorenzo Setale. All rights reserved.
"""

from django.utils.encoding import smart_str

from flask import Flask, render_template, session, url_for, abort, redirect, flash, request
from werkzeug.contrib.cache import FileSystemCache
from functools import wraps

import json

import sys
import os
import datetime
import time

app = Flask(__name__)
app.secret_key = 'ksgnaigjsaoughowearsugobxg7r8aglsuhpao9sef8jsofalsjfaòoseguf'
app.debug = True

from chouse import Poi

if not os.path.isdir("/tmp/chouse-cache"):
    os.mkdir("/tmp/chouse-cache")

cache = FileSystemCache(cache_dir="/tmp/opinionbag-cache")
def cached(timeout=5, key='view/%s'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator

from pymongo import Connection, ASCENDING, DESCENDING

db_connection =  Connection("localhost", 27017, network_timeout=30, socketTimeoutMS=20000, connectTimeoutMS=30000)
db = db_connection["app9597564"]

#[section] Common functions for server
@app.route('/static/<path:afilepath>')
def serve_static(afilepath):
    return redirect(url_for('static', filename=afilepath))

#[section] Index part
@app.route("/")
def homepage():
    return render_template('homepage.html', page="homepage")

@app.route("/search")
def search_page():
    return render_template('search.html', page="search")

@app.route("/p/<point_id>")
def point_data(point_id):
    search = self.database.houses.find_one({"id": self.id})
    if not (search):
        abort(404)
    point = Poi(0,0).by_dictionary(search)
    return render_template('point.html', page="point", point=point)

@app.route("/api")
def api_is_working():
    return json.dumps({"status":True})

@app.route("/api/points")
def api_points():    
    return json.dumps([{"title":"Titolo", "coordinates":{"lat":"41.8493344", "lng":"12.4755884"}, "link":"http://google.com"}])

@app.route("/api/point/<point_id>")
def api_point(point_id):
    output = dict()
    return json.dumps(output)


if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

