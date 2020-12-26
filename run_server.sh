#!/usr/bin/env bash
firefox http://127.0.0.1:5000/
FLASK_APP=src/server.py FLASK_ENV=development flask run
