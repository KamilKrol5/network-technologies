"""
@author: Kamil Król
"""
import networkx as nx
# import random as rand
import matplotlib.pyplot as plt
import task2 as t2

options = {
    'node_color': 'red',
    'node_size': 500,
    'width': 3,
    'style': 'solid'
}


class Vertex:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{{{self.value}}}"

    def __repr__(self):
        return "{%s}" % self.value

    def __hash__(self):
        return self.value


# creating vertexes
V = {i: Vertex(i) for i in range(0, 10)}

# creating edges
E = dict()

C = dict()
A = dict()


def create_edges():
    C[(V[0], V[4])] = 1000
    C[(V[0], V[6])] = 500
    C[(V[0], V[2])] = 1500
    C[(V[1], V[5])] = 5000
    C[(V[1], V[7])] = 1800
    C[(V[1], V[8])] = 800
    C[(V[1], V[2])] = 5000
    C[(V[2], V[4])] = 3000
    C[(V[2], V[3])] = 4000
    C[(V[3], V[7])] = 1300
    C[(V[3], V[6])] = 1400
    C[(V[4], V[9])] = 3900
    C[(V[4], V[5])] = 4100
    C[(V[5], V[9])] = 1000
    C[(V[5], V[8])] = 3400
    C[(V[8], V[9])] = 2100
    for edge in C.keys():
        E[(edge[0].value, edge[1].value)] = edge


create_edges()
# creating function set
H = set()  # = A + C
N = [  # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9| 10
    [0, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # 0
    [1, 0, 1, 2, 3, 1, 1, 1, 1, 1],  # 1
    [1, 2, 0, 3, 4, 1, 1, 1, 2, 3],  # 2
    [1, 1, 1, 0, 1, 1, 1, 1, 3, 3],  # 3
    [1, 2, 1, 1, 0, 1, 1, 1, 1, 1],  # 4
    [2, 2, 2, 1, 1, 0, 2, 1, 1, 1],  # 5
    [4, 3, 1, 1, 1, 1, 0, 2, 3, 1],  # 6
    [1, 5, 1, 4, 4, 1, 1, 0, 2, 1],  # 7
    [1, 0, 1, 2, 3, 4, 1, 1, 0, 1],  # 8
    [2, 3, 1, 1, 2, 3, 1, 1, 1, 0]   # 9
]

my_web = t2.Web(V, E, C, N)
