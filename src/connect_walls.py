#!/usr/bin/env python3

import svgwrite
from read_setup import *
from math import sqrt
def dist(e1,e2):
    dx = e1.x - e2.x
    dy = e1.y - e2.y
    return sqrt(dx*dx+dy*dy)
def connect_walls(haus):
    for geschoss in haus.geschosse:
        # geschoss = haus.geschosse[1]
        for wall in geschoss.walls:
            wall_waagrecht = False
            if wall.dx>wall.dy:
                wall_waagrecht = True
                p1 = edge(wall.x+0.5*wall.dy,wall.y+0.5*wall.dy,wall)
                p2 = edge(wall.x+wall.dx-0.5*wall.dy,wall.y+0.5*wall.dy,wall)
            else:
                p1 = edge(wall.x+0.5*wall.dx,wall.y+0.5*wall.dx,wall)
                p2 = edge(wall.x+0.5*wall.dx,wall.y+wall.dy-0.5*wall.dx,wall)
            p1.connections.append(p2)
            p2.connections.append(p1)
            wall.edges.append(p1)
            wall.edges.append(p2)
            for id1, e1 in enumerate([p1,p2]):
                for id2, e2 in enumerate(geschoss.edges):
                    if dist(e1,e2) <= 3e1:
                        # print ("Dist between {}, {}: {}".format(id1,id2,dist(e1,e2)))
                        e1.n += 1
                        e2.n += 1
                        e1.connections.append(e2)
                        e2.connections.append(e1)
            geschoss.edges.append(p1)
            geschoss.edges.append(p2)

        for wall in geschoss.walls:
            # print (" ==== WALL {} ===== ".format(wall.id))
            wall_waagrecht = False
            if wall.dx>wall.dy:
                wall_waagrecht = True
            p1x = wall.edges[0].x
            p1y = wall.edges[0].y

            p2x = wall.edges[1].x
            p2y = wall.edges[1].y
            for ed in geschoss.edges:
                if ed.parent.id == wall.id:
                    continue
                if     wall_waagrecht and abs(ed.y-p1y) < wall.dy and ed.x >p1x and ed.x < p2x or \
                   not wall_waagrecht and abs(ed.x-p1x) < wall.dx and ed.y >p1y and ed.y < p2y:
                    # check for connection:
                    connected = False
                    for e in wall.edges:
                        if ed in e.connections:
                            connected = True
                            break
                    if not connected:
                        print("EDGE IS ON WALL: wall: {} ed_wall: {}".format(wall.id, ed.parent.id))
                        if wall_waagrecht:
                            ed.y = p1y
                        else:
                            ed.x = p1x
                        wall.edges.append(ed)
                        ed.n += 2
                        ed.connections.append(wall.edges[0])
                        ed.connections.append(wall.edges[1])

if __name__ == '__main__':
    yaml_file = "data/setup.yaml"
    read_setup(yaml_file)
