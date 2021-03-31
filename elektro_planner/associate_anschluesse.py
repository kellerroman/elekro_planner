#!/usr/bin/env python3
from elektro_planner.utils import add_node_to_wall
from elektro_planner.data import Node, NodeType, VerticalPosition
import numpy as np


def associate_objects_to_walls_and_nodes(haus):
    delta = 1
    error = False
    for geschoss in haus.geschosse:
        objects = []
        # dist of list with the objects at same position with the first objects id beening the key
        object_with_same_position = dict()
        for room in geschoss.rooms:
            for obj in room.objects:
                is_unique = True
                # check all objects in list if they are at the same position
                for o2 in objects:
                    # same coord in y and x (z can be different) and on same floor
                    if (
                        o2.x == obj.x
                        and o2.y == obj.y
                        and o2.parent.parent == obj.parent.parent
                    ):
                        # add object to the list of the other object
                        object_with_same_position[o2.cid].append(obj)
                        is_unique = False
                        break
                if is_unique:
                    objects.append(obj)
                    # create list entry in dict with itself in it
                    object_with_same_position[obj.cid] = [obj]

        for wall in geschoss.walls:
            xs = wall.x - delta
            ys = wall.y - delta
            xe = xs + wall.dx + delta * 2
            ye = ys + wall.dy + delta * 2
            assert xs < xe
            assert ys < ye
            for obj in objects.copy():
                if obj.x >= xs and obj.x <= xe and obj.y >= ys and obj.y <= ye:
                    assert obj.z <= geschoss.z1
                    assert obj.z >= geschoss.z0
                    objects.remove(obj)

                    # TODO: check if a close-by edge exists
                    e2 = Node(obj.x, obj.y, geschoss.z0, obj, NodeType.ObjectBottom)
                    add_node_to_wall(wall, e2)

                    e3 = Node(obj.x, obj.y, geschoss.z1, obj, NodeType.ObjectTop)
                    add_node_to_wall(wall, e3)
                    # only add "Object node" if it is not naturally on one of the others
                    object_is_on_top = abs(obj.z - geschoss.z1) <= delta
                    object_is_on_bottom = abs(obj.z - geschoss.z0) <= delta
                    if object_is_on_top:
                        e1 = e3
                        e3.connect(e2)
                    elif object_is_on_bottom:
                        e1 = e2
                        e2.connect(e3)
                    else:
                        e1 = Node(obj.x, obj.y, obj.z, obj, NodeType.Object)
                        wall.add_node(e1, True)
                        e1.connect(e2)
                        e1.connect(e3)
                    for o in object_with_same_position[obj.cid]:
                        o.associated_node = e1
                        o.associated_wall = wall

        # assert len(objects) == 0
        if len(objects) > 0:
            edges = getEdgesofGeschoss(geschoss)
        for o in objects:
            if not associate_special_object(o, geschoss, edges):
                error = True
                print(
                    "Object can not be associated even if it is not on the decke: {}".format(
                        o
                    )
                )
    if error:
        raise RuntimeError(
            "Object can not be associated even if it is not on the decke: "
        )


def associate_special_object(obj, geschoss, edges):
    print("==========================================================")
    print("==========================================================")
    print("============ ASSOCIATE SPECIAL OBJECT ====================")
    print("==========================================================")
    print(obj)
    print("==========================================================")
    if obj.pos.vertical not in [VerticalPosition.Decke, VerticalPosition.Boden]:
        return False

    n = Node(obj.x, obj.y, obj.z, obj, NodeType.Object)
    geschoss.add_node(n)
    # obj.associated_node = n
    L = 10 * 100
    dirs = [[L, 0], [-L, 0], [0, L], [0, -L]]
    xn1 = obj.x
    yn1 = obj.y
    for d in dirs:
        xn2 = xn1 + d[0]
        yn2 = yn1 + d[1]
        dxn = d[0]
        dyn = d[1]
        print("Number of Edges in Geschoss: {}".format(len(edges)))
        x_array = []
        e_array = []
        for e in edges:
            # print(e)
            if abs(e.node[0].z - obj.z) < 100:
                xe1 = e.node[0].x
                ye1 = e.node[0].y
                dxe = e.node[1].x - e.node[0].x
                dye = e.node[1].y - e.node[0].y
                xe2 = e.node[1].x
                ye2 = e.node[1].y
                if not dxe * dyn - dye * dxn == 0:
                    a = np.array([[xn2 - xn1, xe1 - xe2], [yn2 - yn1, ye1 - ye2]])
                    b = np.array([xe1 - xn1, ye1 - yn1])
                    x = np.linalg.solve(a, b)
                    if x[0] >= 0 and x[0] <= 1 and x[1] >= 0 and x[1] <= 1:
                        x_array.append(x[0])
                        e_array.append(e)
                        # nx = xn1 + x[0] * dxn
                        # ny = yn1 + x[0] * dyn
                        # print( "Found connection for {} {}: {} {}".format(xn1, yn1, nx, ny))
                        # wall = e.getWall()
                        # n2 = Node(nx, ny, obj.z, wall, NodeType.SeelingConnect)
                        # n2.connect(n)
                        # geschoss.add_node(n2)
                        # # add_node_to_wall(wall, n2)

        n1 = n
        sorted_list = sorted(zip(x_array, e_array), key=lambda node: node[0])
        for x, e in sorted_list:
            nx = xn1 + x * dxn
            ny = yn1 + x * dyn
            print("Found connection for {} {}: {} {}".format(xn1, yn1, nx, ny))
            wall = e.getWall()
            n2 = Node(nx, ny, obj.z, wall, NodeType.SeelingConnect)
            n2.connect(n1)
            # geschoss.add_node(n2)
            add_node_to_wall(wall, n2)
            n1 = n2
    return True


def getEdgesofGeschoss(geschoss):
    print("==========================================================")
    print("==========================================================")
    print("============ Get Edges of Geschoss    ====================")
    print("==========================================================")
    print("==========================================================")
    edges = []
    for n in geschoss.nodes:
        for e in n.edges:
            if e not in edges:
                if e.node[0].z == e.node[1].z:
                    edges.append(e)
    print("Number of Edges in Geschoss: {}".format(len(edges)))
    return edges
