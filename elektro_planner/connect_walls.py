#!/usr/bin/env python3
from elektro_planner.data import Edge
from elektro_planner.utils import add_edge_to_wall
from math import sqrt
def dist(e1,e2):
    dx = e1.x - e2.x
    dy = e1.y - e2.y
    return sqrt(dx*dx+dy*dy)

def connect_walls(haus):
    for geschoss in haus.geschosse:
        # geschoss = haus.geschosse[0]
        z = geschoss.z0
        for wall in geschoss.walls:

            if wall.waagrecht:
                p1 = Edge(wall.x+0.5*wall.dy,wall.y+0.5*wall.dy,z,wall)
                p2 = Edge(wall.x+wall.dx-0.5*wall.dy,wall.y+0.5*wall.dy,z,wall)
            else:
                p1 = Edge(wall.x+0.5*wall.dx,wall.y+0.5*wall.dx,z,wall)
                p2 = Edge(wall.x+0.5*wall.dx,wall.y+wall.dy-0.5*wall.dx,z,wall)
            p1.connections.append(p2)
            p2.connections.append(p1)
            wall.edges.append(p1)
            wall.edges.append(p2)
            haus.edges[p1.id] = p1
            haus.edges[p2.id] = p2
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
            p1x = wall.edges[0].x
            p1y = wall.edges[0].y

            p2x = wall.edges[1].x
            p2y = wall.edges[1].y
            for ed in geschoss.edges:
                if ed.parent.id == wall.id:
                    continue
                if     wall.waagrecht and abs(ed.y-p1y) < wall.dy and ed.x >p1x and ed.x < p2x or \
                   not wall.waagrecht and abs(ed.x-p1x) < wall.dx and ed.y >p1y and ed.y < p2y:
                    # check for connection:
                    connected = False
                    for e in wall.edges:
                        if ed in e.connections:
                            connected = True
                            break
                    if not connected:
                        # print("EDGE IS ON WALL: wall: {} ed_wall: {}".format(wall.id, ed.parent.id))
                        add_edge_to_wall(wall,ed)
        # add the upper edges
        # since an edge can be part of multiple walls, we have to check if the egde
        # has been worked on already, then we will only add the already existing edge to the wall
        worked_on = []
        upper_id = dict()
        z = geschoss.z1
        for wall in geschoss.walls:
            # e is the original edge
            # e1 is its copy (upper edge)
            # e2 is a connected edge of e
            # e3 is the the copy of e2 thus the egde that e1 should be connected as well
            #since we are looping over the egdes of a wall, we can not diretly add edges to this lis
            # this is done after the loop
            for e in wall.edges.copy():
                if e.id not in worked_on:
                    # prefent to add another upper edge for this
                    worked_on.append(e.id)
                    e1 = Edge(e.x,e.y,z,wall)
                    upper_id[e.id] = e1.id
                    haus.edges[e1.id] = e1
                    geschoss.edges.append(e1)
                    wall.edges.append(e1)
                    e1.connections.append(e)
                    for e2 in e.connections:
                        # for now we can only connect edges that have alower id because the others dont exist yet
                        if e2.id in upper_id:
                            e3 = haus.edges[upper_id[e2.id]]
                            e1.connections.append(e3)
                            e3.connections.append(e1)
                    e.connections.append(e1)
                else:
                    # add this new edge to the wall as well.
                    # it should be the last connection of the original node, since only there brothers "upstears" are added
                    wall.edges.append(e.connections[-1])

if __name__ == '__main__':
    import yaml
    from data import Haus
    from read_struktur import read_struktur

    yaml_file = "data/struktur.yaml"
    with open(yaml_file, 'r') as stream:
        yaml_struktur = yaml.safe_load(stream)
    haus = Haus()
    read_struktur(haus,yaml_struktur)
    connect_walls(haus)

