#!/usr/bin/env python3

from elektro_planner.data import  Haus, Geschoss, Wall, Window, Door
import yaml
def read_struktur(haus,data):
    id = [0,0,0]
    wall_count = 0
    window_count = 0
    door_count = 0
    geschoss_count = 0
    z = 0.0
    for geschoss in data["geschosse"]:
        id[0] = id[0] + 1
        id[1] = 0
        gid = geschoss["id"]
        if id[0] != gid:
            print ("Geschoss-Id not correct {} ist: {}".format(id[0], gid))
            quit(1)
        # print(geschoss["name"]+"("+str(gid)+")")
        haus.geschosse.append(Geschoss(geschoss,z,haus))
        geschoss_count += 1
        if "walls" in geschoss:
            for obj in geschoss["walls"]:
                id[2] = 0
                id[1] = id[1] + 1
                if id[1] != obj["id"]:
                    print ("Wall-Id not correct {} ist: {}".format(id[1],
                        obj["id"]))
                    quit(1)
                haus.geschosse[-1].walls.append(Wall(obj,haus.geschosse[-1]))
                wall_count += 1
        if "windows" in geschoss:
            for obj in geschoss["windows"]:
                haus.geschosse[-1].windows.append(Window(obj,haus.geschosse[-1]))
                window_count += 1
        if "doors" in geschoss:
            for obj in geschoss["doors"]:
                haus.geschosse[-1].doors.append(Door(obj,haus.geschosse[-1]))
                door_count += 1
        z += haus.geschosse[-1].height
if __name__ == '__main__':
    haus = Haus()
    yaml_file = "data/struktur.yaml"
    with open(yaml_file, 'r') as stream:
        data = yaml.safe_load(stream)
    read_struktur(haus,data)
