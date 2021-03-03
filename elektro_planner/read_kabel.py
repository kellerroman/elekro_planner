#!/usr/bin/env python3

from elektro_planner.data import Haus, Kabel, KabelType, Knx
from elektro_planner.utils import find_object
import yaml


def read_kabel(haus, data):
    for kabel in data["kabel"]:
        haus.kabel.append(Kabel.from_yaml(kabel))


# generate cabel for not connected ojects and calculate
def autogenerate_kabel(haus, knx_as_bus=True, start_obj="1.1.1"):

    connected_objects = [start_obj]
    for kabel in haus.kabel:
        for edge in kabel.end:
            connected_objects.append(edge)

    for geschoss in haus.geschosse:
        knx_kabel = None
        for room in geschoss.rooms:
            for obj in room.objects:
                if obj.cid not in connected_objects:
                    if type(obj) == Knx and knx_as_bus:
                        if knx_kabel == None:
                            haus.kabel.append(Kabel(start_obj, obj.cid))
                            knx_kabel = haus.kabel[-1]
                        else:
                            knx_kabel.end.append(obj.cid)
                    else:
                        haus.kabel.append(Kabel(start_obj, obj.cid))


if __name__ == "__main__":
    haus = Haus()
    yaml_file = "data/kabel.yaml"
    with open(yaml_file, "r") as stream:
        data = yaml.safe_load(stream)
    read_kabel(haus, data)
    print(" Anzahl Kabel aus Datei:  {}".format(len(haus.kabel)))
