#!/usr/bin/env python3

from elektro_planner.data import  Haus, Kabel, KabelType, Knx
import yaml
def read_kabel(haus,data,knx_as_bus = True):
    connected_edges = ["1.1.1"]
    for kabel in data["kabel"]:
        haus.kabel.append(Kabel(kabel))
        for edge in haus.kabel[-1].end:
            connected_edges.append(edge)

    # generate cabel for not connected ojects and calculate
    for geschoss in haus.geschosse:
        knx_kabel = None
        for room in geschoss.rooms:
            for obj in room.objects:
                if obj.cid not in connected_edges:
                    if type(obj) == Knx and knx_as_bus:
                        if knx_kabel == None:
                            haus.kabel.append(Kabel({'start': '1.1.1', 'end': [obj.cid]}))
                            knx_kabel = haus.kabel[-1]
                        else:
                            knx_kabel.end.append(obj.cid)
                    else:
                        haus.kabel.append(Kabel({'start': '1.1.1', 'end': [obj.cid]}))

if __name__ == '__main__':
    haus = Haus()
    yaml_file = "data/kabel.yaml"
    with open(yaml_file, 'r') as stream:
        data = yaml.safe_load(stream)
    read_kabel(haus,data)
    print(" Anzahl Kabel aus Datei:  {}".format(len(haus.kabel)))

