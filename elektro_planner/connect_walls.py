#!/usr/bin/env python3
from elektro_planner.data import Node
from elektro_planner.utils import add_node_to_wall
from math import sqrt
def dist(e1,e2):
    dx = e1.x - e2.x
    dy = e1.y - e2.y
    return sqrt(dx*dx+dy*dy)

def create_nodes_from_walls(haus):
    for geschoss in haus.geschosse:
        # geschoss = haus.geschosse[0]
        z = geschoss.z0
        for wall in geschoss.walls:
            if wall.waagrecht:
                n1 = Node(wall.x+0.5*wall.dy,wall.y+0.5*wall.dy,z,wall)
                n2 = Node(wall.x+wall.dx-0.5*wall.dy,wall.y+0.5*wall.dy,z,wall)
            else:
                n1 = Node(wall.x+0.5*wall.dx,wall.y+0.5*wall.dx,z,wall)
                n2 = Node(wall.x+0.5*wall.dx,wall.y+wall.dy-0.5*wall.dx,z,wall)
            n1.connect(n2)
            for id1, e1 in enumerate([n1,n2]):
                for id2, e2 in enumerate(geschoss.nodes):
                    if dist(e1,e2) <= 3e1:
                        # print ("Dist between {}, {}: {}".format(id1,id2,dist(e1,e2)))
                        e1.connect(e2)
            wall.add_nodes([n1,n2],True)

        for wall in geschoss.walls:
            # print (" ==== WALL {} ===== ".format(wall.id))
            p1x = wall.nodes[0].x
            p1y = wall.nodes[0].y

            p2x = wall.nodes[1].x
            p2y = wall.nodes[1].y
            for ed in geschoss.nodes:
                if ed.parent.id == wall.id:
                    continue
                if     wall.waagrecht and abs(ed.y-p1y) < wall.dy and ed.x >p1x and ed.x < p2x or \
                   not wall.waagrecht and abs(ed.x-p1x) < wall.dx and ed.y >p1y and ed.y < p2y:
                    # check for connection:
                    connected = False
                    for node in wall.nodes:
                        if ed in node.get_connected_nodes():
                            connected = True
                            break
                    if not connected:
                        # print("EDGE IS ON WALL: wall: {} edge: {}".format(wall.id, ed))
                        add_node_to_wall(wall,ed,False)
        # add the upper nodes
        # since an edge can be part of multiple walls, we have to check if the egde
        # has been worked on already, then we will only add the already existing edge to the wall
        worked_on = []
        upper_id = dict()
        z = geschoss.z1
        for wall in geschoss.walls:
            # n is the original edge
            # n1 is its copy (upper edge)
            # e2 is a connected edge of e
            # e3 is the the copy of e2 thus the egde that n1 should be connected as well
            #since we are looping over the egdes of a wall, we can not diretly add nodes to this lis
            # this is done after the loop
            for n in wall.nodes.copy():
                if n.id not in worked_on:
                    # prefent to add another upper edge for this
                    worked_on.append(n.id)
                    n1 = Node(n.x,n.y,z,wall)
                    upper_id[n.id] = n1.id
                    wall.add_node(n1,True)
                    for e2 in n.get_connected_nodes():
                        # for now we can only connect nodes that have alower id because the others dont exist yet
                        if e2.id in upper_id:
                            e3 = haus.nodes[upper_id[e2.id]]
                            n1.connect(e3)
                    n.connect(n1)
                else:
                    # add this new edge to the wall as well.
                    # it should be the last connection of the original node, since only there brothers "upstears" are added
                    wall.add_node(n.get_connected_nodes()[-1],False)

if __name__ == '__main__':
    import yaml
    from data import Haus
    from read_struktur import read_struktur

    yaml_file = "data/struktur.yaml"
    with open(yaml_file, 'r') as stream:
        yaml_struktur = yaml.safe_load(stream)
    haus = Haus()
    read_struktur(haus,yaml_struktur)
    create_nodes_from_walls(haus)

