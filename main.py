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
    return json.dumps({"Does it works": True})

if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

