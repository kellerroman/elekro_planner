#!/usr/bin/env python3

from flask import Flask, render_template, request
app = Flask(__name__)
from elektro_planner.read_setup import read_setup
from elektro_planner.create_svg import create_svg
from elektro_planner.create_roombook import create_roombook

@app.route('/')
def mainpage():
    yaml_file= "data/setup.yaml"
    house = read_setup(yaml_file)
    svgs = create_svg(house)
    create_roombook(house)
    return render_template('menu.html',grundriss_ug=svgs[0],grundriss_eg=svgs[1], grundriss_og=svgs[2], haus = house)

if __name__ == '__main__':
   app.run(host="0.0.0.0")
