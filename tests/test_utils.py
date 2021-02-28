
#!/usr/bin/env python3

from elektro_planner.utils import add_node_to_wall
from elektro_planner.data import Node, Wall
from pytest import approx

def test_add_node_to_wall():
    class Parent:
        def __init__(self):
            self.cid = 1
        def add_node(self,node):
            pass
    p = Parent()
    w = Wall( {'id': 1, 'pos': {'hori': [25, 0]}, 'ende': [36.5, 324]}, p)
    e1 = Node(100,200,100,None)
    e2 = Node(300,200,100,None)
    e3 = Node(100,200,300,None)
    e4 = Node(300,200,300,None)

    w.add_nodes([e1,e2,e3,e4],False)

    assert len(w.nodes) == 4

    e1.connect(e2)

    e5 = Node(200,200,100,None)
    add_node_to_wall(w,e5)

    assert len(w.nodes) == 5
    assert len(e1.edges) == 1
    assert len(e2.edges) == 1
    assert len(e5.edges) == 2
    assert e5.is_connected(e1)
    assert e5.is_connected(e2)






