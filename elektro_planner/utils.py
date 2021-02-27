#!/usr/bin/env python3

def find_object(haus,cid):
    pos = cid.split(".")
    return haus.geschosse[int(pos[0])-1].rooms[int(pos[1])-1].objects[int(pos[2])-1]

def add_edge_to_wall(wall,ed):
    print("Wall {}, {} ".format(wall.id,wall.cid))

    ed_temp = [ed]
    for e in wall.edges:
        print("Edge z compare: {}:{}, {}:{}".format(e.id,e.z,ed.id,ed.z))
        if abs(e.z-ed.z) <= 5:
            ed_temp.append(e)
    if wall.waagrecht:
        # ed.y = wall.edges[0].y
        edges_sorted = sorted(ed_temp, key=lambda edge: edge.x)
    else:
        # ed.x = wall.edges[0].x
        edges_sorted = sorted(ed_temp, key=lambda edge: edge.y)

    n_edges = len(ed_temp)
    pos_new = edges_sorted.index(ed)
    if not pos_new < n_edges-1:
        raise RuntimeError("Edge is not in the Middle of the wall: len: {} Pos: {}".format(n_edges,pos_new))

    prev_edge = edges_sorted[pos_new-1]
    next_edge = edges_sorted[pos_new+1]
    prev_edge.connections = [ed if i==next_edge else i for i in prev_edge.connections]
    next_edge.connections = [ed if i==prev_edge else i for i in next_edge.connections]
    ed.connections.append(prev_edge)
    ed.connections.append(next_edge)
    # print(edges_sorted)
    wall.edges.append(ed)
    ed.n += 2


