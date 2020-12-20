#!/usr/bin/env python3

from data import  Haus, Geschoss, Wall
import yaml
def read_walls(haus,yaml_file):
    with open(yaml_file, 'r') as stream:
        data = yaml.safe_load(stream)

    id = [0,0,0]
    wall_count = 0
    geschoss_count = 0
    for geschoss in data["geschosse"]:
        id[0] = id[0] + 1
        id[1] = 0
        gid = geschoss["id"]
        if id[0] != gid:
            print ("Geschoss-Id not correct {} ist: {}".format(id[0], gid))
            quit(1)
        print(geschoss["name"]+"("+str(gid)+")")
        haus.geschosse.append(Geschoss(geschoss))
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
    print(" Geschosse: {} ".format(geschoss_count))
    print(" Wände: {} ".format(wall_count))

if __name__ == '__main__':
    haus = Haus()
    yaml_file = "data/eg.yaml"
    read_walls(haus,yaml_file)
