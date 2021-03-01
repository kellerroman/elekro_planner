
#!/usr/bin/env python3

from elektro_planner.data import Node, Haus
from elektro_planner.read_anschluesse import read_anschluesse
from elektro_planner.read_struktur import read_struktur
from elektro_planner.connect_walls import create_nodes_from_walls
from elektro_planner.associate_anschluesse import associate_objects_to_walls_and_nodes
from elektro_planner.read_kabel import autogenerate_kabel
from elektro_planner.calc_kabel import calc_kabel_len
import simple_haus
from pytest import approx
from math import sqrt
import astar

def test_astar():
    e1 = Node(100,200,100,None)
    e2 = Node(200,200,100,None)
    e3 = Node(300,200,100,None)
    e4 = Node(400,200,100,None)


    e1.connect(e2)
    e2.connect(e3)
    e3.connect(e4)

    def neighbors(n):
        for n1 in n.get_connected_nodes():
            yield n1

    def distance(n1, n2):
        for e in n1.edges:
            if e.get_con_node(n1) == n2:
                return e.length
    def cost(n, goal):
        return abs(n.x - goal.x)

    path = list(astar.find_path(e1, e4, neighbors_fnct=neighbors,
                heuristic_cost_estimate_fnct=cost, distance_between_fnct=distance))
    assert len(path) == 4
    assert path[0] == e1
    assert path[1] == e2
    assert path[2] == e3
    assert path[3] == e4

def test_astar():
    haus = Haus()
    yaml = simple_haus.define_testcase_simple1()

    read_struktur(haus,yaml["struktur"])
    read_anschluesse(haus,yaml["anschluesse"])
    create_nodes_from_walls(haus)
    associate_objects_to_walls_and_nodes(haus)
    autogenerate_kabel(haus)

    assert len(haus.kabel ) == 1

    path = calc_kabel_len(haus,haus.kabel[0])

    assert len(path) == 6

    for e in path:
        print("EDGE: {}".format(e))

    assert haus.kabel[0].length == approx((40+240+2*sqrt(10**2+30**2))*0.01)
