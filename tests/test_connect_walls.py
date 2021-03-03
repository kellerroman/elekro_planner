#!/usr/bin/env python3

from elektro_planner.read_anschluesse import read_anschluesse
from elektro_planner.read_struktur import read_struktur
from elektro_planner.connect_walls import create_nodes_from_walls
from elektro_planner.data import Haus
from elektro_planner.create_svg import create_svg
import simple_haus


def test_read_struktur():
    haus = Haus()
    yaml = simple_haus.define_testcase()

    read_struktur(haus, yaml["struktur"])
    read_anschluesse(haus, yaml["anschluesse"])
    create_nodes_from_walls(haus)
    create_svg(haus)

    assert len(haus.nodes) == 24
    assert len(haus.geschosse) == 2
    assert len(haus.geschosse[0].walls) == 2
    nodes = haus.geschosse[0].nodes
    assert len(nodes) == 8

    # for e in nodes:
    #     print("Edge: {}".format(e))
    #     for c in e.get_connected_nodes():
    #         print("-- connected to {}".format(c))

    assert len(nodes[0].get_connected_nodes()) == 3
    assert nodes[0].get_connected_nodes()[0] == nodes[1]
    assert nodes[0].get_connected_nodes()[1] == nodes[2]
    assert nodes[0].get_connected_nodes()[2] == nodes[4]
    assert len(nodes[1].get_connected_nodes()) == 2
    assert nodes[1].get_connected_nodes()[0] == nodes[0]
    assert nodes[1].get_connected_nodes()[1] == nodes[5]
    assert len(nodes[2].get_connected_nodes()) == 3
    assert nodes[2].get_connected_nodes()[0] == nodes[3]
    assert nodes[2].get_connected_nodes()[1] == nodes[0]
    assert nodes[2].get_connected_nodes()[2] == nodes[6]
    assert len(nodes[3].get_connected_nodes()) == 2
    assert nodes[3].get_connected_nodes()[0] == nodes[2]
    assert nodes[3].get_connected_nodes()[1] == nodes[7]

    #  upper nodes
    assert len(nodes[4].get_connected_nodes()) == 3
    assert nodes[4].get_connected_nodes()[0] == nodes[0]
    assert nodes[4].get_connected_nodes()[1] == nodes[5]
    assert nodes[4].get_connected_nodes()[2] == nodes[6]
    assert len(nodes[5].get_connected_nodes()) == 2
    assert nodes[5].get_connected_nodes()[0].id == nodes[4].id
    assert nodes[5].get_connected_nodes()[1].id == nodes[1].id
    assert len(nodes[6].get_connected_nodes()) == 3
    assert nodes[6].get_connected_nodes()[0] == nodes[4]
    assert nodes[6].get_connected_nodes()[1] == nodes[2]
    assert nodes[6].get_connected_nodes()[2] == nodes[7]
    assert len(nodes[7].get_connected_nodes()) == 2
    assert nodes[7].get_connected_nodes()[0] == nodes[6]
    assert nodes[7].get_connected_nodes()[1] == nodes[3]

    ## obergeschoss
    assert len(haus.geschosse[1].walls) == 4
    nodes = haus.geschosse[1].nodes
    assert len(nodes) == 16
    for i, e in enumerate(nodes):
        print("Node: {}".format(e))
        for c in e.get_connected_nodes():
            print("-- connected to {}".format(c))
        if i < 8:  # nodes at bottom of the wall
            assert e.z == 200
        else:  # nodes at top of the wall
            assert e.z == 500

    assert len(nodes[0].get_connected_nodes()) == 3
    assert nodes[0].get_connected_nodes()[0].id == nodes[1].id
    assert nodes[0].get_connected_nodes()[1].id == nodes[2].id
    assert nodes[0].get_connected_nodes()[2].id == nodes[8].id
    assert len(nodes[1].get_connected_nodes()) == 2
    assert nodes[1].get_connected_nodes()[0].id == nodes[0].id
    assert nodes[1].get_connected_nodes()[1].id == nodes[9].id
    assert len(nodes[2].get_connected_nodes()) == 3
    assert nodes[2].get_connected_nodes()[0].id == nodes[6].id
    assert nodes[2].get_connected_nodes()[1].id == nodes[0].id
    assert nodes[2].get_connected_nodes()[2].id == nodes[10].id
    assert len(nodes[3].get_connected_nodes()) == 3
    assert nodes[3].get_connected_nodes()[0].id == nodes[4].id
    assert nodes[3].get_connected_nodes()[1].id == nodes[6].id
    assert nodes[3].get_connected_nodes()[2].id == nodes[11].id
    assert len(nodes[4].get_connected_nodes()) == 3
    assert nodes[4].get_connected_nodes()[0].id == nodes[5].id
    assert nodes[4].get_connected_nodes()[1].id == nodes[3].id
    assert nodes[4].get_connected_nodes()[2].id == nodes[13].id
    assert len(nodes[5].get_connected_nodes()) == 2
    assert nodes[5].get_connected_nodes()[0].id == nodes[4].id
    assert nodes[5].get_connected_nodes()[1].id == nodes[14].id
    assert len(nodes[6].get_connected_nodes()) == 4
    assert nodes[6].get_connected_nodes()[0].id == nodes[7].id
    assert nodes[6].get_connected_nodes()[1].id == nodes[2].id
    assert nodes[6].get_connected_nodes()[2].id == nodes[3].id
    assert nodes[6].get_connected_nodes()[3].id == nodes[12].id
    assert len(nodes[7].get_connected_nodes()) == 2
    assert nodes[7].get_connected_nodes()[0].id == nodes[6].id
    assert nodes[7].get_connected_nodes()[1].id == nodes[15].id
    # upper nodes
    assert len(nodes[8].get_connected_nodes()) == 3
    assert nodes[8].get_connected_nodes()[0].id == nodes[0].id
    assert nodes[8].get_connected_nodes()[1].id == nodes[9].id
    assert nodes[8].get_connected_nodes()[2].id == nodes[10].id
    assert len(nodes[9].get_connected_nodes()) == 2
    assert nodes[9].get_connected_nodes()[0].id == nodes[8].id
    assert nodes[9].get_connected_nodes()[1].id == nodes[1].id
    assert len(nodes[10].get_connected_nodes()) == 3
    assert nodes[10].get_connected_nodes()[0].id == nodes[8].id
    assert nodes[10].get_connected_nodes()[1].id == nodes[2].id
    assert nodes[10].get_connected_nodes()[2].id == nodes[12].id
    assert len(nodes[11].get_connected_nodes()) == 3
    assert nodes[11].get_connected_nodes()[0].id == nodes[3].id
    assert nodes[11].get_connected_nodes()[1].id == nodes[12].id
    assert nodes[11].get_connected_nodes()[2].id == nodes[13].id
    assert len(nodes[12].get_connected_nodes()) == 4
    assert nodes[12].get_connected_nodes()[0].id == nodes[10].id
    assert nodes[12].get_connected_nodes()[1].id == nodes[11].id
    assert nodes[12].get_connected_nodes()[2].id == nodes[6].id
    assert nodes[12].get_connected_nodes()[3].id == nodes[15].id
    assert len(nodes[13].get_connected_nodes()) == 3
    assert nodes[13].get_connected_nodes()[0].id == nodes[11].id
    assert nodes[13].get_connected_nodes()[1].id == nodes[4].id
    assert nodes[13].get_connected_nodes()[2].id == nodes[14].id
    assert len(nodes[14].get_connected_nodes()) == 2
    assert nodes[14].get_connected_nodes()[0].id == nodes[13].id
    assert nodes[14].get_connected_nodes()[1].id == nodes[5].id
    assert len(nodes[15].get_connected_nodes()) == 2
    assert nodes[15].get_connected_nodes()[0].id == nodes[12].id
    assert nodes[15].get_connected_nodes()[1].id == nodes[7].id
