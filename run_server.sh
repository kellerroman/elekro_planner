#!/usr/bin/env bash
firefox http://127.0.0.1:5000/
FLASK_APP=elektro_planner/server.py FLASK_ENV=development flask run
