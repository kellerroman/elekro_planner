#!/usr/bin/env python3
from elektro_planner.data import Steckdose, Licht, Stromanschluss, Knx, Kontakt, Netzwerk, Haus, Geschoss, Room, Led, LedStrip
def read_anschluesse(haus,data):

    id = [0,0,0]
    object_count = 0
    room_count   = 0
    geschoss_count = 0
    z = 0.0
    for geschoss in data["geschosse"]:
        id[0] = id[0] + 1
        id[1] = 0
        gid = geschoss["id"]
        gname = geschoss["name"]
        if id[0] != gid:
            raise RuntimeError("Geschoss-Id not correct {} ist: {}".format(id[0],gid))
        found = False
        for ges in haus.geschosse:
            if ges.id == gid and ges.name == gname:
                current_geschoss = ges
                found = True
                break
        if not found:
            # haus.geschosse.append(Geschoss(geschoss))
            # current_geschoss = haus.geschosse[-1]
            raise RuntimeError ("Geschoss not in list: {}".format(gid, gname))
        geschoss_count += 1
        if "rooms" in geschoss:
            for room in geschoss["rooms"]:
                id[2] = 0
                id[1] = id[1] + 1
                if id[1] != room["id"]:
                    raise RuntimeError ("Room-Id not correct {} is: {}".format(id[1], room["id"]))
                current_geschoss.rooms.append(Room(room,current_geschoss))
                room_count += 1
                if "objects" in room:
                    current_room = current_geschoss.rooms[-1]
                    for obj in room["objects"]:
                        id[2] = id[2] + 1
                        if id[2] != obj["id"]:
                            raise RuntimeError ("Room-Id not correct {} is: {}".format(id[2], obj["id"]))
                        object_count += 1
                        st = "con-type"
                        if  st in obj:
                            if obj[st] == "knx":
                                current_room.objects.append(Knx(obj,current_room))
                            elif obj[st] == "steckdose":
                                current_room.objects.append(Steckdose(obj,current_room))
                            elif obj[st] == "anschluss":
                                current_room.objects.append(Stromanschluss(obj,current_room))
                            elif obj[st] == "licht":
                                current_room.objects.append(Licht(obj,current_room))
                            elif obj[st] == "led":
                                current_room.objects.append(Led(obj,current_room))
                            elif obj[st] == "ledstrip":
                                current_room.objects.append(LedStrip(obj,current_room))
                            elif obj[st] == "kontakt":
                                current_room.objects.append(Kontakt(obj,current_room))
                            elif obj[st] == "netzwerk":
                                current_room.objects.append(Netzwerk(obj,current_room))
                            else:
                                raise RuntimeError("Connection Type unknown {}".format(obj[st]))
                        else:
                            raise RuntimeError("Connection Type not set")
                        current_room.objects[-1].z += z
        z += current_geschoss.height

if __name__ == '__main__':
    import yaml
    haus = Haus()
    yaml_file = "data/anschluesse.yaml"
    with open(yaml_file, 'r') as stream:
        data= yaml.safe_load(stream)
    read_anschluesse(haus,data)
