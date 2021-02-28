#!/usr/bin/env python3

import astar

def calc_kabel_len(haus,kabel):

    def neighbors(n):
        for n1 in n.get_connected_nodes():
            yield n1

    def distance(n1, n2):
        return n1.distance(n2)

    def cost(n, goal):
        return abs(n.x - goal.x)

    e1 = haus.find_object(kabel.start).associated_node
    e2 = haus.find_object(kabel.end[0]).associated_node

    path = list(astar.find_path(e1, e2, neighbors_fnct=neighbors,
                heuristic_cost_estimate_fnct=cost, distance_between_fnct=distance))
    kabel.length = calc_path_length(path)
    return path

def calc_path_length(path):
    length = 0.0
    for e in range(len(path)-1):
        length += path[e].distance(path[e+1])
    return length

