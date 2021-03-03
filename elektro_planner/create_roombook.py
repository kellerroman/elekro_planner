#!/usr/bin/env python3
from elektro_planner.utils import find_object
from elektro_planner.data import *


def dict_delta(new, old):
    temp = dict()
    for x in new.keys():
        temp[x] = new[x] - old[x]
    return temp


def create_roombook(haus):
    haus.room_count = 0
    haus.geschoss_count = 0

    mybook = dict()
    mybook["object"] = 0
    mybook["licht"] = 0
    mybook["led"] = 0
    mybook["schalten"] = 0
    mybook["knx_input"] = 0
    mybook["knx_presenzmelder"] = 0
    mybook["knx_glastaster"] = 0
    mybook["knx_reserve"] = 0
    mybook["stromanschluss"] = 0
    mybook["steckdose"] = 0
    mybook["steckdose 1-fach"] = 0
    mybook["steckdose 2-fach"] = 0
    mybook["steckdose 3-fach"] = 0
    mybook["unterputzdosen"] = 0
    mybook["rolladen"] = 0
    mybook["kontakt"] = 0
    mybook["netzwerk"] = 0

    for geschoss in haus.geschosse:
        geschoss.book = mybook.copy()
        haus.geschoss_count += 1
        for room in geschoss.rooms:
            room.book = mybook.copy()
            haus.room_count += 1
            for obj in room.objects:
                mybook["object"] += 1
                if type(obj) is Licht:
                    mybook["licht"] += 1
                elif type(obj) is Led:
                    mybook["led"] += 1
                elif type(obj) is Knx:
                    mybook["unterputzdosen"] += 1
                    if obj.knx_anschluss is KnxAnschluss.Praesenzmelder:
                        mybook["knx_presenzmelder"] += 1
                    if obj.knx_anschluss is KnxAnschluss.Glastaster:
                        mybook["knx_glastaster"] += 1
                    else:
                        mybook["knx_reserve"] += 1
                elif type(obj) is Netzwerk:
                    mybook["netzwerk"] += 1
                    mybook["unterputzdosen"] += 1
                elif type(obj) is Kontakt:
                    mybook["kontakt"] += 1
                    mybook["knx_input"] += obj.anzahl
                elif type(obj) is Steckdose:
                    mybook["unterputzdosen"] += obj.anzahl
                    # mybook["stromanschluss"] += 1
                    mybook["steckdose"] += obj.anzahl
                    if obj.anzahl == 1:
                        mybook["steckdose 1-fach"] += 1
                    elif obj.anzahl == 2:
                        mybook["steckdose 2-fach"] += 1
                    elif obj.anzahl == 3:
                        mybook["steckdose 3-fach"] += 1
                else:
                    mybook["stromanschluss"] += 1
                    mybook["unterputzdosen"] += 1
                    if obj.knx == KnxType.Rolladen:
                        mybook["rolladen"] += 1
            room.book = dict_delta(mybook, room.book)
        geschoss.book = dict_delta(mybook, geschoss.book)

    # Kabel part of the roombook
    kabel_len = [0.0, 0.0, 0.0, 0.0, 0.0]
    kabel_anz = [0, 0, 0, 0, 0]
    for kabel in haus.kabel:
        calc_length(kabel, haus)
        kabel_len[kabel.type.value] += kabel.length
        kabel_anz[kabel.type.value] += 1

    for kb in KabelType:
        mybook["laenge_kabel_" + kb.name] = kabel_len[kb.value]
        mybook["anzahl_kabel_" + kb.name] = kabel_anz[kb.value]
    haus.book = mybook.copy()


def calc_length(kabel, haus):
    kabel.length = 10000000.0
    start = find_object(haus, kabel.start)
    # connection to the "clostest" object
    connected_objects = []
    for edge in kabel.end:
        obj = find_object(haus, edge)
        dx = start.x - obj.x
        dy = start.y - obj.y
        dz = start.z - obj.z
        le = (abs(dx) + abs(dy) + abs(dz)) * 0.01
        if le < kabel.length:
            kabel.length = le
            connected_objects = [edge]
        if edge == kabel.end[0]:
            kabel.type = obj.connection_type
        else:
            if kabel.type != obj.connection_type:
                raise RuntimeError("Verschiedene Kabel Typen verbunden")
    # connection to the other objects
    unconnected_objects = list(set(kabel.end) - set(connected_objects))
    while len(unconnected_objects) > 0:
        min_dist = 1000000.0
        obj_to_add = None
        for o1 in connected_objects:
            for o2 in unconnected_objects:
                obj1 = find_object(haus, o1)
                obj2 = find_object(haus, o2)
                dx = obj1.x - obj2.x
                dy = obj1.y - obj2.y
                dz = obj1.z - obj2.z
                le = (abs(dx) + abs(dy) + abs(dz)) * 0.01
                if le < min_dist:
                    min_dist = le
                    obj_to_add = o2
        connected_objects.append(obj_to_add)
        unconnected_objects.remove(obj_to_add)
        kabel.length += min_dist


if __name__ == "__main__":
    from elektro_planner import *

    yaml_file = "data/setup.yaml"
    haus = read_setup(yaml_file)
    create_roombook(haus)

    for geschoss in haus.geschosse:
        print(
            "{} | {} | {}".format(geschoss.id, geschoss.name, geschoss.book["object"])
        )
        for room in geschoss.rooms:
            print("-{} | {} | {}".format(room.id, room.name, room.book["object"]))
            for obj in room.objects:
                print("--{} | {} ".format(obj.id, obj.name))

    print(" Geschosse: {}".format(haus.geschoss_count))
    print(" Räume: {} ".format(haus.room_count))
    print(" Anschlüsse: {} ".format(haus.book["object"]))

    print()
    print(" ---- Roombook ----")
    for name, value in haus.book.items():
        print(" {}: {}".format(name, value))
