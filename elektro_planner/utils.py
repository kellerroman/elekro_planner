#!/usr/bin/env python3


def find_object(haus, cid):
    return haus.find_object(cid)


def add_node_to_wall(wall, ed, recursive_add=True):
    # print(" ==== Add Node To Wall ==== ")
    ed_temp = [ed]
    # print(" Wall Nodes:")
    for e in wall.nodes:
        # print(e)
        if abs(e.z - ed.z) <= 5:
            ed_temp.append(e)
    if wall.waagrecht:
        nodes_sorted = sorted(ed_temp, key=lambda node: node.x * 10000 + node.id)
        ed.y = wall.nodes[0].y
    else:
        nodes_sorted = sorted(ed_temp, key=lambda node: node.y * 10000 + node.id)
        ed.x = wall.nodes[0].x

    # for e in wall.nodes:
    #     if e.x == ed.x and e.y == ed.y and e.z == ed.z:
    #         print("Identical Nodes found")

    n_nodes = len(ed_temp)
    pos_new = nodes_sorted.index(ed)
    wall.add_node(ed, recursive_add)
    if pos_new == 0:
        # raise RuntimeError("Node is at First Pos")
        next_edge = nodes_sorted[pos_new + 1]
        next_edge.connect(ed)
    elif pos_new == n_nodes - 1:
        # raise RuntimeError("Node is at Last Pos")
        prev_edge = nodes_sorted[pos_new - 1]
        prev_edge.connect(ed)
    else:
        prev_edge = nodes_sorted[pos_new - 1]
        next_edge = nodes_sorted[pos_new + 1]
        prev_edge.replace_connection(next_edge, ed)
        next_edge.connect(ed)
