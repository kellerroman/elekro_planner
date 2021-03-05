#!/usr/bin/env python3

from elektro_planner.read_setup import read_setup
from elektro_planner.create_roombook import create_roombook
from elektro_planner.calc_kabel import calc_wires
from elektro_planner.associate_anschluesse import associate_objects_to_walls_and_nodes
from pytest import approx


def test_fully_house():
    yaml_file = "data/setup.yaml"
    haus = read_setup(yaml_file)

    haus.geschosse[0].nodes[0].connect(haus.geschosse[1].nodes[0])
    haus.geschosse[1].nodes[0].connect(haus.geschosse[2].nodes[0])
    associate_objects_to_walls_and_nodes(haus)
    #
    # create_roombook(haus)
    #
    calc_wires(haus)
