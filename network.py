import networkx as nx
import matplotlib.pyplot as plt

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
        return "^%s^" % self.value

    def __repr__(self):
        return "^%s^" % self.value

    def __eq__(self, other):
        return isinstance(other, Vertex) and self.value == other.value

    def __hash__(self):
        return self.value


class Network:
    def __init__(self, nodes: dict, edges: list, n_matrix: list, avg_package_size=500):
        self.G = nx.Graph()
        self.G.add_nodes_from(nodes.values())
        self.G.add_edges_from(edges)
        self.avg_package_size = avg_package_size
        self.n_matrix = n_matrix
        paths = dict(nx.all_pairs_shortest_path(self.G))
        for _, _, data in self.G.edges.data():
            data["a"] = 0
        for subdict in paths.values():
            for path in subdict.values():
                # if Vertex(i) in path and Vertex(j) in path:
                #     print(path)
                for ii in range(0, len(path) - 1):
                    self.G.get_edge_data(path[ii], path[ii + 1])["a"] += 1

    def draw(self):
        nx.draw(self.G, with_labels=True, font_weight='bold', **options)
        plt.show()

    def capacity(self, i, j):
        return self.G.get_edge_data(Vertex(i), Vertex(j))["capacity"]

    def a(self, i, j):

        return self.G.get_edge_data(Vertex(i), Vertex(j))["a"]

    def average_delay(self, avg_size_of_package=None):
        m = avg_size_of_package or self.avg_package_size
        sum_of_n = 0
        for row in self.N:
            sum_of_n += sum(row)
        sum_e = 0
        for node1, node2, attr in self.G.edges.data():
            a = self.a(node1.value, node2.value)
            sum_e += a / (self.c(node1.value, node2.value) / m - a)
        return 1 / sum_of_n * sum_e
