#!/usr/bin/env python3
from read_setup import *

def dict_delta(new,old):
    temp = dict()
    for x in new.keys():
        temp[x] = new[x] - old[x]
    return temp

def create_roombook(haus):
    haus.room_count   = 0
    haus.geschoss_count = 0

    mybook = dict()
    mybook["object"] = 0
    mybook["licht"] = 0
    mybook["schalten"] = 0
    mybook["knx_input"] = 0
    mybook["knx_presenzmelder"] = 0
    mybook["knx_glastaster"] = 0
    mybook["knx_reserve"] = 0
    mybook["stromanschluss"] = 0
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
            elif type(obj) is Knx:
                if obj.knx_anschluss is KnxAnschluss.Praesenzmelder:
                    mybook["knx_presenzmelder"] += 1
                if obj.knx_anschluss is KnxAnschluss.Glastaster:
                    mybook["knx_glastaster"] += 1
                else:
                    mybook["knx_reserve"] += 1
            elif type(obj) is Netzwerk:
               mybook["netzwerk"] += 1
            elif type(obj) is Kontakt:
               mybook["kontakt"] += 1
               mybook["knx_input"] += obj.anzahl
            else:
               mybook["stromanschluss"] += 1
        room.book = dict_delta(mybook,room.book)
      geschoss.book = dict_delta(mybook,geschoss.book)
    haus.book = mybook.copy()
if __name__ == '__main__':
    yaml_file = "data/setup.yaml"
    haus = read_setup(yaml_file)
    create_roombook(haus)

    for geschoss in haus.geschosse:
      print("{} | {} | {}".format(geschoss.id,geschoss.name, geschoss.book["object"]))
      for room in geschoss.rooms:
        print("-{} | {} | {}".format(room.id,room.name, room.book["object"]))
        for obj in room.objects:
          print("--{} | {} ".format(obj.id,obj.name))

    print(" Geschosse: {}".format(haus.geschoss_count))
    print(" Räume: {} ".format(haus.room_count))
    print(" Anschlüsse: {} ".format(haus.book["object"]))
    print(" Licht: {} ".format(haus.book["licht"]))
    print(" Schalten: {} ".format(haus.book["schalten"]))
    print(" KNX Input: {} ".format(haus.book["knx_input"]))
    print(" KNX Präsenzmelder: {} ".format(haus.book["knx_presenzmelder"]))
    print(" KNX Glastaster: {} ".format(haus.book["knx_glastaster"]))
    print(" KNX Reserve: {} ".format(haus.book["knx_reserve"]))
    print(" Stromanschluss: {} ".format(haus.book["stromanschluss"]))
    print(" Kontakte: {} ".format(haus.book["kontakt"]))
    print(" Netzwerk: {} ".format(haus.book["netzwerk"]))
