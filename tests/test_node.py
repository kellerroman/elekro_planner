#!/usr/bin/env python3

from elektro_planner.data import Node
from pytest import approx

def test_node_connect():
    e1 = Node(1,2,3,None)
    e2 = Node(2,2,3,None)
    e3 = Node(3,2,3,None)
    e1.connect(e2)

    assert len(e1.edges) == 1
    assert e1.is_connected(e2)
    assert not e1.is_connected(e3)
    assert e1.get_connected_nodes()[0] == e2
    assert e1.edges[0].length == 1

def test_node_replace_connection():
    e1 = Node(1,2,3,None)
    e2 = Node(2,2,3,None)
    e3 = Node(3,2,3,None)
    e1.connect(e2)

    e1.replace_connection(e2,e3)
    assert len(e1.edges) == 1
    assert len(e2.edges) == 0
    assert len(e3.edges) == 1
    assert not e1.is_connected(e2)
    assert e1.is_connected(e3)
    assert e1.edges[0].node[1] == e3
    assert e1.edges[0].length == approx(2.0)

