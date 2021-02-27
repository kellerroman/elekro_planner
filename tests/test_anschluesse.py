#!/usr/bin/env python3

# from context import *
from elektro_planner.read_anschluesse import read_anschluesse
from elektro_planner.read_struktur import read_struktur
from elektro_planner.data import Haus
import yaml
def test_read_struktur():
    haus = Haus()
    yaml_data= {'geschosse': [\
     {'id': 1, 'name': 'G1', 'rooms': [\
      {'id': 1, 'name': 'R11', 'objects': [\
       {'id': 1, 'name': 'O111', 'con-type': 'steckdose', 'anzahl': 1, 'pos': {'hori': [10, 0], 'vert': 'oben'}}\
      ,{'id': 2, 'name': 'O112', 'con-type': 'steckdose', 'anzahl': 2, 'pos': {'hori': [20, 5], 'vert': 'oben'}}\
      ,{'id': 3, 'name': 'O113', 'con-type': 'steckdose', 'anzahl': 3, 'pos': {'hori': [30, 8], 'vert': 'oben'}}\
     ]}\
    ]}\
    ,{'id': 2, 'name': 'G2', 'rooms': [\
      {'id': 1, 'name': 'R21', 'objects': [\
       {'id': 1, 'name': 'O211', 'con-type': 'steckdose', 'anzahl': 1, 'pos': {'hori': [10, 0], 'vert': 'oben'}}\
      ,{'id': 2, 'name': 'O212', 'con-type': 'steckdose', 'anzahl': 2, 'pos': {'hori': [20, 5], 'vert': 'oben'}}\
     ]}\
    ]}\
    ]}
    yaml_data_struktur = {'geschosse': [\
            {'id': 1, 'name': 'G1', 'height': 236, 'walls': [\
              {'id': 1, 'pos': {'hori': [25, 0]}, 'ende': [36.5, 1049]}\
            , {'id': 2, 'pos': {'hori': [25, 0]}, 'ende': ['36.5+576+11.5', 36.5]}
            ]} \
          , {'id': 2, 'name': 'G2', 'height': 255, 'walls': [\
              {'id': 1, 'pos': {'hori': [25, 0]}, 'ende': [36.5, 324]}\
            , {'id': 2, 'pos': {'hori': ['61.5-36.5', 0]}, 'ende': ['587.5+36.5', 36.5]}\
            ]} \
          , {'id': 3, 'name': 'G3', 'height': 255, 'walls': [\
              {'id': 1, 'pos': {'hori': [25, 0]}, 'ende': [24, '292.5+31.5']}\
            , {'id': 2, 'pos': {'hori': [0, 292.5]}, 'ende': [24, 883]}\
            ]}\
        ]}

    print(yaml_data)
    read_struktur(haus,yaml_data_struktur)
    read_anschluesse(haus,yaml_data)
    assert len(haus.geschosse[0].rooms) == 1
    assert len(haus.geschosse[0].rooms[0].objects) == 3
    assert len(haus.geschosse[1].rooms) == 1
    assert len(haus.geschosse[1].rooms[0].objects) == 2
