#!/usr/bin/env python3

# from context import *
from elektro_planner.read_kabel import read_kabel, autogenerate_kabel
from elektro_planner.data import Haus, KabelType, Kabel
from elektro_planner.read_anschluesse import read_anschluesse
from elektro_planner.read_struktur import read_struktur
from elektro_planner.connect_walls import create_nodes_from_walls
from elektro_planner.create_roombook import create_roombook
from elektro_planner.calc_kabel import calc_kabel_len, calc_wires
from elektro_planner.associate_anschluesse import associate_objects_to_walls_and_nodes
import simple_haus
import simple_haus
from pytest import approx


def test_number_of_kabels():
    haus = Haus()
    yaml_data = {
        "kabel": [
            {
                "id": 1,
                "name": "SK1 KiZi 1",
                "start": "1.1.1",
                "end": ["3.3.1", "3.3.2"],
            },
            {
                "id": 2,
                "name": "SK2 KiZi 1",
                "start": "1.1.1",
                "end": ["3.3.3", "3.3.4", "3.3.5"],
            },
        ]
    }
    print(yaml_data)
    read_kabel(haus, yaml_data)
    assert len(haus.kabel) == 2


def test_simple_haus_kabel():
    haus = Haus()
    yaml = simple_haus.define_testcase()

    read_struktur(haus, yaml["struktur"])
    read_anschluesse(haus, yaml["anschluesse"])
    read_kabel(haus, yaml["kabel"])
    autogenerate_kabel(haus)
    create_nodes_from_walls(haus)
    create_roombook(haus)
    assert len(haus.kabel) == 7
    # explicit cable
    assert haus.kabel[0].start == "1.1.1"
    assert len(haus.kabel[0].end) == 3
    assert haus.kabel[0].end[0] == "2.2.3"
    assert haus.kabel[0].end[1] == "2.2.4"
    assert haus.kabel[0].length == approx(2 + 4 + 0.2 + 0.2 + 0.2)
    # impicit definde cabels
    assert haus.kabel[1].start == "1.1.1"
    assert len(haus.kabel[1].end) == 1
    assert haus.kabel[1].end[0] == "1.1.2"
    assert haus.kabel[1].type == KabelType.NYM5x15
    assert haus.kabel[1].length == approx(0.4 + 2.4)
    assert haus.kabel[2].length == approx(3)
    assert haus.kabel[3].end[0] == "2.1.1"
    # directly above it
    assert haus.kabel[3].length == approx(2)
    assert haus.kabel[4].length == approx(2 + 0.4 + 2.4)


def test_indirect_connection():
    haus = Haus()
    yaml = simple_haus.define_testcase()
    read_struktur(haus, yaml["struktur"])
    read_anschluesse(haus, yaml["anschluesse"])
    create_nodes_from_walls(haus)

    assert len(haus.nodes) == 8 + 16
    assert len(haus.geschosse[0].nodes) == 8
    assert len(haus.geschosse[1].nodes) == 16
    associate_objects_to_walls_and_nodes(haus)
    haus.kabel.append(Kabel("2.1.2", "2.2.2"))
    create_roombook(haus)
    assert haus.kabel[0].start == "2.1.2"
    assert haus.kabel[0].end[0] == "2.2.2"
    assert haus.kabel[0].length == approx(1 + 1.5)

    path = calc_kabel_len(haus, haus.kabel[0])
    for e in path:
        print(e)
    assert len(path) == 8
    assert haus.kabel[0].length == approx(1.0 + 2.4 + 1.0 + 0.9 + 1.0)


def test_autogen_kabel_with_astar_len_calc():
    haus = Haus()
    yaml = simple_haus.define_testcase()
    read_struktur(haus, yaml["struktur"])
    read_anschluesse(haus, yaml["anschluesse"])
    # read_kabel(haus,yaml["kabel"])
    autogenerate_kabel(haus)
    create_nodes_from_walls(haus)
    assert len(haus.nodes) == 8 + 16
    haus.geschosse[0].nodes[4].connect(haus.geschosse[1].nodes[0])
    associate_objects_to_walls_and_nodes(haus)
    create_roombook(haus)
    kabel_length_simple = []
    for kabel in haus.kabel:
        kabel_length_simple.append(kabel.length)

    calc_wires(haus)
    for i, kabel in enumerate(haus.kabel):
        if kabel_length_simple[i] != kabel.length:
            print(
                "Kabel Length differs: {} {} {}".format(
                    kabel.end[0], kabel_length_simple[i], kabel.length
                )
            )

    # for i,kabel in enumerate(haus.kabel):
    #     assert kabel_length_simple[i] == approx(kabel.length)


def test_autogenerate_kabels():
    haus = Haus()
    yaml = simple_haus.define_testcase()

    yaml["anschluesse"] = {
        "geschosse": [
            {
                "id": 1,
                "name": "G1",
                "rooms": [
                    {
                        "id": 1,
                        "name": "R11",
                        "objects": [
                            {
                                "id": 1,
                                "name": "O111",
                                "con-type": "steckdose",
                                "anzahl": 1,
                                "pos": {"hori": [20, 150], "vert": "oben"},
                            },
                            {
                                "id": 2,
                                "name": "O112",
                                "con-type": "knx",
                                "knx-component": "gt",
                                "pos": {"hori": [200, 20], "vert": "oben"},
                            },
                            {
                                "id": 3,
                                "name": "O113",
                                "con-type": "knx",
                                "knx-component": "pm",
                                "pos": {"hori": [350, 20], "vert": "oben"},
                            },
                        ],
                    }
                ],
            }
        ]
    }
    yaml["kabel"] = {"kabel": []}
    read_struktur(haus, yaml["struktur"])
    read_anschluesse(haus, yaml["anschluesse"])
    read_kabel(haus, yaml["kabel"])
    autogenerate_kabel(haus)
    create_roombook(haus)
    assert len(haus.kabel) == 1
    assert haus.kabel[0].length == approx(1.30 + 3.30)

    haus.kabel = []
    read_kabel(haus, yaml["kabel"])
    autogenerate_kabel(haus, False)
    create_roombook(haus)
    assert len(haus.kabel) == 2
    assert haus.kabel[0].length == approx(1.30 + 1.80)
    assert haus.kabel[1].length == approx(1.30 + 3.30)
