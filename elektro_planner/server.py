#!/usr/bin/env python3

from flask import Flask, render_template, request

app = Flask(__name__)
from elektro_planner.read_setup import read_setup
from elektro_planner.create_svg import create_svg
from elektro_planner.create_roombook import create_roombook
from elektro_planner.associate_anschluesse import associate_objects_to_walls_and_nodes
from elektro_planner.calc_kabel import calc_wires


@app.route("/")
def mainpage():
    yaml_file = "data/setup.yaml"
    house = read_setup(yaml_file)
    associate_objects_to_walls_and_nodes(house)
    calc_wires(house)
    svgs = create_svg(house)
    create_roombook(house)
    return render_template(
        "menu.html",
        grundriss_ug=svgs[0],
        grundriss_eg=svgs[1],
        grundriss_og=svgs[2],
        haus=house,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0")
