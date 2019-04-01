import networkx as nx
import matplotlib.pyplot as plt
import random as rand
from pprint import pprint

options = {
    'node_color': 'green',
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

    def __eq__(self, other):
        return isinstance(other, Vertex) and self.value == other.value

    def __hash__(self):
        return self.value


class Network:
    def __init__(self, nodes: dict, edges: list, n_matrix: list, avg_package_size=50, t_max=2):
        self.G = nx.Graph()
        self.G.add_nodes_from(nodes.values())
        self.G.add_edges_from(edges)
        self.edges = edges
        self.avg_package_size = avg_package_size
        self.n_matrix = n_matrix
        self.t_max = t_max
        self.update_a()
        self.number_of_tests = 100000

    def draw(self, label=None, filename=None, graph: nx.Graph = None):
        # plt.title(label=label, loc="left")
        graph_to_draw = graph or self.G
        pos = nx.spring_layout(graph_to_draw)
        nx.draw(graph_to_draw, pos=pos, with_labels=True, font_weight='bold', **options)
        if label is not None:
            nx.draw_networkx_edge_labels(graph_to_draw, pos=pos,
                                     edge_labels={(a, b): c[label] for a, b, c in graph_to_draw.edges.data()})
        if filename is not None:
            plt.savefig(filename)
        plt.show()

    def capacity(self, i, j):
        return self.G.get_edge_data(Vertex(i), Vertex(j))["capacity"]

    def a(self, i, j):
        return self.G.get_edge_data(Vertex(i), Vertex(j))["a"]

    def update_a(self):
        paths = dict(nx.all_pairs_shortest_path(self.G))
        for _, _, data in self.G.edges.data():
            data["a"] = 0
        for source, subdict in paths.items():
            for target, path in subdict.items():
                # if Vertex(i) in path and Vertex(j) in path:
                #     print(path)
                for ii in range(0, len(path) - 1):
                    self.G.get_edge_data(path[ii], path[ii + 1])["a"] += self.n_matrix[source.value][target.value]

    def average_delay(self, avg_size_of_package=None):
        m = avg_size_of_package or self.avg_package_size
        if not self.check_flows_correctness(m):
            print("Flows are incorrect.")
            return None
        sum_of_n = 0
        for row in self.n_matrix:
            sum_of_n += sum(row)
        sum_e = 0
        for node1, node2, attr in self.G.edges.data():
            a = self.a(node1.value, node2.value)
            sum_e += a / (self.capacity(node1.value, node2.value) / m - a)
        return 1 / sum_of_n * sum_e

    def test_reliability(self, preserve_the_same_a=False):
        num_of_successes = 0
        removed_edges = list()
        for i in range(self.number_of_tests):
            #        print(num_of_successes," num of edges: ",tG.number_of_edges())
            for data in self.G.edges.data():
                # print(data)
                rando = rand.random()
                # print(rando)
                if data[2]["probability"] <= rando:
                    removed_edges.append(data)
            self.G.remove_edges_from(removed_edges)
            self.update_a()
            if nx.is_connected(self.G) and self.check_flows_correctness() and self.average_delay() < self.t_max:
                num_of_successes += 1
            if preserve_the_same_a:
                self.G.remove_edges_from(self.edges)
                self.G.add_edges_from(self.edges)
            else:
                self.G.add_edges_from(removed_edges)
            self.update_a()
            removed_edges.clear()
        print("Number of successes", num_of_successes)
        return num_of_successes / self.number_of_tests

    def check_flows_correctness(self, avg_size_of_package=None):
        avg_size_of_package = avg_size_of_package or self.avg_package_size
        for v1, v2, data in self.G.edges.data():
            # print(data["capacity"], " < ", data["a"] * avg_size_of_package)
            if data["capacity"] <= data["a"] * avg_size_of_package:
                return False
        return True

    def show_edges_data(self):
        pprint(list(self.G.edges.data()))
