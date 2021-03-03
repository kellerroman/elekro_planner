#!/usr/bin/env python3

# from context import *
from elektro_planner.read_struktur import read_struktur
from elektro_planner.data import Haus


def test_read_struktur():
    haus = Haus()
    yaml_data = {
        "geschosse": [
            {
                "id": 1,
                "name": "untergeschoss",
                "height": 236,
                "walls": [
                    {"id": 1, "pos": {"hori": [25, 0]}, "ende": [36.5, 1049]},
                    {
                        "id": 2,
                        "pos": {"hori": [25, 0]},
                        "ende": ["36.5+576+11.5", 36.5],
                    },
                ],
            },
            {
                "id": 2,
                "name": "erdgeschoss",
                "height": 255,
                "walls": [
                    {"id": 1, "pos": {"hori": [25, 0]}, "ende": [36.5, 324]},
                    {
                        "id": 2,
                        "pos": {"hori": ["61.5-36.5", 0]},
                        "ende": ["587.5+36.5", 36.5],
                    },
                ],
            },
            {
                "id": 3,
                "name": "obergeschoss",
                "height": 255,
                "walls": [
                    {"id": 1, "pos": {"hori": [25, 0]}, "ende": [24, "292.5+31.5"]},
                    {"id": 2, "pos": {"hori": [0, 292.5]}, "ende": [24, 883]},
                ],
            },
        ]
    }

    print(yaml_data)
    read_struktur(haus, yaml_data)
    assert len(haus.geschosse) == 3
    assert len(haus.geschosse[0].walls) == 2
    assert len(haus.geschosse[1].walls) == 2
    assert haus.geschosse[0].z0 == 0.0
    assert haus.geschosse[0].z1 == 236
    assert haus.geschosse[1].z0 == 236
    assert haus.geschosse[1].z1 == 236 + 255
    assert haus.geschosse[2].z0 == 236 + 255
    assert haus.geschosse[2].z1 == 236 + 255 + 255
    assert len(haus.geschosse[2].walls) == 2
