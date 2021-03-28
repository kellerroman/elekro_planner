#!/usr/bin/env python3
from elektro_planner.data import Node, NodeType
from elektro_planner.utils import add_node_to_wall
from math import sqrt
import numpy as np


def dist(e1, e2):
    dx = e1.x - e2.x
    dy = e1.y - e2.y
    return sqrt(dx * dx + dy * dy)


def create_nodes_from_walls(haus):
    for geschoss in haus.geschosse:
        # geschoss = haus.geschosse[0]
        z = geschoss.z0
        for wall in geschoss.walls:
            if wall.waagrecht:
                n1 = Node(
                    wall.x + 0.5 * wall.dy,
                    wall.y + 0.5 * wall.dy,
                    z,
                    wall,
                    NodeType.StartBottom,
                )
                n2 = Node(
                    wall.x + wall.dx - 0.5 * wall.dy,
                    wall.y + 0.5 * wall.dy,
                    z,
                    wall,
                    NodeType.EndBottom,
                )
            else:
                n1 = Node(
                    wall.x + 0.5 * wall.dx,
                    wall.y + 0.5 * wall.dx,
                    z,
                    wall,
                    NodeType.StartBottom,
                )
                n2 = Node(
                    wall.x + 0.5 * wall.dx,
                    wall.y + wall.dy - 0.5 * wall.dx,
                    z,
                    wall,
                    NodeType.EndBottom,
                )
            n1.connect(n2)
            for id1, e1 in enumerate([n1, n2]):
                for id2, e2 in enumerate(geschoss.nodes):
                    if dist(e1, e2) <= 3e1:
                        # print ("Dist between {}, {}: {}".format(id1,id2,dist(e1,e2)))
                        e1.connect(e2)
            wall.add_nodes([n1, n2], True)

        for wall in geschoss.walls:
            # print (" ==== WALL {} ===== ".format(wall.id))
            p1x = wall.nodes[0].x
            p1y = wall.nodes[0].y

            p2x = wall.nodes[1].x
            p2y = wall.nodes[1].y
            for ed in geschoss.nodes:
                if ed.parent.id == wall.id:
                    continue
                if (
                    wall.waagrecht
                    and abs(ed.y - p1y) < wall.dy
                    and ed.x > p1x
                    and ed.x < p2x
                    or not wall.waagrecht
                    and abs(ed.x - p1x) < wall.dx
                    and ed.y > p1y
                    and ed.y < p2y
                ):
                    # check for connection:
                    connected = False
                    for node in wall.nodes:
                        if ed in node.get_connected_nodes():
                            connected = True
                            break
                    if not connected:
                        # print("EDGE IS ON WALL: wall: {} edge: {}".format(wall.id, ed))
                        add_node_to_wall(wall, ed, False)
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
            # since we are looping over the egdes of a wall, we can not diretly add nodes to this lis
            # this is done after the loop
            for n in wall.nodes.copy():
                if n.id not in worked_on:
                    # prefent to add another upper edge for this
                    worked_on.append(n.id)
                    node_type = (
                        NodeType.StartTop
                        if n.type == NodeType.StartBottom
                        else NodeType.EndTop
                    )
                    n1 = Node(n.x, n.y, z, wall, node_type)
                    upper_id[n.id] = n1.id
                    wall.add_node(n1, True)
                    for e2 in n.get_connected_nodes():
                        # for now we can only connect nodes that have alower id because the others dont exist yet
                        if e2.id in upper_id:
                            e3 = haus.nodes[upper_id[e2.id]]
                            n1.connect(e3)
                    n.connect(n1)
                else:
                    # add this new edge to the wall as well.
                    # it should be the last connection of the original node, since only there brothers "upstears" are added
                    wall.add_node(n.get_connected_nodes()[-1], False)


def create_nodes_from_connectors(haus):
    delta = 10
    for con in haus.connectors:
        print("Checking Connector: {}".format(con))
        if con.dz == 0:
            x1 = con.x
            x2 = con.x + con.dx
            y1 = con.y
            y2 = con.y + con.dy
            found_correct_geschoss = False
            for g in haus.geschosse:
                if con.z >= g.z0 and con.z <= g.z1:
                    found_correct_geschoss = True
                    for wall in g.walls:
                        print("Checking With Wall: {} {}".format(con.id, wall.cid))
                        if wall.waagrecht:
                            x3 = wall.x
                            x4 = wall.x + wall.dx
                            y3 = wall.y + wall.dy * 0.5
                            y4 = y3
                            wdx = wall.dx
                            wdy = 0
                        else:
                            x3 = wall.x + wall.dx * 0.5
                            x4 = x3
                            y3 = wall.y
                            y4 = wall.y + wall.dy
                            wdx = 0
                            wdy = wall.dy
                        print(
                            "{} {} {} {}: {}".format(
                                wdx, con.dy, wdy, con.dx, wdx * con.dy - wdy * con.dx
                            )
                        )
                        if not wdx * con.dy - wdy * con.dx == 0:
                            print("Solving equation")
                            a = np.array([[x2 - x1, x3 - x4], [y2 - y1, y3 - y4]])
                            b = np.array([x3 - x1, y3 - y1])
                            x = np.linalg.solve(a, b)
                            print(x)
                            if x[0] >= 0 and x[0] <= 1 and x[1] >= 0 and x[1] <= 1:
                                nx = x3 + x[1] * wdx
                                ny = y3 + x[1] * wdy
                                print(" New Node at: ({},{})".format(nx, ny))
                                print(wall)
                                for n in wall.nodes:
                                    print(n)
                                new_node = Node(nx, ny, con.z, wall, NodeType.Connector)
                                add_node_to_wall(wall, new_node)
                                con.add_node(new_node, x[0])

                    break
            if not found_correct_geschoss:
                raise RuntimeError(
                    "Could not associate Waagrechten Schacht to Geschoss"
                )
        elif con.dx == 0 and con.dy == 0:
            for g in haus.geschosse:
                if con.z <= g.z1 and con.z + con.dz >= g.z0:
                    for wall in g.walls:
                        if (
                            con.x >= wall.x - delta
                            and con.x <= wall.x + wall.dx + delta
                            and con.y >= wall.y - delta
                            and con.y <= wall.y + wall.dy + delta
                        ):
                            heights = [g.z0, g.z1]
                            for h in heights:
                                if con.z <= h and con.z + con.dz >= h:
                                    new_node = Node(
                                        con.x, con.y, h, wall, NodeType.Connector
                                    )
                                    add_node_to_wall(wall, new_node)
                                    con.add_node(new_node, h)
                                    print(
                                        "Adding node: {} to {}".format(new_node, wall)
                                    )

        else:
            raise RuntimeError("Schräger Schacht noch nicht unterstützt")
        # connect edges of connector
        print("Connecting Edges of Connectorto each other{}".format(len(con.nodes)))
        if len(con.nodes) <= 1:
            raise RuntimeError("Not Enough Nodes associated to Connector: {}".format(con))
        for i, n in enumerate(sorted(con.nodes)):
            if i > 0:
                print("Connecting {} to {}".format(con.nodes[n], old))
                con.nodes[n].connect(old)
            old = con.nodes[n]


if __name__ == "__main__":
    import yaml
    from data import Haus
    from read_struktur import read_struktur

    yaml_file = "data/struktur.yaml"
    with open(yaml_file, "r") as stream:
        yaml_struktur = yaml.safe_load(stream)
    haus = Haus()
    read_struktur(haus, yaml_struktur)
    create_nodes_from_walls(haus)
