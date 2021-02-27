#!/usr/bin/env python3

from elektro_planner.read_anschluesse import read_anschluesse
from elektro_planner.read_struktur import read_struktur
from elektro_planner.connect_walls import connect_walls
from elektro_planner.data import Haus
from elektro_planner.create_svg import create_svg
import simple_haus
def test_read_struktur():
    haus = Haus()
    yaml = simple_haus.define_testcase()

    read_struktur(haus,yaml["struktur"])
    read_anschluesse(haus,yaml["anschluesse"])
    connect_walls(haus)
    create_svg(haus)

    assert len(haus.edges) == 24
    assert len(haus.geschosse) == 2
    assert len(haus.geschosse[0].walls) == 2
    edges = haus.geschosse[0].edges
    assert len(edges) == 8

    # for e in edges:
    #     print("Edge: {}".format(e))
    #     for c in e.connections:
    #         print("-- connected to {}".format(c))

    assert len(edges[0].connections) == 3
    assert edges[0].connections[0] == edges[1]
    assert edges[0].connections[1] == edges[2]
    assert edges[0].connections[2] == edges[4]
    assert len(edges[1].connections) == 2
    assert edges[1].connections[0] == edges[0]
    assert edges[1].connections[1] == edges[5]
    assert len(edges[2].connections) == 3
    assert edges[2].connections[0] == edges[3]
    assert edges[2].connections[1] == edges[0]
    assert edges[2].connections[2] == edges[6]
    assert len(edges[3].connections) == 2
    assert edges[3].connections[0] == edges[2]
    assert edges[3].connections[1] == edges[7]

#  upper edges
    assert len(edges[4].connections) == 3
    assert edges[4].connections[0] == edges[0]
    assert edges[4].connections[1] == edges[5]
    assert edges[4].connections[2] == edges[6]
    assert len(edges[5].connections) == 2
    assert edges[5].connections[0] == edges[1]
    assert edges[5].connections[1] == edges[4]
    assert len(edges[6].connections) == 3
    assert edges[6].connections[0] == edges[2]
    assert edges[6].connections[1] == edges[4]
    assert edges[6].connections[2] == edges[7]
    assert len(edges[7].connections) == 2
    assert edges[7].connections[0] == edges[3]
    assert edges[7].connections[1] == edges[6]

## obergeschoss
    assert len(haus.geschosse[1].walls) == 4
    edges = haus.geschosse[1].edges
    # for e in edges:
    #     print("Edge: {}".format(e))
    #     for c in e.connections:
    #         print("-- connected to {}".format(c))
    assert len(edges) == 16
    assert len(edges[0].connections) == 3
    assert edges[0].connections[0].id == edges[1].id
    assert edges[0].connections[1].id == edges[2].id
    assert edges[0].connections[2].id == edges[8].id
    assert len(edges[1].connections) == 2
    assert edges[1].connections[0].id == edges[0].id
    assert edges[1].connections[1].id == edges[9].id
    assert len(edges[2].connections) == 3
    assert edges[2].connections[0].id == edges[6].id
    assert edges[2].connections[1].id == edges[0].id
    assert edges[2].connections[2].id == edges[10].id
    assert len(edges[3].connections) == 3
    assert edges[3].connections[0].id == edges[6].id
    assert edges[3].connections[1].id == edges[4].id
    assert edges[3].connections[2].id == edges[11].id
    assert len(edges[4].connections) == 3
    assert edges[4].connections[0].id == edges[5].id
    assert edges[4].connections[1].id == edges[3].id
    assert edges[4].connections[2].id == edges[13].id
    assert len(edges[5].connections) == 2
    assert edges[5].connections[0].id == edges[4].id
    assert edges[5].connections[1].id == edges[14].id
    assert len(edges[6].connections) == 4
    assert edges[6].connections[0].id == edges[7].id
    assert edges[6].connections[1].id == edges[2].id
    assert edges[6].connections[2].id == edges[3].id
    assert edges[6].connections[3].id == edges[12].id
    assert len(edges[7].connections) == 2
    assert edges[7].connections[0].id == edges[6].id
    assert edges[7].connections[1].id == edges[15].id
    # upper edges
    assert len(edges[8].connections) == 3
    assert edges[8].connections[0].id == edges[0].id
    assert edges[8].connections[1].id == edges[9].id
    assert edges[8].connections[2].id == edges[10].id
    assert len(edges[9].connections) == 2
    assert edges[9].connections[0].id == edges[1].id
    assert edges[9].connections[1].id == edges[8].id
    assert len(edges[10].connections) == 3
    assert edges[10].connections[0].id == edges[2].id
    assert edges[10].connections[1].id == edges[8].id
    assert edges[10].connections[2].id == edges[12].id
    assert len(edges[11].connections) == 3
    assert edges[11].connections[0].id == edges[3].id
    assert edges[11].connections[1].id == edges[12].id
    assert edges[11].connections[2].id == edges[13].id
    assert len(edges[12].connections) == 4
    assert edges[12].connections[0].id == edges[6].id
    assert edges[12].connections[1].id == edges[10].id
    assert edges[12].connections[2].id == edges[11].id
    assert edges[12].connections[3].id == edges[15].id
    assert len(edges[13].connections) == 3
    assert edges[13].connections[0].id == edges[4].id
    assert edges[13].connections[1].id == edges[11].id
    assert edges[13].connections[2].id == edges[14].id
    assert len(edges[14].connections) == 2
    assert edges[14].connections[0].id == edges[5].id
    assert edges[14].connections[1].id == edges[13].id
    assert len(edges[15].connections) == 2
    assert edges[15].connections[0].id == edges[7].id
    assert edges[15].connections[1].id == edges[12].id
