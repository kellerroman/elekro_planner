#!/usr/bin/env python3
from elektro_planner.utils import add_node_to_wall
from elektro_planner.data import Node, NodeType


def associate_objects_to_walls_and_nodes(haus):
    delta = 1
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
