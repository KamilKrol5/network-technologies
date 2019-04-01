import networkx as nx
# import random as rand
import matplotlib.pyplot as plt
import network as ntw

V = {i: ntw.Vertex(i) for i in range(0, 10)}
E = [(V[0], V[4], {"probability": 0.97, "capacity": 1300}),
     (V[0], V[6], {"probability": 0.97, "capacity": 1500}),
     (V[0], V[2], {"probability": 0.97, "capacity": 1500}),
     (V[1], V[5], {"probability": 0.97, "capacity": 5000}),
     (V[1], V[7], {"probability": 0.97, "capacity": 1800}),
     (V[1], V[8], {"probability": 0.97, "capacity": 1500}),
     (V[1], V[2], {"probability": 0.97, "capacity": 5000}),
     (V[2], V[4], {"probability": 0.97, "capacity": 3000}),
     (V[2], V[3], {"probability": 0.97, "capacity": 4000}),
     (V[3], V[7], {"probability": 0.97, "capacity": 1300}),
     (V[3], V[6], {"probability": 0.97, "capacity": 1400}),
     (V[4], V[9], {"probability": 0.97, "capacity": 3900}),
     (V[4], V[5], {"probability": 0.97, "capacity": 4100}),
     (V[5], V[9], {"probability": 0.97, "capacity": 1000}),
     (V[5], V[8], {"probability": 0.97, "capacity": 3400}),
     (V[8], V[9], {"probability": 0.97, "capacity": 2100})]

N = \
    [
        # 0| 1| 2| 3| 4| 5| 6| 7| 8| 9| 10
        [0, 2, 2, 2, 2, 2, 2, 2, 2, 2],  # 0
        [1, 0, 1, 2, 3, 1, 1, 1, 1, 1],  # 1
        [1, 2, 0, 3, 4, 1, 1, 1, 2, 3],  # 2
        [1, 1, 1, 0, 1, 1, 1, 1, 3, 3],  # 3
        [1, 2, 1, 1, 0, 1, 1, 1, 1, 1],  # 4
        [2, 2, 2, 1, 1, 0, 2, 1, 1, 1],  # 5
        [4, 3, 1, 1, 1, 1, 0, 2, 3, 1],  # 6
        [1, 5, 1, 4, 4, 1, 1, 0, 2, 1],  # 7
        [1, 0, 1, 2, 3, 4, 1, 1, 0, 1],  # 8
        [2, 3, 1, 1, 2, 3, 1, 1, 1, 0]  # 9
    ]

E_dense = [
    (V[0], V[4], {"probability": 0.3, "capacity": 1300}),
    (V[0], V[6], {"probability": 0.3, "capacity": 5000}),
    (V[0], V[2], {"probability": 0.3, "capacity": 5000}),
    (V[1], V[5], {"probability": 0.3, "capacity": 5000}),
    (V[1], V[7], {"probability": 0.3, "capacity": 5000}),
    (V[1], V[8], {"probability": 0.3, "capacity": 5000}),
    (V[1], V[2], {"probability": 0.3, "capacity": 5000}),
    (V[2], V[4], {"probability": 0.3, "capacity": 5000}),
    (V[2], V[3], {"probability": 0.3, "capacity": 5000}),
    (V[3], V[7], {"probability": 0.3, "capacity": 5000}),
    (V[3], V[6], {"probability": 0.3, "capacity": 5000}),
    (V[4], V[9], {"probability": 0.3, "capacity": 5000}),
    (V[4], V[5], {"probability": 0.3, "capacity": 5000}),
    (V[5], V[9], {"probability": 0.3, "capacity": 5000}),
    (V[5], V[8], {"probability": 0.3, "capacity": 5000}),
    (V[8], V[9], {"probability": 0.3, "capacity": 5000}),
    (V[1], V[6], {"probability": 0.3, "capacity": 5000}),
    (V[0], V[5], {"probability": 0.3, "capacity": 5000}),
    (V[1], V[3], {"probability": 0.3, "capacity": 5000}),
    (V[1], V[4], {"probability": 0.3, "capacity": 5000}),
    (V[3], V[4], {"probability": 0.3, "capacity": 5000}),
    (V[2], V[8], {"probability": 0.3, "capacity": 5000}),
    (V[3], V[8], {"probability": 0.3, "capacity": 5000}),
    (V[3], V[9], {"probability": 0.3, "capacity": 5000}),
    (V[4], V[6], {"probability": 0.3, "capacity": 5000}),
    (V[7], V[9], {"probability": 0.3, "capacity": 5000}),
]

E_complete = list()
for j in range(0, len(V)):
    for i in range(0, len(V)):
        if i != j:
            E_complete.append((V[i], V[j], {"probability": 0.3, "capacity": 5000}))

n1 = ntw.Network(V, E_dense, N)
n2 = ntw.Network(V, E_complete, N)
# n1.draw(filename="dense_graph.png")
# n2.draw()

