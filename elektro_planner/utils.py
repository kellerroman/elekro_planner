#!/usr/bin/env python3

def find_object(haus,cid):
    return haus.find_object(cid)

def add_node_to_wall(wall,ed,recursive_add = True):
    ed_temp = [ed]
    for e in wall.nodes:
        if abs(e.z-ed.z) <= 5:
            ed_temp.append(e)
    if wall.waagrecht:
        nodes_sorted = sorted(ed_temp, key=lambda node: node.x)
        ed.y = wall.nodes[0].y
    else:
        nodes_sorted = sorted(ed_temp, key=lambda node: node.y)
        ed.x = wall.nodes[0].x

    n_nodes = len(ed_temp)
    pos_new = nodes_sorted.index(ed)
    if not pos_new < n_nodes-1:
        raise RuntimeError("Node is not in the middle of the wall: len: {} Pos: {}".format(n_nodes_new))


    prev_edge = nodes_sorted[pos_new-1]
    next_edge = nodes_sorted[pos_new+1]
    prev_edge.replace_connection(next_edge,ed)
    next_edge.connect(ed)
    wall.add_node(ed,recursive_add)


