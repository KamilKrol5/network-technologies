"""
@author: Kamil Król
"""

import networkx as nx
import random as rand
import matplotlib.pyplot as plt

# import os
# int.from_bytes(os.urandom(8), byteorder="big") / ((1 << 64) - 1)

reliability = 0.95
numberOfTests = 100000

options = {
    'node_color': 'red',
    'node_size': 600,
    'width': 3,
    'style': 'solid'
}


class Vertex:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "<%s>" % self.value

    def __repr__(self):
        return "<%s>" % self.value


# creating default graph
V = list()
for i in range(1, 21):
    V.insert(i - 1, Vertex(i))
E = list()
H = set()
for j in range(1, 20):
    e = (V[j - 1], V[j])
    E.insert(j - 1, e)
    H.add((e, reliability))

G = nx.MultiGraph()
G.add_nodes_from(V)
G.add_edges_from(E)


def prepare_graph_for_case1():
    edge = (V[0], V[19])
    G.add_edge(*edge)
    H.add((edge, reliability))


def prepare_graph_for_case2():
    edge1 = (V[0], V[9])
    G.add_edge(*edge1)
    H.add((edge1, 0.8))
    edge2 = (V[4], V[14])
    G.add_edge(*edge2)
    H.add((edge2, 0.7))


def prepare_graph_for_case3():
    for i in range(1, 5):
        edge1 = (V[rand.randint(0, 19)], V[rand.randint(0, 19)])
        G.add_edge(*edge1)
        H.add((edge1, 0.4))


# drawing and changing graphs
nx.draw(G, with_labels=True, font_weight='bold', **options)
plt.savefig("graph.png")
G0 = G.copy()
H0 = H.copy()
prepare_graph_for_case1()
plt.figure()
nx.draw_shell(G, with_labels=True, font_weight='bold', **options)
plt.savefig("graph1.png")
G1 = G.copy()
H1 = H.copy()
prepare_graph_for_case2()
plt.figure()
nx.draw_shell(G, with_labels=True, font_weight='bold', **options)
plt.savefig("graph2.png")
G2 = G.copy()
H2 = H.copy()
prepare_graph_for_case3()
plt.figure()
nx.draw_shell(G, with_labels=True, font_weight='bold', **options)
plt.savefig("graph3.png")
G3 = G
H3 = H
plt.show()


def test_reliability(tG, tH):
    # print(nx.is_connected(tG))
    numOfSuccesses = 0
    removedEdges = set()
    for i in range(numberOfTests):
        #        print(numOfSuccesses," num of edges: ",tG.number_of_edges())
        for func in tH:
            rando = rand.random()
            # print(rando)
            if func[1] <= rando:
                # tG.remove_edge(*func[0])
                removedEdges.add(func[0])
        # print("test%s: %s" % (i,nx.is_connected(tG)))
        tG.remove_edges_from(removedEdges)
        # filtered = nx.classes.graphviews.subgraph_view(tG, filter_edge=lambda x, y, _: (x, y) not in removedEdges)
        if nx.is_connected(tG):
            numOfSuccesses += 1
        tG.add_edges_from(removedEdges)
        removedEdges.clear()
        # print(nx.is_connected(tG))
    print(numOfSuccesses, " num of edges: ", tG.number_of_edges())
    return numOfSuccesses / numberOfTests


def run_tests():
    print(test_reliability(G0, H0))
    print(test_reliability(G1, H1))
    print(test_reliability(G2, H2))
    print(test_reliability(G3, H3))
