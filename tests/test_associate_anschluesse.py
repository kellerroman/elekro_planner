#!/usr/bin/env python3

# from context import *
from elektro_planner.data import Haus
from elektro_planner.read_anschluesse import read_anschluesse
from elektro_planner.read_struktur import read_struktur
from elektro_planner.connect_walls import connect_walls
from elektro_planner.associate_anschluesse import associate_anschluesse
import simple_haus
from pytest import approx

def test_simple_haus_kabel():
    haus = Haus()
    yaml = simple_haus.define_testcase_simple1()

    read_struktur(haus,yaml["struktur"])
    read_anschluesse(haus,yaml["anschluesse"])
    connect_walls(haus)
    associate_anschluesse(haus)

    assert haus.geschosse[0].rooms[0].objects[0].associated_wall == haus.geschosse[0].walls[1]
    assert haus.geschosse[0].rooms[0].objects[1].associated_wall == haus.geschosse[0].walls[0]

    assert len(haus.geschosse[0].walls[0].edges) == 7
    e =  haus.geschosse[0].walls[0].edges
    # connection to the new edge on the "floor"
    assert e[0].connections[0].id == e[5].id
    # connection to the upper egde
    assert e[0].connections[2].id == e[2].id
    assert e[5].connections[2].id == e[4].id
    assert e[4].connections[0].id == e[5].id
    assert e[4].connections[1].id == e[6].id
