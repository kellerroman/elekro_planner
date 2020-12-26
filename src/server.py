#!/usr/bin/env python3

from flask import Flask, render_template, request
app = Flask(__name__)
from svg_drawer import create_svg
from read_setup import read_setup

@app.route('/')
def mainpage():
    yaml_file= "data/setup.yaml"
    svg_eg = create_svg(read_setup(yaml_file))
    return render_template('menu.html',grundriss_eg=svg_eg)

if __name__ == '__main__':
   app.run(host="0.0.0.0")
