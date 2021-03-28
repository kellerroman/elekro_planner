#!/usr/bin/env python3

from elektro_planner.data import Kabel, Knx
import astar


def calc_wires(haus):
    for k in haus.kabel:
        get_kabel_objects(haus, k)
        set_kabel_type(k)
        calc_kabel_len(k)


def get_kabel_objects(haus, kabel):
    kabel.objects_associated = True
    kabel.start_obj = haus.find_object(kabel.start)
    for edge in kabel.end:
        obj = haus.find_object(edge)
        kabel.end_objs.append(obj)
        obj.setKabel(kabel)


def set_kabel_type(kabel):
    assert kabel.objects_associated
    kabel.type = kabel.end_objs[0].connection_type
    for obj in kabel.end_objs[1:]:
        if kabel.type != obj.connection_type:
            raise RuntimeError("Verschiedene Kabel Typen verbunden")


def calc_kabel_len(kabel):
    assert kabel.objects_associated
    if not isinstance(kabel, Kabel):
        raise RuntimeError("Kabel is not of Type Kabel")

    def neighbors(n):
        for n1 in n.get_connected_nodes():
            yield n1

    def distance(n1, n2):
        return n1.distance(n2)

    def cost(n, goal):
        return abs(n.x - goal.x)

    print(kabel)
    print(kabel.start_obj)
    print(kabel.end_objs[0])
    kabel.length = 10000000.0
    connected_objects = []
    path = None
    te = False
    for obj in kabel.end_objs:
        e1 = kabel.start_obj.associated_node
        e2 = obj.associated_node
        # TODO: all objects must be connected
        if e2 == None:
            kabel.length = 0.0
            # if te:
            #     raise RuntimeError("KNX Object: {} {}".format(obj, kabel))
            return
        print(e1.info())
        print(e2.info())

        temp_path = list(
            astar.find_path(
                e1,
                e2,
                neighbors_fnct=neighbors,
                heuristic_cost_estimate_fnct=cost,
                distance_between_fnct=distance,
            )
        )
        le = calc_path_length(temp_path) * 0.01
        if le < kabel.length:
            kabel.length = le
            connected_objects = [obj]
            path = temp_path
            if type(connected_objects[0]) == Knx:
                te = True
                # raise RuntimeError("KNX Object: {} {}".format(obj, kabel))
    print(" Length after First: {}".format(kabel.length))
    unconnected_objects = list(set(kabel.end_objs) - set(connected_objects))
    for u in unconnected_objects:
        print("Unconnected Objects: {}".format(u))
    while len(unconnected_objects) > 0:
        min_dist = 1000000.0
        path2 = None
        obj_to_add = None
        for obj1 in connected_objects:
            for obj2 in unconnected_objects:
                e1 = obj1.associated_node
                e2 = obj2.associated_node
                temp_path = list(
                    astar.find_path(
                        e1,
                        e2,
                        neighbors_fnct=neighbors,
                        heuristic_cost_estimate_fnct=cost,
                        distance_between_fnct=distance,
                    )
                )
                le = calc_path_length(temp_path) * 0.01
                if le < min_dist:
                    min_dist = le
                    obj_to_add = obj2
                    path2 = temp_path
        connected_objects.append(obj_to_add)
        unconnected_objects.remove(obj_to_add)
        kabel.length += min_dist
        path += path2
        print(" Length next: {}".format(kabel.length))
        for e in path2:
            print(e)
        for u in unconnected_objects:
            print("Unconnected Objects: {}".format(u))
    for n in path:
        kabel.addNode(n)
        n.addKabel(kabel)
    for n in range(len(path) - 1):
        if path[n].is_connected(path[n + 1]):
            edge = path[n].get_edge_that_connects_to(path[n + 1])
            edge.addKabel(kabel)
    return path


def calc_path_length(path):
    length = 0.0
    for e in range(len(path) - 1):
        length += path[e].distance(path[e + 1])
    return length
