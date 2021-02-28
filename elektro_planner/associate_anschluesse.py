#!/usr/bin/env python3
from elektro_planner.utils import add_node_to_wall
from elektro_planner.data import Node
def associate_anschluesse(haus):
    print(" ==== Associate Anschluesse ==== ")
    delta = 5
    for geschoss in haus.geschosse:
        objects = []
        for room in geschoss.rooms:
            for obj in room.objects:
                objects.append(obj)
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
                    obj.associated_wall = wall

                    # TODO: check if a close by edge exists
                    e1 = Node(obj.x,obj.y,obj.z,wall)
                    wall.add_node(e1,True)
                    e2 = Node(obj.x,obj.y,geschoss.z0,wall)
                    add_node_to_wall(wall,e2)
                    e3 = Node(obj.x,obj.y,geschoss.z1,wall)
                    add_node_to_wall(wall,e3)
                    e1.connect(e2)
                    e1.connect(e3)
                    obj.associated_node = e1
        assert len(objects) == 0
